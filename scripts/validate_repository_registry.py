#!/usr/bin/env python3
"""Initiative 59 P1.1 + I86 Wave H - Validator for REPOSITORY_REGISTRY.csv.

Schema enforcement:
- Required header matches REPOSITORY_REGISTRY_FIELDNAMES (29 columns after I86 Wave H).
- repo_slug matches ^[a-z0-9][a-z0-9-]{1,80}$ ; unique.
- class is in VALID_REPO_CLASSES.
- lifecycle_status is in VALID_REPO_LIFECYCLE.
- primary_owner_role resolves against baseline_organisation.csv.
- topic_ids (semicolon list) - each id resolves to TOPIC_REGISTRY.csv (or "-").
- github_url starts with https://.

I86 Wave H additions (D-IH-86-AD; advisory until backfill closure, then FAIL
via the --strict-app-class flag — I66 INFO->FAIL ramp pattern):
- app_class (when present) must be in VALID_APP_CLASS.
- governance_status (when present) must be in VALID_GOVERNANCE_STATUS.
- github_visibility (when present) must be in VALID_GITHUB_VISIBILITY.
- codeowners_present / branch_protection_enabled (when present) must be true/false.
- created_at / pushed_at / last_inventory_at (when present) must match YYYY-MM-DD.

Usage::

    py scripts/validate_repository_registry.py
    py scripts/validate_repository_registry.py --strict-app-class
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_repository_registry_csv import (
    REPOSITORY_REGISTRY_FIELDNAMES,
    VALID_APP_CLASS,
    VALID_GITHUB_VISIBILITY,
    VALID_GOVERNANCE_STATUS,
    VALID_REPO_CLASSES,
    VALID_REPO_LIFECYCLE,
)
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPOSITORY_REGISTRY.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "baseline_organisation.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOPIC_REGISTRY.csv"

REPO_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,80}$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BOOL_LITERALS = frozenset({"true", "false"})


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate REPOSITORY_REGISTRY.csv (I59 P1.1 + I86 Wave H).",
    )
    # Per D-IH-86-AD: app_class + governance_status promote to FAIL after backfill commit.
    # --strict-app-class flag enables FAIL mode (the I66 INFO->FAIL ramp pattern, applied
    # to schema extension by Lane F-AUTHOR-2).
    parser.add_argument(
        "--strict-app-class",
        action="store_true",
        default=False,
        help=(
            "FAIL when app_class or governance_status is missing on any row. "
            "Defaults off until the Lane F-AUTHOR-2 backfill commit lands; flipped on "
            "by config/verification-profiles.json once the canonical CSV carries app_class "
            "+ governance_status on every row."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    print("\n  REPOSITORY_REGISTRY Validator")
    print("  " + "=" * 40)
    if args.strict_app_class:
        print("  Mode: strict (app_class + governance_status required)")
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
    by_app_class: dict[str, int] = {}
    by_governance_status: dict[str, int] = {}
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

        # I86 Wave H — additive checks (flag INVALID values; missing values only fail
        # under --strict-app-class per D-IH-86-AD INFO->FAIL ramp pattern).
        app_class = (r.get("app_class") or "").strip()
        if app_class:
            if app_class not in VALID_APP_CLASS:
                errors.append(
                    f"{rs}: app_class {app_class!r} not in {sorted(VALID_APP_CLASS)}"
                )
            else:
                by_app_class[app_class] = by_app_class.get(app_class, 0) + 1
        elif args.strict_app_class:
            errors.append(f"{rs}: app_class empty (required under --strict-app-class)")

        governance_status = (r.get("governance_status") or "").strip()
        if governance_status:
            if governance_status not in VALID_GOVERNANCE_STATUS:
                errors.append(
                    f"{rs}: governance_status {governance_status!r} not in {sorted(VALID_GOVERNANCE_STATUS)}"
                )
            else:
                by_governance_status[governance_status] = (
                    by_governance_status.get(governance_status, 0) + 1
                )
        elif args.strict_app_class:
            errors.append(
                f"{rs}: governance_status empty (required under --strict-app-class)"
            )

        gh_vis = (r.get("github_visibility") or "").strip()
        if gh_vis and gh_vis not in VALID_GITHUB_VISIBILITY:
            errors.append(
                f"{rs}: github_visibility {gh_vis!r} not in {sorted(VALID_GITHUB_VISIBILITY)}"
            )

        for col in ("codeowners_present", "branch_protection_enabled"):
            val = (r.get(col) or "").strip()
            if val and val not in BOOL_LITERALS:
                errors.append(f"{rs}: {col} {val!r} must be 'true' or 'false'")

        for col in ("created_at", "pushed_at", "last_inventory_at"):
            val = (r.get(col) or "").strip()
            if val and not ISO_DATE_RE.match(val):
                errors.append(f"{rs}: {col} {val!r} does not match YYYY-MM-DD")

    print(f"  Rows validated:     {len(rows)}")
    print(f"  Repos:              {len(seen)}")
    if by_class:
        print("  By class:")
        for cls in sorted(by_class):
            print(f"    {cls:18s} {by_class[cls]}")
    if by_app_class:
        print("  By app_class:")
        for ac in sorted(by_app_class):
            print(f"    {ac:18s} {by_app_class[ac]}")
    if by_governance_status:
        print("  By governance_status:")
        for gs in sorted(by_governance_status):
            print(f"    {gs:18s} {by_governance_status[gs]}")

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
