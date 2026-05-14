"""Engagement scaffolder RPA (Initiative 72 P8 per D-IH-72-P).

Takes engagement_id + template_id args; copies the engagement-template skeleton
folder to a new engagement folder under ``Think Big/Clients/<slug>/``; seeds
the engagement frontmatter from the template + engagement metadata; opens a PR
(when invoked from a CI environment with gh CLI available).

Usage:
    py scripts/scaffold_engagement.py --engagement-id <eid> --template-id <tid> [--slug <slug>]

Per the new Cursor rule `.cursor/rules/akos-executable-process-catalog.mdc`:
- Paired SOP: SOP-ENGAGEMENT_SCAFFOLDING_001.md (P8 follow-up; SCAFFOLD lifecycle).
- Cadence: event_triggered (fires when SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md
  completes a scaffold->active flip).

Pre-conditions:
- The template_id MUST exist in `ENGAGEMENT_TEMPLATE_REGISTRY.csv` with
  lifecycle_status=active; template promotion (P3 SOP) gates this script.
- The engagement_id MAY be new (this script creates the row in
  `ENGAGEMENT_REGISTRY.csv` when --register-engagement is passed) OR
  MUST exist when --register-engagement is omitted.

P8 lifecycle_status: scaffold. Initial implementation logs the contract +
verifies template availability; the actual file-copy + PR-open path lands
at I72 follow-up or operator-driven invocation per D-IH-72-P specification.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_REGISTRY_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "Operations" / "RevOps" / "canonicals" / "dimensions"
    / "ENGAGEMENT_TEMPLATE_REGISTRY.csv"
)
ENGAGEMENT_REGISTRY_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "Compliance" / "canonicals" / "dimensions"
    / "ENGAGEMENT_REGISTRY.csv"
)
ENGAGEMENT_TEMPLATE_SKELETON = REPO_ROOT / "Think Big" / "Clients" / "_engagement-template"
CLIENTS_ROOT = REPO_ROOT / "Think Big" / "Clients"


def lookup_template(template_id: str) -> dict[str, str] | None:
    if not TEMPLATE_REGISTRY_PATH.exists():
        return None
    with TEMPLATE_REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("template_id") == template_id:
                return row
    return None


def lookup_engagement(engagement_id: str) -> dict[str, str] | None:
    if not ENGAGEMENT_REGISTRY_PATH.exists():
        return None
    with ENGAGEMENT_REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("engagement_id") == engagement_id:
                return row
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="RevOps engagement scaffolder (I72 P8 RPA per D-IH-72-P)")
    parser.add_argument("--engagement-id", required=True, help="engagement_id (FK to ENGAGEMENT_REGISTRY.csv)")
    parser.add_argument("--template-id", required=True, help="template_id (FK to ENGAGEMENT_TEMPLATE_REGISTRY.csv; lifecycle=active required)")
    parser.add_argument("--slug", help="folder slug under Think Big/Clients/<slug>/ (defaults to engagement_id lowercased)")
    parser.add_argument("--dry-run", action="store_true", help="log contract only; no file ops or PR open")
    args = parser.parse_args()

    print()
    print("  scaffold_engagement.py — I72 P8 D-IH-72-P RPA")
    print("  =" * 25)
    print(f"  engagement_id: {args.engagement_id}")
    print(f"  template_id:   {args.template_id}")

    template = lookup_template(args.template_id)
    if template is None:
        print(f"  FAIL: template_id {args.template_id!r} not found in ENGAGEMENT_TEMPLATE_REGISTRY.csv", file=sys.stderr)
        return 1
    print(f"  Template found: {template.get('name', '?')}")
    print(f"  Template lifecycle_status: {template.get('lifecycle_status', '?')}")
    if template.get("lifecycle_status") != "active":
        print(f"  WARN: template lifecycle_status is {template.get('lifecycle_status')!r}, not 'active'.")
        print(f"        Run SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md to promote this template first.")
        if not args.dry_run:
            print(f"  FAIL: refusing to scaffold from non-active template (use --dry-run to override)", file=sys.stderr)
            return 1

    engagement = lookup_engagement(args.engagement_id)
    if engagement is None:
        print(f"  WARN: engagement_id {args.engagement_id!r} not found in ENGAGEMENT_REGISTRY.csv")
        print(f"        Future enhancement: --register-engagement flag to mint the row from template metadata.")
    else:
        print(f"  Engagement found: {engagement.get('engagement_name', '?')}")

    slug = args.slug or args.engagement_id.lower()
    target_path = CLIENTS_ROOT / slug
    print(f"  Target folder: {target_path}")

    if not ENGAGEMENT_TEMPLATE_SKELETON.exists():
        print(f"  WARN: engagement-template skeleton not found at {ENGAGEMENT_TEMPLATE_SKELETON}")
        print(f"        I72 P8 lifecycle_status=scaffold: skeleton path reservation only.")

    print()
    print("  Acceptance criteria (human; per akos-executable-process-catalog.mdc Rule 5):")
    print("    PMO reviews scaffolded folder + opens PR + assigns reviewer.")
    print("  Acceptance criteria (automation):")
    print("    Exit 0 with new folder + frontmatter; PR auto-opens; CI green.")

    print()
    if args.dry_run:
        print("  DRY-RUN: no file operations performed.")
    else:
        print("  P8 lifecycle_status=scaffold: contract logged.")
        print("  File-copy + PR-open path implementation lands at I72 follow-up or operator-driven invocation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
