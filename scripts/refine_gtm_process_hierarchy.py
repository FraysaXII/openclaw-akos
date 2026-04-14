#!/usr/bin/env python3
"""Refine merged GTM rows in process_list.csv (Pattern 2 hierarchy + item_name cleanup).

Reads canonical process_list + candidate_gtm_process_rows, inserts gtm_cl_* cluster
process rows, rewires item_parent_1/item_parent_2 for gtm_* rows, sanitizes
code-like item_name values. Run from repo root:

    py scripts/refine_gtm_process_hierarchy.py --write

Default is dry-run (prints counts only).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_process_csv import normalize_process_row, resolve_all_parent_ids, write_process_csv

PROC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "process_list.csv"
CANDIDATE_CSV = (
    REPO_ROOT / "docs" / "wip" / "planning" / "02-hlk-on-akos-madeira" / "candidate_gtm_process_rows.csv"
)

# Mirrors scripts/merge_gtm_into_process_list.py
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

WORKSTREAM_PROJECT: dict[str, str] = {
    WS_RESEARCH_MAT: PROJ_HOL_RESEA,
    WS_M_RADAR: PROJ_MADEIRA,
    WS_M_PLAN: PROJ_MADEIRA,
    WS_M_SALES: PROJ_MADEIRA,
    WS_M_UX: PROJ_MADEIRA,
    WS_M_DEVOPS: PROJ_MADEIRA,
    WS_M_BENCH: PROJ_MADEIRA,
    WS_BRAND: PROJ_THI_MKT,
    WS_TEAM: PROJ_HOL_PEO,
    WS_GTM_ENT: PROJ_THI_OP,
    WS_SVC: PROJ_THI_OP,
    WS_OPS_CTL: PROJ_THI_OP,
}

STRUCTURAL_IDS = frozenset(
    {
        "gtm_ws_research_material",
        "gtm_proc_research_pipeline",
        "gtm_ws_madeira_radar",
        "gtm_ws_madeira_planning",
        "gtm_ws_madeira_sales",
        "gtm_ws_madeira_ux",
        "gtm_ws_madeira_devops",
        "gtm_ws_madeira_benchmark",
        "gtm_ws_brand_presence",
        "gtm_ws_team_growth",
        "gtm_ws_gtm_entity",
        "gtm_ws_service_catalog",
        "gtm_ws_ops_control",
        "gtm_pm_st_promo",
    }
)

ITEM_NAME_MAX = 120

# Spanish / Trello first-segment gloss for cluster titles (English registry)
SEG_EN: dict[str, str] = {
    "Canales como web y linkedin": "Web and LinkedIn channels",
    "Marca y mensajes": "Brand messaging",
    "Paid media y posicionamiento": "Paid media and positioning",
    "Darnos a conocer": "Brand discovery and channels",
    "Control financiero": "Financial control",
    "Establecer sociedad": "Entity formation",
    "Optimizar FTEs": "FTE optimization",
    "Salir a mercado": "Go-to-market readiness",
    "Capacidad de absorber y colocar intel": "Intelligence absorption and placement",
    "Conocer el end to end del funcionamiento": "End-to-end operating model",
    "Controlar la empresa": "Corporate control",
    "Documentar infraestructura": "Infrastructure documentation",
    "Categorizar inventario de capacidades y recursos": "Capability and resource inventory",
    "Conocer demanda de mercado": "Market demand",
    "Definir servicios": "Service definition",
    "Definir y documentar procesos de servicio": "Service process documentation",
    "Crecer equipo": "Team growth",
    "Definición de huecos donde caben sus capacidades": "Role fit and capability gaps",
    "Plan de carrera": "Career planning",
    "Procesos de formación y output": "Training and output processes",
    "Research Material": "Research material sources",
    "MADEIRA Project": "MADEIRA project umbrella",
}


def _slug_key(ws: str, trello_path: str) -> str:
    raw = f"{ws}::{trello_path}".encode("utf-8", errors="replace")
    return hashlib.sha256(raw).hexdigest()[:14]


def cluster_item_id(ws: str, trello_path: str) -> str:
    return f"gtm_cl_{_slug_key(ws, trello_path)}"


def _cap_words(s: str) -> str:
    return " ".join(w[:1].upper() + w[1:].lower() if w else "" for w in re.split(r"\s+", s.strip()) if w)


def english_cluster_title(ws: str, trello_path: str) -> str:
    """Derive concise English cluster item_name from workstream + Trello path."""
    path = (trello_path or "").strip()
    parts = [p.strip() for p in path.split(" / ") if p.strip()]
    last = parts[-1] if parts else "General scope"
    first = parts[0] if parts else ""

    if ws == WS_M_RADAR and "topics on radar" in first.lower():
        tail = last.replace("'", "")
        title = f"MADEIRA research radar — {_cap_words(tail)} themes"
    elif ws == WS_M_BENCH:
        title = f"MADEIRA benchmarking — {_cap_words(last)}"
    elif ws == WS_M_DEVOPS:
        clean = last.replace(".py", " module").replace("_", " ")
        title = f"MADEIRA delivery — {_cap_words(clean)}"
    elif ws == WS_M_UX:
        title = f"MADEIRA UX — {_cap_words(last.replace('/', ' '))}"
    elif ws in (WS_M_PLAN, WS_M_SALES) and "PMO" in first:
        title = f"MADEIRA product delivery — {_cap_words(last)}"
    elif ws == WS_M_PLAN and path == "MADEIRA Project":
        title = "MADEIRA product planning — project-level backlog"
    elif ws == WS_RESEARCH_MAT and path == "Research Material":
        title = "Research material — curated learning playlists"
    else:
        en_first = SEG_EN.get(first, first)
        en_last = SEG_EN.get(last, last)
        if len(parts) >= 2:
            title = f"{ws} — {en_first}: {en_last}"
        else:
            title = f"{ws} — {en_first}"

    if len(title) > ITEM_NAME_MAX:
        title = title[: ITEM_NAME_MAX - 1].rstrip() + "…"
    return title


def uses_pipeline_process_instead(ws: str, trello_path: str) -> bool:
    p = (trello_path or "").strip()
    return ws == WS_RESEARCH_MAT and p == "Research Material / Pipeline"


def humanize_identifier(name: str) -> str:
    n = name.strip()
    n = re.sub(r"\s+", " ", n)
    if "_" in n and re.match(r"^[a-z][a-z0-9_]*$", n):
        return " ".join(part.capitalize() for part in n.split("_") if part)
    if re.match(r"^[A-Z][a-zA-Z0-9_]+$", n) and not n.isupper():
        s = re.sub(r"([a-z])([A-Z])", r"\1 \2", n)
        return s.replace("_", " ")
    return n


def looks_codeish(name: str) -> bool:
    n = name.strip()
    if not n:
        return True
    if "/" in n or "\\" in n:
        return True
    if ".py" in n.lower() or ".ts" in n.lower():
        return True
    if "`" in n or n.startswith("post(") or n.startswith("get("):
        return True
    if re.search(r"__\w+__", n):
        return True
    if "_" in n and re.match(r"^[a-z][a-z0-9_]{2,}$", n):
        return True
    if n in {"Query", "Demo", "Settings", "Pitch", "People"}:
        return True
    # PascalCase / StudlyCaps identifiers (e.g. RetrieverQueryEngine), not plain words like "Office"
    if re.match(r"^[A-Z][a-zA-Z0-9_]{2,}$", n) and "_" not in n and " " not in n:
        caps = sum(1 for c in n if c.isupper())
        if n.lower() in {"demo", "pitch", "people", "settings", "query"}:
            return True
        if caps >= 2 or any(c.isdigit() for c in n):
            return True
    return False


def sanitize_leaf_item_name(
    name: str,
    *,
    cluster_title: str,
    workstream: str,
    orig_symbol_line: str,
) -> tuple[str, str]:
    """Return (new_item_name, extra_description_prefix)."""
    n = (name or "").strip()
    extra = ""
    if len(n) > ITEM_NAME_MAX:
        extra = f"Full original title: {n}\n"
        n = n[: ITEM_NAME_MAX - 1].rstrip() + "…"

    if not looks_codeish(n):
        return n, extra

    sym = n
    human = humanize_identifier(sym)
    if human == sym and "(" in sym:
        human = "MADEIRA API surface item"
    base = f"{cluster_title.split('—')[0].strip()} — {human}"
    if len(base) > ITEM_NAME_MAX:
        base = base[: ITEM_NAME_MAX - 1].rstrip() + "…"
    extra = f"{orig_symbol_line}Original registry symbol: {sym}\n" + extra
    return base, extra


def load_csv(path: Path) -> list[dict[str, str]]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def refine(rows: list[dict[str, str]], candidates: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, int]]:
    cand_by_id = {(r.get("item_id") or "").strip(): r for r in candidates}
    by_id = {(r.get("item_id") or "").strip(): dict(r) for r in rows}

    # Workstream template rows (entity/area/roles)
    ws_templates: dict[str, dict[str, str]] = {}
    for r in rows:
        iid = (r.get("item_id") or "").strip()
        nm = (r.get("item_name") or "").strip()
        if iid.startswith("gtm_ws_") and nm in WORKSTREAM_PROJECT:
            ws_templates[nm] = dict(r)

    stats = {"clusters": 0, "leaves_rewired": 0, "names_sanitized": 0, "structural_fixed": 0}

    # --- Structural containers (parents only)
    for iid in STRUCTURAL_IDS:
        row = by_id.get(iid)
        if not row:
            continue
        gran = (row.get("item_granularity") or "").strip()
        name = (row.get("item_name") or "").strip()
        if iid == "gtm_pm_st_promo":
            row["item_parent_2"] = PROJ_THI_OP
            row["item_parent_1"] = "Engage"
            stats["structural_fixed"] += 1
            continue
        if iid == "gtm_proc_research_pipeline":
            row["item_parent_2"] = PROJ_HOL_RESEA
            row["item_parent_1"] = WS_RESEARCH_MAT
            stats["structural_fixed"] += 1
            continue
        if gran == "workstream" and name in WORKSTREAM_PROJECT:
            proj = WORKSTREAM_PROJECT[name]
            row["item_parent_2"] = proj
            row["item_parent_1"] = proj
            stats["structural_fixed"] += 1

    # --- Build cluster keys for non-structural gtm rows
    cluster_specs: dict[tuple[str, str], dict] = {}
    for iid, row in by_id.items():
        if not iid.startswith("gtm_") or iid in STRUCTURAL_IDS:
            continue
        cand = cand_by_id.get(iid)
        if not cand:
            continue
        ws = (row.get("item_parent_1") or "").strip()
        path = (cand.get("item_parent_1") or "").strip()
        if uses_pipeline_process_instead(ws, path):
            continue
        key = (ws, path)
        if key not in cluster_specs:
            title = english_cluster_title(ws, path)
            proj = WORKSTREAM_PROJECT.get(ws, PROJ_THI_OP)
            tpl = ws_templates.get(ws, row)
            cid = cluster_item_id(ws, path)
            cluster_specs[key] = {
                "item_id": cid,
                "item_name": title,
                "workstream": ws,
                "project": proj,
                "trello_path": path,
                "template": tpl,
                "members": [],
            }
        cluster_specs[key]["members"].append(iid)

    used_names = {((r.get("item_name") or "").strip()) for r in rows if r.get("item_name")}

    def disambiguate(nm: str) -> str:
        base = nm
        if base not in used_names:
            used_names.add(base)
            return base
        n = 2
        while f"{base} ({n})" in used_names:
            n += 1
        out = f"{base} ({n})"
        used_names.add(out)
        return out

    cluster_rows: list[dict[str, str]] = []
    for spec in cluster_specs.values():
        tpl = spec["template"]
        nm = disambiguate(spec["item_name"])
        spec["item_name_resolved"] = nm
        desc = (
            f"Cluster scope for Holistika GTM items sourced from Trello path prefixes. "
            f"Outcome-focused grouping under {spec['workstream']}."
        )
        add = f"Original Trello item_parent_1 path: {spec['trello_path']!r}."
        cr = {
            "type": tpl.get("type", "Internal"),
            "orientation": tpl.get("orientation", "Employee"),
            "entity": tpl.get("entity", ""),
            "area": tpl.get("area", ""),
            "role_parent_1": tpl.get("role_parent_1", ""),
            "role_owner": tpl.get("role_owner", ""),
            "item_parent_2_id": "",
            "item_parent_2": spec["project"],
            "item_parent_1_id": "",
            "item_parent_1": spec["workstream"],
            "item_name": nm,
            "item_id": spec["item_id"],
            "item_granularity": "process",
            "time_hours_par": "",
            "description": desc,
            "instructions": "",
            "addundum_extras": add[:1500],
            "confidence": tpl.get("confidence", "2"),
            "count_name": tpl.get("count_name", "1"),
            "frequency": tpl.get("frequency", "medium"),
            "quality": tpl.get("quality", "3"),
        }
        cluster_rows.append(cr)
        stats["clusters"] += 1

    cluster_parent_by_key = {
        (ws, path): cluster_specs[(ws, path)]["item_name_resolved"]
        for ws, path in cluster_specs
    }

    # --- Rewire leaves + sanitize
    for iid, row in by_id.items():
        if not iid.startswith("gtm_") or iid in STRUCTURAL_IDS:
            continue
        cand = cand_by_id.get(iid)
        if not cand:
            continue
        ws = (row.get("item_parent_1") or "").strip()
        path = (cand.get("item_parent_1") or "").strip()

        if uses_pipeline_process_instead(ws, path):
            row["item_parent_1"] = PROC_PIPELINE
            row["item_parent_2"] = WS_RESEARCH_MAT
            cluster_title = PROC_PIPELINE
        else:
            pnm = cluster_parent_by_key.get((ws, path))
            if not pnm:
                continue
            row["item_parent_1"] = pnm
            row["item_parent_2"] = ws
            cluster_title = pnm
        stats["leaves_rewired"] += 1

        orig_name = (row.get("item_name") or "").strip()
        new_name, extra = sanitize_leaf_item_name(
            orig_name,
            cluster_title=cluster_title,
            workstream=ws,
            orig_symbol_line="",
        )
        if new_name != orig_name:
            stats["names_sanitized"] += 1
            row["item_name"] = new_name
            if extra:
                desc = (row.get("description") or "").strip()
                row["description"] = (extra + desc).strip()[:1800]

        # Refresh stale boilerplate one-liner
        desc = (row.get("description") or "").strip()
        if "Canonical parent workstream:" in desc:
            tail = desc.split("Scope:", 1)
            scope = tail[1].strip() if len(tail) > 1 else ""
            row["description"] = (f"GTM operating item under {cluster_title}. Scope: {scope}")[:1800]

    # --- Insert cluster rows (after structural block, before first non-structural gtm row)
    insert_at: int | None = None
    struct_seen = 0
    for i, r in enumerate(rows):
        iid = (r.get("item_id") or "").strip()
        if iid in STRUCTURAL_IDS:
            struct_seen += 1
            if struct_seen == len(STRUCTURAL_IDS):
                insert_at = i + 1
                break
    if insert_at is None:
        raise RuntimeError("GTM structural rows not found or incomplete")

    out: list[dict[str, str]] = []
    for i, r in enumerate(rows):
        iid = (r.get("item_id") or "").strip()
        if i == insert_at:
            out.extend(sorted(cluster_rows, key=lambda x: x["item_id"]))
        out.append(by_id[iid])

    if insert_at == len(rows):
        out.extend(sorted(cluster_rows, key=lambda x: x["item_id"]))

    return out, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Overwrite process_list.csv")
    args = parser.parse_args()

    rows = load_csv(PROC_CSV)
    candidates = load_csv(CANDIDATE_CSV)

    new_rows, stats = refine(rows, candidates)
    print(
        f"clusters={stats['clusters']} leaves_rewired={stats['leaves_rewired']} "
        f"names_sanitized={stats['names_sanitized']} structural_fixed={stats['structural_fixed']}"
    )

    if not args.write:
        print("Dry run: pass --write to apply.")
        return 0

    fixed = resolve_all_parent_ids([normalize_process_row(r) for r in new_rows])
    write_process_csv(PROC_CSV, fixed)
    print("Wrote", PROC_CSV)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
