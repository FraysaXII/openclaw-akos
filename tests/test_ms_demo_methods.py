"""Tests for MS demo factory method registry (I93 P5c)."""

from __future__ import annotations

from pathlib import Path

from akos.hlk_ms_demo_methods import MS_DEMO_METHODS

REPO_ROOT = Path(__file__).resolve().parent.parent
SOP_PATH = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "SOP-DATA_MS_DEMO_FACTORY_001.md"
)


def test_ms_demo_methods_registry_has_two_methods() -> None:
    assert set(MS_DEMO_METHODS) == {"MS-DEMO-METHOD-A", "MS-DEMO-METHOD-B"}


def test_ms_demo_runbooks_exist() -> None:
    for method in MS_DEMO_METHODS.values():
        path = REPO_ROOT / method["runbook_path"]
        assert path.is_file(), f"missing runbook: {method['runbook_path']}"


def test_sop_references_method_ids() -> None:
    text = SOP_PATH.read_text(encoding="utf-8")
    for method_id in MS_DEMO_METHODS:
        assert method_id in text
