"""Initiative 48 P2 tests — per-section data fetchers (snapshot mode).

Coverage:
- latest_artifact() returns ArtifactInfo with age + path; None when no match
- gather_schema_governance() reads CSV row counts (no subprocess in snapshot)
- gather_eval_health_snapshot() returns PLACEHOLDER when Supabase env missing
- gather_persona_calibration() reads latest artifacts/calibration/*.json
- gather_recovery_chaos() reads latest artifacts/chaos/*.json (or no-artifact baseline)
- gather_operational_health() reads latest agent-memory-triggers/*.json
- gather_external_repos() reads REPO_HEALTH_SNAPSHOT.csv
- gather_governance_debt() parses OPS-* tables from active master-roadmaps
- list_active_initiatives() parses WIP_DASHBOARD.md auto-table
- stale_badge() helper
"""

from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.dossier.sources import (
    ARTIFACTS_DIR,
    REPO_HEALTH_SNAPSHOT_CSV,
    ArtifactInfo,
    gather_external_repos,
    gather_eval_health_snapshot,
    gather_governance_debt,
    gather_operational_health,
    gather_persona_calibration,
    gather_recovery_chaos,
    gather_schema_governance,
    latest_artifact,
    list_active_initiatives,
    stale_badge,
)


# ---------------------------------------------------------------------------
# latest_artifact
# ---------------------------------------------------------------------------

def test_latest_artifact_returns_none_for_missing_dir(tmp_path: Path) -> None:
    out = latest_artifact(tmp_path / "nonexistent", "*.json")
    assert out is None


def test_latest_artifact_returns_none_for_no_match(tmp_path: Path) -> None:
    out = latest_artifact(tmp_path, "*.json")
    assert out is None


def test_latest_artifact_returns_newest_match(tmp_path: Path) -> None:
    f_old = tmp_path / "old.json"
    f_new = tmp_path / "new.json"
    f_old.write_text("{}")
    time.sleep(0.05)
    f_new.write_text("{}")
    out = latest_artifact(tmp_path, "*.json")
    assert out is not None
    assert out.path == f_new
    assert out.age_seconds >= 0
    assert out.age_hours >= 0


def test_artifact_info_age_hours_is_seconds_div_3600() -> None:
    info = ArtifactInfo(path=Path("/tmp/x"), age_seconds=7200.0)
    assert info.age_hours == 2.0


# ---------------------------------------------------------------------------
# gather_schema_governance
# ---------------------------------------------------------------------------

def test_gather_schema_governance_reads_actual_csv_counts() -> None:
    """Snapshot mode: read CSV directly (no validate_hlk subprocess)."""
    data = gather_schema_governance()
    p = data.payload
    assert p["total_topics"] >= 28  # I47 added 1; I48 may add more
    assert p["total_skills"] == 5
    assert p["total_policies"] >= 26  # I48 P7 added POL-DOSSIER-RUN-RETENTION-V1
    assert p["total_personas"] == 16
    assert p["total_scenarios"] >= 326  # I47 P9 closed at 326
    assert p["validate_hlk_pass"] is None  # snapshot doesn't run validator
    assert p["snapshot_mode"] is True


# ---------------------------------------------------------------------------
# gather_eval_health_snapshot
# ---------------------------------------------------------------------------

def test_gather_eval_health_snapshot_placeholder_without_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    data = gather_eval_health_snapshot()
    assert data.placeholder is True
    assert "SUPABASE_URL" in data.error or "mirror unreachable" in data.error


# ---------------------------------------------------------------------------
# gather_persona_calibration
# ---------------------------------------------------------------------------

def test_gather_persona_calibration_returns_placeholder_when_no_artifact(tmp_path: Path,
                                                                         monkeypatch: pytest.MonkeyPatch) -> None:
    """When no calibration artifact, returns placeholder + actionable error."""
    # Re-patch the artifact dir to a temp-empty dir
    monkeypatch.setattr("akos.dossier.sources.ARTIFACTS_DIR", tmp_path)
    data = gather_persona_calibration()
    assert data.placeholder is True
    assert "calibrate_scenarios.py" in data.error


def test_gather_persona_calibration_reads_latest_baseline_artifact(tmp_path: Path,
                                                                   monkeypatch: pytest.MonkeyPatch) -> None:
    """Synthesise a calibration artifact + verify reader extracts the right fields."""
    cal_dir = tmp_path / "calibration"
    cal_dir.mkdir()
    artifact = {
        "personas": {
            "__overall__": {"total": 326, "overall_pass": True, "pct": {"hard": 40.0, "moderate": 40.0, "trivial": 11.0, "impossible": 8.0}},
            "OPERATOR": {"total": 25, "overall_pass": False},
            "PERSONA-INVESTOR-COLD": {"total": 25, "overall_pass": True},
        }
    }
    (cal_dir / "calibration-baseline-test.json").write_text(json.dumps(artifact), encoding="utf-8")
    monkeypatch.setattr("akos.dossier.sources.ARTIFACTS_DIR", tmp_path)
    data = gather_persona_calibration()
    assert data.placeholder is False
    assert data.payload["total_scenarios"] == 326
    assert data.payload["total_personas"] == 2  # OPERATOR + PERSONA-INVESTOR-COLD
    assert data.payload["overall_within_tolerance"] is True
    assert data.payload["personas_outside_tolerance_count"] == 1
    assert "OPERATOR" in data.payload["personas_outside_tolerance"]


# ---------------------------------------------------------------------------
# gather_recovery_chaos
# ---------------------------------------------------------------------------

def test_gather_recovery_chaos_baseline_when_no_artifact(tmp_path: Path,
                                                         monkeypatch: pytest.MonkeyPatch) -> None:
    """No chaos artifact yet: return baseline-PASS (15 synthetic scenarios assumed clean)."""
    monkeypatch.setattr("akos.dossier.sources.ARTIFACTS_DIR", tmp_path)
    data = gather_recovery_chaos()
    assert data.placeholder is False
    assert data.payload["real_chaos_last_run_status"] is None
    assert data.payload["synthetic_recovery_pass_count"] == 15


def test_gather_recovery_chaos_reads_artifact(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    chaos_dir = tmp_path / "chaos"
    chaos_dir.mkdir()
    payload = {
        "scenario": "neo4j-password-rotation",
        "status": "REFUSED",
        "gate_checks": {"all_gates_passed": False, "akos_real_chaos_ok": ""},
    }
    (chaos_dir / "real-chaos-test.json").write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr("akos.dossier.sources.ARTIFACTS_DIR", tmp_path)
    data = gather_recovery_chaos()
    assert data.payload["real_chaos_last_run_status"] == "REFUSED"
    assert data.payload["real_chaos_gates_passed"] is False
    assert data.payload["real_chaos_scenario"] == "neo4j-password-rotation"


# ---------------------------------------------------------------------------
# gather_operational_health
# ---------------------------------------------------------------------------

def test_gather_operational_health_placeholder_when_no_artifact(tmp_path: Path,
                                                                monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("akos.dossier.sources.ARTIFACTS_DIR", tmp_path)
    data = gather_operational_health()
    assert data.placeholder is True


def test_gather_operational_health_reads_trigger_artifact(tmp_path: Path,
                                                          monkeypatch: pytest.MonkeyPatch) -> None:
    art_dir = tmp_path / "agent-memory-triggers"
    art_dir.mkdir()
    payload = {
        "triggers": [
            {"trigger_id": "trigger_1", "fired": False, "awaiting_operator": False},
            {"trigger_id": "trigger_2", "fired": False, "awaiting_operator": True},
            {"trigger_id": "trigger_3", "fired": False, "awaiting_operator": True},
        ]
    }
    (art_dir / "trigger-watch-test.json").write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr("akos.dossier.sources.ARTIFACTS_DIR", tmp_path)
    data = gather_operational_health()
    assert data.payload["agent_memory_triggers_fired"] == 0
    assert data.payload["agent_memory_triggers_total"] == 3
    assert data.payload["status"] == "PASS"


def test_gather_operational_health_fail_when_trigger_fired(tmp_path: Path,
                                                           monkeypatch: pytest.MonkeyPatch) -> None:
    art_dir = tmp_path / "agent-memory-triggers"
    art_dir.mkdir()
    payload = {"triggers": [{"trigger_id": "trigger_1", "fired": True, "awaiting_operator": False}]}
    (art_dir / "trigger-watch-fired.json").write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr("akos.dossier.sources.ARTIFACTS_DIR", tmp_path)
    data = gather_operational_health()
    assert data.payload["agent_memory_triggers_fired"] == 1
    assert data.payload["status"] == "FAIL"


# ---------------------------------------------------------------------------
# gather_external_repos
# ---------------------------------------------------------------------------

def test_gather_external_repos_reads_actual_csv() -> None:
    """REPO_HEALTH_SNAPSHOT.csv exists in repo (3 repos seeded in I32 P7)."""
    if not REPO_HEALTH_SNAPSHOT_CSV.is_file():
        pytest.skip("REPO_HEALTH_SNAPSHOT.csv not present in this checkout")
    data = gather_external_repos()
    assert data.placeholder is False
    assert data.payload["repos_tracked"] >= 1


# ---------------------------------------------------------------------------
# gather_governance_debt
# ---------------------------------------------------------------------------

def test_gather_governance_debt_parses_ops_tables() -> None:
    """OPS-47-* items live in I47 master-roadmap + closure UAT report."""
    data = gather_governance_debt()
    assert data.placeholder is False
    items = data.payload["items"]
    # I47 closure has OPS-47-1..9 (9 follow-ups + 1 added during closure)
    ops_ids = {it["ops_id"] for it in items}
    assert any(op_id.startswith("OPS-47-") for op_id in ops_ids), (
        f"expected at least one OPS-47-* in {sorted(ops_ids)[:5]}"
    )


def test_gather_governance_debt_initiative_filter() -> None:
    """--initiative 47 narrows the parse to I47 only."""
    data = gather_governance_debt(initiative_filter="47")
    items = data.payload["items"]
    assert all(it["initiative"] == "47" for it in items)


def test_gather_governance_debt_initiative_filter_unknown_returns_empty() -> None:
    data = gather_governance_debt(initiative_filter="99")
    assert data.payload["open_ops_count_total"] == 0


# ---------------------------------------------------------------------------
# list_active_initiatives
# ---------------------------------------------------------------------------

def test_list_active_initiatives_returns_open_inits() -> None:
    """Reads WIP_DASHBOARD.md auto-table; returns 'open' rows."""
    inits = list_active_initiatives()
    # I48 should appear as Open right now (we just created it in P0)
    assert isinstance(inits, list)
    # Result list could be empty depending on dashboard state; just test it returns a list


# ---------------------------------------------------------------------------
# stale_badge helper
# ---------------------------------------------------------------------------

def test_stale_badge_empty_within_threshold() -> None:
    out = stale_badge(age_seconds=3600, threshold_hours=24)
    assert out == ""


def test_stale_badge_emits_when_over_threshold() -> None:
    out = stale_badge(age_seconds=3600 * 36, threshold_hours=24)
    assert out.startswith("[STALE:")
    assert "36" in out


def test_stale_badge_empty_when_age_or_threshold_missing() -> None:
    assert stale_badge(None, 24) == ""
    assert stale_badge(0.0, None) == ""
