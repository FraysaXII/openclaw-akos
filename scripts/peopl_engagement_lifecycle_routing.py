"""Engagement onboarding + lifecycle routing checklist (I73 P3).

Paired SOP: docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/SOP-ENGAGEMENT_ONBOARDING_001.md
process_list_id: tbi_peopl_dtp_engagement_lifecycle_routing_001
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

ITEM_ID = "tbi_peopl_dtp_engagement_lifecycle_routing_001"
SOP_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "SOP-ENGAGEMENT_ONBOARDING_001.md"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Engagement onboarding routing checklist")
    parser.add_argument("--engagement-model-id", default="eng_model_apprentice_learner", help="FK slug")
    args = parser.parse_args()

    setup_logging(json_output=False)
    logger = logging.getLogger("scripts.peopl_engagement_lifecycle_routing")
    log_runbook_pairing(logger, script=Path(__file__).name, sop_path=SOP_PATH, item_id=ITEM_ID)

    checklist = [
        f"[ ] engagement_model_id={args.engagement_model_id}",
        "[ ] Engagement folder copied from Think Big/_engagement-template/ per blueprint",
        "[ ] Apply access_level_default + access_levels.md gates",
        "[ ] Route payroll monitors -> SOP-ENGAGEMENT_PAYROLL_OPS_001",
        "[ ] Route exits / rounds -> SOP-ENGAGEMENT_OFFBOARDING_001",
        "[ ] Apprentices -> scripts/peopl_engagement_apprentice_curriculum_assign.py",
    ]
    print("\n  Engagement onboarding / lifecycle routing (operator checklist)\n")
    for line in checklist:
        print(f"  {line}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
