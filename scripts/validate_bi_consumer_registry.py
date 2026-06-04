#!/usr/bin/env python3
"""Validate BI_CONSUMER_REGISTRY.csv (Initiative 93 P5b).

Usage::

    py scripts/validate_bi_consumer_registry.py
    py scripts/validate_bi_consumer_registry.py --self-test
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_bi_consumer_csv import (  # noqa: E402
    BI_CONSUMER_REGISTRY_FIELDNAMES,
    VALID_BI_TIERS,
    VALID_ENGAGEMENT_STREAMS,
    BiConsumerRegistryRow,
)
from pydantic import ValidationError  # noqa: E402

CSV_PATH = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "dimensions/BI_CONSUMER_REGISTRY.csv"
)
MATRIX_CSV = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "techops/COMPONENT_SERVICE_MATRIX.csv"
)
ORG_CSV = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv"
DECISION_CSV = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv"


def _load_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(r.get(key) or "").strip() for r in csv.DictReader(fh) if (r.get(key) or "").strip()}


def validate_csv() -> int:
    errors: list[str] = []
    if not CSV_PATH.is_file():
        print(f"FAIL: missing {CSV_PATH.relative_to(REPO_ROOT)}")
        return 1
    roles = _load_set(ORG_CSV, "role_name")
    decisions = _load_set(DECISION_CSV, "decision_id")
    matrix_ids = _load_set(MATRIX_CSV, "component_id")

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != BI_CONSUMER_REGISTRY_FIELDNAMES:
            errors.append("Header mismatch vs BI_CONSUMER_REGISTRY_FIELDNAMES")
            print("FAIL")
            for e in errors:
                print(f"  - {e}")
            return 1
        seen: set[str] = set()
        for line_no, row in enumerate(reader, start=2):
            cid = row.get("consumer_id", "")
            if cid in seen:
                errors.append(f"L{line_no}: duplicate consumer_id {cid!r}")
            seen.add(cid)
            try:
                BiConsumerRegistryRow.model_validate(row)
            except ValidationError as exc:
                errors.append(f"L{line_no}: Pydantic {exc.errors()[0]['msg']}")
                continue
            tier = (row.get("bi_tier") or "").strip()
            if tier not in VALID_BI_TIERS:
                errors.append(f"L{line_no}: bi_tier {tier!r} not in T1..T10")
            stream = (row.get("engagement_stream") or "").strip()
            if stream not in VALID_ENGAGEMENT_STREAMS:
                errors.append(f"L{line_no}: engagement_stream {stream!r} invalid")
            owner = (row.get("owner_role") or "").strip()
            if owner and owner not in roles:
                errors.append(f"L{line_no}: owner_role {owner!r} not in baseline_organisation")
            comp = (row.get("component_id") or "").strip()
            if comp and matrix_ids and comp not in matrix_ids:
                errors.append(f"L{line_no}: component_id {comp!r} not in COMPONENT_SERVICE_MATRIX")
            did = (row.get("linked_decision_id") or "").strip()
            if did and did not in decisions:
                errors.append(f"L{line_no}: linked_decision_id {did!r} not in DECISION_REGISTER")
            sop = (row.get("paired_sop_path") or "").strip()
            if sop.startswith("docs/") and not (REPO_ROOT / sop).is_file():
                errors.append(f"L{line_no}: paired_sop_path missing: {sop!r}")

    if errors:
        print(f"FAIL ({len(errors)} issues)")
        for e in errors[:30]:
            print(f"  - {e}")
        return 1
    print(f"PASS ({len(seen)} rows)")
    return 0


def run_self_test() -> int:
    sample = {
        "consumer_id": "BI-HOL-SELF-TEST-001",
        "bi_tier": "T1",
        "tool_name": "Self Test Fixture",
        "component_id": "comp_i93_hlk_erp",
        "data_surfaces": "erp.vw_test",
        "status": "planned",
        "paired_sop_path": "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md",
        "engagement_stream": "internal",
        "owner_role": "Data Governance Lead",
        "linked_decision_id": "D-IH-93-I",
        "notes": "fixture",
        "last_review_at": "2026-06-04",
        "last_review_by": "Data Governance Lead",
        "last_review_decision_id": "D-IH-93-I",
        "methodology_version_at_review": "v3.1",
    }
    try:
        BiConsumerRegistryRow.model_validate(sample)
    except ValidationError as exc:
        print(f"FAIL: Pydantic self-test {exc}")
        return 1
    print("PASS (self-test)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate BI_CONSUMER_REGISTRY.csv")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    return validate_csv()


if __name__ == "__main__":
    raise SystemExit(main())
