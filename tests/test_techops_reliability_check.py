"""Tests for TechOps reliability check chassis (I90 P3b / OPS-86-9)."""

from __future__ import annotations

import pytest

from akos.hlk_techops_reliability import (
    VALID_TECHOPS_DIMENSION_CODES,
    VALID_TECHOPS_VERDICTS,
    TechOpsFindingRow,
    fixture_techops_finding_row,
    fixture_techops_sweep_report,
)
from scripts.techops_reliability_check import PROBE_REGISTRY, run_sweep, self_test


@pytest.mark.hlk
def test_fixture_finding_constructs() -> None:
    row = fixture_techops_finding_row()
    assert row.dimension_code in VALID_TECHOPS_DIMENSION_CODES
    assert row.verdict in VALID_TECHOPS_VERDICTS


@pytest.mark.hlk
def test_fixture_report_constructs() -> None:
    report = fixture_techops_sweep_report()
    assert report.total_findings == 1
    assert report.skip_count == 1


@pytest.mark.hlk
def test_invalid_verdict_rejected() -> None:
    with pytest.raises(Exception):
        TechOpsFindingRow(
            dimension_code="TECH-01-UPTIME-SLO",
            verdict="not-a-verdict",  # type: ignore[arg-type]
        )


@pytest.mark.hlk
def test_probe_registry_covers_all_dimensions() -> None:
    assert set(PROBE_REGISTRY.keys()) == set(VALID_TECHOPS_DIMENSION_CODES)


@pytest.mark.hlk
def test_stub_sweep_all_skip() -> None:
    report = run_sweep("preview")
    assert report.total_findings == 7
    assert report.skip_count == 7
    assert report.service_tier == "preview"


@pytest.mark.hlk
def test_self_test_passes() -> None:
    assert self_test() == 0
