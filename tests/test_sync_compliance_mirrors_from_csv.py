"""Smoke tests for sync_compliance_mirrors_from_csv.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_sync_compliance_mirrors_count_only() -> None:
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"), "--count-only"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    assert "process_list_rows=1069" in r.stdout
    assert "baseline_organisation_rows=" in r.stdout
    assert "source_git_sha=" in r.stdout


def test_sync_compliance_mirrors_sql_contains_holistika_and_conflict() -> None:
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".sql", delete=False) as tf:
        out_path = Path(tf.name)
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"),
                "--no-begin-commit",
                "--process-list-only",
                "--output",
                str(out_path),
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert r.returncode == 0, r.stderr + r.stdout
        out = out_path.read_text(encoding="utf-8")
    finally:
        out_path.unlink(missing_ok=True)
    assert "compliance.process_list_mirror" in out
    assert "ON CONFLICT (item_id) DO UPDATE SET" in out
    assert "holistika_gtm_dtp_001" in out
