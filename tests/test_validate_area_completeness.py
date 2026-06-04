"""Tests for area-completeness validator (I93 P0)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_area_completeness import (  # noqa: E402
    VALID_AREA_COMPONENT_CODES,
    VALID_AREA_VERDICTS,
    VALID_SCORED_AREAS,
    AreaCompletenessFindingRow,
    AreaCompletenessReport,
)
from scripts.validate_area_completeness import (  # noqa: E402
    AREA_CONFIG,
    COMPONENT_ORDER,
    PROBE_BY_COMPONENT,
    print_matrix,
    run_sweep,
    self_test,
)

VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_area_completeness.py"


@pytest.mark.hlk
def test_component_codes_count() -> None:
    assert len(VALID_AREA_COMPONENT_CODES) == 14
    assert len(COMPONENT_ORDER) == 14
    assert set(PROBE_BY_COMPONENT) == VALID_AREA_COMPONENT_CODES


@pytest.mark.hlk
def test_area_config_matches_scored_areas() -> None:
    assert set(AREA_CONFIG) == set(VALID_SCORED_AREAS)


@pytest.mark.hlk
def test_finding_row_enums() -> None:
    row = AreaCompletenessFindingRow(
        component_code="AREA-01-PARENT-REDESIGN",
        area="People",
        verdict="pass",
        severity="low",
    )
    assert row.verdict == "pass"
    with pytest.raises(ValidationError):
        AreaCompletenessFindingRow(
            component_code="AREA-01-PARENT-REDESIGN",
            area="People",
            verdict="fresh",  # type: ignore[arg-type]
            severity="low",
        )


@pytest.mark.hlk
def test_self_test_returns_zero() -> None:
    assert self_test() == 0


@pytest.mark.hlk
def test_run_sweep_emits_full_grid() -> None:
    report = run_sweep(sweep_trigger="on_demand", swept_by="pytest")
    assert report.total_findings == len(VALID_SCORED_AREAS) * 14
    assert (
        report.pass_count
        + report.partial_count
        + report.gap_count
        + report.blocked_count
        + report.skip_count
        == report.total_findings
    )


@pytest.mark.hlk
def test_print_matrix_smoke(capsys: pytest.CaptureFixture[str]) -> None:
    report = run_sweep(swept_by="pytest-matrix")
    print_matrix(report)
    out = capsys.readouterr().out
    assert "Area completeness matrix" in out
    assert "People" in out
    assert "Data" in out


@pytest.mark.hlk
def test_cli_self_test() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--self-test"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout


@pytest.mark.hlk
def test_cli_matrix() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--matrix"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert "Area completeness matrix" in result.stdout
