#!/usr/bin/env python3
"""Initiative 59 P1.5 - Validator for DECISION_REGISTER.csv.

Schema enforcement:
- Required header matches DECISION_REGISTER_FIELDNAMES.
- decision_id matches the standard ^D-IH-\\d{1,3}-[A-Z][A-Z0-9]{0,7}(-[A-Z]{1,2})?(-V\\d+)?$ pattern
  (single letter A-Z; double letter AA-ZZ; descriptive alphanumeric W3CNORM-style
  suffix up to 8 chars; multi-segment letter-suffix D-IH-86-RH-A..H; V-suffix versions)
  OR the closure-decision pattern ^D-IH-\\d{1,3}-Decision-P\\d+(-[A-Z0-9-]+)?-\\d{4}-\\d{2}-\\d{2}$.
  Lineage: (a) 2026-05-11 release-gate hygiene pass widened single→double letter for
  I66 D-IH-66-U..AD; (b) Lane D Wave H 2026-05-19 widened to accept multi-segment
  D-IH-86-RH-A..H; (c) Wave H closure commit 2026-05-19 (D-IH-86-W3CNORM) widened
  first segment from [A-Z]{1,2} to [A-Z][A-Z0-9]{0,7} for descriptive workflow-norm IDs.
- initiating_initiative_id FK to INITIATIVE_REGISTRY.csv.
- linked_initiative_ids / linked_ops_action_ids / linked_policies / linked_topic_ids FK
  to their respective registries (semicolon lists; nullable).
- decision_class in VALID_DECISION_CLASSES.
- status in VALID_DECISION_STATUSES.
- reversibility in VALID_REVERSIBILITY.
- decided_at YYYY-MM-DD.
- supersedes_decision_id FK to DECISION_REGISTER (self; nullable).
- decision_log_path resolves to a file relative to the repo root (advisory only;
  warns if missing because some legacy initiatives may not have been audited yet).

Usage::

    py scripts/validate_decision_register.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_decision_register_csv import (
    DECISION_REGISTER_FIELDNAMES,
    VALID_DECISION_CLASSES,
    VALID_DECISION_STATUSES,
    VALID_REVERSIBILITY,
)
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "DECISION_REGISTER.csv"
INITIATIVE_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "INITIATIVE_REGISTRY.csv"
OPS_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "OPS_REGISTER.csv"
POLICY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "POLICY_REGISTER.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOPIC_REGISTRY.csv"

DECISION_ID_STANDARD_RE = re.compile(r"^D-IH-\d{1,3}-[A-Z][A-Z0-9]{0,7}(-[A-Z]{1,2})?(-V\d+)?$")
DECISION_ID_CLOSURE_RE = re.compile(r"^D-IH-\d{1,3}-Decision-P\d+(-[A-Z0-9-]+)?-\d{4}-\d{2}-\d{2}$")
DECISION_ID_INITIATIVE_CLOSURE_RE = re.compile(r"^D-IH-\d{1,3}-CLOSURE(-[A-Z0-9-]+)?$")
DECISION_ID_OPS_RE = re.compile(r"^D-IH-OPS-\d{1,3}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def _decision_id_valid(did: str) -> bool:
    return bool(
        DECISION_ID_STANDARD_RE.match(did)
        or DECISION_ID_CLOSURE_RE.match(did)
        or DECISION_ID_INITIATIVE_CLOSURE_RE.match(did)
        or DECISION_ID_OPS_RE.match(did)
    )


def main() -> int:
    print("\n  DECISION_REGISTER Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: DECISION_REGISTER.csv not present")
        return 0

    initiatives = _load_csv_set(INITIATIVE_CSV, "initiative_id")
    ops_ids = _load_csv_set(OPS_CSV, "ops_action_id")
    policy_ids = _load_csv_set(POLICY_CSV, "policy_id")
    topic_ids = _load_csv_set(TOPIC_CSV, "topic_id")

    errors: list[str] = []
    warnings: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(DECISION_REGISTER_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(DECISION_REGISTER_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    decision_ids: set[str] = {(r.get("decision_id") or "").strip() for r in rows if r.get("decision_id")}
    by_class: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for i, r in enumerate(rows, start=2):
        did = (r.get("decision_id") or "").strip()
        if not did:
            errors.append(f"row {i}: decision_id empty")
            continue
        if not _decision_id_valid(did):
            errors.append(
                f"row {i}: decision_id {did!r} matches neither standard nor closure pattern"
            )
        if did in seen:
            errors.append(f"row {i}: decision_id {did!r} duplicated")
        seen.add(did)

        ii = (r.get("initiating_initiative_id") or "").strip()
        if not ii:
            errors.append(f"{did}: initiating_initiative_id empty")
        elif initiatives and ii not in initiatives:
            errors.append(f"{did}: initiating_initiative_id {ii!r} not in INITIATIVE_REGISTRY.csv")

        for sub in _split_semi(r.get("linked_initiative_ids") or ""):
            if initiatives and sub not in initiatives:
                errors.append(f"{did}: linked_initiative_id {sub!r} not in INITIATIVE_REGISTRY.csv")

        for ops in _split_semi(r.get("linked_ops_action_ids") or ""):
            if ops_ids and ops not in ops_ids:
                errors.append(f"{did}: linked_ops_action_id {ops!r} not in OPS_REGISTER.csv")

        for pol in _split_semi(r.get("linked_policies") or ""):
            if policy_ids and pol not in policy_ids:
                errors.append(f"{did}: linked_policy {pol!r} not in POLICY_REGISTER.csv")

        for tid in _split_semi(r.get("linked_topic_ids") or ""):
            if topic_ids and tid not in topic_ids:
                errors.append(f"{did}: linked_topic_id {tid!r} not in TOPIC_REGISTRY.csv")

        dc = (r.get("decision_class") or "").strip()
        if dc not in VALID_DECISION_CLASSES:
            errors.append(f"{did}: decision_class {dc!r} not in {sorted(VALID_DECISION_CLASSES)}")
        else:
            by_class[dc] = by_class.get(dc, 0) + 1

        st = (r.get("status") or "").strip()
        if st not in VALID_DECISION_STATUSES:
            errors.append(f"{did}: status {st!r} not in {sorted(VALID_DECISION_STATUSES)}")
        else:
            by_status[st] = by_status.get(st, 0) + 1

        rev = (r.get("reversibility") or "").strip()
        if rev not in VALID_REVERSIBILITY:
            errors.append(f"{did}: reversibility {rev!r} not in {sorted(VALID_REVERSIBILITY)}")

        d = (r.get("decided_at") or "").strip()
        if not d:
            errors.append(f"{did}: decided_at empty")
        elif not DATE_RE.match(d):
            errors.append(f"{did}: decided_at {d!r} not YYYY-MM-DD")

        sup = (r.get("supersedes_decision_id") or "").strip()
        if sup and sup not in decision_ids:
            errors.append(f"{did}: supersedes_decision_id {sup!r} not in DECISION_REGISTER (self)")

        log_path = (r.get("decision_log_path") or "").strip()
        if log_path:
            full = REPO_ROOT / log_path
            if not full.is_file():
                warnings.append(f"{did}: decision_log_path {log_path!r} does not resolve to a file")

    print(f"  Rows validated:     {len(rows)}")
    print(f"  Decisions:          {len(seen)}")
    if by_class:
        print("  By class:")
        for cls in sorted(by_class):
            print(f"    {cls:18s} {by_class[cls]}")
    if by_status:
        print("  By status:")
        for st in sorted(by_status):
            print(f"    {st:14s} {by_status[st]}")
    if warnings:
        print(f"  Warnings: {len(warnings)} (advisory; not failing)")
        for w in warnings[:5]:
            print(f"    - {w}")
        if len(warnings) > 5:
            print(f"    ... and {len(warnings) - 5} more")

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
