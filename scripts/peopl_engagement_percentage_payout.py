"""Percentage collaborator payout reconciliation checklist (I73 P3).

Paired SOP: docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/SOP-ENGAGEMENT_PAYROLL_OPS_001.md
process_list_id: tbi_peopl_dtp_percentage_collaborator_payout_001
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

ITEM_ID = "tbi_peopl_dtp_percentage_collaborator_payout_001"
SOP_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "SOP-ENGAGEMENT_PAYROLL_OPS_001.md"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Percentage collaborator payout checklist")
    parser.add_argument("--deal-ref", default="", help="registered_fact / deal reference label")
    args = parser.parse_args()

    setup_logging(json_output=False)
    logger = logging.getLogger("scripts.peopl_engagement_percentage_payout")
    log_runbook_pairing(logger, script=Path(__file__).name, sop_path=SOP_PATH, item_id=ITEM_ID)

    deal = args.deal_ref or "(provide deal / registered_fact reference)"
    checklist = [
        f"[ ] Deal / fact: {deal}",
        "[ ] Confirm engagement_model_id=eng_model_percentage_collaborator",
        "[ ] Pull collaborator-share agreement terms",
        "[ ] Link payout counterparty via FINOPS_COUNTERPARTY_REGISTER slug (no duplicate SSOT)",
        "[ ] Queue payout + archive evidence to engagement folder",
    ]
    print("\n  Percentage collaborator payout reconciliation (operator checklist)\n")
    for line in checklist:
        print(f"  {line}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
