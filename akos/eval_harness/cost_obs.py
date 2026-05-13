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
ENDPOINT_PRICES_PATH = REPO_ROOT / "config" / "eval" / "endpoint-prices.json"
POLICY_REGISTER_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "POLICY_REGISTER.csv"
)

COST_REGRESSION_HARD_FAIL_PCT = 20.0  # D-IH-45-D
COST_REGRESSION_SOFT_WARN_PCT = 10.0

# I52 P5 (D-IH-52-D / D-IH-52-E): unit discriminator on every CostRecord.
# - "token"     -> per-token providers (Anthropic, OpenAI, ...) read model-prices.json
# - "gpu_hour"  -> per-GPU-hour endpoints (RunPod, Kalavai, ...) read endpoint-prices.json
VALID_COST_UNITS: tuple[str, ...] = ("token", "gpu_hour")
DEFAULT_COST_UNIT = "token"
ENDPOINT_HOURLY_TO_DAILY_PROJECTION = 24.0
ENDPOINT_HOURLY_MICRO_ENVELOPE_FACTOR = 1.5  # R-52-5 mitigation


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


@dataclass
class CostRecord:
    """I52 P5 (D-IH-52-D): unit-aware cost record.

    The `unit` field is the discriminator that determines:
      - "token":    cost = (tokens_in/1k * in_rate) + (tokens_out/1k * out_rate)
                    via model-prices.json
      - "gpu_hour": cost = duration_hours * usd_per_hour
                    via endpoint-prices.json

    Operators MUST set `unit` explicitly when authoring CostRecords; mixing
    units silently is a governance violation per D-IH-52-E (no mixed-unit
    aggregation in cost ceilings).
    """

    cost_usd: float
    unit: str
    model_id: str | None = None
    endpoint_id: str | None = None
    tokens_in: int = 0
    tokens_out: int = 0
    duration_hours: float = 0.0

    def __post_init__(self) -> None:
        if self.unit not in VALID_COST_UNITS:
            raise ValueError(
                f"CostRecord.unit must be one of {VALID_COST_UNITS}; got {self.unit!r}"
            )
        if self.unit == "token" and not self.model_id:
            raise ValueError("CostRecord with unit='token' requires model_id")
        if self.unit == "gpu_hour" and not self.endpoint_id:
            raise ValueError("CostRecord with unit='gpu_hour' requires endpoint_id")


@dataclass
class EndpointPrice:
    """I52 P5: per-endpoint hourly pricing row (RunPod, Kalavai, ...)."""

    endpoint_id: str
    provider: str
    gpu_class: str
    usd_per_hour: float
    notes: str = ""


@dataclass
class EndpointCeiling:
    """I52 P5: per-endpoint hourly cost ceiling row.

    Sourced from POLICY_REGISTER rows with policy_class=cost_ceiling AND
    policy_id matching POL-EVAL-COST-CEILING-ENDPOINT-<NAME>-V*.
    """

    endpoint_id: str
    policy_id: str
    max_usd_per_hour: float


@dataclass
class EndpointMetrics:
    endpoint_id: str
    runs: int
    duration_hours_total: float
    cost_usd_total: float
    cost_usd_per_hour_avg: float
    projected_daily_usd: float


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


def load_endpoint_prices(*, path: Path | None = None) -> dict[str, EndpointPrice]:
    """I52 P5: Load the endpoint price table. Returns {} on any failure (soft-fail).

    Endpoint prices express per-GPU-hour rates for RunPod / Kalavai-style
    serverless GPU endpoints. They are deliberately a SEPARATE SSOT from
    model-prices.json (per D-IH-52-E) to keep token vs gpu_hour units from
    co-mingling in any single cost computation path.
    """
    p = path or ENDPOINT_PRICES_PATH
    if not p.is_file():
        logger.warning("endpoint-prices.json not found at %s", p)
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("endpoint-prices.json parse failed: %s", exc)
        return {}
    raw = data.get("endpoints", {}) if isinstance(data, dict) else {}
    out: dict[str, EndpointPrice] = {}
    for endpoint_id, row in raw.items():
        if not isinstance(row, dict):
            continue
        try:
            out[endpoint_id] = EndpointPrice(
                endpoint_id=endpoint_id,
                provider=str(row.get("provider", "")),
                gpu_class=str(row.get("gpu_class", "")),
                usd_per_hour=float(row.get("usd_per_hour", 0.0)),
                notes=str(row.get("notes", "")),
            )
        except (TypeError, ValueError) as exc:
            logger.warning("endpoint-prices row %r invalid: %s", endpoint_id, exc)
    return out


