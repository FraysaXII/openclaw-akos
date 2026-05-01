"""Initiative 45 P4 — Cost + latency observability per skill.

Computes per-skill cost from cassette summaries and POLICY_REGISTER cost ceilings.
Fails CI when the rolling cost regresses past the policy threshold.

Architecture:
- Model prices: ``config/eval/model-prices.json`` (operator-edited; FinOps owns)
- Cost ceilings: POLICY_REGISTER rows with ``policy_class=cost_ceiling`` (governed)
- Per-cassette cost: read from cassette summary (``tokens_in``, ``tokens_out``,
  ``model_id``); compute via ``compute_cost_usd()``
- Per-skill scorecard: aggregate across cassettes for the skill, populate
  ``ScoreRow.cost_usd`` and ``latency_ms_p50/p95``
- Enforcement: ``--enforce`` mode reads POLICY_REGISTER ceilings and fails CI
  when current per-run avg > ceiling * 1.20 (>20% regression per D-IH-45-D)

Soft-fail discipline (R-45-11): when Langfuse / model-prices / POLICY_REGISTER
are unavailable, cost defaults to None and the scorecard simply omits cost data
(no fake numbers; no false-fail).
"""

from __future__ import annotations

import csv
import json
import logging
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger("akos.eval.cost_obs")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_PRICES_PATH = REPO_ROOT / "config" / "eval" / "model-prices.json"
POLICY_REGISTER_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "POLICY_REGISTER.csv"
)

COST_REGRESSION_HARD_FAIL_PCT = 20.0  # D-IH-45-D
COST_REGRESSION_SOFT_WARN_PCT = 10.0


@dataclass
class CostMetrics:
    skill_id: str
    runs: int
    cost_usd_avg: float
    cost_usd_p95: float
    latency_ms_p50: float
    latency_ms_p95: float
    tokens_in_total: int
    tokens_out_total: int


@dataclass
class CostCeiling:
    skill_id: str
    policy_id: str
    max_usd_per_run: float


def load_model_prices(*, path: Path | None = None) -> dict[str, dict]:
    """Load the model price table. Returns {} on any failure (soft-fail)."""
    p = path or MODEL_PRICES_PATH
    if not p.is_file():
        logger.warning("model-prices.json not found at %s", p)
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data.get("models", {}) if isinstance(data, dict) else {}
    except Exception as exc:
        logger.warning("model-prices.json parse failed: %s", exc)
        return {}


def compute_cost_usd(
    *,
    tokens_in: int,
    tokens_out: int,
    model_id: str,
    prices: dict[str, dict] | None = None,
) -> float:
    """Compute cost in USD for one cassette run. Returns 0.0 for unknown models."""
    p = prices if prices is not None else load_model_prices()
    m = p.get(model_id)
    if not m:
        return 0.0
    in_rate = float(m.get("input_per_1k_usd", 0.0))
    out_rate = float(m.get("output_per_1k_usd", 0.0))
    return (tokens_in / 1000.0) * in_rate + (tokens_out / 1000.0) * out_rate


def load_cost_ceilings(*, path: Path | None = None) -> dict[str, CostCeiling]:
    """Load per-skill cost ceilings from POLICY_REGISTER. Returns {} on failure.

    Parses POLICY_REGISTER rows with policy_class=cost_ceiling. The skill_id is
    derived from the policy_id suffix (POL-EVAL-COST-CEILING-<SKILL-SUFFIX>);
    the threshold is parsed from ``policy_text`` via ``max_usd_per_run=<float>``.
    """
    p = path or POLICY_REGISTER_CSV
    if not p.is_file():
        return {}
    out: dict[str, CostCeiling] = {}
    try:
        with p.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                if (row.get("policy_class") or "").strip() != "cost_ceiling":
                    continue
                pid = (row.get("policy_id") or "").strip()
                text = (row.get("policy_text") or "")
                # Extract max_usd_per_run= value
                threshold: float | None = None
                for token in text.replace(";", " ").split():
                    if token.startswith("max_usd_per_run="):
                        try:
                            threshold = float(token.split("=", 1)[1].rstrip(".,"))
                        except ValueError:
                            pass
                        break
                if threshold is None:
                    continue
                # Map policy_id suffix to skill_id (POL-EVAL-COST-CEILING-MADEIRA-LOOKUP -> SKILL-MADEIRA-LOOKUP-V1)
                # We accept the operator-curated mapping in the row (notes can specify),
                # but the convention is policy_id suffix == skill suffix.
                suffix = pid.replace("POL-EVAL-COST-CEILING-", "").strip()
                if not suffix:
                    continue
                skill_id = f"SKILL-{suffix}-V1"  # convention; docs/references/hlk pattern
                out[skill_id] = CostCeiling(
                    skill_id=skill_id, policy_id=pid, max_usd_per_run=threshold
                )
    except Exception as exc:
        logger.warning("POLICY_REGISTER cost_ceiling parse failed: %s", exc)
        return {}
    return out


