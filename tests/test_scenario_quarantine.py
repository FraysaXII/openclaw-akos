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