def compute_cost_record(
    *,
    unit: str,
    tokens_in: int = 0,
    tokens_out: int = 0,
    model_id: str | None = None,
    endpoint_id: str | None = None,
    duration_hours: float = 0.0,
    prices: dict[str, dict] | None = None,
    endpoint_prices: dict[str, EndpointPrice] | None = None,
) -> CostRecord:
    """I52 P5 (D-IH-52-D): unit-aware cost computation.

    Single entry point for any new cost-bearing event. The `unit` discriminator
    selects the rate table:
      - "token":    model-prices.json (existing pathway, unchanged)
      - "gpu_hour": endpoint-prices.json (new in I52)

    Soft-fail discipline (R-45-11 + R-52-3): unknown rates -> cost 0.0; the
    record is still emitted so downstream aggregation can flag missing pricing.
    """
    if unit == "token":
        if not model_id:
            raise ValueError("compute_cost_record(unit='token') requires model_id")
        cost = compute_cost_usd(
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            model_id=model_id,
            prices=prices,
        )
        return CostRecord(
            cost_usd=cost,
            unit="token",
            model_id=model_id,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
        )
    if unit == "gpu_hour":
        if not endpoint_id:
            raise ValueError("compute_cost_record(unit='gpu_hour') requires endpoint_id")
        ep_prices = endpoint_prices if endpoint_prices is not None else load_endpoint_prices()
        ep = ep_prices.get(endpoint_id)
        rate = float(ep.usd_per_hour) if ep is not None else 0.0
        return CostRecord(
            cost_usd=duration_hours * rate,
            unit="gpu_hour",
            endpoint_id=endpoint_id,
            duration_hours=duration_hours,
        )
    raise ValueError(
        f"compute_cost_record: unit must be one of {VALID_COST_UNITS}; got {unit!r}"
    )


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


def load_endpoint_ceilings(*, path: Path | None = None) -> dict[str, EndpointCeiling]:
    """I52 P5: Load per-endpoint hourly cost ceilings from POLICY_REGISTER.

    Looks for rows where:
      - policy_class=cost_ceiling
      - policy_id matches POL-EVAL-COST-CEILING-ENDPOINT-<NAME>-V*

    Threshold parsed from policy_text via ``max_usd_per_hour=<float>``. The
    ENDPOINT-<NAME> portion of the policy_id is used as the endpoint_id key.
    """
    p = path or POLICY_REGISTER_CSV
    if not p.is_file():
        return {}
    out: dict[str, EndpointCeiling] = {}
    try:
        with p.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                if (row.get("policy_class") or "").strip() != "cost_ceiling":
                    continue
                pid = (row.get("policy_id") or "").strip()
                if "ENDPOINT-" not in pid:
                    continue
                text = row.get("policy_text") or ""
                threshold: float | None = None
                for token in text.replace(";", " ").split():
                    if token.startswith("max_usd_per_hour="):
                        try:
                            threshold = float(token.split("=", 1)[1].rstrip(".,"))
                        except ValueError:
                            pass
                        break
                if threshold is None:
                    continue
                # POL-EVAL-COST-CEILING-ENDPOINT-RUNPOD-V1 -> endpoint_id = RUNPOD
                marker = "ENDPOINT-"
                idx = pid.find(marker)
                if idx < 0:
                    continue
                tail = pid[idx + len(marker):]
                # Strip trailing -V<n>
                parts = tail.rsplit("-V", 1)
                endpoint_key = parts[0] if len(parts) == 2 and parts[1].isdigit() else tail
                out[endpoint_key] = EndpointCeiling(
                    endpoint_id=endpoint_key,
                    policy_id=pid,
                    max_usd_per_hour=threshold,
                )
    except Exception as exc:
        logger.warning("POLICY_REGISTER endpoint cost_ceiling parse failed: %s", exc)
        return {}
    return out


