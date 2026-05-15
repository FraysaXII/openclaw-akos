"""Smoke test for scripts/check_ethics_learning_review_due.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_check_ethics_learning_review_due_smoke() -> None:
    script = REPO_ROOT / "scripts" / "check_ethics_learning_review_due.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--today", "2026-05-15"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
