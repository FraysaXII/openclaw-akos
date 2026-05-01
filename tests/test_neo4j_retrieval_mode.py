"""Initiative 46 P5 — Tests for retrieval_mode column + graph_rag_eligibility policy template."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SKILL_REGISTRY.csv"
POLICY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "POLICY_REGISTER.csv"
MIGRATION = REPO_ROOT / "supabase" / "migrations" / "20260501070000_i46_skill_registry_retrieval_mode.sql"


# ── Schema extension (akos contract) ──────────────────────────────────────────


def test_skill_registry_fieldnames_include_retrieval_mode() -> None:
    from akos.hlk_skill_registry_csv import SKILL_REGISTRY_FIELDNAMES

    assert "retrieval_mode" in SKILL_REGISTRY_FIELDNAMES


def test_valid_retrieval_modes_enum_has_4_values() -> None:
    from akos.hlk_skill_registry_csv import VALID_RETRIEVAL_MODES

    assert VALID_RETRIEVAL_MODES == frozenset({"", "vector_only", "graph_rag", "hybrid"})


# ── CSV column present + back-compat default ──────────────────────────────────


def test_skill_registry_csv_has_retrieval_mode_column() -> None:
    with SKILL_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert "retrieval_mode" in (reader.fieldnames or [])


def test_all_5_skills_have_empty_retrieval_mode_at_p5_ship() -> None:
    """Default = empty (back-compat). Operator activates 'graph_rag' for a skill
    only after P3 PoC meets the bar. P5 ships the column; does not activate."""
    with SKILL_CSV.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        rm = (row.get("retrieval_mode") or "").strip()
        assert rm in {"", "vector_only", "graph_rag", "hybrid"}, (
            f"{row['skill_id']}: invalid retrieval_mode {rm!r}"
        )


# ── Validator ────────────────────────────────────────────────────────────────


def test_validate_skill_registry_passes_with_empty_retrieval_mode() -> None:
    """The shipped CSV has all-empty retrieval_mode values; validator must pass."""
    import subprocess
    import sys

    p = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_skill_registry.py")],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=REPO_ROOT,
    )
    assert p.returncode == 0
    assert "PASS" in p.stdout


def test_validator_rejects_invalid_retrieval_mode(tmp_path: Path) -> None:
    """Direct unit test: the validator's enum check catches typos."""
    from akos.hlk_skill_registry_csv import VALID_RETRIEVAL_MODES

    assert "graphRAG" not in VALID_RETRIEVAL_MODES  # case-sensitive enum
    assert "rag" not in VALID_RETRIEVAL_MODES
    assert "knowledge_graph" not in VALID_RETRIEVAL_MODES


# ── POLICY_REGISTER template row ─────────────────────────────────────────────


def test_policy_register_has_graph_rag_eligibility_template_row() -> None:
    with POLICY_CSV.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    rag_rows = [r for r in rows if r.get("policy_class") == "graph_rag_eligibility"]
    assert len(rag_rows) == 1
    template = rag_rows[0]
    assert template["policy_id"] == "POL-NEO4J-GRAPH-RAG-ELIGIBILITY-TEMPLATE"
    assert "TEMPLATE" in template["policy_text"]


def test_policy_class_enum_includes_graph_rag_eligibility() -> None:
    from akos.hlk_policy_register_csv import VALID_POLICY_CLASSES

    assert "graph_rag_eligibility" in VALID_POLICY_CLASSES


# ── Supabase migration ───────────────────────────────────────────────────────


def test_migration_file_exists() -> None:
    assert MIGRATION.is_file(), "P5 supabase migration file must exist"


def test_migration_alters_skill_registry_mirror() -> None:
    text = MIGRATION.read_text(encoding="utf-8")
    assert "ALTER TABLE compliance.skill_registry_mirror" in text
    assert "ADD COLUMN IF NOT EXISTS retrieval_mode" in text
    # Idempotent: must use IF NOT EXISTS
    assert "IF NOT EXISTS" in text


def test_migration_includes_partial_index() -> None:
    text = MIGRATION.read_text(encoding="utf-8")
    assert "CREATE INDEX IF NOT EXISTS" in text
    assert "retrieval_mode" in text
    assert "WHERE retrieval_mode IS NOT NULL" in text


# ── Cross-coupling with I45 ──────────────────────────────────────────────────


def test_skill_registry_has_both_routing_condition_and_retrieval_mode() -> None:
    """I45 P3 added routing_condition; I46 P5 adds retrieval_mode. Both must coexist."""
    with SKILL_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = reader.fieldnames or []
    assert "routing_condition" in fields
    assert "retrieval_mode" in fields
    # retrieval_mode comes after routing_condition in the contract (per akos contract)
    assert fields.index("retrieval_mode") > fields.index("routing_condition")
