#!/usr/bin/env python3
"""Per-tranche synthesis sweep runbook (14th Quality Fabric specialty).

Canonical doctrine:
  ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/``
  ``SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md``
Pydantic SSOT:
  ``akos/hlk_synthesis_before_tranche.py``
Paired validator:
  ``scripts/validate_synthesis_before_tranche.py``
Cursor rule (Commit 2c-a):
  ``.cursor/rules/akos-synthesis-before-tranche.mdc``
Skill (Commit 2c-a):
  ``.cursor/skills/synthesis-before-tranche-craft/SKILL.md``
SOP (Commit 2c-a):
  ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/``
  ``SOP-PEOPLE_SYNTHESIS_BEFORE_TRANCHE_001.md``
Decision lineage:
  D-IH-86-EA (doctrine mint + INFO ramp),
  D-IH-86-EB (10-dimension probe set ratification),
  D-IH-86-EC (5-option disposition enum + per-tranche-class firing),
  D-IH-86-ED (broad-fire posture with INFO ramp).

The runbook is the operator-facing entry point to the doctrine's
``compose_SYNTHESIS()`` function. Given a tranche charter (YAML
frontmatter + body) describing the work the operator + agent are about
to commit, the runbook:

  1. Reads the charter's tranche_class + audiences_named + channels_named
     + scenarios_named + ratifying_decisions + reversibility_class +
     closing_loop_test + erp_surface_citations.

  2. Resolves the per-tranche-class fire-set via
     ``akos.hlk_synthesis_before_tranche.resolve_fire_set()``.

  3. Walks each fired dimension and emits a synthesis report row with
     status (PASS / WARN / FAIL / INFO / N/A) + recommended disposition
     (scope-complete / scope-extend / scope-narrow / defer-OPS /
     escalate-to-blocker-tracker).

  4. Writes the synthesis report at
     ``docs/wip/planning/86-initiative-cluster-execution-coordinator/``
     ``reports/synthesis-check-<tranche_id>-<YYYY-MM-DD>.md``
     (or under the parent initiative's reports/ folder when the tranche
     is engagement-scoped per ``akos-planning-traceability.mdc``).

  5. Surfaces any FAIL / WARN findings to stdout so the operator + agent
     can disposition before commit.

Per D-IH-86-ED INFO ramp: at mint, the dimension checks live mostly in
the agent + operator's heads via the cursor rule + skill (the *how*
layer). The runbook's primary job at INFO is the always-on chassis
self-test (mirroring the COLLABORATOR_SHARE precedent) + a charter-shape
verification entry point. Per-dimension automated probes (e.g., audience
FK resolution against AUDIENCE_REGISTRY; brand-register scan;
recipient-fallback-channel cross-check against CHANNEL_TOUCHPOINT_REGISTRY)
land incrementally as engagement charters surface real failure modes.

CLI shape::

    py scripts/synthesis_before_tranche_check.py --self-test

    py scripts/synthesis_before_tranche_check.py \\
        --check-charter docs/wip/planning/86-.../tranches/p3-commit2b.md

    py scripts/synthesis_before_tranche_check.py \\
        --tranche-id "Wave-S-Commit-1" \\
        --tranche-class specialty_mint \\
        --audiences "J-OP" \\
        --ratifying-decisions "D-IH-86-EA" \\
        --reversibility medium \\
        --closing-loop-test "validate_*.py --self-test PASS"

Per ``akos-executable-process-catalog.mdc`` Rule 1: this runbook is the
AC-AUTOMATION half of the SOP+runbook pair. The SOP (Commit 2c-a) carries
the AC-HUMAN narrative + operator walkthrough.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import logging
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_synthesis_before_tranche import (  # noqa: E402
    DIMENSION_DESCRIPTIONS,
    DIMENSION_FIRE_RULES,
    DIMENSION_SEVERITY_CLASS,
    VALID_DIMENSION_CODES,
    VALID_TRANCHE_CLASSES,
    SynthesisFindingRow,
    SynthesisReportSummary,
    SynthesisTrancheCharter,
    resolve_fire_set,
)

logger = logging.getLogger(__name__)

REPORTS_DIR_DEFAULT = (
    REPO_ROOT
    / "docs"
    / "wip"
    / "planning"
    / "86-initiative-cluster-execution-coordinator"
    / "reports"
)


def _today() -> str:
    return _dt.date.today().isoformat()


def _slug(s: str) -> str:
    """Lowercase + hyphen + alphanum-only slug for filenames."""
    return re.sub(r"[^a-z0-9-]+", "-", s.lower()).strip("-")


def _parse_yaml_frontmatter(text: str) -> dict[str, Any]:
    """Minimal YAML-ish frontmatter parser (no external deps).

    Supports the subset needed for SynthesisTrancheCharter fixtures:
    - top-level ``key: value`` pairs (strings + ints + bools)
    - list values formatted as ``key: [a, b, c]`` or
      bullet-list under ``key:`` with ``  - item`` lines
    - YAML frontmatter delimited by leading ``---`` and trailing ``---``.

    For more complex schemas, replace with PyYAML when it lands in the
    repo's dependency tree.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    body = text[4:end].strip("\n")
    out: dict[str, Any] = {}
    current_list_key: str | None = None
    current_list: list[Any] = []

    def _flush_list() -> None:
        nonlocal current_list_key, current_list
        if current_list_key:
            out[current_list_key] = current_list
        current_list_key = None
        current_list = []

    for raw in body.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list_key:
            current_list.append(line[4:].strip().strip('"').strip("'"))
            continue
        # New key terminates any open list
        _flush_list()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            current_list_key = key
            current_list = []
            continue
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            items = [
                x.strip().strip('"').strip("'")
                for x in inner.split(",") if x.strip()
            ] if inner else []
            out[key] = items
            continue
        if value.lower() in ("true", "false"):
            out[key] = value.lower() == "true"
            continue
        # Strip simple quotes
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        out[key] = value
    _flush_list()
    return out


