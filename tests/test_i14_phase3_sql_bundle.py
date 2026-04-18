"""Initiative 14 Phase 3: SQL bundle and verify helper are present."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = REPO_ROOT / "scripts" / "sql" / "i14_phase3_staging"


def test_phase3_sql_files_exist() -> None:
    assert (SQL_DIR / "20260417_i14_phase3_up.sql").is_file()
    assert (SQL_DIR / "20260417_i14_phase3_rollback.sql").is_file()
    assert (SQL_DIR / "verify_staging.sql").is_file()


def test_phase3_up_sql_contains_mirrors_and_rls() -> None:
    up = (SQL_DIR / "20260417_i14_phase3_up.sql").read_text(encoding="utf-8")
    assert "compliance.process_list_mirror" in up
    assert "baseline_organisation_mirror" in up
    assert "holistika_ops.stripe_customer_link" in up
    assert "ENABLE ROW LEVEL SECURITY" in up


def test_verify_phase3_print_only_exits_zero() -> None:
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "verify_phase3_mirror_schema.py"), "--print-only"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout


def test_verify_phase3_skip_if_no_db_exits_zero() -> None:
    env = {k: v for k, v in __import__("os").environ.items() if k not in ("DATABASE_URL", "SUPABASE_DB_URL")}
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "verify_phase3_mirror_schema.py"), "--skip-if-no-db"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    assert "skip" in r.stdout.lower()
