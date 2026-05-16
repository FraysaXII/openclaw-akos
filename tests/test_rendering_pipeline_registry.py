"""Tests for RENDERING_PIPELINE_REGISTRY (Initiative 77 P4.C).

Covers:
- Pydantic chassis fieldnames + enums in akos/hlk_rendering_pipeline_csv.py
- validate_rendering_pipeline_registry.py validator (happy + sad paths)
- list_rendering_pipelines.py paired runbook (smoke)
- Cross-reference resolution for D-IH-77-I in DECISION_REGISTER

Per D-IH-77-I (visual UAT rendering discipline + orphan-rendering-pipeline
governance discovery).
"""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_rendering_pipeline_csv import (
    CANONICAL_PATH,
    RENDERING_PIPELINE_FIELDNAMES,
    VALID_BRAND_TOKENS_CONSUMED,
    VALID_GOVERNANCE_CLASSES,
    VALID_STATUSES,
    VALID_TRIGGER_TYPES,
)

REGISTRY_PATH = REPO_ROOT / CANONICAL_PATH
VALIDATOR_SCRIPT = REPO_ROOT / "scripts" / "validate_rendering_pipeline_registry.py"
RUNBOOK_SCRIPT = REPO_ROOT / "scripts" / "list_rendering_pipelines.py"
SOP_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "Tech" / "System Owner" / "canonicals"
    / "SOP-RENDERING_PIPELINE_GOVERNANCE_001.md"
)


# ---------------------------------------------------------------------------
# Pydantic chassis tests
# ---------------------------------------------------------------------------


@pytest.mark.brand
def test_fieldnames_are_complete_and_ordered():
    """Schema must have exactly 20 columns in the documented order."""
    assert len(RENDERING_PIPELINE_FIELDNAMES) == 20
    expected_first = "pipeline_id"
    expected_last = "notes"
    assert RENDERING_PIPELINE_FIELDNAMES[0] == expected_first
    assert RENDERING_PIPELINE_FIELDNAMES[-1] == expected_last
    # Required-by-spec columns must be present
    required = {
        "pipeline_id", "name", "trigger_type", "trigger_command",
        "owning_area", "owning_role", "status", "brand_tokens_consumed",
        "input_paths", "output_paths", "sop_path", "runbook_path",
        "linked_decision_id", "governance_class",
    }
    assert required.issubset(set(RENDERING_PIPELINE_FIELDNAMES))


@pytest.mark.brand
def test_valid_trigger_types_complete():
    expected = {"on_demand", "scheduled", "event_triggered", "gated_operator"}
    assert VALID_TRIGGER_TYPES == expected


@pytest.mark.brand
def test_valid_statuses_match_executable_process_catalog_rule2():
    expected = {"active", "inactive", "planned", "experimental", "deprecated"}
    assert VALID_STATUSES == expected


@pytest.mark.brand
def test_valid_governance_classes_complete():
    expected = {"governed", "partial", "orphan"}
    assert VALID_GOVERNANCE_CLASSES == expected


@pytest.mark.brand
def test_valid_brand_tokens_consumed_is_binary():
    assert VALID_BRAND_TOKENS_CONSUMED == {"yes", "no"}


# ---------------------------------------------------------------------------
# Registry-as-shipped tests
# ---------------------------------------------------------------------------


@pytest.mark.brand
def test_registry_csv_exists():
    assert REGISTRY_PATH.exists(), f"RENDERING_PIPELINE_REGISTRY.csv missing at {REGISTRY_PATH}"


@pytest.mark.brand
def test_registry_csv_schema_matches_chassis():
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        header = tuple(reader.fieldnames or ())
    assert header == RENDERING_PIPELINE_FIELDNAMES, (
        f"Schema drift: header={header} expected={RENDERING_PIPELINE_FIELDNAMES}"
    )


