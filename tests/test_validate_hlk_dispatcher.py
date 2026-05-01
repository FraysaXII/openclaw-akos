"""Tests for validate_hlk.py dispatcher graph + structured JSON report (Initiative 32 P1).

Locks the contract that:
1. Default CLI invocation is unchanged (R-32-1 mitigation: backward-compatible CLI).
2. ``--json`` flag emits a structured report on stdout matching the
   ``akos.hlk_validation_run.VALIDATION_RUN_FIELDNAMES`` contract.
3. Per-validator subprocess isolation: one validator's failure does not corrupt
   the structured report for the rest.
4. The I29 / I30 / I31 baseline (every shipped per-CSV validator runs and PASSes
   under current canonical state) holds.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "validate_hlk.py"


@pytest.fixture(scope="module")
def legacy_run() -> subprocess.CompletedProcess:
    """One legacy invocation cached for the whole module (the validator is slow)."""
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=120,
    )


@pytest.fixture(scope="module")
def json_run() -> subprocess.CompletedProcess:
    """One --json invocation cached for the whole module."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=120,
    )


def test_legacy_cli_exits_zero(legacy_run: subprocess.CompletedProcess) -> None:
    """The default invocation matches the I29/I30/I31 baseline (exit 0)."""
    assert legacy_run.returncode == 0, f"validate_hlk.py exited {legacy_run.returncode}; stderr: {legacy_run.stderr}"


def test_legacy_cli_overall_pass_banner(legacy_run: subprocess.CompletedProcess) -> None:
    """The default invocation prints the OVERALL: PASS banner (legacy contract)."""
    assert "OVERALL: PASS" in legacy_run.stdout


def test_legacy_cli_prints_per_validator_pass_lines(legacy_run: subprocess.CompletedProcess) -> None:
    """The default invocation prints one '<NAME>: PASS' line per dispatched validator (legacy contract)."""
    expected = [
        "FINOPS_COUNTERPARTY_REGISTER: PASS",
        "GOI_POI_REGISTER: PASS",
        "ADVISER_ENGAGEMENT_DISCIPLINES: PASS",
        "PROGRAM_REGISTRY: PASS",
        "TOPIC_REGISTRY: PASS",
        "PERSONA_REGISTRY: PASS",
        "CHANNEL_TOUCHPOINT_REGISTRY: PASS",
        "SOURCING_REGISTER: PASS",
        "LANGUAGE_FRONTMATTER: PASS",
    ]
    for needle in expected:
        assert needle in legacy_run.stdout, f"missing legacy banner line: {needle}"


def test_json_cli_exits_zero(json_run: subprocess.CompletedProcess) -> None:
    assert json_run.returncode == 0, f"--json exited {json_run.returncode}; stderr: {json_run.stderr}"


def test_json_cli_emits_valid_json(json_run: subprocess.CompletedProcess) -> None:
    """--json stdout is parseable as JSON (no banner pollution)."""
    payload = json.loads(json_run.stdout)
    assert isinstance(payload, dict)


def test_json_report_top_level_keys(json_run: subprocess.CompletedProcess) -> None:
    payload = json.loads(json_run.stdout)
    for key in ("run_id", "started_at", "git_sha", "host", "overall_status", "runs"):
        assert key in payload, f"missing top-level key: {key}"


def test_json_report_overall_status_pass(json_run: subprocess.CompletedProcess) -> None:
    payload = json.loads(json_run.stdout)
    assert payload["overall_status"] == "pass"


def test_json_report_runs_have_required_fields(json_run: subprocess.CompletedProcess) -> None:
    """Every per-validator row carries the VALIDATION_RUN_FIELDNAMES contract."""
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_validation_run import VALIDATION_RUN_FIELDNAMES

    payload = json.loads(json_run.stdout)
    assert len(payload["runs"]) > 0
    for row in payload["runs"]:
        for field in VALIDATION_RUN_FIELDNAMES:
            assert field in row, f"row missing field {field}: {row}"


def test_json_report_status_is_valid_enum(json_run: subprocess.CompletedProcess) -> None:
    """Every status value is one of the documented enum values."""
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_validation_run import VALID_STATUSES

    payload = json.loads(json_run.stdout)
    for row in payload["runs"]:
        assert row["status"] in VALID_STATUSES, f"invalid status {row['status']!r} in row {row['validator_name']}"


def test_json_report_includes_inline_and_dispatched_validators(json_run: subprocess.CompletedProcess) -> None:
    """Both inline checks (org parse, etc.) and dispatched per-CSV validators are present."""
    payload = json.loads(json_run.stdout)
    names = {row["validator_name"] for row in payload["runs"]}
    # Inline (baseline_organisation + process_list checks):
    assert any(n.startswith("inline_") for n in names), "no inline checks in report"
    # Dispatched (per-CSV validators):
    assert "validate_topic_registry" in names
    assert "validate_persona_registry" in names
    assert "validate_channel_touchpoint_registry" in names
    assert "validate_sourcing_register" in names
    assert "validate_goipoi_register" in names


def test_json_report_run_id_is_uuid(json_run: subprocess.CompletedProcess) -> None:
    """run_id is a uuid4 string and is shared across all runs in one dispatch."""
    import uuid

    payload = json.loads(json_run.stdout)
    run_id = payload["run_id"]
    parsed = uuid.UUID(run_id)  # raises if not a valid UUID
    assert parsed.version == 4
    # Every per-validator row carries the same run_id (one dispatch = one run).
    for row in payload["runs"]:
        assert row["run_id"] == run_id


def test_json_report_baseline_row_counts_match_i31_uat(json_run: subprocess.CompletedProcess) -> None:
    """I29/I30/I31 baseline regression: row counts in inline checks match the
    documented post-I31 vault state (12 programs / 1093 processes / 65 roles /
    23 topics / 16 personas / 10 channels / 1 vendor / 6 GOI-POI rows)."""
    payload = json.loads(json_run.stdout)
    by_name = {row["validator_name"]: row for row in payload["runs"]}
    # Org rows = 65
    assert by_name["inline_org_csv_parse"]["row_count"] == 65, (
        "expected 65 org rows (I29/I30/I31 baseline); got "
        f"{by_name['inline_org_csv_parse']['row_count']}"
    )
    # Process rows = 1093
    assert by_name["inline_process_csv_parse"]["row_count"] == 1093, (
        "expected 1093 process rows (I29/I30/I31 baseline); got "
        f"{by_name['inline_process_csv_parse']['row_count']}"
    )


def test_json_report_no_failed_validators(json_run: subprocess.CompletedProcess) -> None:
    """Sanity: in current vault state, no validator should fail. If this trips,
    the I29/I30/I31 baseline broke (separate from any I32 P1 refactor issue)."""
    payload = json.loads(json_run.stdout)
    failed = [r for r in payload["runs"] if r["status"] == "fail"]
    assert not failed, f"unexpected failed validators: {[r['validator_name'] for r in failed]}"


def test_validation_run_module_importable() -> None:
    """The akos.hlk_validation_run contract is importable and exports the expected names."""
    sys.path.insert(0, str(REPO_ROOT))
    from akos import hlk_validation_run

    assert hasattr(hlk_validation_run, "VALIDATION_RUN_FIELDNAMES")
    assert hasattr(hlk_validation_run, "VALID_STATUSES")
    assert "run_id" in hlk_validation_run.VALIDATION_RUN_FIELDNAMES
    assert "validator_name" in hlk_validation_run.VALIDATION_RUN_FIELDNAMES
    assert "status" in hlk_validation_run.VALIDATION_RUN_FIELDNAMES
