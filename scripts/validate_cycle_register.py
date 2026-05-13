#!/usr/bin/env python3
"""Initiative 59 P1.4 - Validator for CYCLE_REGISTER.csv.

Schema enforcement:
- Required header matches CYCLE_REGISTER_FIELDNAMES.
- cycle_id matches ^CYC-\\d{1,3}$ ; unique.
- coordinating_initiative_id FK to INITIATIVE_REGISTRY.csv.
- coordinated_initiative_ids FK to INITIATIVE_REGISTRY.csv (semicolon list; nullable).
- status in VALID_CYCLE_STATUSES.
- closed_at YYYY-MM-DD when status=closed.
- linked_topic_ids FK to TOPIC_REGISTRY.csv (semicolon list; nullable).

Usage::

    py scripts/validate_cycle_register.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_cycle_register_csv import (
    CYCLE_REGISTER_FIELDNAMES,
    VALID_CYCLE_STATUSES,
)
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "CYCLE_REGISTER.csv"
INITIATIVE_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "INITIATIVE_REGISTRY.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOPIC_REGISTRY.csv"

CYCLE_ID_RE = re.compile(r"^CYC-\d{1,3}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def _parse_int(s: str) -> int | None:
    try:
        return int(s)
    except (TypeError, ValueError):
        return None


def main() -> int:
    print("\n  CYCLE_REGISTER Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: CYCLE_REGISTER.csv not present")
        return 0

    initiatives = _load_csv_set(INITIATIVE_CSV, "initiative_id")
    topic_ids = _load_csv_set(TOPIC_CSV, "topic_id")

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(CYCLE_REGISTER_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(CYCLE_REGISTER_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    by_status: dict[str, int] = {}
    for i, r in enumerate(rows, start=2):
        cid = (r.get("cycle_id") or "").strip()
        if not cid:
            errors.append(f"row {i}: cycle_id empty")
            continue
        if not CYCLE_ID_RE.match(cid):
            errors.append(f"row {i}: cycle_id {cid!r} does not match {CYCLE_ID_RE.pattern}")
        if cid in seen:
            errors.append(f"row {i}: cycle_id {cid!r} duplicated")
        seen.add(cid)

        ci = (r.get("coordinating_initiative_id") or "").strip()
        if not ci:
            errors.append(f"{cid}: coordinating_initiative_id empty")
        elif initiatives and ci not in initiatives:
            errors.append(f"{cid}: coordinating_initiative_id {ci!r} not in INITIATIVE_REGISTRY.csv")

        for sub in _split_semi(r.get("coordinated_initiative_ids") or ""):
            if initiatives and sub not in initiatives:
                errors.append(f"{cid}: coordinated_initiative_id {sub!r} not in INITIATIVE_REGISTRY.csv")

        st = (r.get("status") or "").strip()
        if st not in VALID_CYCLE_STATUSES:
            errors.append(f"{cid}: status {st!r} not in {sorted(VALID_CYCLE_STATUSES)}")
        else:
            by_status[st] = by_status.get(st, 0) + 1
            if st == "closed":
                ca = (r.get("closed_at") or "").strip()
                if not ca:
                    errors.append(f"{cid}: status=closed requires closed_at")
                elif not DATE_RE.match(ca):
                    errors.append(f"{cid}: closed_at {ca!r} not YYYY-MM-DD")

        sa = (r.get("started_at") or "").strip()
        if sa and not DATE_RE.match(sa):
            errors.append(f"{cid}: started_at {sa!r} not YYYY-MM-DD")

        for fld in ("verification_matrix_count", "operator_approval_gates_count"):
            v = (r.get(fld) or "").strip()
            if v:
                n = _parse_int(v)
                if n is None or n < 0:
                    errors.append(f"{cid}: {fld} {v!r} not a non-negative int")

        for tid in _split_semi(r.get("linked_topic_ids") or ""):
            if topic_ids and tid not in topic_ids:
                errors.append(f"{cid}: linked_topic_id {tid!r} not in TOPIC_REGISTRY.csv")

    print(f"  Rows validated:     {len(rows)}")
    print(f"  Cycles:             {len(seen)}")
    if by_status:
        print("  By status:")
        for st in sorted(by_status):
            print(f"    {st:14s} {by_status[st]}")

    if errors:
        print(f"  FAIL: {len(errors)} errors")
        for e in errors[:10]:
            print(f"    - {e}")
        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more")
        return 1

    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
