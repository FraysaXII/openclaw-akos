#!/usr/bin/env python3
"""Initiative 59 P1.3 - Validator for OPS_REGISTER.csv.

Schema enforcement:
- Required header matches OPS_REGISTER_FIELDNAMES.
- ops_action_id matches ^OPS-\\d{1,3}-\\d+(\\.[a-z0-9]+)?$ ; unique.
- originating_initiative_id FK to INITIATIVE_REGISTRY.csv.
- forwarded_to_initiative_id FK to INITIATIVE_REGISTRY.csv (nullable).
- owner_class in VALID_OPS_OWNER_CLASSES.
- owner_role FK to baseline_organisation.csv.
- status in VALID_OPS_STATUSES.
- rice_impact in VALID_RICE_IMPACTS.
- closed_at YYYY-MM-DD when status=closed.
- linked_decision_ids FK to DECISION_REGISTER (semicolon list; nullable).

Usage::

    py scripts/validate_ops_register.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_ops_register_csv import (
    OPS_REGISTER_FIELDNAMES,
    VALID_OPS_OWNER_CLASSES,
    VALID_OPS_STATUSES,
    VALID_RICE_IMPACTS,
)
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "OPS_REGISTER.csv"
INITIATIVE_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "INITIATIVE_REGISTRY.csv"
DECISION_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "DECISION_REGISTER.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "baseline_organisation.csv"

OPS_ACTION_ID_RE = re.compile(r"^OPS-\d{1,3}-\d+(\.[a-z0-9]+)?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def main() -> int:
    print("\n  OPS_REGISTER Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: OPS_REGISTER.csv not present")
        return 0

    initiatives = _load_csv_set(INITIATIVE_CSV, "initiative_id")
    decisions = _load_csv_set(DECISION_CSV, "decision_id")
    org_roles = _load_csv_set(ORG_CSV, "role_name")

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(OPS_REGISTER_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(OPS_REGISTER_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    by_status: dict[str, int] = {}
    by_owner_class: dict[str, int] = {}
    for i, r in enumerate(rows, start=2):
        oid = (r.get("ops_action_id") or "").strip()
        if not oid:
            errors.append(f"row {i}: ops_action_id empty")
            continue
        if not OPS_ACTION_ID_RE.match(oid):
            errors.append(f"row {i}: ops_action_id {oid!r} does not match {OPS_ACTION_ID_RE.pattern}")
        if oid in seen:
            errors.append(f"row {i}: ops_action_id {oid!r} duplicated")
        seen.add(oid)

        oi = (r.get("originating_initiative_id") or "").strip()
        if not oi:
            errors.append(f"{oid}: originating_initiative_id empty")
        elif initiatives and oi not in initiatives:
            errors.append(f"{oid}: originating_initiative_id {oi!r} not in INITIATIVE_REGISTRY.csv")

        fi = (r.get("forwarded_to_initiative_id") or "").strip()
        if fi and initiatives and fi not in initiatives:
            errors.append(f"{oid}: forwarded_to_initiative_id {fi!r} not in INITIATIVE_REGISTRY.csv")

        oc = (r.get("owner_class") or "").strip()
        if oc not in VALID_OPS_OWNER_CLASSES:
            errors.append(f"{oid}: owner_class {oc!r} not in {sorted(VALID_OPS_OWNER_CLASSES)}")
        else:
            by_owner_class[oc] = by_owner_class.get(oc, 0) + 1

        owner = (r.get("owner_role") or "").strip()
        if not owner:
            errors.append(f"{oid}: owner_role empty")
        elif org_roles and owner not in org_roles:
            errors.append(f"{oid}: owner_role {owner!r} not in baseline_organisation.csv")

        st = (r.get("status") or "").strip()
        if st not in VALID_OPS_STATUSES:
            errors.append(f"{oid}: status {st!r} not in {sorted(VALID_OPS_STATUSES)}")
        else:
            by_status[st] = by_status.get(st, 0) + 1
            if st == "closed":
                ca = (r.get("closed_at") or "").strip()
                if not ca:
                    errors.append(f"{oid}: status=closed requires closed_at")
                elif not DATE_RE.match(ca):
                    errors.append(f"{oid}: closed_at {ca!r} not YYYY-MM-DD")

        ri = (r.get("rice_impact") or "").strip()
        if ri and ri not in VALID_RICE_IMPACTS:
            errors.append(f"{oid}: rice_impact {ri!r} not in {sorted(VALID_RICE_IMPACTS)}")

        opened = (r.get("opened_at") or "").strip()
        if opened and not DATE_RE.match(opened):
            errors.append(f"{oid}: opened_at {opened!r} not YYYY-MM-DD")

        for did in _split_semi(r.get("linked_decision_ids") or ""):
            if decisions and did not in decisions:
                errors.append(f"{oid}: linked_decision_id {did!r} not in DECISION_REGISTER.csv")

    print(f"  Rows validated:     {len(rows)}")
    print(f"  OPS items:          {len(seen)}")
    if by_status:
        print("  By status:")
        for st in sorted(by_status):
            print(f"    {st:14s} {by_status[st]}")
    if by_owner_class:
        print("  By owner_class:")
        for oc in sorted(by_owner_class):
            print(f"    {oc:14s} {by_owner_class[oc]}")

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
