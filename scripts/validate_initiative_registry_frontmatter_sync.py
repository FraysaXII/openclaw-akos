#!/usr/bin/env python3
"""Initiative 59 P1.2 sync gate - master-roadmap.md frontmatter <-> INITIATIVE_REGISTRY.csv.

Per **D-IH-59-B** two-layer SSOT: per-initiative ``master-roadmap.md`` files
stay canonical for prose; ``INITIATIVE_REGISTRY.csv`` is canonical for governed
metadata. This validator asserts both surfaces agree on:

- One INITIATIVE_REGISTRY.csv row exists per ``docs/wip/planning/<NN>-<slug>/master-roadmap.md`` file.
- ``status`` field matches between frontmatter and CSV.
- ``last_review`` field matches between frontmatter and CSV (if both set).

The check is intentionally permissive: missing frontmatter on a planning folder
yields a **warning**, not a hard fail (some folders are placeholders or
``00-ad-hoc-proposals/`` ad-hoc artifacts). Status mismatch on a row that exists in
both surfaces is a **hard fail**.

Usage::

    py scripts/validate_initiative_registry_frontmatter_sync.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.planning.status_taxonomy import VALID_INITIATIVE_STATUSES

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "INITIATIVE_REGISTRY.csv"
PLANNING_ROOT = REPO_ROOT / "docs" / "wip" / "planning"

FOLDER_RE = re.compile(r"^(\d{2}[a-z]?)-(.+)$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
KV_RE = re.compile(r"^([a-z_]+):\s*(.*?)\s*$")


def _parse_frontmatter(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        kv = KV_RE.match(line)
        if kv:
            out[kv.group(1)] = kv.group(2).strip().strip("\"'")
    return out


def main() -> int:
    print("\n  INITIATIVE_REGISTRY frontmatter sync")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: INITIATIVE_REGISTRY.csv not present")
        return 0

    csv_rows: dict[str, dict[str, str]] = {}
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            iid = (row.get("initiative_id") or "").strip()
            if iid:
                csv_rows[iid] = row

    csv_by_folder: dict[str, dict[str, str]] = {}
    for iid, row in csv_rows.items():
        fp = (row.get("folder_path") or "").strip().rstrip("/")
        if fp:
            csv_by_folder[fp] = row

    folders: list[Path] = []
    if PLANNING_ROOT.is_dir():
        for d in sorted(PLANNING_ROOT.iterdir()):
            if not d.is_dir():
                continue
            if d.name == "00-ad-hoc-proposals":
                continue
            if FOLDER_RE.match(d.name):
                folders.append(d)

    errors: list[str] = []
    warnings: list[str] = []
    matched = 0
    for folder in folders:
        rel = folder.relative_to(REPO_ROOT).as_posix()
        mr = folder / "master-roadmap.md"
        if not mr.is_file():
            warnings.append(f"{rel}: no master-roadmap.md (skipped)")
            continue

        fm = _parse_frontmatter(mr)
        if not fm:
            warnings.append(f"{rel}: frontmatter empty/missing (skipped)")
            continue

        csv_row = csv_by_folder.get(rel)
        if not csv_row:
            warnings.append(f"{rel}: no INITIATIVE_REGISTRY.csv row matches folder_path")
            continue

        matched += 1

        md_status = fm.get("status", "").strip()
        csv_status = (csv_row.get("status") or "").strip()
        if md_status and csv_status and md_status != csv_status:
            if md_status not in VALID_INITIATIVE_STATUSES and csv_status in VALID_INITIATIVE_STATUSES:
                warnings.append(
                    f"{rel}: legacy frontmatter status {md_status!r} -> CSV uses canonical "
                    f"{csv_status!r} (P3 audit pending)"
                )
            else:
                errors.append(
                    f"{rel}: status mismatch md={md_status!r} csv={csv_status!r}"
                )

        md_lr = fm.get("last_review", "").strip()
        csv_lr = (csv_row.get("last_review") or "").strip()
        if md_lr and csv_lr and md_lr != csv_lr:
            warnings.append(f"{rel}: last_review mismatch md={md_lr!r} csv={csv_lr!r}")

    print(f"  Folders checked:    {len(folders)}")
    print(f"  CSV rows total:     {len(csv_rows)}")
    print(f"  Matched MD<->CSV:   {matched}")
    if warnings:
        print(f"  Warnings: {len(warnings)} (advisory; not failing)")
        for w in warnings[:10]:
            print(f"    - {w}")
        if len(warnings) > 10:
            print(f"    ... and {len(warnings) - 10} more")

    if errors:
        print(f"  FAIL: {len(errors)} mismatches")
        for e in errors[:10]:
            print(f"    - {e}")
        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more")
        return 1

    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
