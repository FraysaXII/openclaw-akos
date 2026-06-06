#!/usr/bin/env python3
"""Data contract registry coverage + forward-mirror gap report (I93 P2b).

Paired SOP: ``SOP-DATA_CONTRACT_REGISTRY_MAINTENANCE_001.md``

Usage::

    py scripts/data_contract_registry_check.py --self-test
    py scripts/data_contract_registry_check.py --coverage-report
    py scripts/data_contract_registry_check.py --coverage-report --json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_data_contract_csv import (  # noqa: E402
    CSV_PATH_RELATIVE,
    DATA_CONTRACT_REGISTRY_FIELDNAMES,
    DataContractRegistryRow,
)

CSV_PATH = REPO_ROOT / CSV_PATH_RELATIVE

# OPS-86-15 gap CSVs without mirror DDL (from cross-area-data-map-2026-06-04.md)
OPS_86_15_GAP_CSVS: tuple[str, ...] = (
    "AIC_REGISTRY.csv",
    "AUDIENCE_REGISTRY.csv",
    "CAPABILITY_REGISTRY.csv",
    "CAPABILITY_CONFIDENCE_REGISTRY.csv",
    "COUNTRY_WORK_CALENDAR.csv",
)

DATA_FAM_SEED_FAMILIES: tuple[str, ...] = (
    "COMPLIANCE-MIRROR",
    "ENGAGEMENT-FACT",
    "GTM-CRM",
)

P6_FAMILY_TARGET = 7
MAPPED_PROCESS_TARGET = 115  # cross-area-data-map heuristic count


def _load_rows() -> list[dict[str, str]]:
    if not CSV_PATH.is_file():
        return []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def run_self_test() -> int:
    sample = {
        "contract_id": "DC-HOL-SELF-TEST-001",
        "producer_process_id": "env_tech_dtp_dataops_quality_001",
        "producer_area": "Tech",
        "consumer_area_ids": "Data",
        "data_surface": "mirror_table",
        "schema_ref": "compliance.example_mirror",
        "semantics_ref": "self-test",
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
        "notes": "self-test",
    }
    DataContractRegistryRow.model_validate(sample)
    if tuple(DATA_CONTRACT_REGISTRY_FIELDNAMES) != DATA_CONTRACT_REGISTRY_FIELDNAMES:
        print("FAIL: fieldnames tuple drift")
        return 1
    print("PASS (self-test)")
    return 0


def build_coverage_report() -> dict[str, object]:
    rows = _load_rows()
    active = [r for r in rows if (r.get("status") or "").strip() == "active"]
    draft = [r for r in rows if (r.get("status") or "").strip() == "draft"]
    forward = [
        r for r in rows
        if "forward" in (r.get("notes") or "").lower()
        or "not minted" in (r.get("notes") or "").lower()
    ]
    by_surface: dict[str, int] = {}
    for r in rows:
        surf = (r.get("data_surface") or "unknown").strip()
        by_surface[surf] = by_surface.get(surf, 0) + 1

    families_in_notes = []
    for r in rows:
        notes = r.get("notes") or ""
        for fam in DATA_FAM_SEED_FAMILIES:
            if fam in notes and fam not in families_in_notes:
                families_in_notes.append(fam)

    return {
        "registry_path": CSV_PATH_RELATIVE,
        "total_rows": len(rows),
        "active_rows": len(active),
        "draft_rows": len(draft),
        "forward_declaration_rows": len(forward),
        "by_data_surface": by_surface,
        "data_fam_families_with_seeds": families_in_notes,
        "data_fam_families_target_p6": P6_FAMILY_TARGET,
        "mapped_processes_target_p6": MAPPED_PROCESS_TARGET,
        "coverage_posture": "seed_only",
        "ops_86_15_gap_csvs": list(OPS_86_15_GAP_CSVS),
        "recommendation": (
            "P2/P2b machinery complete; bulk contract rows land in P6 DATA-FAM tranches. "
            "Run validate_data_contract_registry.py before every CSV edit."
        ),
    }


def run_coverage_report(*, as_json: bool = False) -> int:
    report = build_coverage_report()
    if as_json:
        print(json.dumps(report, indent=2))
        return 0
    print("DATA_CONTRACT_REGISTRY coverage report (I93 P2b)")
    print(f"  path: {report['registry_path']}")
    print(f"  rows: total={report['total_rows']} active={report['active_rows']} draft={report['draft_rows']}")
    print(f"  forward declarations: {report['forward_declaration_rows']}")
    print(f"  by data_surface: {report['by_data_surface']}")
    print(f"  DATA-FAM seeds present: {report['data_fam_families_with_seeds']} (target {P6_FAMILY_TARGET} at P6)")
    print(f"  mapped processes (P6 target): ~{MAPPED_PROCESS_TARGET}")
    print(f"  OPS-86-15 gap CSVs (mirror DDL pending): {', '.join(OPS_86_15_GAP_CSVS)}")
    print(f"  posture: {report['coverage_posture']}")
    print(f"  recommendation: {report['recommendation']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Data contract registry coverage check")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--coverage-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    if args.coverage_report:
        return run_coverage_report(as_json=args.json)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
