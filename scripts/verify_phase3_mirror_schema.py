#!/usr/bin/env python3
"""Run Initiative 14 §8 verification SQL against Postgres (staging).

Requires `psql` on PATH and `DATABASE_URL` or `SUPABASE_DB_URL` (libpq connection URI).

See `scripts/sql/i14_phase3_staging/verify_staging.sql` and
`docs/wip/planning/14-holistika-internal-gtm-mops/reports/sql-proposal-stack-20260417.md` §8.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERIFY_SQL = REPO_ROOT / "scripts" / "sql" / "i14_phase3_staging" / "verify_staging.sql"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sql-file",
        type=Path,
        default=VERIFY_SQL,
        help="Path to verify_staging.sql",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Print resolved paths and env presence; exit 0",
    )
    parser.add_argument(
        "--skip-if-no-db",
        action="store_true",
        help="Exit 0 when DATABASE_URL / SUPABASE_DB_URL is unset (CI / local without DB)",
    )
    args = parser.parse_args()
    sql_path = args.sql_file
    if not sql_path.is_absolute():
        sql_path = REPO_ROOT / sql_path
    if not sql_path.is_file():
        print("error: SQL file not found:", sql_path, file=sys.stderr)
        return 1

    db_url = os.environ.get("DATABASE_URL") or os.environ.get("SUPABASE_DB_URL")
    psql = shutil.which("psql")
    if args.print_only:
        print("SQL file:", sql_path)
        print("DATABASE_URL or SUPABASE_DB_URL:", "set" if db_url else "unset")
        print("psql:", psql or "not found")
        return 0

    if not db_url:
        if args.skip_if_no_db:
            print("skip: no DATABASE_URL or SUPABASE_DB_URL")
            return 0
        print(
            "error: set DATABASE_URL or SUPABASE_DB_URL; or pass --skip-if-no-db; "
            "manual SQL:",
            sql_path,
            file=sys.stderr,
        )
        return 1
    if not psql:
        print(
            "error: psql not on PATH; install PostgreSQL client tools or run SQL in the Supabase SQL editor",
            file=sys.stderr,
        )
        return 1

    r = subprocess.run(
        [psql, db_url, "-v", "ON_ERROR_STOP=1", "-f", str(sql_path)],
        cwd=str(REPO_ROOT),
        check=False,
    )
    return int(r.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
