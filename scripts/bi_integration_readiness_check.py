#!/usr/bin/env python3
"""BI/integration readiness check (I93 P5b).

Paired canonicals: DATA_BI_GOVERNANCE.md + DATA_INTEGRATION_PLANE.md

Usage::

    py scripts/bi_integration_readiness_check.py --self-test
    py scripts/bi_integration_readiness_check.py --report
    py scripts/bi_integration_readiness_check.py --report --json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_bi_consumer_csv import BI_CONSUMER_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_component_service_csv import COMPONENT_SERVICE_FIELDNAMES  # noqa: E402

BI_CSV = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "dimensions/BI_CONSUMER_REGISTRY.csv"
)
MATRIX_CSV = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "techops/COMPONENT_SERVICE_MATRIX.csv"
)
ERP_VIEWS_SQL = REPO_ROOT / "supabase/migrations/20260506130100_i62_p2_erp_schema_views.sql"
RPA_CSV = REPO_ROOT / (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "dimensions/RPA_ADAPTER_REGISTRY.csv"
)

REQUIRED_MATRIX_COMPONENTS: tuple[str, ...] = (
    "comp_i93_hlk_erp",
    "comp_i93_langfuse",
    "comp_i93_neo4j",
    "comp_i93_openclaw_akos",
    "comp_i93_holistika_edge",
)

REQUIRED_ERP_VIEW_FRAGMENTS: tuple[str, ...] = (
    "erp.vw_mission_control_today",
    "erp.vw_mirror_health",
)

REQUIRED_CANONICALS: tuple[str, ...] = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATA_BI_GOVERNANCE.md",
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATA_INTEGRATION_PLANE.md",
)


def _load_matrix_ids() -> set[str]:
    if not MATRIX_CSV.is_file():
        return set()
    with MATRIX_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != tuple(COMPONENT_SERVICE_FIELDNAMES):
            return set()
        return {(r.get("component_id") or "").strip() for r in reader if r.get("component_id")}


def _load_bi_rows() -> list[dict[str, str]]:
    if not BI_CSV.is_file():
        return []
    with BI_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != BI_CONSUMER_REGISTRY_FIELDNAMES:
            return []
        return list(reader)


def _analyze() -> dict[str, list[dict[str, str]]]:
    findings: dict[str, list[dict[str, str]]] = {
        "missing_canonical": [],
        "missing_erp_views_migration": [],
        "missing_matrix_component": [],
        "bi_consumer_orphan_component": [],
        "missing_rpa_registry": [],
    }
    for rel in REQUIRED_CANONICALS:
        if not (REPO_ROOT / rel).is_file():
            findings["missing_canonical"].append({"path": rel, "detail": "canonical missing"})
    if not ERP_VIEWS_SQL.is_file():
        findings["missing_erp_views_migration"].append(
            {"path": str(ERP_VIEWS_SQL.relative_to(REPO_ROOT)), "detail": "migration missing"}
        )
    else:
        sql_text = ERP_VIEWS_SQL.read_text(encoding="utf-8")
        for frag in REQUIRED_ERP_VIEW_FRAGMENTS:
            if frag not in sql_text:
                findings["missing_erp_views_migration"].append(
                    {"fragment": frag, "detail": "erp view not in migration"}
                )
    matrix_ids = _load_matrix_ids()
    for comp_id in REQUIRED_MATRIX_COMPONENTS:
        if comp_id not in matrix_ids:
            findings["missing_matrix_component"].append(
                {"component_id": comp_id, "detail": "required matrix row missing"}
            )
    for row in _load_bi_rows():
        cid = (row.get("component_id") or "").strip()
        if cid and matrix_ids and cid not in matrix_ids:
            findings["bi_consumer_orphan_component"].append(
                {
                    "consumer_id": row.get("consumer_id", ""),
                    "component_id": cid,
                    "detail": "BI consumer FK not in matrix",
                }
            )
    if not RPA_CSV.is_file():
        findings["missing_rpa_registry"].append({"path": "RPA_ADAPTER_REGISTRY.csv", "detail": "missing"})
    return findings


def run_self_test() -> int:
    findings = _analyze()
    blocking = (
        findings["missing_canonical"]
        + findings["missing_erp_views_migration"]
        + findings["missing_matrix_component"]
        + findings["bi_consumer_orphan_component"]
        + findings["missing_rpa_registry"]
    )
    if blocking:
        print(f"FAIL self-test: {len(blocking)} blocking finding(s)")
        for item in blocking[:8]:
            print(f"  - {item}")
        return 1
    bi_rows = _load_bi_rows()
    if len(bi_rows) < 10:
        print(f"FAIL self-test: expected >=10 BI consumer rows, got {len(bi_rows)}")
        return 1
    print(f"PASS self-test ({len(bi_rows)} BI consumers, matrix + erp views OK)")
    return 0


def run_report(as_json: bool) -> int:
    findings = _analyze()
    summary = {
        "bi_consumer_count": len(_load_bi_rows()),
        "matrix_component_count": len(_load_matrix_ids()),
        "findings": findings,
    }
    blocking = sum(len(v) for v in findings.values())
    if as_json:
        print(json.dumps(summary, indent=2))
    else:
        print("BI Integration Readiness Report")
        print("=" * 40)
        print(f"  BI consumers: {summary['bi_consumer_count']}")
        print(f"  Matrix components: {summary['matrix_component_count']}")
        for category, items in findings.items():
            if items:
                print(f"  {category}: {len(items)}")
                for item in items[:5]:
                    print(f"    - {item}")
    return 1 if blocking else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="BI/integration readiness check (I93 P5b)")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    if args.report:
        return run_report(args.json)
    return run_self_test()


if __name__ == "__main__":
    raise SystemExit(main())
