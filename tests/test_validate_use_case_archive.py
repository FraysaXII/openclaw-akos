"""Tests for USE_CASE_ARCHIVE validator (I82 P4 / Wave Q CSV 3)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from akos.hlk_use_case_archive_csv import UseCaseArchiveRow

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_validate_use_case_archive_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_use_case_archive.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_use_case_id_pattern_rejects_freeform() -> None:
    with pytest.raises(Exception):
        UseCaseArchiveRow(
            use_case_id="usecase-1",
            capability_id="CAP-X",
            engagement_id="",
            realised_at="2026-05-22",
            realised_by="PMO",
            outcome_summary="summary",
            evidence_paths="",
            audience_tags="",
            channel_tag="",
            artifact_class_id="",
            quality_self_rating=3,
            lifecycle_event="first_realisation",
            notes="",
            last_review_at="2026-05-22",
            last_review_by="PMO",
            last_review_decision_id="D-IH-82-R",
            methodology_version_at_review="v3.1",
        )


def test_lifecycle_event_enum_enforced() -> None:
    with pytest.raises(Exception):
        UseCaseArchiveRow(
            use_case_id="USE-000099",
            capability_id="CAP-X",
            engagement_id="",
            realised_at="2026-05-22",
            realised_by="PMO",
            outcome_summary="summary",
            evidence_paths="",
            audience_tags="",
            channel_tag="",
            artifact_class_id="",
            quality_self_rating=3,
            lifecycle_event="invented_lifecycle_event",
            notes="",
            last_review_at="2026-05-22",
            last_review_by="PMO",
            last_review_decision_id="D-IH-82-R",
            methodology_version_at_review="v3.1",
        )
