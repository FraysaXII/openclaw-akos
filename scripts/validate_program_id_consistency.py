#!/usr/bin/env python3
"""Cross-asset `program_id` consistency check (Initiative 23 P3).

Asserts that every `program_id` referenced anywhere in the canonical assets
resolves to a row in `docs/references/hlk/compliance/dimensions/PROGRAM_REGISTRY.csv`.

Scanned references:

- `GOI_POI_REGISTER.csv` `program_id` column.
- `ADVISER_OPEN_QUESTIONS.csv` `program_id` column.
- `FOUNDER_FILED_INSTRUMENTS.csv` `program_id` column.
- KM manifests under `docs/references/hlk/v3.0/_assets/<plane>/<program_id>/<topic_id>/*.manifest.md`
  -- the second path component when the layout matches the convention.
- Vault `programs/<program_id>/` folders under `docs/references/hlk/v3.0/<role>/`.

Exits 0 on PASS, 1 on FAIL. Hooked into `scripts/validate_hlk.py` after the
PROGRAM_REGISTRY validator. SKIPs gracefully when `PROGRAM_REGISTRY.csv` is
absent (the gate only applies once Initiative 23 P1 has shipped).

Authority: Wave-2 plan §"Initiative 23 P3" + D-IH-8.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
PROGRAM_REGISTRY_CSV = HLK_COMPLIANCE / "dimensions" / "PROGRAM_REGISTRY.csv"
GOIPOI_CSV = HLK_COMPLIANCE / "GOI_POI_REGISTER.csv"
QUESTIONS_CSV = HLK_COMPLIANCE / "ADVISER_OPEN_QUESTIONS.csv"
INSTRUMENTS_CSV = HLK_COMPLIANCE / "FOUNDER_FILED_INSTRUMENTS.csv"
ASSETS_ROOT = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "_assets"
V30_ROOT = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0"

PROGRAM_ID_RE = re.compile(r"^PRJ-HOL-[A-Z0-9-]+-\d{4}$")

# Reserved/aggregate placeholders that are intentionally not registry rows.
RESERVED_KEYWORDS = {"shared", "_meta"}


def _origin_label(path: Path) -> str:
    """Return a path label relative to REPO_ROOT, or absolute when outside."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def load_registered_program_ids() -> set[str]:
    if not PROGRAM_REGISTRY_CSV.is_file():
        return set()
    with PROGRAM_REGISTRY_CSV.open(encoding="utf-8", newline="") as f:
        return {(row.get("program_id") or "").strip() for row in csv.DictReader(f) if row.get("program_id")}


def collect_csv_program_ids(csv_path: Path) -> list[tuple[str, int, str]]:
    """Return (origin, row_index_starting_at_2, program_id) tuples for a single CSV."""
    if not csv_path.is_file():
        return []
    out: list[tuple[str, int, str]] = []
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            value = (row.get("program_id") or "").strip()
            if value:
                out.append((_origin_label(csv_path), i, value))
    return out


def collect_assets_program_ids() -> list[tuple[str, int, str]]:
    """Return path-derived program_ids from `_assets/<plane>/<program_id>/<topic_id>/`.

    Skips the grandfathered `_assets/km-pilot/` flat layout (Initiative 22 P2)
    and the cross-program `_meta/` aggregate area.
    """
    out: list[tuple[str, int, str]] = []
    if not ASSETS_ROOT.is_dir():
        return out
    for plane_dir in sorted(ASSETS_ROOT.iterdir()):
        if not plane_dir.is_dir():
            continue
        if plane_dir.name in {"km-pilot"} or plane_dir.name in RESERVED_KEYWORDS:
            continue
        for program_dir in sorted(plane_dir.iterdir()):
            if not program_dir.is_dir():
                continue
            if program_dir.name in RESERVED_KEYWORDS:
                continue
            out.append((_origin_label(program_dir), 0, program_dir.name))
    return out


def collect_vault_program_ids() -> list[tuple[str, int, str]]:
    """Return path-derived program_ids from `<role>/programs/<program_id>/`."""
    out: list[tuple[str, int, str]] = []
    if not V30_ROOT.is_dir():
        return out
    for programs_dir in V30_ROOT.rglob("programs"):
        if not programs_dir.is_dir():
            continue
        if "_assets" in programs_dir.parts:
            # Skip _assets/<plane>/<program_id>/ -- handled by collect_assets_program_ids.
            continue
        for program_dir in sorted(programs_dir.iterdir()):
            if not program_dir.is_dir():
                continue
            if program_dir.name in RESERVED_KEYWORDS:
                continue
            out.append((_origin_label(program_dir), 0, program_dir.name))
    return out


def main() -> int:
    print("\n  PROGRAM_ID consistency validator")
    print("  " + "=" * 40)
    if not PROGRAM_REGISTRY_CSV.is_file():
        print("  SKIP: PROGRAM_REGISTRY.csv not found (Initiative 23 not yet shipped)")
        return 0

    registered = load_registered_program_ids()
    if not registered:
        print("  SKIP: PROGRAM_REGISTRY.csv has no rows")
        return 0

    references: list[tuple[str, int, str]] = []
    references.extend(collect_csv_program_ids(GOIPOI_CSV))
    references.extend(collect_csv_program_ids(QUESTIONS_CSV))
    references.extend(collect_csv_program_ids(INSTRUMENTS_CSV))
    references.extend(collect_assets_program_ids())
    references.extend(collect_vault_program_ids())

    errors: list[str] = []
    referenced_ids: set[str] = set()
    for origin, row_index, value in references:
        if value in RESERVED_KEYWORDS:
            continue
        referenced_ids.add(value)
        if not PROGRAM_ID_RE.match(value):
            errors.append(f"{origin} (row {row_index}): malformed program_id {value!r}")
            continue
        if value not in registered:
            errors.append(
                f"{origin} (row {row_index}): unknown program_id {value!r} "
                "(not in PROGRAM_REGISTRY.csv)"
            )

    if errors:
        print(f"  FAIL: {len(errors)} unresolved reference(s)")
        for err in errors[:25]:
            print(f"    - {err}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        return 1

    print(f"  Registered programs: {len(registered)}")
    print(f"  References scanned:  {len(references)}")
    print(f"  Distinct ids ref'd:  {len(referenced_ids)}")
    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
