"""Tests for DataOps quality check chassis (I90 P3c / OPS-86-19)."""

from __future__ import annotations

import pytest

from akos.hlk_dataops_quality import (
    VALID_DATAOPS_DIMENSION_CODES,
    VALID_DATAOPS_VERDICTS,
    DataOpsFindingRow,
    fixture_dataops_finding_row,
    fixture_dataops_sweep_report,
)
from scripts.dataops_quality_check import PROBE_REGISTRY, run_sweep, self_test


@pytest.mark.hlk
def test_fixture_finding_constructs() -> None:
    row = fixture_dataops_finding_row()
    assert row.dimension_code in VALID_DATAOPS_DIMENSION_CODES
    assert row.verdict in VALID_DATAOPS_VERDICTS


@pytest.mark.hlk
def test_fixture_report_constructs() -> None:
    report = fixture_dataops_sweep_report()
    assert report.total_findings == 1
    assert report.skip_count == 1


@pytest.mark.hlk
def test_invalid_verdict_rejected() -> None:
    with pytest.raises(Exception):
        DataOpsFindingRow(
            dimension_code="DATA-01-FK-INTEGRITY",
            verdict="not-a-verdict",  # type: ignore[arg-type]
        )


@pytest.mark.hlk
def test_probe_registry_covers_all_dimensions() -> None:
    assert set(PROBE_REGISTRY.keys()) == set(VALID_DATAOPS_DIMENSION_CODES)


@pytest.mark.hlk
def test_stub_sweep_all_skip() -> None:
    report = run_sweep("mirror_table")
    assert report.total_findings == 7
    assert report.skip_count == 7
    assert report.data_surface == "mirror_table"


@pytest.mark.hlk
def test_self_test_passes() -> None:
    assert self_test() == 0
