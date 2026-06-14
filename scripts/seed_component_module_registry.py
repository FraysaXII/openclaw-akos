"""One-shot / refresh generator for COMPONENT_MODULE_REGISTRY.csv from matrix SSOT.

Usage: py scripts/seed_component_module_registry.py [--write]
"""
from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

from akos.hlk_component_module_registry import (
    ALIAS_OF,
    D1_KEYWORDS,
    D2_COMPONENTS,
    D3_CANONICAL,
    DIMENSION_REGISTRY_BY_FAMILY,
    DOC_URL_BY_FAMILY,
    FIELDNAMES,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People"
    / "Compliance" / "canonicals" / "techops" / "COMPONENT_SERVICE_MATRIX.csv"
)
OUT_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Tech"
    / "System Owner" / "canonicals" / "dimensions" / "COMPONENT_MODULE_REGISTRY.csv"
)

NEXT_VERIFY = "2026-09-14"


def _family_from_row(row: dict[str, str]) -> str:
    name = (row.get("component_name") or "").lower()
    cid = row["component_id"]
    if cid in D3_CANONICAL:
        return D3_CANONICAL[cid]
    if cid in D2_COMPONENTS:
        return D2_COMPONENTS[cid]
    if cid in ALIAS_OF:
        canon = ALIAS_OF[cid]
        return D3_CANONICAL.get(canon) or D2_COMPONENTS.get(canon, "other")
    if "supabase" in name:
        return "supabase"
    if "vercel" in name:
        return "vercel"
    if "cloudflare" in name:
        return "cloudflare"
    if "github" in name:
        return "github"
    if "sentry" in name:
        return "sentry"
    if "langfuse" in name:
        return "langfuse"
    if "stripe" in name:
        return "stripe"
    if "make" in name and "make" in name.split("—")[0].lower():
        return "make"
    if "n8n" in name:
        return "n8n"
    if "render" in name:
        return "render"
    if row.get("repo_slug") == "openclaw-akos" or "openclaw" in name or "akos" in name:
        return "openclaw_akos"
    return "other"


def _classify(row: dict[str, str]) -> dict[str, str]:
    cid = row["component_id"]
    name = row.get("component_name") or cid
    slo = (row.get("slo_tier") or "standard").lower()
    owner = (row.get("primary_owner_role") or "System Owner").strip()
    family = _family_from_row(row)
    doc_link = (row.get("doc_link") or "").strip()

    if cid in ALIAS_OF:
        canon = ALIAS_OF[cid]
        return {
            "governed_status": "alias",
            "governance_depth": "D0",
            "dimension_registry_path": "",
            "doc_url": doc_link or DOC_URL_BY_FAMILY.get(family, ""),
            "volatility_class": "n_a",
            "next_verify_by": "",
            "gap": "",
            "priority": "low",
            "notes": f"alias_of={canon}; sheet clone — inventory FK only",
        }

    if cid in D3_CANONICAL or cid == "comp_matriz_00004":
        reg = DIMENSION_REGISTRY_BY_FAMILY.get(family, "")
        gap = "" if family == "supabase" else ""
        status = "governed" if reg or family == "supabase" else "partial"
        if family == "openclaw_akos":
            reg = ""
            status = "governed"
        return {
            "governed_status": status,
            "governance_depth": "D3",
            "dimension_registry_path": reg,
            "doc_url": doc_link or DOC_URL_BY_FAMILY.get(family, ""),
            "volatility_class": "high" if family in {"vercel", "cloudflare", "github"} else "medium",
            "next_verify_by": NEXT_VERIFY,
            "gap": gap,
            "priority": "critical" if slo == "critical" else "high",
            "notes": f"D3 ecosystem family={family}; I100 Wave-1" if family != "supabase" else "D3 absorbed from I99 SUPABASE_ECOSYSTEM_GOVERNANCE; doctrine owned by Data Architect",
        }

    if cid in D2_COMPONENTS:
        reg = DIMENSION_REGISTRY_BY_FAMILY.get(family, "")
        return {
            "governed_status": "partial" if reg else "forward",
            "governance_depth": "D2",
            "dimension_registry_path": reg,
            "doc_url": doc_link or DOC_URL_BY_FAMILY.get(family, ""),
            "volatility_class": "medium",
            "next_verify_by": NEXT_VERIFY,
            "gap": "" if reg else f"Wave-2 dimension registry pending for {family}",
            "priority": "critical" if slo == "critical" else "high",
            "notes": f"D2 Wave-2 family={family}",
        }

    name_l = name.lower()
    if any(k in name_l for k in D1_KEYWORDS) or row.get("component_kind") == "research_tool":
        return {
            "governed_status": "inventory",
            "governance_depth": "D1",
            "dimension_registry_path": "",
            "doc_url": doc_link,
            "volatility_class": "medium",
            "next_verify_by": NEXT_VERIFY,
            "gap": "Doc trace only — no dimension registry until active consumer",
            "priority": "medium",
            "notes": "D1 doc trace; Research Radar cadence",
        }

    if slo == "critical":
        return {
            "governed_status": "partial",
            "governance_depth": "D2",
            "dimension_registry_path": "",
            "doc_url": doc_link,
            "volatility_class": "medium",
            "next_verify_by": NEXT_VERIFY,
            "gap": "Critical component without Wave-1/2 registry — schedule Wave-3",
            "priority": "critical",
            "notes": "D2 scheduled — critical slo_tier",
        }

    return {
        "governed_status": "inventory",
        "governance_depth": "D0",
        "dimension_registry_path": "",
        "doc_url": doc_link,
        "volatility_class": "low",
        "next_verify_by": "",
        "gap": "",
        "priority": "low" if slo == "standard" else "medium",
        "notes": "D0 inventory-only; matrix row sufficient",
    }


def build_rows() -> list[dict[str, str]]:
    with MATRIX_PATH.open(newline="", encoding="utf-8") as fh:
        matrix = list(csv.DictReader(fh))
    out: list[dict[str, str]] = []
    for i, row in enumerate(matrix, start=1):
        cid = row["component_id"]
        cls = _classify(row)
        family = _family_from_row(row)
        out.append(
            {
                "module_id": f"COMP-MOD-{i:03d}",
                "component_id": cid,
                "module_name": (row.get("component_name") or cid)[:120],
                "module_family": family,
                **cls,
                "owner_role": (row.get("primary_owner_role") or "System Owner").strip(),
            }
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    rows = build_rows()
    depths = {}
    for r in rows:
        depths[r["governance_depth"]] = depths.get(r["governance_depth"], 0) + 1
    print(f"Generated {len(rows)} rows: {depths}")
    if args.write:
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with OUT_PATH.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=FIELDNAMES)
            w.writeheader()
            w.writerows(rows)
        print(f"Wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
