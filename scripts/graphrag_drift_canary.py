#!/usr/bin/env python3
"""Initiative 46 P2 — Neo4j drift canary.

Compares Neo4j node counts (governance KG, use-case A) against canonical CSV
row counts. Fails on >1 row deviation per dimension (allows for in-flight
syncs between CSV edit and the next ``sync_hlk_neo4j.py`` run).

Reads count snapshots from a Cypher MATCH per node label vs the CSV row counts
sourced from each dimension's akos contract. SKIPs gracefully when Neo4j is
not configured (avoids confusing CI failures on dev workstations without
Aura access).

Usage::

    py scripts/graphrag_drift_canary.py
    py scripts/graphrag_drift_canary.py --json
    py scripts/graphrag_drift_canary.py --csv-only         # don't touch Neo4j; print canonical CSV row counts
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT, bootstrap_openclaw_process_env

logger = logging.getLogger("akos.graphrag_drift_canary")

DIM = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions"
COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals"

# (CSV path, label/key column, Neo4j node label, friendly name)
DIMENSIONS = [
    (COMPLIANCE / "baseline_organisation.csv", "role_name", "Role", "roles"),
    (COMPLIANCE / "process_list.csv", "item_id", "Process", "processes"),
    (DIM / "PROGRAM_REGISTRY.csv", "program_id", "Program", "programs"),
    (DIM / "TOPIC_REGISTRY.csv", "topic_id", "Topic", "topics"),
    (DIM / "PERSONA_REGISTRY.csv", "persona_id", "Persona", "personas"),
    (DIM / "CHANNEL_TOUCHPOINT_REGISTRY.csv", "channel_id", "Channel", "channels"),
    (DIM / "SOURCING_REGISTER.csv", "vendor_id", "Sourcing", "sourcing"),
    (DIM / "SKILL_REGISTRY.csv", "skill_id", "Skill", "skills"),
    (DIM / "TOUCHPOINT_KIT_CELL_REGISTRY.csv", "cell_id", "TouchpointKitCell", "cells"),
    (DIM / "POLICY_REGISTER.csv", "policy_id", "Policy", "policies"),
]

DRIFT_TOLERANCE = 1  # rows; allows a single in-flight sync gap


def csv_row_count(path: Path) -> int:
    if not path.is_file():
        return 0
    with path.open(encoding="utf-8", newline="") as fh:
        return sum(1 for _ in csv.DictReader(fh))


def neo4j_label_counts() -> dict[str, int] | None:
    """Return label -> count from a single Cypher MATCH. None if Neo4j not configured."""
    from akos.hlk_neo4j import get_neo4j_driver, neo4j_configured

    if not neo4j_configured():
        return None
    drv = get_neo4j_driver()
    if drv is None:
        return None
    try:
        with drv.session() as session:
            rows = session.run(
                "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS c"
            ).data()
        return {r["label"]: int(r["c"]) for r in rows if r.get("label")}
    finally:
        drv.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Neo4j drift canary (I46 P2)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--csv-only",
        action="store_true",
        help="skip Neo4j; print canonical CSV row counts (useful when Neo4j unavailable)",
    )
    parser.add_argument(
        "--tolerance",
        type=int,
        default=DRIFT_TOLERANCE,
        help=f"max row deviation per dimension (default {DRIFT_TOLERANCE})",
    )
    args = parser.parse_args()

    bootstrap_openclaw_process_env()

    csv_counts = {label: csv_row_count(p) for p, _, _, label in [(p, k, l, name) for p, k, l, name in DIMENSIONS]}
    csv_by_friendly = {name: csv_row_count(p) for p, _, _, name in DIMENSIONS}
    csv_by_label = {label: csv_row_count(p) for p, _, label, _ in DIMENSIONS}

    if args.csv_only:
        if args.json:
            print(json.dumps({"status": "csv_only", "csv_counts": csv_by_label}, indent=2, sort_keys=True))
        else:
            print("\n  Neo4j drift canary (CSV-only mode)")
            print("  " + "=" * 50)
            for label, c in sorted(csv_by_label.items()):
                print(f"    {label:24s} {c}")
        return 0

    neo4j_counts = neo4j_label_counts()
    if neo4j_counts is None:
        if args.json:
            print(json.dumps({"status": "skip", "reason": "Neo4j not configured"}, indent=2))
        else:
            print("\n  Neo4j drift canary: SKIP (Neo4j not configured; use --csv-only for CSV count summary)")
        return 0

    drifts: list[dict] = []
    for label, csv_count in csv_by_label.items():
        neo_count = int(neo4j_counts.get(label, 0))
        delta = csv_count - neo_count
        if abs(delta) > args.tolerance:
            drifts.append(
                {
                    "label": label,
                    "csv_count": csv_count,
                    "neo4j_count": neo_count,
                    "delta": delta,
                }
            )

    overall = "fail" if drifts else "pass"
    payload = {
        "status": overall,
        "tolerance": args.tolerance,
        "csv_counts": csv_by_label,
        "neo4j_counts": {k: int(v) for k, v in neo4j_counts.items() if k in csv_by_label},
        "drifts": drifts,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("\n  Neo4j drift canary")
        print("  " + "=" * 60)
        for label, csv_c in sorted(csv_by_label.items()):
            neo_c = int(neo4j_counts.get(label, 0))
            delta = csv_c - neo_c
            marker = " [DRIFT]" if abs(delta) > args.tolerance else ""
            print(f"    {label:24s}  csv={csv_c:6d}  neo4j={neo_c:6d}  delta={delta:+d}{marker}")
        print()
        print(f"  OVERALL: {overall.upper()}")
        if drifts:
            print(f"  Run `py scripts/sync_hlk_neo4j.py` to bring Neo4j into parity.")

    return 1 if overall == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
