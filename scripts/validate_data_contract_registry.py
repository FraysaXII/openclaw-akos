#!/usr/bin/env python3
"""Validate DATA_CONTRACT_REGISTRY.csv (Initiative 93 P2).

Usage::

    py scripts/validate_data_contract_registry.py
    py scripts/validate_data_contract_registry.py --self-test
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_data_contract_csv import (  # noqa: E402
    DATA_CONTRACT_REGISTRY_FIELDNAMES,
    VALID_CONSUMER_AREAS,
    VALID_DATAOPS_QUALITY_CODES,
    DataContractRegistryRow,
)
from pydantic import ValidationError  # noqa: E402

CSV_PATH = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/dimensions/DATA_CONTRACT_REGISTRY.csv"
ORG_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "baseline_organisation.csv"
)
PROCESS_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "process_list.csv"
)
DECISION_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "DECISION_REGISTER.csv"
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
    processes = _load_set(PROCESS_CSV, "item_id")
    decisions = _load_set(DECISION_CSV, "decision_id")

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != DATA_CONTRACT_REGISTRY_FIELDNAMES:
            errors.append("Header mismatch vs DATA_CONTRACT_REGISTRY_FIELDNAMES")
            print("FAIL")
            for e in errors:
                print(f"  - {e}")
            return 1, 0
        seen: set[str] = set()
        for line_no, row in enumerate(reader, start=2):
            cid = row.get("contract_id", "")
            if cid in seen:
                errors.append(f"L{line_no}: duplicate contract_id {cid!r}")
            seen.add(cid)
            try:
                DataContractRegistryRow.model_validate(row)
            except ValidationError as exc:
                errors.append(f"L{line_no}: Pydantic {exc.errors()[0]['msg']}")
                continue
            owner = (row.get("owner_role") or "").strip()
            if owner and owner not in roles:
                errors.append(f"L{line_no}: owner_role {owner!r} not in baseline_organisation")
            pid = (row.get("producer_process_id") or "").strip()
            if pid and pid not in processes:
                errors.append(f"L{line_no}: producer_process_id {pid!r} not in process_list")
            did = (row.get("last_review_decision_id") or "").strip()
            if did and did not in decisions:
                errors.append(f"L{line_no}: last_review_decision_id {did!r} not in DECISION_REGISTER")
            for code in (row.get("quality_rules") or "").split(";"):
                code = code.strip()
                if code and code not in VALID_DATAOPS_QUALITY_CODES:
                    errors.append(
                        f"L{line_no}: quality_rules code {code!r} not in DATA-01..DATA-07"
                    )
            for area in (row.get("consumer_area_ids") or "").split(";"):
                area = area.strip()
                if area and area not in VALID_CONSUMER_AREAS:
                    errors.append(
                        f"L{line_no}: consumer_area_ids {area!r} not in VALID_CONSUMER_AREAS"
                    )
            schema_ref = (row.get("schema_ref") or "").strip()
            if schema_ref.startswith("docs/"):
                ref_path = REPO_ROOT / schema_ref
                if not ref_path.is_file():
                    errors.append(
                        f"L{line_no}: schema_ref path missing on disk: {schema_ref!r}"
                    )

    if errors:
        print(f"FAIL ({len(errors)} issues)")
        for e in errors[:30]:
            print(f"  - {e}")
        if len(errors) > 30:
            print(f"  ... and {len(errors) - 30} more")
        return 1, len(seen)
    print(f"PASS ({len(seen)} rows)")
    return 0, len(seen)


def run_self_test() -> int:
    sample = {
        "contract_id": "DC-HOL-SELF-TEST-001",
        "producer_process_id": "env_tech_dtp_dataops_quality_001",
        "producer_area": "Tech",
        "consumer_area_ids": "Data",
        "data_surface": "mirror_table",
        "schema_ref": "docs/example/schema.csv",
        "semantics_ref": "self-test fixture",
        "sla_freshness": "24h",
        "sla_availability": "99%",
        "quality_rules": "DATA-01",
        "classification": "internal",
        "retention_policy_ref": "",
        "version": "0.0.1",
        "status": "draft",
        "owner_role": "Data Steward",
        "last_review_at": "2026-06-04",
        "last_review_by": "Data Governance Office",
        "last_review_decision_id": "D-IH-93-D",
        "methodology_version_at_review": "v3.1",
        "notes": "self-test fixture only",
    }
    try:
        DataContractRegistryRow.model_validate(sample)
    except ValidationError as exc:
        print(f"FAIL: Pydantic self-test {exc}")
        return 1
    if tuple(DATA_CONTRACT_REGISTRY_FIELDNAMES) != DATA_CONTRACT_REGISTRY_FIELDNAMES:
        print("FAIL: fieldnames tuple integrity")
        return 1
    print("PASS (self-test)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate DATA_CONTRACT_REGISTRY.csv")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run Pydantic fixture self-test without reading the CSV.",
    )
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    code, _ = validate_csv()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
