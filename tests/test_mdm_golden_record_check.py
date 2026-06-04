"""Tests for mdm_golden_record_check.py (I93 P5)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_mdm_golden_record_self_test_passes():
    result = subprocess.run(
        [sys.executable, "scripts/mdm_golden_record_check.py", "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


def test_mdm_golden_record_report_exits_zero():
    result = subprocess.run(
        [sys.executable, "scripts/mdm_golden_record_check.py", "--report"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
