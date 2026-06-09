"""Tests for CANONICAL_GOVERNANCE_REGISTRY path-union helpers (P95-GOV-3)."""

from __future__ import annotations

from pathlib import Path

import pytest

from akos.hlk_canonical_governance_registry_csv import (
    CSV_PATH_RELATIVE,
    MAX_PLANE2_WORKFLOW_PATHS,
    iter_emit_contract_rows,
    load_registry_rows,
    mirror_table_short_name,
    plane2_workflow_path_union,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / CSV_PATH_RELATIVE

ENGAGEMENT_TEMPLATE_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/"
    "dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv"
)


@pytest.fixture(scope="module")
def registry_rows() -> list[dict[str, str]]:
    return load_registry_rows(REGISTRY)


def test_plane2_workflow_path_union_includes_sibling_area_mirrors(registry_rows):
    union = plane2_workflow_path_union(registry_rows)
    assert ENGAGEMENT_TEMPLATE_PATH in union
    assert len(union) <= MAX_PLANE2_WORKFLOW_PATHS
    assert len(union) >= 30


def test_iter_emit_contract_rows_main_and_gap_splice(registry_rows):
    contracts = iter_emit_contract_rows(registry_rows)
    profiles = {(r.get("plane2_emit_profile") or "").strip() for r in contracts}
    assert profiles <= {"main", "gap_splice"}
    assert len(contracts) >= 20
    csv_paths = {r["csv_path"] for r in contracts}
    assert (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv"
        in csv_paths
    )


def test_mirror_table_short_name_touchpoint_alias(registry_rows):
    row = next(
        r
        for r in registry_rows
        if r["governance_id"] == "gov_people_compliance_touchpoint_kit_cell_registry"
    )
    assert mirror_table_short_name(row) == "touchpoint_kit_cell_mirror"


def test_plane2_workflow_path_union_rejects_oversized_union():
    rows = [
        {
            "status": "active",
            "plane2_sync_policy": "active",
            "plane2_workflow_paths": ";".join(f"path/{i}.csv" for i in range(MAX_PLANE2_WORKFLOW_PATHS + 1)),
        }
    ]
    with pytest.raises(ValueError, match="exceeds max"):
        plane2_workflow_path_union(rows)
