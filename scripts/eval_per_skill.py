#!/usr/bin/env python3
"""Initiative 32 P9 — Per-skill eval scorecard generator.

Reads SKILL_REGISTRY.csv + per-skill baseline JSONs from config/eval-baselines/,
optionally computes a "current" score (placeholder; in a real runtime this
reads Langfuse traces or a similar telemetry surface), and emits a per-skill
scorecard.

Tripping the 5 canaries (per the I32 plan + D-IH-32-I lazy-load posture):

  Canary 1 (bootstrap drift):     scripts/check-drift.py flags an undeclared skill
  Canary 2 (eval regression):     this script flags a > 2pp drop from baseline
  Canary 3 (trace shape):         Langfuse trace traverses > 3 skills (op-side)
  Canary 4 (validator FK reject): scripts/validate_skill_registry.py rejects bad FK
  Canary 5 (UAT smoke):           "should I ask the Orchestrator?" fallback (op-side)

This script focuses on Canary 2 (and emits a clean scorecard for canaries 1, 3, 4, 5
to consume). Synthetic regression test in tests/test_madeira_eval_per_skill.py
proves canary 2 trips when a 3pp drop is injected.

Usage::

    py scripts/eval_per_skill.py                 # human-readable scorecard
    py scripts/eval_per_skill.py --json          # machine-readable JSON
    py scripts/eval_per_skill.py --threshold 2.0 # canary 2 threshold (default 2.0pp)
    py scripts/eval_per_skill.py --current <skill_id>=<pct>  # inject current score (testing)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT

SKILL_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SKILL_REGISTRY.csv"
BASELINES_DIR = REPO_ROOT / "config" / "eval-baselines"


def _load_skill_baselines() -> dict[str, float]:
    """Load skill_id -> eval_baseline_pct from each baseline JSON file."""
    baselines: dict[str, float] = {}
    if not BASELINES_DIR.is_dir():
        return baselines
    for p in BASELINES_DIR.glob("skill_*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            sid = data.get("skill_id")
            ebp = data.get("eval_baseline_pct")
            if sid and isinstance(ebp, (int, float)):
                baselines[sid] = float(ebp)
        except Exception:
            continue
    return baselines


def _load_skill_registry() -> dict[str, dict]:
    """Load skill rows keyed by skill_id."""
    if not SKILL_CSV.is_file():
        return {}
    with SKILL_CSV.open(encoding="utf-8", newline="") as fh:
        return {r["skill_id"]: r for r in csv.DictReader(fh)}


def _parse_current_overrides(current_args: list[str]) -> dict[str, float]:
    """Parse --current skill_id=pct overrides (used in synthetic regression tests)."""
    out: dict[str, float] = {}
    for arg in current_args or []:
        if "=" not in arg:
            continue
        sid, pct = arg.split("=", 1)
        try:
            out[sid.strip()] = float(pct.strip())
        except ValueError:
            continue
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Per-skill eval scorecard generator (Initiative 32 P9)")
    parser.add_argument("--json", action="store_true", help="Emit JSON scorecard on stdout")
    parser.add_argument(
        "--threshold", type=float, default=2.0,
        help="Canary 2 threshold in percentage points (default 2.0pp)",
    )
    parser.add_argument(
        "--current", action="append", default=[],
        help="Override current score: --current SKILL-ID=PCT (repeatable)",
    )
    args = parser.parse_args()

    registry = _load_skill_registry()
    baselines = _load_skill_baselines()
    overrides = _parse_current_overrides(args.current)

    scorecard: list[dict] = []
    canary_2_trips: list[str] = []

    for sid, row in sorted(registry.items()):
        baseline = baselines.get(sid)
        if baseline is None:
            # Treat the SKILL_REGISTRY.csv eval_baseline_pct as the live baseline
            # if no separate JSON exists yet (initial-bootstrap-friendly).
            try:
                baseline = float(row.get("eval_baseline_pct", "0") or "0")
            except ValueError:
                baseline = 0.0
        # Current score: explicit override (testing) or echo baseline (no live runtime here).
        current = overrides.get(sid, baseline)
        delta = current - baseline
        canary_2_tripped = delta < -args.threshold
        if canary_2_tripped:
            canary_2_trips.append(sid)
        scorecard.append({
            "skill_id": sid,
            "name": row.get("name", ""),
            "agents_supported": row.get("agents_supported", ""),
            "axes_consumed": row.get("axes_consumed", ""),
            "baseline_pct": baseline,
            "current_pct": current,
            "delta_pp": round(delta, 2),
            "canary_2_tripped": canary_2_tripped,
            "lifecycle_status": row.get("lifecycle_status", ""),
        })

    overall = {
        "skills_total": len(scorecard),
        "skills_with_baseline_json": len(baselines),
        "canary_2_threshold_pp": args.threshold,
        "canary_2_trips_count": len(canary_2_trips),
        "canary_2_trips": canary_2_trips,
        "overall_status": "fail" if canary_2_trips else "pass",
        "scorecard": scorecard,
    }

    if args.json:
        json.dump(overall, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        print("\n  Madeira per-skill eval scorecard (Initiative 32 P9)")
        print("  " + "=" * 60)
        for row in scorecard:
            marker = " !! CANARY 2 TRIPPED" if row["canary_2_tripped"] else ""
            print(
                f"  {row['skill_id']:36s}  baseline={row['baseline_pct']:5.1f}  "
                f"current={row['current_pct']:5.1f}  delta={row['delta_pp']:+5.1f}pp{marker}"
            )
        print()
        print(f"  skills:                {overall['skills_total']}")
        print(f"  with baseline JSON:    {overall['skills_with_baseline_json']}")
        print(f"  canary 2 threshold:    {overall['canary_2_threshold_pp']}pp")
        print(f"  canary 2 trips:        {overall['canary_2_trips_count']}")
        print()
        print(f"  OVERALL: {overall['overall_status'].upper()}")

    return 1 if canary_2_trips else 0


if __name__ == "__main__":
    sys.exit(main())
