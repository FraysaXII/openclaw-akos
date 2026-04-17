#!/usr/bin/env python3
"""Merge a canonical-format process_list candidate CSV into process_list.csv.

Candidate rows must use the same columns as PROCESS_LIST_FIELDNAMES in akos.hlk_process_csv.
Default is dry-run. Requires operator approval before --write (HLK governance).

Example:

    py scripts/merge_process_list_tranche.py \\
      --candidate docs/wip/planning/14-holistika-internal-gtm-mops/candidates/process_list_tranche_holistika_internal.csv

    py scripts/merge_process_list_tranche.py --candidate ... --write
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_process_csv import (  # noqa: E402
    PROCESS_LIST_FIELDNAMES,
    normalize_process_row,
    resolve_all_parent_ids,
    write_process_csv,
)

PROC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "process_list.csv"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidate",
        type=Path,
        required=True,
        help="Path to candidate CSV (same columns as process_list.csv)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Overwrite process_list.csv (operator approval required)",
    )
    args = parser.parse_args()
    cand_path = args.candidate
    if not cand_path.is_absolute():
        cand_path = REPO_ROOT / cand_path
    if not cand_path.is_file():
        print("error: candidate file not found:", cand_path, file=sys.stderr)
        return 1

    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        existing = list(csv.DictReader(f))
    header = existing[0].keys() if existing else []
    if list(header) != PROCESS_LIST_FIELDNAMES:
        print("error: process_list.csv header drift vs PROCESS_LIST_FIELDNAMES", file=sys.stderr)
        return 1

    existing_ids = {r["item_id"].strip() for r in existing if r.get("item_id")}
    existing_names = {r["item_name"].strip() for r in existing if r.get("item_name")}

    with open(cand_path, encoding="utf-8", newline="") as f:
        candidates = list(csv.DictReader(f))
    if not candidates:
        print("candidates=0 nothing to merge")
        return 0

    c0 = candidates[0]
    if set(c0.keys()) != set(PROCESS_LIST_FIELDNAMES):
        missing = set(PROCESS_LIST_FIELDNAMES) - set(c0.keys())
        extra = set(c0.keys()) - set(PROCESS_LIST_FIELDNAMES)
        print("error: candidate columns must match PROCESS_LIST_FIELDNAMES", file=sys.stderr)
        if missing:
            print("  missing:", sorted(missing), file=sys.stderr)
        if extra:
            print("  extra:", sorted(extra), file=sys.stderr)
        return 1

    new_rows: list[dict[str, str]] = []
    for r in candidates:
        iid = (r.get("item_id") or "").strip()
        name = (r.get("item_name") or "").strip()
        if not iid or not name:
            print("error: row missing item_id or item_name", r, file=sys.stderr)
            return 1
        if iid in existing_ids:
            print("error: item_id already in process_list:", iid, file=sys.stderr)
            return 1
        if name in existing_names:
            print("error: item_name collision with existing row:", name, file=sys.stderr)
            return 1
        new_rows.append({k: (r.get(k) or "").strip() for k in PROCESS_LIST_FIELDNAMES})
        existing_ids.add(iid)
        existing_names.add(name)

    print(
        f"candidate_file={cand_path.name} new_rows={len(new_rows)} "
        f"total_after_merge={len(existing) + len(new_rows)}"
    )
    if not args.write:
        print("Dry run: pass --write to apply (operator approval required).")
        return 0

    combined = existing + new_rows
    fixed = resolve_all_parent_ids([normalize_process_row(r) for r in combined])
    write_process_csv(PROC_CSV, fixed)
    print("Wrote", PROC_CSV)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
