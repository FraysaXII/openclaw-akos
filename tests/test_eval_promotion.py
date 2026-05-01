"""Initiative 45 P7 — Tests for the skill promotion gate."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from akos.eval_harness.promotion import (
    check_adversarial_pass,
    check_routing_condition_non_empty,
    check_tier_a_green,
    check_tier_b_recent,
    evaluate_promotion,
)


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


# ── Per-criterion checks ─────────────────────────────────────────────────────


def test_check_routing_condition_non_empty_passes_for_madeira() -> None:
    r = check_routing_condition_non_empty("SKILL-MADEIRA-LOOKUP-V1")
    assert r.status == "PASS"
    assert "intent_in" in r.reason


def test_check_routing_condition_fails_for_shared_locale() -> None:
    """SHARED-LOCALE intentionally has empty routing_condition (always-eligible)."""
    r = check_routing_condition_non_empty("SKILL-SHARED-LOCALE-DETECT-V1")
    assert r.status == "FAIL"
    assert "empty" in r.reason.lower()


def test_check_routing_condition_fails_for_unknown_skill() -> None:
    r = check_routing_condition_non_empty("SKILL-DOES-NOT-EXIST-V99")
    assert r.status == "FAIL"


def test_check_adversarial_pass_for_madeira() -> None:
    r = check_adversarial_pass("SKILL-MADEIRA-LOOKUP-V1")
    assert r.status == "PASS"
    assert r.reason.startswith("all ") and "adversarial cassettes" in r.reason


def test_check_adversarial_fails_for_skill_without_cassettes() -> None:
    r = check_adversarial_pass("SKILL-DOES-NOT-EXIST-V99")
    assert r.status == "FAIL"
    assert "no adversarial" in r.reason


def test_check_tier_b_recent_skips_with_clear_reason() -> None:
    """Today: Tier B is operator-side; check returns SKIP with the explanatory reason."""
    r = check_tier_b_recent("SKILL-MADEIRA-LOOKUP-V1")
    assert r.status == "SKIP"
    assert "compliance.eval_run" in r.reason


def test_check_tier_a_green_passes_for_madeira() -> None:
    r = check_tier_a_green("SKILL-MADEIRA-LOOKUP-V1")
    assert r.status == "PASS"


# ── Aggregate verdict ────────────────────────────────────────────────────────


def test_evaluate_promotion_madeira_passes() -> None:
    """3 PASS + 1 SKIP (Tier B) -> overall PASS (skip is data-not-yet-available, not failure)."""
    v = evaluate_promotion("SKILL-MADEIRA-LOOKUP-V1")
    assert v.overall == "PASS"
    statuses = [c.status for c in v.criteria]
    assert "FAIL" not in statuses
    assert statuses.count("PASS") == 3
    assert statuses.count("SKIP") == 1


def test_evaluate_promotion_shared_locale_fails_on_routing_condition() -> None:
    v = evaluate_promotion("SKILL-SHARED-LOCALE-DETECT-V1")
    assert v.overall == "FAIL"
    rc = next(c for c in v.criteria if c.name == "routing_condition_non_empty")
    assert rc.status == "FAIL"


def test_evaluate_promotion_unknown_skill_fails_on_3_criteria() -> None:
    v = evaluate_promotion("SKILL-DOES-NOT-EXIST-V99")
    assert v.overall == "FAIL"
    fails = [c for c in v.criteria if c.status == "FAIL"]
    # adversarial_pass + routing_condition_non_empty fail; tier_a_green SKIPs
    assert len(fails) >= 2


def test_evaluate_promotion_override_returns_override_verdict() -> None:
    v = evaluate_promotion("SKILL-SHARED-LOCALE-DETECT-V1", override=True, override_reason="exec-emergency-2026-05-01")
    assert v.overall == "OVERRIDE"
    assert any(c.name == "operator_override" for c in v.criteria)
    assert "exec-emergency" in v.criteria[0].reason


# ── CLI surface ──────────────────────────────────────────────────────────────


def test_cli_promote_madeira_exits_0() -> None:
    p = _run_cli("promote", "--skill", "SKILL-MADEIRA-LOOKUP-V1")
    assert p.returncode == 0
    assert "OVERALL: PASS" in p.stdout


def test_cli_promote_shared_locale_exits_1() -> None:
    p = _run_cli("promote", "--skill", "SKILL-SHARED-LOCALE-DETECT-V1")
    assert p.returncode == 1
    assert "OVERALL: FAIL" in p.stdout


def test_cli_promote_override_without_reason_exits_2() -> None:
    p = _run_cli("promote", "--skill", "SKILL-SHARED-LOCALE-DETECT-V1", "--override")
    assert p.returncode == 2
    assert "audit trail" in p.stderr


def test_cli_promote_override_with_reason_exits_0() -> None:
    p = _run_cli(
        "promote",
        "--skill", "SKILL-SHARED-LOCALE-DETECT-V1",
        "--override", "--reason", "test-override-2026-05-01",
    )
    assert p.returncode == 0
    assert "OVERRIDE" in p.stdout


def test_cli_promote_json_emits_structured_verdict() -> None:
    p = _run_cli("promote", "--skill", "SKILL-MADEIRA-LOOKUP-V1", "--json")
    assert p.returncode == 0
    parsed = json.loads(p.stdout)
    assert parsed["skill_id"] == "SKILL-MADEIRA-LOOKUP-V1"
    assert parsed["overall"] == "PASS"
    assert len(parsed["criteria"]) == 4


# ── Policy register coupling ─────────────────────────────────────────────────


def test_policy_register_has_promotion_gate_row() -> None:
    import csv as _csv

    p = (
        REPO_ROOT
        / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "POLICY_REGISTER.csv"
    )
    rows = [r for r in _csv.DictReader(p.open(encoding="utf-8")) if r.get("policy_class") == "promotion_gate"]
    assert len(rows) == 1
    assert rows[0]["policy_id"] == "POL-EVAL-PROMOTION-GATE"