def aggregate_endpoint_cost(
    endpoint_id: str,
    runs: list[dict[str, Any]],
    *,
    endpoint_prices: dict[str, EndpointPrice] | None = None,
) -> EndpointMetrics | None:
    """I52 P5: Aggregate hourly cost across N endpoint runs.

    Each run dict must include ``duration_hours`` (float). Returns None if
    no runs are supplied. Computes a daily projection using the
    ``ENDPOINT_HOURLY_TO_DAILY_PROJECTION`` factor (24h) for the envelope
    alarm path.
    """
    if not runs:
        return None
    ep_prices = endpoint_prices if endpoint_prices is not None else load_endpoint_prices()
    ep = ep_prices.get(endpoint_id)
    rate = float(ep.usd_per_hour) if ep is not None else 0.0

    duration_total = 0.0
    cost_total = 0.0
    for r in runs:
        dh = float(r.get("duration_hours", 0.0) or 0.0)
        duration_total += dh
        cost_total += dh * rate

    avg_per_hour = (cost_total / duration_total) if duration_total > 0 else 0.0
    projected_daily = avg_per_hour * ENDPOINT_HOURLY_TO_DAILY_PROJECTION

    return EndpointMetrics(
        endpoint_id=endpoint_id,
        runs=len(runs),
        duration_hours_total=duration_total,
        cost_usd_total=cost_total,
        cost_usd_per_hour_avg=avg_per_hour,
        projected_daily_usd=projected_daily,
    )


def evaluate_endpoint_envelope(
    endpoint_id: str,
    metrics: EndpointMetrics | None,
    ceiling: EndpointCeiling | None,
) -> dict[str, Any]:
    """I52 P5: Compare endpoint hourly cost against the per-endpoint ceiling.

    Reuses the 10/20pct soft/hard regression bands from the per-token
    pathway (D-IH-45-D) for symmetry. The headline metric is
    ``cost_usd_per_hour_avg``; the daily projection is informational.
    """
    if metrics is None or ceiling is None:
        return {
            "status": "SKIP",
            "failures": [],
            "delta_pct": None,
            "reason": "no metrics or no ceiling",
        }
    threshold = ceiling.max_usd_per_hour
    current = metrics.cost_usd_per_hour_avg
    if threshold == 0.0:
        if current > 0.0:
            return {
                "status": "FAIL",
                "failures": [
                    f"endpoint_envelope_breach:current_per_hour={current:.4f},"
                    f"ceiling_per_hour={threshold:.4f}"
                ],
                "delta_pct": float("inf"),
                "reason": "zero-cost endpoint ceiling breached",
            }
        return {"status": "PASS", "failures": [], "delta_pct": 0.0, "reason": "within zero-cost endpoint ceiling"}
    delta_pct = ((current - threshold) / threshold) * 100.0
    if delta_pct > COST_REGRESSION_HARD_FAIL_PCT:
        return {
            "status": "FAIL",
            "failures": [
                f"endpoint_envelope_hard:{delta_pct:+.1f}%>{COST_REGRESSION_HARD_FAIL_PCT:.0f}%"
                f":current_per_hour={current:.4f},ceiling_per_hour={threshold:.4f}"
            ],
            "delta_pct": delta_pct,
            "reason": f"hard-fail >{COST_REGRESSION_HARD_FAIL_PCT:.0f}%",
        }
    if delta_pct > COST_REGRESSION_SOFT_WARN_PCT:
        return {
            "status": "WARN",
            "failures": [
                f"endpoint_envelope_warn:{delta_pct:+.1f}%>{COST_REGRESSION_SOFT_WARN_PCT:.0f}%"
                f":current_per_hour={current:.4f},ceiling_per_hour={threshold:.4f}"
            ],
            "delta_pct": delta_pct,
            "reason": f"soft-warn {COST_REGRESSION_SOFT_WARN_PCT:.0f}-{COST_REGRESSION_HARD_FAIL_PCT:.0f}%",
        }
    return {
        "status": "PASS",
        "failures": [],
        "delta_pct": delta_pct,
        "reason": f"within endpoint ceiling (delta {delta_pct:+.1f}%)",
    }
