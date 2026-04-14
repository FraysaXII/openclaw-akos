#!/usr/bin/env python3
"""Assign unique item_name values for rows that share a display name (HLK SSOT).

Duplicate item_name values block parent-id resolution (see akos.hlk_process_csv).
This script renames a fixed set of canonical rows by item_id only; it does not
change parent name strings on other rows (each duplicate pair is split so one
side keeps the original name where that name is still used as item_parent_1/2).

Usage (repo root):
    py scripts/dedupe_ambiguous_process_item_names.py
    py scripts/dedupe_ambiguous_process_item_names.py --write
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROC_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "process_list.csv"

sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_process_csv import (  # noqa: E402
    ambiguous_item_names,
    normalize_process_row,
    resolve_all_parent_ids,
    write_process_csv,
)

# item_id -> new unique item_name (keep sibling row on original name where TB/MADEIRA graph needs it).
RENAMES_BY_ITEM_ID: dict[str, str] = {
    # Engage: Think Big workstream keeps "Engage"; Holistika process disambiguated.
    "hol_peopl_dtp_118": "Engage (Holistika Project Lifecycle)",
    # Generational Filter: process keeps name; task disambiguated.
    "hol__dtp_162": "Generational Filter (execution task)",
    # HLK Data Governance vs Think Big marketing — disambiguate env_tech_* leaves.
    "env_tech_dtp_35": "Audiences (HLK Data Governance)",
    "env_tech_dtp_36": "Events (HLK Data Governance)",
    "env_tech_dtp_37": "Campaign Management (HLK Data Governance)",
    "env_tech_dtp_38": "Facebook Business Manager (HLK Data Governance)",
    "env_tech_dtp_45": "Linkedin (HLK Data Governance)",
    "env_tech_dtp_46": "Instagram (HLK Data Governance)",
    "env_tech_dtp_68": "Masterdata Design (HLK Data Governance)",
    # Legal / retention / NDA duplicates.
    "env_tech_dtp_24": "Retention (HLK Tech Lab)",
    "thi_legal_dtp_23": "Retention (Think Big Legal)",
    "env_tech_dtp_25": "NDA (HLK Tech Lab)",
    "thi_legal_dtp_26": "NDA (Think Big Legal template A)",
    "thi_legal_dtp_27": "NDA (Think Big Legal template B)",
    # Layout: Next.js branch keeps "Layout"; marketing pod disambiguated.
    "thi_mkt_dtp_40": "Layout (marketing pod)",
    # GTM MADEIRA duplicate cluster titles.
    "gtm_madeira_dtp_101": "MADEIRA UX API surface — connection pool",
    "gtm_madeira_dtp_106": "MADEIRA UX API surface — Highway AI",
    "gtm_madeira_dtp_201": "MADEIRA delivery API — POST madeira_query",
    "gtm_madeira_dtp_203": "MADEIRA delivery API — POST madeira_stream_query",
    "gtm_madeira_dtp_204": "MADEIRA delivery API — GET madeira_personality",
    "gtm_madeira_dtp_205": "MADEIRA delivery API — POST madeira_personality",
    "gtm_madeira_dtp_207": "MADEIRA delivery API — GET health",
    "gtm_madeira_dtp_208": "MADEIRA delivery API — POST clear_madeira_memory",
}


def load_rows() -> list[dict[str, str]]:
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    rows = load_rows()
    changed = 0
    for r in rows:
        iid = (r.get("item_id") or "").strip()
        if iid in RENAMES_BY_ITEM_ID:
            new_name = RENAMES_BY_ITEM_ID[iid]
            if (r.get("item_name") or "").strip() != new_name:
                r["item_name"] = new_name
                changed += 1
    fixed = resolve_all_parent_ids([normalize_process_row(r) for r in rows])
    amb = ambiguous_item_names(fixed)
    print(f"rows_renamed={changed} ambiguous_item_names_after={len(amb)}")
    if amb:
        for n in sorted(amb)[:20]:
            print(f"  still ambiguous: {n!r}", file=sys.stderr)
        if len(amb) > 20:
            print(f"  ... and {len(amb) - 20} more", file=sys.stderr)
        return 1
    if not args.write:
        print("Dry run: pass --write to apply.")
        return 0
    write_process_csv(PROC_CSV, fixed)
    print("Wrote", PROC_CSV)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
