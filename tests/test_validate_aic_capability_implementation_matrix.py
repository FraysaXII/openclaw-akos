"""Tests for AIC_CAPABILITY_IMPLEMENTATION_MATRIX validator (I86 Wave R Lane A)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from akos.hlk_aic_capability_implementation_matrix_csv import (
    AICCapabilityImplementationMatrixRow,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_validate_aic_capability_implementation_matrix_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_aic_capability_implementation_matrix.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_matrix_id_pattern_rejects_freeform() -> None:
    with pytest.raises(Exception):
        AICCapabilityImplementationMatrixRow(
            matrix_id="matrix-001",
            capability_id="CAP-X-Y",
            aic_id="AIC-MADEIRA-ON-CURSOR",
            implementation_status="implemented",
            approach_summary="summary",
            tool_catalog_ref="",
            realisation_refs="",
            paired_madeira_task_id="",
            confidence_class="confirmed",
            notes="",
            last_review_at="2026-05-22",
            last_review_by="PMO",
            last_review_decision_id="D-IH-86-CQ",
            methodology_version_at_review="v3.1",
        )


def test_implementation_status_enum_enforced() -> None:
    with pytest.raises(Exception):
        AICCapabilityImplementationMatrixRow(
            matrix_id="ACIM-9999",
            capability_id="CAP-X-Y",
            aic_id="AIC-MADEIRA-ON-CURSOR",
            implementation_status="invented_status",
            approach_summary="summary",
            tool_catalog_ref="",
            realisation_refs="",
            paired_madeira_task_id="",
            confidence_class="confirmed",
            notes="",
            last_review_at="2026-05-22",
            last_review_by="PMO",
            last_review_decision_id="D-IH-86-CQ",
            methodology_version_at_review="v3.1",
        )


def test_confidence_class_enum_enforced() -> None:
    with pytest.raises(Exception):
        AICCapabilityImplementationMatrixRow(
            matrix_id="ACIM-9999",
            capability_id="CAP-X-Y",
            aic_id="AIC-MADEIRA-ON-CURSOR",
            implementation_status="implemented",
            approach_summary="summary",
            tool_catalog_ref="",
            realisation_refs="",
            paired_madeira_task_id="",
            confidence_class="invented_confidence",
            notes="",
            last_review_at="2026-05-22",
            last_review_by="PMO",
            last_review_decision_id="D-IH-86-CQ",
            methodology_version_at_review="v3.1",
        )
