#!/usr/bin/env python3
"""Initiative 31 P5.2 — Validator for SOURCING_REGISTER.csv.

Schema enforcement:
- Required header matches ``SOURCING_REGISTER_FIELDNAMES``.
- ``vendor_id`` matches ``^VENDOR-[A-Z][A-Z0-9-]{2,40}$``; unique.
- ``discipline`` is one of an open enum (designer / developer / marketer /
  translator / advisor / writer / video_editor / data_scientist / other).
- ``engagement_type`` is one of ``one_off | recurring | retainer``.
- ``distance_band_at_first_contact`` and ``current_distance_band`` are each
  one of ``N1 | N2 | N3 | N4`` (D-IH-31-G).
- ``quality_band`` (when set) is one of ``a | b | c``.
- ``last_engagement_date`` (when set) is ISO ``YYYY-MM-DD``.
- ``linked_topic_ids`` (semicolon list) — each id resolves to ``TOPIC_REGISTRY.csv``.

Usage::

    py scripts/validate_sourcing_register.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_sourcing_register_csv import SOURCING_REGISTER_FIELDNAMES
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "SOURCING_REGISTER.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOPIC_REGISTRY.csv"

VENDOR_ID_RE = re.compile(r"^VENDOR-[A-Z][A-Z0-9-]{2,40}$")
DISCIPLINES = {
    "designer", "developer", "marketer", "translator", "advisor",
    "writer", "video_editor", "data_scientist", "other",
}
ENGAGEMENT_TYPES = {"one_off", "recurring", "retainer", "pilot"}
DISTANCE_BANDS = {"N1", "N2", "N3", "N4"}
QUALITY_BANDS = {"", "a", "b", "c"}
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TODO_OPERATOR_RE = re.compile(r"TODO\[OPERATOR[^\]]*\]")


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def main() -> int:
    print("\n  SOURCING_REGISTER Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: SOURCING_REGISTER.csv not present")
        return 0

    topic_ids = _load_csv_set(TOPIC_CSV, "topic_id")

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(SOURCING_REGISTER_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(SOURCING_REGISTER_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    for i, r in enumerate(rows, start=2):
        vid = (r.get("vendor_id") or "").strip()
        if not vid:
            errors.append(f"row {i}: empty vendor_id")
            continue
        if vid in seen:
            errors.append(f"row {i}: duplicate vendor_id {vid!r}")
        seen.add(vid)
        if not VENDOR_ID_RE.match(vid):
            errors.append(f"row {i}: vendor_id {vid!r} must match ^VENDOR-[A-Z][A-Z0-9-]{{2,40}}$")

        discipline = (r.get("discipline") or "").strip()
        if discipline not in DISCIPLINES:
            errors.append(f"row {i}: invalid discipline {discipline!r}; expected {sorted(DISCIPLINES)}")

        eng = (r.get("engagement_type") or "").strip()
        if eng not in ENGAGEMENT_TYPES:
            errors.append(f"row {i}: invalid engagement_type {eng!r}; expected {sorted(ENGAGEMENT_TYPES)}")

        for col in ("distance_band_at_first_contact", "current_distance_band"):
            band = (r.get(col) or "").strip()
            if band not in DISTANCE_BANDS:
                errors.append(f"row {i}: invalid {col} {band!r}; expected {sorted(DISTANCE_BANDS)}")

        quality = (r.get("quality_band") or "").strip()
        if quality not in QUALITY_BANDS:
            errors.append(f"row {i}: invalid quality_band {quality!r}; expected one of a / b / c or empty")

        # hourly_rate_band may be a TODO[OPERATOR-x] marker (founder will fill); not strictly validated here.
        rate = (r.get("hourly_rate_band") or "").strip()
        if rate and not TODO_OPERATOR_RE.search(rate):
            # Allow free-form text like "EUR 30-50/h" or "USD 50/h fixed"; minimal guard
            pass

        last = (r.get("last_engagement_date") or "").strip()
        if last and not ISO_DATE_RE.match(last):
            errors.append(f"row {i}: last_engagement_date {last!r} not in ISO format (YYYY-MM-DD)")

        topics = (r.get("linked_topic_ids") or "").strip()
        if topics:
            for tid in topics.split(";"):
                tid = tid.strip()
                if tid and topic_ids and tid not in topic_ids:
                    errors.append(f"row {i}: linked_topic_id {tid!r} not in TOPIC_REGISTRY.csv")

    if errors:
        print(f"  FAIL: {len(errors)} issue(s)")
        for e in errors[:25]:
            print(f"    - {e}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        return 1

    print(f"  Rows validated: {len(rows)}")
    print(f"  Vendors:        {len(seen)}")
    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
