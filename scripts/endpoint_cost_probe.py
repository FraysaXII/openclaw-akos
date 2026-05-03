#!/usr/bin/env python3
"""Initiative 52 P5 — Endpoint cost probe (RunPod / Kalavai per-GPU-hour).

Reads observed endpoint runs (offline JSONL log or stub fixture) and emits a
human-readable per-endpoint cost report. Mirrors ``scripts/cost_obs.py`` for
the per-token pathway, but uses the unit-discriminated path
``akos.eval_harness.cost_obs.aggregate_endpoint_cost`` so the reader never
has to reason about token vs gpu_hour mathematics.

Run::

    py scripts/endpoint_cost_probe.py --runs-jsonl artifacts/endpoint-runs/*.jsonl
    py scripts/endpoint_cost_probe.py --stub  # built-in mock fixture
    py scripts/endpoint_cost_probe.py --stub --json  # machine-readable output

The probe is offline-by-design: it does NOT call RunPod / Kalavai APIs.
Operators feed it observed run logs; the live-API calibration is bound to
the next AKOS_RECORD_LIVE=1 cycle (see I52 P3 / OPS-52-1 for symmetry with
the multi-judge calibration burn).

Exit codes:
- 0: report written
- 1: invalid args
- 2: no runs found / empty input
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.eval_harness.cost_obs import (  # noqa: E402
    EndpointMetrics,
    aggregate_endpoint_cost,
    load_endpoint_ceilings,
    load_endpoint_prices,
    evaluate_endpoint_envelope,
)

REPORT_DIR = REPO_ROOT / "artifacts" / "endpoint-cost"


def _stub_runs() -> dict[str, list[dict[str, float]]]:
    """Built-in mock fixture for dispatcher validation (R-52-3)."""
    return {
        "runpod:a100-80gb": [
            {"duration_hours": 0.5},
            {"duration_hours": 1.25},
            {"duration_hours": 0.75},
        ],
        "runpod:h100-80gb": [
            {"duration_hours": 0.10},
        ],
        "kalavai:default": [
            {"duration_hours": 2.0},
            {"duration_hours": 1.5},
        ],
    }


def _load_runs_jsonl(paths: list[Path]) -> dict[str, list[dict[str, float]]]:
    """Load endpoint runs from JSONL files. Each line: {endpoint_id, duration_hours, ...}."""
    out: dict[str, list[dict[str, float]]] = {}
    for path in paths:
        if not path.is_file():
            print(f"[probe] WARN: {path} not found, skipping", file=sys.stderr)
            continue
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError as exc:
                    print(f"[probe] WARN: malformed line in {path}: {exc}", file=sys.stderr)
                    continue
                eid = rec.get("endpoint_id")
                if not eid:
                    continue
                out.setdefault(eid, []).append(
                    {"duration_hours": float(rec.get("duration_hours", 0.0))}
                )
    return out


def _render_markdown(
    *,
    runs_by_endpoint: dict[str, list[dict[str, float]]],
    metrics_by_endpoint: dict[str, EndpointMetrics],
    envelope_by_endpoint: dict[str, dict],
    ts: str,
    is_stub: bool,
) -> str:
    lines = [
        f"# Endpoint cost probe — {ts}",
        "",
        f"**Mode:** {'STUB FIXTURE (dispatcher validation only)' if is_stub else 'JSONL log replay'}",
        "",
        "## Summary",
        "",
        "| endpoint_id | runs | duration_hours | cost_usd_total | cost_per_hour_avg | projected_daily | envelope |",
        "|:--|--:|--:|--:|--:|--:|:--|",
    ]
    for eid in sorted(runs_by_endpoint.keys()):
        m = metrics_by_endpoint.get(eid)
        env = envelope_by_endpoint.get(eid, {"status": "SKIP"})
        if m is None:
            lines.append(f"| `{eid}` | 0 | - | - | - | - | SKIP |")
            continue
        lines.append(
            f"| `{eid}` | {m.runs} | {m.duration_hours_total:.3f} | "
            f"${m.cost_usd_total:.4f} | ${m.cost_usd_per_hour_avg:.4f} | "
            f"${m.projected_daily_usd:.2f} | {env['status']} |"
        )
    lines.append("")
    lines.append("## Envelope details")
    lines.append("")
    for eid in sorted(envelope_by_endpoint.keys()):
        env = envelope_by_endpoint[eid]
        lines.append(f"- `{eid}`: **{env['status']}** — {env.get('reason', '')}")
        for f in env.get("failures", []) or []:
            lines.append(f"  - {f}")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append(
        "- Pricing source: `config/eval/endpoint-prices.json` (per-GPU-hour SSOT, "
        "separate from `config/eval/model-prices.json` per D-IH-52-E)."
    )
    lines.append(
        "- Ceilings: POLICY_REGISTER `cost_ceiling` rows whose policy_id contains "
        "`ENDPOINT-` (POL-EVAL-COST-CEILING-ENDPOINT-{RUNPOD,KALAVAI}-V1)."
    )
    lines.append(
        "- Daily projection = `cost_per_hour_avg * 24` (informational; not the "
        "envelope-alarm trigger — see `scripts/endpoint_envelope_alarm.py`)."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="I52 P5 endpoint cost probe")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument(
        "--runs-jsonl",
        nargs="+",
        type=Path,
        help="One or more JSONL files where each line has endpoint_id + duration_hours",
    )
    src.add_argument(
        "--stub",
        action="store_true",
        help="Use built-in mock fixture (dispatcher validation; no live data)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a machine-readable JSON sidecar instead of (in addition to) markdown.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=REPORT_DIR,
        help=f"Output directory (default: {REPORT_DIR.relative_to(REPO_ROOT)})",
    )
    args = parser.parse_args()

    if args.stub:
        runs_by_endpoint = _stub_runs()
        is_stub = True
    else:
        runs_by_endpoint = _load_runs_jsonl(args.runs_jsonl or [])
        is_stub = False

    if not runs_by_endpoint:
        print("[probe] No endpoint runs to report.", file=sys.stderr)
        return 2

    prices = load_endpoint_prices()
    ceilings = load_endpoint_ceilings()

    metrics_by_endpoint: dict[str, EndpointMetrics] = {}
    envelope_by_endpoint: dict[str, dict] = {}
    for eid, runs in runs_by_endpoint.items():
        m = aggregate_endpoint_cost(eid, runs, endpoint_prices=prices)
        metrics_by_endpoint[eid] = m
        # POL key uses the upper portion after "ENDPOINT-"; e.g. runpod:a100-80gb
        # is gated by POL-EVAL-COST-CEILING-ENDPOINT-RUNPOD-V1 (RUNPOD).
        ceiling_key = eid.split(":")[0].upper()
        ceiling = ceilings.get(ceiling_key)
        envelope_by_endpoint[eid] = evaluate_endpoint_envelope(eid, m, ceiling)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    md_path = args.out_dir / f"endpoint-cost-probe-{ts}.md"
    json_path = args.out_dir / f"endpoint-cost-probe-{ts}.json"

    md = _render_markdown(
        runs_by_endpoint=runs_by_endpoint,
        metrics_by_endpoint=metrics_by_endpoint,
        envelope_by_endpoint=envelope_by_endpoint,
        ts=ts,
        is_stub=is_stub,
    )
    md_path.write_text(md, encoding="utf-8")

    sidecar = {
        "ts_utc": ts,
        "is_stub": is_stub,
        "endpoints": {
            eid: {
                "runs": m.runs,
                "duration_hours_total": m.duration_hours_total,
                "cost_usd_total": m.cost_usd_total,
                "cost_usd_per_hour_avg": m.cost_usd_per_hour_avg,
                "projected_daily_usd": m.projected_daily_usd,
                "envelope": envelope_by_endpoint[eid],
            }
            for eid, m in metrics_by_endpoint.items()
            if m is not None
        },
    }
    json_path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")

    print(f"[probe] markdown: {md_path.relative_to(REPO_ROOT)}")
    print(f"[probe] json    : {json_path.relative_to(REPO_ROOT)}")

    if args.json:
        print(json.dumps(sidecar, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
