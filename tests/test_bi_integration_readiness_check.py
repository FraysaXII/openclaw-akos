"""Tests for bi_integration_readiness_check.py (I93 P5b)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_bi_integration_readiness_self_test_passes():
    result = subprocess.run(
        [sys.executable, "scripts/bi_integration_readiness_check.py", "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_bi_integration_readiness_report_exits_zero():
    result = subprocess.run(
        [sys.executable, "scripts/bi_integration_readiness_check.py", "--report"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
