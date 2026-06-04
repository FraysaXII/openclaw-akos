"""Tests for METRICS_REGISTRY and lineage check (I93 P4)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_validate_metrics_registry_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_metrics_registry.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_validate_metrics_registry_self_test() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_metrics_registry.py", "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_data_lineage_check_self_test() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/data_lineage_check.py", "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_data_lineage_check_report() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/data_lineage_check.py", "--report"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Graph parity: PASS" in result.stdout
