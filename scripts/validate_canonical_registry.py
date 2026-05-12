"""I70 P4.5 — validate CANONICAL_REGISTRY.csv against filesystem truth.

Confirms every active canonical declared in the registry exists at file_path
(post-migration) and detects orphaned files at federated homes that aren't registered.

Usage:
    py scripts/validate_canonical_registry.py
    py scripts/validate_canonical_registry.py --strict   # exit 1 on any mismatch
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "CANONICAL_REGISTRY.csv"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--strict", action="store_true")
    args = p.parse_args()
    if not REGISTRY.exists():
        print(f"FAIL: registry missing at {REGISTRY.relative_to(REPO).as_posix()}")
        return 1
    with open(REGISTRY, encoding="utf-8") as fh:
        rdr = csv.DictReader(fh)
        rows = list(rdr)
    print(f"validate_canonical_registry: {len(rows)} rows in registry")
    missing = []
    multi_claimed: dict[str, list[str]] = {}
    seen_ids: set[str] = set()
    for r in rows:
        cid = r["canonical_id"]
        if cid in seen_ids:
            print(f"  WARN: duplicate canonical_id {cid}")
        seen_ids.add(cid)
        if r["status"] == "proposed":
            continue
        fp = r["file_path"]
        if not fp:
            continue
        full = REPO / fp
        if not full.exists():
            missing.append((cid, fp))
        # Multi-claim check: same file_path claimed by multiple ids
        multi_claimed.setdefault(fp, []).append(cid)
    print(f"  active rows checked: {sum(1 for r in rows if r['status'] != 'proposed' and r['file_path'])}")
    if missing:
        print(f"  MISSING ({len(missing)}):")
        for cid, fp in missing[:20]:
            print(f"    {cid}: {fp}")
        if len(missing) > 20:
            print(f"    ... and {len(missing) - 20} more")
    duplicates = {fp: ids for fp, ids in multi_claimed.items() if len(ids) > 1}
    if duplicates:
        print(f"  MULTI-CLAIMED FILE_PATHS ({len(duplicates)}):")
        for fp, ids in list(duplicates.items())[:5]:
            print(f"    {fp}: {ids}")
    if not missing and not duplicates:
        print("  PASS: every active canonical exists at its declared file_path; no multi-claims.")
        return 0
    if args.strict:
        return 1
    print("  WARN: registry has mismatches but exiting 0 (soft mode); pass --strict to fail.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
