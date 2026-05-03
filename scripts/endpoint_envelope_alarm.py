#!/usr/bin/env python3
"""Initiative 52 P5 — Endpoint envelope alarm (G-52-4 gate).

Companion to ``scripts/endpoint_cost_probe.py``: takes a probe JSON sidecar
(or runs the probe internally) and exits non-zero when any endpoint breaches
its POLICY_REGISTER ceiling beyond the hard-fail band (>20% per D-IH-45-D
symmetry).

Run::

    py scripts/endpoint_envelope_alarm.py --probe-json artifacts/endpoint-cost/endpoint-cost-probe-*.json
    py scripts/endpoint_envelope_alarm.py --stub  # composes a stub probe inline

Used as the G-52-4 hard-fail gate in eval-tier-b.yml (I52 P7) so a misrouted
serverless run cannot silently rack up GPU-hours.

Exit codes:
- 0: all endpoints PASS or WARN
- 1: invalid args
- 2: at least one endpoint FAIL (envelope breach beyond hard-fail band)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.eval_harness.cost_obs import (  # noqa: E402
    aggregate_endpoint_cost,
    evaluate_endpoint_envelope,
    load_endpoint_ceilings,
    load_endpoint_prices,
)


def _stub_runs() -> dict[str, list[dict[str, float]]]:
    return {
        "runpod:a100-80gb": [
            {"duration_hours": 0.5},
            {"duration_hours": 0.5},
        ],
        "kalavai:default": [
            {"duration_hours": 1.0},
        ],
    }


def _evaluate_runs(
    runs_by_endpoint: dict[str, list[dict[str, float]]],
) -> tuple[int, list[str]]:
    """Returns (worst_status_code, lines_for_stdout). status_code: 0 PASS, 1 WARN, 2 FAIL."""
    prices = load_endpoint_prices()
    ceilings = load_endpoint_ceilings()
    lines: list[str] = []
    worst = 0  # 0 PASS, 1 WARN, 2 FAIL
    for eid, runs in sorted(runs_by_endpoint.items()):
        m = aggregate_endpoint_cost(eid, runs, endpoint_prices=prices)
        ceiling_key = eid.split(":")[0].upper()
        ceiling = ceilings.get(ceiling_key)
        env = evaluate_endpoint_envelope(eid, m, ceiling)
        status = env.get("status", "SKIP")
        reason = env.get("reason", "")
        if m is None:
            lines.append(f"  - {eid}: {status} (no metrics)")
            continue
        lines.append(
            f"  - {eid}: {status} — per_hour=${m.cost_usd_per_hour_avg:.4f} "
            f"daily_proj=${m.projected_daily_usd:.2f} "
            f"ceiling={'$' + format(ceiling.max_usd_per_hour, '.4f') if ceiling else 'N/A'} "
            f"({reason})"
        )
        if status == "FAIL":
            worst = max(worst, 2)
        elif status == "WARN":
            worst = max(worst, 1)
    return worst, lines


def main() -> int:
    parser = argparse.ArgumentParser(description="I52 P5 endpoint envelope alarm (G-52-4)")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument(
        "--probe-json",
        type=Path,
        help="Path to a sidecar JSON emitted by scripts/endpoint_cost_probe.py",
    )
    src.add_argument(
        "--stub",
        action="store_true",
        help="Run with an internal stub fixture (dispatcher validation only)",
    )
    parser.add_argument(
        "--warn-as-fail",
        action="store_true",
        help="Treat WARN as exit-2 (stricter mode for canary runs)",
    )
    args = parser.parse_args()

    if args.stub:
        runs_by_endpoint = _stub_runs()
        worst, lines = _evaluate_runs(runs_by_endpoint)
    else:
        if not args.probe_json or not args.probe_json.is_file():
            print(f"[alarm] FAIL: probe JSON not found: {args.probe_json}", file=sys.stderr)
            return 1
        try:
            sidecar = json.loads(args.probe_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"[alarm] FAIL: probe JSON malformed: {exc}", file=sys.stderr)
            return 1
        # Reconstruct minimal runs from sidecar duration totals.
        # Each endpoint becomes a single synthesized run carrying the
        # aggregated duration; aggregate_endpoint_cost is unit-pure so the
        # average per-hour stays correct.
        runs_by_endpoint = {
            eid: [{"duration_hours": float(d.get("duration_hours_total", 0.0))}]
            for eid, d in (sidecar.get("endpoints") or {}).items()
        }
        if not runs_by_endpoint:
            print("[alarm] FAIL: probe sidecar contains no endpoints", file=sys.stderr)
            return 1
        worst, lines = _evaluate_runs(runs_by_endpoint)

    print("[alarm] Endpoint envelope evaluation:")
    for line in lines:
        print(line)

    if worst >= 2:
        print("[alarm] result: FAIL (at least one endpoint exceeded hard-fail band)")
        return 2
    if worst >= 1 and args.warn_as_fail:
        print("[alarm] result: WARN (treated as FAIL via --warn-as-fail)")
        return 2
    if worst >= 1:
        print("[alarm] result: WARN (within soft-warn band)")
        return 0
    print("[alarm] result: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
