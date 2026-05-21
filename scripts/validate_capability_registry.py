#!/usr/bin/env python3
"""Validate CAPABILITY_REGISTRY.csv (Initiative 82 P2 / I86 Wave Q).

Usage::

    py scripts/validate_capability_registry.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_capability_registry_csv import (  # noqa: E402
    CAPABILITY_REGISTRY_FIELDNAMES,
    CapabilityRegistryRow,
)
from pydantic import ValidationError  # noqa: E402

CSV_PATH = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "dimensions/CAPABILITY_REGISTRY.csv"
)
ORG_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "baseline_organisation.csv"
)
PROCESS_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "process_list.csv"
)
SUBSTRATE_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "dimensions/SUBSTRATE_REGISTRY.csv"
)
DECISION_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "DECISION_REGISTER.csv"
)


def _load_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(r.get(key) or "").strip() for r in csv.DictReader(fh) if (r.get(key) or "").strip()}


def main() -> int:
    errors: list[str] = []
    if not CSV_PATH.is_file():
        print(f"FAIL: missing {CSV_PATH.relative_to(REPO_ROOT)}")
        return 1
    roles = _load_set(ORG_CSV, "role_name")
    processes = _load_set(PROCESS_CSV, "item_id")
    substrates = _load_set(SUBSTRATE_CSV, "substrate_id")
    decisions = _load_set(DECISION_CSV, "decision_id")

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != CAPABILITY_REGISTRY_FIELDNAMES:
            errors.append("Header mismatch vs CAPABILITY_REGISTRY_FIELDNAMES")
            print("FAIL")
            for e in errors:
                print(f"  - {e}")
            return 1
        seen: set[str] = set()
        for line_no, row in enumerate(reader, start=2):
            cid = row.get("capability_id", "")
            if cid in seen:
                errors.append(f"L{line_no}: duplicate capability_id {cid!r}")
            seen.add(cid)
            try:
                CapabilityRegistryRow.model_validate(row)
            except ValidationError as exc:
                errors.append(f"L{line_no}: Pydantic {exc.errors()[0]['msg']}")
                continue
            owner = (row.get("role_owner") or "").strip()
            if owner and owner not in roles:
                errors.append(f"L{line_no}: role_owner {owner!r} not in baseline_organisation")
            for pid in (row.get("originating_process_ids") or "").split(";"):
                pid = pid.strip()
                if pid and pid not in processes:
                    errors.append(f"L{line_no}: originating_process_ids {pid!r} not in process_list")
            sid = (row.get("substrate_id") or "").strip()
            if sid and sid not in substrates:
                errors.append(f"L{line_no}: substrate_id {sid!r} not in SUBSTRATE_REGISTRY")
            did = (row.get("last_review_decision_id") or "").strip()
            if did and did not in decisions:
                errors.append(f"L{line_no}: last_review_decision_id {did!r} not in DECISION_REGISTER")

    if errors:
        print(f"FAIL ({len(errors)} issues)")
        for e in errors[:30]:
            print(f"  - {e}")
        if len(errors) > 30:
            print(f"  ... and {len(errors) - 30} more")
        return 1
    print(f"PASS ({len(seen)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
