"""Initiative 47 P9 tests — recovery_chaos_runner.py safety gates.

Coverage:
- Default refuses (AKOS_REAL_CHAOS_OK not set)
- Refuses when NEO4J_URI missing
- Refuses when host is in forbidden list (default + AKOS_REAL_CHAOS_FORBIDDEN_HOSTS)
- Refuses --non-interactive without matching --confirm-test-host
- Accepts --non-interactive with matching --confirm-test-host (gate-only, dry-run)
- Dry-run emits planned report; live without Aura key refuses
- Chaos report file is always written
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNNER = REPO_ROOT / "scripts" / "recovery_chaos_runner.py"

# A safe forbidden host (matches DEFAULT_FORBIDDEN_HOSTS in the runner).
FORBIDDEN_HOST = "cpibdpgaarsbfnamudya.databases.neo4j.io"
SAFE_TEST_HOST = "test-throwaway-instance.databases.neo4j.io"


def _run(env: dict[str, str], extra_args: list[str]) -> subprocess.CompletedProcess:
    """Invoke the runner with a clean env + given env vars + args."""
    full_env = {
        # Keep PATH so the python interpreter can find dependencies.
        "PATH": os.environ.get("PATH", ""),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),  # Windows requirement
        **env,
    }
    return subprocess.run(
        [sys.executable, str(RUNNER), "--scenario", "neo4j-password-rotation", *extra_args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=full_env,
        timeout=20,
    )


def test_default_refuses_without_opt_in() -> None:
    """Without AKOS_REAL_CHAOS_OK=1 the runner must refuse with exit 10."""
    res = _run({}, ["--non-interactive", "--confirm-test-host", SAFE_TEST_HOST])
    assert res.returncode == 10
    assert "AKOS_REAL_CHAOS_OK" in (res.stdout + res.stderr)


def test_refuses_without_neo4j_uri() -> None:
    res = _run({"AKOS_REAL_CHAOS_OK": "1"},
               ["--non-interactive", "--confirm-test-host", SAFE_TEST_HOST])
    assert res.returncode == 11
    assert "NEO4J_URI" in (res.stdout + res.stderr)


def test_refuses_against_default_forbidden_host() -> None:
    """MasterData host is in the default forbidden list."""
    res = _run(
        {"AKOS_REAL_CHAOS_OK": "1", "NEO4J_URI": f"neo4j+s://{FORBIDDEN_HOST}:7687"},
        ["--non-interactive", "--confirm-test-host", FORBIDDEN_HOST],
    )
    assert res.returncode == 11
    assert "forbidden" in (res.stdout + res.stderr).lower()


def test_refuses_against_extra_forbidden_host() -> None:
    """AKOS_REAL_CHAOS_FORBIDDEN_HOSTS extends the forbidden list."""
    extra_forbidden = "extra-forbidden.databases.neo4j.io"
    res = _run(
        {
            "AKOS_REAL_CHAOS_OK": "1",
            "NEO4J_URI": f"neo4j+s://{extra_forbidden}:7687",
            "AKOS_REAL_CHAOS_FORBIDDEN_HOSTS": extra_forbidden,
        },
        ["--non-interactive", "--confirm-test-host", extra_forbidden],
    )
    assert res.returncode == 11
    assert "forbidden" in (res.stdout + res.stderr).lower()


def test_refuses_non_interactive_without_matching_confirm_host() -> None:
    res = _run(
        {"AKOS_REAL_CHAOS_OK": "1", "NEO4J_URI": f"neo4j+s://{SAFE_TEST_HOST}:7687"},
        ["--non-interactive", "--confirm-test-host", "wrong-host.example.com"],
    )
    assert res.returncode == 12
    assert "confirm-test-host" in (res.stdout + res.stderr)


def test_dry_run_passes_with_full_gates() -> None:
    """All gates verified + dry-run -> exit 0; emits planned report."""
    res = _run(
        {"AKOS_REAL_CHAOS_OK": "1", "NEO4J_URI": f"neo4j+s://{SAFE_TEST_HOST}:7687"},
        ["--non-interactive", "--confirm-test-host", SAFE_TEST_HOST, "--dry-run"],
    )
    assert res.returncode == 0, res.stdout + res.stderr
    assert "DRY-RUN" in res.stdout
    assert "Report:" in res.stdout


def test_live_without_aura_api_key_refuses() -> None:
    """Live mode requires NEO4J_AURA_API_KEY; otherwise exit 14."""
    res = _run(
        {"AKOS_REAL_CHAOS_OK": "1", "NEO4J_URI": f"neo4j+s://{SAFE_TEST_HOST}:7687"},
        ["--non-interactive", "--confirm-test-host", SAFE_TEST_HOST],
    )
    assert res.returncode == 14
    assert "NEO4J_AURA_API_KEY" in (res.stdout + res.stderr)


def test_live_with_aura_key_emits_planned_only() -> None:
    """Live with Aura key still emits PLANNED-only until operator approves."""
    res = _run(
        {
            "AKOS_REAL_CHAOS_OK": "1",
            "NEO4J_URI": f"neo4j+s://{SAFE_TEST_HOST}:7687",
            "NEO4J_AURA_API_KEY": "fake-test-key",
        },
        ["--non-interactive", "--confirm-test-host", SAFE_TEST_HOST],
    )
    assert res.returncode == 0
    assert "PLANNED-ONLY" in res.stdout


def test_chaos_report_file_emitted_with_gate_checks() -> None:
    """Verify the chaos report contains the safety-gate audit trail."""
    res = _run(
        {"AKOS_REAL_CHAOS_OK": "1", "NEO4J_URI": f"neo4j+s://{SAFE_TEST_HOST}:7687"},
        ["--non-interactive", "--confirm-test-host", SAFE_TEST_HOST, "--dry-run"],
    )
    assert res.returncode == 0
    # Find the most recent report file (artifacts/chaos/).
    artifacts = REPO_ROOT / "artifacts" / "chaos"
    reports = sorted(artifacts.glob("real-chaos-neo4j-rotation-*.json"))
    assert reports, "no chaos report file found"
    payload = json.loads(reports[-1].read_text(encoding="utf-8"))
    assert payload["scenario"] == "neo4j-password-rotation"
    assert payload["gate_checks"]["all_gates_passed"] is True
    assert payload["gate_checks"]["operator_confirmation"] == "non_interactive_match"
    assert payload["gate_checks"]["neo4j_uri_host"] == SAFE_TEST_HOST


def test_runner_is_executable_module() -> None:
    """Runner is reachable as a script (smoke)."""
    assert RUNNER.is_file()
    src = RUNNER.read_text(encoding="utf-8")
    assert "AKOS_REAL_CHAOS_OK" in src
    assert "DEFAULT_FORBIDDEN_HOSTS" in src
    assert "neo4j-password-rotation" in src
