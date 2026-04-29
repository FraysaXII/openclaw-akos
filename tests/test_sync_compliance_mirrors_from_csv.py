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
    assert "process_list_rows=1093" in r.stdout
    assert "baseline_organisation_rows=" in r.stdout
    assert "finops_counterparty_register_rows=2" in r.stdout
    assert "goipoi_register_rows=6" in r.stdout
    assert "adviser_engagement_disciplines_rows=6" in r.stdout
    assert "adviser_open_questions_rows=12" in r.stdout
    assert "founder_filed_instruments_rows=1" in r.stdout
    assert "program_registry_rows=12" in r.stdout
    assert "topic_registry_rows=5" in r.stdout
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


def test_sync_finops_counterparty_register_only_sql() -> None:
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".sql", delete=False) as tf:
        out_path = Path(tf.name)
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"),
                "--no-begin-commit",
                "--finops-counterparty-register-only",
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
    assert "compliance.finops_counterparty_register_mirror" in out
    assert "ON CONFLICT (counterparty_id) DO UPDATE SET" in out
    assert "finops_example_cloud_platform" in out
    assert "finops_example_customer" in out


def test_sync_full_emit_includes_counterparty_upserts() -> None:
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".sql", delete=False) as tf:
        out_path = Path(tf.name)
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"),
                "--no-begin-commit",
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
    assert "compliance.baseline_organisation_mirror" in out
    assert "compliance.finops_counterparty_register_mirror" in out
