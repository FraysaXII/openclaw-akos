"""Initiative 18: FINOPS counterparty mirror staging SQL is present."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = REPO_ROOT / "scripts" / "sql" / "i18_phase1_staging"
MIG_DIR = REPO_ROOT / "supabase" / "migrations"


def test_i18_sql_files_exist() -> None:
    assert (SQL_DIR / "20260423_i18_finops_counterparty_mirror_up.sql").is_file()
    assert (SQL_DIR / "20260423_i18_finops_counterparty_mirror_rollback.sql").is_file()


def test_i18_up_sql_contains_mirror_rls() -> None:
    up = (SQL_DIR / "20260423_i18_finops_counterparty_mirror_up.sql").read_text(encoding="utf-8")
    assert "compliance.finops_counterparty_register_mirror" in up
    assert "PRIMARY KEY (counterparty_id)" in up
    assert "ENABLE ROW LEVEL SECURITY" in up
    assert "finops_counterparty_register_mirror_deny_anon" in up
    assert "finops_counterparty_id" in up


def test_i18_migration_parity_file_exists() -> None:
    mig = list(MIG_DIR.glob("*_i18_finops_counterparty_mirror_cutover.sql"))
    assert len(mig) == 1
    body = mig[0].read_text(encoding="utf-8")
    assert "compliance.finops_counterparty_register_mirror" in body
    assert "finops_vendor_register_mirror" in body