def _charter_from_dict(data: dict[str, Any]) -> SynthesisTrancheCharter:
    """Coerce a frontmatter dict into a SynthesisTrancheCharter."""
    def _as_list(key: str, default: list[str] | None = None) -> list[str]:
        v = data.get(key)
        if v is None:
            return list(default or [])
        if isinstance(v, list):
            return [str(x) for x in v]
        if isinstance(v, str) and v:
            return [v]
        return list(default or [])

    return SynthesisTrancheCharter(
        tranche_id=str(data.get("tranche_id", "unspecified")),
        tranche_class=str(data.get("tranche_class", "internal_governance")),
        tranche_title=str(data.get("tranche_title", data.get("tranche_id", ""))),
        audiences_named=_as_list("audiences_named", ["J-OP"]),
        channels_named=_as_list("channels_named"),
        scenarios_named=_as_list("scenarios_named"),
        brand_register=str(data.get("brand_register", "internal-corpint")),
        ratifying_decisions=_as_list("ratifying_decisions"),
        erp_surface_citations=_as_list("erp_surface_citations"),
        is_atomic_commit=bool(data.get("is_atomic_commit", True)),
        reversibility_class=str(data.get("reversibility_class", "medium")),
        reversibility_rationale=str(data.get("reversibility_rationale", "")),
        closing_loop_test=str(data.get("closing_loop_test", "")),
        recipient_fallback_channel=str(data.get("recipient_fallback_channel", "n/a")),
    )


# ---------------------------------------------------------------------------
# Dimension probes
# ---------------------------------------------------------------------------
# Each probe returns (status, finding_text, recommended_disposition).
# At INFO ramp, probes are heuristic — they enforce charter completeness
# (the operator + agent named the input) rather than deep semantic
# resolution. Future expansion lands per the FAIL ramp Stage 2 gates.


def _probe_audience(charter: SynthesisTrancheCharter) -> tuple[str, str, str]:
    if charter.audiences_named:
        return (
            "PASS",
            f"audiences_named present: {charter.audiences_named}",
            "scope-complete",
        )
    return (
        "FAIL",
        "audiences_named empty — at least J-OP must be named",
        "scope-extend",
    )


def _probe_channel(charter: SynthesisTrancheCharter) -> tuple[str, str, str]:
    if charter.channels_named:
        return (
            "PASS",
            f"channels_named present: {charter.channels_named}",
            "scope-complete",
        )
    return (
        "INFO",
        "channels_named empty — acceptable for J-OP-only tranches",
        "defer-OPS",
    )


