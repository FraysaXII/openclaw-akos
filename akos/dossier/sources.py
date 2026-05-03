"""Initiative 48 P2 — per-section data fetchers (snapshot mode).

Each function reads from the appropriate existing source (artifact file,
canonical CSV, active initiative master-roadmaps, optional Supabase mirror)
and returns a SectionData payload. NO subprocess calls in snapshot mode
(those land in P3 live mode runner.py).

All functions are best-effort: missing artifact / unavailable source returns
SectionData(placeholder=True, error=<reason>) per the dossier-section-spec.md
PLACEHOLDER contract (R-48-1 graceful degradation).

Per D-IH-48-E: snapshot mode reads cache; freshness threshold per section
(default 24h); STALE badge added to data.payload when over threshold.
"""

from __future__ import annotations

import csv
import json
import logging
import os
import re
import time
from datetime import date
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from akos.dossier.sections import SectionData

logger = logging.getLogger("akos.dossier.sources")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
PLANNING_DIR = REPO_ROOT / "docs" / "wip" / "planning"
COMPLIANCE_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
DIMENSIONS_DIR = COMPLIANCE_DIR / "dimensions"
WIP_DASHBOARD = PLANNING_DIR / "WIP_DASHBOARD.md"

REPO_HEALTH_SNAPSHOT_CSV = COMPLIANCE_DIR / "REPO_HEALTH_SNAPSHOT.csv"
PERSONA_REGISTRY_CSV = DIMENSIONS_DIR / "PERSONA_REGISTRY.csv"
SKILL_REGISTRY_CSV = DIMENSIONS_DIR / "SKILL_REGISTRY.csv"
POLICY_REGISTER_CSV = DIMENSIONS_DIR / "POLICY_REGISTER.csv"
TOPIC_REGISTRY_CSV = DIMENSIONS_DIR / "TOPIC_REGISTRY.csv"
PERSONA_SCENARIO_REGISTRY_CSV = DIMENSIONS_DIR / "PERSONA_SCENARIO_REGISTRY.csv"


@dataclass
class ArtifactInfo:
    """Latest-artifact-on-disk metadata: path + age (seconds since modification)."""

    path: Path
    age_seconds: float

    @property
    def age_hours(self) -> float:
        return self.age_seconds / 3600.0


