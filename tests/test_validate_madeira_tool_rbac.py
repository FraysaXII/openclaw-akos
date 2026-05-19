"""Tests for scripts/validate_madeira_tool_rbac.py and akos/hlk_madeira_tool_rbac.py per I76 P2."""
from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from akos.hlk_madeira_tool_rbac import (
    MADEIRA_TOOL_RBAC_FIELDNAMES,
    MadeiraToolRbacRegistry,
    MadeiraToolRbacRow,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Envoy Tech Lab"
    / "canonicals"
    / "dimensions"
    / "MADEIRA_TOOL_RBAC.csv"
)


def _import_validator():
    spec = importlib.util.spec_from_file_location(
        "_test_vmt",
        REPO_ROOT / "scripts" / "validate_madeira_tool_rbac.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["_test_vmt"] = module
    spec.loader.exec_module(module)
    return module


def _valid_row(**overrides: str) -> dict[str, str]:
    base: dict[str, str] = {
        "tool_id": "tool_test_read",
        "tool_category_name": "Test read",
        "description": "Test read category",
        "allowed_in_ask": "yes",
        "allowed_in_plan": "yes",
        "allowed_in_agent": "yes",
        "allowed_in_debug": "yes",
        "allowed_in_methodology": "yes",
        "conditional_constraint": "",
        "representative_tools": "Read",
        "provenance": "cursor-native",
        "status": "active",
        "last_review": "2026-05-19",
        "last_review_decision_id": "D-IH-76-A",
        "notes": "",
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Pydantic model tests
# ---------------------------------------------------------------------------


def test_minimal_valid_row_parses() -> None:
    row = MadeiraToolRbacRow(**_valid_row())
    assert row.tool_id == "tool_test_read"


def test_tool_id_pattern_enforced() -> None:
    with pytest.raises(ValidationError):
        MadeiraToolRbacRow(**_valid_row(tool_id="bad-id-with-dash"))


def test_tool_id_must_have_prefix() -> None:
    with pytest.raises(ValidationError):
        MadeiraToolRbacRow(**_valid_row(tool_id="missing_prefix"))


def test_invalid_permission_value_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraToolRbacRow(**_valid_row(allowed_in_ask="maybe"))


def test_invalid_status_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraToolRbacRow(**_valid_row(status="released"))


def test_invalid_provenance_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraToolRbacRow(**_valid_row(provenance="other"))


def test_invalid_date_format_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraToolRbacRow(**_valid_row(last_review="May 19 2026"))


def test_invalid_decision_id_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraToolRbacRow(**_valid_row(last_review_decision_id="D76A"))


def test_closure_decision_id_accepted() -> None:
    row = MadeiraToolRbacRow(**_valid_row(last_review_decision_id="D-IH-17-CLOSURE"))
    assert row.last_review_decision_id == "D-IH-17-CLOSURE"


def test_conditional_without_constraint_fails() -> None:
    with pytest.raises(ValidationError) as exc:
        MadeiraToolRbacRow(**_valid_row(allowed_in_agent="conditional"))
    assert "conditional_constraint must be non-empty" in str(exc.value)


def test_conditional_with_constraint_passes() -> None:
    row = MadeiraToolRbacRow(
        **_valid_row(
            allowed_in_agent="conditional",
            conditional_constraint="Only when audience is internal.",
        )
    )
    assert row.allowed_in_agent == "conditional"


def test_stale_constraint_rejected() -> None:
    """No allowed_in_* cell is 'conditional', but conditional_constraint is non-empty -> reject."""
    with pytest.raises(ValidationError) as exc:
        MadeiraToolRbacRow(
            **_valid_row(conditional_constraint="Stale constraint that should not be here.")
        )
    assert "stale constraint detected" in str(exc.value)


def test_registry_rejects_duplicate_tool_ids() -> None:
    row1 = MadeiraToolRbacRow(**_valid_row(tool_id="tool_a"))
    row2 = MadeiraToolRbacRow(**_valid_row(tool_id="tool_a"))
    with pytest.raises(ValidationError) as exc:
        MadeiraToolRbacRegistry(rows=(row1, row2))
    assert "duplicate tool_id" in str(exc.value)


def test_registry_accepts_distinct_rows() -> None:
    row1 = MadeiraToolRbacRow(**_valid_row(tool_id="tool_a"))
    row2 = MadeiraToolRbacRow(**_valid_row(tool_id="tool_b"))
    registry = MadeiraToolRbacRegistry(rows=(row1, row2))
    assert len(registry.rows) == 2


# ---------------------------------------------------------------------------
# CSV header + integration tests
# ---------------------------------------------------------------------------


def test_canonical_csv_header_matches() -> None:
    assert CSV_PATH.is_file(), f"missing {CSV_PATH}"
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames == list(MADEIRA_TOOL_RBAC_FIELDNAMES)


def test_canonical_csv_all_rows_parse() -> None:
    assert CSV_PATH.is_file(), f"missing {CSV_PATH}"
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = [MadeiraToolRbacRow(**raw) for raw in reader]
    assert len(rows) > 0
    MadeiraToolRbacRegistry(rows=tuple(rows))


def test_canonical_csv_no_duplicate_tool_ids() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        tool_ids = [(raw.get("tool_id") or "").strip() for raw in reader]
    assert len(tool_ids) == len(set(tool_ids))


# ---------------------------------------------------------------------------
# Validator script tests
# ---------------------------------------------------------------------------


def test_validator_passes_on_real_csv() -> None:
    vmt = _import_validator()
    result = vmt.main([])
    assert result == 0


def test_validator_strict_flag_runs_clean_when_decisions_resolve() -> None:
    vmt = _import_validator()
    result = vmt.main(["--strict"])
    assert result == 0
