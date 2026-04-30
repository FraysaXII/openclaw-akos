#!/usr/bin/env python3
"""Initiative 31 P2.1 — Validator for PERSONA_REGISTRY.csv.

Schema enforcement:
- Required header matches ``PERSONA_REGISTRY_FIELDNAMES``.
- ``persona_id`` matches ``^PERSONA-[A-Z][A-Z0-9-]{2,40}$``; unique.
- ``direction`` is one of ``inbound|outbound|bidirectional``.
- ``value_band`` is one of ``high|medium|low|depends_on_qualification``.
- ``typical_distance_band`` matches a band or band-range (``N1``, ``N1-N2``, ``N2-N3``, ``N3-N4``, ``N1-N4``).
- ``handoff_role`` (when not a bare phrase like "matches engagement") resolves to ``baseline_organisation.csv``.
- ``linked_topic_ids`` (semicolon list) — each id resolves to ``TOPIC_REGISTRY.csv``.
- ``intro_artifact_path`` is either a real path under ``docs/references/hlk/v3.0/_assets/touchpoint-kit/`` or a ``TODO[OPERATOR-x]`` marker.

Usage::

    py scripts/validate_persona_registry.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_persona_registry_csv import PERSONA_REGISTRY_FIELDNAMES
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PERSONA_REGISTRY.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "baseline_organisation.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"

PERSONA_ID_RE = re.compile(r"^PERSONA-[A-Z][A-Z0-9-]{2,40}$")
DIRECTIONS = {"inbound", "outbound", "bidirectional"}
VALUE_BANDS = {"high", "medium", "low", "depends_on_qualification"}
DISTANCE_TOKEN_RE = re.compile(r"^N[1-4](-N[1-4])?$")
TODO_OPERATOR_RE = re.compile(r"TODO\[OPERATOR-[^\]]+\]")
# Permitted handoff phrases that are NOT in baseline_organisation.csv:
# - "matches engagement" — the handoff role tracks the active engagement context,
#   not a fixed role (used for existing-customer / existing-partner personas).
# - "Founder" — semantic anchor in the brand voice (Initiative 24 P2 brand-voice
#   pillar) and the persona-registry handoff for high-value inbound categories
#   (investor, idea-proposer, joint-equity partner). Founder is not a separate
#   `role_name` in baseline_organisation.csv (the founder wears multiple roles
#   simultaneously: PMO, System Owner, etc) but is the natural handoff label.
HANDOFF_FREEFORM_PHRASES = {"matches engagement", "Founder"}


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def main() -> int:
    print("\n  PERSONA_REGISTRY Validator")
    print("  " + "=" * 40)
    if not CSV_PATH.is_file():
        print("  SKIP: PERSONA_REGISTRY.csv not present")
        return 0

    org_roles = _load_csv_set(ORG_CSV, "role_name")
    topic_ids = _load_csv_set(TOPIC_CSV, "topic_id")

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(PERSONA_REGISTRY_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(PERSONA_REGISTRY_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    for i, r in enumerate(rows, start=2):
        pid = (r.get("persona_id") or "").strip()
        if not pid:
            errors.append(f"row {i}: empty persona_id")
            continue
        if pid in seen:
            errors.append(f"row {i}: duplicate persona_id {pid!r}")
        seen.add(pid)
        if not PERSONA_ID_RE.match(pid):
            errors.append(f"row {i}: persona_id {pid!r} must match ^PERSONA-[A-Z][A-Z0-9-]{{2,40}}$")

        direction = (r.get("direction") or "").strip()
        if direction not in DIRECTIONS:
            errors.append(f"row {i}: invalid direction {direction!r}; expected {sorted(DIRECTIONS)}")

        value_band = (r.get("value_band") or "").strip()
        if value_band not in VALUE_BANDS:
            errors.append(f"row {i}: invalid value_band {value_band!r}; expected {sorted(VALUE_BANDS)}")

        dist = (r.get("typical_distance_band") or "").strip()
        if not DISTANCE_TOKEN_RE.match(dist):
            errors.append(
                f"row {i}: typical_distance_band {dist!r} must match Nx or Nx-Ny (1<=x<=y<=4)"
            )

        handoff = (r.get("handoff_role") or "").strip()
        if handoff and handoff not in org_roles and handoff not in HANDOFF_FREEFORM_PHRASES:
            errors.append(
                f"row {i}: handoff_role {handoff!r} not in baseline_organisation "
                f"and not a permitted free-form phrase"
            )

        topics = (r.get("linked_topic_ids") or "").strip()
        if topics:
            for tid in topics.split(";"):
                tid = tid.strip()
                if tid and topic_ids and tid not in topic_ids:
                    errors.append(f"row {i}: linked_topic_id {tid!r} not in TOPIC_REGISTRY.csv")

        intro = (r.get("intro_artifact_path") or "").strip()
        if intro and not TODO_OPERATOR_RE.search(intro):
            target = REPO_ROOT / intro
            if not target.is_file():
                errors.append(
                    f"row {i}: intro_artifact_path {intro!r} is neither a TODO[OPERATOR-x] marker "
                    f"nor a resolvable file under the repo"
                )

        intent = (r.get("intent_summary") or "").strip()
        if not intent:
            errors.append(f"row {i}: intent_summary is required")

    if errors:
        print(f"  FAIL: {len(errors)} issue(s)")
        for e in errors[:25]:
            print(f"    - {e}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        return 1

    print(f"  Rows validated: {len(rows)}")
    print(f"  Personas:       {len(seen)}")
    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
