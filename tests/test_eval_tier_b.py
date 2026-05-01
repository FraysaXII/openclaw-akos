"""Initiative 45 P6 — Tier B weekly schedule + cost ceiling tests.

Asserts:
- --tier B without AKOS_RECORD_LIVE=1 exits 2 (cost-control guard)
- --tier B with AKOS_RECORD_LIVE=1 emits the cost ceiling banner
- --max-spend / MAX_TIER_B_USD env var precedence
- --regression-pp threshold marks rows as FAIL when delta_pp regresses past it
- GitHub workflow YAML exists with the expected cron + matrix
- verification_profile eval_harness_smoke registered with the right steps
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run_cli(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    import os

    cli_env = os.environ.copy()
    cli_env["AKOS_EVAL_NO_DEPRECATION_WARN"] = "1"
    if env:
        cli_env.update(env)
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "eval.py"), *args],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=REPO_ROOT,
        env=cli_env,
    )


# ── Cost-control guard ───────────────────────────────────────────────────────


def test_tier_b_without_live_env_exits_2() -> None:
    p = _run_cli("--tier", "B", "--mode", "replay", env={"AKOS_RECORD_LIVE": ""})
    assert p.returncode == 2
    assert "AKOS_RECORD_LIVE=1" in p.stderr


def test_tier_b_with_live_env_emits_banner() -> None:
    p = _run_cli("--tier", "B", "--mode", "replay", env={"AKOS_RECORD_LIVE": "1"})
    assert "Live regression mode" in p.stderr
    assert "Cost ceiling" in p.stderr


def test_tier_a_default_does_not_emit_tier_b_banner() -> None:
    p = _run_cli("--tier", "A", "--mode", "replay")
    assert "Live regression mode" not in p.stderr


def test_tier_b_max_spend_flag_appears_in_banner() -> None:
    p = _run_cli(
        "--tier", "B", "--mode", "replay", "--max-spend", "12.34",
        env={"AKOS_RECORD_LIVE": "1"},
    )
    assert "$12.34" in p.stderr


def test_tier_b_env_var_max_spend_used_when_no_flag() -> None:
    p = _run_cli(
        "--tier", "B", "--mode", "replay",
        env={"AKOS_RECORD_LIVE": "1", "MAX_TIER_B_USD": "7.50"},
    )
    assert "$7.50" in p.stderr


# ── Regression threshold ─────────────────────────────────────────────────────


def test_regression_pp_flag_marks_synthetic_drop_as_fail() -> None:
    """When a skill regresses >5pp via --current and we run --tier B, the row
    should FAIL (in addition to the canary-2 trip already detected at >2pp)."""
    p = _run_cli(
        "--tier", "B",
        "--mode", "canary",
        "--current", "SKILL-MADEIRA-LOOKUP-V1=80.0",  # 12pp drop from 92.0 baseline
        "--regression-pp", "5.0",
        "--json",
        env={"AKOS_RECORD_LIVE": "1"},
    )
    assert p.returncode == 1, p.stderr
    parsed = json.loads(p.stdout)
    assert parsed["overall_status"] == "fail"
    madeira = next(r for r in parsed["rows"] if r["skill_id"] == "SKILL-MADEIRA-LOOKUP-V1")
    assert madeira["status"] == "FAIL"
    assert any("tier_b_regression" in f or "canary_2_regression" in f for f in madeira["failures"])


def test_regression_pp_threshold_lets_3pp_drop_pass_when_threshold_5pp() -> None:
    """A 3pp drop trips canary-2 (2pp threshold) but NOT tier_b_regression (5pp threshold).
    The canary-2 still FAILs the row, but the failures list should NOT include tier_b_regression."""
    p = _run_cli(
        "--tier", "B",
        "--mode", "canary",
        "--current", "SKILL-MADEIRA-LOOKUP-V1=89.0",  # 3pp drop
        "--regression-pp", "5.0",
        "--json",
        env={"AKOS_RECORD_LIVE": "1"},
    )
    parsed = json.loads(p.stdout)
    madeira = next(r for r in parsed["rows"] if r["skill_id"] == "SKILL-MADEIRA-LOOKUP-V1")
    # canary-2 is the cause of FAIL at 3pp (>2pp default threshold)
    assert any("canary_2_regression" in f for f in madeira["failures"])
    # tier_b_regression should NOT fire at 3pp (we set threshold to 5pp)
    assert not any("tier_b_regression" in f for f in madeira["failures"])


# ── GitHub workflow YAML ─────────────────────────────────────────────────────


def test_eval_tier_b_workflow_exists_and_has_cron() -> None:
    workflow_path = REPO_ROOT / ".github" / "workflows" / "eval-tier-b.yml"
    assert workflow_path.is_file(), "eval-tier-b.yml must exist (P6 deliverable)"
    text = workflow_path.read_text(encoding="utf-8")
    assert "cron:" in text
    assert "0 6 * * 1" in text  # Monday 06:00 UTC
    assert "workflow_dispatch" in text
    assert "MAX_TIER_B_USD" in text


def test_eval_tier_b_workflow_has_model_tier_matrix() -> None:
    workflow_path = REPO_ROOT / ".github" / "workflows" / "eval-tier-b.yml"
    text = workflow_path.read_text(encoding="utf-8")
    assert "matrix:" in text
    assert "model_tier:" in text
    assert "cheap" in text
    assert "flagship" in text


def test_eval_tier_b_workflow_gated_on_repo_var() -> None:
    """Operator opts in via repo variable AKOS_TIER_B_ENABLED to prevent
    accidental cost when the workflow first lands."""
    workflow_path = REPO_ROOT / ".github" / "workflows" / "eval-tier-b.yml"
    text = workflow_path.read_text(encoding="utf-8")
    assert "AKOS_TIER_B_ENABLED" in text


# ── Verification profile ─────────────────────────────────────────────────────


def test_verification_profile_eval_harness_smoke_registered() -> None:
    profiles_path = REPO_ROOT / "config" / "verification-profiles.json"
    data = json.loads(profiles_path.read_text(encoding="utf-8"))
    profiles = data.get("profiles", {})
    assert "eval_harness_smoke" in profiles, "P6 profile must be registered under .profiles"
    profile = profiles["eval_harness_smoke"]
    step_ids = [s["id"] for s in profile.get("steps", [])]
    assert "eval_all_modes_tier_a" in step_ids
    assert "eval_replay_tier_a" in step_ids
    assert "eval_adversarial_tier_a" in step_ids
    assert "eval_pii_lint" in step_ids
