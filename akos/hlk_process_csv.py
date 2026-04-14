"""Canonical `process_list.csv` column order and parent-id resolution (HLK SSOT).

Single definition for CSV writers and upgrade scripts. No parallel inventory.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

PROCESS_LIST_FIELDNAMES: list[str] = [
    "type",
    "orientation",
    "entity",
    "area",
    "role_parent_1",
    "role_owner",
    "item_parent_2",
    "item_parent_2_id",
    "item_parent_1",
    "item_parent_1_id",
    "item_name",
    "item_id",
    "item_granularity",
    "time_hours_par",
    "description",
    "instructions",
    "addundum_extras",
    "confidence",
    "count_name",
    "frequency",
    "quality",
]


def ambiguous_item_names(rows: list[dict[str, str]]) -> set[str]:
    """item_name values that map to more than one item_id (registry tech debt)."""
    groups: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        name = (row.get("item_name") or "").strip()
        iid = (row.get("item_id") or "").strip()
        if name and iid:
            groups[name].add(iid)
    return {n for n, ids in groups.items() if len(ids) > 1}


def build_unique_item_name_to_id(rows: list[dict[str, str]]) -> dict[str, str]:
    """Map item_name -> item_id only when that name is unique across the file."""
    amb = ambiguous_item_names(rows)
    out: dict[str, str] = {}
    for row in rows:
        name = (row.get("item_name") or "").strip()
        iid = (row.get("item_id") or "").strip()
        if not name or not iid or name in amb:
            continue
        out[name] = iid
    return out


def attach_parent_ids(row: dict[str, str], name_to_id: dict[str, str], ambiguous: set[str]) -> dict[str, str]:
    """Return a copy of row with item_parent_*_id filled when parent name resolves uniquely."""
    r = {k: (row.get(k) or "") for k in PROCESS_LIST_FIELDNAMES}
    for num in ("1", "2"):
        nk = f"item_parent_{num}"
        ik = f"item_parent_{num}_id"
        name = (r.get(nk) or "").strip()
        if not name:
            r[ik] = ""
        elif name in ambiguous:
            r[ik] = ""
        else:
            r[ik] = name_to_id.get(name, "")
    return r


def normalize_process_row(row: dict[str, str]) -> dict[str, str]:
    """Project a dict onto PROCESS_LIST_FIELDNAMES (missing keys become empty)."""
    return {k: (row.get(k) or "") for k in PROCESS_LIST_FIELDNAMES}


def resolve_all_parent_ids(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Build unique name map from full row set, then attach ids to every row."""
    amb = ambiguous_item_names(rows)
    name_to_id = build_unique_item_name_to_id(rows)
    return [attach_parent_ids(r, name_to_id, amb) for r in rows]


def read_process_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fn = list(reader.fieldnames or [])
        raw = [dict(r) for r in reader]
    return fn, raw


def write_process_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=PROCESS_LIST_FIELDNAMES, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: (row.get(k) or "") for k in PROCESS_LIST_FIELDNAMES})
