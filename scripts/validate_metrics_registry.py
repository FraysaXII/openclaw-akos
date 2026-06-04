#!/usr/bin/env python3
"""Validate METRICS_REGISTRY.csv (Initiative 93 P4).

Usage::

    py scripts/validate_metrics_registry.py
    py scripts/validate_metrics_registry.py --self-test
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_metrics_registry_csv import (  # noqa: E402
    METRICS_REGISTRY_FIELDNAMES,
    MetricsRegistryRow,
)
from pydantic import ValidationError  # noqa: E402

CSV_PATH = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/METRICS_REGISTRY.csv"
)
ORG_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "baseline_organisation.csv"
)
DECISION_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "DECISION_REGISTER.csv"
)
CONTRACT_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals"
    / "dimensions/DATA_CONTRACT_REGISTRY.csv"
)


def _load_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(r.get(key) or "").strip() for r in csv.DictReader(fh) if (r.get(key) or "").strip()}


def validate_csv() -> tuple[int, int]:
    errors: list[str] = []
    if not CSV_PATH.is_file():
        print(f"FAIL: missing {CSV_PATH.relative_to(REPO_ROOT)}")
        return 1, 0
    roles = _load_set(ORG_CSV, "role_name")
    decisions = _load_set(DECISION_CSV, "decision_id")
    contracts = _load_set(CONTRACT_CSV, "contract_id")

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != METRICS_REGISTRY_FIELDNAMES:
            errors.append("Header mismatch vs METRICS_REGISTRY_FIELDNAMES")
            print("FAIL")
            for e in errors:
                print(f"  - {e}")
            return 1, 0
        seen: set[str] = set()
        for line_no, row in enumerate(reader, start=2):
            mid = row.get("metric_id", "")
            if mid in seen:
                errors.append(f"L{line_no}: duplicate metric_id {mid!r}")
            seen.add(mid)
            try:
                MetricsRegistryRow.model_validate(row)
            except ValidationError as exc:
                errors.append(f"L{line_no}: Pydantic {exc.errors()[0]['msg']}")
                continue
            for role_key in ("owner_business_role", "owner_technical_role"):
                role = (row.get(role_key) or "").strip()
                if role and role not in roles:
                    errors.append(f"L{line_no}: {role_key} {role!r} not in baseline_organisation")
            did = (row.get("last_review_decision_id") or "").strip()
            if did and did not in decisions:
                errors.append(f"L{line_no}: last_review_decision_id {did!r} not in DECISION_REGISTER")
            cid = (row.get("source_contract_id") or "").strip()
            if cid and cid not in contracts:
                errors.append(f"L{line_no}: source_contract_id {cid!r} not in DATA_CONTRACT_REGISTRY")
            ref = (row.get("definition_sql_ref") or "").strip()
            if ref.startswith("docs/") or ref.startswith("scripts/"):
                ref_path = REPO_ROOT / ref.split()[0]
                if not ref_path.is_file():
                    errors.append(f"L{line_no}: definition_sql_ref path missing: {ref!r}")

    if errors:
        print(f"FAIL ({len(errors)} issues)")
        for e in errors[:30]:
            print(f"  - {e}")
        return 1, len(seen)
    print(f"PASS ({len(seen)} rows)")
    return 0, len(seen)


def run_self_test() -> int:
    sample = {
        "metric_id": "MET-HOL-SELF-TEST-001",
        "metric_name": "Self test metric",
        "definition_sql_ref": "scripts/validate_metrics_registry.py",
        "grain": "test",
        "dimensions": "none",
        "owner_business_role": "Data Steward",
        "owner_technical_role": "Data Steward",
        "source_contract_id": "",
        "access_level": "4",
        "status": "draft",
        "last_review_at": "2026-06-04",
        "last_review_by": "Data Architect",
        "last_review_decision_id": "D-IH-93-D",
        "methodology_version_at_review": "v3.1",
        "notes": "self-test",
    }
    try:
        MetricsRegistryRow.model_validate(sample)
    except ValidationError as exc:
        print(f"FAIL: Pydantic self-test {exc}")
        return 1
    print("PASS (self-test)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate METRICS_REGISTRY.csv")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    code, _ = validate_csv()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
