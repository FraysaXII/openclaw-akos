"""Tests for AUDIENCE_REGISTRY (Initiative 85 P1).

Covers:
- Pydantic chassis fieldnames + enums in ``akos/hlk_audience_csv.py``
- ``validate_audience_registry.py`` validator (happy + sad paths)
- Cross-reference resolution for D-IH-85-A in DECISION_REGISTER

Per D-IH-85-A (narrow FK index pattern) + D-IH-85-B (YAML list multi-audience
encoding) + I86 inline-ratify pre-pass ratification on 2026-05-16.
"""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_audience_csv import (
    AUDIENCE_REGISTRY_FIELDNAMES,
    CANONICAL_PATH,
    VALID_REGISTER_SIDES,
    VALID_STATUSES,
)

REGISTRY_PATH = REPO_ROOT / CANONICAL_PATH
VALIDATOR_SCRIPT = REPO_ROOT / "scripts" / "validate_audience_registry.py"
DECISION_REGISTER_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "Compliance" / "canonicals" / "DECISION_REGISTER.csv"
)


# ---------------------------------------------------------------------------
# Pydantic chassis tests
# ---------------------------------------------------------------------------


@pytest.mark.brand
def test_fieldnames_are_complete_and_ordered():
    """Header column order is the immutable schema contract per D-IH-85-A."""
    assert isinstance(AUDIENCE_REGISTRY_FIELDNAMES, tuple)
    assert len(AUDIENCE_REGISTRY_FIELDNAMES) == 14
    assert AUDIENCE_REGISTRY_FIELDNAMES[0] == "audience_code"
    assert AUDIENCE_REGISTRY_FIELDNAMES[1] == "name"
    assert AUDIENCE_REGISTRY_FIELDNAMES[2] == "register_side"
    assert "status" in AUDIENCE_REGISTRY_FIELDNAMES
    assert "linked_decision_id" in AUDIENCE_REGISTRY_FIELDNAMES
    assert "methodology_version_at_review" in AUDIENCE_REGISTRY_FIELDNAMES


@pytest.mark.brand
def test_register_side_enum_complete():
    """Dual-register contract per akos-brand-baseline-reality.mdc requires 3 sides."""
    assert VALID_REGISTER_SIDES == frozenset({"internal", "external", "hybrid"})


@pytest.mark.brand
def test_status_enum_complete():
    """Status enum mirrors akos-executable-process-catalog.mdc Rule 2."""
    assert VALID_STATUSES == frozenset({
        "active", "inactive", "planned", "experimental", "deprecated",
    })


# ---------------------------------------------------------------------------
# CSV content tests (canonical seed integrity)
# ---------------------------------------------------------------------------


@pytest.mark.brand
def test_csv_header_matches_chassis():
    """CSV header MUST equal AUDIENCE_REGISTRY_FIELDNAMES (Pydantic SSOT)."""
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert tuple(reader.fieldnames or ()) == AUDIENCE_REGISTRY_FIELDNAMES


@pytest.mark.brand
def test_csv_has_nine_seed_rows():
    """I85 P0 charter specifies 8 J-* audience codes; I86 Wave J extended to
    9 by adding J-AIC (AICs as internal-and-external receivers per the agentic
    DoD posture; named alongside J-OP internal-operator class).
    """
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 9, f"expected 9 seed rows, got {len(rows)}"


@pytest.mark.brand
def test_csv_audience_codes_are_unique_and_valid():
    """All J-* codes match regex AND are unique."""
    import re
    audience_code_re = re.compile(r"^J-[A-Z]{2,8}$")
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    codes = [r["audience_code"] for r in rows]
    assert len(codes) == len(set(codes)), "duplicate audience_code"
    for c in codes:
        assert audience_code_re.match(c), f"invalid audience_code: {c!r}"


@pytest.mark.brand
def test_csv_required_codes_present():
    """The 8 charter-named codes (J-IN, J-CU, J-PT, J-ENISA, J-AD, J-RC, J-CO, J-OP)
    plus the I86 Wave J extension J-AIC are all present."""
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        codes = {r["audience_code"] for r in csv.DictReader(fh)}
    expected = {"J-IN", "J-CU", "J-PT", "J-ENISA", "J-AD", "J-RC", "J-CO", "J-OP", "J-AIC"}
    assert codes == expected, f"missing or extra codes: missing={expected - codes}, extra={codes - expected}"


@pytest.mark.brand
def test_csv_register_sides_use_valid_enum():
    """Every row's register_side is in the enum."""
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            assert row["register_side"] in VALID_REGISTER_SIDES, (
                f"{row['audience_code']}: register_side {row['register_side']!r} invalid"
            )


@pytest.mark.brand
def test_csv_statuses_use_valid_enum():
    """Every row's status is in the enum."""
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            assert row["status"] in VALID_STATUSES, (
                f"{row['audience_code']}: status {row['status']!r} invalid"
            )


@pytest.mark.brand
def test_csv_jop_is_internal_register():
    """J-OP (operator-internal) MUST carry register_side=internal — load-bearing dual-register invariant."""
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        rows = {r["audience_code"]: r for r in csv.DictReader(fh)}
    assert rows["J-OP"]["register_side"] == "internal"


@pytest.mark.brand
def test_csv_jin_jenisa_are_external_register():
    """J-IN (investor) + J-ENISA (regulator) MUST carry register_side=external per akos-brand-baseline-reality.mdc."""
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        rows = {r["audience_code"]: r for r in csv.DictReader(fh)}
    assert rows["J-IN"]["register_side"] == "external"
    assert rows["J-ENISA"]["register_side"] == "external"


@pytest.mark.brand
def test_csv_jad_jco_are_hybrid_register():
    """J-AD (advisor) + J-CO (collaborator) carry hybrid posture (external until NDA, internal post-NDA)."""
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        rows = {r["audience_code"]: r for r in csv.DictReader(fh)}
    assert rows["J-AD"]["register_side"] == "hybrid"
    assert rows["J-CO"]["register_side"] == "hybrid"


# ---------------------------------------------------------------------------
# Validator script tests (happy path)
# ---------------------------------------------------------------------------


@pytest.mark.brand
def test_validator_script_passes_on_canonical():
    """Standalone validator returns exit 0 on the canonical CSV."""
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_SCRIPT)],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, (
        f"validator failed unexpectedly: stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    assert "PASS: AUDIENCE_REGISTRY validated" in result.stdout


# ---------------------------------------------------------------------------
# DECISION_REGISTER cross-reference test
# ---------------------------------------------------------------------------


@pytest.mark.brand
def test_dih_85_a_in_decision_register():
    """D-IH-85-A (the I85 inception decision FK target) MUST exist in DECISION_REGISTER."""
    with DECISION_REGISTER_PATH.open(encoding="utf-8", newline="") as fh:
        decision_ids = {r["decision_id"] for r in csv.DictReader(fh)}
    assert "D-IH-85-A" in decision_ids


@pytest.mark.brand
def test_all_linked_decision_ids_resolve():
    """Every row's linked_decision_id MUST FK-resolve to DECISION_REGISTER."""
    with DECISION_REGISTER_PATH.open(encoding="utf-8", newline="") as fh:
        decision_ids = {r["decision_id"] for r in csv.DictReader(fh)}
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            ldid = row.get("linked_decision_id", "")
            if ldid:
                assert ldid in decision_ids, (
                    f"{row['audience_code']}: linked_decision_id {ldid!r} not in DECISION_REGISTER"
                )
