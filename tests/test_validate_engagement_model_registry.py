"""Tests for ENGAGEMENT_MODEL_REGISTRY.csv + akos.hlk_engagement_model_csv + validator
(Initiative 73 P1; D-IH-73-C sibling-dimension + D-IH-73-D 7-class taxonomy).

Covers:
- The canonical CSV header matches the SSOT `ENGAGEMENT_MODEL_FIELDNAMES` tuple.
- The seven D-IH-73-D classes are all present in the CSV (taxonomy completeness).
- Each row Pydantic-validates against `EngagementModelRow` (enum, slug, int bounds).
- Per-class enum row content matches the operator-ratified default at D-IH-73-H..M.
- The `outsourced_helper` row carries D-IH-73-E SOC posture (low_trust + access_level=1).
- The `operator_self` row carries D-IH-73-D baseline (internal SOC + access_level=6).
- The validator script (`scripts/validate_engagement_model_registry.py`) exits 0
  against the canonical CSV.
- Invalid input pairs are rejected: bad slug, bad enum, out-of-range access_level.

These tests are registered under the `engagement` lane via the implicit
`tests/test_*.py` collection (the `engagement` group is added to scripts/test.py
GROUPS at I73 P1 commit-time). Default `py scripts/test.py all` covers them.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_engagement_model_csv import (  # noqa: E402
    ENGAGEMENT_MODEL_FIELDNAMES,
    VALID_IP_CLAUSE_CLASSES,
    VALID_KNOWLEDGE_ACCESS_LEVELS,
    VALID_PAYMENT_CADENCES,
    VALID_RETRIBUTION_PATTERNS,
    VALID_SOC_POSTURES,
    VALID_STATUSES,
    EngagementModelRow,
)

CSV_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "People Operations"
    / "canonicals" / "dimensions" / "ENGAGEMENT_MODEL_REGISTRY.csv"
)
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_engagement_model_registry.py"

# Operator-ratified D-IH-73-D 7-class taxonomy
EXPECTED_CLASSES = (
    "eng_model_hourly_consultant",
    "eng_model_milestone_consultant",
    "eng_model_percentage_collaborator",
    "eng_model_apprentice_learner",
    "eng_model_investor_advisor",
    "eng_model_outsourced_helper",
    "eng_model_operator_self",
)


def _read_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_csv_exists():
    assert CSV_PATH.is_file(), f"canonical CSV missing at {CSV_PATH}"


def test_csv_header_matches_fieldnames_tuple():
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
    assert tuple(header) == ENGAGEMENT_MODEL_FIELDNAMES, (
        "ENGAGEMENT_MODEL_REGISTRY.csv header drifted from ENGAGEMENT_MODEL_FIELDNAMES SSOT tuple"
    )


def test_csv_column_count_is_16():
    """D-IH-73-C 16-column schema; matches sibling ENGAGEMENT_REGISTRY.csv flat 16-col pattern
    (no I71 P4 review-stamp suffix — same posture as sibling, per pre-P1 self-checkpoint
    "decided not to do" item).
    """
    assert len(ENGAGEMENT_MODEL_FIELDNAMES) == 16, (
        f"expected 16-column schema; got {len(ENGAGEMENT_MODEL_FIELDNAMES)}"
    )


def test_seven_classes_present():
    rows = _read_rows()
    ids = {(r.get("engagement_model_id") or "").strip() for r in rows}
    assert set(EXPECTED_CLASSES) <= ids, (
        f"D-IH-73-D 7-class taxonomy incomplete; missing {set(EXPECTED_CLASSES) - ids}"
    )


def test_every_row_pydantic_validates():
    rows = _read_rows()
    errors: list[str] = []
    for i, r in enumerate(rows, start=2):
        try:
            EngagementModelRow.model_validate({k: (v or "") for k, v in r.items() if k})
        except ValidationError as exc:
            errors.append(f"row {i}: {exc}")
    assert not errors, "Pydantic validation errors:\n" + "\n".join(errors)


def test_outsourced_helper_carries_d_ih_73_e_soc_posture():
    """D-IH-73-E: outsourced_helper carries low_trust SOC, access_level=1,
    work_product_scope_only knowledge, outsourced_workproduct_only IP clause."""
    rows = {(r["engagement_model_id"]).strip(): r for r in _read_rows()}
    row = rows["eng_model_outsourced_helper"]
    assert row["soc_posture"] == "low_trust"
    assert row["access_level_default"] == "1"
    assert row["knowledge_access_level"] == "work_product_scope_only"
    assert row["ip_clause_class"] == "outsourced_workproduct_only"
    assert row["payment_cadence"] == "per_hour_capped"


def test_operator_self_carries_baseline_internal_posture():
    """D-IH-73-D operator baseline: operator_self carries internal SOC,
    access_level=6, full_internal knowledge, operator_owns_all IP clause."""
    rows = {(r["engagement_model_id"]).strip(): r for r in _read_rows()}
    row = rows["eng_model_operator_self"]
    assert row["soc_posture"] == "internal"
    assert row["access_level_default"] == "6"
    assert row["knowledge_access_level"] == "full_internal"
    assert row["ip_clause_class"] == "operator_owns_all"
    assert row["payment_cadence"] == "none"


def test_apprentice_learner_carries_training_posture():
    """D-IH-73-K apprentice: training_only SOC, access_level=3 (Internal),
    training_curriculum_only knowledge, training_recipient IP clause."""
    rows = {(r["engagement_model_id"]).strip(): r for r in _read_rows()}
    row = rows["eng_model_apprentice_learner"]
    assert row["soc_posture"] == "training_only"
    assert row["access_level_default"] == "3"
    assert row["knowledge_access_level"] == "training_curriculum_only"
    assert row["ip_clause_class"] == "training_recipient"
    assert row["payment_cadence"] == "barter_continuous"


def test_all_status_values_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["status"] in VALID_STATUSES, (
            f"row {r['engagement_model_id']}: status {r['status']!r} not in {sorted(VALID_STATUSES)}"
        )


def test_all_retribution_patterns_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["retribution_pattern"] in VALID_RETRIBUTION_PATTERNS


def test_all_soc_postures_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["soc_posture"] in VALID_SOC_POSTURES


def test_all_ip_clause_classes_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["ip_clause_class"] in VALID_IP_CLAUSE_CLASSES


def test_all_knowledge_access_levels_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["knowledge_access_level"] in VALID_KNOWLEDGE_ACCESS_LEVELS


def test_all_payment_cadences_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["payment_cadence"] in VALID_PAYMENT_CADENCES


def test_invalid_slug_rejected():
    """Slug must match ^eng_model_[a-z0-9_]+$; uppercase / no-prefix rejected."""
    bad_payload = {
        "engagement_model_id": "Bad-Slug",  # uppercase + hyphen
        "engagement_model_name": "Bad",
        "retribution_pattern": "hourly",
        "retribution_unit": "hour",
        "typical_duration": "test",
        "access_level_default": "3",
        "soc_posture": "cleared",
        "ip_clause_class": "standard_consultant",
        "knowledge_access_level": "full_by_engagement",
        "onboarding_pattern": "x",
        "offboarding_pattern": "x",
        "payment_cadence": "per_hour",
        "legal_template_default": "x",
        "historical_examples": "",
        "status": "active",
        "notes": "",
    }
    with pytest.raises(ValidationError):
        EngagementModelRow.model_validate(bad_payload)


def test_invalid_enum_rejected():
    """Unknown retribution_pattern must be rejected by Literal type."""
    bad_payload = {
        "engagement_model_id": "eng_model_test_bad_enum",
        "engagement_model_name": "Bad",
        "retribution_pattern": "not_a_valid_pattern",
        "retribution_unit": "hour",
        "typical_duration": "test",
        "access_level_default": "3",
        "soc_posture": "cleared",
        "ip_clause_class": "standard_consultant",
        "knowledge_access_level": "full_by_engagement",
        "onboarding_pattern": "x",
        "offboarding_pattern": "x",
        "payment_cadence": "per_hour",
        "legal_template_default": "x",
        "historical_examples": "",
        "status": "active",
        "notes": "",
    }
    with pytest.raises(ValidationError):
        EngagementModelRow.model_validate(bad_payload)


def test_invalid_access_level_rejected():
    """access_level_default must be int 0-6; 7 is rejected (Secret+1 out of range)."""
    bad_payload = {
        "engagement_model_id": "eng_model_test_bad_access",
        "engagement_model_name": "Bad",
        "retribution_pattern": "hourly",
        "retribution_unit": "hour",
        "typical_duration": "test",
        "access_level_default": "7",  # out of range 0-6
        "soc_posture": "cleared",
        "ip_clause_class": "standard_consultant",
        "knowledge_access_level": "full_by_engagement",
        "onboarding_pattern": "x",
        "offboarding_pattern": "x",
        "payment_cadence": "per_hour",
        "legal_template_default": "x",
        "historical_examples": "",
        "status": "active",
        "notes": "",
    }
    with pytest.raises(ValidationError):
        EngagementModelRow.model_validate(bad_payload)


def test_validator_script_exits_zero():
    """End-to-end: the validator CLI exits 0 on the canonical CSV."""
    if not VALIDATOR_PATH.is_file():
        pytest.skip(f"validator script not present at {VALIDATOR_PATH}")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, (
        f"validator failed (exit={result.returncode}):\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )
