#!/usr/bin/env python3
"""Validate AREA_BI_PROFILE.csv (Initiative 93 P5c).

Usage::

    py scripts/validate_area_bi_profile.py
    py scripts/validate_area_bi_profile.py --self-test
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_area_bi_profile_csv import (  # noqa: E402
    AREA_BI_PROFILE_FIELDNAMES,
    AreaBiProfileRow,
)
from akos.hlk_bi_consumer_csv import VALID_BI_TIERS  # noqa: E402
from pydantic import ValidationError  # noqa: E402

CSV_PATH = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "dimensions/AREA_BI_PROFILE.csv"
)
BI_CONSUMER_CSV = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "dimensions/BI_CONSUMER_REGISTRY.csv"
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
    consumer_ids = _load_set(BI_CONSUMER_CSV, "consumer_id")

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != AREA_BI_PROFILE_FIELDNAMES:
            errors.append("Header mismatch vs AREA_BI_PROFILE_FIELDNAMES")
            print("FAIL")
            for e in errors:
                print(f"  - {e}")
            return 1
        seen: set[str] = set()
        for line_no, row in enumerate(reader, start=2):
            aid = row.get("area_id", "")
            if aid in seen:
                errors.append(f"L{line_no}: duplicate area_id {aid!r}")
            seen.add(aid)
            try:
                AreaBiProfileRow.model_validate(row)
            except ValidationError as exc:
                errors.append(f"L{line_no}: Pydantic {exc.errors()[0]['msg']}")
                continue
            steward = (row.get("steward_role") or "").strip()
            if steward and steward not in roles:
                errors.append(f"L{line_no}: steward_role {steward!r} not in baseline_organisation")
            for tier in (row.get("primary_bi_tiers") or "").split(","):
                t = tier.strip()
                if t and t not in VALID_BI_TIERS:
                    errors.append(f"L{line_no}: bi tier {t!r} invalid")
            did = (row.get("linked_decision_id") or "").strip()
            if did and did not in decisions:
                errors.append(f"L{line_no}: linked_decision_id {did!r} not in DECISION_REGISTER")
            for cid in (row.get("primary_consumer_ids") or "").split(";"):
                c = cid.strip()
                if c and consumer_ids and c not in consumer_ids:
                    errors.append(f"L{line_no}: consumer_id {c!r} not in BI_CONSUMER_REGISTRY")
            sop = (row.get("paired_sop_family") or "").strip()
            if sop.startswith("docs/") and not (REPO_ROOT / sop).is_file():
                errors.append(f"L{line_no}: paired_sop_family missing: {sop!r}")

    if errors:
        print(f"FAIL ({len(errors)} issues)")
        for e in errors[:30]:
            print(f"  - {e}")
        return 1
    print(f"PASS ({len(seen)} rows)")
    return 0


def run_self_test() -> int:
    sample = {
        "area_id": "Marketing",
        "steward_role": "Marketing Analytics Manager",
        "primary_bi_tiers": "T4",
        "default_engagement_stream": "internal",
        "analytics_buckets_posture": "operator_production",
        "primary_consumer_ids": "BI-HOL-METABASE",
        "paired_sop_family": "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATA_BI_GOVERNANCE.md",
        "contract_obligation": "required",
        "status": "active",
        "linked_decision_id": "D-IH-93-I",
        "notes": "fixture",
        "last_review_at": "2026-06-04",
        "last_review_by": "Data Governance Lead",
        "last_review_decision_id": "D-IH-93-I",
        "methodology_version_at_review": "v3.1",
    }
    try:
        AreaBiProfileRow.model_validate(sample)
    except ValidationError as exc:
        print(f"FAIL: Pydantic self-test {exc}")
        return 1
    print("PASS (self-test)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AREA_BI_PROFILE.csv")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    return validate_csv()


if __name__ == "__main__":
    raise SystemExit(main())
