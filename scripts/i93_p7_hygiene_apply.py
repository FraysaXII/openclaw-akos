#!/usr/bin/env python3
"""Apply I93 P7 hygiene rules to COMPONENT_SERVICE_MATRIX.csv (D-IH-93-E).

Deterministic rule pass — safe to re-run. Does not touch other P7 CSVs.

Usage::

    py scripts/i93_p7_hygiene_apply.py --dry-run
    py scripts/i93_p7_hygiene_apply.py --apply
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MATRIX_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv"
)

POL_GIT = "POL-DATA-GIT-CSV-DEFAULT"
POL_MIRROR = "POL-DATA-MIRROR-OPERATIONAL"
POL_ENGAGEMENT = "POL-DATA-ENGAGEMENT-FACT"
POL_TELEMETRY = "POL-DATA-TELEMETRY-OBS"


def _classify(row: dict[str, str]) -> tuple[str, str, str]:
    """Return (data_classification, retention_policy_ref, legal_hold)."""
    name = (row.get("component_name") or "").lower()
    notes = (row.get("notes") or "").lower()
    api = (row.get("api_exposure") or "").strip()
    doc = (row.get("doc_link") or "").lower()
    steward = (row.get("steward_ops_domain") or "").strip()

    blob = f"{name} {notes} {doc}"

    if api == "public":
        return "public", POL_GIT, "n"

    if any(k in blob for k in ("enisa", "legal_hold", "restricted")):
        return "restricted", POL_ENGAGEMENT, "y"

    if any(
        k in blob
        for k in (
            "suez",
            "engagement",
            "stripe",
            "finops",
            "goi",
            "collaborator",
            "share_registry",
            "hol_eng",
        )
    ):
        return "confidential", POL_ENGAGEMENT, "n"

    if steward == "DATAOPS" or "mirror" in blob or "compliance." in blob:
        return "internal", POL_MIRROR, "n"

    if any(k in blob for k in ("langfuse", "sentry", "telemetry", "observability", "madeira")):
        return "internal", POL_TELEMETRY, "n"

    if api == "partner":
        return "confidential", POL_ENGAGEMENT, "n"

    return "internal", POL_GIT, "n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write matrix CSV")
    parser.add_argument("--dry-run", action="store_true", help="Print summary only")
    args = parser.parse_args()

    if not MATRIX_CSV.is_file():
        print(f"FAIL: missing {MATRIX_CSV}", file=sys.stderr)
        return 1

    with MATRIX_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    counts: dict[str, int] = {}
    for row in rows:
        dc, ret, lh = _classify(row)
        row["data_classification"] = dc
        row["retention_policy_ref"] = ret
        row["legal_hold"] = lh
        counts[dc] = counts.get(dc, 0) + 1

    print(f"rows={len(rows)} classification={counts}")
    if args.dry_run or not args.apply:
        if not args.dry_run:
            print("INFO: pass --apply to write")
        return 0

    with MATRIX_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {MATRIX_CSV}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