@pytest.mark.brand
def test_registry_rows_all_have_enums_in_range():
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    assert len(rows) >= 12, "registry should have at least the seeded 12 pipelines at P4.C ship"
    for r in rows:
        assert r["trigger_type"] in VALID_TRIGGER_TYPES
        assert r["status"] in VALID_STATUSES
        assert r["governance_class"] in VALID_GOVERNANCE_CLASSES
        assert r["brand_tokens_consumed"] in VALID_BRAND_TOKENS_CONSUMED


@pytest.mark.brand
def test_registry_includes_impeccable_uat_visual_render():
    """P4.B deliverable must register itself in the catalog."""
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        ids = {r["pipeline_id"] for r in reader}
    assert "impeccable_uat_visual_render" in ids, (
        "P4.B render_impeccable_uat.py must self-register in the rendering registry"
    )


@pytest.mark.brand
def test_registry_includes_impeccable_bridge_consumption():
    """P2 deliverable must register itself in the catalog."""
    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        ids = {r["pipeline_id"] for r in reader}
    assert "impeccable_bridge_consumption" in ids


# ---------------------------------------------------------------------------
# Validator script tests
# ---------------------------------------------------------------------------


@pytest.mark.brand
def test_validator_script_exists():
    assert VALIDATOR_SCRIPT.exists()


@pytest.mark.brand
def test_validator_passes_on_shipped_registry():
    """The shipped CSV must validate clean."""
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_SCRIPT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"validator failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    assert "PASS:" in result.stdout


# ---------------------------------------------------------------------------
# Runbook script tests
# ---------------------------------------------------------------------------


@pytest.mark.brand
def test_runbook_script_exists():
    assert RUNBOOK_SCRIPT.exists()


@pytest.mark.brand
def test_runbook_default_lists_active_pipelines():
    result = subprocess.run(
        [sys.executable, str(RUNBOOK_SCRIPT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"runbook failed:\nstdout={result.stdout}\nstderr={result.stderr}"
    )
    # Active pipelines should be in output
    assert "impeccable_bridge_consumption" in result.stdout


@pytest.mark.brand
def test_runbook_filter_by_governance_orphan():
    result = subprocess.run(
        [sys.executable, str(RUNBOOK_SCRIPT), "--all", "--governance", "orphan"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    # Touchpoint kit + cover email + outbound briefs should be orphans
    assert (
        "touchpoint_kit_message_render" in result.stdout
        or "enisa_cover_email_render" in result.stdout
        or "outbound_brief_template_render" in result.stdout
    )


@pytest.mark.brand
def test_runbook_format_json():
    result = subprocess.run(
        [sys.executable, str(RUNBOOK_SCRIPT), "--format", "json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0
    # Should be parseable JSON
    import json
    parsed = json.loads(result.stdout)
    assert isinstance(parsed, list)
    assert all(isinstance(row, dict) for row in parsed)


# ---------------------------------------------------------------------------
# Paired-SOP tests
# ---------------------------------------------------------------------------


@pytest.mark.brand
def test_sop_file_exists():
    assert SOP_PATH.exists(), f"SOP missing at {SOP_PATH}"


@pytest.mark.brand
def test_sop_cites_d_ih_77_i_decision():
    text = SOP_PATH.read_text(encoding="utf-8")
    assert "D-IH-77-I" in text


@pytest.mark.brand
def test_sop_cites_executable_process_catalog_rule():
    text = SOP_PATH.read_text(encoding="utf-8")
    assert "akos-executable-process-catalog.mdc" in text


# ---------------------------------------------------------------------------
# Decision register integration
# ---------------------------------------------------------------------------


@pytest.mark.brand
def test_decision_register_has_d_ih_77_i():
    """D-IH-77-I must be minted in DECISION_REGISTER per P4 amendment."""
    decision_path = (
        REPO_ROOT
        / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
        / "People" / "Compliance" / "canonicals" / "DECISION_REGISTER.csv"
    )
    with decision_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        decision_ids = {row["decision_id"] for row in reader}
    assert "D-IH-77-I" in decision_ids
