"""Tests for CAPABILITY_CONFIDENCE_REGISTRY validator (I82 P3 / Wave Q CSV 2)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from akos.hlk_capability_confidence_csv import CapabilityConfidenceRow

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_validate_capability_confidence_registry_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_capability_confidence_registry.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_aggregate_must_equal_mean() -> None:
    with pytest.raises(ValueError, match="aggregate_confidence"):
        CapabilityConfidenceRow(
            confidence_id="CONF-CAP-X-20260522",
            capability_id="CAP-X",
            substrate_score=1,
            repeatability_score=1,
            quality_score=1,
            translatability_score=1,
            auditability_score=1,
            aggregate_confidence=3.0,
            rating_method="seed_v1_unrated",
            rated_at="2026-05-22",
            rated_by="Capability Curator",
            notes="",
            last_review_at="2026-05-22",
            last_review_by="Capability Curator",
            last_review_decision_id="D-IH-82-Q",
            methodology_version_at_review="v3.1",
        )


def test_valid_seed_row_accepted() -> None:
    row = CapabilityConfidenceRow(
        confidence_id="CONF-CAP-EXAMPLE-20260522",
        capability_id="CAP-EXAMPLE",
        substrate_score=1,
        repeatability_score=1,
        quality_score=1,
        translatability_score=1,
        auditability_score=1,
        aggregate_confidence=1.0,
        rating_method="seed_v1_unrated",
        rated_at="2026-05-22",
        rated_by="Capability Curator",
        notes="",
        last_review_at="2026-05-22",
        last_review_by="Capability Curator",
        last_review_decision_id="D-IH-82-Q",
        methodology_version_at_review="v3.1",
    )
    assert row.aggregate_confidence == 1.0
