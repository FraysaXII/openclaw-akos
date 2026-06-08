#!/usr/bin/env python3
"""Offline SSOT: Pydantic enum sets must be ⊆ mirror DDL CHECK constraints (DATA-05).

Scans ``supabase/migrations/*.sql`` for plain enum CHECK constraints and compares them to
the canonical Pydantic ``VALID_*`` frozensets. Catches the I93/I88 drift where
``area_governance`` was added to Pydantic but the mirror CHECK lagged until apply-time failure.

Pair with ``validate_mirror_enum_parity.py`` (emit vs live/snapshot CHECK at apply time).

Usage::

    py scripts/validate_pydantic_mirror_enum_ssot.py
    py scripts/validate_pydantic_mirror_enum_ssot.py --self-test
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MIGRATIONS = REPO_ROOT / "supabase" / "migrations"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_design_pattern_csv import VALID_PATTERN_CLASSES  # noqa: E402

_ANY_ARRAY_RE = re.compile(r"([a-z_][a-z0-9_]*) = ANY \(ARRAY\[(.*?)\]\)", re.DOTALL)
_IN_LIST_RE = re.compile(r"([a-z_][a-z0-9_]*) IN \((.*?)\)", re.DOTALL)
_ARRAY_VALUE_RE = re.compile(r"'((?:[^']|'')*)'::text")
_QUOTED_VALUE_RE = re.compile(r"'((?:[^']|'')*)'")
_COMPOUND_MARKERS = (" AND ", "<>", ">=", "<=", " < ", " > ", "CURRENT_DATE")
_TABLE_RE = re.compile(
    r"ALTER TABLE compliance\.(?P<tbl>[a-z0-9_]+).*?"
    r"ADD CONSTRAINT (?P<con>[a-z0-9_]+)\s+CHECK \((?P<def>.*?)\);",
    re.IGNORECASE | re.DOTALL,
)

# Pydantic SSOT enums keyed by (mirror_table, column)
_PYDANTIC_ENUM_SSOT: dict[tuple[str, str], frozenset[str]] = {
    ("people_design_pattern_registry_mirror", "pattern_class"): VALID_PATTERN_CLASSES,
}


def _parse_enum_check(def_str: str) -> tuple[str, set[str]] | tuple[None, None]:
    if any(m in def_str for m in _COMPOUND_MARKERS):
        return None, None
    if def_str.count("= ANY (ARRAY") == 1:
        m = _ANY_ARRAY_RE.search(def_str)
        if m:
            col = m.group(1)
            vals = {v.replace("''", "'") for v in _ARRAY_VALUE_RE.findall(m.group(2))}
            return col, vals
    if " IN (" in def_str:
        m = _IN_LIST_RE.search(def_str)
        if m:
            col = m.group(1)
            vals = {v.replace("''", "'") for v in _QUOTED_VALUE_RE.findall(m.group(2))}
            if vals:
                return col, vals
    return None, None


def _latest_migration_constraints() -> dict[tuple[str, str], set[str]]:
    """Last migration wins per (table, column) for ADD CONSTRAINT CHECK."""
    out: dict[tuple[str, str], set[str]] = {}
    for mig in sorted(MIGRATIONS.glob("*.sql")):
        text = mig.read_text(encoding="utf-8", errors="replace")
        # DROP CONSTRAINT clears prior — track drops
        drops: set[tuple[str, str]] = set()
        for drop_m in re.finditer(
            r"ALTER TABLE compliance\.(?P<tbl>[a-z0-9_]+)\s+DROP CONSTRAINT IF EXISTS (?P<con>[a-z0-9_]+)",
            text,
            re.IGNORECASE,
        ):
            tbl = drop_m.group("tbl")
            for key in list(out):
                if key[0] == tbl:
                    drops.add(key)
        for key in drops:
            out.pop(key, None)
        for m in _TABLE_RE.finditer(text):
            tbl = m.group("tbl")
            parsed = _parse_enum_check(m.group("def"))
            if not parsed[0]:
                continue
            col, allowed = parsed
            out[(tbl, col)] = allowed
    return out


def run_checks() -> list[str]:
    errors: list[str] = []
    mig_enums = _latest_migration_constraints()
    for (tbl, col), pydantic_vals in _PYDANTIC_ENUM_SSOT.items():
        ddl_vals = mig_enums.get((tbl, col))
        if ddl_vals is None:
            errors.append(f"{tbl}.{col}: no plain enum CHECK found in migrations (Pydantic has {len(pydantic_vals)} values)")
            continue
        missing = sorted(pydantic_vals - ddl_vals)
        if missing:
            errors.append(
                f"{tbl}.{col}: Pydantic allows {missing!r} but latest migration CHECK does not — "
                "add ALTER migration before mirror apply"
            )
    return errors


def self_test() -> int:
    assert "area_governance" in VALID_PATTERN_CLASSES
    col, vals = _parse_enum_check(
        "pattern_class IN ('register_dimension', 'area_governance', 'intent_ranked_regression_cadence')"
    )
    assert col == "pattern_class"
    assert "area_governance" in vals
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    errors = run_checks()
    if errors:
        print(f"FAIL: {len(errors)} pydantic<->migration enum drift(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"PASS: pydantic mirror enum SSOT — {len(_PYDANTIC_ENUM_SSOT)} bindings OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
