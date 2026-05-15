"""Smoke tests for I73 People Operations engagement runbook scripts.

Runs each ``scripts/peopl_engagement*.py`` with CPython and asserts exit code 0.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _peopl_scripts() -> list[Path]:
    return sorted((REPO_ROOT / "scripts").glob("peopl_engagement*.py"))


@pytest.mark.parametrize("script_path", _peopl_scripts(), ids=lambda p: p.name)
def test_peopl_engagement_script_smoke(script_path: Path) -> None:
    assert script_path.is_file()
    proc = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
