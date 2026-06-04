"""Tests for data_contract_registry_check runbook (I93 P2b)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_data_contract_registry_check_self_test() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/data_contract_registry_check.py", "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_data_contract_registry_check_coverage_report() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/data_contract_registry_check.py", "--coverage-report"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "seed_only" in result.stdout
