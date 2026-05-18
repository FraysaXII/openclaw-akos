#!/usr/bin/env python3
"""Initiative 59 P1.2 - Validator for INITIATIVE_REGISTRY.csv.

Schema enforcement:
- Required header matches INITIATIVE_REGISTRY_FIELDNAMES.
- initiative_id matches ^INIT-[A-Z0-9_]+-\\d{2,3}$ ; unique.
- repo_slug FK to REPOSITORY_REGISTRY.csv.
- status in VALID_INITIATIVE_STATUSES (akos.planning.status_taxonomy).
- Companion-field rules enforced per REQUIRED_COMPANION_FIELDS:
    * status=closed   -> closed_at non-empty (YYYY-MM-DD).
    * status=archived -> archived_at + superseded_by non-empty.
    * status=continuous   -> continuous_rationale non-empty.
    * status=program_line -> cadence non-empty (in VALID_CADENCES).
    * status=gated_external -> gated_on non-empty.
    * status=gated_operator -> gated_on + operator_action non-empty.
- cycle_id FK to CYCLE_REGISTER.csv (nullable).
- inception_decision_id / closure_decision_id FK to DECISION_REGISTER.csv (nullable).
- superseded_by FK to INITIATIVE_REGISTRY (nullable; required when status=archived).
- linked_topic_ids FK to TOPIC_REGISTRY.csv (semicolon list; nullable).
- program_anchors FK to PROGRAM_REGISTRY.csv (semicolon list; nullable; I86 P2 / D-IH-86-J Stage B).
- inception_date / last_review / closed_at / archived_at YYYY-MM-DD when set.

Usage::

    py scripts/validate_initiative_registry.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_initiative_registry_csv import (
    INITIATIVE_REGISTRY_FIELDNAMES,
    VALID_CADENCES,
)
from akos.io import REPO_ROOT
from akos.planning.status_taxonomy import (
    REQUIRED_COMPANION_FIELDS,
    VALID_INITIATIVE_STATUSES,
)

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "INITIATIVE_REGISTRY.csv"
REPOSITORY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPOSITORY_REGISTRY.csv"
CYCLE_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "CYCLE_REGISTER.csv"
DECISION_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "DECISION_REGISTER.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "baseline_organisation.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOPIC_REGISTRY.csv"
PROCESS_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "process_list.csv"
PROGRAM_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "PROGRAM_REGISTRY.csv"  # I86 P2 / D-IH-86-J Stage B

INITIATIVE_ID_RE = re.compile(r"^INIT-[A-Z0-9_]+-\d{2,3}[A-Z]?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def main() -> int:
    print("\n  INITIATIVE_REGISTRY Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: INITIATIVE_REGISTRY.csv not present")
        return 0

    repos = _load_csv_set(REPOSITORY_CSV, "repo_slug")
    cycles = _load_csv_set(CYCLE_CSV, "cycle_id")
    decisions = _load_csv_set(DECISION_CSV, "decision_id")
    org_roles = _load_csv_set(ORG_CSV, "role_name")
    topic_ids = _load_csv_set(TOPIC_CSV, "topic_id")
    process_ids = _load_csv_set(PROCESS_CSV, "item_id")
    program_ids = _load_csv_set(PROGRAM_CSV, "program_id")

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(INITIATIVE_REGISTRY_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(INITIATIVE_REGISTRY_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    initiative_ids: set[str] = {(r.get("initiative_id") or "").strip() for r in rows if r.get("initiative_id")}
    by_status: dict[str, int] = {}
    for i, r in enumerate(rows, start=2):
        iid = (r.get("initiative_id") or "").strip()
        if not iid:
            errors.append(f"row {i}: initiative_id empty")
            continue
        if not INITIATIVE_ID_RE.match(iid):
            errors.append(f"row {i}: initiative_id {iid!r} does not match {INITIATIVE_ID_RE.pattern}")
        if iid in seen:
            errors.append(f"row {i}: initiative_id {iid!r} duplicated")
        seen.add(iid)

        rs = (r.get("repo_slug") or "").strip()
        if not rs:
            errors.append(f"{iid}: repo_slug empty")
        elif repos and rs not in repos:
            errors.append(f"{iid}: repo_slug {rs!r} not in REPOSITORY_REGISTRY.csv")

        status = (r.get("status") or "").strip()
        if status not in VALID_INITIATIVE_STATUSES:
            errors.append(f"{iid}: status {status!r} not in {sorted(VALID_INITIATIVE_STATUSES)}")
        else:
            by_status[status] = by_status.get(status, 0) + 1
            for fld in REQUIRED_COMPANION_FIELDS.get(status, ()):
                if not (r.get(fld) or "").strip():
                    errors.append(f"{iid}: status={status} requires non-empty {fld!r}")

        cadence = (r.get("cadence") or "").strip()
        if cadence and cadence not in VALID_CADENCES:
            errors.append(f"{iid}: cadence {cadence!r} not in {sorted(c for c in VALID_CADENCES if c)}")

        owner = (r.get("owner_role") or "").strip()
        if not owner:
            errors.append(f"{iid}: owner_role empty")
        elif org_roles and owner not in org_roles:
            errors.append(f"{iid}: owner_role {owner!r} not in baseline_organisation.csv")

        for date_field in ("inception_date", "last_review", "closed_at", "archived_at"):
            v = (r.get(date_field) or "").strip()
            if v and not DATE_RE.match(v):
                errors.append(f"{iid}: {date_field} {v!r} not YYYY-MM-DD")

        cid = (r.get("cycle_id") or "").strip()
        if cid and cycles and cid not in cycles:
            errors.append(f"{iid}: cycle_id {cid!r} not in CYCLE_REGISTER.csv")

        for fld in ("inception_decision_id", "closure_decision_id"):
            did = (r.get(fld) or "").strip()
            if did and decisions and did not in decisions:
                errors.append(f"{iid}: {fld} {did!r} not in DECISION_REGISTER.csv")

        sb = (r.get("superseded_by") or "").strip()
        if sb and sb not in initiative_ids:
            errors.append(f"{iid}: superseded_by {sb!r} not in INITIATIVE_REGISTRY (self)")

        for tid in _split_semi(r.get("linked_topic_ids") or ""):
            if topic_ids and tid not in topic_ids:
                errors.append(f"{iid}: linked_topic_id {tid!r} not in TOPIC_REGISTRY.csv")

        for pid in _split_semi(r.get("manifests_processes") or ""):
            if process_ids and pid not in process_ids:
                errors.append(f"{iid}: manifests_processes {pid!r} not in process_list.csv")

        for anchor in _split_semi(r.get("program_anchors") or ""):
            if program_ids and anchor not in program_ids:
                errors.append(f"{iid}: program_anchors {anchor!r} not in PROGRAM_REGISTRY.csv (I86 P2 / D-IH-86-J)")

    print(f"  Rows validated:     {len(rows)}")
    print(f"  Initiatives:        {len(seen)}")
    if by_status:
        print("  By status:")
        for st in sorted(by_status):
            print(f"    {st:20s} {by_status[st]}")

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
