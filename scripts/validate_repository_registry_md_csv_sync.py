#!/usr/bin/env python3
"""Initiative 59 P1.1 sync gate - REPOSITORIES_REGISTRY.md <-> REPOSITORY_REGISTRY.csv.

Per D-IH-59-C two-layer SSOT: the markdown table at
``docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md``
stays canonical for operator-readable narrative; the CSV at
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv`` becomes canonical for
machine-readable FK joins. This validator asserts both stay in sync at the row
level (one repo_slug per row in each surface; no orphans).

The check is **row-existence by repo_slug**, not field-by-field equality.
Fields like ``notes`` legitimately diverge between the prose-friendly markdown
and the FK-friendly CSV.

Usage::

    py scripts/validate_repository_registry_md_csv_sync.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "REPOSITORY_REGISTRY.csv"
MD_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Envoy Tech Lab" / "Repositories" / "REPOSITORIES_REGISTRY.md"

REPO_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,80}$")


def _csv_repo_slugs(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {
            (row.get("repo_slug") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("repo_slug") or "").strip()
        }


def _md_repo_slugs(path: Path) -> set[str]:
    """Extract repo_slugs from the markdown registry table.

    The table has rows of the shape:

        | repo_slug | github_url | class | primary_owner_role | topic_ids | ... |

    The header row + the ``|---|---|...|`` separator row are skipped because
    they don't match the slug regex.
    """
    if not path.is_file():
        return set()
    out: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        if first.startswith("---") or first.startswith("|") or first == "":
            continue
        if first.startswith("repo_slug"):
            continue
        if REPO_SLUG_RE.match(first):
            out.add(first)
    return out


def main() -> int:
    print("\n  REPOSITORY_REGISTRY md<->csv sync")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: REPOSITORY_REGISTRY.csv not present")
        return 0
    if not MD_PATH.is_file():
        print("  SKIP: REPOSITORIES_REGISTRY.md not present")
        return 0

    csv_slugs = _csv_repo_slugs(CSV_PATH)
    md_slugs = _md_repo_slugs(MD_PATH)

    only_md = md_slugs - csv_slugs
    only_csv = csv_slugs - md_slugs

    print(f"  CSV rows:           {len(csv_slugs)}")
    print(f"  Markdown rows:      {len(md_slugs)}")
    print(f"  Common:             {len(csv_slugs & md_slugs)}")

    errors: list[str] = []
    if only_md:
        for s in sorted(only_md):
            errors.append(f"in MD but not CSV: {s!r}")
    if only_csv:
        for s in sorted(only_csv):
            errors.append(f"in CSV but not MD: {s!r}")

    if errors:
        print(f"  FAIL: {len(errors)} drift entries")
        for e in errors[:10]:
            print(f"    - {e}")
        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more")
        return 1

    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
