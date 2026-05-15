"""Engagement model classification at intake checklist (I73 P3).

Paired SOP: docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md
process_list_id: tbi_peopl_dtp_engagement_model_classification_001
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

ITEM_ID = "tbi_peopl_dtp_engagement_model_classification_001"
SOP_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "SOP-ENGAGEMENT_HIRING_LIFECYCLE_001.md"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Engagement classification intake checklist")
    parser.add_argument("--engagement-id", default="", help="ENGAGEMENT_REGISTRY engagement_id being classified")
    parser.add_argument(
        "--candidate-model",
        default="eng_model_hourly_consultant",
        help="proposed engagement_model_id slug",
    )
    args = parser.parse_args()

    setup_logging(json_output=False)
    logger = logging.getLogger("scripts.peopl_engagement_model_classification_intake")
    log_runbook_pairing(logger, script=Path(__file__).name, sop_path=SOP_PATH, item_id=ITEM_ID)

    eid = args.engagement_id or "(unset — provide --engagement-id)"
    checklist = [
        f"[ ] Engagement instance: {eid}",
        f"[ ] Proposed engagement_model_id={args.candidate_model} exists in ENGAGEMENT_MODEL_REGISTRY.csv",
        "[ ] Pick Clients vs Advisers _engagement-template/ per WORKSPACE_BLUEPRINT §3–§4",
        "[ ] If outsourced_helper — confirm work-product-only SOC briefing captured",
        "[ ] Link FINOPS_COUNTERPARTY_REGISTER slug when payouts expected",
    ]
    print("\n  Engagement model classification at intake (operator checklist)\n")
    for line in checklist:
        print(f"  {line}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
