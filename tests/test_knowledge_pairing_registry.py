"""Tests for KNOWLEDGE_PAIRING_REGISTRY.csv + akos.hlk_knowledge_pairing_csv + validator
(Initiative 80 P6.5; D-IH-80-H knowledge-pairing-registry mint).

Covers:
- The canonical CSV header matches the SSOT ``KNOWLEDGE_PAIRING_FIELDNAMES`` tuple.
- Each row Pydantic-validates against ``KnowledgePairingRow`` (Literal enums,
  ISO-date last_review, methodology_version regex).
- Every ``pairing_class`` is in ``VALID_PAIRING_CLASSES``.
- Every ``area`` is in ``VALID_AREAS``.
- Every ``authority`` is in ``VALID_AUTHORITIES``.
- Every readiness state column value is in ``VALID_READINESS_STATES``.
- The validator script (``scripts/validate_knowledge_pairing_registry.py``)
  exits 0 against the canonical CSV.
- Invalid input pairs are rejected: bad pairing_class enum, malformed
  last_review date, missing required field.
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

from akos.hlk_knowledge_pairing_csv import (  # noqa: E402
    KNOWLEDGE_PAIRING_FIELDNAMES,
    VALID_AREAS,
    VALID_AUTHORITIES,
    VALID_PAIRING_CLASSES,
    VALID_READINESS_STATES,
    KnowledgePairingRow,
)

CANONICAL_CSV = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Compliance"
    / "canonicals"
    / "dimensions"
    / "KNOWLEDGE_PAIRING_REGISTRY.csv"
)
VALIDATOR_SCRIPT = REPO_ROOT / "scripts" / "validate_knowledge_pairing_registry.py"


@pytest.mark.governance
def test_csv_header_matches_ssot() -> None:
    with CANONICAL_CSV.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        actual_fieldnames = tuple(reader.fieldnames or ())
    assert actual_fieldnames == KNOWLEDGE_PAIRING_FIELDNAMES


@pytest.mark.governance
def test_each_row_pydantic_validates() -> None:
    with CANONICAL_CSV.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert rows, "KNOWLEDGE_PAIRING_REGISTRY.csv must have at least one row"
    for idx, row in enumerate(rows, start=2):
        try:
            KnowledgePairingRow(**row)
        except ValidationError as exc:
            pytest.fail(f"Row {idx} ({row.get('pairing_id')}): {exc}")


@pytest.mark.governance
def test_pairing_class_enum_coverage() -> None:
    with CANONICAL_CSV.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        assert row["pairing_class"] in VALID_PAIRING_CLASSES, (
            f"pairing_class '{row['pairing_class']}' for {row['pairing_id']} "
            f"not in VALID_PAIRING_CLASSES"
        )


@pytest.mark.governance
def test_area_enum_coverage() -> None:
    with CANONICAL_CSV.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        assert row["area"] in VALID_AREAS, (
            f"area '{row['area']}' for {row['pairing_id']} not in VALID_AREAS"
        )


@pytest.mark.governance
def test_authority_enum_coverage() -> None:
    with CANONICAL_CSV.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        assert row["authority"] in VALID_AUTHORITIES, (
            f"authority '{row['authority']}' for {row['pairing_id']} "
            f"not in VALID_AUTHORITIES"
        )


@pytest.mark.governance
def test_readiness_columns_enum_coverage() -> None:
    with CANONICAL_CSV.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    readiness_cols = ("mirror_ready", "hlk_erp_panel_ready", "ai_archivist_ready")
    for row in rows:
        for col in readiness_cols:
            assert row[col] in VALID_READINESS_STATES, (
                f"{col} '{row[col]}' for {row['pairing_id']} "
                f"not in VALID_READINESS_STATES"
            )


@pytest.mark.governance
def test_pairing_id_uniqueness() -> None:
    with CANONICAL_CSV.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    ids = [row["pairing_id"] for row in rows]
    assert len(ids) == len(set(ids)), "Duplicate pairing_id detected"


@pytest.mark.governance
def test_validator_script_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, (
        f"validate_knowledge_pairing_registry.py failed:\n"
        f"stdout={result.stdout}\nstderr={result.stderr}"
    )


@pytest.mark.governance
def test_invalid_pairing_class_rejected() -> None:
    bad_row = {
        "pairing_id": "pair_test_invalid_001",
        "pairing_class": "not_a_valid_class",
        "parent_doc_path": "docs/references/hlk/v3.0/index.md",
        "companion_doc_paths": "docs/references/hlk/v3.0/index.md",
        "area": "People",
        "pattern_id": "pattern_sop_addendum_split",
        "authority": "parent",
        "mirror_ready": "yes",
        "hlk_erp_panel_ready": "yes",
        "ai_archivist_ready": "yes",
        "status": "active",
        "last_review": "2026-05-16",
        "last_review_by": "People Operations Manager",
        "last_review_decision_id": "D-IH-80-H",
        "methodology_version_at_review": "v3.1",
        "notes": "",
    }
    with pytest.raises(ValidationError):
        KnowledgePairingRow(**bad_row)


@pytest.mark.governance
def test_invalid_last_review_date_rejected() -> None:
    bad_row = {
        "pairing_id": "pair_test_invalid_002",
        "pairing_class": "sop_addendum_split",
        "parent_doc_path": "docs/references/hlk/v3.0/index.md",
        "companion_doc_paths": "docs/references/hlk/v3.0/index.md",
        "area": "People",
        "pattern_id": "pattern_sop_addendum_split",
        "authority": "parent",
        "mirror_ready": "yes",
        "hlk_erp_panel_ready": "yes",
        "ai_archivist_ready": "yes",
        "status": "active",
        "last_review": "May 16 2026",
        "last_review_by": "People Operations Manager",
        "last_review_decision_id": "D-IH-80-H",
        "methodology_version_at_review": "v3.1",
        "notes": "",
    }
    with pytest.raises(ValidationError):
        KnowledgePairingRow(**bad_row)


@pytest.mark.governance
def test_invalid_methodology_version_rejected() -> None:
    bad_row = {
        "pairing_id": "pair_test_invalid_003",
        "pairing_class": "sop_addendum_split",
        "parent_doc_path": "docs/references/hlk/v3.0/index.md",
        "companion_doc_paths": "docs/references/hlk/v3.0/index.md",
        "area": "People",
        "pattern_id": "pattern_sop_addendum_split",
        "authority": "parent",
        "mirror_ready": "yes",
        "hlk_erp_panel_ready": "yes",
        "ai_archivist_ready": "yes",
        "status": "active",
        "last_review": "2026-05-16",
        "last_review_by": "People Operations Manager",
        "last_review_decision_id": "D-IH-80-H",
        "methodology_version_at_review": "3.1",
        "notes": "",
    }
    with pytest.raises(ValidationError):
        KnowledgePairingRow(**bad_row)
