#!/usr/bin/env python3
"""Initiative 47 P1 — Validator for PERSONA_SCENARIO_REGISTRY.csv.

Schema enforcement:
- Required header matches ``PERSONA_SCENARIO_REGISTRY_FIELDNAMES``.
- ``scenario_id`` matches ``^SCN-[A-Z0-9-]{4,80}-V\\d+$``; unique.
- ``persona_id`` resolves against ``PERSONA_REGISTRY.csv`` (or equals
  ``OPERATOR`` pseudo-persona).
- ``skill_id`` resolves against ``SKILL_REGISTRY.csv``.
- ``tenant_id`` accepts empty/NULL (default per D-IH-47-K) or any non-empty
  string (future I34 multi-tenant).
- ``tier`` is in ``VALID_TIERS`` (1/2/3).
- ``scenario_class`` is in ``VALID_SCENARIO_CLASSES``.
- ``difficulty_class`` is in ``VALID_DIFFICULTY_CLASSES``.
- ``expected_route`` is in ``VALID_EXPECTED_ROUTES`` (akos.intent literals).
- ``expected_outcome_class`` is in ``VALID_EXPECTED_OUTCOME_CLASSES``.
- ``language`` is in ``VALID_LANGUAGES``.
- ``lifecycle_status`` is in ``VALID_LIFECYCLE_STATUSES``.
- ``topic_ids`` (semicolon list) — each id resolves to ``TOPIC_REGISTRY.csv``.
- ``priority_score`` (optional float string) — Initiative 49; non-negative if set.
- ``safety_lane`` / ``release_blocking`` — empty or ``true``/``false``.
- ``prompt_text`` is non-empty.

Usage::

    py scripts/validate_persona_scenario_registry.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_persona_scenario_csv import (
    OPERATOR_PSEUDO_PERSONA,
    PERSONA_SCENARIO_REGISTRY_FIELDNAMES,
    VALID_DIFFICULTY_CLASSES,
    VALID_EXPECTED_OUTCOME_CLASSES,
    VALID_EXPECTED_ROUTES,
    VALID_LANGUAGES,
    VALID_LIFECYCLE_STATUSES,
    VALID_SCENARIO_CLASSES,
    VALID_TIERS,
    parse_target_difficulty_band,
)
from akos.io import REPO_ROOT

CSV_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PERSONA_SCENARIO_REGISTRY.csv"
PERSONA_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PERSONA_REGISTRY.csv"
SKILL_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SKILL_REGISTRY.csv"
TOPIC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"

SCENARIO_ID_RE = re.compile(r"^SCN-[A-Z0-9-]{4,80}-V\d+$")


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def _validate_bool_csv(errors: list[str], sid: str, key: str, value: str | None) -> None:
    """I49: safety_lane / release_blocking empty or true|false (case-insensitive)."""
    v = (value or "").strip().lower()
    if not v:
        return
    if v not in ("true", "false"):
        errors.append(f"{sid}: {key} {v!r} must be empty, true, or false")


def main() -> int:
    print("\n  PERSONA_SCENARIO_REGISTRY Validator")
    print("  " + "=" * 50)
    if not CSV_PATH.is_file():
        print("  SKIP: PERSONA_SCENARIO_REGISTRY.csv not present")
        return 0

    persona_ids = _load_csv_set(PERSONA_CSV, "persona_id")
    skill_ids = _load_csv_set(SKILL_CSV, "skill_id")
    topic_ids = _load_csv_set(TOPIC_CSV, "topic_id")

    errors: list[str] = []
    warnings: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(PERSONA_SCENARIO_REGISTRY_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    per_persona: dict[str, int] = {}
    per_difficulty: dict[str, int] = {}
    # I51 P3 D-IH-51-A: per-persona consistency check for target_difficulty_band.
    # The column is a persona-level attribute carried on every row; all rows for
    # a given persona must share the same (potentially empty) band string.
    persona_band_seen: dict[str, set[str]] = {}
    for i, r in enumerate(rows, start=2):
        sid = (r.get("scenario_id") or "").strip()
        if not sid:
            errors.append(f"row {i}: scenario_id empty")
            continue
        if not SCENARIO_ID_RE.match(sid):
            errors.append(f"row {i}: scenario_id {sid!r} does not match {SCENARIO_ID_RE.pattern}")
        if sid in seen:
            errors.append(f"row {i}: scenario_id {sid!r} duplicated")
        seen.add(sid)

        persona = (r.get("persona_id") or "").strip()
        if not persona:
            errors.append(f"{sid}: persona_id empty")
        elif persona != OPERATOR_PSEUDO_PERSONA and persona_ids and persona not in persona_ids:
            errors.append(f"{sid}: persona_id {persona!r} not in PERSONA_REGISTRY.csv (or OPERATOR pseudo-persona)")
        per_persona[persona] = per_persona.get(persona, 0) + 1

        skill = (r.get("skill_id") or "").strip()
        if not skill:
            errors.append(f"{sid}: skill_id empty")
        elif skill_ids and skill not in skill_ids:
            errors.append(f"{sid}: skill_id {skill!r} not in SKILL_REGISTRY.csv")

        # tenant_id: empty/NULL accepted (D-IH-47-K default = shared); non-empty string accepted
        # (no FK validation today; future I34 may add one).
        # No error path; just informational tracking.

        tier = (r.get("tier") or "").strip()
        if tier not in VALID_TIERS:
            errors.append(f"{sid}: tier {tier!r} not in {sorted(VALID_TIERS)}")

        sc_class = (r.get("scenario_class") or "").strip()
        if sc_class not in VALID_SCENARIO_CLASSES:
            errors.append(f"{sid}: scenario_class {sc_class!r} not in {sorted(VALID_SCENARIO_CLASSES)}")

        diff = (r.get("difficulty_class") or "").strip()
        if diff not in VALID_DIFFICULTY_CLASSES:
            errors.append(f"{sid}: difficulty_class {diff!r} not in {sorted(VALID_DIFFICULTY_CLASSES)}")
        per_difficulty[diff] = per_difficulty.get(diff, 0) + 1

        prompt = (r.get("prompt_text") or "").strip()
        if not prompt:
            errors.append(f"{sid}: prompt_text empty")

        route = (r.get("expected_route") or "").strip()
        if route not in VALID_EXPECTED_ROUTES:
            errors.append(
                f"{sid}: expected_route {route!r} not in {sorted(VALID_EXPECTED_ROUTES)} (akos.intent literals)"
            )

        outcome = (r.get("expected_outcome_class") or "").strip()
        if outcome not in VALID_EXPECTED_OUTCOME_CLASSES:
            errors.append(
                f"{sid}: expected_outcome_class {outcome!r} not in {sorted(VALID_EXPECTED_OUTCOME_CLASSES)}"
            )

        lang = (r.get("language") or "").strip()
        if lang not in VALID_LANGUAGES:
            errors.append(f"{sid}: language {lang!r} not in {sorted(VALID_LANGUAGES)}")

        lc = (r.get("lifecycle_status") or "").strip()
        if lc not in VALID_LIFECYCLE_STATUSES:
            errors.append(f"{sid}: lifecycle_status {lc!r} not in {sorted(VALID_LIFECYCLE_STATUSES)}")

        for tid in _split_semi(r.get("topic_ids") or ""):
            if topic_ids and tid not in topic_ids:
                errors.append(f"{sid}: topic_id {tid!r} not in TOPIC_REGISTRY.csv")

        ps = (r.get("priority_score") or "").strip().lower()
        if ps:
            try:
                fv = float(ps.replace(",", "."))
                if fv < 0:
                    errors.append(f"{sid}: priority_score negative")
            except ValueError:
                errors.append(f"{sid}: priority_score {ps!r} not a float")

        _validate_bool_csv(errors, sid, "safety_lane", r.get("safety_lane"))
        _validate_bool_csv(errors, sid, "release_blocking", r.get("release_blocking"))

        # I51 P3 D-IH-51-A: target_difficulty_band format + per-persona consistency.
        band_raw = (r.get("target_difficulty_band") or "").strip()
        try:
            parse_target_difficulty_band(band_raw)
        except ValueError as exc:
            errors.append(f"{sid}: {exc}")
        # Track per-persona band values (across all rows of that persona).
        if persona:
            persona_band_seen.setdefault(persona, set()).add(band_raw)

    # I51 P3 D-IH-51-A: per-persona consistency enforcement.
    inconsistent_personas: list[str] = []
    for pid, bands in persona_band_seen.items():
        if len(bands) > 1:
            inconsistent_personas.append(f"{pid}: {sorted(bands)}")
    if inconsistent_personas:
        for s in inconsistent_personas:
            errors.append(f"target_difficulty_band inconsistent within persona — {s}")

    band_overrides = sum(
        1 for pid, bands in persona_band_seen.items()
        if len(bands) == 1 and next(iter(bands)) != ""
    )

    print(f"  Rows validated: {len(rows)}")
    print(f"  Scenarios:      {len(seen)}")
    print(f"  By persona:     {len(per_persona)} distinct personas (incl. OPERATOR pseudo)")
    print(f"  By difficulty:  {dict(sorted(per_difficulty.items()))}")
    print(f"  Personas with target_difficulty_band override: {band_overrides} / {len(persona_band_seen)}")

    if warnings:
        print("  Warnings (informational):")
        for w in warnings[:5]:
            print(f"    - {w}")

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
