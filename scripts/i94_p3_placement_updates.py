#!/usr/bin/env python3
"""I94 P3 placement: IntelligenceOps path fixes + Engagement AREA-16 FK."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_process_csv import normalize_process_row, write_process_csv

PL = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv"
BL = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv"

OLD_PREFIX = "docs/references/hlk/v3.0/Admin/O5-1/Operations/IntelligenceOps/"
NEW_PREFIX = "docs/references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/"

IO_SOP_PATHS = {
    "hol_res_prc_counterparty_baseline_assess_001": (
        f"{NEW_PREFIX}SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md",
        "scripts/validate_research_action.py",
    ),
    "hol_res_prc_elicitation_discipline_001": (
        f"{NEW_PREFIX}SOP-IO_ELICITATION_DISCIPLINE_001.md",
        "scripts/validate_research_action.py",
    ),
    "hol_res_prc_reliability_grading_001": (
        f"{NEW_PREFIX}SOP-IO_RELIABILITY_GRADING_001.md",
        "scripts/validate_research_action.py",
    ),
    "hol_res_prc_intelligence_report_001": (
        f"{NEW_PREFIX}SOP-IO_INTELLIGENCE_REPORT_001.md",
        "scripts/validate_research_action.py",
    ),
}


def main() -> int:
    rows: list[dict[str, str]] = []
    with PL.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            rows.append(normalize_process_row(row))

    for row in rows:
        iid = (row.get("item_id") or "").strip()
        if iid == "hol_res_prj_intelligence_ops_001":
            instr = (row.get("instructions") or "").replace(OLD_PREFIX, NEW_PREFIX)
            row["instructions"] = instr
        if iid in IO_SOP_PATHS:
            sop, rb = IO_SOP_PATHS[iid]
            row["instructions"] = sop
            row["sop_path"] = sop
            row["runbook_path"] = rb
            row["last_review_at"] = "2026-06-10"
            row["last_review_decision_id"] = "D-IH-94-C"

    write_process_csv(PL, rows)

    bl_rows: list[dict[str, str]] = []
    with BL.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            if (row.get("role_name") or "").strip() == "PMO":
                row["sub_area"] = "Engagement"
                row["last_review_at"] = "2026-06-10"
                row["last_review_decision_id"] = "D-IH-94-C"
            bl_rows.append(row)

    with BL.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(bl_rows)

    print("P3 placement updates applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
