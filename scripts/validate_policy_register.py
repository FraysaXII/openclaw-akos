#!/usr/bin/env python3
"""Initiative 32 P4 — Validator for POLICY_REGISTER.csv.

Schema enforcement:
- Required header matches ``POLICY_REGISTER_FIELDNAMES``.
- ``policy_id`` matches ``^POL-[A-Z0-9-]{4,80}$``; unique.
- ``policy_class`` is in ``VALID_POLICY_CLASSES``.
- ``cadence`` is in ``VALID_CADENCES``.
- ``owner_role`` resolves against ``baseline_organisation.csv``.
- ``last_review`` and ``next_review`` are YYYY-MM-DD; next_review >= last_review.
- ``policy_text`` non-empty.
- ``topic_ids`` (semicolon list) — each id resolves to ``TOPIC_REGISTRY.csv``.

Usage::

    py scripts/validate_policy_register.py
"""

from __future__ import annotations

import csv
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_policy_register_csv import (
    POLICY_REGISTER_FIELDNAMES,
    VALID_CADENCES,
    VALID_POLICY_CLASSES,
)
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "POLICY_REGISTER.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "baseline_organisation.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOPIC_REGISTRY.csv"

POLICY_ID_RE = re.compile(r"^POL-[A-Z0-9-]{4,80}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def _parse_date(s: str) -> date | None:
    try:
        y, m, d = s.split("-")
        return date(int(y), int(m), int(d))
    except Exception:
        return None


def main() -> int:
    print("\n  POLICY_REGISTER Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: POLICY_REGISTER.csv not present")
        return 0

    org_roles = _load_csv_set(ORG_CSV, "role_name")
    topic_ids = _load_csv_set(TOPIC_CSV, "topic_id")

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(POLICY_REGISTER_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(POLICY_REGISTER_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    by_class: dict[str, int] = {}
    for i, r in enumerate(rows, start=2):
        pid = (r.get("policy_id") or "").strip()
        if not pid:
            errors.append(f"row {i}: policy_id empty")
            continue
        if not POLICY_ID_RE.match(pid):
            errors.append(f"row {i}: policy_id {pid!r} does not match {POLICY_ID_RE.pattern}")
        if pid in seen:
            errors.append(f"row {i}: policy_id {pid!r} duplicated")
        seen.add(pid)

        # policy_class enum
        pc = (r.get("policy_class") or "").strip()
        if pc not in VALID_POLICY_CLASSES:
            errors.append(f"{pid}: policy_class {pc!r} not in {sorted(VALID_POLICY_CLASSES)}")
        else:
            by_class[pc] = by_class.get(pc, 0) + 1

        # applies_to_schema / applies_to_table non-empty (`*` is valid)
        if not (r.get("applies_to_schema") or "").strip():
            errors.append(f"{pid}: applies_to_schema empty")
        if not (r.get("applies_to_table") or "").strip():
            errors.append(f"{pid}: applies_to_table empty")

        # cadence enum
        cad = (r.get("cadence") or "").strip()
        if cad not in VALID_CADENCES:
            errors.append(f"{pid}: cadence {cad!r} not in {sorted(VALID_CADENCES)}")

        # owner_role FK
        owner = (r.get("owner_role") or "").strip()
        if not owner:
            errors.append(f"{pid}: owner_role empty")
        elif org_roles and owner not in org_roles:
            errors.append(f"{pid}: owner_role {owner!r} not in baseline_organisation.csv")

        # last_review / next_review dates
        lr = (r.get("last_review") or "").strip()
        nr = (r.get("next_review") or "").strip()
        if not DATE_RE.match(lr):
            errors.append(f"{pid}: last_review {lr!r} not YYYY-MM-DD")
        if not DATE_RE.match(nr):
            errors.append(f"{pid}: next_review {nr!r} not YYYY-MM-DD")
        else:
            lrd = _parse_date(lr)
            nrd = _parse_date(nr)
            if lrd and nrd and nrd < lrd:
                errors.append(
                    f"{pid}: next_review {nr} < last_review {lr} (review cadence violation)"
                )

        # policy_text non-empty
        if not (r.get("policy_text") or "").strip():
            errors.append(f"{pid}: policy_text empty")

        # topic_ids FK
        for tid in _split_semi(r.get("topic_ids") or ""):
            if topic_ids and tid not in topic_ids:
                errors.append(f"{pid}: topic_id {tid!r} not in TOPIC_REGISTRY.csv")

    print(f"  Rows validated:     {len(rows)}")
    print(f"  Policies:           {len(seen)}")
    if by_class:
        print("  By class:")
        for cls in sorted(by_class):
            print(f"    {cls:24s} {by_class[cls]}")

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
