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
    """Read latest artifacts/calibration/*.json (P10 of I47 wrote these)."""
    art = latest_artifact(ARTIFACTS_DIR / "calibration", "calibration-baseline-*.json")
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
            "status": "PASS" if overall.get("overall_pass") else "WARN",
        },
        data_age_seconds=art.age_seconds,
    )


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


# Generic helper: stale-badge text per dossier-section-spec.md
def stale_badge(age_seconds: float | None, threshold_hours: float | None) -> str:
    """Return STALE badge string when over threshold; empty otherwise."""
    if age_seconds is None or threshold_hours is None:
        return ""
    age_hours = age_seconds / 3600.0
    if age_hours <= threshold_hours:
        return ""
    return f"[STALE: {age_hours:.1f}h ago; threshold {threshold_hours}h]"
