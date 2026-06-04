"""Tests for production readiness method registry (I93 P5c)."""

from __future__ import annotations

from pathlib import Path

from akos.hlk_production_readiness_methods import PRODUCTION_READINESS_METHODS

REPO_ROOT = Path(__file__).resolve().parent.parent
SOP_PATH = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "SOP-DATA_PRODUCTION_READINESS_001.md"
)


def test_production_readiness_methods_registry_has_three_methods() -> None:
    assert set(PRODUCTION_READINESS_METHODS) == {
        "PROD-METHOD-INTERNAL",
        "PROD-METHOD-CLIENT-MS",
        "PROD-METHOD-HYBRID",
    }


def test_upstream_sop_paths_exist() -> None:
    for method in PRODUCTION_READINESS_METHODS.values():
        path = REPO_ROOT / method["paired_upstream_sop"]
        assert path.is_file(), f"missing upstream SOP: {method['paired_upstream_sop']}"


def test_sop_references_method_ids() -> None:
    text = SOP_PATH.read_text(encoding="utf-8")
    for method_id in PRODUCTION_READINESS_METHODS:
        assert method_id in text