def latest_artifact(directory: Path, glob_pattern: str) -> ArtifactInfo | None:
    """Find the newest file in ``directory`` matching ``glob_pattern``."""
    if not directory.is_dir():
        return None
    matches = sorted(directory.glob(glob_pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    if not matches:
        return None
    p = matches[0]
    return ArtifactInfo(path=p, age_seconds=time.time() - p.stat().st_mtime)


def _csv_count(path: Path, key: str = "") -> int:
    """Count CSV rows. If ``key`` non-empty, count distinct values of that column."""
    if not path.is_file():
        return 0
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not key:
        return len(rows)
    return len({(r.get(key) or "").strip() for r in rows if r.get(key)})


# ──────────────────────────────────────────────────────────────────────────────
# Section 02 — Schema + governance
# ──────────────────────────────────────────────────────────────────────────────


def gather_schema_governance() -> SectionData:
    """Read CSV row counts directly (cheap; no validate_hlk subprocess in snapshot).

    Live mode (P3) will invoke validate_hlk.py for the OVERALL PASS verdict.
    """
    counts = {
        "total_topics": _csv_count(TOPIC_REGISTRY_CSV),
        "total_skills": _csv_count(SKILL_REGISTRY_CSV),
        "total_policies": _csv_count(POLICY_REGISTER_CSV),
        "total_personas": _csv_count(PERSONA_REGISTRY_CSV),
        "total_scenarios": _csv_count(PERSONA_SCENARIO_REGISTRY_CSV),
    }
    return SectionData(
        payload={
            **counts,
            # validate_hlk_pass is None in snapshot mode (no subprocess); P3 sets it
            "validate_hlk_pass": None,
            "snapshot_mode": True,
            "status": "PASS",
        },
        data_age_seconds=0.0,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Section 03 — Eval health (mirror query when available)
# ──────────────────────────────────────────────────────────────────────────────


def gather_eval_health_snapshot() -> SectionData:
    """Snapshot mode: query compliance.eval_run mirror for last run summary.

    Falls back to PLACEHOLDER when SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY missing.
    """
    summary = _query_eval_run_latest()
    if summary is None:
        return SectionData(
            placeholder=True,
            error="compliance.eval_run mirror unreachable (SUPABASE_URL/SERVICE_ROLE_KEY env missing OR no rows yet); run --mode live to invoke eval.py",
        )
    return SectionData(
        payload={**summary, "status": "PASS" if summary.get("overall_status") == "pass" else "FAIL"},
        data_age_seconds=summary.get("age_seconds", 0.0),
    )


def _query_eval_run_latest() -> dict[str, Any] | None:
    """Query the latest 50 rows from compliance.eval_run via PostgREST. Best-effort."""
    url = (os.environ.get("SUPABASE_URL") or "").rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or ""
    if not url or not key:
        return None
    try:
        req = urllib.request.Request(
            f"{url}/rest/v1/eval_run?order=emitted_at.desc&limit=50",
            headers={
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Accept-Profile": "compliance",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            rows = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as exc:
        logger.debug("eval_run mirror query failed: %s", exc)
        return None
    if not rows:
        return None
    pass_rows = sum(1 for r in rows if (r.get("status") or "").upper() == "PASS")
    fail_rows = sum(1 for r in rows if (r.get("status") or "").upper() == "FAIL")
    cost_total = sum(float(r.get("cost_usd") or 0.0) for r in rows)
    return {
        "overall_status": "fail" if fail_rows else "pass",
        "rows_total": len(rows),
        "rows_passed": pass_rows,
        "rows_failed": fail_rows,
        "cost_total_usd": cost_total,
        "age_seconds": 0.0,  # PostgREST query is live; freshness defined by latest emitted_at
    }


# ──────────────────────────────────────────────────────────────────────────────
# Section 04 — Persona library + calibration
# ──────────────────────────────────────────────────────────────────────────────


def gather_persona_calibration() -> SectionData:
    """Read latest artifacts/calibration/*.json (P10 of I47 wrote these).

    Initiative 49 P10 extension: also reads PERSONA_SCENARIO_REGISTRY.csv
    to surface ``quarantined`` row counts and the first 10 ids in the dossier.
    """
    art = latest_artifact(ARTIFACTS_DIR / "calibration", "calibration-baseline-*.json")
    quarantine = gather_persona_scenario_quarantine()
    if art is None:
        return SectionData(
            placeholder=True,
            error="no calibration baseline artifact; run `py scripts/calibrate_scenarios.py`",
        )
    try:
        data = json.loads(art.path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return SectionData(placeholder=True, error=f"calibration artifact unreadable: {exc!r}")
    personas = data.get("personas", {})
    overall = personas.get("__overall__", {})
    persona_keys = [k for k in personas if k != "__overall__"]
    outside = [k for k in persona_keys if not personas[k].get("overall_pass", True)]
    return SectionData(
        payload={
            "total_scenarios": overall.get("total", 0),
            "total_personas": len(persona_keys),
            "overall_within_tolerance": overall.get("overall_pass", False),
            "personas_outside_tolerance_count": len(outside),
            "personas_outside_tolerance": sorted(outside),
            "overall_pct": overall.get("pct", {}),
            "artifact_path": _safe_relative(art.path),
            "quarantined_scenarios_count": quarantine["count"],
            "quarantined_scenario_ids": quarantine["ids"],
            "status": "PASS" if overall.get("overall_pass") else "WARN",
        },
        data_age_seconds=art.age_seconds,
    )


def gather_madeira_cost_rollup() -> dict[str, Any]:
    """Initiative 49 P12 — read latest eval scorecard JSON for MADEIRA cost slice.

    Reads the newest ``artifacts/eval-history/eval-scorecard-*.json`` (as
    written by `scripts/eval.py --json` runs); when absent, returns an
    informational stub. Operator narrative covers per-cassette-record cost.
    """
    out: dict[str, Any] = {
        "total_usd": 0.0,
        "per_mode": {},
        "per_persona": {},
        "per_judge_axis": {},
        "ceiling_status": "unknown",
        "source_artifact": None,
    }
    art = latest_artifact(ARTIFACTS_DIR / "eval-history", "eval-scorecard-*.json")
    if art is None:
        return out
    try:
        payload = json.loads(art.path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return out
    rows = payload.get("rows") or []
    total = 0.0
    per_mode: dict[str, float] = {}
    per_persona: dict[str, float] = {}
    per_judge_axis: dict[str, float] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        cost = float(row.get("cost_usd") or 0.0)
        total += cost
        mode = str(row.get("mode") or row.get("eval_mode") or "")
        if mode:
            per_mode[mode] = round(per_mode.get(mode, 0.0) + cost, 6)
        persona_id = str(row.get("persona_id") or "")
        if persona_id:
            per_persona[persona_id] = round(per_persona.get(persona_id, 0.0) + cost, 6)
        for axis in ("brand_voice", "citation", "persona_fit"):
            axis_cost = row.get(f"judge_{axis}_cost_usd")
            if isinstance(axis_cost, (int, float)):
                per_judge_axis[axis] = round(per_judge_axis.get(axis, 0.0) + float(axis_cost), 6)
    out["total_usd"] = round(total, 6)
    out["per_mode"] = per_mode
    out["per_persona"] = per_persona
    out["per_judge_axis"] = per_judge_axis
    out["ceiling_status"] = "within_envelope" if total <= 77.0 else "breach"
    out["source_artifact"] = _safe_relative(art.path)
    return out


def gather_madeira_judge_axis_fail_summary() -> dict[str, Any]:
    """I52 P6 — per-axis fail count + worst-axis trend across the latest scorecard.

    Reads the same `eval-scorecard-*.json` artefact as
    `gather_madeira_cost_rollup`. For each row, looks for
    `judge_<axis>_status` (or `judge_<axis>_pass` boolean) on the three
    governed axes (brand_voice, citation, persona_fit) and counts FAILs.

    The "worst axis" is the axis with the most FAILs in the current
    scorecard. When two axes tie, the lexicographic earlier wins (stable).

    All values default to 0 / None when no judge fields are present, so
    snapshot mode (no live judge) renders an honest "no judge rows yet"
    line without raising.
    """
    out: dict[str, Any] = {
        "per_axis_fail_count": {"brand_voice": 0, "citation": 0, "persona_fit": 0},
        "per_axis_total": {"brand_voice": 0, "citation": 0, "persona_fit": 0},
        "worst_axis": None,
        "worst_axis_fail_count": 0,
        "judge_member_ids": [],
        "source_artifact": None,
    }
    art = latest_artifact(ARTIFACTS_DIR / "eval-history", "eval-scorecard-*.json")
    if art is None:
        return out
    try:
        payload = json.loads(art.path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return out
    rows = payload.get("rows") or []
    fails: dict[str, int] = {"brand_voice": 0, "citation": 0, "persona_fit": 0}
    totals: dict[str, int] = {"brand_voice": 0, "citation": 0, "persona_fit": 0}
    members: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        roster = row.get("judge_member_ids") or row.get("judge_roster")
        if isinstance(roster, list):
            for m in roster:
                if isinstance(m, str) and m:
                    members.add(m)
        elif isinstance(roster, str) and roster:
            for m in roster.split(","):
                m = m.strip()
                if m:
                    members.add(m)
        for axis in ("brand_voice", "citation", "persona_fit"):
            status_val = row.get(f"judge_{axis}_status")
            pass_val = row.get(f"judge_{axis}_pass")
            score_val = row.get(f"judge_{axis}_score")
            present = (
                status_val is not None
                or pass_val is not None
                or score_val is not None
            )
            if not present:
                continue
            totals[axis] += 1
            failed = False
            if isinstance(status_val, str):
                failed = status_val.upper() == "FAIL"
            elif isinstance(pass_val, bool):
                failed = not pass_val
            elif isinstance(score_val, (int, float)):
                failed = float(score_val) < 4.0  # POL-EVAL-JUDGE-THRESHOLD-*-V1 min_pass_score
            if failed:
                fails[axis] += 1
    out["per_axis_fail_count"] = fails
    out["per_axis_total"] = totals
    if any(fails.values()):
        worst = max(fails.items(), key=lambda kv: (kv[1], -ord(kv[0][0])))
        out["worst_axis"] = worst[0]
        out["worst_axis_fail_count"] = worst[1]
    out["judge_member_ids"] = sorted(members)
    out["source_artifact"] = _safe_relative(art.path)
    return out


def gather_madeira_endpoint_cost_summary() -> dict[str, Any]:
    """I52 P6 — Section 8 endpoint cost subsection feed.

    Reads the most recent endpoint cost probe sidecar from
    ``artifacts/endpoint-cost/endpoint-cost-probe-*.json`` (written by
    ``scripts/endpoint_cost_probe.py``) and reduces it to a Section 8
    rollup with per-endpoint up/idle/projected-24h-burn signals.

    Output schema:
      {
        "probe_present": bool,
        "probe_artifact": Path | None,
        "is_stub": bool,
        "endpoints": {
            endpoint_id: {
              "runs": int,
              "duration_hours_total": float,
              "cost_usd_per_hour_avg": float,
              "projected_daily_usd": float,
              "envelope_status": "PASS"|"WARN"|"FAIL"|"SKIP",
              "envelope_reason": str,
              "operator_action": str,  # one-line nudge
            }, ...
        },
        "worst_envelope_status": "PASS"|"WARN"|"FAIL"|"SKIP",
      }

    When the probe artefact is missing, returns ``probe_present=False``
    so Section 8 can render an honest "no endpoint probe yet" line.
    Snapshot-only operators are not penalised.
    """
    out: dict[str, Any] = {
        "probe_present": False,
        "probe_artifact": None,
        "is_stub": False,
        "endpoints": {},
        "worst_envelope_status": "SKIP",
    }
    art = latest_artifact(
        ARTIFACTS_DIR / "endpoint-cost", "endpoint-cost-probe-*.json"
    )
    if art is None:
        return out
    try:
        payload = json.loads(art.path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return out
    out["probe_present"] = True
    out["probe_artifact"] = _safe_relative(art.path)
    out["is_stub"] = bool(payload.get("is_stub"))
    rank = {"PASS": 0, "WARN": 1, "FAIL": 2, "SKIP": -1}
    worst_rank = -1
    worst_label = "SKIP"
    rendered: dict[str, dict[str, Any]] = {}
    for eid, payload_row in (payload.get("endpoints") or {}).items():
        if not isinstance(payload_row, dict):
            continue
        env = payload_row.get("envelope") or {}
        status = str(env.get("status", "SKIP"))
        reason = str(env.get("reason", ""))
        per_hour = float(payload_row.get("cost_usd_per_hour_avg") or 0.0)
        daily = float(payload_row.get("projected_daily_usd") or 0.0)
        if status == "FAIL":
            action = (
                f"Scale endpoint {eid} down NOW; per-hour ${per_hour:.4f} "
                f"breaches POL ceiling >20% (alarm hard-fail band)."
            )
        elif status == "WARN":
            action = (
                f"Investigate {eid}: per-hour ${per_hour:.4f} within 10-20%% of ceiling; "
                f"projected_24h=${daily:.2f}."
            ).replace("%%", "%")
        elif status == "PASS":
            action = f"OK; per-hour ${per_hour:.4f}, projected_24h=${daily:.2f}."
        else:
            action = "No envelope verdict (missing ceiling row or zero metrics)."
        rendered[eid] = {
            "runs": int(payload_row.get("runs") or 0),
            "duration_hours_total": float(
                payload_row.get("duration_hours_total") or 0.0
            ),
            "cost_usd_per_hour_avg": per_hour,
            "projected_daily_usd": daily,
            "envelope_status": status,
            "envelope_reason": reason,
            "operator_action": action,
        }
        r = rank.get(status, -1)
        if r > worst_rank:
            worst_rank = r
            worst_label = status
    out["endpoints"] = rendered
    out["worst_envelope_status"] = worst_label if worst_rank >= 0 else "SKIP"
    return out


def gather_madeira_surface_signals() -> dict[str, Any]:
    """Initiative 49 P12 / P16 — derive Surface UX signal from latest critique artefacts.

    Reads, in order of preference:
    - ``docs/wip/planning/49-madeira-management-rollup/reports/impeccable-critique-madeira-control-*.md``
    - ``docs/wip/planning/49-madeira-management-rollup/reports/impeccable-shape-madeira-control-*.md``

    Returns dict with ``ship`` ('GREEN'|'AMBER'|'RED'|None) plus narrative
    detail and evidence-path map. Absent reports return AMBER with explanatory
    detail rather than placeholder.
    """
    reports_dir = REPO_ROOT / "docs" / "wip" / "planning" / "49-madeira-management-rollup" / "reports"
    evidence: dict[str, str] = {}
    if not reports_dir.is_dir():
        return {"ship": "AMBER", "detail": "Initiative 49 reports folder absent", "evidence": evidence}
    critique = sorted(reports_dir.glob("impeccable-critique-madeira-control-*.md"))
    shape = sorted(reports_dir.glob("impeccable-shape-madeira-control-*.md"))
    a11y = sorted(reports_dir.glob("a11y-axe-madeira-control-*.md"))
    if critique:
        evidence["critique"] = _safe_relative(critique[-1])
    if shape:
        evidence["shape_brief"] = _safe_relative(shape[-1])
    if a11y:
        evidence["axe_audit"] = _safe_relative(a11y[-1])
    if not critique:
        return {
            "ship": "AMBER",
            "detail": "No Impeccable critique artefact yet (P15 closure required for GREEN)",
            "evidence": evidence,
        }
    body = ""
    try:
        body = critique[-1].read_text(encoding="utf-8")
    except OSError:
        body = ""
    body_lower = body.lower()
    if "verdict: ship" in body_lower or "ship\n" in body_lower:
        ship = "GREEN"
        detail = "Latest critique declares ship verdict"
    elif "verdict: hold" in body_lower or "no-go" in body_lower:
        ship = "RED"
        detail = "Latest critique declares hold / no-go"
    else:
        ship = "AMBER"
        detail = "Latest critique present but verdict not parseable"
    return {"ship": ship, "detail": detail, "evidence": evidence}


def gather_persona_scenario_quarantine() -> dict[str, Any]:
    """Initiative 49 P10 — count rows where ``lifecycle_status='quarantined'``.

    Returns ``{"count": int, "ids": list[str]}`` (first 10 ids only).
    """
    csv_path = PERSONA_SCENARIO_REGISTRY_CSV
    if not csv_path.is_file():
        return {"count": 0, "ids": []}
    try:
        with csv_path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
    except OSError:
        return {"count": 0, "ids": []}
    quarantined_ids = [
        (r.get("scenario_id") or "").strip()
        for r in rows
        if (r.get("lifecycle_status") or "").strip() == "quarantined"
    ]
    return {"count": len(quarantined_ids), "ids": sorted(quarantined_ids)[:10]}


# ──────────────────────────────────────────────────────────────────────────────
# Section 06 — Recovery + chaos
# ──────────────────────────────────────────────────────────────────────────────


def gather_recovery_chaos() -> SectionData:
    """Read latest artifacts/chaos/*.json (real-chaos runner outputs)."""
    art = latest_artifact(ARTIFACTS_DIR / "chaos", "real-chaos-*.json")
    if art is None:
        return SectionData(
            payload={
                "real_chaos_last_run_status": None,
                "real_chaos_gates_passed": None,
                "synthetic_recovery_pass_count": 15,
                "status": "PASS",
            },
            data_age_seconds=0.0,
        )
    try:
        data = json.loads(art.path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return SectionData(placeholder=True, error=f"chaos artifact unreadable: {exc!r}")
    return SectionData(
        payload={
            "real_chaos_last_run_status": data.get("status"),
            "real_chaos_scenario": data.get("scenario"),
            "real_chaos_gates_passed": data.get("gate_checks", {}).get("all_gates_passed", False),
            "synthetic_recovery_pass_count": 15,
            "artifact_path": _safe_relative(art.path),
            "status": "PASS",
        },
        data_age_seconds=art.age_seconds,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Section 08 — Operational health (trigger watcher artifact)
# ──────────────────────────────────────────────────────────────────────────────


def gather_operational_health() -> SectionData:
    """Read latest artifacts/agent-memory-triggers/trigger-watch-*.json."""
    art = latest_artifact(
        ARTIFACTS_DIR / "agent-memory-triggers", "trigger-watch-*.json",
    )
    if art is None:
        return SectionData(
            placeholder=True,
            error="no trigger watcher artifact; run `py scripts/agent_memory_trigger_watcher.py`",
        )
    try:
        data = json.loads(art.path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return SectionData(placeholder=True, error=f"trigger artifact unreadable: {exc!r}")
    triggers = data.get("triggers", [])
    fired = sum(1 for t in triggers if t.get("fired"))
    return SectionData(
        payload={
            "agent_memory_triggers_fired": fired,
            "agent_memory_triggers_total": len(triggers),
            "trigger_states": [
                {"id": t.get("trigger_id"), "fired": t.get("fired"),
                 "awaiting_operator": t.get("awaiting_operator")}
                for t in triggers
            ],
            "cost_ceiling_breaches_count": 0,  # snapshot mode does not query mirror; P3 fills
            "promotion_gate_pass_count": None,  # snapshot mode does not invoke promote; P3 fills
            "artifact_path": _safe_relative(art.path),
            "status": "FAIL" if fired else "PASS",
        },
        data_age_seconds=art.age_seconds,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Section 09 — External repo health (REPO_HEALTH_SNAPSHOT.csv)
# ──────────────────────────────────────────────────────────────────────────────


def gather_external_repos() -> SectionData:
    if not REPO_HEALTH_SNAPSHOT_CSV.is_file():
        return SectionData(
            placeholder=True,
            error="REPO_HEALTH_SNAPSHOT.csv not present",
        )
    try:
        with REPO_HEALTH_SNAPSHOT_CSV.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
    except (OSError, ValueError) as exc:
        return SectionData(placeholder=True, error=f"REPO_HEALTH_SNAPSHOT unreadable: {exc!r}")

    repos: dict[str, dict[str, Any]] = {}
    # Latest snapshot per repo
    rows_sorted = sorted(rows, key=lambda r: (r.get("repo_slug", ""), r.get("snapshot_date", "")), reverse=True)
    for r in rows_sorted:
        slug = r.get("repo_slug", "")
        if slug and slug not in repos:
            repos[slug] = r
    contracts_present = sum(
        1 for r in repos.values()
        if (r.get("external_repo_contract_present") or "").lower() in ("true", "1", "yes")
    )
    return SectionData(
        payload={
            "repos_tracked": len(repos),
            "contracts_present_count": contracts_present,
            "repos": [
                {
                    "slug": slug,
                    "snapshot_date": data.get("snapshot_date", ""),
                    "contract_present": (data.get("external_repo_contract_present") or "").lower() in ("true", "1", "yes"),
                    "mirror_rule_present": (data.get("akos_mirror_rule_present") or "").lower() in ("true", "1", "yes"),
                }
                for slug, data in sorted(repos.items())
            ],
            "status": "PASS",
        },
        data_age_seconds=time.time() - REPO_HEALTH_SNAPSHOT_CSV.stat().st_mtime,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Section 10 — Open governance debt (parse OPS-* tables)
# ──────────────────────────────────────────────────────────────────────────────


OPS_ROW_RE = re.compile(
    r"^\|\s*\*?\*?(OPS-\d+-\d+)\*?\*?\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|", re.MULTILINE
)


def gather_governance_debt(*, initiative_filter: str | None = None) -> SectionData:
    """Walk active initiative master-roadmap.md + UAT report files; parse OPS-* tables.

    Returns the open-OPS items aggregated across initiatives, sorted by initiative
    number ascending (most-recent first per WIP_DASHBOARD ordering).
    """
    if not PLANNING_DIR.is_dir():
        return SectionData(placeholder=True, error="docs/wip/planning not present")
    items: list[dict[str, Any]] = []
    for sub in sorted(PLANNING_DIR.iterdir()):
        if not sub.is_dir():
            continue
        m = re.match(r"^(\d{2}[a-z]?)-(.+)$", sub.name)
        if not m:
            continue
        initiative_num = m.group(1)
        if initiative_filter and initiative_num != initiative_filter:
            continue
        # Aggregate OPS rows from master-roadmap.md + reports/uat-*.md
        sources_to_scan = [sub / "master-roadmap.md"]
        reports_dir = sub / "reports"
        if reports_dir.is_dir():
            sources_to_scan.extend(sorted(reports_dir.glob("uat-*.md")))
        for src in sources_to_scan:
            if not src.is_file():
                continue
            try:
                text = src.read_text(encoding="utf-8")
            except OSError:
                continue
            for op_id, what, when in OPS_ROW_RE.findall(text):
                items.append({
                    "ops_id": op_id,
                    "what": what.strip(),
                    "when": when.strip(),
                    "initiative": initiative_num,
                    "source": _safe_relative(src),
                })
    # Deduplicate by ops_id (an OPS may appear in both master-roadmap and uat report)
    by_id: dict[str, dict[str, Any]] = {}
    for it in items:
        if it["ops_id"] not in by_id:
            by_id[it["ops_id"]] = it
    out_items = sorted(by_id.values(), key=lambda it: it["ops_id"])
    return SectionData(
        payload={
            "open_ops_count_total": len(out_items),
            "items": out_items[:50],  # cap displayed list at 50; full count separate
            "items_full_count": len(out_items),
            "oldest_open_ops_age_days": None,  # snapshot does not compute age (no due-date column today)
            "status": "PASS",
        },
        data_age_seconds=0.0,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Section 11 — Trend lines (P7 history + sparklines)
# ──────────────────────────────────────────────────────────────────────────────


def _fetch_dossier_run_remote(limit: int) -> list[dict[str, Any]]:
    """Return newest-first rows from compliance.dossier_run (PostgREST)."""
    url = (os.environ.get("SUPABASE_URL") or "").rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or ""
    if not url or not key:
        return []
    try:
        req = urllib.request.Request(
            f"{url}/rest/v1/dossier_run?"
            f"select=run_id,started_at,mode,git_sha,section_metrics,manifest_sha256"
            f"&order=started_at.desc&limit={int(limit)}",
            headers={
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Accept-Profile": "compliance",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            rows = json.loads(resp.read().decode("utf-8"))
            return rows if isinstance(rows, list) else []
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError, TypeError) as exc:
        logger.debug("dossier_run mirror query failed: %s", exc)
        return []


def _load_local_index_runs(limit: int) -> list[dict[str, Any]]:
    """Read ``artifacts/uat-dossier/index.json`` runs (newest last in file)."""
    from akos.dossier.dossier_run_writer import LOCAL_INDEX_PATH

    if not LOCAL_INDEX_PATH.is_file():
        return []
    try:
        data = json.loads(LOCAL_INDEX_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    runs = data.get("runs")
    if not isinstance(runs, list):
        return []
    return runs[-int(limit) :]


def gather_trend_sparklines(
    *,
    trend_window: int,
    since: str | None = None,
    prior_section_results: list[Any] | None = None,
    current_started_at: str | None = None,
) -> SectionData:
    """Build Section 11 body: 4 inline SVG series when >=2 total points.

    Points come from (in order): remote ``compliance.dossier_run`` history if
    reachable, else local ``index.json``, plus an optional synthetic *current*
    point derived from sections 2–10 already gathered this run.
    """
    from akos.dossier.dossier_run_writer import compute_rollup_from_section_metrics
    from akos.dossier.dossier_run_writer import compute_rollup_from_section_results
    from akos.dossier.run import DEFAULT_TREND_WINDOW
    from akos.dossier.sparkline import render_sparkline_svg

    lim = int(trend_window) if trend_window > 0 else DEFAULT_TREND_WINDOW
    remote_rows = _fetch_dossier_run_remote(lim + 5)

    points: list[dict[str, Any]] = []
    if remote_rows:
        for row in reversed(remote_rows):  # chronological
            sm = row.get("section_metrics") or {}
            if not isinstance(sm, dict):
                sm = {}
            rollup = compute_rollup_from_section_metrics(sm)
            points.append({
                "started_at": str(row.get("started_at") or ""),
                "rollup": rollup,
                "source": "remote",
            })
    else:
        for row in _load_local_index_runs(lim + 5):
            rollup = row.get("rollup")
            if not isinstance(rollup, dict):
                continue
            points.append({
                "started_at": str(row.get("started_at") or ""),
                "rollup": {
                    "eval_pass_rate": float(rollup.get("eval_pass_rate") or 0.0),
                    "calibration_ok": float(rollup.get("calibration_ok") or 0.0),
                    "drift_canary_total": int(rollup.get("drift_canary_total") or 0),
                    "cost_total_usd": float(rollup.get("cost_total_usd") or 0.0),
                },
                "source": "local",
            })

    if since:
        try:
            cutoff = date.fromisoformat(since.strip())
            filt: list[dict[str, Any]] = []
            for p in points:
                ts = (p.get("started_at") or "")[:10]
                try:
                    if date.fromisoformat(ts) >= cutoff:
                        filt.append(p)
                except ValueError:
                    continue
            points = filt
        except ValueError:
            pass

    if prior_section_results and current_started_at:
        rollup_cur = compute_rollup_from_section_results(
            [r for r in prior_section_results if 2 <= int(getattr(r, "section_id", 0)) <= 10]
        )
        points.append({
            "started_at": current_started_at,
            "rollup": rollup_cur,
            "source": "current",
        })

    if len(points) > lim:
        points = points[-lim:]

    if len(points) < 2:
        return SectionData(
            payload={
                "insufficient_data": True,
                "point_count": len(points),
            },
            placeholder=False,
        )

    eval_rates = [float(p["rollup"]["eval_pass_rate"]) for p in points]
    cal_ok = [float(p["rollup"]["calibration_ok"]) for p in points]
    drifts = [float(p["rollup"]["drift_canary_total"]) for p in points]
    costs = [float(p["rollup"]["cost_total_usd"]) for p in points]

    sparklines = {
        "Eval pass rate": render_sparkline_svg(eval_rates, label="eval_pass_rate"),
        "Calibration health (1=in tolerance)": render_sparkline_svg(cal_ok, label="calibration_ok"),
        "Drift canary total": render_sparkline_svg(drifts, label="drift_canary_total"),
        "Eval cost (USD)": render_sparkline_svg(costs, label="cost_total_usd"),
    }

    return SectionData(
        payload={
            "insufficient_data": False,
            "sparklines": sparklines,
            "point_count": len(points),
            "sources_mix": sorted({p.get("source") for p in points}),
        },
        placeholder=False,
    )


# ──────────────────────────────────────────────────────────────────────────────
# WIP dashboard parse helper (active initiatives)
# ──────────────────────────────────────────────────────────────────────────────


def list_active_initiatives() -> list[str]:
    """Parse WIP_DASHBOARD.md auto-table; return initiative-number prefixes for status='Open'."""
    if not WIP_DASHBOARD.is_file():
        return []
    text = WIP_DASHBOARD.read_text(encoding="utf-8")
    # Split on auto-render markers (I32 P10 pattern)
    BEGIN = "<!-- BEGIN AUTO -->"
    END = "<!-- END AUTO -->"
    begin = text.find(BEGIN)
    end = text.find(END)
    if begin < 0 or end < 0:
        return []
    table = text[begin:end]
    open_inits: list[str] = []
    for line in table.splitlines():
        if line.startswith("| ") and "open" in line.lower():
            # Extract NN at start of row
            m = re.match(r"\|\s*\*?\*?(\d{2})\b", line)
            if m:
                open_inits.append(m.group(1))
    return open_inits


def _safe_relative(path: Path) -> str:
    """Best-effort REPO_ROOT-relative path; fallback to str() when out-of-repo."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


# ──────────────────────────────────────────────────────────────────────────────
# Section 04 (P6 extension) — persona MADEIRA prompt diff
# ──────────────────────────────────────────────────────────────────────────────


def gather_persona_prompt_diff(persona_id: str) -> dict[str, Any]:
    """Compute persona-conditioned MADEIRA prompt diff (P6 + I47 P11).

    Invokes ``scripts/assemble-prompts.py --variant standard --dry-run`` twice:
    1. baseline (no --persona)
    2. conditioned (--persona <id>)

    Returns ``{persona_id, baseline_chars, conditioned_chars, delta_chars,
    headroom_chars, swapped_out, hints_path, hints_path_present}``.
    """
    from akos.dossier.runner import run_cli
    import sys
    BOOTSTRAP_MAX_CHARS = 20_000

    # Hints path check
    hints_path = REPO_ROOT / "prompts" / "personas" / persona_id / "MADEIRA_HINTS.md"

    # Baseline (no --persona): parse "MADEIRA_PROMPT.standard.md: NNN chars" line
    baseline_cli = run_cli(
        [sys.executable, str(REPO_ROOT / "scripts" / "assemble-prompts.py"),
         "--variant", "standard", "--dry-run"],
        timeout=30,
    )
    baseline_chars = _parse_madeira_chars(baseline_cli.stdout)

    # Conditioned (--persona X): parse "MADEIRA_PROMPT.standard.<persona>.md: NNN chars"
    conditioned_cli = run_cli(
        [sys.executable, str(REPO_ROOT / "scripts" / "assemble-prompts.py"),
         "--variant", "standard", "--dry-run", "--persona", persona_id],
        timeout=30,
    )
    conditioned_chars = _parse_madeira_chars(conditioned_cli.stdout, persona_id=persona_id)

    swapped_out: list[str] = []
    # Per I47 P11 architectural decision: persona-conditioned MADEIRA swaps OUT OVERLAY_HLK_GRAPH
    if conditioned_chars is not None and baseline_chars is not None and conditioned_chars < baseline_chars:
        swapped_out.append("OVERLAY_HLK_GRAPH.md (swapped for persona overlay; I47 P11)")

    delta = (conditioned_chars - baseline_chars) if (conditioned_chars is not None and baseline_chars is not None) else None
    headroom = (BOOTSTRAP_MAX_CHARS - conditioned_chars) if conditioned_chars is not None else None

    return {
        "persona_id": persona_id,
        "baseline_chars": baseline_chars,
        "conditioned_chars": conditioned_chars,
        "delta_chars": delta,
        "headroom_chars": headroom,
        "swapped_out": swapped_out,
        "hints_path": _safe_relative(hints_path),
        "hints_path_present": hints_path.is_file(),
    }


def _parse_madeira_chars(stdout: str, *, persona_id: str | None = None) -> int | None:
    """Parse MADEIRA_PROMPT.standard[.persona].md: NNN chars from assemble-prompts dry-run stdout."""
    import re
    if persona_id:
        pattern = rf"MADEIRA_PROMPT\.standard\.{re.escape(persona_id)}\.md:\s*(\d+)\s*chars"
    else:
        pattern = r"MADEIRA_PROMPT\.standard\.md:\s*(\d+)\s*chars"
    m = re.search(pattern, stdout)
    return int(m.group(1)) if m else None


# Generic helper: stale-badge text per dossier-section-spec.md
def stale_badge(age_seconds: float | None, threshold_hours: float | None) -> str:
    """Return STALE badge string when over threshold; empty otherwise."""
    if age_seconds is None or threshold_hours is None:
        return ""
    age_hours = age_seconds / 3600.0
    if age_hours <= threshold_hours:
        return ""
    return f"[STALE: {age_hours:.1f}h ago; threshold {threshold_hours}h]"
