#!/usr/bin/env python3
"""Validate FINOPS_TAX_CALENDAR.csv (FINANCE-AREA-FULL F2b / OPS-81-13).

Usage::

    py scripts/validate_finops_tax_calendar.py
    py scripts/validate_finops_tax_calendar.py --self-test
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_finops_tax_calendar_csv import (  # noqa: E402
    FINOPS_TAX_CALENDAR_FIELDNAMES,
    FinopsTaxCalendarRow,
)
from pydantic import ValidationError  # noqa: E402

CSV_PATH = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/"
    "dimensions/FINOPS_TAX_CALENDAR.csv"
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


def _load_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(r.get(key) or "").strip() for r in csv.DictReader(fh) if (r.get(key) or "").strip()}


def validate_csv() -> tuple[int, int]:
    errors: list[str] = []
    warnings: list[str] = []
    if not CSV_PATH.is_file():
        print(f"FAIL: missing {CSV_PATH.relative_to(REPO_ROOT)}")
        return 1, 0

    roles = _load_set(ORG_CSV, "role_name")
    decisions = _load_set(DECISION_CSV, "decision_id")

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != FINOPS_TAX_CALENDAR_FIELDNAMES:
            errors.append("Header mismatch vs FINOPS_TAX_CALENDAR_FIELDNAMES")
            print("FAIL")
            for e in errors:
                print(f"  - {e}")
            return 1, 0
        seen: set[str] = set()
        seen_modelo: set[str] = set()
        row_count = 0
        for line_no, row in enumerate(reader, start=2):
            row_count += 1
            oid = (row.get("obligation_id") or "").strip()
            modelo = (row.get("modelo_code") or "").strip()
            if oid in seen:
                errors.append(f"L{line_no}: duplicate obligation_id {oid!r}")
            if modelo in seen_modelo:
                errors.append(f"L{line_no}: duplicate modelo_code {modelo!r}")
            seen.add(oid)
            seen_modelo.add(modelo)
            try:
                FinopsTaxCalendarRow.model_validate(row)
            except ValidationError as exc:
                errors.append(f"L{line_no}: Pydantic {exc.errors()[0]['msg']}")
                continue
            role = (row.get("responsible_role") or "").strip()
            if role and role not in roles:
                errors.append(f"L{line_no}: responsible_role {role!r} not in baseline_organisation")
            did = (row.get("last_review_decision_id") or "").strip()
            if did and did not in decisions:
                errors.append(
                    f"L{line_no}: last_review_decision_id {did!r} not in DECISION_REGISTER"
                )
            for path_key in ("paired_sop_path", "paired_runbook_path"):
                ref = (row.get(path_key) or "").strip()
                if ref.startswith("docs/") or ref.startswith("scripts/"):
                    ref_path = REPO_ROOT / ref.split()[0].split("#")[0]
                    if not ref_path.is_file():
                        errors.append(f"L{line_no}: {path_key} path missing: {ref!r}")
            status = (row.get("status") or "").strip()
            next_due = (row.get("next_due_at") or "").strip()
            if status == "active" and not next_due:
                warnings.append(
                    f"L{line_no}: active row {oid!r} has empty next_due_at "
                    "(expected until entity live; AT-Pymes/counsel confirms)"
                )

    if errors:
        print(f"FAIL ({len(errors)} issues)")
        for e in errors[:30]:
            print(f"  - {e}")
        if len(errors) > 30:
            print(f"  ... and {len(errors) - 30} more")
        return 1, row_count
    for w in warnings[:10]:
        print(f"  [WARN] {w}")
    if len(warnings) > 10:
        print(f"  [WARN] ... and {len(warnings) - 10} more")
    print(f"PASS ({row_count} obligations)")
    return 0, row_count


def run_self_test() -> int:
    sample = {
        "obligation_id": "TAX-FIN-HOL-SELF-TEST",
        "modelo_code": "SELF-TEST",
        "obligation_name": "Self-test obligation",
        "cadence_type": "annual",
        "cadence_rule": "self-test fixture cadence",
        "hacienda_authority": "AEAT_common",
        "applicability_gate": "always",
        "responsible_role": "Business Controller",
        "executor_party": "AT-Pymes gestoria",
        "paired_sop_path": "",
        "paired_runbook_path": "",
        "last_filed_at": "",
        "next_due_at": "",
        "source_ref": "https://sede.agenciatributaria.gob.es/",
        "status": "draft",
        "last_review_at": "2026-06-05",
        "last_review_by": "Business Controller",
        "last_review_decision_id": "D-IH-88-E",
        "methodology_version_at_review": "v3.1",
        "notes": "self-test fixture only",
    }
    try:
        FinopsTaxCalendarRow.model_validate(sample)
    except ValidationError as exc:
        print(f"FAIL: Pydantic self-test {exc}")
        return 1
    print("PASS (self-test)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate FINOPS_TAX_CALENDAR.csv")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run Pydantic fixture self-test without reading the CSV.",
    )
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    rc, _ = validate_csv()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
