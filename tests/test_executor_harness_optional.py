"""Optional SWE-bench-style oracle: patch + pytest in an ephemeral copy (swarm scope).

Enable with ``AKOS_EXECUTOR_HARNESS=1``. Default CI skips this marker.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "executor_harness_micro"


pytestmark = pytest.mark.executor_harness


@pytest.mark.skipif(
    os.environ.get("AKOS_EXECUTOR_HARNESS") != "1",
    reason="set AKOS_EXECUTOR_HARNESS=1 to run ephemeral patch oracle",
)
def test_executor_harness_patch_then_pytest_passes(tmp_path: Path) -> None:
    dest = tmp_path / "micro"
    shutil.copytree(FIXTURE, dest)
    oracle = dest / "value_check.py"
    proc_fail = subprocess.run(
        [sys.executable, "-m", "pytest", str(oracle), "-q"],
        cwd=dest,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc_fail.returncode != 0, proc_fail.stdout + proc_fail.stderr

    mod_path = dest / "target_module.py"
    mod_path.write_text('"""patched"""\nVALUE = 2\n', encoding="utf-8")

    proc_ok = subprocess.run(
        [sys.executable, "-m", "pytest", str(oracle), "-q"],
        cwd=dest,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc_ok.returncode == 0, proc_ok.stdout + proc_ok.stderr
