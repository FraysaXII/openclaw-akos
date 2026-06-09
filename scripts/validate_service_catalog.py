#!/usr/bin/env python3
"""Validate SERVICE_CATALOG.csv (Operations/SMO; P95-GOV-4).

Header drift gate + Pydantic row validation + unique service_id + optional
delivery_role_primary FK to baseline_organisation (with engagement aliases).

Usage::

    py scripts/validate_service_catalog.py
    py scripts/validate_service_catalog.py --self-test
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_service_catalog_csv import (  # noqa: E402
    CANONICAL_PATH,
    DELIVERY_ROLE_ALIASES,
    SERVICE_CATALOG_FIELDNAMES,
    ServiceCatalogRow,
)
from akos.io import REPO_ROOT  # noqa: E402
from akos.log import setup_logging  # noqa: E402

CSV_PATH = REPO_ROOT / CANONICAL_PATH
BASELINE_ORG_PATH = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "baseline_organisation.csv"
)


def _load_org_roles() -> set[str]:
    if not BASELINE_ORG_PATH.is_file():
        return set()
    with BASELINE_ORG_PATH.open(encoding="utf-8", newline="") as fh:
        return {(row.get("role_name") or "").strip() for row in csv.DictReader(fh) if row.get("role_name")}


def validate(path: Path = CSV_PATH) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return False, [f"SERVICE_CATALOG.csv not found at {path}"]

    org_roles = _load_org_roles()
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if list(reader.fieldnames or []) != list(SERVICE_CATALOG_FIELDNAMES):
            return False, [
                f"header mismatch: expected {list(SERVICE_CATALOG_FIELDNAMES)}, got {reader.fieldnames}"
            ]
        rows = list(reader)

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        try:
            ServiceCatalogRow.model_validate({k: (v or "") for k, v in row.items() if k})
        except Exception as exc:  # noqa: BLE001
            sid = (row.get("service_id") or f"row_{i}").strip()
            errors.append(f"row {i} ({sid}): {exc}")
            continue

        sid = (row.get("service_id") or "").strip()
        if sid in seen:
            errors.append(f"row {i}: duplicate service_id {sid!r}")
        seen.add(sid)

        primary = (row.get("delivery_role_primary") or "").strip()
        if org_roles and primary and primary not in org_roles and primary not in DELIVERY_ROLE_ALIASES:
            errors.append(
                f"row {i} ({sid}): delivery_role_primary {primary!r} not in baseline_organisation "
                f"or DELIVERY_ROLE_ALIASES"
            )

    return not errors, errors


def self_test() -> int:
    ok_row = ServiceCatalogRow.model_validate({
        "service_id": "SVC-001",
        "name": "Example",
        "customer_facing_description": "Desc",
        "delivery_role_primary": "SMO",
        "delivery_role_secondary": "",
        "cost_model": "Forfait",
        "sla_tier": "Tier 2 (Standard)",
        "active_engagements": "2026-example",
        "status": "active",
        "notes": "",
    })
    assert ok_row.service_id == "SVC-001"
    try:
        ServiceCatalogRow.model_validate({
            "service_id": "bad",
            "name": "Example",
            "customer_facing_description": "Desc",
            "delivery_role_primary": "SMO",
            "delivery_role_secondary": "",
            "cost_model": "Forfait",
            "sla_tier": "Tier 2 (Standard)",
            "active_engagements": "x",
            "status": "active",
            "notes": "",
        })
        return 1
    except Exception:
        pass
    print("PASS: validate_service_catalog self-test")
    return 0


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description="Validate SERVICE_CATALOG.csv")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    logger.debug("SERVICE_CATALOG validator invoked")
    print("\n  SERVICE_CATALOG Validator")
    print("  " + "=" * 50)
    ok, errors = validate()
    if ok:
        with CSV_PATH.open(encoding="utf-8", newline="") as fh:
            count = sum(1 for _ in csv.DictReader(fh))
        print(f"  PASS: SERVICE_CATALOG ({count} rows)")
        return 0
    print(f"  FAIL: SERVICE_CATALOG ({len(errors)} error(s))")
    for err in errors:
        print(f"    - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
