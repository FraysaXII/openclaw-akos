"""Research ledger bootstrap/append operations (Automation OS engine chassis).

Pairs with scripts/research_ledger.py and akos/hlk_research_action.py SSOT.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from akos.hlk_research_action import SOURCE_LEDGER_FIELDNAMES, ResearchSourceRow

PROCESS_LIST_PATH = Path(
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv"
)

# Holistika area (process_list ``area`` column) → Automation OS charter prong.
AREA_TO_PRONG: dict[str, str] = {
    "Tech": "P1-TECH",
    "Data": "P2-DATA",
    "Operations": "P3-OPS",
    "Research": "P4-RESEARCH",
    "People": "P5-PEOPLE",
    "Finance": "P7-FINANCE",
    "Legal": "P8-LEGAL",
    "Marketing": "P9-MARKETING",
    "MKT": "P9-MARKETING",
}

DEFAULT_UNRESOLVED_PRONG = "P1-TECH"

GITHUB_BLOB = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def pack_dir(repo_root: Path, pack_slug: str) -> Path:
    return repo_root / "docs/wip/intelligence" / pack_slug


def ledger_path(pack_root: Path) -> Path:
    return pack_root / "source-ledger.csv"


def norm_url(url: str) -> str:
    return url.split("#")[0].rstrip("/")


def rel_url(repo_root: Path, path: Path) -> str:
    rel = path.relative_to(repo_root).as_posix()
    if rel.startswith("docs/"):
        return rel
    return f"{GITHUB_BLOB}{rel}"


def load_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        return [dict(row) for row in reader]


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(SOURCE_LEDGER_FIELDNAMES))
        writer.writeheader()
        writer.writerows(rows)


def validate_row_dict(raw: dict[str, Any]) -> ResearchSourceRow:
    return ResearchSourceRow.model_validate(raw)


def load_runbook_prong_map(repo_root: Path) -> dict[str, str]:
    """Map normalized ``scripts/foo.py`` paths to charter prongs via process_list."""
    path = repo_root / PROCESS_LIST_PATH
    if not path.is_file():
        return {}
    mapping: dict[str, str] = {}
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            runbook = (row.get("runbook_path") or "").strip().replace("\\", "/")
            if not runbook.startswith("scripts/"):
                continue
            area = (row.get("area") or "").strip()
            prong = AREA_TO_PRONG.get(area, DEFAULT_UNRESOLVED_PRONG)
            mapping.setdefault(runbook, prong)
    return mapping


def resolve_prong_for_script(
    script_rel: str,
    *,
    runbook_map: dict[str, str],
    manifest_prong: str | None = None,
) -> tuple[str, str]:
    """Return (prong_id, binding_note) using manifest → process_list → unresolved."""
    if manifest_prong:
        return manifest_prong, "prong-binding:manifest"
    normalized = script_rel.replace("\\", "/")
    if normalized in runbook_map:
        return runbook_map[normalized], "prong-binding:process_list"
    return DEFAULT_UNRESOLVED_PRONG, "prong-binding:unresolved; ICS:registry-debt"


def count_tranche_prefix(rows: list[dict[str, str]], prefix: str) -> tuple[int, int]:
    """Return (corpint_count, osint_count) for source_ids containing prefix."""
    corp = osint = 0
    for row in rows:
        sid = row.get("source_id", "")
        if prefix not in sid:
            continue
        if row.get("source_category") == "CORPINT":
            corp += 1
        elif row.get("source_category") == "OSINT":
            osint += 1
    return corp, osint


def existing_ids(rows: list[dict[str, str]]) -> set[str]:
    return {row["source_id"] for row in rows if row.get("source_id")}


def existing_urls(rows: list[dict[str, str]]) -> set[str]:
    return {norm_url(row["url"]) for row in rows if row.get("url")}


def append_validated(
    rows: list[dict[str, str]],
    candidates: list[dict[str, str]],
    *,
    id_prefix: str,
    corpint_target: int,
    osint_target: int,
) -> tuple[list[dict[str, str]], int, int]:
    """Append deficit-only rows; return (new_rows, added_corpint, added_osint)."""
    corp_have, osint_have = count_tranche_prefix(rows, id_prefix)
    corp_deficit = max(0, corpint_target - corp_have)
    osint_deficit = max(0, osint_target - osint_have)
    seen_ids = existing_ids(rows)
    seen_urls = existing_urls(rows)
    added_corp = added_osint = 0
    out = list(rows)
    for cand in candidates:
        cat = cand.get("source_category", "")
        if cat == "CORPINT" and corp_deficit <= 0:
            continue
        if cat == "OSINT" and osint_deficit <= 0:
            continue
        row = validate_row_dict(cand)
        if row.source_id in seen_ids:
            continue
        if norm_url(row.url) in seen_urls:
            continue
        dump = row.model_dump()
        out.append(dump)
        seen_ids.add(row.source_id)
        seen_urls.add(norm_url(row.url))
        if cat == "CORPINT":
            corp_deficit -= 1
            added_corp += 1
        else:
            osint_deficit -= 1
            added_osint += 1
    return out, added_corp, added_osint
