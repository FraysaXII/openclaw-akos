"""Tests for workspace fleet hygiene sweep."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from akos.hlk_fleet_hygiene import (
    FLEET_FINDING_FIELDNAMES,
    STANDING_OPS_WATCH_IDS,
    VALID_FLEET_DIMENSION_CODES,
    FleetFindingRow,
    fixture_fleet_finding_row,
    fixture_fleet_sweep_report,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "workspace_fleet_hygiene_sweep.py"


@pytest.mark.hlk
def test_fleet_finding_row_validates() -> None:
    row = fixture_fleet_finding_row()
    assert row.dimension_code in VALID_FLEET_DIMENSION_CODES
    assert len(FLEET_FINDING_FIELDNAMES) == 6


@pytest.mark.hlk
def test_fleet_sweep_report_fixture() -> None:
    report = fixture_fleet_sweep_report()
    assert report.total_findings == 1
    assert report.clean_count == 1


@pytest.mark.hlk
def test_standing_ops_watch_list_nonempty() -> None:
    assert "OPS-81-1" in STANDING_OPS_WATCH_IDS
    assert len(STANDING_OPS_WATCH_IDS) >= 4


@pytest.mark.hlk
def test_self_test_exits_zero() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--self-test"],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


@pytest.mark.hlk
def test_sweep_runs_on_akos() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--sweep", "--no-write-artifacts"],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode in (0, 1)
    assert "Fleet hygiene" in proc.stdout + proc.stderr
