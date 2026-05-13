"""Initiative 49 P10 — quarantine_scenario.py tests."""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path
from typing import Iterable

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_persona_scenario_csv import (
    PERSONA_SCENARIO_REGISTRY_FIELDNAMES,
    VALID_LIFECYCLE_STATUSES,
)


def _load_quarantine_module():
    path = REPO_ROOT / "scripts" / "quarantine_scenario.py"
    spec = importlib.util.spec_from_file_location("scripts.quarantine_scenario", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["scripts.quarantine_scenario"] = mod
    spec.loader.exec_module(mod)
    return mod


qmod = _load_quarantine_module()


def _write_csv(tmp_path: Path, rows: Iterable[dict[str, str]]) -> Path:
    p = tmp_path / "PERSONA_SCENARIO_REGISTRY.csv"
    with p.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES), extrasaction="ignore"
        )
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    return p


def _row(scenario_id: str, *, lifecycle_status: str = "active", notes: str = "") -> dict[str, str]:
    base = {name: "" for name in PERSONA_SCENARIO_REGISTRY_FIELDNAMES}
    base.update({
        "scenario_id": scenario_id,
        "persona_id": "OPERATOR",
        "skill_id": "skill_madeira_lookup_v1",
        "scenario_class": "lookup",
        "difficulty_class": "moderate",
        "expected_route": "hlk_lookup",
        "expected_outcome_class": "PASS",
        "lifecycle_status": lifecycle_status,
        "language": "en",
        "tier": "1",
        "owner_role": "System Owner",
        "notes": notes,
        "priority_score": "1.0000",
        "safety_lane": "false",
        "release_blocking": "false",
    })
    return base


def test_quarantined_is_a_valid_lifecycle_status() -> None:
    assert "quarantined" in VALID_LIFECYCLE_STATUSES


def test_quarantine_active_row_writes_status_and_note(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, [_row("SCN-001"), _row("SCN-002")])
    result = qmod.quarantine_scenario(
        csv_path,
        scenario_id="SCN-001",
        reason="three consecutive judge regressions",
        release=False,
        today="2026-05-03",
    )
    assert result["found"] is True
    assert result["before"] == "active"
    assert result["after"] == "quarantined"
    assert result["note_appended"] is True
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8", newline="")))
    by_id = {r["scenario_id"]: r for r in rows}
    assert by_id["SCN-001"]["lifecycle_status"] == "quarantined"
    assert "I49-QUARANTINE" in by_id["SCN-001"]["notes"]
    assert "2026-05-03" in by_id["SCN-001"]["notes"]
    assert by_id["SCN-002"]["lifecycle_status"] == "active"


def test_release_back_to_active_does_not_append_note(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, [_row("SCN-001", lifecycle_status="quarantined", notes="prior")])
    result = qmod.quarantine_scenario(
        csv_path, scenario_id="SCN-001", reason="", release=True, today="2026-05-03",
    )
    assert result["after"] == "active"
    assert result["note_appended"] is False
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8", newline="")))
    assert rows[0]["lifecycle_status"] == "active"
    assert rows[0]["notes"] == "prior"


def test_dry_run_does_not_persist(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, [_row("SCN-001")])
    result = qmod.quarantine_scenario(
        csv_path,
        scenario_id="SCN-001",
        reason="trial",
        release=False,
        today="2026-05-03",
        dry_run=True,
    )
    assert result["found"] is True
    assert result["dry_run"] is True
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8", newline="")))
    assert rows[0]["lifecycle_status"] == "active"
    assert rows[0]["notes"] == ""


def test_unknown_scenario_id_returns_not_found(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, [_row("SCN-001")])
    result = qmod.quarantine_scenario(
        csv_path, scenario_id="SCN-999", reason="absent", release=False,
    )
    assert result["found"] is False


