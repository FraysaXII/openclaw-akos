"""Initiative 52 P5 — Tests for endpoint (per-GPU-hour) cost discipline.

Covers:
- CostRecord unit discriminator validation (D-IH-52-D)
- compute_cost_record dispatch token vs gpu_hour (D-IH-52-D / D-IH-52-E)
- load_endpoint_prices soft-fail discipline
- load_endpoint_ceilings POL_REGISTER row parsing
- aggregate_endpoint_cost runs aggregation + daily projection
- evaluate_endpoint_envelope soft-warn / hard-fail bands
- POL-EVAL-COST-CEILING-ENDPOINT-{RUNPOD,KALAVAI}-V1 rows present in canon
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from akos.eval_harness.cost_obs import (
    COST_REGRESSION_HARD_FAIL_PCT,
    COST_REGRESSION_SOFT_WARN_PCT,
    DEFAULT_COST_UNIT,
    ENDPOINT_HOURLY_TO_DAILY_PROJECTION,
    VALID_COST_UNITS,
    CostRecord,
    EndpointCeiling,
    EndpointPrice,
    aggregate_endpoint_cost,
    compute_cost_record,
    evaluate_endpoint_envelope,
    load_endpoint_ceilings,
    load_endpoint_prices,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY_REGISTER_CSV = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals"
    / "dimensions"
    / "POLICY_REGISTER.csv"
)
ENDPOINT_PRICES_PATH = REPO_ROOT / "config" / "eval" / "endpoint-prices.json"


# ── CostRecord unit discriminator (D-IH-52-D) ──────────────────────────────────


def test_cost_record_token_unit_requires_model_id() -> None:
    with pytest.raises(ValueError, match="model_id"):
        CostRecord(cost_usd=0.01, unit="token")


def test_cost_record_gpu_hour_unit_requires_endpoint_id() -> None:
    with pytest.raises(ValueError, match="endpoint_id"):
        CostRecord(cost_usd=1.0, unit="gpu_hour")


def test_cost_record_rejects_unknown_unit() -> None:
    with pytest.raises(ValueError, match="unit must be one of"):
        CostRecord(cost_usd=0.0, unit="bananas", model_id="x")


def test_cost_record_token_unit_constructs() -> None:
    r = CostRecord(
        cost_usd=0.012,
        unit="token",
        model_id="anthropic:claude-3-5-sonnet-20241022",
        tokens_in=1000,
        tokens_out=500,
    )
    assert r.unit == "token"
    assert r.cost_usd == 0.012


def test_cost_record_gpu_hour_unit_constructs() -> None:
    r = CostRecord(
        cost_usd=1.95,
        unit="gpu_hour",
        endpoint_id="runpod:a100-80gb",
        duration_hours=1.0,
    )
    assert r.unit == "gpu_hour"
    assert r.endpoint_id == "runpod:a100-80gb"


def test_cost_unit_constants_are_governed() -> None:
    assert "token" in VALID_COST_UNITS
    assert "gpu_hour" in VALID_COST_UNITS
    assert DEFAULT_COST_UNIT == "token"


# ── compute_cost_record dispatch (D-IH-52-D / D-IH-52-E) ───────────────────────


def test_compute_cost_record_token_path_routes_to_model_prices() -> None:
    rec = compute_cost_record(
        unit="token",
        tokens_in=1000,
        tokens_out=1000,
        model_id="anthropic:claude-3-5-sonnet-20241022",
    )
    assert rec.unit == "token"
    # 1k * 0.003 + 1k * 0.015 = 0.018
    assert rec.cost_usd == pytest.approx(0.018)


def test_compute_cost_record_gpu_hour_path_routes_to_endpoint_prices(
    tmp_path: Path,
) -> None:
    fake = tmp_path / "endpoints.json"
    fake.write_text(
        json.dumps(
            {
                "endpoints": {
                    "runpod:test": {
                        "provider": "runpod",
                        "gpu_class": "A10",
                        "usd_per_hour": 1.00,
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    prices = load_endpoint_prices(path=fake)
    rec = compute_cost_record(
        unit="gpu_hour",
        endpoint_id="runpod:test",
        duration_hours=2.5,
        endpoint_prices=prices,
    )
    assert rec.unit == "gpu_hour"
    assert rec.cost_usd == pytest.approx(2.50)


def test_compute_cost_record_rejects_unit_mixing_implicitly() -> None:
    with pytest.raises(ValueError, match="endpoint_id"):
        compute_cost_record(unit="gpu_hour", duration_hours=1.0)
    with pytest.raises(ValueError, match="model_id"):
        compute_cost_record(unit="token", tokens_in=10, tokens_out=10)


def test_compute_cost_record_rejects_unknown_unit() -> None:
    with pytest.raises(ValueError, match="unit must be one of"):
        compute_cost_record(unit="energy", endpoint_id="x")


def test_compute_cost_record_unknown_endpoint_returns_zero(tmp_path: Path) -> None:
    fake = tmp_path / "endpoints.json"
    fake.write_text(json.dumps({"endpoints": {}}), encoding="utf-8")
    prices = load_endpoint_prices(path=fake)
    rec = compute_cost_record(
        unit="gpu_hour",
        endpoint_id="not-in-table",
        duration_hours=10.0,
        endpoint_prices=prices,
    )
    assert rec.cost_usd == 0.0  # soft-fail per R-45-11 + R-52-3


# ── load_endpoint_prices ───────────────────────────────────────────────────────


def test_load_endpoint_prices_returns_real_endpoints() -> None:
    p = load_endpoint_prices()
    assert "runpod:a100-80gb" in p
    assert "kalavai:default" in p
    assert isinstance(p["runpod:a100-80gb"], EndpointPrice)
    assert p["runpod:a100-80gb"].provider == "runpod"


def test_load_endpoint_prices_soft_fails_for_missing_file(tmp_path: Path) -> None:
    out = load_endpoint_prices(path=tmp_path / "missing.json")
    assert out == {}


def test_load_endpoint_prices_soft_fails_for_malformed(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    assert load_endpoint_prices(path=bad) == {}


def test_load_endpoint_prices_skips_invalid_rows(tmp_path: Path) -> None:
    fake = tmp_path / "endpoints.json"
    fake.write_text(
        json.dumps(
            {
                "endpoints": {
                    "good": {
                        "provider": "p",
                        "gpu_class": "g",
                        "usd_per_hour": 1.0,
                    },
                    "bad": "not-a-dict",
                    "broken": {"usd_per_hour": "not-a-float"},
                }
            }
        ),
        encoding="utf-8",
    )
    out = load_endpoint_prices(path=fake)
    assert "good" in out
    assert "bad" not in out
    assert "broken" not in out


# ── load_endpoint_ceilings ─────────────────────────────────────────────────────


def test_load_endpoint_ceilings_finds_runpod_and_kalavai() -> None:
    ceilings = load_endpoint_ceilings()
    assert "RUNPOD" in ceilings
    assert "KALAVAI" in ceilings
    assert isinstance(ceilings["RUNPOD"], EndpointCeiling)
    assert ceilings["RUNPOD"].max_usd_per_hour == pytest.approx(4.00)
    assert ceilings["KALAVAI"].max_usd_per_hour == pytest.approx(1.00)


def test_load_endpoint_ceilings_soft_fail_for_missing_file(tmp_path: Path) -> None:
    out = load_endpoint_ceilings(path=tmp_path / "missing.csv")
    assert out == {}


def test_load_endpoint_ceilings_ignores_non_endpoint_cost_rows(tmp_path: Path) -> None:
    fake = tmp_path / "policy.csv"
    fake.write_text(
        "policy_id,policy_class,applies_to_schema,applies_to_table,policy_text,cadence,owner_role,last_review,next_review,topic_ids,notes\n"
        'POL-EVAL-COST-CEILING-MADEIRA-LOOKUP,cost_ceiling,*,*,'
        '"max_usd_per_run=0.005",continuous,X,2026-05-03,2026-08-03,topic_x,note\n'
        'POL-EVAL-COST-CEILING-ENDPOINT-FOO-V1,cost_ceiling,*,*,'
        '"max_usd_per_hour=2.50",continuous,X,2026-05-03,2026-08-03,topic_x,note\n',
        encoding="utf-8",
    )
    out = load_endpoint_ceilings(path=fake)
    assert "FOO" in out
    assert out["FOO"].max_usd_per_hour == pytest.approx(2.50)
    assert "MADEIRA-LOOKUP" not in out  # not an endpoint row


# ── POLICY_REGISTER.csv canonical contract (D-IH-52-D / D-IH-52-E) ─────────────


def test_policy_register_has_runpod_and_kalavai_endpoint_ceilings() -> None:
    """The two new endpoint cost-ceiling rows are present in canonical CSV."""
    with POLICY_REGISTER_CSV.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    pids = {(r.get("policy_id") or "").strip() for r in rows}
    assert "POL-EVAL-COST-CEILING-ENDPOINT-RUNPOD-V1" in pids
    assert "POL-EVAL-COST-CEILING-ENDPOINT-KALAVAI-V1" in pids


def test_endpoint_ceiling_rows_are_classified_as_cost_ceiling() -> None:
    with POLICY_REGISTER_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            pid = (row.get("policy_id") or "").strip()
            if pid in {
                "POL-EVAL-COST-CEILING-ENDPOINT-RUNPOD-V1",
                "POL-EVAL-COST-CEILING-ENDPOINT-KALAVAI-V1",
            }:
                assert row["policy_class"] == "cost_ceiling"
                assert "max_usd_per_hour=" in (row.get("policy_text") or "")


# ── aggregate_endpoint_cost ────────────────────────────────────────────────────


def _stub_endpoint_prices() -> dict[str, EndpointPrice]:
    return {
        "runpod:test": EndpointPrice(
            endpoint_id="runpod:test", provider="runpod", gpu_class="A10", usd_per_hour=2.00
        )
    }


def test_aggregate_endpoint_cost_returns_none_for_no_runs() -> None:
    out = aggregate_endpoint_cost(
        "runpod:test", runs=[], endpoint_prices=_stub_endpoint_prices()
    )
    assert out is None


def test_aggregate_endpoint_cost_computes_avg_per_hour() -> None:
    runs = [{"duration_hours": 0.5}, {"duration_hours": 1.5}, {"duration_hours": 2.0}]
    m = aggregate_endpoint_cost(
        "runpod:test", runs=runs, endpoint_prices=_stub_endpoint_prices()
    )
    assert m is not None
    assert m.runs == 3
    assert m.duration_hours_total == pytest.approx(4.0)
    # 4 hours * $2/hr = $8 total
    assert m.cost_usd_total == pytest.approx(8.0)
    # avg per hour = 8 / 4 = 2.0 (rate)
    assert m.cost_usd_per_hour_avg == pytest.approx(2.0)


def test_aggregate_endpoint_cost_emits_daily_projection() -> None:
    runs = [{"duration_hours": 1.0}]
    m = aggregate_endpoint_cost(
        "runpod:test", runs=runs, endpoint_prices=_stub_endpoint_prices()
    )
    assert m is not None
    assert m.projected_daily_usd == pytest.approx(
        m.cost_usd_per_hour_avg * ENDPOINT_HOURLY_TO_DAILY_PROJECTION
    )


def test_aggregate_endpoint_cost_unknown_endpoint_zero_rate() -> None:
    runs = [{"duration_hours": 5.0}]
    m = aggregate_endpoint_cost("not-in-table", runs=runs, endpoint_prices={})
    assert m is not None
    assert m.cost_usd_total == 0.0
    assert m.cost_usd_per_hour_avg == 0.0


# ── evaluate_endpoint_envelope ─────────────────────────────────────────────────


def _ceiling(rate: float) -> EndpointCeiling:
    return EndpointCeiling(
        endpoint_id="X", policy_id="POL-EVAL-COST-CEILING-ENDPOINT-X-V1", max_usd_per_hour=rate
    )


def _metrics(per_hour: float) -> "object":
    from akos.eval_harness.cost_obs import EndpointMetrics

    return EndpointMetrics(
        endpoint_id="X",
        runs=1,
        duration_hours_total=1.0,
        cost_usd_total=per_hour,
        cost_usd_per_hour_avg=per_hour,
        projected_daily_usd=per_hour * 24,
    )


def test_envelope_skip_when_no_metrics_or_no_ceiling() -> None:
    assert evaluate_endpoint_envelope("X", None, _ceiling(1.0))["status"] == "SKIP"
    assert evaluate_endpoint_envelope("X", _metrics(1.0), None)["status"] == "SKIP"


def test_envelope_pass_within_ceiling() -> None:
    out = evaluate_endpoint_envelope("X", _metrics(0.50), _ceiling(1.00))
    assert out["status"] == "PASS"
    assert out["delta_pct"] == pytest.approx(-50.0)


def test_envelope_warn_band_10_to_20_pct() -> None:
    # +15% over ceiling
    out = evaluate_endpoint_envelope("X", _metrics(1.15), _ceiling(1.00))
    assert out["status"] == "WARN"
    assert COST_REGRESSION_SOFT_WARN_PCT < out["delta_pct"] <= COST_REGRESSION_HARD_FAIL_PCT


def test_envelope_fail_above_hard_fail_band() -> None:
    # +30% over ceiling
    out = evaluate_endpoint_envelope("X", _metrics(1.30), _ceiling(1.00))
    assert out["status"] == "FAIL"
    assert out["delta_pct"] > COST_REGRESSION_HARD_FAIL_PCT


def test_envelope_zero_ceiling_strict_fail_on_any_cost() -> None:
    out = evaluate_endpoint_envelope("X", _metrics(0.01), _ceiling(0.0))
    assert out["status"] == "FAIL"


def test_envelope_zero_ceiling_pass_on_zero_cost() -> None:
    out = evaluate_endpoint_envelope("X", _metrics(0.0), _ceiling(0.0))
    assert out["status"] == "PASS"
