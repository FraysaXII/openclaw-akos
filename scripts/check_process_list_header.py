#!/usr/bin/env python3
"""Verify process_list.csv header matches PROCESS_LIST_FIELDNAMES (fork / drift guard).

Use after merging an older branch or importing a CSV from another system: writers that
hard-coded 19 columns will corrupt rows if the canonical file has grown.

Usage (repo root):
    py scripts/check_process_list_header.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "process_list.csv"

sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_process_csv import PROCESS_LIST_FIELDNAMES  # noqa: E402


def main() -> int:
    if not PROC_CSV.is_file():
        print("error: process_list.csv not found", PROC_CSV, file=sys.stderr)
        return 1
    with PROC_CSV.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        got = list(reader.fieldnames or [])
    if got == PROCESS_LIST_FIELDNAMES:
        print("process_list.csv header: OK", f"({len(got)} columns)")
        return 0
    print("error: header mismatch (fork or manual edit risk)", file=sys.stderr)
    print("  expected:", PROCESS_LIST_FIELDNAMES, file=sys.stderr)
    print("  got:     ", got, file=sys.stderr)
    print("  hint: merge latest main or align header to akos.hlk_process_csv.PROCESS_LIST_FIELDNAMES", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
