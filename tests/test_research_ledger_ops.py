"""Tests for research ledger prong normalization (BL-* lattice)."""
from akos.research_ledger_ops import (
    BASELINE_PRONG_IDS,
    normalize_prong,
    resolve_prong_for_script,
    validate_row_dict,
)


def test_normalize_prong_baseline_passthrough():
    assert normalize_prong("BL-TECH") == "BL-TECH"
    assert normalize_prong("bl-data") == "BL-DATA"


def test_normalize_prong_charter_aliases():
    assert normalize_prong("P1-TECH") == "BL-TECH"
    assert normalize_prong("P1-DATA") == "BL-DATA"
    assert normalize_prong("P8-MADEIRA") == "BL-ENVOY"
    assert normalize_prong("P12-RPA-ADAPTERS") == "BL-ADAPTER"
    assert normalize_prong("P7-AGENT-CLI") == "BL-ENVOY"


def test_normalize_prong_empty_defaults():
    assert normalize_prong("") == "BL-TECH"
    assert normalize_prong(None) == "BL-TECH"


def test_validate_row_dict_normalizes_prong():
    row = validate_row_dict(
        {
            "source_id": "SRC-TEST-001",
            "prong": "P2-DATA",
            "topic_cluster": "test",
            "source_title_or_owner": "t",
            "url": "docs/wip/intelligence/x/source-ledger.csv",
            "format": "internal_canonical",
            "source_category": "CORPINT",
            "source_level": "5.1",
            "holistika_reliability_score": "5",
            "external_perceived_credibility_score": "3",
            "control_confidence_level": "Safe",
            "decision_use": "test",
            "notes": "",
        }
    )
    assert row.prong == "BL-DATA"


def test_resolve_prong_manifest_normalized():
    prong, note = resolve_prong_for_script(
        "scripts/foo.py",
        runbook_map={},
        manifest_prong="P6-COMPLIANCE",
    )
    assert prong == "BL-COMPLY"
    assert note == "prong-binding:manifest"


def test_normalize_prong_finance_typo_alias():
    assert normalize_prong("BL-FINANCE") == "BL-FIN"


def test_baseline_registry_count():
    assert len(BASELINE_PRONG_IDS) == 14
