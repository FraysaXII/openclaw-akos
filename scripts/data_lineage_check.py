#!/usr/bin/env python3
"""Data lineage report + graph parity dry-run (I93 P4).

Paired SOP: ``SOP-DATA_LINEAGE_001.md`` (process ``thi_data_dtp_275``)

Usage::

    py scripts/data_lineage_check.py --self-test
    py scripts/data_lineage_check.py --report
    py scripts/data_lineage_check.py --report --json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_data_contract_csv import CSV_PATH_RELATIVE as CONTRACT_CSV_REL
from akos.hlk_graph_model import assert_graph_registry_parity, build_hlk_csv_graph
from akos.hlk import get_hlk_registry

CONTRACT_CSV = REPO_ROOT / CONTRACT_CSV_REL

TIER_BY_SURFACE: dict[str, str] = {
    "canonical_csv": "T1-git",
    "mirror_table": "T2-supabase",
    "fdw_projection": "T2-supabase",
    "graph": "T3-neo4j",
}


def _load_contracts() -> list[dict[str, str]]:
    if not CONTRACT_CSV.is_file():
        return []
    with CONTRACT_CSV.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def run_self_test() -> int:
    chains = _build_lineage_chains(_load_contracts())
    if not chains:
        print("FAIL self-test: no contract rows")
        return 1
    reg = get_hlk_registry()
    nodes, edges = build_hlk_csv_graph(reg)
    try:
        assert_graph_registry_parity(reg, nodes, edges)
    except ValueError as exc:
        print(f"FAIL self-test parity: {exc}")
        return 1
    print("PASS self-test (lineage chains + graph parity)")
    return 0


def _build_lineage_chains(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        surface = (row.get("data_surface") or "").strip()
        out.append({
            "contract_id": row.get("contract_id", ""),
            "producer_process_id": row.get("producer_process_id", ""),
            "data_surface": surface,
            "tier": TIER_BY_SURFACE.get(surface, "unknown"),
            "schema_ref": row.get("schema_ref", ""),
            "status": row.get("status", ""),
            "sync_path": _sync_path_for_surface(surface),
        })
    return out


def _sync_path_for_surface(surface: str) -> str:
    mapping = {
        "canonical_csv": "git SSOT (authoritative)",
        "mirror_table": "supabase/migrations + compliance_mirror_emit",
        "fdw_projection": "FDW server DDL + finops runbooks",
        "graph": "scripts/sync_hlk_neo4j.py",
    }
    return mapping.get(surface, "document in DATA_ARCHITECTURE.md")


def run_report(as_json: bool) -> int:
    rows = _load_contracts()
    chains = _build_lineage_chains(rows)
    reg = get_hlk_registry()
    nodes, edges = build_hlk_csv_graph(reg)
    parity_ok = True
    parity_error = ""
    try:
        assert_graph_registry_parity(reg, nodes, edges)
    except ValueError as exc:
        parity_ok = False
        parity_error = str(exc)

    payload = {
        "contract_chains": chains,
        "graph_parity_ok": parity_ok,
        "graph_parity_error": parity_error,
        "graph_role_nodes": sum(1 for n in nodes if n.label == "Role"),
        "graph_process_nodes": sum(1 for n in nodes if n.label == "Process"),
        "graph_edge_count": len(edges),
    }
    if as_json:
        print(json.dumps(payload, indent=2))
        return 0 if parity_ok else 1

    print("Data lineage report (I93 P4)")
    print(f"  Active contract surfaces: {len(chains)}")
    for chain in chains:
        print(
            f"  - {chain['contract_id']}: {chain['tier']} "
            f"({chain['data_surface']}) -> {chain['sync_path']}"
        )
    if parity_ok:
        print(
            f"  Graph parity: PASS "
            f"(roles={payload['graph_role_nodes']} "
            f"processes={payload['graph_process_nodes']} "
            f"edges={payload['graph_edge_count']})"
        )
    else:
        print(f"  Graph parity: FAIL — {parity_error}")
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Data lineage check (I93 P4)")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    if args.report:
        return run_report(as_json=args.json)
    parser.error("Specify --self-test or --report")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
