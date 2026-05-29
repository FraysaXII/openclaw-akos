"""Tests for scripts/validate_research_radar.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_self_test_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts/validate_research_radar.py"), "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout
