#!/usr/bin/env python3
"""Initiative 31 P3 — Validator for CHANNEL_TOUCHPOINT_REGISTRY.csv.

Schema enforcement:
- Required header matches ``CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES``.
- ``channel_id`` matches ``^CHAN-[A-Z][A-Z0-9-]{2,40}$``; unique.
- ``direction`` is one of ``inbound|outbound|bidirectional``.
- ``typical_distance_band_inbound`` matches a band or band-range
  (``N1``, ``N1-N2``, ``N2-N3``, ``N3-N4``, ``N1-N4``).
- ``typical_personas`` (semicolon list) — each persona_id resolves to
  ``PERSONA_REGISTRY.csv``.
- ``response_owner_role`` is in ``baseline_organisation.csv`` OR a permitted
  free-form phrase (``Founder``).
- ``linked_topic_ids`` (semicolon list) — each id resolves to
  ``TOPIC_REGISTRY.csv``.

Usage::

    py scripts/validate_channel_touchpoint_registry.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_channel_touchpoint_registry_csv import CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "CHANNEL_TOUCHPOINT_REGISTRY.csv"
PERSONA_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "PERSONA_REGISTRY.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "baseline_organisation.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "TOPIC_REGISTRY.csv"

CHANNEL_ID_RE = re.compile(r"^CHAN-[A-Z][A-Z0-9-]{2,40}$")
DIRECTIONS = {"inbound", "outbound", "bidirectional"}
DISTANCE_TOKEN_RE = re.compile(r"^N[1-4](-N[1-4])?$")
HANDOFF_FREEFORM_PHRASES = {"Founder"}


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def main() -> int:
    print("\n  CHANNEL_TOUCHPOINT_REGISTRY Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: CHANNEL_TOUCHPOINT_REGISTRY.csv not present")
        return 0

    persona_ids = _load_csv_set(PERSONA_CSV, "persona_id")
    org_roles = _load_csv_set(ORG_CSV, "role_name")
    topic_ids = _load_csv_set(TOPIC_CSV, "topic_id")

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    for i, r in enumerate(rows, start=2):
        cid = (r.get("channel_id") or "").strip()
        if not cid:
            errors.append(f"row {i}: empty channel_id")
            continue
        if cid in seen:
            errors.append(f"row {i}: duplicate channel_id {cid!r}")
        seen.add(cid)
        if not CHANNEL_ID_RE.match(cid):
            errors.append(f"row {i}: channel_id {cid!r} must match ^CHAN-[A-Z][A-Z0-9-]{{2,40}}$")

        direction = (r.get("direction") or "").strip()
        if direction not in DIRECTIONS:
            errors.append(f"row {i}: invalid direction {direction!r}; expected {sorted(DIRECTIONS)}")

        dist = (r.get("typical_distance_band_inbound") or "").strip()
        if not DISTANCE_TOKEN_RE.match(dist):
            errors.append(
                f"row {i}: typical_distance_band_inbound {dist!r} must match Nx or Nx-Ny (1<=x<=y<=4)"
            )

        personas = (r.get("typical_personas") or "").strip()
        if personas:
            for pid in personas.split(";"):
                pid = pid.strip()
                if pid and persona_ids and pid not in persona_ids:
                    errors.append(f"row {i}: typical_persona {pid!r} not in PERSONA_REGISTRY.csv")

        owner = (r.get("response_owner_role") or "").strip()
        if owner and owner not in org_roles and owner not in HANDOFF_FREEFORM_PHRASES:
            errors.append(
                f"row {i}: response_owner_role {owner!r} not in baseline_organisation "
                f"and not a permitted free-form phrase"
            )

        topics = (r.get("linked_topic_ids") or "").strip()
        if topics:
            for tid in topics.split(";"):
                tid = tid.strip()
                if tid and topic_ids and tid not in topic_ids:
                    errors.append(f"row {i}: linked_topic_id {tid!r} not in TOPIC_REGISTRY.csv")

        name = (r.get("name") or "").strip()
        if not name:
            errors.append(f"row {i}: name is required")

    if errors:
        print(f"  FAIL: {len(errors)} issue(s)")
        for e in errors[:25]:
            print(f"    - {e}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        return 1

    print(f"  Rows validated: {len(rows)}")
    print(f"  Channels:       {len(seen)}")
    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
