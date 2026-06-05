"""Tests for finops_monthly_recon (I88 F3)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_finops_monthly_recon_self_test() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/finops_monthly_recon.py", "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_finops_spine_dataops_sweep() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/dataops_quality_check.py",
            "--sweep",
            "--data-fam",
            "FINOPS-SPINE",
            "--data-surface",
            "mirror_table",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DATA-02-MIRROR-PARITY\tclean" in result.stdout
