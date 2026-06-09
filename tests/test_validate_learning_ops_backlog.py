"""Tests for LEARNING_OPS_BACKLOG.csv + validate_learning_ops_backlog (P95-GOV-4)."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_learning_ops_backlog_csv import (  # noqa: E402
    LEARNING_OPS_BACKLOG_FIELDNAMES,
    LearningOpsBacklogRow,
)

CSV_PATH = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Learning/canonicals/dimensions"
    / "LEARNING_OPS_BACKLOG.csv"
)
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_learning_ops_backlog.py"


def test_header_matches_fieldnames_tuple() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        assert list(csv.DictReader(fh).fieldnames or []) == list(LEARNING_OPS_BACKLOG_FIELDNAMES)


def test_canonical_rows_pydantic_validate() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            LearningOpsBacklogRow.model_validate({k: (v or "") for k, v in row.items()})


def test_invalid_cohort_id_rejected() -> None:
    sample = {
        "cohort_id": "not-a-cohort",
        "engagement_model_id": "eng_model_apprentice_learner",
        "methodology_version_at_onboarding": "methodology-anchor",
        "start_date": "2026-05-15",
        "status": "planned",
        "notes": "",
    }
    with pytest.raises(ValidationError):
        LearningOpsBacklogRow.model_validate(sample)


def test_validator_script_passes_on_canonical_csv() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_validator_self_test() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
