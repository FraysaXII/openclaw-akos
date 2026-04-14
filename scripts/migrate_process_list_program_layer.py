#!/usr/bin/env python3
"""Insert Pattern 3 program workstreams (hlk_prog_*) and re-parent selected GTM workstreams.

Reads and writes docs/references/hlk/compliance/process_list.csv. Idempotent: safe to
re-run when program rows already exist.

Usage (repo root):
    py scripts/migrate_process_list_program_layer.py
    py scripts/migrate_process_list_program_layer.py --write
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_process_csv import PROCESS_LIST_FIELDNAMES, normalize_process_row, resolve_all_parent_ids, write_process_csv

PROC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "process_list.csv"

PROJ_MADEIRA = "MADEIRA Platform"
PROJ_THINK = "Think Big Operational Excellence"

PROG_PRODUCT = "MADEIRA product and research program"
PROG_ENG = "MADEIRA engineering and UX program"
PROG_THINK = "Think Big PMO and operating model program"

PROGRAM_SPECS: list[tuple[str, str, str, str, str, str, str, str, str]] = [
    (
        "hlk_prog_madeira_product_research",
        PROG_PRODUCT,
        PROJ_MADEIRA,
        "HLK Tech Lab",
        "Tech",
        "CTO",
        "AI Engineer",
        "Groups MADEIRA radar, product planning, sales collateral, and benchmarking workstreams under one program.",
        "Pattern 3 program layer; see docs/wip/planning/02-hlk-on-akos-madeira/reports/trello-list-to-workstream-matrix.md",
    ),
    (
        "hlk_prog_madeira_engineering_ux",
        PROG_ENG,
        PROJ_MADEIRA,
        "HLK Tech Lab",
        "Tech",
        "CTO",
        "AI Engineer",
        "Groups MADEIRA UX capability and DevOps/CI/CD delivery workstreams.",
        "Pattern 3 program layer; see trello-list-to-workstream-matrix.md",
    ),
    (
        "hlk_prog_think_big_pmo",
        PROG_THINK,
        PROJ_THINK,
        "Think Big",
        "Operations",
        "COO",
        "PMO",
        "Groups PMO-aligned GTM operating workstreams (services, GTM entity, internal controls). Engage stays a direct child of the project.",
        "Pattern 3 program layer; see trello-list-to-workstream-matrix.md",
    ),
]

CHILD_PROGRAM: dict[str, str] = {
    "gtm_ws_madeira_radar": PROG_PRODUCT,
    "gtm_ws_madeira_planning": PROG_PRODUCT,
    "gtm_ws_madeira_sales": PROG_PRODUCT,
    "gtm_ws_madeira_benchmark": PROG_PRODUCT,
    "gtm_ws_madeira_ux": PROG_ENG,
    "gtm_ws_madeira_devops": PROG_ENG,
    "gtm_ws_gtm_entity": PROG_THINK,
    "gtm_ws_service_catalog": PROG_THINK,
    "gtm_ws_ops_control": PROG_THINK,
}


def load_rows() -> tuple[list[str], list[dict[str, str]]]:
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = [dict(r) for r in reader]
    return fieldnames, rows


def program_dict(
    item_id: str,
    item_name: str,
    project: str,
    entity: str,
    area: str,
    role_parent: str,
    role_owner: str,
    description: str,
    addendum: str,
) -> dict[str, str]:
    row = {k: "" for k in PROCESS_LIST_FIELDNAMES}
    row.update(
        {
            "type": "Internal",
            "orientation": "Employee",
            "entity": entity,
            "area": area,
            "role_parent_1": role_parent,
            "role_owner": role_owner,
            "item_parent_2_id": "",
            "item_parent_2": project,
            "item_parent_1_id": "",
            "item_parent_1": project,
            "item_name": item_name,
            "item_id": item_id,
            "item_granularity": "workstream",
            "time_hours_par": "",
            "description": description,
            "instructions": "",
            "addundum_extras": addendum,
            "confidence": "2",
            "count_name": "1",
            "frequency": "high",
            "quality": "3",
        }
    )
    return row


def _rewire_children(rows: list[dict[str, str]]) -> int:
    n = 0
    names = {(r.get("item_name") or "").strip() for r in rows}
    for prog_name in {CHILD_PROGRAM[i] for i in CHILD_PROGRAM}:
        if prog_name not in names:
            print(f"error: program {prog_name!r} not in item_name set", file=sys.stderr)
            sys.exit(1)
    for r in rows:
        iid = (r.get("item_id") or "").strip()
        if iid not in CHILD_PROGRAM:
            continue
        prog = CHILD_PROGRAM[iid]
        if (r.get("item_parent_1") or "").strip() == prog and (r.get("item_parent_2") or "").strip() == prog:
            continue
        r["item_parent_1"] = prog
        r["item_parent_2"] = prog
        n += 1
    return n


def migrate(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, int]]:
    stats = {"programs_added": 0, "children_rewired": 0}
    by_id = {(r.get("item_id") or "").strip(): r for r in rows}

    to_add_madeira: list[dict[str, str]] = []
    to_add_think: list[dict[str, str]] = []
    for spec in PROGRAM_SPECS:
        iid, iname, proj, ent, ar, rp, ro, desc, add = spec
        if iid in by_id:
            continue
        pr = program_dict(iid, iname, proj, ent, ar, rp, ro, desc, add)
        if proj == PROJ_MADEIRA:
            to_add_madeira.append(pr)
        else:
            to_add_think.append(pr)
        stats["programs_added"] += 1

    out: list[dict[str, str]] = []
    inserted_madeira = False
    inserted_think = False
    for r in rows:
        iid = (r.get("item_id") or "").strip()
        out.append(r)
        if iid == "env_tech_prj_3" and to_add_madeira and not inserted_madeira:
            out.extend([{k: pr.get(k, "") for k in PROCESS_LIST_FIELDNAMES} for pr in to_add_madeira])
            inserted_madeira = True
        if iid == "thi_opera_prj_1" and to_add_think and not inserted_think:
            out.extend([{k: pr.get(k, "") for k in PROCESS_LIST_FIELDNAMES} for pr in to_add_think])
            inserted_think = True

    if to_add_madeira and not inserted_madeira:
        print("error: env_tech_prj_3 (MADEIRA Platform) not found; cannot insert MADEIRA programs", file=sys.stderr)
        return rows, stats
    if to_add_think and not inserted_think:
        print("error: thi_opera_prj_1 not found; cannot insert Think Big program", file=sys.stderr)
        return rows, stats

    stats["children_rewired"] = _rewire_children(out)
    return out, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    _fieldnames, rows = load_rows()
    new_rows, stats = migrate([dict(r) for r in rows])
    print(f"programs_added={stats['programs_added']} children_rewired={stats['children_rewired']}")
    if not args.write:
        print("Dry run: pass --write to apply.")
        return 0
    fixed = resolve_all_parent_ids([normalize_process_row(r) for r in new_rows])
    write_process_csv(PROC_CSV, fixed)
    print("Wrote", PROC_CSV)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
