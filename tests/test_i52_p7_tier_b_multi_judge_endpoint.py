"""Initiative 52 P7 tests — Tier B multi-judge roster + endpoint envelope gate.

Coverage:
- AKOS_JUDGE_ROSTER env var wired into matrix job (G-52-3)
- MAX_JUDGE_USD_PER_RUN env var wired (D-IH-52-C; default 15.0)
- workflow_dispatch input `judge_roster` exists
- workflow_dispatch input `max_judge_usd_per_run` exists
- new `endpoint-envelope-gate` job present (G-52-4)
- endpoint-envelope-gate runs scripts/endpoint_cost_probe.py
- endpoint-envelope-gate runs scripts/endpoint_envelope_alarm.py
- endpoint-envelope-gate uploads endpoint-cost artifacts
- endpoint-envelope-gate is needs: tier-b
- endpoint-envelope-gate is gated by AKOS_TIER_B_ENABLED
- pre-existing calibration-drift-gate untouched
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "eval-tier-b.yml"


@pytest.fixture(scope="module")
def yaml_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


# ── Multi-judge roster wiring (G-52-3) ─────────────────────────────────────────


def test_workflow_exposes_akos_judge_roster_env(yaml_text: str) -> None:
    assert "AKOS_JUDGE_ROSTER:" in yaml_text


def test_workflow_exposes_max_judge_usd_per_run_env(yaml_text: str) -> None:
    assert "MAX_JUDGE_USD_PER_RUN:" in yaml_text


def test_workflow_dispatch_has_judge_roster_input(yaml_text: str) -> None:
    assert "judge_roster:" in yaml_text


def test_workflow_dispatch_has_max_judge_usd_per_run_input(yaml_text: str) -> None:
    assert "max_judge_usd_per_run:" in yaml_text
    assert "'15.0'" in yaml_text  # D-IH-52-C default


def test_judge_roster_default_is_empty_for_legacy_path(yaml_text: str) -> None:
    """Empty roster preserves legacy single-judge / offline behaviour."""
    # Look for the input declaration default
    assert "default: ''" in yaml_text


def test_judge_roster_supports_repo_var_override(yaml_text: str) -> None:
    """Repo-level vars.AKOS_JUDGE_ROSTER overrides workflow_dispatch fallback."""
    assert "vars.AKOS_JUDGE_ROSTER" in yaml_text


# ── Endpoint envelope gate (G-52-4) ────────────────────────────────────────────


def test_endpoint_envelope_gate_job_present(yaml_text: str) -> None:
    assert "endpoint-envelope-gate:" in yaml_text


def test_endpoint_envelope_gate_runs_probe(yaml_text: str) -> None:
    assert "scripts/endpoint_cost_probe.py" in yaml_text


def test_endpoint_envelope_gate_runs_alarm(yaml_text: str) -> None:
    assert "scripts/endpoint_envelope_alarm.py" in yaml_text


def test_endpoint_envelope_gate_uploads_artifacts(yaml_text: str) -> None:
    assert "endpoint-cost-probe" in yaml_text
    assert "artifacts/endpoint-cost/endpoint-cost-probe-*" in yaml_text


def test_endpoint_envelope_gate_needs_tier_b(yaml_text: str) -> None:
    """Gate runs after tier-b matrix completes."""
    # Both calibration-drift-gate and endpoint-envelope-gate need: tier-b
    needs_count = yaml_text.count("needs: tier-b")
    assert needs_count >= 2, f"expected >=2 'needs: tier-b' (calibration + endpoint); got {needs_count}"


def test_endpoint_envelope_gate_repo_var_gated(yaml_text: str) -> None:
    """Gate respects AKOS_TIER_B_ENABLED operator opt-in."""
    # Three jobs total now gate on AKOS_TIER_B_ENABLED:
    # tier-b matrix, calibration-drift-gate, endpoint-envelope-gate.
    var_count = yaml_text.count("vars.AKOS_TIER_B_ENABLED == 'true'")
    assert var_count >= 3, (
        f"expected >=3 AKOS_TIER_B_ENABLED gates "
        f"(tier-b + calibration-drift-gate + endpoint-envelope-gate); got {var_count}"
    )


def test_endpoint_envelope_gate_has_timeout(yaml_text: str) -> None:
    """Each gate job has a timeout-minutes; endpoint gate is short."""
    # The pattern 'timeout-minutes: 5' covers both the calibration-drift-gate
    # (5 min) and endpoint-envelope-gate (5 min). Ensure at least 2 occurrences.
    short_timeouts = yaml_text.count("timeout-minutes: 5")
    assert short_timeouts >= 2, (
        f"expected both gate jobs to have timeout-minutes: 5; got {short_timeouts}"
    )


# ── Backward-compat: pre-existing calibration-drift-gate untouched ─────────────


def test_calibration_drift_gate_still_present(yaml_text: str) -> None:
    """I51 P5 gate must not be regressed by the I52 P7 changes."""
    assert "calibration-drift-gate:" in yaml_text
    assert "scripts/calibrate_scenarios.py --hard-fail-on-drift" in yaml_text


def test_workflow_yaml_parses(yaml_text: str) -> None:
    """Belt-and-braces: YAML round-trip after I52 P7 edits."""
    import yaml

    data = yaml.safe_load(yaml_text)
    assert isinstance(data, dict)
    # `on:` is a YAML reserved word — pyyaml may load `on` as boolean True
    triggers = data.get("on") if "on" in data else data.get(True)
    assert triggers is not None, f"workflow triggers missing; keys={list(data.keys())}"
    jobs = data.get("jobs") or {}
    assert "tier-b" in jobs
    assert "calibration-drift-gate" in jobs
    assert "endpoint-envelope-gate" in jobs


def test_endpoint_envelope_gate_uses_stub_today(yaml_text: str) -> None:
    """Until OPS-52-2 ships real run-log JSONLs, gate uses --stub fixture."""
    assert "scripts/endpoint_cost_probe.py --stub" in yaml_text
    assert "scripts/endpoint_envelope_alarm.py --stub" in yaml_text
