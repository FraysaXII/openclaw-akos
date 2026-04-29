#!/usr/bin/env python3
"""Validate ADVISER_ENGAGEMENT_DISCIPLINES.csv (Initiative 21 / P3).

Usage: py scripts/validate_adviser_disciplines.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_adviser_disciplines_csv import ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES
from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
DISCIPLINES_CSV = HLK_COMPLIANCE / "ADVISER_ENGAGEMENT_DISCIPLINES.csv"
ORG_CSV = HLK_COMPLIANCE / "baseline_organisation.csv"
PROC_CSV = HLK_COMPLIANCE / "process_list.csv"

DISCIPLINE_ID_RE = re.compile(r"^[a-z][a-z0-9_]{1,30}$")
CODE_RE = re.compile(r"^[A-Z]{3}$")
PROGRAM_ID_RE = re.compile(r"^(PRJ-[A-Z0-9]+-[A-Z0-9]+-\d{4})?$")


def load_org_roles() -> set[str]:
    with open(ORG_CSV, encoding="utf-8", newline="") as f:
        return {r["role_name"].strip() for r in csv.DictReader(f) if r.get("role_name")}


def load_process_ids() -> set[str]:
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        return {r["item_id"].strip() for r in csv.DictReader(f) if r.get("item_id")}


def main() -> int:
    print("\n  ADVISER_ENGAGEMENT_DISCIPLINES Validator")
    print("  " + "=" * 40)
    if not DISCIPLINES_CSV.is_file():
        print("  FAIL: ADVISER_ENGAGEMENT_DISCIPLINES.csv not found")
        return 1

    org_roles = load_org_roles()
    proc_ids = load_process_ids()

    errors: list[str] = []
    with open(DISCIPLINES_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen_id: set[str] = set()
    seen_code: set[str] = set()
    for i, r in enumerate(rows, start=2):
        did = (r.get("discipline_id") or "").strip()
        if not did:
            errors.append(f"row {i}: empty discipline_id")
            continue
        if did in seen_id:
            errors.append(f"row {i}: duplicate discipline_id {did}")
        seen_id.add(did)
        if not DISCIPLINE_ID_RE.match(did):
            errors.append(f"row {i}: discipline_id must be lowercase_snake (1-30): {did!r}")

        code = (r.get("discipline_code") or "").strip()
        if not CODE_RE.match(code):
            errors.append(f"row {i}: discipline_code must be 3 uppercase letters: {code!r}")
        if code in seen_code:
            errors.append(f"row {i}: duplicate discipline_code {code}")
        seen_code.add(code)

        display = (r.get("display_name") or "").strip()
        if not display:
            errors.append(f"row {i}: display_name required")

        role = (r.get("canonical_role") or "").strip()
        if role and role not in org_roles:
            errors.append(f"row {i}: canonical_role {role!r} not in baseline_organisation")

        pid = (r.get("default_process_item_id") or "").strip()
        if pid and pid not in proc_ids:
            errors.append(f"row {i}: default_process_item_id {pid!r} not in process_list")

        prog = (r.get("default_program_id") or "").strip()
        if prog and not PROGRAM_ID_RE.match(prog):
            errors.append(f"row {i}: default_program_id must match PRJ-<E>-<TOPIC>-<YYYY>: {prog!r}")

    if errors:
        print(f"  FAIL: {len(errors)} issue(s)")
        for e in errors[:25]:
            print(f"    - {e}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        return 1

    print(f"  Rows validated: {len(rows)}")
    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
