"""Initiative 49 P4 tests — Docker engine IPC probe + doctor CLI flag."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.docker_engine_probe import probe_docker_engine

DOCTOR = REPO_ROOT / "scripts" / "doctor.py"


def test_probe_docker_engine_returns_bool_and_message() -> None:
    ok, msg = probe_docker_engine(timeout_sec=0.5)
    assert isinstance(ok, bool)
    assert isinstance(msg, str)
    assert msg.strip()


def test_docker_sandbox_mode_exits_within_timeout() -> None:
    proc = subprocess.run(
        [sys.executable, str(DOCTOR), "--docker-sandbox"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert proc.returncode in (0, 1)
    assert "Docker sandbox preflight" in (proc.stdout or "")


def test_doctor_help_mentions_docker_sandbox() -> None:
    proc = subprocess.run(
        [sys.executable, str(DOCTOR), "--help"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    assert proc.returncode == 0
    assert "--docker-sandbox" in (proc.stdout or "")
