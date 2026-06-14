"""Validate COMPONENT_MODULE_REGISTRY.csv (I100 / D-IH-100-C).

Checks: Pydantic schema, unique module_id, matrix FK coverage, owner_role in baseline,
scorecard (governed/partial/ungoverned/alias/inventory), critical-priority gaps.

Usage: py scripts/validate_component_module_registry.py [--self-test]
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from akos.hlk_component_module_registry import ComponentModuleRow, FIELDNAMES

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Tech"
    / "System Owner" / "canonicals" / "dimensions" / "COMPONENT_MODULE_REGISTRY.csv"
)
MATRIX_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People"
    / "Compliance" / "canonicals" / "techops" / "COMPONENT_SERVICE_MATRIX.csv"
)
BASELINE_ORG_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People"
    / "Compliance" / "canonicals" / "baseline_organisation.csv"
)


def _role_names() -> set[str]:
    with BASELINE_ORG_PATH.open(newline="", encoding="utf-8") as fh:
        return {(r.get("role_name") or "").strip() for r in csv.DictReader(fh)}


def _matrix_ids() -> set[str]:
    with MATRIX_PATH.open(newline="", encoding="utf-8") as fh:
        return {(r.get("component_id") or "").strip() for r in csv.DictReader(fh)}


def validate(path: Path = REGISTRY_PATH) -> tuple[bool, list[str]]:
    errors: list[str] = []
    roles = _role_names()
    matrix_ids = _matrix_ids()
    seen: set[str] = set()
    seen_components: set[str] = set()
    by_status: dict[str, int] = {}
    by_depth: dict[str, int] = {}
    crit_gaps: list[str] = []
    if not path.is_file():
        return False, [f"Missing registry: {path}"]
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return False, ["Registry is empty"]
    for i, raw in enumerate(rows, start=2):
        try:
            row = ComponentModuleRow(**raw)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"L{i}: {exc}")
            continue
        if row.module_id in seen:
            errors.append(f"L{i}: duplicate module_id {row.module_id}")
        seen.add(row.module_id)
        if row.component_id in seen_components:
            errors.append(f"L{i}: duplicate component_id {row.component_id}")
        seen_components.add(row.component_id)
        if row.component_id not in matrix_ids:
            errors.append(f"L{i}: component_id {row.component_id} not in matrix")
        if row.owner_role not in roles:
            errors.append(f"L{i}: owner_role {row.owner_role!r} not in baseline_organisation")
        by_status[row.governed_status] = by_status.get(row.governed_status, 0) + 1
        by_depth[row.governance_depth] = by_depth.get(row.governance_depth, 0) + 1
        if row.priority == "critical" and row.governed_status in {"ungoverned", "partial", "forward"}:
            if row.gap:
                crit_gaps.append(f"{row.module_id} ({row.component_id}): {row.gap}")
    missing = matrix_ids - seen_components
    if missing:
        errors.append(f"Matrix rows missing from registry: {sorted(missing)[:5]}… ({len(missing)} total)")
    print(
        f"[COMPONENT_MODULE_REGISTRY] rows={len(rows)} "
        f"status={by_status} depth={by_depth}"
    )
    if crit_gaps:
        print("[COMPONENT_MODULE_REGISTRY] critical-priority gaps (advisory):")
        for g in crit_gaps[:10]:
            print(f"  - {g}")
    return len(errors) == 0, errors


def _self_test() -> int:
    ok, errs = validate()
    if not ok:
        for e in errs:
            print(e, file=sys.stderr)
        return 1
    print("self-test OK")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _self_test()
    ok, errs = validate()
    for e in errs:
        print(e, file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
