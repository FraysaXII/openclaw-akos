"""Tests for scripts/kirbe_sync_daemon.py dry-run report."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def kirbe_mod():
    import importlib.util

    path = REPO_ROOT / "scripts" / "kirbe_sync_daemon.py"
    spec = importlib.util.spec_from_file_location("kirbe_sync_daemon", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_build_drift_report_contains_fingerprints(kirbe_mod):
    rep = kirbe_mod.build_drift_report(run_validate_hlk=False)
    assert rep["authority"] == "canonical_csv_first"
    fp_org = rep["fingerprints"]["baseline_organisation"]
    assert "sha256" in fp_org
    assert fp_org["path"].endswith("baseline_organisation.csv")


def test_cli_writes_report(tmp_path: Path):
    out = tmp_path / "drift.json"
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "kirbe_sync_daemon.py"), "--skip-validate-hlk", "-o", str(out)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "fingerprints" in data


def test_apply_without_env_fails():
    env = os.environ.copy()
    env.pop("KIRBE_SYNC_APPLY", None)
    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "kirbe_sync_daemon.py"),
            "--apply",
            "--i-approve-canonical-writes",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
    )
    assert r.returncode == 3