def _probe_scenario(charter: SynthesisTrancheCharter) -> tuple[str, str, str]:
    if charter.scenarios_named:
        return (
            "PASS",
            f"scenarios_named present: {charter.scenarios_named}",
            "scope-complete",
        )
    return (
        "INFO",
        "scenarios_named empty — acceptable for internal-governance tranches",
        "defer-OPS",
    )


def _probe_brand_register(charter: SynthesisTrancheCharter) -> tuple[str, str, str]:
    if charter.brand_register:
        return (
            "PASS",
            f"brand_register declared: {charter.brand_register}",
            "scope-complete",
        )
    return (
        "WARN",
        "brand_register unspecified",
        "scope-extend",
    )


def _probe_governance(charter: SynthesisTrancheCharter) -> tuple[str, str, str]:
    if charter.ratifying_decisions:
        return (
            "PASS",
            f"ratifying_decisions present: {charter.ratifying_decisions}",
            "scope-complete",
        )
    return (
        "FAIL",
        "ratifying_decisions empty — every tranche needs decision lineage",
        "scope-extend",
    )


def _probe_erp_surface(charter: SynthesisTrancheCharter) -> tuple[str, str, str]:
    if charter.erp_surface_citations:
        return (
            "PASS",
            f"erp_surface_citations present: {charter.erp_surface_citations}",
            "scope-complete",
        )
    if charter.tranche_class in {"engagement", "external_deliverable"}:
        return (
            "WARN",
            "erp_surface_citations empty — engagement/external tranches "
            "should cite operator-dashboard / customer-dashboard / "
            "ERP-workflow-join surfaces",
            "scope-extend",
        )
    return (
        "N/A",
        "erp_surface_citations not required for this tranche class",
        "scope-complete",
    )


def _probe_atomicity(charter: SynthesisTrancheCharter) -> tuple[str, str, str]:
    if charter.is_atomic_commit:
        return (
            "PASS",
            "is_atomic_commit=true (single-commit landing)",
            "scope-complete",
        )
    return (
        "WARN",
        "is_atomic_commit=false — multi-commit tranches risk mid-state breakage",
        "scope-extend",
    )


def _probe_reversibility(charter: SynthesisTrancheCharter) -> tuple[str, str, str]:
    if charter.reversibility_class and charter.reversibility_rationale:
        return (
            "PASS",
            f"reversibility={charter.reversibility_class} with rationale",
            "scope-complete",
        )
    return (
        "FAIL",
        "reversibility_class / reversibility_rationale missing",
        "scope-extend",
    )


def _probe_closing_loop(charter: SynthesisTrancheCharter) -> tuple[str, str, str]:
    if charter.closing_loop_test:
        return (
            "PASS",
            f"closing_loop_test named: {charter.closing_loop_test[:80]}",
            "scope-complete",
        )
    return (
        "FAIL",
        "closing_loop_test missing — every tranche needs a verifiable PASS criterion",
        "scope-extend",
    )


def _probe_recipient_fallback(
    charter: SynthesisTrancheCharter,
) -> tuple[str, str, str]:
    if charter.recipient_fallback_channel:
        return (
            "PASS",
            f"recipient_fallback_channel: {charter.recipient_fallback_channel}",
            "scope-complete",
        )
    if charter.tranche_class == "external_deliverable":
        return (
            "WARN",
            "recipient_fallback_channel missing for external_deliverable tranche",
            "scope-extend",
        )
    return (
        "N/A",
        "recipient_fallback_channel not required for this tranche class",
        "scope-complete",
    )


_DIMENSION_PROBE_DISPATCH = {
    "SYN-01-AUDIENCE-COMPLETENESS": _probe_audience,
    "SYN-02-CHANNEL-COVERAGE": _probe_channel,
    "SYN-03-SCENARIO-INVENTORY": _probe_scenario,
    "SYN-04-BRAND-REGISTER-CITATION": _probe_brand_register,
    "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE": _probe_governance,
    "SYN-06-ERP-SURFACE-CITATION": _probe_erp_surface,
    "SYN-07-TRANCHE-ATOMICITY": _probe_atomicity,
    "SYN-08-REVERSIBILITY-DECLARATION": _probe_reversibility,
    "SYN-09-CLOSING-LOOP-TEST": _probe_closing_loop,
    "SYN-10-RECIPIENT-FALLBACK-CHANNEL": _probe_recipient_fallback,
}


