"""Tests for CAPABILITY_REGISTRY validator (I82 P2 / Wave Q)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_validate_capability_registry_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_capability_registry.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