def test_appended_note_concatenates_existing_notes(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, [_row("SCN-001", notes="prior context")])
    qmod.quarantine_scenario(
        csv_path, scenario_id="SCN-001", reason="judge fail x3",
        release=False, today="2026-05-03",
    )
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8", newline="")))
    assert rows[0]["notes"].startswith("prior context | I49-QUARANTINE 2026-05-03: judge fail x3")


def test_canonical_registry_validator_accepts_quarantined() -> None:
    """Confirm the live PERSONA_SCENARIO_REGISTRY.csv validator path tolerates the new enum."""
    from scripts.validate_persona_scenario_registry import VALID_LIFECYCLE_STATUSES as v_lifecycle
    assert "quarantined" in v_lifecycle


# ---------------------------------------------------------------------------
# I51 P4 D-IH-51-B — --auto-from-flake-history mode
# ---------------------------------------------------------------------------


def _write_policy_csv(tmp_path: Path, rows: list[dict[str, str]]) -> Path:
    """Build a minimal POLICY_REGISTER.csv test fixture."""
    from akos.hlk_policy_register_csv import POLICY_REGISTER_FIELDNAMES

    p = tmp_path / "POLICY_REGISTER.csv"
    with p.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=list(POLICY_REGISTER_FIELDNAMES), extrasaction="ignore"
        )
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    return p


def _flake_policy_row(threshold: int) -> dict[str, str]:
    return {
        "policy_id": "POL-EVAL-FLAKE-THRESHOLD-V1",
        "policy_class": "flake_threshold",
        "applies_to_schema": "compliance",
        "applies_to_table": "persona_scenario_registry_mirror",
        "policy_text": f"min_consecutive_failures={threshold}",
        "cadence": "continuous",
        "owner_role": "System Owner",
        "last_review": "2026-05-03",
        "next_review": "2026-08-03",
        "topic_ids": "topic_policy_register",
        "notes": "I51 P4 test fixture",
    }


def test_flake_threshold_resolves_from_policy(tmp_path: Path) -> None:
    """I51 P4: --auto-from-flake-history reads threshold from POL-EVAL-FLAKE-THRESHOLD-V1."""
    policy_csv = _write_policy_csv(tmp_path, [_flake_policy_row(5)])
    threshold, source = qmod._read_flake_threshold(policy_csv)
    assert threshold == 5
    assert source == "policy"


def test_flake_threshold_default_when_policy_missing(tmp_path: Path) -> None:
    """Falls back to DEFAULT_FLAKE_THRESHOLD when POLICY row is absent."""
    policy_csv = _write_policy_csv(tmp_path, [])
    threshold, source = qmod._read_flake_threshold(policy_csv)
    assert threshold == qmod.DEFAULT_FLAKE_THRESHOLD
    assert source == "default"


def test_flake_threshold_default_when_no_policy_file(tmp_path: Path) -> None:
    """Falls back when POLICY_REGISTER.csv doesn't exist at all."""
    threshold, source = qmod._read_flake_threshold(tmp_path / "missing.csv")
    assert threshold == qmod.DEFAULT_FLAKE_THRESHOLD
    assert source == "default"


def test_load_flake_history_validates_schema(tmp_path: Path) -> None:
    import json
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"not": "a list"}), encoding="utf-8")
    with pytest.raises(ValueError):
        qmod._load_flake_history(bad)
    bad.write_text(json.dumps([{"scenario_id": ""}]), encoding="utf-8")
    with pytest.raises(ValueError):
        qmod._load_flake_history(bad)
    bad.write_text(json.dumps([{"scenario_id": "S", "consecutive_failures": -1}]), encoding="utf-8")
    with pytest.raises(ValueError):
        qmod._load_flake_history(bad)