def sweep_tranche(charter: SynthesisTrancheCharter) -> tuple[list[SynthesisFindingRow], SynthesisReportSummary]:
    """Run every fired dimension probe against the charter."""
    fire_set = resolve_fire_set(charter.tranche_class, conditional_triggers=True)
    findings: list[SynthesisFindingRow] = []
    for dim in sorted(fire_set):
        probe = _DIMENSION_PROBE_DISPATCH.get(dim)
        if probe is None:
            continue
        status, text, disposition = probe(charter)
        sev = DIMENSION_SEVERITY_CLASS.get(dim, "judgement")
        findings.append(
            SynthesisFindingRow(
                tranche_id=charter.tranche_id,
                tranche_class=charter.tranche_class,
                dimension_code=dim,
                status=status,
                finding_text=text,
                recommendation_text=f"severity_class={sev}",
                recommended_disposition=disposition,
            )
        )
    counts = {"PASS": 0, "WARN": 0, "FAIL": 0, "INFO": 0, "N/A": 0}
    for f in findings:
        counts[f.status] = counts.get(f.status, 0) + 1
    summary = SynthesisReportSummary(
        tranche_id=charter.tranche_id,
        tranche_class=charter.tranche_class,
        swept_at=_today(),
        sweep_trigger="tranche_charter",
        dimensions_fired=len(findings),
        pass_count=counts["PASS"],
        warn_count=counts["WARN"],
        fail_count=counts["FAIL"],
        info_count=counts["INFO"],
        na_count=counts["N/A"],
        synthesis_complete=counts["FAIL"] == 0,
        inline_ratify_gates_open=counts["FAIL"] + counts["WARN"],
        operator_disposition_recorded=False,
    )
    return findings, summary


def render_report_markdown(
    charter: SynthesisTrancheCharter,
    findings: list[SynthesisFindingRow],
    summary: SynthesisReportSummary,
) -> str:
    lines: list[str] = []
    lines.append("---")
    lines.append("intellectual_kind: synthesis_before_tranche_report")
    lines.append("sharing_label: internal_only")
    lines.append(f"tranche_id: {charter.tranche_id}")
    lines.append(f"tranche_class: {charter.tranche_class}")
    lines.append(f"swept_at: {summary.swept_at}")
    lines.append(f"sweep_trigger: {summary.sweep_trigger}")
    lines.append(f"synthesis_complete: {str(summary.synthesis_complete).lower()}")
    lines.append("language: en")
    lines.append("---\n")
    lines.append(f"# Synthesis-before-tranche check — {charter.tranche_id}\n")
    lines.append(
        "Generated by `scripts/synthesis_before_tranche_check.py` per the "
        "[SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE](../../../references/hlk/v3.0/"
        "Admin/O5-1/People/canonicals/SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md)"
        " (14th Quality Fabric specialty).\n"
    )
    lines.append("## Tranche charter\n")
    lines.append(f"- **Title**: {charter.tranche_title}")
    lines.append(f"- **Class**: `{charter.tranche_class}`")
    lines.append(f"- **Audiences**: {charter.audiences_named}")
    lines.append(f"- **Channels**: {charter.channels_named}")
    lines.append(f"- **Scenarios**: {charter.scenarios_named}")
    lines.append(f"- **Brand register**: {charter.brand_register}")
    lines.append(f"- **Ratifying decisions**: {charter.ratifying_decisions}")
    lines.append(f"- **ERP surfaces**: {charter.erp_surface_citations}")
    lines.append(f"- **Atomic commit**: {charter.is_atomic_commit}")
    lines.append(
        f"- **Reversibility**: {charter.reversibility_class} — "
        f"{charter.reversibility_rationale or 'no rationale'}"
    )
    lines.append(f"- **Closing loop test**: {charter.closing_loop_test or '(none)'}")
    lines.append(
        f"- **Recipient fallback channel**: {charter.recipient_fallback_channel}\n"
    )
    lines.append("## Summary\n")
    lines.append(
        f"- Dimensions fired: **{summary.dimensions_fired}** "
        f"(PASS={summary.pass_count} / WARN={summary.warn_count} / "
        f"FAIL={summary.fail_count} / INFO={summary.info_count} / "
        f"N/A={summary.na_count})"
    )
    lines.append(
        f"- Synthesis complete: **{summary.synthesis_complete}**"
    )
    lines.append(
        f"- Inline-ratify gates open: **{summary.inline_ratify_gates_open}**\n"
    )
    lines.append("## Per-dimension findings\n")
    lines.append("| Dimension | Status | Finding | Recommended disposition |")
    lines.append("|:---|:---|:---|:---|")
    for f in findings:
        text = f.finding_text.replace("|", "\\|")
        lines.append(
            f"| `{f.dimension_code}` | {f.status} | {text} | "
            f"`{f.recommended_disposition}` |"
        )
    lines.append("")
    lines.append("## Disposition workflow\n")
    lines.append(
        "Per `akos-inline-ratification.mdc` + the synthesis-before-tranche "
        "skill: every FAIL + WARN finding needs an inline-ratify gate "
        "before tranche commit. The 5-option enum is:\n"
    )
    lines.append("1. `scope-complete` — finding cleared; no action needed.")
    lines.append("2. `scope-extend` — extend the tranche to cover the gap.")
    lines.append("3. `scope-narrow` — narrow the tranche; surface deferral.")
    lines.append("4. `defer-OPS` — file an OPS_REGISTER row for next cycle.")
    lines.append(
        "5. `escalate-to-blocker-tracker` — mint `_blockers/<slug>-tracker.md` "
        "per `akos-conflict-surfacing-and-blocker-trackers.mdc`."
    )
    return "\n".join(lines) + "\n"


