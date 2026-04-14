#!/usr/bin/env python3
"""Upgrade process_list.csv to include item_parent_*_id columns and backfill values.

Reads the canonical CSV (any prior header shape), normalizes to PROCESS_LIST_FIELDNAMES,
resolves parent names to item_id for every row, and writes the file.

Usage (repo root):
    py scripts/backfill_process_parent_ids.py
    py scripts/backfill_process_parent_ids.py --write
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "process_list.csv"

sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_process_csv import (  # noqa: E402
    PROCESS_LIST_FIELDNAMES,
    ambiguous_item_names,
    item_name_uniqueness_errors,
    normalize_process_row,
    resolve_all_parent_ids,
    write_process_csv,
)


def load_raw_rows() -> list[dict[str, str]]:
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def upgrade(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    normalized = [normalize_process_row(r) for r in rows]
    return resolve_all_parent_ids(normalized)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    raw = load_raw_rows()
    dup_err = item_name_uniqueness_errors(raw)
    if dup_err:
        print("error: duplicate item_name values block parent-id resolution; fix CSV or run:", file=sys.stderr)
        print("  py scripts/dedupe_ambiguous_process_item_names.py --report", file=sys.stderr)
        for e in dup_err[:15]:
            print(f"  - {e}", file=sys.stderr)
        if len(dup_err) > 15:
            print(f"  ... and {len(dup_err) - 15} more", file=sys.stderr)
        return 1
    new_rows = upgrade(raw)
    amb = ambiguous_item_names(new_rows)
    missing = 0
    for r in new_rows:
        gran = (r.get("item_granularity") or "").strip()
        if gran == "project":
            continue
        p1 = (r.get("item_parent_1") or "").strip()
        p2 = (r.get("item_parent_2") or "").strip()
        if p1 and p1 not in amb and not (r.get("item_parent_1_id") or "").strip():
            missing += 1
        if p2 and p2 not in amb and not (r.get("item_parent_2_id") or "").strip():
            missing += 1
    print(
        f"rows={len(new_rows)} ambiguous_item_names={len(amb)} "
        f"parent_id_holes_excluding_ambiguous={missing} columns={len(PROCESS_LIST_FIELDNAMES)}"
    )
    if missing:
        print("error: unresolved parent id(s) for uniquely-named parents", file=sys.stderr)
        return 1
    if not args.write:
        print("Dry run: pass --write to apply.")
        return 0
    write_process_csv(PROC_CSV, new_rows)
    print("Wrote", PROC_CSV)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
