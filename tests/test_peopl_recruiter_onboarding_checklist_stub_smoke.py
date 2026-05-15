"""Smoke test for scripts/peopl_recruiter_onboarding_checklist_stub.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_peopl_recruiter_onboarding_checklist_stub_smoke() -> None:
    script = REPO_ROOT / "scripts" / "peopl_recruiter_onboarding_checklist_stub.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
