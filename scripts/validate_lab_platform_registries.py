"""Validate Wave-1 and Wave-2 lab platform dimension registries (I100 / D-IH-100-E).

Unified validator for Vercel, Cloudflare, GitHub, and Wave-2 posture CSVs.

Usage: py scripts/validate_lab_platform_registries.py [--self-test]
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DIM_ROOT = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Tech"
    / "System Owner" / "canonicals" / "dimensions"
)
BASELINE_ORG_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People"
    / "Compliance" / "canonicals" / "baseline_organisation.csv"
)

REGISTRY_SPECS: dict[str, tuple[str, ...]] = {
    "VERCEL_PROJECT_SETTINGS_REGISTRY.csv": (
        "setting_id", "project_slug", "setting_surface", "expected_value", "probe_command",
        "governed_status", "owner_role", "component_fk", "contract_fk", "last_verified", "notes",
    ),
    "CLOUDFLARE_ZONE_SURFACE_REGISTRY.csv": (
        "surface_id", "zone_name", "surface_kind", "expected_value", "probe_command",
        "governed_status", "owner_role", "component_fk", "related_fk", "last_verified", "notes",
    ),
    "GITHUB_REPO_CI_POSTURE_REGISTRY.csv": (
        "posture_id", "repo_slug", "workflow_or_check", "expected_value", "probe_command",
        "governed_status", "owner_role", "component_fk", "baseline_sop_fk", "last_verified", "notes",
    ),
    "SENTRY_PROJECT_POSTURE_REGISTRY.csv": (
        "posture_id", "project_slug", "surface", "expected_value", "probe_command",
        "governed_status", "owner_role", "component_fk", "last_verified", "notes",
    ),
    "LANGFUSE_PROJECT_POSTURE_REGISTRY.csv": (
        "posture_id", "project_slug", "surface", "expected_value", "probe_command",
        "governed_status", "owner_role", "component_fk", "last_verified", "notes",
    ),
    "STRIPE_INTEGRATION_POSTURE_REGISTRY.csv": (
        "posture_id", "integration_slug", "surface", "expected_value", "probe_command",
        "governed_status", "owner_role", "component_fk", "last_verified", "notes",
    ),
    "MAKE_SCENARIO_POSTURE_REGISTRY.csv": (
        "posture_id", "workspace_slug", "surface", "expected_value", "probe_command",
        "governed_status", "owner_role", "component_fk", "last_verified", "notes",
    ),
    "N8N_WORKFLOW_POSTURE_REGISTRY.csv": (
        "posture_id", "instance_slug", "surface", "expected_value", "probe_command",
        "governed_status", "owner_role", "component_fk", "last_verified", "notes",
    ),
    "RENDER_SERVICE_POSTURE_REGISTRY.csv": (
        "posture_id", "service_slug", "surface", "expected_value", "probe_command",
        "governed_status", "owner_role", "component_fk", "last_verified", "notes",
    ),
    "LAB_PLATFORM_DIMENSION_REGISTRY.csv": (
        "dimension_id", "dimension_kind", "platform_slug", "resource_ref", "dimension_key",
        "expected_value", "probe_command", "governed_status", "owner_role", "component_fk",
        "contract_fk", "last_verified", "notes",
    ),
}

GOVERNED = {"governed", "partial", "ungoverned", "inventory", "forward"}


def _roles() -> set[str]:
    with BASELINE_ORG_PATH.open(newline="", encoding="utf-8") as fh:
        return {(r.get("role_name") or "").strip() for r in csv.DictReader(fh)}


def _validate_file(name: str, roles: set[str]) -> list[str]:
    errors: list[str] = []
    path = DIM_ROOT / name
    if not path.is_file():
        return [f"Missing {name}"]
    fields = REGISTRY_SPECS[name]
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(fields):
            errors.append(f"{name}: header mismatch expected {fields}")
        rows = list(reader)
    if not rows:
        errors.append(f"{name}: empty registry")
        return errors
    seen: set[str] = set()
    pk = fields[0]
    for i, row in enumerate(rows, start=2):
        rid = (row.get(pk) or "").strip()
        if not rid:
            errors.append(f"{name} L{i}: empty {pk}")
            continue
        if rid in seen:
            errors.append(f"{name} L{i}: duplicate {pk} {rid}")
        seen.add(rid)
        status = (row.get("governed_status") or "").strip()
        if status not in GOVERNED:
            errors.append(f"{name} L{i}: invalid governed_status {status!r}")
        owner = (row.get("owner_role") or "").strip()
        if owner and owner not in roles:
            errors.append(f"{name} L{i}: owner_role {owner!r} not in baseline")
    print(f"[{name}] rows={len(rows)}")
    return errors


def validate() -> tuple[bool, list[str]]:
    roles = _roles()
    errors: list[str] = []
    for name in REGISTRY_SPECS:
        errors.extend(_validate_file(name, roles))
    return len(errors) == 0, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    ok, errs = validate()
    for e in errs:
        print(e, file=sys.stderr)
    if args.self_test and ok:
        print("self-test OK")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
