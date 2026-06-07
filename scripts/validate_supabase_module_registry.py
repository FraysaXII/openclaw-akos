"""Validate SUPABASE_MODULE_REGISTRY.csv (R2-03 / D-IH-95-G).

The Supabase ecosystem governance SSOT: every Supabase-governable surface (schemas, mirrors,
Edge Functions, extensions, cron, RLS, FDW, Auth/Storage/Realtime, API exposure) with its
governed/partial/ungoverned status + owner. Closes the operator's drift fear: governance must
cover the *whole* ecosystem, not just tables.

Checks: schema (Pydantic) + enums + unique module_id (SUPA-MOD-NN) + owner_role resolves in
baseline_organisation. Prints a governance scorecard (governed/partial/ungoverned counts +
critical-priority ungoverned gaps). Advisory-but-failing on schema/FK errors.

Usage: py scripts/validate_supabase_module_registry.py [--self-test]
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Data"
    / "Architecture" / "canonicals" / "dimensions" / "SUPABASE_MODULE_REGISTRY.csv"
)
BASELINE_ORG_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People"
    / "Compliance" / "canonicals" / "baseline_organisation.csv"
)

FIELDNAMES = (
    "module_id", "module_name", "supabase_surface", "repo_artifact",
    "governed_status", "owner_role", "priority", "gap", "notes",
)


class SupabaseModuleRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    module_id: str = Field(min_length=1, max_length=40)
    module_name: str = Field(min_length=1, max_length=120)
    supabase_surface: str = Field(min_length=1, max_length=80)
    repo_artifact: str = Field(min_length=1, max_length=300)
    governed_status: Literal["governed", "partial", "ungoverned", "forward"]
    owner_role: str = Field(min_length=1, max_length=60)
    priority: Literal["critical", "high", "medium", "low", "forward"]
    gap: str = Field(default="", max_length=300)
    notes: str = Field(default="", max_length=400)

    @field_validator("module_id")
    @classmethod
    def id_shape(cls, v: str) -> str:
        if not v.startswith("SUPA-MOD-"):
            raise ValueError("module_id must start with SUPA-MOD-")
        return v


def _role_names() -> set[str]:
    with BASELINE_ORG_PATH.open(newline="", encoding="utf-8") as fh:
        return {(r.get("role_name") or "").strip() for r in csv.DictReader(fh)}


def validate(path: Path = REGISTRY_PATH) -> tuple[bool, list[str]]:
    errors: list[str] = []
    roles = _role_names()
    seen: set[str] = set()
    by_status: dict[str, int] = {}
    crit_ungoverned: list[str] = []
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for i, raw in enumerate(rows, start=2):
        try:
            row = SupabaseModuleRow(**raw)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"L{i}: {exc}")
            continue
        if row.module_id in seen:
            errors.append(f"L{i}: duplicate module_id {row.module_id}")
        seen.add(row.module_id)
        if row.owner_role not in roles:
            errors.append(f"L{i}: owner_role {row.owner_role!r} not in baseline_organisation")
        by_status[row.governed_status] = by_status.get(row.governed_status, 0) + 1
        if row.governed_status == "ungoverned" and row.priority == "critical":
            crit_ungoverned.append(row.module_id)

    ok = not errors
    if ok:
        print(
            f"PASS: SUPABASE_MODULE_REGISTRY ({len(rows)} modules; "
            f"governed={by_status.get('governed',0)} partial={by_status.get('partial',0)} "
            f"ungoverned={by_status.get('ungoverned',0)} forward={by_status.get('forward',0)})"
        )
        if crit_ungoverned:
            print(f"  ADVISORY: critical-priority UNGOVERNED modules: {crit_ungoverned}")
    else:
        print(f"FAIL: SUPABASE_MODULE_REGISTRY ({len(errors)} error(s))")
        for e in errors:
            print(f"  - {e}")
    return ok, errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate the Supabase module registry")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        row = SupabaseModuleRow(
            module_id="SUPA-MOD-01", module_name="x", supabase_surface="migrations",
            repo_artifact="supabase/migrations", governed_status="governed",
            owner_role="Data Architect", priority="high",
        )
        assert row.module_id == "SUPA-MOD-01"
        print("validate_supabase_module_registry: self-test PASS")
        return 0
    ok, _ = validate()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
