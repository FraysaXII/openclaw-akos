"""Initiative 19: finops ledger Phase 1 staging SQL parity."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = REPO_ROOT / "scripts" / "sql" / "i19_phase1_staging"
MIG_DIR = REPO_ROOT / "supabase" / "migrations"


def test_i19_sql_files_exist() -> None:
    assert (SQL_DIR / "20260423_i19_finops_ledger_phase1_up.sql").is_file()
    assert (SQL_DIR / "20260423_i19_finops_ledger_phase1_rollback.sql").is_file()


def test_i19_up_sql_contains_schema_table_rls() -> None:
    up = (SQL_DIR / "20260423_i19_finops_ledger_phase1_up.sql").read_text(encoding="utf-8")
    assert "CREATE SCHEMA IF NOT EXISTS finops" in up
    assert "finops.registered_fact" in up
    assert "ENABLE ROW LEVEL SECURITY" in up
    assert "registered_fact_deny_anon" in up
    assert "counterparty_id" in up


def test_i19_migration_parity_file_exists() -> None:
    mig = list(MIG_DIR.glob("*_i19_finops_ledger_phase1.sql"))
    assert len(mig) == 1
    body = mig[0].read_text(encoding="utf-8")
    assert "finops.registered_fact" in body
    assert "registered_fact_deny_authenticated" in body
