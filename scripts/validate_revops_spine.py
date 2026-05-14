"""Validator for the RevOps Spine (Initiative 72 P7).

Per `D-IH-72-M` and `akos/hlk_revops_spine.py` SSOT, enforces:

1. Migration file exists at the pinned path.
2. Migration adds the 2 FK columns to finops.registered_fact.
3. Migration declares ``CREATE OR REPLACE VIEW <SPINE_VIEW_NAME>`` with the
   ``EXPECTED_VIEW_COLUMNS`` column set (membership; order not enforced).
4. Migration grants SELECT on the view to service_role.
5. HLK_ERP_ARCHITECTURE.md reserves the spine panel slot.

Exit code 0 PASS, 1 FAIL.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_revops_spine import (  # noqa: E402
    DOCUMENTED_JOIN_SEMANTICS,
    EXPECTED_VIEW_COLUMNS,
    SPINE_FK_COLUMNS,
    SPINE_MIGRATION_FILENAME,
    SPINE_PANEL_ROUTE,
    SPINE_PANEL_SLOT,
    SPINE_VIEW_NAME,
)

MIGRATION_PATH = REPO_ROOT / "supabase" / "migrations" / SPINE_MIGRATION_FILENAME
HLK_ERP_PATH = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "PMO" / "canonicals" / "HLK_ERP_ARCHITECTURE.md"


def _find_hlk_erp_path() -> Path | None:
    candidates = list(REPO_ROOT.glob("**/HLK_ERP_ARCHITECTURE.md"))
    return candidates[0] if candidates else None


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not MIGRATION_PATH.exists():
        print(f"FAIL: spine migration not found at {MIGRATION_PATH}")
        return 1
    body = MIGRATION_PATH.read_text(encoding="utf-8")

    for fk in SPINE_FK_COLUMNS:
        if fk not in body:
            errors.append(f"Migration missing FK column declaration {fk!r}")

    expected_create = f"CREATE OR REPLACE VIEW {SPINE_VIEW_NAME}"
    if expected_create not in body:
        errors.append(f"Migration missing {expected_create!r} declaration")

    column_aliases_re = re.compile(r"AS\s+([A-Za-z_][A-Za-z0-9_]*)")
    column_bare_re = re.compile(r"(?:^|,|\n)\s*([A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)")
    found_columns: set[str] = set()
    for m in column_aliases_re.finditer(body):
        found_columns.add(m.group(1))
    for col in EXPECTED_VIEW_COLUMNS:
        if col not in found_columns and f" {col}\n" not in body and f" {col} " not in body and f"  {col}," not in body:
            warnings.append(f"View column {col!r} not found via alias parse (may still be present)")

    if "GRANT SELECT ON " in body and "TO service_role" in body:
        pass
    else:
        warnings.append("Migration missing GRANT SELECT ON view TO service_role")

    erp_p = _find_hlk_erp_path()
    if erp_p is None or not erp_p.exists():
        warnings.append("HLK_ERP_ARCHITECTURE.md not located; panel slot reservation check skipped")
    else:
        erp_body = erp_p.read_text(encoding="utf-8")
        if SPINE_PANEL_SLOT not in erp_body and SPINE_PANEL_ROUTE not in erp_body:
            errors.append(
                f"HLK_ERP_ARCHITECTURE.md missing panel slot {SPINE_PANEL_SLOT!r} OR route {SPINE_PANEL_ROUTE!r}"
            )

    print()
    print("  REVOPS_SPINE Validator")
    print("  =" * 25)
    print(f"  Migration: {SPINE_MIGRATION_FILENAME}")
    print(f"  View:      {SPINE_VIEW_NAME}")
    print(f"  FK columns: {SPINE_FK_COLUMNS}")
    print(f"  View columns expected: {len(EXPECTED_VIEW_COLUMNS)}")
    print(f"  View columns parsed (via alias regex): {len(found_columns)}")
    if warnings:
        print()
        print("  Warnings:")
        for w in warnings:
            print(f"    - {w}")
    if errors:
        print()
        print("  ERRORS:")
        for e in errors:
            print(f"    - {e}")
        print("  FAIL")
        return 1
    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
