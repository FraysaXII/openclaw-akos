#!/usr/bin/env python3
"""Strip hash-padded duplicate URLs from a research source ledger (machine-only).

Usage:
    py scripts/strip_padded_source_ledger.py --ledger PATH [--write]
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.evidence_class_gate import is_url_hash_padding, normalize_url_for_dedupe  # noqa: E402
from akos.hlk_research_action import SOURCE_LEDGER_FIELDNAMES  # noqa: E402


def strip_ledger(path: Path) -> tuple[list[dict[str, str]], int]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    kept: list[dict[str, str]] = []
    removed = 0
    seen_external_bases: set[str] = set()
    for row in rows:
        url = row.get("url", "")
        fmt = row.get("format", "")
        if fmt == "webpage" and is_url_hash_padding(url):
            removed += 1
            continue
        if fmt == "webpage":
            base = normalize_url_for_dedupe(url)
            if base in seen_external_bases:
                removed += 1
                continue
            seen_external_bases.add(base)
        kept.append(row)
    return kept, removed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    path = Path(args.ledger)
    if not path.is_file():
        print(f"FAIL: not found: {path}")
        return 1
    kept, removed = strip_ledger(path)
    print(f"Kept {len(kept)} rows; removed {removed} padded/duplicate external rows")
    if args.write:
        with path.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(SOURCE_LEDGER_FIELDNAMES))
            w.writeheader()
            w.writerows(kept)
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
