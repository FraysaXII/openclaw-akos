#!/usr/bin/env python3
"""Initiative 32 P7 — Validator for REPO_HEALTH_SNAPSHOT.csv.

Schema enforcement:
- Required header matches ``REPO_HEALTH_SNAPSHOT_FIELDNAMES``.
- ``repo_slug`` resolves against ``REPOSITORIES_REGISTRY.md`` slug list.
- ``snapshot_date`` is YYYY-MM-DD.
- ``cursor_rule_count`` and ``brand_jargon_violations`` parse as int.
- ``has_external_repo_contract`` / ``has_akos_mirror_rule`` /
  ``embedded_obsidian_snapshot_present`` are 'true' or 'false'.
- ``language_frontmatter_compliance_pct`` parses as float in ``[0.0, 100.0]``.

Usage::

    py scripts/validate_repo_health_snapshot.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_repo_health_csv import REPO_HEALTH_SNAPSHOT_FIELDNAMES
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPO_HEALTH_SNAPSHOT.csv"
REPOS_REGISTRY = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Envoy Tech Lab" / "Repositories" / "REPOSITORIES_REGISTRY.md"

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BOOL_VALUES = {"true", "false"}
SLUG_ROW_RE = re.compile(r"^\| ([a-z0-9-]+)\s+\|", re.MULTILINE)


def _registry_slugs() -> set[str]:
    if not REPOS_REGISTRY.is_file():
        return set()
    text = REPOS_REGISTRY.read_text(encoding="utf-8")
    return set(SLUG_ROW_RE.findall(text))


def main() -> int:
    print("\n  REPO_HEALTH_SNAPSHOT Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: REPO_HEALTH_SNAPSHOT.csv not present")
        return 0

    registry_slugs = _registry_slugs()

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(REPO_HEALTH_SNAPSHOT_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(REPO_HEALTH_SNAPSHOT_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen_slugs: set[str] = set()
    for i, r in enumerate(rows, start=2):
        slug = (r.get("repo_slug") or "").strip()
        if not slug:
            errors.append(f"row {i}: repo_slug empty")
            continue
        if registry_slugs and slug not in registry_slugs:
            errors.append(f"row {i}: repo_slug {slug!r} not in REPOSITORIES_REGISTRY.md")
        if slug in seen_slugs:
            # Snapshot CSV is overwritten weekly so each slug appears at most once per snapshot.
            errors.append(f"row {i}: repo_slug {slug!r} duplicated in snapshot")
        seen_slugs.add(slug)

        # snapshot_date YYYY-MM-DD
        sd = (r.get("snapshot_date") or "").strip()
        if not DATE_RE.match(sd):
            errors.append(f"{slug}: snapshot_date {sd!r} not YYYY-MM-DD")

        # int fields
        for field in ("cursor_rule_count", "brand_jargon_violations"):
            v = (r.get(field) or "").strip()
            try:
                int(v)
            except ValueError:
                errors.append(f"{slug}: {field} {v!r} not int")

        # bool fields
        for field in (
            "has_external_repo_contract",
            "has_akos_mirror_rule",
            "embedded_obsidian_snapshot_present",
        ):
            v = (r.get(field) or "").strip().lower()
            if v not in BOOL_VALUES:
                errors.append(f"{slug}: {field} {v!r} not in {sorted(BOOL_VALUES)}")

        # float field
        pct_raw = (r.get("language_frontmatter_compliance_pct") or "").strip()
        try:
            pct = float(pct_raw)
            if pct < 0.0 or pct > 100.0:
                errors.append(f"{slug}: language_frontmatter_compliance_pct {pct} out of [0, 100]")
        except ValueError:
            errors.append(f"{slug}: language_frontmatter_compliance_pct {pct_raw!r} not float")

    print(f"  Rows validated: {len(rows)}")
    print(f"  Repos:          {len(seen_slugs)}")

    if errors:
        print(f"  FAIL: {len(errors)} errors")
        for e in errors[:10]:
            print(f"    - {e}")
        return 1

    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
