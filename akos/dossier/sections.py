"""Initiative 48 P1 — Section ABC + 12 subclasses (skeleton).

Each Section subclass implements 4 methods per dossier-section-spec.md:
- gather(mode, filter) -> SectionData      (data fetch)
- render_markdown(data) -> str             (markdown body)
- render_html(data) -> str                 (HTML body wrapped in <details>)
- metrics_for_trend(data) -> dict          (P7 trend storage)

Section ordering (D-IH-48-D) is enforced by SECTION_CLASSES tuple — subclasses
must appear in 1..12 order. tests/test_dossier_sections.py asserts this.

P1 ships SKELETON subclasses with PLACEHOLDER text per dossier-section-spec.md
PLACEHOLDER contract; data sources land in P2 (sources.py) and onwards.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from akos.dossier.run import DossierFilter, DossierSectionResult


@dataclass
class SectionData:
    """Generic per-section data container. Subclasses may store anything in payload."""

    payload: dict[str, Any] = field(default_factory=dict)
    data_age_seconds: float | None = None
    placeholder: bool = False
    error: str = ""


class Section(ABC):
    """Abstract base for all 12 dossier sections.

    Per D-IH-48-D, section_id is fixed 1..12 and ordering is invariant across
    modes. Subclasses set ``section_id``, ``name``, ``default_open_html`` as
    class attributes.
    """

    section_id: int = 0
    name: str = "abstract"
    default_open_html: bool = False
    staleness_threshold_hours: int | None = 24  # D-IH-48-E; None = never re-fetch (Section 6)

    @abstractmethod
    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        """Fetch the data. Mode-aware (snapshot reads cache; live re-runs)."""
        raise NotImplementedError

    @abstractmethod
    def render_markdown(self, data: SectionData) -> str:
        """Emit markdown body. Must include `## Section <id> — <Name>` header."""
        raise NotImplementedError

    def render_html(self, data: SectionData) -> str:
        """Emit HTML body wrapped in <details> per D-IH-48-I.

        Default implementation wraps render_markdown() in a <details> block;
        P5 will replace this with a richer brand-CSS-styled implementation
        that renders the markdown body via the markdown library.
        """
        from akos.dossier.html_render import section_to_html_details
        return section_to_html_details(
            section_id=self.section_id,
            name=self.name,
            markdown_body=self.render_markdown(data),
            default_open=self.default_open_html,
        )

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        """Emit per-section metrics for compliance.dossier_run.section_metrics JSONB.

        Default returns empty dict; subclasses override per dossier-section-spec.md.
        """
        return {}

    def execute(self, mode: str, filter: DossierFilter | None = None) -> DossierSectionResult:
        """Convenience wrapper: gather + render markdown + compute metrics."""
        try:
            data = self.gather(mode, filter)
        except Exception as exc:  # pragma: no cover - defensive (R-48-1)
            data = SectionData(placeholder=True, error=str(exc)[:300])
        try:
            md = self.render_markdown(data)
        except Exception as exc:  # pragma: no cover
            md = _placeholder_markdown(self.section_id, self.name,
                                       f"render_markdown crashed: {exc!r}")
            data.placeholder = True
            data.error = str(exc)[:300]
        try:
            metrics = self.metrics_for_trend(data)
        except Exception:  # pragma: no cover
            metrics = {}
        status = self._infer_status(data)
        return DossierSectionResult(
            section_id=self.section_id,
            name=self.name,
            status=status,
            markdown=md,
            html="",  # html rendered separately when format requested
            metrics=metrics,
            data_age_seconds=data.data_age_seconds,
            placeholder=data.placeholder,
            error=data.error,
        )

    def _infer_status(self, data: SectionData) -> str:
        """Default status inference. Subclasses override for richer logic."""
        if data.placeholder:
            return "SKIP"
        return data.payload.get("status", "PASS")


# ──────────────────────────────────────────────────────────────────────────────
# PLACEHOLDER text contract (dossier-section-spec.md)
# ──────────────────────────────────────────────────────────────────────────────


def _placeholder_markdown(section_id: int, name: str, reason: str) -> str:
    return (
        f"## Section {section_id} — {name}\n"
        f"\n"
        f"> [STALE / UNAVAILABLE] {reason}\n"
        f"> Run `py scripts/render_uat_dossier.py --mode live` to refresh this section.\n"
    )


def _section_header(section_id: int, name: str) -> str:
    return f"## Section {section_id} — {name}"


# ──────────────────────────────────────────────────────────────────────────────
# Section 01 — Executive summary (computed last; rendered first)
# ──────────────────────────────────────────────────────────────────────────────


class Section01ExecutiveSummary(Section):
    section_id = 1
    name = "Executive summary"
    default_open_html = True
    staleness_threshold_hours = 0  # always re-aggregated

    def gather(self, mode: str, filter: DossierFilter | None = None,
               prior_results: list[DossierSectionResult] | None = None) -> SectionData:
        """Compute outcome from prior section results (Sections 2-12).

        Per dossier-section-spec.md: Section 1 is computed LAST (after all
        other sections have gathered) but rendered FIRST. The orchestrator
        passes ``prior_results`` containing the other 11 section outputs.
        """
        if not prior_results:
            return SectionData(
                payload={
                    "outcome": "PASS",
                    "section_count": 12,
                    "fail_count": 0,
                    "skip_count": 0,
                    "warn_count": 0,
                    "cost_total_usd": 0.0,
                    "status": "PASS",
                },
            )
        fails = sum(1 for r in prior_results if r.status == "FAIL")
        warns = sum(1 for r in prior_results if r.status == "WARN")
        skips = sum(1 for r in prior_results if r.status == "SKIP")
        infos = sum(1 for r in prior_results if r.status == "INFO")
        passes = sum(1 for r in prior_results if r.status == "PASS")
        cost_total = 0.0
        for r in prior_results:
            cost = r.metrics.get("cost_total_usd")
            if isinstance(cost, (int, float)):
                cost_total += float(cost)
        outcome = "FAIL" if fails > 0 else ("WARN" if warns > 0 else "PASS")
        # Per-section-status table for the executive summary body
        section_table = [
            {"id": r.section_id, "name": r.name,
             "status": r.status,
             "data_age_hours": (r.data_age_seconds / 3600.0) if r.data_age_seconds is not None else None}
            for r in sorted(prior_results, key=lambda x: x.section_id)
        ]
        return SectionData(
            payload={
                "outcome": outcome,
                "section_count": len(prior_results) + 1,
                "fail_count": fails,
                "warn_count": warns,
                "skip_count": skips,
                "info_count": infos,
                "pass_count": passes,
                "cost_total_usd": cost_total,
                "section_table": section_table,
                "status": outcome if outcome != "WARN" else "PASS",
            },
        )

    def render_markdown(self, data: SectionData) -> str:
        if data.placeholder:
            return _placeholder_markdown(self.section_id, self.name,
                                         data.error or "executive summary unavailable")
        p = data.payload
        outcome = p.get("outcome", "?")
        lines = [
            _section_header(self.section_id, self.name),
            "",
            f"**Outcome: {outcome}**",
            "",
            f"- sections aggregated: {p.get('section_count', 0)}",
            f"- FAIL count: {p.get('fail_count', 0)}",
            f"- WARN count: {p.get('warn_count', 0)}",
            f"- SKIP count: {p.get('skip_count', 0)}",
            f"- INFO count: {p.get('info_count', 0)}",
            f"- PASS count: {p.get('pass_count', 0)}",
            f"- cost_total_usd: ${p.get('cost_total_usd', 0.0):.4f}",
        ]
        section_table = p.get("section_table")
        if section_table:
            lines.append("")
            lines.append("| section | name | status | age (h) |")
            lines.append("|:--:|:---|:--:|:--:|")
            for row in section_table:
                age = row.get("data_age_hours")
                age_str = f"{age:.1f}" if isinstance(age, (int, float)) else "-"
                lines.append(
                    f"| {row['id']} | {row['name']} | {row['status']} | {age_str} |"
                )
        return "\n".join(lines) + "\n"

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        p = data.payload
        return {
            "overall_status_pass": (p.get("outcome") == "PASS"),
            "section_count": p.get("section_count", 0),
            "fail_count": p.get("fail_count", 0),
            "warn_count": p.get("warn_count", 0),
            "skip_count": p.get("skip_count", 0),
            "cost_total_usd": float(p.get("cost_total_usd", 0.0)),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Section 02 — Schema + governance
# ──────────────────────────────────────────────────────────────────────────────


class Section02SchemaGovernance(Section):
    section_id = 2
    name = "Schema + governance"
    default_open_html = True
    staleness_threshold_hours = 12

    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        from akos.dossier.sources import gather_schema_governance
        return gather_schema_governance()

    def render_markdown(self, data: SectionData) -> str:
        if data.placeholder:
            return _placeholder_markdown(self.section_id, self.name,
                                         data.error or "validate_hlk not yet wired")
        p = data.payload
        validate_status = p.get("validate_hlk_pass")
        validate_label = (
            "PASS" if validate_status is True else
            "FAIL" if validate_status is False else
            "(snapshot mode; live mode invokes validate_hlk)"
        )
        return (
            f"{_section_header(self.section_id, self.name)}\n"
            f"\n"
            f"- validate_hlk: {validate_label}\n"
            f"- topics: {p.get('total_topics', 0)}\n"
            f"- skills: {p.get('total_skills', 0)}\n"
            f"- policies: {p.get('total_policies', 0)}\n"
            f"- personas: {p.get('total_personas', 0)}\n"
            f"- scenarios: {p.get('total_scenarios', 0)}\n"
        )

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        p = data.payload
        return {
            "validate_hlk_pass": p.get("validate_hlk_pass", False),
            "total_topics": p.get("total_topics", 0),
            "total_skills": p.get("total_skills", 0),
            "total_policies": p.get("total_policies", 0),
            "total_personas": p.get("total_personas", 0),
            "total_scenarios": p.get("total_scenarios", 0),
            "pre_existing_failures_count": p.get("pre_existing_failures_count", 0),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Section 03 — Eval health
# ──────────────────────────────────────────────────────────────────────────────


class Section03EvalHealth(Section):
    section_id = 3
    name = "Eval health"
    default_open_html = True
    staleness_threshold_hours = 12

    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        from akos.dossier.sources import gather_eval_health_snapshot
        return gather_eval_health_snapshot()

    def render_markdown(self, data: SectionData) -> str:
        if data.placeholder:
            return _placeholder_markdown(self.section_id, self.name,
                                         data.error or "eval Scorecard not yet wired")
        return (
            f"{_section_header(self.section_id, self.name)}\n"
            f"\n"
            + str(data.payload.get("scorecard_markdown", "(no scorecard)"))
        )

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        p = data.payload
        return {
            "eval_overall_status_pass": p.get("overall_status") == "pass",
            "rows_total": p.get("rows_total", 0),
            "rows_passed": p.get("rows_passed", 0),
            "rows_failed": p.get("rows_failed", 0),
            "judge_score_brand_voice_mean": p.get("judge_brand_voice_mean"),
            "judge_score_citation_mean": p.get("judge_citation_mean"),
            "judge_score_persona_fit_mean": p.get("judge_persona_fit_mean"),
            "cost_total_usd": float(p.get("cost_total_usd", 0.0)),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Section 04 — Persona library + calibration
# ──────────────────────────────────────────────────────────────────────────────


class Section04PersonaCalibration(Section):
    section_id = 4
    name = "Persona library + calibration"
    default_open_html = True
    staleness_threshold_hours = 24

    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        from akos.dossier.sources import gather_persona_calibration
        return gather_persona_calibration()

    def render_markdown(self, data: SectionData) -> str:
        if data.placeholder:
            return _placeholder_markdown(self.section_id, self.name,
                                         data.error or "calibration not yet wired")
        p = data.payload
        return (
            f"{_section_header(self.section_id, self.name)}\n"
            f"\n"
            f"- total scenarios: {p.get('total_scenarios', 0)}\n"
            f"- total personas: {p.get('total_personas', 0)}\n"
            f"- overall within tolerance: {p.get('overall_within_tolerance', False)}\n"
        )

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        p = data.payload
        return {
            "total_scenarios": p.get("total_scenarios", 0),
            "total_personas": p.get("total_personas", 0),
            "overall_within_tolerance": p.get("overall_within_tolerance", False),
            "personas_outside_tolerance_count": p.get("personas_outside_tolerance_count", 0),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Section 05 — Adversarial coverage
# ──────────────────────────────────────────────────────────────────────────────


class Section05Adversarial(Section):
    section_id = 5
    name = "Adversarial coverage"
    default_open_html = True
    staleness_threshold_hours = 24

    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        return SectionData(placeholder=True,
                           error="P1 skeleton; eval --mode adversarial wiring lands in P2")

    def render_markdown(self, data: SectionData) -> str:
        if data.placeholder:
            return _placeholder_markdown(self.section_id, self.name,
                                         data.error or "adversarial sweep not yet wired")
        p = data.payload
        return (
            f"{_section_header(self.section_id, self.name)}\n"
            f"\n"
            f"- adversarial PASS count: {p.get('adversarial_pass_count', 0)}\n"
            f"- adversarial FAIL count: {p.get('adversarial_fail_count', 0)}\n"
            f"- pii_linter_clean: {p.get('pii_linter_clean', True)}\n"
        )

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        p = data.payload
        return {
            "adversarial_pass_count": p.get("adversarial_pass_count", 0),
            "adversarial_fail_count": p.get("adversarial_fail_count", 0),
            "pii_linter_clean": p.get("pii_linter_clean", True),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Section 06 — Recovery + chaos
# ──────────────────────────────────────────────────────────────────────────────


class Section06Recovery(Section):
    section_id = 6
    name = "Recovery + chaos"
    default_open_html = False  # collapsed by default
    staleness_threshold_hours = None  # NEVER auto-refresh (read latest artifact)

    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        from akos.dossier.sources import gather_recovery_chaos
        return gather_recovery_chaos()

    def render_markdown(self, data: SectionData) -> str:
        if data.placeholder:
            return _placeholder_markdown(self.section_id, self.name,
                                         data.error or "chaos artifacts not yet read")
        p = data.payload
        return (
            f"{_section_header(self.section_id, self.name)}\n"
            f"\n"
            f"- synthetic recovery PASS count (out of 15): {p.get('synthetic_recovery_pass_count', 0)}\n"
            f"- real-chaos last run status: {p.get('real_chaos_last_run_status', 'never')}\n"
        )

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        p = data.payload
        return {
            "synthetic_recovery_pass_count": p.get("synthetic_recovery_pass_count", 0),
            "real_chaos_last_run_status": p.get("real_chaos_last_run_status"),
            "real_chaos_gates_passed": p.get("real_chaos_gates_passed"),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Section 07 — Drift canaries
# ──────────────────────────────────────────────────────────────────────────────


class Section07DriftCanaries(Section):
    section_id = 7
    name = "Drift canaries"
    default_open_html = True
    staleness_threshold_hours = 24

    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        return SectionData(placeholder=True,
                           error="P1 skeleton; drift canary + mirror staleness wiring lands in P2")

    def render_markdown(self, data: SectionData) -> str:
        if data.placeholder:
            return _placeholder_markdown(self.section_id, self.name,
                                         data.error or "drift canary not yet wired")
        p = data.payload
        return (
            f"{_section_header(self.section_id, self.name)}\n"
            f"\n"
            f"- total drift: {p.get('drift_canary_total_drift', 0)}\n"
            f"- mirrors stale (>7d): {p.get('mirrors_stale_count', 0)}\n"
        )

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        p = data.payload
        return {
            "drift_canary_total_drift": p.get("drift_canary_total_drift", 0),
            "mirror_oldest_age_seconds": p.get("mirror_oldest_age_seconds"),
            "mirrors_stale_count": p.get("mirrors_stale_count", 0),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Section 08 — Operational health
# ──────────────────────────────────────────────────────────────────────────────


class Section08OperationalHealth(Section):
    section_id = 8
    name = "Operational health"
    default_open_html = False  # collapsed by default
    staleness_threshold_hours = 12

    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        from akos.dossier.sources import gather_operational_health
        return gather_operational_health()

    def render_markdown(self, data: SectionData) -> str:
        if data.placeholder:
            return _placeholder_markdown(self.section_id, self.name,
                                         data.error or "operational health sources not yet wired")
        p = data.payload
        return (
            f"{_section_header(self.section_id, self.name)}\n"
            f"\n"
            f"- agent memory triggers fired: {p.get('agent_memory_triggers_fired', 0)}\n"
            f"- cost ceiling breaches: {p.get('cost_ceiling_breaches_count', 0)}\n"
            f"- promotion gate PASS count (of 5): {p.get('promotion_gate_pass_count', 0)}\n"
        )

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        p = data.payload
        return {
            "agent_memory_triggers_fired": p.get("agent_memory_triggers_fired", 0),
            "cost_ceiling_breaches_count": p.get("cost_ceiling_breaches_count", 0),
            "promotion_gate_pass_count": p.get("promotion_gate_pass_count", 0),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Section 09 — External repo health
# ──────────────────────────────────────────────────────────────────────────────


class Section09ExternalRepos(Section):
    section_id = 9
    name = "External repo health"
    default_open_html = False  # collapsed by default
    staleness_threshold_hours = 7 * 24  # weekly cadence

    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        from akos.dossier.sources import gather_external_repos
        return gather_external_repos()

    def render_markdown(self, data: SectionData) -> str:
        if data.placeholder:
            return _placeholder_markdown(self.section_id, self.name,
                                         data.error or "REPO_HEALTH_SNAPSHOT not yet read")
        p = data.payload
        return (
            f"{_section_header(self.section_id, self.name)}\n"
            f"\n"
            f"- repos tracked: {p.get('repos_tracked', 0)}\n"
            f"- contracts present: {p.get('contracts_present_count', 0)}\n"
        )

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        p = data.payload
        return {
            "repos_tracked": p.get("repos_tracked", 0),
            "contracts_present_count": p.get("contracts_present_count", 0),
            "consecutive_weeks_regression": p.get("consecutive_weeks_regression", 0),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Section 10 — Open governance debt
# ──────────────────────────────────────────────────────────────────────────────


class Section10GovernanceDebt(Section):
    section_id = 10
    name = "Open governance debt"
    default_open_html = True
    staleness_threshold_hours = 0  # always re-parse

    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        from akos.dossier.sources import gather_governance_debt
        return gather_governance_debt(initiative_filter=(filter.initiative if filter else None))

    def render_markdown(self, data: SectionData) -> str:
        if data.placeholder:
            return _placeholder_markdown(self.section_id, self.name,
                                         data.error or "OPS-* parser not yet wired")
        p = data.payload
        return (
            f"{_section_header(self.section_id, self.name)}\n"
            f"\n"
            f"- open OPS-* total: {p.get('open_ops_count_total', 0)}\n"
            f"- oldest open OPS age (days): {p.get('oldest_open_ops_age_days', 0)}\n"
        )

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        p = data.payload
        return {
            "open_ops_count_total": p.get("open_ops_count_total", 0),
            "oldest_open_ops_age_days": p.get("oldest_open_ops_age_days", 0),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Section 11 — Trend lines (P7 consumer)
# ──────────────────────────────────────────────────────────────────────────────


class Section11TrendLines(Section):
    section_id = 11
    name = "Trend lines"
    default_open_html = True
    staleness_threshold_hours = 0  # always re-query

    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        # P1 skeleton: emits INSUFFICIENT-DATA placeholder until P7 wires sparklines.
        return SectionData(payload={"insufficient_data": True}, placeholder=False)

    def render_markdown(self, data: SectionData) -> str:
        from akos.dossier.sparkline import INSUFFICIENT_DATA_PLACEHOLDER
        p = data.payload
        if p.get("insufficient_data"):
            return (
                f"{_section_header(self.section_id, self.name)}\n"
                f"\n"
                f"{INSUFFICIENT_DATA_PLACEHOLDER}\n"
                f"\n"
                f"_Sparklines render starting at run #2 (this is run #1 OR mirror is unreachable)._\n"
            )
        sparklines: dict[str, str] = p.get("sparklines", {})
        lines = [f"{_section_header(self.section_id, self.name)}", ""]
        for metric, svg in sparklines.items():
            lines.append(f"### {metric}")
            lines.append("")
            lines.append(svg)
            lines.append("")
        return "\n".join(lines)

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        # Section 11 CONSUMES trend metrics; emits none.
        return {}

    def _infer_status(self, data: SectionData) -> str:
        return "INFO"


# ──────────────────────────────────────────────────────────────────────────────
# Section 12 — Appendix
# ──────────────────────────────────────────────────────────────────────────────


class Section12Appendix(Section):
    section_id = 12
    name = "Appendix"
    default_open_html = False  # collapsed by default
    staleness_threshold_hours = 0  # always emitted

    def gather(self, mode: str, filter: DossierFilter | None = None) -> SectionData:
        return SectionData(payload={"emitted_at_end": True})

    def render_markdown(self, data: SectionData) -> str:
        p = data.payload
        return (
            f"{_section_header(self.section_id, self.name)}\n"
            f"\n"
            f"_Run config + sha256 manifest + raw artifact paths are written to "
            f"`manifest.json` alongside this dossier._\n"
            f"\n"
            f"- run config: see manifest.json `run_id`, `mode`, `formats`, `filter`\n"
            f"- per-section data sources: see manifest.json `section_metrics`\n"
            f"- sha256 hashes: see manifest.json `files.{{dossier.md, dossier.pdf, dossier.html}}.sha256`\n"
            f"- raw artifact paths: under `artifacts/uat-dossier/uat-dossier-<UTC>/`\n"
        )

    def metrics_for_trend(self, data: SectionData) -> dict[str, Any]:
        return {}

    def _infer_status(self, data: SectionData) -> str:
        return "INFO"


# ──────────────────────────────────────────────────────────────────────────────
# Section ordering invariant (D-IH-48-D)
# ──────────────────────────────────────────────────────────────────────────────


SECTION_CLASSES: tuple[type[Section], ...] = (
    Section01ExecutiveSummary,
    Section02SchemaGovernance,
    Section03EvalHealth,
    Section04PersonaCalibration,
    Section05Adversarial,
    Section06Recovery,
    Section07DriftCanaries,
    Section08OperationalHealth,
    Section09ExternalRepos,
    Section10GovernanceDebt,
    Section11TrendLines,
    Section12Appendix,
)
