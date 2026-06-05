"""Tests for FINOPS_TAX_CALENDAR (I88 F2b)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_validate_finops_tax_calendar_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_finops_tax_calendar.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_validate_finops_tax_calendar_self_test() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_finops_tax_calendar.py", "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
