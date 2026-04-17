"""Smoke test: merge_process_list_tranche dry-run (empty candidate = no-op)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_merge_process_list_tranche_dry_run_empty_exits_zero() -> None:
    """Use header-only fixture so dry-run stays valid after Initiative 14 rows are merged."""
    cand = REPO_ROOT / "tests" / "fixtures" / "process_list_empty_candidates.csv"
    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "merge_process_list_tranche.py"),
            "--candidate",
            str(cand),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    assert "candidates=0" in r.stdout or "nothing to merge" in r.stdout

