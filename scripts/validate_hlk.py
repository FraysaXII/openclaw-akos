#!/usr/bin/env python3
"""HLK canonical vault validator.

Deterministic checks against baseline_organisation.csv and process_list.csv:
- CSV parseability with Pydantic models
- Referential integrity (role_owner resolves against org baseline)
- Graph integrity (0 broken parent refs, 0 orphans)
- Granularity canon (project/workstream/process/task only)
- No duplicate item_id or org_id
- All projects have at least one child

Usage: py scripts/validate_hlk.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.hlk_process_csv import ambiguous_item_names
from akos.models import OrgRole, ProcessItem

HLK_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
ORG_CSV = HLK_DIR / "baseline_organisation.csv"
PROC_CSV = HLK_DIR / "process_list.csv"

VALID_GRANULARITIES = {"project", "workstream", "process", "task"}
ALIAS_ROLE_OWNERS = {"Process Owner", "TBD"}


def load_org() -> list[dict]:
    with open(ORG_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_proc() -> list[dict]:
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def check_org_parse(rows: list[dict]) -> list[str]:
    errors = []
    for i, row in enumerate(rows, start=2):
        try:
            OrgRole.model_validate({k: (v or "") for k, v in row.items() if k})
        except Exception as e:
            errors.append(f"org row {i} ({row.get('role_name', '?')}): {e}")
    return errors


def check_proc_parse(rows: list[dict]) -> list[str]:
    errors = []
    for i, row in enumerate(rows, start=2):
        try:
            ProcessItem.model_validate({k: (v or "") for k, v in row.items() if k})
        except Exception as e:
            errors.append(f"proc row {i} ({row.get('item_id', '?')}): {e}")
    return errors


def check_role_owner_integrity(proc_rows: list[dict], org_names: set[str]) -> list[str]:
    errors = []
    for row in proc_rows:
        owner = row.get("role_owner", "").strip()
        if owner and owner not in org_names and owner not in ALIAS_ROLE_OWNERS:
            errors.append(f"{row.get('item_id', '?')}: role_owner '{owner}' not in baseline org")
    return errors


def check_graph_integrity(proc_rows: list[dict]) -> tuple[list[str], list[str]]:
    names = {row["item_name"].strip() for row in proc_rows if row.get("item_name")}
    broken = []
    orphans = []
    for row in proc_rows:
        p1 = row.get("item_parent_1", "").strip()
        gran = row.get("item_granularity", "").strip()
        if p1 and p1 not in names:
            broken.append(f"{row.get('item_id', '?')}: parent '{p1}' not found")
        if not p1 and gran != "project":
            orphans.append(f"{row.get('item_id', '?')}: non-project without parent")
    return broken, orphans


def check_granularity(proc_rows: list[dict]) -> list[str]:
    errors = []
    for row in proc_rows:
        g = row.get("item_granularity", "").strip().lower()
        if g and g not in VALID_GRANULARITIES:
            errors.append(f"{row.get('item_id', '?')}: invalid granularity '{g}'")
    return errors


def check_duplicate_ids(proc_rows: list[dict]) -> list[str]:
    seen: dict[str, int] = {}
    dupes = []
    for row in proc_rows:
        iid = row.get("item_id", "").strip()
        if iid:
            seen[iid] = seen.get(iid, 0) + 1
    for iid, count in seen.items():
        if count > 1:
            dupes.append(f"item_id '{iid}' appears {count} times")
    return dupes


def check_duplicate_org_ids(org_rows: list[dict]) -> list[str]:
    seen: dict[str, int] = {}
    dupes = []
    for row in org_rows:
        oid = row.get("org_id", "").strip()
        if oid:
            seen[oid] = seen.get(oid, 0) + 1
    for oid, count in seen.items():
        if count > 1:
            dupes.append(f"org_id '{oid}' appears {count} times")
    return dupes


def check_parent_id_consistency(proc_rows: list[dict]) -> list[str]:
    """When item_parent_*_id is set, it must resolve to item_name; strict id required for unique parent names."""
    by_id = {(row.get("item_id") or "").strip(): row for row in proc_rows if row.get("item_id")}
    amb = ambiguous_item_names([{k: (v or "") for k, v in r.items()} for r in proc_rows])
    errors: list[str] = []
    for row in proc_rows:
        iid = (row.get("item_id") or "").strip()
        gran = (row.get("item_granularity") or "").strip()
        for num in ("1", "2"):
            pname = (row.get(f"item_parent_{num}") or "").strip()
            pid = (row.get(f"item_parent_{num}_id") or "").strip()
            if pid:
                target = by_id.get(pid)
                if not target:
                    errors.append(f"{iid}: item_parent_{num}_id '{pid}' not found")
                elif (target.get("item_name") or "").strip() != pname:
                    errors.append(
                        f"{iid}: item_parent_{num}_id '{pid}' points to wrong item_name "
                        f"(expected {pname!r}, got {(target.get('item_name') or '').strip()!r})"
                    )
            if gran == "project":
                if pid:
                    errors.append(f"{iid}: project row must not set item_parent_{num}_id")
                continue
            if pname and pname not in amb and not pid:
                errors.append(f"{iid}: item_parent_{num} set to unique name {pname!r} but item_parent_{num}_id empty")
    return errors


def check_projects_have_children(proc_rows: list[dict]) -> list[str]:
    names = {row["item_name"].strip() for row in proc_rows if row.get("item_name")}
    parents_used = {row["item_parent_1"].strip() for row in proc_rows if row.get("item_parent_1")}
    errors = []
    for row in proc_rows:
        if row.get("item_granularity", "").strip() == "project":
            pname = row.get("item_name", "").strip()
            if pname not in parents_used:
                errors.append(f"project '{pname}' has no children")
    return errors


def main() -> int:
    print("\n  HLK Canonical Vault Validator")
    print("  " + "=" * 40)

    org_rows = load_org()
    proc_rows = load_proc()
    org_names = {row["role_name"].strip() for row in org_rows if row.get("role_name")}

    all_errors: list[str] = []
    checks = [
        ("Org CSV parse", check_org_parse(org_rows)),
        ("Process CSV parse", check_proc_parse(proc_rows)),
        ("Role owner integrity", check_role_owner_integrity(proc_rows, org_names)),
        ("Granularity canon", check_granularity(proc_rows)),
        ("Duplicate item_id", check_duplicate_ids(proc_rows)),
        ("Duplicate org_id", check_duplicate_org_ids(org_rows)),
        ("Projects have children", check_projects_have_children(proc_rows)),
    ]

    broken, orphans = check_graph_integrity(proc_rows)
    checks.append(("Broken parent refs", broken))
    checks.append(("Orphan items", orphans))
    checks.append(("Parent id consistency", check_parent_id_consistency(proc_rows)))

    for name, errors in checks:
        status = "PASS" if not errors else "FAIL"
        print(f"  {name:30s} {status}")
        if errors:
            for e in errors[:5]:
                print(f"    - {e}")
            if len(errors) > 5:
                print(f"    ... and {len(errors) - 5} more")
            all_errors.extend(errors)

    print()
    print(f"  Org roles:    {len(org_rows)}")
    print(f"  Process items: {len(proc_rows)}")
    print()

    if all_errors:
        print(f"  OVERALL: FAIL ({len(all_errors)} errors)")
        return 1
    else:
        print("  OVERALL: PASS")
        return 0


if __name__ == "__main__":
    sys.exit(main())
