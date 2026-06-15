#!/usr/bin/env python3
"""Validate CANONICAL_GOVERNANCE_REGISTRY.csv (I95 P95-GOV-1).

Checks schema, unique governance_id, csv_path file existence, and 1:1 vault inventory
coverage (every ``docs/references/hlk/v3.0/**/canonicals/**/*.csv`` except this registry).

Usage::

    py scripts/validate_canonical_governance_registry.py
    py scripts/validate_canonical_governance_registry.py --self-test
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from akos.hlk_canonical_governance_registry_csv import (  # noqa: E402
    CANONICAL_GOVERNANCE_REGISTRY_FIELDNAMES,
    EXPECTED_VAULT_CSV_COUNT,
    CanonicalGovernanceRegistryRow,
)
from pydantic import ValidationError  # noqa: E402

REGISTRY = (
    REPO
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions"
    / "CANONICAL_GOVERNANCE_REGISTRY.csv"
)
VAULT_ROOT = REPO / "docs" / "references" / "hlk" / "v3.0"
CANONICAL_REGISTRY = (
    REPO
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv"
)


def _discover_vault_csvs() -> set[str]:
    return {
        p.relative_to(REPO).as_posix()
        for p in VAULT_ROOT.rglob("canonicals/**/*.csv")
        if p.name != "CANONICAL_GOVERNANCE_REGISTRY.csv"
    }


def _load_canonical_ids() -> set[str]:
    if not CANONICAL_REGISTRY.is_file():
        return set()
    with CANONICAL_REGISTRY.open(encoding="utf-8", newline="") as fh:
        return {(r.get("canonical_id") or "").strip() for r in csv.DictReader(fh) if r.get("canonical_id")}


def run_checks() -> tuple[list[str], int]:
    errors: list[str] = []
    if not REGISTRY.is_file():
        return [f"missing registry at {REGISTRY.relative_to(REPO).as_posix()}"], 0

    with REGISTRY.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != CANONICAL_GOVERNANCE_REGISTRY_FIELDNAMES:
            return ["header mismatch vs CANONICAL_GOVERNANCE_REGISTRY_FIELDNAMES"], 0
        rows = list(reader)

    if len(rows) != EXPECTED_VAULT_CSV_COUNT:
        errors.append(f"row count {len(rows)} != expected {EXPECTED_VAULT_CSV_COUNT}")

    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    canon_ids = _load_canonical_ids()

    for i, row in enumerate(rows, start=2):
        gid = (row.get("governance_id") or "").strip()
        cp = (row.get("csv_path") or "").strip()
        if cp:
            if cp in seen_paths:
                errors.append(f"L{i}: duplicate csv_path {cp}")
            seen_paths.add(cp)
        try:
            CanonicalGovernanceRegistryRow.model_validate(row)
        except ValidationError as exc:
            errors.append(f"L{i}: {exc.errors()[0]['msg']}")
            continue
        if gid in seen_ids:
            errors.append(f"L{i}: duplicate governance_id {gid}")
        seen_ids.add(gid)
        if not (REPO / cp).is_file():
            errors.append(f"L{i}: csv_path missing on disk: {cp}")
        rid = (row.get("canonical_registry_id") or "").strip()
        if rid and rid not in canon_ids:
            errors.append(f"L{i}: canonical_registry_id {rid!r} not in CANONICAL_REGISTRY")
        if row["plane2_sync_policy"] == "active" and not (row.get("plane2_mirror_table") or "").strip():
            errors.append(f"L{i}: plane2_sync_policy=active requires plane2_mirror_table")
        if row["plane1_in_validate_hlk"] != "true":
            errors.append(
                f"L{i}: plane1_in_validate_hlk must be true for universal plane-1 hardening ({gid})"
            )

    vault = _discover_vault_csvs()
    missing = vault - seen_paths
    extra = seen_paths - vault
    if missing:
        errors.append(f"vault CSVs not indexed ({len(missing)}): {sorted(missing)[:5]}")
    if extra:
        errors.append(f"registry paths not in vault ({len(extra)}): {sorted(extra)[:5]}")

    return errors, len(rows)


def self_test() -> int:
    sample = CanonicalGovernanceRegistryRow.model_validate({
        "governance_id": "gov_people_compliance_topic_registry",
        "csv_path": (
            "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
            "dimensions/TOPIC_REGISTRY.csv"
        ),
        "owning_area": "People_Compliance",
        "owning_role": "Compliance",
        "asset_class": "compliance_mirror",
        "plane1_validator": "validate_topic_registry.py",
        "plane1_in_validate_hlk": "true",
        "plane2_mirror_table": "compliance.topic_registry_mirror",
        "plane2_sync_policy": "active",
        "plane2_emit_profile": "main",
        "plane2_workflow_paths": "dimensions/TOPIC_REGISTRY.csv",
        "precedence_registered": "true",
        "canonical_registry_id": "topic_registry",
        "mirror_ddl_migration": "",
        "enum_parity_required": "true",
        "delete_reconcile_pk": "topic_id",
        "last_review": "2026-06-09",
        "last_review_decision_id": "D-IH-95-B",
        "status": "active",
        "notes": "",
    })
    assert sample.governance_id.startswith("gov_")
    assert len(CANONICAL_GOVERNANCE_REGISTRY_FIELDNAMES) == 20
    assert EXPECTED_VAULT_CSV_COUNT == 92
    print("PASS: validate_canonical_governance_registry self-test")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    errors, count = run_checks()
    if errors:
        print(f"FAIL: CANONICAL_GOVERNANCE_REGISTRY ({len(errors)} error(s))")
        for e in errors[:25]:
            print(f"  - {e}")
        return 1
    print(f"PASS: CANONICAL_GOVERNANCE_REGISTRY ({count} vault CSV rows indexed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
