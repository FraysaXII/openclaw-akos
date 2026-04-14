#!/usr/bin/env python3
"""Merge GTM candidate process rows into canonical process_list.csv.

Implements docs/wip planning: Trello-aligned English parents, Tier C exclusion,
org alignment, and metadata backfill. Run from repo root:

    py scripts/merge_gtm_into_process_list.py --write

Default is dry-run (prints counts only). Use --write to overwrite process_list.csv.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_process_csv import normalize_process_row, resolve_all_parent_ids, write_process_csv

PROC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "process_list.csv"
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "baseline_organisation.csv"
CANDIDATE_CSV = (
    REPO_ROOT / "docs" / "wip" / "planning" / "02-hlk-on-akos-madeira" / "candidate_gtm_process_rows.csv"
)

# Canonical English parents (must match existing or new row item_name exactly)
WS_RESEARCH_MAT = "Research material and learning pipelines"
PROC_PIPELINE = "Research material pipeline execution"
WS_M_RADAR = "MADEIRA research radar topics"
WS_M_PLAN = "MADEIRA product planning and PO timeline"
WS_M_SALES = "MADEIRA sales tools and collateral"
WS_M_UX = "MADEIRA UX capability definitions"
WS_M_DEVOPS = "MADEIRA DevOps and CI/CD delivery"
WS_M_BENCH = "MADEIRA benchmarking and AI ethics"
WS_BRAND = "Brand presence and messaging"
WS_TEAM = "Team growth and talent pathways"
WS_GTM_ENT = "Go-to-market and entity readiness"
WS_SVC = "Service catalog and capability definition"
WS_OPS_CTL = "Operating model and internal controls"

PROJ_HOL_RESEA = "Holistika Research and Methodology"
PROJ_MADEIRA = "MADEIRA Platform"
PROJ_THI_OP = "Think Big Operational Excellence"
PROJ_THI_MKT = "Think Big Channel and Marketing Operations"
PROJ_HOL_PEO = "Holistika People and Organisational Development"


def load_org_roles() -> dict[str, tuple[str, str, str]]:
    """role_name -> (entity, area, reports_to role_name for role_parent_1)."""
    out: dict[str, tuple[str, str, str]] = {}
    with open(ORG_CSV, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            name = (row.get("role_name") or "").strip()
            if not name:
                continue
            ent = (row.get("entity") or "").strip()
            area = (row.get("area") or "").strip()
            rto = (row.get("reports_to") or "").strip()
            # Map legacy reports_to label to canonical process_list role_parent style
            parent = rto
            if rto == "O5-1":
                parent = "05-1"
            if name == "05-1":
                parent = "Admin"
            out[name] = (ent, area, parent)
    return out


def exclude_row(row: dict[str, str]) -> bool:
    iid = (row.get("item_id") or "").strip()
    if iid.startswith("gtm_backlog"):
        return True
    p1 = (row.get("item_parent_1") or "").strip()
    p2 = (row.get("item_parent_2") or "").strip()
    if p1 == "To Do" or p2 == "To Do" or p1 == "ToDo" or p2 == "ToDo":
        return True
    if p2 == "To Do" or p2 == "ToDo":
        return True
    return False


def _bag(row: dict[str, str]) -> str:
    return f"{row.get('item_parent_1','')}|{row.get('item_parent_2','')}|{row.get('item_name','')}".lower()


def resolve_canonical_parent(row: dict[str, str]) -> str | None:
    """Return item_parent_1 target item_name, or None if excluded."""
    if exclude_row(row):
        return None
    p1 = (row.get("item_parent_1") or "").strip()
    p2 = (row.get("item_parent_2") or "").strip()
    pl = p1.lower()
    p2l = p2.lower()
    bag = _bag(row)

    # MADEIRA first when explicit in p2 (avoid accidental research branch)
    if p2 == "MADEIRA Project" or "madeira project" in bag:
        if "benchmark" in pl or "ai ethics" in pl or "benchmarker" in pl:
            return WS_M_BENCH
        if any(
            x in pl
            for x in (
                "devops",
                "cicd",
                "llamaindex",
                "code structure",
                "pipeline",
                "madeira.py",
                "personality_manager",
            )
        ):
            return WS_M_DEVOPS
        if any(
            x in pl
            for x in (
                "product owner - ux",
                "capabilities",
                "persona",
                "use cases",
                "madeira components",
                "kirbe components",
                "text-to-speech",
                "text-to-text",
                "accessible",
            )
        ):
            return WS_M_UX
        if "sales tools" in pl or "prospect presentation" in pl or "competitive positioning" in pl:
            return WS_M_SALES
        if "research - topics" in pl or "topics on radar" in pl:
            return WS_M_RADAR
        if any(
            x in pl
            for x in (
                "pmo - product",
                "planning phase",
                "product timeline",
                "launch plan",
                "business case",
                "pest",
                "pricing strategy",
                "target metrics",
            )
        ):
            return WS_M_PLAN
        return WS_M_PLAN

    # Research material (Trello list + pipeline)
    if p2 == "Research Material" or pl.startswith("research material"):
        if "pipeline" in pl or p1 == "Research Material / Pipeline":
            return PROC_PIPELINE
        return WS_RESEARCH_MAT

    # Spanish Trello lists (p2 or standalone p1)
    if "darnos" in p2l or p1 == "Darnos a conocer" or pl.startswith("darnos a conocer"):
        return WS_BRAND
    if "crecer equipo" in p2l or p2 == "Crecer equipo" or pl.startswith("crecer equipo"):
        return WS_TEAM
    if "salir a mercado" in p2l or p2 == "Salir a mercado" or pl.startswith("salir a mercado"):
        return WS_GTM_ENT
    if p2 == "Definir servicios" or "definir servicios" in p2l:
        return WS_SVC
    if p2 == "Controlar la empresa" or "controlar la empresa" in p2l:
        return WS_OPS_CTL

    # PMO long paths: infer from Spanish fragments in p1
    if "definir servicios" in pl or p2 == "Definir servicios":
        return WS_SVC
    if "controlar la empresa" in pl or "documentar infraestructura" in pl or "conocer el end to end" in pl:
        return WS_OPS_CTL
    if "salir a mercado" in pl or "establecer sociedad" in pl:
        return WS_GTM_ENT

    # Fallback: AI Engineer rows without MADEIRA in path -> planning
    if (row.get("role_owner") or "").strip() == "AI Engineer":
        return WS_M_PLAN
    if (row.get("role_owner") or "").strip() == "PMO":
        return WS_SVC
    return WS_OPS_CTL


def role_context(role_owner: str, org: dict[str, tuple[str, str, str]]) -> tuple[str, str, str]:
    """entity, area, role_parent_1 for process_list conventions."""
    if role_owner not in org:
        return ("Holistika", "Operations", "COO")
    ent, area, parent = org[role_owner]
    # process_list uses functional titles; fix O5-1 style
    if parent == "O5-1":
        parent = "05-1"
    # CMO/PMO/CPO etc. already have sensible parents from org
    if role_owner == "Holistik Researcher":
        parent = "Holistik Researcher"
    if role_owner == "AI Engineer":
        parent = "CTO"
        ent, area = "HLK Tech Lab", "Tech"
    if role_owner == "PMO":
        parent = "COO"
        ent, area = "Think Big", "Operations"
    if role_owner == "CMO":
        parent = "CMO"
        ent, area = "Think Big", "MKT"
    if role_owner == "CPO":
        parent = "People"
        ent, area = "Holistika", "People"
    return ent, area, parent


def build_description(row: dict[str, str], canon_parent: str, *, final_item_name: str) -> tuple[str, str, str]:
    """description, instructions, addundum_extras."""
    raw_desc = (row.get("description") or "").strip()
    raw_instr = (row.get("instructions") or "").strip()
    legacy = f"Original Trello path: item_parent_2={row.get('item_parent_2','')!r}; item_parent_1={row.get('item_parent_1','')!r}."
    if raw_desc:
        desc = raw_desc[:1800]
    else:
        desc = (
            f"Holistika GTM operating item (promoted from PMO board 67697e19). "
            f"Canonical parent workstream: {canon_parent}. "
            f"Scope: {final_item_name[:200]}."
        )
    instr = raw_instr[:4000] if raw_instr else ""
    add = legacy[:500]
    return desc, instr, add


def default_meta(gran: str) -> tuple[str, str, str, str]:
    if gran == "task":
        return ("2", "1", "medium", "3")
    if gran == "process":
        return ("2", "1", "medium", "3")
    return ("2", "1", "high", "3")


def new_container_rows() -> list[dict[str, str]]:
    """Workstreams, one process, anchor process — all with metadata."""
    rows: list[dict[str, str]] = []

    def ws(
        name: str,
        project: str,
        role_owner: str,
        role_parent: str,
        entity: str,
        area: str,
        iid: str,
        desc: str,
    ) -> dict[str, str]:
        conf, cn, fq, ql = default_meta("workstream")
        return {
            "type": "Internal",
            "orientation": "Employee",
            "entity": entity,
            "area": area,
            "role_parent_1": role_parent,
            "role_owner": role_owner,
            "item_parent_2": project,
            "item_parent_1": project,
            "item_name": name,
            "item_id": iid,
            "item_granularity": "workstream",
            "time_hours_par": "",
            "description": desc,
            "instructions": "",
            "addundum_extras": "Source: Trello list harmonization matrix (planning/02-hlk-on-akos-madeira/reports).",
            "confidence": conf,
            "count_name": cn,
            "frequency": fq,
            "quality": ql,
        }

    def proc(
        name: str,
        parent: str,
        role_owner: str,
        role_parent: str,
        entity: str,
        area: str,
        iid: str,
        desc: str,
    ) -> dict[str, str]:
        conf, cn, fq, ql = default_meta("process")
        return {
            "type": "Internal",
            "orientation": "Employee",
            "entity": entity,
            "area": area,
            "role_parent_1": role_parent,
            "role_owner": role_owner,
            "item_parent_2": PROJ_HOL_RESEA,
            "item_parent_1": parent,
            "item_name": name,
            "item_id": iid,
            "item_granularity": "process",
            "time_hours_par": "",
            "description": desc,
            "instructions": "",
            "addundum_extras": "",
            "confidence": conf,
            "count_name": cn,
            "frequency": fq,
            "quality": ql,
        }

    rows.append(
        ws(
            WS_RESEARCH_MAT,
            PROJ_HOL_RESEA,
            "Holistik Researcher",
            "Holistik Researcher",
            "Holistika",
            "Research",
            "gtm_ws_research_material",
            "Learning tracks, playlists, and ingestion paths for research material aligned with Holistika Research methodology.",
        )
    )
    rows.append(
        proc(
            PROC_PIPELINE,
            WS_RESEARCH_MAT,
            "Holistik Researcher",
            "Holistik Researcher",
            "Holistika",
            "Research",
            "gtm_proc_research_pipeline",
            "Pipeline tasks: build process, gather channels, integrate into MADEIRA, scrape channels, data governance, KMS UI.",
        )
    )

    madeira_owner = "AI Engineer"
    madeira_rp = "CTO"
    madeira_ent = "HLK Tech Lab"
    madeira_area = "Tech"
    for name, iid, desc in (
        (
            WS_M_RADAR,
            "gtm_ws_madeira_radar",
            "Thematic research radar (political, social, technology, legal, economics) for MADEIRA context building.",
        ),
        (
            WS_M_PLAN,
            "gtm_ws_madeira_planning",
            "Product owner timeline: planning phase, business case, launch plan, metrics, pricing, positioning.",
        ),
        (
            WS_M_SALES,
            "gtm_ws_madeira_sales",
            "Sales collateral: prospect decks, demos, competitive positioning, FAQs.",
        ),
        (
            WS_M_UX,
            "gtm_ws_madeira_ux",
            "UX capability definitions: persona, accessibility, use cases, MADEIRA and KiRBe component surfaces.",
        ),
        (
            WS_M_DEVOPS,
            "gtm_ws_madeira_devops",
            "CI/CD, LlamaIndex modules, repository and code structure for MADEIRA delivery.",
        ),
        (
            WS_M_BENCH,
            "gtm_ws_madeira_benchmark",
            "Benchmarking and AI ethics workstreams for MADEIRA.",
        ),
    ):
        rows.append(ws(name, PROJ_MADEIRA, madeira_owner, madeira_rp, madeira_ent, madeira_area, iid, desc))

    rows.append(
        ws(
            WS_BRAND,
            PROJ_THI_MKT,
            "CMO",
            "CMO",
            "Think Big",
            "MKT",
            "gtm_ws_brand_presence",
            "Brand messaging, web and LinkedIn channels, paid media, editorial calendar (Trello: Darnos a conocer).",
        )
    )
    rows.append(
        ws(
            WS_TEAM,
            PROJ_HOL_PEO,
            "CPO",
            "People",
            "Holistika",
            "People",
            "gtm_ws_team_growth",
            "Team growth: training outputs, role fit gaps, career plans (Trello: Crecer equipo).",
        )
    )
    for name, iid, desc in (
        (
            WS_GTM_ENT,
            "gtm_ws_gtm_entity",
            "Entity formation, financial control, FTE optimization for go-to-market (Trello: Salir a mercado).",
        ),
        (
            WS_SVC,
            "gtm_ws_service_catalog",
            "Service definition: capability inventory, market demand, documented service processes (Trello: Definir servicios).",
        ),
        (
            WS_OPS_CTL,
            "gtm_ws_ops_control",
            "Operating model: infrastructure documentation, end-to-end understanding, intelligence absorption (Trello: Controlar la empresa).",
        ),
    ):
        rows.append(ws(name, PROJ_THI_OP, "PMO", "COO", "Think Big", "Operations", iid, desc))

    # Anchor process under Engage workstream
    rows.append(
        {
            "type": "Internal",
            "orientation": "Employee",
            "entity": "Think Big",
            "area": "Operations",
            "role_parent_1": "COO",
            "role_owner": "PMO",
            "item_parent_2": PROJ_THI_OP,
            "item_parent_1": "Engage",
            "item_name": "PMO vault promotion gate",
            "item_id": "gtm_pm_st_promo",
            "item_granularity": "process",
            "time_hours_par": "",
            "description": (
                "Governed path from Trello/WIP to process_list.csv. "
                "See docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-PMO_VAULT_PROMOTION_GATE_001.md."
            ),
            "instructions": "Follow SOP-PMO_VAULT_PROMOTION_GATE_001 before merging registry tranches.",
            "addundum_extras": "Planning matrix: docs/wip/planning/02-hlk-on-akos-madeira/reports/trello-list-to-workstream-matrix.md",
            "confidence": "2",
            "count_name": "1",
            "frequency": "medium",
            "quality": "3",
        }
    )
    return rows


def disambiguate_item_name(name: str, used: set[str]) -> str:
    base = name.strip() or "GTM item"
    if base not in used:
        return base
    n = 2
    while f"{base} ({n})" in used:
        n += 1
    return f"{base} ({n})"


def transform_candidate_rows(
    candidates: list[dict[str, str]],
    org: dict[str, tuple[str, str, str]],
    existing_names: set[str],
) -> list[dict[str, str]]:
    used_names = set(existing_names)
    out: list[dict[str, str]] = []
    for row in candidates:
        parent = resolve_canonical_parent(row)
        if parent is None:
            continue
        ro = (row.get("role_owner") or "").strip()
        ent, area, rp = role_context(ro, org)
        gran = (row.get("item_granularity") or "task").strip().lower()
        if gran not in ("task", "process", "workstream"):
            gran = "task"
        iname = (row.get("item_name") or "").strip()
        final_name = disambiguate_item_name(iname, used_names)
        used_names.add(final_name)
        desc, instr, add = build_description(row, parent, final_item_name=final_name)
        conf, cn, fq, ql = default_meta(gran)
        out.append(
            {
                "type": "Internal",
                "orientation": "Employee",
                "entity": ent,
                "area": area,
                "role_parent_1": rp,
                "role_owner": ro,
                "item_parent_2": "",
                "item_parent_1": parent,
                "item_name": final_name,
                "item_id": (row.get("item_id") or "").strip(),
                "item_granularity": gran,
                "time_hours_par": (row.get("time_hours_par") or "").strip(),
                "description": desc,
                "instructions": instr,
                "addundum_extras": add[:1500],
                "confidence": conf,
                "count_name": cn,
                "frequency": fq,
                "quality": ql,
            }
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Overwrite process_list.csv")
    args = parser.parse_args()

    org = load_org_roles()
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        existing = list(csv.DictReader(f))
    existing_ids = {r["item_id"].strip() for r in existing if r.get("item_id")}
    existing_names = {r["item_name"].strip() for r in existing if r.get("item_name")}

    with open(CANDIDATE_CSV, encoding="utf-8", newline="") as f:
        candidates = list(csv.DictReader(f))

    excluded = sum(1 for r in candidates if exclude_row(r))
    containers = new_container_rows()
    for r in containers:
        if r["item_id"] in existing_ids:
            print("error: container id collision", r["item_id"], file=sys.stderr)
            return 1
        existing_names.add(r["item_name"].strip())

    transformed = transform_candidate_rows(candidates, org, existing_names)
    dup_ids = [r["item_id"] for r in transformed if r["item_id"] in existing_ids]
    if dup_ids:
        print("error: candidate item_id already in process_list:", dup_ids[:10], file=sys.stderr)
        return 1

    new_rows = containers + transformed
    print(
        f"candidates={len(candidates)} excluded_tier_c~={excluded} "
        f"containers={len(containers)} merged_gtm={len(transformed)} total_new={len(new_rows)}"
    )

    if not args.write:
        print("Dry run: pass --write to apply.")
        return 0

    combined = existing + new_rows
    fixed = resolve_all_parent_ids([normalize_process_row(r) for r in combined])
    write_process_csv(PROC_CSV, fixed)
    print("Wrote", PROC_CSV)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
