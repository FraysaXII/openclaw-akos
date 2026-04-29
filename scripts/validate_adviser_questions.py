#!/usr/bin/env python3
"""Validate ADVISER_OPEN_QUESTIONS.csv (Initiative 21 / P4).

Cross-checks against ADVISER_ENGAGEMENT_DISCIPLINES.csv, GOI_POI_REGISTER.csv,
baseline_organisation.csv, and process_list.csv. Enforces id schemes and
discipline-code prefix consistency.

Usage: py scripts/validate_adviser_questions.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_adviser_questions_csv import ADVISER_OPEN_QUESTIONS_FIELDNAMES
from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
QUESTIONS_CSV = HLK_COMPLIANCE / "ADVISER_OPEN_QUESTIONS.csv"
DISCIPLINES_CSV = HLK_COMPLIANCE / "ADVISER_ENGAGEMENT_DISCIPLINES.csv"
GOIPOI_CSV = HLK_COMPLIANCE / "GOI_POI_REGISTER.csv"
ORG_CSV = HLK_COMPLIANCE / "baseline_organisation.csv"

QUESTION_ID_RE = re.compile(r"^Q-([A-Z]{3})-(\d{3})$")
PROGRAM_ID_RE = re.compile(r"^(PRJ-[A-Z0-9]+-[A-Z0-9]+-\d{4})?$")
TARGET_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|tbd|asap|before_signing)$", re.IGNORECASE)
STATUS_SET = {"open", "answered", "deferred", "closed"}


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
    print("\n  ADVISER_OPEN_QUESTIONS Validator")
    print("  " + "=" * 40)
    if not QUESTIONS_CSV.is_file():
        print("  FAIL: ADVISER_OPEN_QUESTIONS.csv not found")
        return 1

    disc_by_id = load_disciplines()
    refs = load_goipoi_refs()
    org_roles = load_org_roles()

    errors: list[str] = []
    with open(QUESTIONS_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(ADVISER_OPEN_QUESTIONS_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(ADVISER_OPEN_QUESTIONS_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    for i, r in enumerate(rows, start=2):
        qid = (r.get("question_id") or "").strip()
        if not qid:
            errors.append(f"row {i}: empty question_id")
            continue
        if qid in seen:
            errors.append(f"row {i}: duplicate question_id {qid}")
        seen.add(qid)
        m = QUESTION_ID_RE.match(qid)
        if not m:
            errors.append(f"row {i}: question_id must match Q-<DISC3>-<NNN>: {qid!r}")

        did = (r.get("discipline_id") or "").strip()
        if did not in disc_by_id:
            errors.append(f"row {i}: discipline_id {did!r} not in ADVISER_ENGAGEMENT_DISCIPLINES")
        elif m and disc_by_id[did] != m.group(1):
            errors.append(
                f"row {i}: question_id prefix {m.group(1)!r} does not match discipline_code {disc_by_id[did]!r} for {did}"
            )

        prog = (r.get("program_id") or "").strip()
        if prog and not PROGRAM_ID_RE.match(prog):
            errors.append(f"row {i}: program_id must match PRJ-<E>-<TOPIC>-<YYYY>: {prog!r}")

        text = (r.get("question_or_action") or "").strip()
        if not text:
            errors.append(f"row {i}: question_or_action required")
        if "@" in text:
            errors.append(f"row {i}: '@' in question_or_action (potential email leak)")

        role = (r.get("owner_role") or "").strip()
        if role and role not in org_roles:
            primary = role.split(";")[0].split("/")[0].strip()
            if primary not in org_roles:
                errors.append(f"row {i}: owner_role {role!r} not resolvable in baseline_organisation")

        td = (r.get("target_date") or "").strip()
        if td and not TARGET_DATE_RE.match(td):
            errors.append(f"row {i}: target_date must be YYYY-MM-DD or one of tbd|asap|before_signing: {td!r}")

        st = (r.get("status") or "").strip()
        if st not in STATUS_SET:
            errors.append(f"row {i}: status must be one of {sorted(STATUS_SET)}: {st!r}")

        poi = (r.get("poi_ref_id") or "").strip()
        if poi:
            if not poi.startswith("POI-"):
                errors.append(f"row {i}: poi_ref_id must start with POI-: {poi!r}")
            elif refs and poi not in refs:
                errors.append(f"row {i}: poi_ref_id {poi!r} not in GOI_POI_REGISTER")

        goi = (r.get("goi_ref_id") or "").strip()
        if goi:
            if not goi.startswith("GOI-"):
                errors.append(f"row {i}: goi_ref_id must start with GOI-: {goi!r}")
            elif refs and goi not in refs:
                errors.append(f"row {i}: goi_ref_id {goi!r} not in GOI_POI_REGISTER")

        ev = (r.get("evidence_pointer") or "").strip()
        if ev and ".." in ev:
            errors.append(f"row {i}: evidence_pointer must not contain '..': {ev!r}")

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
