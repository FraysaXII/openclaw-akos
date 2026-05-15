"""Investor advisor round review checklist (I73 P3).

Paired SOP: docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/SOP-ENGAGEMENT_OFFBOARDING_001.md
process_list_id: tbi_peopl_dtp_investor_advisor_round_review_001
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

ITEM_ID = "tbi_peopl_dtp_investor_advisor_round_review_001"
SOP_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "SOP-ENGAGEMENT_OFFBOARDING_001.md"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Investor advisor round review checklist")
    parser.add_argument("--round-label", default="", help="round name / date stamp")
    args = parser.parse_args()

    setup_logging(json_output=False)
    logger = logging.getLogger("scripts.peopl_engagement_investor_round_review")
    log_runbook_pairing(logger, script=Path(__file__).name, sop_path=SOP_PATH, item_id=ITEM_ID)

    rnd = args.round_label or "(label this financing round)"
    checklist = [
        f"[ ] Round label: {rnd}",
        "[ ] engagement_model_id=eng_model_investor_advisor",
        "[ ] Cap-table sanity + SAFE/convertible status",
        "[ ] Advisor grant vesting checkpoints",
        "[ ] If methodology IP surfaced — note D-IH-73-F filing matrix deferral",
        "[ ] Prepare archive/offboarding handoff per SOP-ENGAGEMENT_OFFBOARDING_001",
    ]
    print("\n  Investor advisor round review (operator checklist)\n")
    for line in checklist:
        print(f"  {line}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
