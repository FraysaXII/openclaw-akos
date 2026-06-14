#!/usr/bin/env python3
"""Validate ``master-roadmap.md`` frontmatter against the I59 status taxonomy.

Initiative 59 P2 — frontmatter-side enforcement (companion to
``validate_initiative_registry.py`` which enforces the CSV side and
``validate_initiative_registry_frontmatter_sync.py`` which enforces the
markdown↔CSV agreement).

Walks every ``docs/wip/planning/<NN>-<slug>/master-roadmap.md`` file and
checks:

1. The frontmatter ``status:`` value (when present) is one of the seven
   ``akos.planning.status_taxonomy.InitiativeStatus`` enum values.
2. Required companion fields per :data:`REQUIRED_COMPANION_FIELDS` are
   present in the frontmatter when applicable.

Mode discipline:
    - **Advisory (default for P1–P2)**: missing ``status:`` is a *warning*
      (printed but does not fail the run); invalid status values fail.
    - **Strict (``--strict``, gated for P10)**: missing ``status:`` is an
      error.

Usage::

    py scripts/validate_master_roadmap_frontmatter.py
    py scripts/validate_master_roadmap_frontmatter.py --strict
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.planning.status_taxonomy import (
    REQUIRED_COMPANION_FIELDS,
    VALID_INITIATIVE_STATUSES,
)

PLANNING_DIR = REPO_ROOT / "docs" / "wip" / "planning"
INITIATIVE_DIR_RE = re.compile(r"^(\d{2}[a-z]?)-(.+)$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SCALAR_RE_TEMPLATE = r"^{key}\s*:\s*([^\s#][^\n#]*?)\s*(?:#.*)?$"


def _scalar(block: str, key: str) -> str | None:
    m = re.search(SCALAR_RE_TEMPLATE.format(key=re.escape(key)), block, re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip().strip('"').strip("'")


def _iter_master_roadmaps() -> list[Path]:
    out: list[Path] = []
    for d in sorted(PLANNING_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name == "00-ad-hoc-proposals":
            continue
        if not INITIATIVE_DIR_RE.match(d.name):
            continue
        roadmap = d / "master-roadmap.md"
        if roadmap.is_file():
            out.append(roadmap)
    return out


def _check_one(path: Path, strict: bool) -> tuple[list[str], list[str]]:
    """Return ``(errors, warnings)`` for a single master-roadmap.

    Errors fail the run. Warnings are printed but only fail under ``--strict``.
    """
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    fm = FRONTMATTER_RE.match(text)
    if not fm:
        msg = f"{path.relative_to(REPO_ROOT)}: missing frontmatter"
        if strict:
            errors.append(msg)
        else:
            warnings.append(msg)
        return errors, warnings
    block = fm.group(1)
    status = _scalar(block, "status")
    if status is None:
        msg = f"{path.relative_to(REPO_ROOT)}: frontmatter missing 'status:' field"
        if strict:
            errors.append(msg)
        else:
            warnings.append(msg)
        return errors, warnings
    status_norm = status.lower()
    if status_norm not in VALID_INITIATIVE_STATUSES:
        msg = (
            f"{path.relative_to(REPO_ROOT)}: status='{status}' is not in the I59 taxonomy "
            f"(valid: {sorted(VALID_INITIATIVE_STATUSES)})"
        )
        if strict:
            errors.append(msg)
        else:
            warnings.append(msg)
        return errors, warnings
    required = REQUIRED_COMPANION_FIELDS.get(status_norm, ())
    for field in required:
        value = _scalar(block, field)
        if not value:
            warnings.append(
                f"{path.relative_to(REPO_ROOT)}: status='{status_norm}' requires "
                f"companion field '{field}' (missing or empty)"
            )
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat missing frontmatter / missing status: / missing companion fields as errors",
    )
    args = parser.parse_args()

    paths = _iter_master_roadmaps()
    all_errors: list[str] = []
    all_warnings: list[str] = []
    valid_status_count = 0
    for p in paths:
        errors, warnings = _check_one(p, args.strict)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
        if not errors and not warnings:
            valid_status_count += 1

    print()
    print("  Master-roadmap frontmatter validator (I59 P2)")
    print("  ========================================")
    print(f"  Master-roadmaps scanned:  {len(paths)}")
    print(f"  With valid taxonomy status + companions: {valid_status_count}")
    print(f"  Warnings: {len(all_warnings)}{' (advisory; not failing)' if not args.strict else ''}")
    print(f"  Errors:   {len(all_errors)}")

    if args.strict and all_warnings:
        all_errors.extend(all_warnings)

    if all_warnings and not args.strict:
        for w in all_warnings[:10]:
            print(f"    - {w}")
        if len(all_warnings) > 10:
            print(f"    ... and {len(all_warnings) - 10} more")

    if all_errors:
        print()
        print("  Errors:")
        for e in all_errors[:25]:
            print(f"    - {e}")
        if len(all_errors) > 25:
            print(f"    ... and {len(all_errors) - 25} more")
        print("  FAIL")
        return 1

    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
