"""Validate BUILDOUT_BACKLOG.csv (D-IH-95-I). Schema + unique item_id + NO collision with
process_list item_ids (the two catalogs partition the id space) + role_owner FK when present.
Wired into validate_hlk.py. SKIPs gracefully if absent. Exit 0 PASS / 1 FAIL.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from akos.hlk_buildout_backlog_csv import BUILDOUT_BACKLOG_FIELDNAMES, BuildoutBacklogRow  # noqa: E402
from pydantic import ValidationError  # noqa: E402

DIM = REPO / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions"
BACKLOG = DIM / "BUILDOUT_BACKLOG.csv"
PROC = DIM.parent / "process_list.csv"
ORG = DIM.parent / "baseline_organisation.csv"


def _ids(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as f:
        return {(r.get(key) or "").strip() for r in csv.DictReader(f) if (r.get(key) or "").strip()}


def main() -> int:
    if not BACKLOG.is_file():
        print("  SKIP: BUILDOUT_BACKLOG.csv not found")
        return 0
    proc_ids = _ids(PROC, "item_id")
    roles = _ids(ORG, "role_name")
    errors: list[str] = []
    with BACKLOG.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != BUILDOUT_BACKLOG_FIELDNAMES:
            print("  FAIL: header mismatch vs BUILDOUT_BACKLOG_FIELDNAMES")
            return 1
        seen: set[str] = set()
        rows = list(reader)
    for i, row in enumerate(rows, start=2):
        try:
            BuildoutBacklogRow.model_validate(row)
        except ValidationError as exc:
            errors.append(f"L{i}: {exc.errors()[0]['msg']}")
            continue
        iid = (row.get("item_id") or "").strip()
        if iid in seen:
            errors.append(f"L{i}: duplicate item_id {iid}")
        seen.add(iid)
        if iid in proc_ids:
            errors.append(f"L{i}: item_id {iid} collides with a process_list item_id (id space must partition)")
        owner = (row.get("role_owner") or "").strip()
        if owner and owner not in roles:
            errors.append(f"L{i}: role_owner {owner!r} not in baseline_organisation")
    if errors:
        print(f"  FAIL: BUILDOUT_BACKLOG ({len(errors)} error(s))")
        for e in errors[:20]:
            print(f"    - {e}")
        return 1
    print(f"  PASS: BUILDOUT_BACKLOG ({len(rows)} backlog items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
