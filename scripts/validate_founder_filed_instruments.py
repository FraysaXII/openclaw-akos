#!/usr/bin/env python3
"""Validate FOUNDER_FILED_INSTRUMENTS.csv (Initiative 21 / P5).

Cross-checks discipline FK, GOI counterparty FK, owner_role FK, supersedes
chain, status enum, and date format.

Usage: py scripts/validate_founder_filed_instruments.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_founder_filed_instruments_csv import FOUNDER_FILED_INSTRUMENTS_FIELDNAMES
from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
INSTRUMENTS_CSV = HLK_COMPLIANCE / "FOUNDER_FILED_INSTRUMENTS.csv"
DISCIPLINES_CSV = HLK_COMPLIANCE / "ADVISER_ENGAGEMENT_DISCIPLINES.csv"
GOIPOI_CSV = HLK_COMPLIANCE / "GOI_POI_REGISTER.csv"
ORG_CSV = HLK_COMPLIANCE / "baseline_organisation.csv"

INSTRUMENT_ID_RE = re.compile(r"^INST-([A-Z]{3})-[A-Z0-9-]{1,40}-\d{4}$")
PROGRAM_ID_RE = re.compile(r"^(PRJ-[A-Z0-9]+-[A-Z0-9]+-\d{4})?$")
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|tbd)$", re.IGNORECASE)
STATUS_SET = {"draft", "signed", "filed", "superseded", "withdrawn"}


def load_disciplines() -> dict[str, str]:
    if not DISCIPLINES_CSV.is_file():
        return {}
    with open(DISCIPLINES_CSV, encoding="utf-8", newline="") as f:
        return {
            (r.get("discipline_id") or "").strip(): (r.get("discipline_code") or "").strip()
            for r in csv.DictReader(f)
            if r.get("discipline_id")
        }


def load_goipoi_refs() -> set[str]:
    if not GOIPOI_CSV.is_file():
        return set()
    with open(GOIPOI_CSV, encoding="utf-8", newline="") as f:
        return {(r.get("ref_id") or "").strip() for r in csv.DictReader(f) if r.get("ref_id")}


def load_org_roles() -> set[str]:
    with open(ORG_CSV, encoding="utf-8", newline="") as f:
        return {r["role_name"].strip() for r in csv.DictReader(f) if r.get("role_name")}


def main() -> int:
    print("\n  FOUNDER_FILED_INSTRUMENTS Validator")
    print("  " + "=" * 40)
    if not INSTRUMENTS_CSV.is_file():
        print("  FAIL: FOUNDER_FILED_INSTRUMENTS.csv not found")
        return 1

    disc_by_id = load_disciplines()
    refs = load_goipoi_refs()
    org_roles = load_org_roles()

    errors: list[str] = []
    with open(INSTRUMENTS_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(FOUNDER_FILED_INSTRUMENTS_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(FOUNDER_FILED_INSTRUMENTS_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    ids: set[str] = {(r.get("instrument_id") or "").strip() for r in rows if r.get("instrument_id")}

    for i, r in enumerate(rows, start=2):
        iid = (r.get("instrument_id") or "").strip()
        if not iid:
            errors.append(f"row {i}: empty instrument_id")
            continue
        if iid in seen:
            errors.append(f"row {i}: duplicate instrument_id {iid}")
        seen.add(iid)
        m = INSTRUMENT_ID_RE.match(iid)
        if not m:
            errors.append(f"row {i}: instrument_id must match INST-<DISC3>-<SLUG>-<YYYY>: {iid!r}")

        did = (r.get("discipline_id") or "").strip()
        if did not in disc_by_id:
            errors.append(f"row {i}: discipline_id {did!r} not in ADVISER_ENGAGEMENT_DISCIPLINES")
        elif m and disc_by_id[did] != m.group(1):
            errors.append(
                f"row {i}: instrument_id prefix {m.group(1)!r} does not match discipline_code {disc_by_id[did]!r} for {did}"
            )

        prog = (r.get("program_id") or "").strip()
        if prog and not PROGRAM_ID_RE.match(prog):
            errors.append(f"row {i}: program_id must match PRJ-<E>-<TOPIC>-<YYYY>: {prog!r}")

        itype = (r.get("instrument_type") or "").strip()
        if not itype:
            errors.append(f"row {i}: instrument_type required")

        st = (r.get("status") or "").strip()
        if st not in STATUS_SET:
            errors.append(f"row {i}: status must be one of {sorted(STATUS_SET)}: {st!r}")

        d = (r.get("effective_or_filing_date") or "").strip()
        if d and not DATE_RE.match(d):
            errors.append(f"row {i}: effective_or_filing_date must be YYYY-MM-DD or 'tbd': {d!r}")

        vlink = (r.get("vault_link") or "").strip()
        if vlink and ".." in vlink:
            errors.append(f"row {i}: vault_link must not contain '..': {vlink!r}")

        role = (r.get("primary_owner_role") or "").strip()
        if role and role not in org_roles:
            errors.append(f"row {i}: primary_owner_role {role!r} not in baseline_organisation")

        cp = (r.get("counterparty_goi_ref_id") or "").strip()
        if cp:
            if not cp.startswith("GOI-"):
                errors.append(f"row {i}: counterparty_goi_ref_id must start with GOI-: {cp!r}")
            elif refs and cp not in refs:
                errors.append(f"row {i}: counterparty_goi_ref_id {cp!r} not in GOI_POI_REGISTER")

        sup = (r.get("supersedes_instrument_id") or "").strip()
        if sup and sup not in ids:
            errors.append(f"row {i}: supersedes_instrument_id {sup!r} not in this register")
        if sup == iid:
            errors.append(f"row {i}: supersedes_instrument_id cannot equal instrument_id (self-loop)")

        if st == "filed" and d == "tbd":
            errors.append(f"row {i}: status=filed requires effective_or_filing_date YYYY-MM-DD (got 'tbd')")

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
