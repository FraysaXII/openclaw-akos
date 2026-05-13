#!/usr/bin/env python3
"""Initiative 32 P3 — Validator for TOUCHPOINT_KIT_CELL_REGISTRY.csv.

Schema enforcement:
- Required header matches ``TOUCHPOINT_KIT_CELL_FIELDNAMES``.
- ``cell_id`` matches ``^CELL-[A-Z0-9-]{4,80}-(EN|ES|FR)$``; unique.
- ``persona_id`` resolves to ``PERSONA_REGISTRY.csv``.
- ``channel_id`` resolves to ``CHANNEL_TOUCHPOINT_REGISTRY.csv``.
- ``language`` is in ``ALLOWED_LANGUAGES``.
- ``topic_ids`` (semicolon list) — each id resolves to ``TOPIC_REGISTRY.csv``.
- ``template_path`` is a real file under
  ``docs/references/hlk/v3.0/_assets/touchpoint-kit/`` (FS-drift gate).
- ``distance_variants_in_file`` — each band is in ``VALID_DISTANCE_BANDS``.
- ``lifecycle_status`` is in ``VALID_LIFECYCLE_STATUSES``.
- ``last_review`` matches ``YYYY-MM-DD``.

Keystone invariant — **FS-vs-CSV drift detector**: the validator scans the
touchpoint-kit folder tree, derives the expected cell set from the filesystem
(every ``intro_message_<lang>.md`` under ``<persona>/<channel>/``), and asserts
the CSV mirrors it 1:1. Phantom rows (in CSV but not on disk) and missing
rows (on disk but not in CSV) both fail the validator.

Usage::

    py scripts/validate_touchpoint_kit_cells.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_touchpoint_kit_cell_csv import (
    ALLOWED_LANGUAGES,
    TOUCHPOINT_KIT_CELL_FIELDNAMES,
    TOUCHPOINT_KIT_ROOT,
    VALID_DISTANCE_BANDS,
    VALID_LIFECYCLE_STATUSES,
)
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOUCHPOINT_KIT_CELL_REGISTRY.csv"
PERSONA_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "PERSONA_REGISTRY.csv"
CHANNEL_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "CHANNEL_TOUCHPOINT_REGISTRY.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOPIC_REGISTRY.csv"
TKIT_ROOT = REPO_ROOT / TOUCHPOINT_KIT_ROOT

CELL_ID_RE = re.compile(r"^CELL-[A-Z0-9-]{4,80}-(EN|ES|FR)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TEMPLATE_FILE_RE = re.compile(r"^intro_message_(en|es|fr)\.md$")


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def _scan_filesystem_cells() -> set[tuple[str, str, str, str]]:
    """Derive expected (persona_id, channel_id, language, template_path) tuples
    from the filesystem. The path scheme is fixed by I31 P4:
        <TKIT_ROOT>/<persona_id>/<channel_id>/intro_message_<lang>.md
    """
    found: set[tuple[str, str, str, str]] = set()
    if not TKIT_ROOT.is_dir():
        return found
    for persona_dir in TKIT_ROOT.iterdir():
        if not persona_dir.is_dir() or not persona_dir.name.startswith("PERSONA-"):
            continue
        for channel_dir in persona_dir.iterdir():
            if not channel_dir.is_dir() or not channel_dir.name.startswith("CHAN-"):
                continue
            for f in channel_dir.iterdir():
                if not f.is_file():
                    continue
                m = TEMPLATE_FILE_RE.match(f.name)
                if not m:
                    continue
                lang = m.group(1)
                rel_path = f.relative_to(REPO_ROOT).as_posix()
                found.add((persona_dir.name, channel_dir.name, lang, rel_path))
    return found


def main() -> int:
    print("\n  TOUCHPOINT_KIT_CELL_REGISTRY Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: TOUCHPOINT_KIT_CELL_REGISTRY.csv not present")
        return 0

    persona_ids = _load_csv_set(PERSONA_CSV, "persona_id")
    channel_ids = _load_csv_set(CHANNEL_CSV, "channel_id")
    topic_ids = _load_csv_set(TOPIC_CSV, "topic_id")

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(TOUCHPOINT_KIT_CELL_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(TOUCHPOINT_KIT_CELL_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen_ids: set[str] = set()
    csv_cells: set[tuple[str, str, str, str]] = set()
    for i, r in enumerate(rows, start=2):
        cid = (r.get("cell_id") or "").strip()
        if not cid:
            errors.append(f"row {i}: cell_id empty")
            continue
        if not CELL_ID_RE.match(cid):
            errors.append(f"row {i}: cell_id {cid!r} does not match {CELL_ID_RE.pattern}")
        if cid in seen_ids:
            errors.append(f"row {i}: cell_id {cid!r} duplicated")
        seen_ids.add(cid)

        # persona_id FK
        pid = (r.get("persona_id") or "").strip()
        if persona_ids and pid not in persona_ids:
            errors.append(f"{cid}: persona_id {pid!r} not in PERSONA_REGISTRY.csv")

        # channel_id FK
        ccid = (r.get("channel_id") or "").strip()
        if channel_ids and ccid not in channel_ids:
            errors.append(f"{cid}: channel_id {ccid!r} not in CHANNEL_TOUCHPOINT_REGISTRY.csv")

        # language enum
        lang = (r.get("language") or "").strip()
        if lang not in ALLOWED_LANGUAGES:
            errors.append(f"{cid}: language {lang!r} not in {sorted(ALLOWED_LANGUAGES)}")

        # topic_ids FK
        for tid in _split_semi(r.get("topic_ids") or ""):
            if topic_ids and tid not in topic_ids:
                errors.append(f"{cid}: topic_id {tid!r} not in TOPIC_REGISTRY.csv")

        # template_path: file must exist on disk (FS-drift gate)
        tpath = (r.get("template_path") or "").strip()
        if not tpath:
            errors.append(f"{cid}: template_path empty")
        else:
            abs_path = REPO_ROOT / tpath
            if not abs_path.is_file():
                errors.append(f"{cid}: template_path {tpath!r} not found on disk (FS-drift)")
            else:
                csv_cells.add((pid, ccid, lang, tpath.replace("\\", "/")))

        # distance_variants_in_file enum
        for band in _split_semi(r.get("distance_variants_in_file") or ""):
            if band not in VALID_DISTANCE_BANDS:
                errors.append(
                    f"{cid}: distance band {band!r} not in {sorted(VALID_DISTANCE_BANDS)}"
                )

        # lifecycle_status enum
        lc = (r.get("lifecycle_status") or "").strip()
        if lc not in VALID_LIFECYCLE_STATUSES:
            errors.append(
                f"{cid}: lifecycle_status {lc!r} not in {sorted(VALID_LIFECYCLE_STATUSES)}"
            )

        # last_review YYYY-MM-DD
        lr = (r.get("last_review") or "").strip()
        if not DATE_RE.match(lr):
            errors.append(f"{cid}: last_review {lr!r} not YYYY-MM-DD")

    # Keystone: FS-vs-CSV drift detector
    fs_cells = _scan_filesystem_cells()
    fs_keys = {(p, c, l, t) for (p, c, l, t) in fs_cells}
    csv_keys = csv_cells

    missing_in_csv = fs_keys - csv_keys
    phantom_in_csv = csv_keys - fs_keys
    for (p, c, l, t) in sorted(missing_in_csv):
        errors.append(
            f"FS-drift: filesystem has {p}/{c}/intro_message_{l}.md but no matching CSV row "
            f"(template_path {t!r})"
        )
    for (p, c, l, t) in sorted(phantom_in_csv):
        errors.append(
            f"FS-drift: CSV row references {p}/{c}/{l} ({t!r}) but the file is not on disk"
        )

    print(f"  Rows validated: {len(rows)}")
    print(f"  CSV cells:      {len(csv_cells)}")
    print(f"  FS cells:       {len(fs_cells)}")

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
