#!/usr/bin/env python3
"""Validate GOI_POI_REGISTER.csv against org, process_list, and ref-id discipline.

Usage: py scripts/validate_goipoi_register.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_goipoi_csv import GOIPOI_REGISTER_FIELDNAMES
from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
GOIPOI_CSV = HLK_COMPLIANCE / "GOI_POI_REGISTER.csv"
ORG_CSV = HLK_COMPLIANCE / "baseline_organisation.csv"
PROC_CSV = HLK_COMPLIANCE / "process_list.csv"

ENTITY_KINDS = {"person", "organisation"}
# `class` enum — Initiative 22 P4 (D-IH-5) extended set so the dimension supports
# multi-program reuse across MKTOPS / FINOPS / ADVOPS / public-affairs touchpoints.
# Backwards-compatible: existing rows (Initiative 21) only use the first nine entries.
CLASSES = {
    # Original Initiative 21 set (founder-incorporation seed scope)
    "external_adviser",
    "banking_channel",
    "supplier",
    "research_benchmark",
    "lead",
    "client_org",
    "collaborator",
    "public_authority",
    "other",
    # Initiative 22 P4 extension — multi-program / multi-plane reuse
    "client",          # active client of Holistika (engagement-keyed via program_id)
    "partner",         # strategic partner / channel partner / SI partner
    "investor",        # angel, VC, public-funding agency operating as investor (private flow)
    "regulator",       # public regulator authority (typically is_public_entity=true)
    "vendor",          # paid commercial supplier (FINOPS counterparty); cross-references FINOPS_COUNTERPARTY_REGISTER.csv
    "media",           # press, podcast host, public-relations contact
}
SENSITIVITY = {"public", "internal", "confidential", "restricted"}
BOOLS = {"true", "false"}

REF_ID_RE = re.compile(r"^(POI|GOI)-[A-Z0-9]{2,5}-[A-Z0-9-]{1,40}-\d{4}$")
PROGRAM_ID_RE = re.compile(r"^(PRJ-[A-Z0-9]+-[A-Z0-9]+-\d{4})?$")
LENS_RE = re.compile(r"^[a-z][a-z0-9_]{1,40}$")


def load_org_roles() -> set[str]:
    with open(ORG_CSV, encoding="utf-8", newline="") as f:
        return {r["role_name"].strip() for r in csv.DictReader(f) if r.get("role_name")}


def load_process_ids() -> set[str]:
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        return {r["item_id"].strip() for r in csv.DictReader(f) if r.get("item_id")}


def main() -> int:
    print("\n  GOI_POI_REGISTER Validator")
    print("  " + "=" * 40)
    if not GOIPOI_CSV.is_file():
        print("  FAIL: GOI_POI_REGISTER.csv not found")
        return 1

    org_roles = load_org_roles()
    proc_ids = load_process_ids()

    errors: list[str] = []
    with open(GOIPOI_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(GOIPOI_REGISTER_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(GOIPOI_REGISTER_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    for i, r in enumerate(rows, start=2):
        ref = (r.get("ref_id") or "").strip()
        if not ref:
            errors.append(f"row {i}: empty ref_id")
            continue
        if ref in seen:
            errors.append(f"row {i}: duplicate ref_id {ref}")
        seen.add(ref)
        if not REF_ID_RE.match(ref):
            errors.append(f"row {i}: ref_id must match POI/GOI-<class>-<slug>-<YYYY>: {ref!r}")

        kind = (r.get("entity_kind") or "").strip()
        if kind not in ENTITY_KINDS:
            errors.append(f"row {i}: invalid entity_kind {kind!r}")
        if ref.startswith("POI-") and kind != "person":
            errors.append(f"row {i}: ref_id {ref} starts with POI- but entity_kind={kind!r}")
        if ref.startswith("GOI-") and kind != "organisation":
            errors.append(f"row {i}: ref_id {ref} starts with GOI- but entity_kind={kind!r}")

        cls = (r.get("class") or "").strip()
        if cls not in CLASSES:
            errors.append(f"row {i}: invalid class {cls!r}")

        public = (r.get("is_public_entity") or "").strip().lower()
        if public not in BOOLS:
            errors.append(f"row {i}: is_public_entity must be 'true' or 'false', got {public!r}")

        display = (r.get("display_name") or "").strip()
        if not display:
            errors.append(f"row {i}: display_name required")
        if "@" in display or "@" in (r.get("notes") or ""):
            errors.append(f"row {i}: '@' in display_name or notes (potential email leak)")

        lens = (r.get("lens") or "").strip()
        if lens and not LENS_RE.match(lens):
            errors.append(f"row {i}: lens must be lowercase_snake (1-40 chars): {lens!r}")

        sens = (r.get("sensitivity") or "").strip()
        if sens not in SENSITIVITY:
            errors.append(f"row {i}: invalid sensitivity {sens!r}")

        prog = (r.get("program_id") or "").strip()
        if prog and not PROGRAM_ID_RE.match(prog):
            errors.append(f"row {i}: program_id must match PRJ-<E>-<TOPIC>-<YYYY> or empty: {prog!r}")

        role = (r.get("role_owner") or "").strip()
        if role and role not in org_roles:
            errors.append(f"row {i}: role_owner {role!r} not in baseline_organisation")

        pid = (r.get("process_item_id") or "").strip()
        if pid and pid not in proc_ids:
            errors.append(f"row {i}: process_item_id {pid!r} not in process_list")

        link = (r.get("primary_link") or "").strip()
        if link and ".." in link:
            errors.append(f"row {i}: primary_link must not contain '..': {link!r}")

        if public == "false" and sens == "public":
            errors.append(f"row {i}: is_public_entity=false but sensitivity=public (inconsistent)")

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
