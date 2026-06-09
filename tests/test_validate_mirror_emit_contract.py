"""Tests for scripts/validate_mirror_emit_contract.py (P95-GOV-3 registry-driven contract)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_mirror_emit_contract.py"
WORKFLOW = REPO_ROOT / ".github/workflows/supabase-mirror-sync.yml"

ENGAGEMENT_TEMPLATE_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/"
    "dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv"
)


@pytest.fixture(scope="module")
def emit_module():
    spec = importlib.util.spec_from_file_location(
        "validate_mirror_emit_contract_under_test", SCRIPT_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["validate_mirror_emit_contract_under_test"] = module
    spec.loader.exec_module(module)
    return module


def test_load_emit_contracts_from_registry_not_hardcoded(emit_module):
    contracts = emit_module._load_emit_contracts()
    assert len(contracts) >= 20
    csv_paths = {c[0] for c in contracts}
    assert (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv"
        in csv_paths
    )
    assert (
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/"
        "CAPABILITY_REGISTRY.csv"
        in csv_paths
    )


def test_workflow_paths_cover_registry_active_union(emit_module):
    rows = emit_module.load_registry_rows(emit_module.REGISTRY)
    expected = set(emit_module.plane2_workflow_path_union(rows))
    workflow_paths = emit_module._parse_workflow_push_paths()
    assert ENGAGEMENT_TEMPLATE_PATH in expected
    assert workflow_paths == expected


def test_workflow_wiring_includes_registry_preflight(emit_module):
    rows = emit_module.load_registry_rows(emit_module.REGISTRY)
    errors = emit_module._check_workflow_wiring(rows)
    assert not errors, errors
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "validate_canonical_governance_registry.py" in text


def test_run_checks_pass_offline(emit_module):
    errors = emit_module.run_checks()
    assert not errors, errors
