#!/usr/bin/env python3
"""Initiative 49 — Rewrite ``priority_score`` on PERSONA_SCENARIO_REGISTRY.csv.

Leaves ``safety_lane`` and ``release_blocking`` untouched (operator-maintained).

Usage::

    py scripts/recalculate_persona_scenario_priorities.py
    py scripts/recalculate_persona_scenario_priorities.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_persona_scenario_priority import rewrite_persona_registry_priority_scores
from akos.io import REPO_ROOT as IO_REPO_ROOT

CSV_PATH = IO_REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "PERSONA_SCENARIO_REGISTRY.csv"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--dry-run", action="store_true", help="Compute only; print first 5 deltas")
    args = ap.parse_args()

    if not CSV_PATH.is_file():
        print("FAIL: PERSONA_SCENARIO_REGISTRY.csv missing")
        return 1

    if args.dry_run:
        rows, delta = rewrite_persona_registry_priority_scores(CSV_PATH, dry_run=True)
        print(f"Would update priority_score on {rows} rows; ~{delta} values would change:")
        print("  (omit --dry-run to apply; deltas not enumerated in dry-run mode)")
        return 0

    rows, delta = rewrite_persona_registry_priority_scores(CSV_PATH, dry_run=False)
    print(f"Wrote {rows} rows; priority_score changed on {delta} rows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
