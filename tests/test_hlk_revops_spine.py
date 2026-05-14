"""Tests for the RevOps Spine SSOT (Initiative 72 P7).

Per `D-IH-72-M`, the spine SSOT (`akos/hlk_revops_spine.py`) and the
migration body must stay aligned. These tests pin the contract so that any
future migration drift fails CI before reaching release-gate.
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

from akos.hlk_revops_spine import (
    DOCUMENTED_JOIN_SEMANTICS,
    EXPECTED_VIEW_COLUMNS,
    SPINE_FK_COLUMNS,
    SPINE_MIGRATION_FILENAME,
    SPINE_PANEL_ROUTE,
    SPINE_PANEL_SLOT,
    SPINE_VIEW_NAME,
)


@pytest.fixture(scope="module")
def migration_body() -> str:
    p = REPO_ROOT / "supabase" / "migrations" / SPINE_MIGRATION_FILENAME
    assert p.exists(), f"spine migration missing at {p}"
    return p.read_text(encoding="utf-8")


def test_spine_migration_filename_pinned() -> None:
    assert SPINE_MIGRATION_FILENAME.startswith("20260514")
    assert SPINE_MIGRATION_FILENAME.endswith(".sql")
    assert "i72_revops_spine" in SPINE_MIGRATION_FILENAME


def test_spine_view_name_namespaced() -> None:
    assert "." in SPINE_VIEW_NAME
    assert SPINE_VIEW_NAME.startswith("governance.")


def test_spine_fk_columns_present_in_migration(migration_body: str) -> None:
    for col in SPINE_FK_COLUMNS:
        assert col in migration_body, f"FK column {col!r} missing from migration"


def test_spine_view_create_present_in_migration(migration_body: str) -> None:
    assert f"CREATE OR REPLACE VIEW {SPINE_VIEW_NAME}" in migration_body


def test_spine_view_columns_membership(migration_body: str) -> None:
    """Every EXPECTED_VIEW_COLUMNS member must appear in the migration body.

    Allows column to appear via either AS alias or bare reference; just
    requires the symbol presence.
    """
    for col in EXPECTED_VIEW_COLUMNS:
        assert col in migration_body, f"view column {col!r} missing from migration"


def test_spine_panel_slot_or_route_in_hlk_erp() -> None:
    erp_p = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "PMO" / "canonicals" / "HLK_ERP_ARCHITECTURE.md"
    assert erp_p.exists()
    body = erp_p.read_text(encoding="utf-8")
    assert SPINE_PANEL_SLOT in body or SPINE_PANEL_ROUTE in body


def test_spine_join_semantics_documented() -> None:
    assert "LEFT JOIN" in DOCUMENTED_JOIN_SEMANTICS
    assert "engagement_template_registry_mirror" in DOCUMENTED_JOIN_SEMANTICS
    assert "registered_fact" in DOCUMENTED_JOIN_SEMANTICS


def test_spine_grant_select_to_service_role(migration_body: str) -> None:
    assert "GRANT SELECT ON" in migration_body
    assert "service_role" in migration_body
