#!/usr/bin/env python3
"""Validate Finance plane-2 registries (FINANCE-AREA-FULL F2a).

Usage::

    py scripts/validate_pricing_tier_registry.py
    py scripts/validate_pricing_tier_registry.py --self-test
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_pricing_tier_registry_csv import (  # noqa: E402
    FINOPS_PERFORMANCE_OBLIGATION_REGISTRY_FIELDNAMES,
    PRICING_TIER_REGISTRY_FIELDNAMES,
    FinopsPerformanceObligationRow,
    PricingTierRegistryRow,
)
from pydantic import ValidationError  # noqa: E402

PRICING_CSV = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/"
    "dimensions/PRICING_TIER_REGISTRY.csv"
)
OBLIGATION_CSV = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/"
    "dimensions/FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv"
)
POLICY_MD = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/canonicals/"
    "FINOPS_REVENUE_RECOGNITION_POLICY.md"
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


def _validate_obligations() -> tuple[int, set[str], list[str]]:
    errors: list[str] = []
    if not OBLIGATION_CSV.is_file():
        return 1, set(), [f"missing {OBLIGATION_CSV.relative_to(REPO_ROOT)}"]
    decisions = _load_set(DECISION_CSV, "decision_id")
    obligation_ids: set[str] = set()
    with OBLIGATION_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != FINOPS_PERFORMANCE_OBLIGATION_REGISTRY_FIELDNAMES:
            return 1, set(), ["FINOPS_PERFORMANCE_OBLIGATION_REGISTRY header mismatch"]
        for line_no, row in enumerate(reader, start=2):
            oid = (row.get("obligation_id") or "").strip()
            if oid in obligation_ids:
                errors.append(f"obligation L{line_no}: duplicate obligation_id {oid!r}")
            obligation_ids.add(oid)
            try:
                FinopsPerformanceObligationRow.model_validate(row)
            except ValidationError as exc:
                errors.append(f"obligation L{line_no}: Pydantic {exc.errors()[0]['msg']}")
                continue
            did = (row.get("last_review_decision_id") or "").strip()
            if did and did not in decisions:
                errors.append(
                    f"obligation L{line_no}: last_review_decision_id {did!r} not in DECISION_REGISTER"
                )
    return (1 if errors else 0), obligation_ids, errors


def validate_csv() -> tuple[int, int]:
    errors: list[str] = []
    obl_rc, obligation_ids, obl_errors = _validate_obligations()
    errors.extend(obl_errors)
    if obl_rc != 0 and not PRICING_CSV.is_file():
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1, 0
    if not PRICING_CSV.is_file():
        errors.append(f"missing {PRICING_CSV.relative_to(REPO_ROOT)}")
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1, 0

    decisions = _load_set(DECISION_CSV, "decision_id")
    policy_text = ""
    if POLICY_MD.is_file():
        policy_text = POLICY_MD.read_text(encoding="utf-8", errors="replace")

    with PRICING_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != PRICING_TIER_REGISTRY_FIELDNAMES:
            errors.append("PRICING_TIER_REGISTRY header mismatch")
            print("FAIL")
            for e in errors:
                print(f"  - {e}")
            return 1, 0
        seen: set[str] = set()
        seen_slugs: set[str] = set()
        row_count = 0
        for line_no, row in enumerate(reader, start=2):
            row_count += 1
            tid = (row.get("pricing_tier_id") or "").strip()
            slug = (row.get("tier_slug") or "").strip()
            if tid in seen:
                errors.append(f"pricing L{line_no}: duplicate pricing_tier_id {tid!r}")
            if slug in seen_slugs:
                errors.append(f"pricing L{line_no}: duplicate tier_slug {slug!r}")
            seen.add(tid)
            seen_slugs.add(slug)
            try:
                PricingTierRegistryRow.model_validate(row)
            except ValidationError as exc:
                errors.append(f"pricing L{line_no}: Pydantic {exc.errors()[0]['msg']}")
                continue
            did = (row.get("last_review_decision_id") or "").strip()
            if did and did not in decisions:
                errors.append(
                    f"pricing L{line_no}: last_review_decision_id {did!r} not in DECISION_REGISTER"
                )
            poid = (row.get("performance_obligation_id") or "").strip()
            if poid and poid not in obligation_ids:
                errors.append(
                    f"pricing L{line_no}: performance_obligation_id {poid!r} "
                    "not in FINOPS_PERFORMANCE_OBLIGATION_REGISTRY"
                )
            if policy_text and poid and poid not in policy_text:
                errors.append(
                    f"pricing L{line_no}: performance_obligation_id {poid!r} "
                    "not cited in FINOPS_REVENUE_RECOGNITION_POLICY.md"
                )
            ref = (row.get("pmo_pricing_model_ref") or "").strip()
            if ref.startswith("docs/"):
                ref_path = REPO_ROOT / ref.split()[0].split("#")[0]
                if not ref_path.is_file():
                    errors.append(f"pricing L{line_no}: pmo_pricing_model_ref path missing: {ref!r}")

    if errors:
        print(f"FAIL ({len(errors)} issues)")
        for e in errors[:30]:
            print(f"  - {e}")
        if len(errors) > 30:
            print(f"  ... and {len(errors) - 30} more")
        return 1, row_count
    print(f"PASS ({row_count} pricing tiers; {len(obligation_ids)} obligations)")
    return 0, row_count


def run_self_test() -> int:
    obligation = {
        "obligation_id": "PO-FIN-HOL-SELF-TEST",
        "obligation_name": "Self-test obligation",
        "ifrs15_pattern": "over_time",
        "recognition_trigger": "self-test fixture",
        "policy_section_ref": "§self-test",
        "status": "draft",
        "last_review_at": "2026-06-05",
        "last_review_by": "Business Controller",
        "last_review_decision_id": "D-IH-88-E",
        "methodology_version_at_review": "v3.1",
        "notes": "self-test fixture only",
    }
    pricing = {
        "pricing_tier_id": "PT-FIN-HOL-SELF-TEST",
        "tier_slug": "self_test",
        "display_name": "Self Test",
        "product_surface": "internal_trial",
        "performance_obligation_id": "PO-FIN-HOL-SELF-TEST",
        "pmo_pricing_model_ref": "",
        "billing_cadence": "n_a",
        "status": "draft",
        "last_review_at": "2026-06-05",
        "last_review_by": "Business Controller",
        "last_review_decision_id": "D-IH-88-E",
        "methodology_version_at_review": "v3.1",
        "notes": "self-test fixture only",
    }
    try:
        FinopsPerformanceObligationRow.model_validate(obligation)
        PricingTierRegistryRow.model_validate(pricing)
    except ValidationError as exc:
        print(f"FAIL: Pydantic self-test {exc}")
        return 1
    print("PASS (self-test)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Finance pricing tier registries")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run Pydantic fixture self-test without reading CSVs.",
    )
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    rc, _ = validate_csv()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
