"""Outsourced helper quarterly SOC review checklist (I73 P3).

Paired SOP: docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/SOP-ENGAGEMENT_PAYROLL_OPS_001.md
process_list_id: tbi_peopl_dtp_outsourced_helper_soc_review_001
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.log import setup_logging
from akos.peopl_engagement_runbooks import log_runbook_pairing

ITEM_ID = "tbi_peopl_dtp_outsourced_helper_soc_review_001"
SOP_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "SOP-ENGAGEMENT_PAYROLL_OPS_001.md"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Outsourced helper SOC review checklist")
    parser.add_argument("--engagement-id", default="", help="specific engagement row id / slug")
    args = parser.parse_args()

    setup_logging(json_output=False)
    logger = logging.getLogger("scripts.peopl_engagement_outsourced_soc_review")
    log_runbook_pairing(logger, script=Path(__file__).name, sop_path=SOP_PATH, item_id=ITEM_ID)

    label = args.engagement_id or "(scan all eng_model_outsourced_helper rows)"
    checklist = [
        f"[ ] Scope: {label}",
        "[ ] Verify access_level stays 1–2 for outsourced_helper engagements",
        "[ ] Confirm methodology exposure = none (work-product-only)",
        "[ ] Validate capped compensation clauses where €400/mo cap applies",
        "[ ] Log findings under engagement 00-internal/checkpoints/",
    ]
    print("\n  Outsourced helper SOC review (operator checklist)\n")
    for line in checklist:
        print(f"  {line}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