def _emit_report(
    charter: SynthesisTrancheCharter,
    findings: list[SynthesisFindingRow],
    summary: SynthesisReportSummary,
    reports_dir: Path,
) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    fname = f"synthesis-check-{_slug(charter.tranche_id)}-{summary.swept_at}.md"
    path = reports_dir / fname
    path.write_text(
        render_report_markdown(charter, findings, summary),
        encoding="utf-8",
    )
    return path


def self_test() -> int:
    """Runbook self-test: chassis is importable + dispatch table covers all 10 dimensions."""
    missing = VALID_DIMENSION_CODES - set(_DIMENSION_PROBE_DISPATCH)
    if missing:
        print(
            f"FAIL [probe-dispatch-coverage]: missing probes for: {sorted(missing)}"
        )
        return 1
    extra = set(_DIMENSION_PROBE_DISPATCH) - VALID_DIMENSION_CODES
    if extra:
        print(
            f"FAIL [probe-dispatch-orphan]: probes for unknown dimensions: {sorted(extra)}"
        )
        return 2

    # Spot-check sweep on a worked-example charter (this commit itself)
    charter = SynthesisTrancheCharter(
        tranche_id="I86-WaveRplus1-P3-Commit2b-synthesis-runbook",
        tranche_class="specialty_mint",
        tranche_title="14th specialty runbook self-test fixture",
        audiences_named=["J-OP"],
        channels_named=[],
        scenarios_named=[],
        brand_register="internal-corpint",
        ratifying_decisions=["D-IH-86-EA", "D-IH-86-EB", "D-IH-86-EC", "D-IH-86-ED"],
        erp_surface_citations=[],
        is_atomic_commit=True,
        reversibility_class="medium",
        reversibility_rationale=(
            "runbook + verification wiring; revert via git revert + "
            "verification-profiles.json + release-gate.py unwiring; no "
            "canonical CSV writes; medium reversibility"
        ),
        closing_loop_test="synthesis_before_tranche_check.py --self-test PASS",
        recipient_fallback_channel="n/a (J-OP-only governance tranche)",
    )
    findings, summary = sweep_tranche(charter)
    if summary.fail_count > 0:
        print(
            f"FAIL [self-test-charter]: {summary.fail_count} FAIL findings on "
            f"runbook-self-test fixture (expected 0): {[f.dimension_code for f in findings if f.status == 'FAIL']}"
        )
        return 3

    print(
        "synthesis_before_tranche_check --self-test: PASS "
        f"({len(_DIMENSION_PROBE_DISPATCH)} dimension probes wired; "
        f"specialty_mint fire-set yields {summary.dimensions_fired} fired "
        f"(PASS={summary.pass_count}/WARN={summary.warn_count}/"
        f"FAIL={summary.fail_count}/INFO={summary.info_count}/N/A={summary.na_count}); "
        "Pydantic chassis consistent)"
    )
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

    parser = argparse.ArgumentParser(
        description=(
            "Per-tranche synthesis sweep runbook (14th Quality Fabric "
            "specialty per D-IH-86-EA). Reads a tranche charter + dispatches "
            "the 10-dimension fire-set + emits a synthesis report markdown."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "Verify Pydantic chassis + probe dispatch table covers all 10 "
            "dimensions + runbook-self-test fixture passes. Wired into "
            "pre_commit + release-gate.py for zero-cost CI gating."
        ),
    )
    parser.add_argument(
        "--check-charter",
        type=str,
        default=None,
        help=(
            "Path to a tranche charter markdown file with YAML frontmatter. "
            "Runbook parses the frontmatter into a SynthesisTrancheCharter + "
            "dispatches the appropriate fire-set."
        ),
    )
    parser.add_argument(
        "--tranche-id", type=str, default=None,
        help="Inline tranche_id (when not using --check-charter).",
    )
    parser.add_argument(
        "--tranche-class", type=str, default=None,
        choices=sorted(VALID_TRANCHE_CLASSES),
        help="Inline tranche_class (when not using --check-charter).",
    )
    parser.add_argument(
        "--audiences", type=str, default="",
        help="Inline audiences (comma-separated; e.g. 'J-OP,J-CU').",
    )
    parser.add_argument(
        "--ratifying-decisions", type=str, default="",
        help="Inline ratifying decision IDs (comma-separated).",
    )
    parser.add_argument(
        "--reversibility", type=str, default="medium",
        help="Inline reversibility_class (low/medium/high).",
    )
    parser.add_argument(
        "--closing-loop-test", type=str, default="",
        help="Inline closing_loop_test text.",
    )
    parser.add_argument(
        "--emit-report",
        action="store_true",
        help="Write the synthesis report markdown to the reports/ folder.",
    )
    parser.add_argument(
        "--reports-dir",
        type=str,
        default=str(REPORTS_DIR_DEFAULT),
        help="Override reports output directory.",
    )
    args = parser.parse_args()

    if args.self_test or (
        not args.check_charter and not args.tranche_id
    ):
        return self_test()

    if args.check_charter:
        path = Path(args.check_charter)
        if not path.is_file():
            print(f"FAIL: charter file not found: {path}")
            return 4
        text = path.read_text(encoding="utf-8")
        data = _parse_yaml_frontmatter(text)
        if not data:
            print(f"FAIL: no YAML frontmatter found in: {path}")
            return 5
        charter = _charter_from_dict(data)
    else:
        if not args.tranche_class:
            print("FAIL: --tranche-class required when not using --check-charter")
            return 6
        charter = SynthesisTrancheCharter(
            tranche_id=args.tranche_id,
            tranche_class=args.tranche_class,
            tranche_title=args.tranche_id,
            audiences_named=[
                s.strip() for s in args.audiences.split(",") if s.strip()
            ] or ["J-OP"],
            channels_named=[],
            scenarios_named=[],
            brand_register="internal-corpint",
            ratifying_decisions=[
                s.strip() for s in args.ratifying_decisions.split(",") if s.strip()
            ],
            erp_surface_citations=[],
            is_atomic_commit=True,
            reversibility_class=args.reversibility,
            reversibility_rationale="inline-CLI tranche; rationale TBD",
            closing_loop_test=args.closing_loop_test or "(inline CLI; TBD)",
            recipient_fallback_channel="n/a",
        )

    findings, summary = sweep_tranche(charter)
    print(
        f"Tranche `{charter.tranche_id}` ({charter.tranche_class}): "
        f"{summary.dimensions_fired} dimensions fired — "
        f"PASS={summary.pass_count} WARN={summary.warn_count} "
        f"FAIL={summary.fail_count} INFO={summary.info_count} "
        f"N/A={summary.na_count}"
    )
    for f in findings:
        if f.status in ("FAIL", "WARN"):
            print(
                f"  [{f.status}] {f.dimension_code}: {f.finding_text}  "
                f"→ disposition: {f.recommended_disposition}"
            )
    if args.emit_report:
        path = _emit_report(
            charter, findings, summary, Path(args.reports_dir)
        )
        print(f"Synthesis report written: {path}")

    return 0 if summary.fail_count == 0 else 7


if __name__ == "__main__":
    sys.exit(main())
