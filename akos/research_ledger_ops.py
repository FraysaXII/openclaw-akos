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

# Holistika area (process_list ``area`` column) → baseline consumer prong (BL-*).
# SSOT: docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_PRONG_LATTICE_DISCIPLINE.md
AREA_TO_BASELINE_PRONG: dict[str, str] = {
    "Tech": "BL-TECH",
    "Data": "BL-DATA",
    "Operations": "BL-OPS",
    "Research": "BL-RESEARCH",
    "People": "BL-PEOPLE",
    "Finance": "BL-FIN",
    "Legal": "BL-LEGAL",
    "Marketing": "BL-MKT",
    "MKT": "BL-MKT",
}

# Charter alias → baseline (holistic-agentic + Automation OS packs).
CHARTER_ALIAS_TO_BASELINE: dict[str, str] = {
    # Holistic-agentic
    "P1-DATA": "BL-DATA",
    "P2-FINANCE": "BL-FIN",
    "P3-LEGAL": "BL-LEGAL",
    "P4-MARKETING": "BL-MKT",
    "P5-OPS-PEOPLE": "BL-OPS",
    "P6-TECH-SUBSTRATE": "BL-TECH",
    "P7-RESEARCH": "BL-RESEARCH",
    "P8-MADEIRA": "BL-ENVOY",
    # Automation OS
    "P1-TECH": "BL-TECH",
    "P2-DATA": "BL-DATA",
    "P3-OPS": "BL-OPS",
    "P4-RESEARCH": "BL-RESEARCH",
    "P5-PEOPLE": "BL-PEOPLE",
    "P6-COMPLIANCE": "BL-COMPLY",
    "P7-FINANCE": "BL-FIN",
    "P8-LEGAL": "BL-LEGAL",
    "P9-MARKETING": "BL-MKT",
    "P10-INTEL-OPS": "BL-INTEL",
    "P11-ENVOY-MADEIRA": "BL-ENVOY",
    "P12-RPA-ADAPTERS": "BL-ADAPTER",
    # Automation OS R1 legacy charter id (agent CLI / monorepo OSINT block)
    "P7-AGENT-CLI": "BL-ENVOY",
    # WIP ledger typo alias (GOJ + analytics packs, 2026-06-12)
    "BL-FINANCE": "BL-FIN",
}

BASELINE_PRONG_IDS = frozenset(
    {
        "BL-DATA",
        "BL-FIN",
        "BL-LEGAL",
        "BL-MKT",
        "BL-OPS",
        "BL-PEOPLE",
        "BL-TECH",
        "BL-RESEARCH",
        "BL-COMPLY",
        "BL-INTEL",
        "BL-ENVOY",
        "BL-ADAPTER",
        "BL-UX",
        "BL-ETHICS",
    }
)

DEFAULT_UNRESOLVED_PRONG = "BL-TECH"

# Back-compat alias for imports/tests written before BL-* mint.
AREA_TO_PRONG = CHARTER_ALIAS_TO_BASELINE

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


def normalize_prong(raw: str | None) -> str:
    """Map charter alias or legacy tag to baseline ``BL-*`` consumer prong."""
    if not raw:
        return DEFAULT_UNRESOLVED_PRONG
    key = raw.strip().upper()
    if key in BASELINE_PRONG_IDS:
        return key
    return CHARTER_ALIAS_TO_BASELINE.get(key, key)


def validate_row_dict(raw: dict[str, Any]) -> ResearchSourceRow:
    payload = dict(raw)
    if "prong" in payload:
        payload["prong"] = normalize_prong(str(payload.get("prong", "")))
    return ResearchSourceRow.model_validate(payload)


def normalize_ledger_prong_rows(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], int]:
    """Rewrite ``prong`` cells to baseline ``BL-*`` IDs; return (rows, changed_count)."""
    out: list[dict[str, str]] = []
    changed = 0
    for raw in rows:
        prior = (raw.get("prong") or "").strip()
        normalized = normalize_prong(prior)
        if normalized != prior:
            changed += 1
        row = dict(raw)
        row["prong"] = normalized
        out.append(row)
    return out, changed


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
            prong = AREA_TO_BASELINE_PRONG.get(area, DEFAULT_UNRESOLVED_PRONG)
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
        return normalize_prong(manifest_prong), "prong-binding:manifest"
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
