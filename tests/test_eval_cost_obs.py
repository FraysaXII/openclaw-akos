"""Initiative 45 P4 — Tests for cost + latency observability."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from akos.eval_harness.cost_obs import (
    COST_REGRESSION_HARD_FAIL_PCT,
    COST_REGRESSION_SOFT_WARN_PCT,
    CostCeiling,
    CostMetrics,
    aggregate_skill_cost,
    compute_cost_usd,
    evaluate_cost_ceiling,
    load_cost_ceilings,
    load_model_prices,
)


# ── Model prices ──────────────────────────────────────────────────────────────


def test_load_model_prices_returns_real_models() -> None:
    p = load_model_prices()
    assert "deterministic:akos.intent.classify_request" in p
    assert "anthropic:claude-3-5-sonnet-20241022" in p
    assert p["anthropic:claude-3-5-sonnet-20241022"]["input_per_1k_usd"] == 0.003


def test_load_model_prices_returns_empty_for_missing_file(tmp_path: Path) -> None:
    out = load_model_prices(path=tmp_path / "missing.json")
    assert out == {}


def test_load_model_prices_returns_empty_for_malformed(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("not json", encoding="utf-8")
    assert load_model_prices(path=p) == {}


# ── compute_cost_usd ──────────────────────────────────────────────────────────


def test_compute_cost_for_known_model() -> None:
    # Sonnet at 1k in / 1k out = 0.003 + 0.015 = 0.018
    cost = compute_cost_usd(
        tokens_in=1000, tokens_out=1000, model_id="anthropic:claude-3-5-sonnet-20241022"
    )
    assert cost == pytest.approx(0.018, rel=1e-9)


def test_compute_cost_for_unknown_model_returns_zero() -> None:
    assert compute_cost_usd(tokens_in=1000, tokens_out=1000, model_id="nonexistent:fake") == 0.0


def test_compute_cost_for_deterministic_returns_zero() -> None:
    cost = compute_cost_usd(
        tokens_in=10000,
        tokens_out=10000,
        model_id="deterministic:akos.intent.classify_request",
    )
    assert cost == 0.0


# ── load_cost_ceilings ────────────────────────────────────────────────────────


def test_load_cost_ceilings_finds_5_skill_ceilings() -> None:
    """The 5 POL-EVAL-COST-CEILING-* rows shipped in I45 P4."""
    ceilings = load_cost_ceilings()
    assert "SKILL-MADEIRA-LOOKUP-V1" in ceilings
    assert "SKILL-ARCHITECT-PLAN-V1" in ceilings
    assert "SKILL-EXECUTOR-RUN-V1" in ceilings
    assert "SKILL-VERIFIER-CHECK-V1" in ceilings
    assert "SKILL-SHARED-LOCALE-DETECT-V1" in ceilings
    # Check threshold parsing
    assert ceilings["SKILL-MADEIRA-LOOKUP-V1"].max_usd_per_run == 0.005
    assert ceilings["SKILL-EXECUTOR-RUN-V1"].max_usd_per_run == 0.10
    assert ceilings["SKILL-SHARED-LOCALE-DETECT-V1"].max_usd_per_run == 0.0


def test_load_cost_ceilings_empty_for_missing_file(tmp_path: Path) -> None:
    out = load_cost_ceilings(path=tmp_path / "missing.csv")
    assert out == {}


# ── evaluate_cost_ceiling ─────────────────────────────────────────────────────


def test_evaluate_within_ceiling_passes() -> None:
    metrics = CostMetrics(
        skill_id="X", runs=1, cost_usd_avg=0.001, cost_usd_p95=0.002,
        latency_ms_p50=100, latency_ms_p95=200, tokens_in_total=10, tokens_out_total=20,
    )
    ceiling = CostCeiling(skill_id="X", policy_id="POL-X", max_usd_per_run=0.005)
    out = evaluate_cost_ceiling("X", metrics, ceiling)
    assert out["status"] == "PASS"


def test_evaluate_warn_at_15pct_over() -> None:
    metrics = CostMetrics(
        skill_id="X", runs=1, cost_usd_avg=0.00575, cost_usd_p95=0.006,
        latency_ms_p50=100, latency_ms_p95=200, tokens_in_total=10, tokens_out_total=20,
    )  # 15% over 0.005
    ceiling = CostCeiling(skill_id="X", policy_id="POL-X", max_usd_per_run=0.005)
    out = evaluate_cost_ceiling("X", metrics, ceiling)
    assert out["status"] == "WARN"
    assert out["delta_pct"] > COST_REGRESSION_SOFT_WARN_PCT
    assert out["delta_pct"] < COST_REGRESSION_HARD_FAIL_PCT


def test_evaluate_fail_at_25pct_over() -> None:
    metrics = CostMetrics(
        skill_id="X", runs=1, cost_usd_avg=0.00625, cost_usd_p95=0.007,
        latency_ms_p50=100, latency_ms_p95=200, tokens_in_total=10, tokens_out_total=20,
    )  # 25% over 0.005
    ceiling = CostCeiling(skill_id="X", policy_id="POL-X", max_usd_per_run=0.005)
    out = evaluate_cost_ceiling("X", metrics, ceiling)
    assert out["status"] == "FAIL"
    assert any("cost_regression" in f for f in out["failures"])


def test_evaluate_zero_cost_ceiling_breach_fails() -> None:
    metrics = CostMetrics(
        skill_id="X", runs=1, cost_usd_avg=0.0001, cost_usd_p95=0.0002,
        latency_ms_p50=100, latency_ms_p95=200, tokens_in_total=10, tokens_out_total=20,
    )
    ceiling = CostCeiling(skill_id="X", policy_id="POL-X", max_usd_per_run=0.0)
    out = evaluate_cost_ceiling("X", metrics, ceiling)
    assert out["status"] == "FAIL"
    assert any("cost_ceiling_breach" in f for f in out["failures"])


def test_evaluate_zero_cost_ceiling_zero_current_passes() -> None:
    metrics = CostMetrics(
        skill_id="X", runs=1, cost_usd_avg=0.0, cost_usd_p95=0.0,
        latency_ms_p50=100, latency_ms_p95=200, tokens_in_total=0, tokens_out_total=0,
    )
    ceiling = CostCeiling(skill_id="X", policy_id="POL-X", max_usd_per_run=0.0)
    out = evaluate_cost_ceiling("X", metrics, ceiling)
    assert out["status"] == "PASS"


def test_evaluate_skip_when_no_ceiling() -> None:
    metrics = CostMetrics(
        skill_id="X", runs=1, cost_usd_avg=0.001, cost_usd_p95=0.002,
        latency_ms_p50=100, latency_ms_p95=200, tokens_in_total=10, tokens_out_total=20,
    )
    out = evaluate_cost_ceiling("X", metrics, None)
    assert out["status"] == "SKIP"


# ── aggregate_skill_cost (uses real cassettes) ────────────────────────────────


def test_aggregate_madeira_returns_metrics_for_2_cassettes() -> None:
    metrics = aggregate_skill_cost("SKILL-MADEIRA-LOOKUP-V1")
    assert metrics is not None
    assert metrics.skill_id == "SKILL-MADEIRA-LOOKUP-V1"
    assert metrics.runs == 2  # we seeded 2 Madeira cassettes (lookup_role + hlk_search)
    assert metrics.cost_usd_avg == 0.0  # deterministic cassettes have zero cost
    assert metrics.latency_ms_p50 > 0  # but they do have measured latency


def test_aggregate_unknown_skill_returns_none() -> None:
    metrics = aggregate_skill_cost("SKILL-DOES-NOT-EXIST-V99")
    assert metrics is None


# ── End-to-end: --enforce-cost on the unified harness ─────────────────────────


def test_run_canary_enforce_cost_passes_in_clean_state() -> None:
    from akos.eval_harness.v2 import Scorecard, run_canary

    sc = Scorecard()
    run_canary(sc, enforce_cost=True)
    canary_rows = [r for r in sc.rows if r.mode == "canary"]
    assert len(canary_rows) == 5
    fails = [r for r in canary_rows if r.status == "FAIL"]
    assert not fails, f"unexpected cost failures: {[(r.skill_id, r.failures) for r in fails]}"
    # All rows should have populated cost + latency
    for r in canary_rows:
        assert r.cost_usd is not None
        assert r.latency_ms_p50 is not None
        assert r.latency_ms_p95 is not None


def test_canary_without_enforce_does_not_block_on_cost() -> None:
    """When --enforce-cost is OFF, even a hypothetical cost regression must not
    flip canary rows to FAIL (only canary-2 accuracy regression does)."""
    from akos.eval_harness.v2 import Scorecard, run_canary

    sc = Scorecard()
    run_canary(sc, enforce_cost=False)
    canary_rows = [r for r in sc.rows if r.mode == "canary"]
    assert all(r.status == "PASS" for r in canary_rows)


# ── Drift detector ────────────────────────────────────────────────────────────


def test_policy_register_has_cost_ceiling_rows() -> None:
    """Locks in three governed cost_ceiling tranches:

    - 5 skill-level rows (I45 P4): MADEIRA-LOOKUP, ARCHITECT-PLAN, EXECUTOR-RUN,
      VERIFIER-CHECK, SHARED-LOCALE-DETECT.
    - 3 runtime-envelope rows (I50 P2 / D-IH-50-A): DOSSIER, PERSONA, JUDGE.
    - 2 endpoint-envelope rows (I52 P5 / D-IH-52-D + D-IH-52-E):
      ENDPOINT-RUNPOD-V1, ENDPOINT-KALAVAI-V1.

    If anyone removes a cost_ceiling row from POLICY_REGISTER, this fails fast.
    """
    import csv as _csv

    p = (
        Path(__file__).resolve().parent.parent
        / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "POLICY_REGISTER.csv"
    )
    cost_rows = [
        r for r in _csv.DictReader(p.open(encoding="utf-8"))
        if r.get("policy_class") == "cost_ceiling"
    ]
    assert len(cost_rows) == 10, (
        f"Expected 10 cost_ceiling rows (5 skill-level I45 P4 + 3 runtime-envelope "
        f"I50 P2 + 2 endpoint-envelope I52 P5); "
        f"got {len(cost_rows)}: {[r['policy_id'] for r in cost_rows]}"
    )

    skill_level = {
        "POL-EVAL-COST-CEILING-MADEIRA-LOOKUP",
        "POL-EVAL-COST-CEILING-ARCHITECT-PLAN",
        "POL-EVAL-COST-CEILING-EXECUTOR-RUN",
        "POL-EVAL-COST-CEILING-VERIFIER-CHECK",
        "POL-EVAL-COST-CEILING-SHARED-LOCALE-DETECT",
    }
    runtime_envelope = {
        "POL-EVAL-COST-CEILING-DOSSIER-V1",
        "POL-EVAL-COST-CEILING-PERSONA-V1",
        "POL-EVAL-COST-CEILING-JUDGE-V1",
    }
    endpoint_envelope = {
        "POL-EVAL-COST-CEILING-ENDPOINT-RUNPOD-V1",
        "POL-EVAL-COST-CEILING-ENDPOINT-KALAVAI-V1",
    }
    actual = {r["policy_id"] for r in cost_rows}
    missing_skill = skill_level - actual
    missing_runtime = runtime_envelope - actual
    missing_endpoint = endpoint_envelope - actual
    assert not missing_skill, f"Missing skill-level cost_ceiling rows: {missing_skill}"
    assert not missing_runtime, f"Missing runtime-envelope cost_ceiling rows: {missing_runtime}"
    assert not missing_endpoint, f"Missing endpoint-envelope cost_ceiling rows: {missing_endpoint}"


def test_policy_class_enum_includes_i45_p4_p5_p7_and_i46_p5_classes() -> None:
    from akos.hlk_policy_register_csv import VALID_POLICY_CLASSES

    assert "cost_ceiling" in VALID_POLICY_CLASSES
    assert "adversarial_floor" in VALID_POLICY_CLASSES
    assert "promotion_gate" in VALID_POLICY_CLASSES
    assert "graph_rag_eligibility" in VALID_POLICY_CLASSES
