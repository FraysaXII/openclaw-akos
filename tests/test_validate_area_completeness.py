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
    AREA_KIND_ENTITY,
    CRITICAL_COMPONENT_CODES,
    VALID_AREA_COMPONENT_CODES,
    VALID_AREA_KINDS,
    VALID_AREA_VERDICTS,
    VALID_MATURITY_LEVELS,
    VALID_SCORED_AREAS,
    AreaCompletenessFindingRow,
    AreaCompletenessReport,
    level_ge,
)
from scripts.validate_area_completeness import (  # noqa: E402
    AREA_CONFIG,
    COMPONENT_ORDER,
    PROBE_BY_COMPONENT,
    print_matrix,
    print_worklist,
    run_sweep,
    self_test,
)

VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_area_completeness.py"


@pytest.mark.hlk
def test_component_codes_count() -> None:
    # v2 (D-IH-94-A): 16 components (was 14); added AREA-15 placement + AREA-16 file-plan
    assert len(VALID_AREA_COMPONENT_CODES) == 16
    assert len(COMPONENT_ORDER) == 16
    assert set(PROBE_BY_COMPONENT) == VALID_AREA_COMPONENT_CODES
    assert "AREA-15-PLACEMENT-INTEGRITY" in VALID_AREA_COMPONENT_CODES
    assert "AREA-16-FILE-PLAN" in VALID_AREA_COMPONENT_CODES


@pytest.mark.hlk
def test_v2_eight_scored_areas_with_legal() -> None:
    assert len(VALID_SCORED_AREAS) == 8
    assert "Legal" in VALID_SCORED_AREAS


@pytest.mark.hlk
def test_v2_kind_entity_map_covers_all_areas() -> None:
    assert set(AREA_KIND_ENTITY) == set(VALID_SCORED_AREAS)
    for area, profile in AREA_KIND_ENTITY.items():
        assert profile["kind"] in VALID_AREA_KINDS, area
        assert profile["owner_role"]


@pytest.mark.hlk
def test_v2_maturity_and_criticality_on_findings() -> None:
    report = run_sweep(swept_by="pytest-v2")
    for f in report.findings:
        assert f.maturity_level in VALID_MATURITY_LEVELS
        assert f.criticality in {"critical", "enhancing"}
        assert (f.component_code in CRITICAL_COMPONENT_CODES) == (f.criticality == "critical")


@pytest.mark.hlk
def test_v2_area_09_is_enhancing_not_critical() -> None:
    # Calibration finding: paired-SOP+runbook is forward debt, must not gate closure
    assert "AREA-09-PAIRED-SOP-RUNBOOK" not in CRITICAL_COMPONENT_CODES


@pytest.mark.hlk
def test_level_ge() -> None:
    assert level_ge("L3", "L3")
    assert level_ge("L4", "L3")
    assert not level_ge("L2", "L3")


@pytest.mark.hlk
def test_v2_data_finance_complete_for_tier() -> None:
    # v2 must not break the Data/Finance closures: all critical components at L3+
    report = run_sweep(swept_by="pytest-tier")
    for area in ("Data", "Finance"):
        crit = [f for f in report.findings if f.area == area and f.criticality == "critical"]
        assert crit, area
        assert all(level_ge(f.maturity_level, "L3") for f in crit), (
            area,
            [(f.component_code, f.maturity_level) for f in crit if not level_ge(f.maturity_level, "L3")],
        )


@pytest.mark.hlk
def test_v2_print_worklist_smoke(capsys: pytest.CaptureFixture[str]) -> None:
    report = run_sweep(swept_by="pytest-worklist")
    print_worklist(report, area_filter="Legal")
    out = capsys.readouterr().out
    assert "worklist" in out.lower()
    assert "next_action" in out


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
    assert report.total_findings == len(VALID_SCORED_AREAS) * 16
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