def test_auto_quarantine_quarantines_above_threshold(tmp_path: Path) -> None:
    csv_path = _write_csv(
        tmp_path,
        [_row("SCN-001"), _row("SCN-002"), _row("SCN-003"), _row("SCN-004")],
    )
    history = [
        {"scenario_id": "SCN-001", "consecutive_failures": 5},
        {"scenario_id": "SCN-002", "consecutive_failures": 1},
        {"scenario_id": "SCN-003", "consecutive_failures": 3},
        {"scenario_id": "SCN-004", "consecutive_failures": 2},
    ]
    summary = qmod.auto_quarantine_from_flake_history(
        csv_path, history, threshold=3, today="2026-05-03",
    )
    assert summary["threshold"] == 3
    assert sorted(summary["quarantined"]) == ["SCN-001", "SCN-003"]
    assert summary["not_found"] == []
    assert sorted(summary["no_change_below_threshold"]) == ["SCN-002", "SCN-004"]
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8", newline="")))
    by_id = {r["scenario_id"]: r for r in rows}
    assert by_id["SCN-001"]["lifecycle_status"] == "quarantined"
    assert "I51-FLAKE-QUARANTINE" in by_id["SCN-001"]["notes"]
    assert "consecutive_failures=5" in by_id["SCN-001"]["notes"]
    assert "POL-EVAL-FLAKE-THRESHOLD-V1" in by_id["SCN-001"]["notes"]
    assert by_id["SCN-002"]["lifecycle_status"] == "active"
    assert by_id["SCN-003"]["lifecycle_status"] == "quarantined"
    assert by_id["SCN-004"]["lifecycle_status"] == "active"


def test_auto_quarantine_skips_already_quarantined(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, [_row("SCN-001", lifecycle_status="quarantined")])
    history = [{"scenario_id": "SCN-001", "consecutive_failures": 10}]
    summary = qmod.auto_quarantine_from_flake_history(
        csv_path, history, threshold=3, today="2026-05-03",
    )
    assert summary["quarantined"] == []
    assert summary["skipped_already_quarantined"] == ["SCN-001"]


def test_auto_quarantine_dry_run_does_not_write(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, [_row("SCN-001")])
    history = [{"scenario_id": "SCN-001", "consecutive_failures": 10}]
    summary = qmod.auto_quarantine_from_flake_history(
        csv_path, history, threshold=3, today="2026-05-03", dry_run=True,
    )
    assert summary["quarantined"] == ["SCN-001"]
    assert summary["dry_run"] is True
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8", newline="")))
    assert rows[0]["lifecycle_status"] == "active"
    assert rows[0]["notes"] == ""


def test_auto_quarantine_reports_unknown_scenarios(tmp_path: Path) -> None:
    csv_path = _write_csv(tmp_path, [_row("SCN-001")])
    history = [{"scenario_id": "SCN-DOESNT-EXIST", "consecutive_failures": 99}]
    summary = qmod.auto_quarantine_from_flake_history(
        csv_path, history, threshold=3, today="2026-05-03",
    )
    assert summary["quarantined"] == []
    assert summary["not_found"] == ["SCN-DOESNT-EXIST"]


def test_canonical_policy_register_has_flake_threshold_row() -> None:
    """The canonical POLICY_REGISTER.csv must define POL-EVAL-FLAKE-THRESHOLD-V1."""
    from akos.hlk_policy_register_csv import POLICY_REGISTER_FIELDNAMES, VALID_POLICY_CLASSES
    p = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "POLICY_REGISTER.csv"
    with p.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    flake_rows = [r for r in rows if r["policy_id"] == "POL-EVAL-FLAKE-THRESHOLD-V1"]
    assert len(flake_rows) == 1, "expected exactly one POL-EVAL-FLAKE-THRESHOLD-V1 row"
    fr = flake_rows[0]
    assert fr["policy_class"] == "flake_threshold"
    assert "flake_threshold" in VALID_POLICY_CLASSES
    assert "min_consecutive_failures=3" in fr["policy_text"]
    assert fr["cadence"] == "continuous"
    # Ensure the row is shape-valid against the canonical fieldnames list.
    assert set(fr.keys()) == set(POLICY_REGISTER_FIELDNAMES)
