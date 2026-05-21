#!/usr/bin/env python3
"""Seed CAPABILITY_REGISTRY.csv from I81 kb-integrity-matrix (Wave Q CSV 1).

Operator ratified seed-all-pass-rows at Wave P close (2026-05-22). The matrix
uses verdict=partial for all rows (0 pass); D-IH-82-P records full-matrix seed
as the operator's full-coverage intent.

Usage::

    py scripts/seed_capability_registry_from_i81_matrix.py
    py scripts/seed_capability_registry_from_i81_matrix.py --dry-run
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_capability_registry_csv import (  # noqa: E402
    CAPABILITY_REGISTRY_FIELDNAMES,
    TALENT_A_ROLE_HINTS,
)

MATRIX_PATH = (
    REPO_ROOT
    / "docs/wip/planning/81-vault-integrity-layout-milestones-retrofit"
    / "reports/i81/kb-integrity-matrix-2026-05-22.csv"
)
OUT_PATH = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    / "dimensions/CAPABILITY_REGISTRY.csv"
)

DECISION_ID = "D-IH-82-P"
REVIEW_DATE = "2026-05-22"


def item_id_to_capability_id(item_id: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", item_id.lower()).strip("-").upper()
    return f"CAP-{slug}"


def infer_bearer_class(role_owner: str) -> str:
    if role_owner in TALENT_A_ROLE_HINTS or "MADEIRA" in role_owner.upper():
        return "Talent-A"
    if role_owner in {"AIC", "AI Engineer"}:
        return "Talent-A"
    return "Talent-H"


def infer_lifecycle(i81_verdict: str, paired_sop: str) -> str:
    if paired_sop == "matched" and i81_verdict == "partial":
        return "active"
    if i81_verdict == "fail":
        return "scaffold"
    return "planned"


def build_rows() -> list[dict[str, str]]:
    if not MATRIX_PATH.is_file():
        raise FileNotFoundError(MATRIX_PATH)
    process_csv = (
        REPO_ROOT
        / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
        / "process_list.csv"
    )
    process_roles: dict[str, str] = {}
    if process_csv.is_file():
        with process_csv.open(encoding="utf-8", newline="") as pf:
            for prow in csv.DictReader(pf):
                iid = (prow.get("item_id") or "").strip()
                owner = (prow.get("role_owner") or "").strip()
                if iid and owner:
                    process_roles[iid] = owner
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    with MATRIX_PATH.open(encoding="utf-8", newline="") as fh:
        for src in csv.DictReader(fh):
            item_id = (src.get("item_id") or "").strip()
            if not item_id or item_id in seen:
                continue
            seen.add(item_id)
            role_owner = process_roles.get(item_id) or (src.get("role_owner") or "PMO").strip()
            if role_owner in {"Process Owner", "TBD"}:
                role_owner = "PMO"
            area = (src.get("area") or "Operations").strip()
            name = (src.get("item_name") or item_id).strip()
            verdict = (src.get("verdict") or "partial").strip().lower()
            if verdict not in {"pass", "partial", "fail"}:
                verdict = "partial"
            paired = (src.get("paired_sop_status") or "").strip()
            cap_id = item_id_to_capability_id(item_id)
            rows.append({
                "capability_id": cap_id,
                "capability_name": name[:200],
                "bearer_class": infer_bearer_class(role_owner),
                "area": area,
                "role_owner": role_owner,
                "originating_process_ids": item_id,
                "substrate_id": "",
                "skill_ids": "",
                "lifecycle_status": infer_lifecycle(verdict, paired),
                "i81_verdict": verdict,
                "i81_gap_summary": (src.get("gap_summary") or "")[:500],
                "external_register_summary": "",
                "last_review_at": REVIEW_DATE,
                "last_review_by": "Capability Curator",
                "last_review_decision_id": DECISION_ID,
                "methodology_version_at_review": "v3.1",
                "notes": "Seeded from I81 kb-integrity-matrix per D-IH-82-P",
            })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    rows = build_rows()
    if args.dry_run:
        print(f"Would write {len(rows)} rows to {OUT_PATH.relative_to(REPO_ROOT)}")
        return 0
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(CAPABILITY_REGISTRY_FIELDNAMES))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {OUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
