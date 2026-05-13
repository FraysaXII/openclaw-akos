#!/usr/bin/env python3
"""Initiative 47 P10 — Scenario calibration meta-eval (D-IH-47-C).

Computes the difficulty distribution per persona AND overall against the
40/40/10/10 target with tolerance ±5 percentage points. Emits a calibration
report file + writes back the operator-overridable distribution snapshot to
``artifacts/calibration/calibration-baseline-<UTC-timestamp>.{md,json}``.

Run::

    py scripts/calibrate_scenarios.py
    py scripts/calibrate_scenarios.py --persona OPERATOR
    py scripts/calibrate_scenarios.py --hard-fail-on-drift   # CI-friendly mode
    py scripts/calibrate_scenarios.py --write-priority-scores  # Initiative 49: refresh CSV priorities

Exit codes:
- 0: all calibrations within tolerance
- 1: at least one persona outside tolerance (only with --hard-fail-on-drift)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.eval_harness.persona import (
    CALIBRATION_TARGET,
    CALIBRATION_TOLERANCE_PP,
    calibration_distribution,
    load_persona_scenarios,
    render_calibration_markdown,
)

ARTIFACTS = REPO_ROOT / "artifacts" / "calibration"
ARTIFACTS.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="I47 P10 scenario calibration meta-eval")
    parser.add_argument("--persona", default="", help="Filter to a single persona_id (default: all).")
    parser.add_argument(
        "--hard-fail-on-drift",
        action="store_true",
        help="Exit non-zero when any persona is outside tolerance (CI mode).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print summary only; suppress full markdown output.",
    )
    parser.add_argument(
        "--write-priority-scores",
        action="store_true",
        help=(
            "Initiative 49 - after calibration, rewrite PERSONA_SCENARIO_REGISTRY.csv "
            "priority_score via akos.hlk_persona_scenario_priority (deterministic)."
        ),
    )
    args = parser.parse_args()

    scenarios = load_persona_scenarios()
    if args.persona:
        scenarios = [r for r in scenarios if r.get("persona_id") == args.persona]
        if not scenarios:
            print(f"FAIL: no scenarios found for persona_id={args.persona!r}")
            return 1

    results = calibration_distribution(scenarios=scenarios)
    md = render_calibration_markdown(results)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    md_out = ARTIFACTS / f"calibration-baseline-{ts}.md"
    json_out = ARTIFACTS / f"calibration-baseline-{ts}.json"
    md_out.write_text(md, encoding="utf-8")

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": CALIBRATION_TARGET,
        "tolerance_pp": CALIBRATION_TOLERANCE_PP,
        "personas": {},
        "overall_pass": True,
    }
    for pid, r in sorted(results.items()):
        summary["personas"][pid] = {
            "total": r.total,
            "counts": r.counts,
            "pct": r.pct,
            "deltas_pp": r.deltas_pp,
            "within_tolerance": r.within_tolerance,
            "overall_pass": r.overall_pass,
        }
        if not r.overall_pass:
            summary["overall_pass"] = False
    json_out.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    if not args.quiet:
        print(md)
    failures = [pid for pid, r in results.items() if not r.overall_pass]
    if failures:
        print(f"WARNING: {len(failures)} persona(s) outside +/-{CALIBRATION_TOLERANCE_PP}pp tolerance: {sorted(failures)}")
    print(f"Calibration report written: {md_out}")
    print(f"Calibration JSON written:   {json_out}")

    if args.hard_fail_on_drift and failures:
        return 1

    if args.write_priority_scores:
        from akos.hlk_persona_scenario_priority import rewrite_persona_registry_priority_scores

        csv_out = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "PERSONA_SCENARIO_REGISTRY.csv"
        try:
            n, delta = rewrite_persona_registry_priority_scores(csv_out)
        except ValueError as e:
            print(f"FAIL: could not rewrite priority_score - {e}")
            return 1
        msg = f"I49 priority_score rewrite: {n} rows written; {delta} cells changed.\n"
        if not args.quiet:
            print(msg)
        else:
            sys.stdout.write(msg)

    return 0


if __name__ == "__main__":
    sys.exit(main())
