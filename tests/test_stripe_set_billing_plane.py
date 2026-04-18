"""Smoke: stripe_set_billing_plane.py argparse exits 0 on --help."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_stripe_set_billing_plane_help() -> None:
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "stripe_set_billing_plane.py"), "--help"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr
    assert "hlk_billing_plane" in r.stdout
