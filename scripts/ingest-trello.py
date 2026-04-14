#!/usr/bin/env python3
"""Ingest a Trello board JSON export into candidate HLK process_list.csv rows.

Maps the Trello card/checklist hierarchy into the HLK process tree:
  list.name     -> project
  card.name     -> workstream (if card has checklists) or process (if leaf)
  checklist     -> task group (process)
  checklist item -> task

Outputs candidate rows as CSV for operator review before canonical commit.
Does NOT auto-commit to the canonical process_list.csv.

Usage:
    python scripts/ingest-trello.py <trello_json> [--output candidate_rows.csv]
    python scripts/ingest-trello.py <trello_json> --dry-run
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_process_csv import normalize_process_row, resolve_all_parent_ids, write_process_csv

SKIP_LISTS = {"Done", "Viejo"}
DEFAULT_ENTITY = "Holistika"
DEFAULT_AREA = "Operations"
DEFAULT_ROLE_PARENT = "O5-1"

_LIST_TO_PROJECT: dict[str, dict[str, str]] = {
    "MADEIRA Project": {"area": "Tech", "role_owner": "AI Engineer", "project_prefix": "gtm_madeira"},
    "Research Material": {"area": "Research", "role_owner": "Holistik Researcher", "project_prefix": "gtm_research"},
    "Definir servicios": {"area": "Operations", "role_owner": "PMO", "project_prefix": "gtm_services"},
    "Salir a mercado": {"area": "Operations", "role_owner": "PMO", "project_prefix": "gtm_launch"},
    "Controlar la empresa": {"area": "Operations", "role_owner": "PMO", "project_prefix": "gtm_ops"},
    "Darnos a conocer": {"area": "Marketing", "role_owner": "CMO", "project_prefix": "gtm_brand"},
    "Crecer equipo": {"area": "People", "role_owner": "CPO", "project_prefix": "gtm_team"},
    "To Do": {"area": "Operations", "role_owner": "PMO", "project_prefix": "gtm_backlog"},
    "ToDo": {"area": "Operations", "role_owner": "PMO", "project_prefix": "gtm_backlog2"},
}

def _slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower().strip())
    return s.strip("_")[:60]


def _dedup_cards(cards: list[dict]) -> list[dict]:
    """Remove duplicate cards (Trello exports sometimes double them)."""
    seen: set[str] = set()
    result: list[dict] = []
    for card in cards:
        cid = card.get("id", "")
        if cid in seen:
            continue
        seen.add(cid)
        result.append(card)
    return result


def ingest(trello_path: Path) -> list[dict]:
    with open(trello_path, encoding="utf-8") as f:
        cards = json.load(f)

    cards = _dedup_cards(cards)
    rows: list[dict] = []
    id_counter: dict[str, int] = {}

    for card in cards:
        list_name = card.get("list", {}).get("name", "Unknown")
        if list_name in SKIP_LISTS:
            continue

        config = _LIST_TO_PROJECT.get(list_name)
        if config is None:
            continue

        prefix = config["project_prefix"]
        area = config["area"]
        role_owner = config["role_owner"]
        card_name = card.get("name", "").strip()
        if not card_name:
            continue

        checklists = card.get("checklists", [])
        project_name = list_name

        if not checklists:
            n = id_counter.get(prefix, 0) + 1
            id_counter[prefix] = n
            rows.append({
                "type": "Internal",
                "orientation": "Employee",
                "entity": DEFAULT_ENTITY,
                "area": area,
                "role_parent_1": DEFAULT_ROLE_PARENT,
                "role_owner": role_owner,
                "item_parent_2_id": "",
                "item_parent_2": "",
                "item_parent_1_id": "",
                "item_parent_1": project_name,
                "item_name": card_name,
                "item_id": f"{prefix}_dtp_{n}",
                "item_granularity": "process",
                "time_hours_par": "",
                "description": card.get("description", "")[:200],
                "instructions": "",
                "addundum_extras": "",
                "confidence": "",
                "count_name": "",
                "frequency": "",
                "quality": "",
            })
            continue

        for checklist in checklists:
            cl_name = checklist.get("name", "").strip()
            if not cl_name:
                continue

            items = checklist.get("items", [])
            for item in items:
                item_name = item.get("name", "").strip()
                if not item_name:
                    continue
                n = id_counter.get(prefix, 0) + 1
                id_counter[prefix] = n
                rows.append({
                    "type": "Internal",
                    "orientation": "Employee",
                    "entity": DEFAULT_ENTITY,
                    "area": area,
                    "role_parent_1": DEFAULT_ROLE_PARENT,
                    "role_owner": role_owner,
                    "item_parent_2_id": "",
                    "item_parent_2": project_name,
                    "item_parent_1_id": "",
                    "item_parent_1": f"{card_name} / {cl_name}",
                    "item_name": item_name,
                    "item_id": f"{prefix}_dtp_{n}",
                    "item_granularity": "task",
                    "time_hours_par": "",
                    "description": "",
                    "instructions": "",
                    "addundum_extras": "",
                    "confidence": "",
                    "count_name": "",
                    "frequency": "",
                    "quality": "",
                })

    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Trello board into HLK process candidate rows")
    parser.add_argument("trello_json", type=Path, help="Path to formatted Trello JSON export")
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="Output CSV path (default: candidate_process_rows.csv in repo root)")
    parser.add_argument("--dry-run", action="store_true", help="Print summary without writing")
    args = parser.parse_args()

    if not args.trello_json.exists():
        print(f"Error: {args.trello_json} not found")
        return 1

    rows = ingest(args.trello_json)
    print(f"Ingested {len(rows)} candidate process rows from Trello board")

    by_project: dict[str, int] = {}
    for r in rows:
        project = r.get("item_parent_2") or r.get("item_parent_1", "Unknown")
        by_project[project] = by_project.get(project, 0) + 1

    print("\nBreakdown by project/workstream:")
    for project, count in sorted(by_project.items()):
        print(f"  {project}: {count} rows")

    if args.dry_run:
        print("\n[DRY-RUN] No file written.")
        return 0

    output = args.output or Path("candidate_process_rows.csv")
    fixed = resolve_all_parent_ids([normalize_process_row(r) for r in rows])
    write_process_csv(output, fixed)
    print(f"\nCandidate rows written to: {output}")
    print("IMPORTANT: Review these rows before appending to docs/references/hlk/compliance/process_list.csv")
    print("Run: py scripts/validate_hlk.py after merging to verify integrity")
    return 0


if __name__ == "__main__":
    sys.exit(main())