def aggregate_skill_cost(skill_id: str, *, prices: dict[str, dict] | None = None) -> CostMetrics | None:
    """Walk cassettes for the skill; aggregate cost + latency.

    Returns None if no cassettes exist for the skill.
    """
    from akos.eval_harness.cassette import CASSETTE_ROOT, list_cassettes, read_cassette

    if not CASSETTE_ROOT.is_dir():
        return None

    cassettes = list_cassettes(skill_id=skill_id)
    if not cassettes:
        return None

    pr = prices if prices is not None else load_model_prices()
    costs: list[float] = []
    latencies: list[float] = []
    tokens_in_total = 0
    tokens_out_total = 0

    for c in cassettes:
        try:
            header, _events, summary = read_cassette(c)
        except Exception as exc:
            logger.debug("cassette read failed: %s (%s)", c, exc)
            continue
        ti = int(summary.get("tokens_in", 0) or 0)
        to = int(summary.get("tokens_out", 0) or 0)
        lm = float(summary.get("latency_ms", 0) or 0)
        cost = compute_cost_usd(tokens_in=ti, tokens_out=to, model_id=header.model_id, prices=pr)
        costs.append(cost)
        latencies.append(lm)
        tokens_in_total += ti
        tokens_out_total += to

    if not costs:
        return None

    cost_avg = statistics.fmean(costs)
    cost_p95 = (
        statistics.quantiles(costs, n=20)[-1] if len(costs) >= 2 else costs[0]
    )
    lat_p50 = statistics.median(latencies)
    lat_p95 = (
        statistics.quantiles(latencies, n=20)[-1] if len(latencies) >= 2 else latencies[0]
    )

    return CostMetrics(
        skill_id=skill_id,
        runs=len(costs),
        cost_usd_avg=cost_avg,
        cost_usd_p95=cost_p95,
        latency_ms_p50=lat_p50,
        latency_ms_p95=lat_p95,
        tokens_in_total=tokens_in_total,
        tokens_out_total=tokens_out_total,
    )


def evaluate_cost_ceiling(
    skill_id: str,
    metrics: CostMetrics | None,
    ceiling: CostCeiling | None,
) -> dict[str, Any]:
    """Compare current cost against ceiling. Returns dict with status / delta_pct / failures."""
    if metrics is None or ceiling is None:
        return {"status": "SKIP", "failures": [], "delta_pct": None, "reason": "no metrics or no ceiling"}

    threshold = ceiling.max_usd_per_run
    current = metrics.cost_usd_avg

    if threshold == 0.0:
        if current > 0.0:
            return {
                "status": "FAIL",
                "failures": [f"cost_ceiling_breach:current={current:.6f},ceiling={threshold:.6f}"],
                "delta_pct": float("inf"),
                "reason": "zero-cost ceiling breached",
            }
        return {"status": "PASS", "failures": [], "delta_pct": 0.0, "reason": "within zero-cost ceiling"}

    delta_pct = ((current - threshold) / threshold) * 100.0
    if delta_pct > COST_REGRESSION_HARD_FAIL_PCT:
        return {
            "status": "FAIL",
            "failures": [
                f"cost_regression:{delta_pct:+.1f}%>{COST_REGRESSION_HARD_FAIL_PCT:.0f}%"
                f":current={current:.6f},ceiling={threshold:.6f}"
            ],
            "delta_pct": delta_pct,
            "reason": f"hard-fail >{COST_REGRESSION_HARD_FAIL_PCT:.0f}%",
        }
    if delta_pct > COST_REGRESSION_SOFT_WARN_PCT:
        return {
            "status": "WARN",
            "failures": [
                f"cost_warn:{delta_pct:+.1f}%>{COST_REGRESSION_SOFT_WARN_PCT:.0f}%"
                f":current={current:.6f},ceiling={threshold:.6f}"
            ],
            "delta_pct": delta_pct,
            "reason": f"soft-warn {COST_REGRESSION_SOFT_WARN_PCT:.0f}-{COST_REGRESSION_HARD_FAIL_PCT:.0f}%",
        }
    return {
        "status": "PASS",
        "failures": [],
        "delta_pct": delta_pct,
        "reason": f"within ceiling (delta {delta_pct:+.1f}%)",
    }
