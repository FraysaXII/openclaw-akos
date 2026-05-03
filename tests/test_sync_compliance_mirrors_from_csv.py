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
    assert "process_list_rows=1100" in r.stdout
    assert "baseline_organisation_rows=" in r.stdout
    assert "finops_counterparty_register_rows=2" in r.stdout
    assert "goipoi_register_rows=6" in r.stdout
    assert "adviser_engagement_disciplines_rows=6" in r.stdout
    assert "adviser_open_questions_rows=12" in r.stdout
    assert "founder_filed_instruments_rows=1" in r.stdout
    assert "program_registry_rows=12" in r.stdout
    # Initiative 32 P2/P3/P4/P7: +4 topic rows; Initiative 47 P1: +1 (persona_scenario_registry) -> 28.
    assert "topic_registry_rows=28" in r.stdout
    # Initiative 31 P2.1 / P3 / P5.2 — three new dimension registers.
    assert "persona_registry_rows=16" in r.stdout
    # I51 P1 (closes OPS-47-9): persona_scenario_registry mirror reseed wired up.
    # Row count: 326 (I47 base) + 3 telemetry-merged scaffolds (I50 P5) = 329.
    assert "persona_scenario_registry_rows=329" in r.stdout
    assert "channel_touchpoint_registry_rows=10" in r.stdout
    assert "sourcing_register_rows=" in r.stdout
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
    # I51 P1: full bundle MUST now include persona_scenario_registry upserts.
    assert "compliance.persona_scenario_registry_mirror" in out
    assert "ON CONFLICT (scenario_id) DO UPDATE SET" in out


def test_sync_persona_scenario_registry_only_sql() -> None:
    """I51 P1 — persona_scenario_registry mirror reseed (closes OPS-47-9)."""
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".sql", delete=False) as tf:
        out_path = Path(tf.name)
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"),
                "--no-begin-commit",
                "--persona-scenario-registry-only",
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
    assert "compliance.persona_scenario_registry_mirror" in out
    assert "ON CONFLICT (scenario_id) DO UPDATE SET" in out
    # Anchored fixture row from I47 baseline.
    assert "SCN-OP-001-V1" in out
    # Scaffold row from I50 P5 telemetry promotion (one of the 3 merged).
    assert "SCN-OP-TP-001-V1" in out
    # Empty tenant_id should be emitted as NULL (D-IH-47-K shared semantics),
    # not an empty TEXT literal — verify the very first row uses NULL for it.
    first_row = next((line for line in out.splitlines() if "SCN-OP-001-V1" in line), "")
    assert first_row, "expected SCN-OP-001-V1 row in emitted SQL"
    # SCN-OP-001-V1 has empty tenant_id in the CSV; assert the NULL emission.
    assert "'OPERATOR', 'SKILL-MADEIRA-LOOKUP-V1', NULL," in first_row
    # Row count assertion: 329 INSERT statements (one per scenario row).
    insert_count = sum(
        1
        for line in out.splitlines()
        if line.startswith("INSERT INTO compliance.persona_scenario_registry_mirror")
    )
    assert insert_count == 329, f"expected 329 INSERT rows, got {insert_count}"
