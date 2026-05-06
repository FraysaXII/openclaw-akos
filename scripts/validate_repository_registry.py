#!/usr/bin/env python3
"""Initiative 59 P1.1 - Validator for REPOSITORY_REGISTRY.csv.

Schema enforcement:
- Required header matches REPOSITORY_REGISTRY_FIELDNAMES.
- repo_slug matches ^[a-z0-9][a-z0-9-]{1,80}$ ; unique.
- class is in VALID_REPO_CLASSES.
- lifecycle_status is in VALID_REPO_LIFECYCLE.
- primary_owner_role resolves against baseline_organisation.csv.
- topic_ids (semicolon list) - each id resolves to TOPIC_REGISTRY.csv (or "-").
- github_url starts with https://.

Usage::

    py scripts/validate_repository_registry.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_repository_registry_csv import (
    REPOSITORY_REGISTRY_FIELDNAMES,
    VALID_REPO_CLASSES,
    VALID_REPO_LIFECYCLE,
)
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "REPOSITORY_REGISTRY.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "baseline_organisation.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"

REPO_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,80}$")


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def main() -> int:
    print("\n  REPOSITORY_REGISTRY Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: REPOSITORY_REGISTRY.csv not present")
        return 0

    org_roles = _load_csv_set(ORG_CSV, "role_name")
    topic_ids = _load_csv_set(TOPIC_CSV, "topic_id")

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(REPOSITORY_REGISTRY_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(REPOSITORY_REGISTRY_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    by_class: dict[str, int] = {}
    for i, r in enumerate(rows, start=2):
        rs = (r.get("repo_slug") or "").strip()
        if not rs:
            errors.append(f"row {i}: repo_slug empty")
            continue
        if not REPO_SLUG_RE.match(rs):
            errors.append(f"row {i}: repo_slug {rs!r} does not match {REPO_SLUG_RE.pattern}")
        if rs in seen:
            errors.append(f"row {i}: repo_slug {rs!r} duplicated")
        seen.add(rs)

        url = (r.get("github_url") or "").strip()
        if not url.startswith("https://"):
            errors.append(f"{rs}: github_url {url!r} does not start with https://")

        cls = (r.get("class") or "").strip()
        if cls not in VALID_REPO_CLASSES:
            errors.append(f"{rs}: class {cls!r} not in {sorted(VALID_REPO_CLASSES)}")
        else:
            by_class[cls] = by_class.get(cls, 0) + 1

        lc = (r.get("lifecycle_status") or "").strip()
        if lc not in VALID_REPO_LIFECYCLE:
            errors.append(f"{rs}: lifecycle_status {lc!r} not in {sorted(VALID_REPO_LIFECYCLE)}")

        owner = (r.get("primary_owner_role") or "").strip()
        if not owner:
            errors.append(f"{rs}: primary_owner_role empty")
        elif org_roles and owner not in org_roles:
            errors.append(f"{rs}: primary_owner_role {owner!r} not in baseline_organisation.csv")

        for tid in _split_semi(r.get("topic_ids") or ""):
            if tid in {"-", "—"}:
                continue
            if topic_ids and tid not in topic_ids:
                errors.append(f"{rs}: topic_id {tid!r} not in TOPIC_REGISTRY.csv")

        api_topic = (r.get("api_topic_id") or "").strip()
        if api_topic and api_topic not in {"-", "—"}:
            if topic_ids and api_topic not in topic_ids:
                errors.append(f"{rs}: api_topic_id {api_topic!r} not in TOPIC_REGISTRY.csv")

    print(f"  Rows validated:     {len(rows)}")
    print(f"  Repos:              {len(seen)}")
    if by_class:
        print("  By class:")
        for cls in sorted(by_class):
            print(f"    {cls:18s} {by_class[cls]}")

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
