#!/usr/bin/env python3
"""GOI/POI golden-record integrity report (I93 P5).

Paired SOP: ``SOP-DATA_MASTERDATA_GOLDEN_RECORD_001.md`` (process ``thi_data_dtp_32``)

Usage::

    py scripts/mdm_golden_record_check.py --self-test
    py scripts/mdm_golden_record_check.py --report
    py scripts/mdm_golden_record_check.py --report --json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

GOI_POI_CSV = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv"
)

VALID_CLASSIFICATION = frozenset(
    {"public", "community", "internal", "confidential", "restricted"}
)
GOI_POI_SENSITIVITY = frozenset({"internal", "confidential"})


def _load_rows() -> list[dict[str, str]]:
    if not GOI_POI_CSV.is_file():
        return []
    with GOI_POI_CSV.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _analyze(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    findings: dict[str, list[dict[str, str]]] = {
        "duplicate_ref_id": [],
        "orphan_bridge_via": [],
        "invalid_sensitivity": [],
    }
    ref_ids = {r.get("ref_id", "") for r in rows if r.get("ref_id")}
    seen: dict[str, int] = {}
    for row in rows:
        ref = row.get("ref_id", "")
        if ref:
            seen[ref] = seen.get(ref, 0) + 1
        sens = row.get("sensitivity", "")
        if sens and sens not in GOI_POI_SENSITIVITY:
            findings["invalid_sensitivity"].append(
                {"ref_id": ref, "sensitivity": sens, "detail": "not in GOI/POI enum"}
            )
        bridge = (row.get("bridge_via") or "").strip()
        if bridge and bridge not in ref_ids:
            findings["orphan_bridge_via"].append(
                {"ref_id": ref, "bridge_via": bridge, "detail": "target ref_id missing"}
            )
    for ref, count in seen.items():
        if count > 1:
            findings["duplicate_ref_id"].append(
                {"ref_id": ref, "count": str(count), "detail": "duplicate golden key"}
            )
    return findings


def run_self_test() -> int:
    rows = _load_rows()
    if not rows:
        print("FAIL self-test: GOI_POI_REGISTER.csv missing or empty")
        return 1
    findings = _analyze(rows)
    errors = findings["duplicate_ref_id"] + findings["orphan_bridge_via"]
    if errors:
        print(f"FAIL self-test: {len(errors)} blocking finding(s)")
        for item in errors[:5]:
            print(f"  - {item}")
        return 1
    print(f"PASS self-test ({len(rows)} GOI/POI rows; classification enum OK)")
    return 0


def run_report(as_json: bool = False) -> int:
    rows = _load_rows()
    findings = _analyze(rows)
    summary = {
        "row_count": len(rows),
        "valid_classification_enum": sorted(VALID_CLASSIFICATION),
        "findings": findings,
        "blocking_count": len(findings["duplicate_ref_id"]) + len(findings["orphan_bridge_via"]),
        "warn_count": len(findings["invalid_sensitivity"]),
    }
    if as_json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"GOI/POI golden-record report ({summary['row_count']} rows)")
        print(f"  blocking: {summary['blocking_count']}")
        print(f"  warnings: {summary['warn_count']}")
        for kind, items in findings.items():
            for item in items:
                print(f"  [{kind}] {item}")
    return 1 if summary["blocking_count"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="MDM golden-record check (I93 P5)")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    if args.report:
        return run_report(as_json=args.json)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
