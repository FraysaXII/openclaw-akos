"""Apprentice curriculum assignment runbook (I73 P2).

Paired SOP / charter: docs/references/hlk/v3.0/Admin/O5-1/People/Learning/canonicals/LEARNING_CHARTER.md
process_list_id: tbi_peopl_dtp_apprentice_curriculum_assignment_001

Emits a checklist for binding ``eng_model_apprentice_learner`` intakes to the
Holistik Researcher curriculum + ``LEARNING_OPS_BACKLOG.csv``. CSV mutations
stay operator-gated (canonical CSV discipline).
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

ITEM_ID = "tbi_peopl_dtp_apprentice_curriculum_assignment_001"
SOP_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Learning/canonicals/LEARNING_CHARTER.md"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Apprentice curriculum assignment checklist (I73 P2)")
    parser.add_argument("--cohort-id", default="cohort_placeholder_001", help="cohort_id for backlog row")
    parser.add_argument(
        "--engagement-model-id",
        default="eng_model_apprentice_learner",
        help="FK to ENGAGEMENT_MODEL_REGISTRY.csv",
    )
    args = parser.parse_args()

    setup_logging(json_output=False)
    logger = logging.getLogger("scripts.peopl_engagement_apprentice_curriculum_assign")
    log_runbook_pairing(logger, script=Path(__file__).name, sop_path=SOP_PATH, item_id=ITEM_ID)

    checklist = [
        f"[ ] Confirm engagement_model_id={args.engagement_model_id} in ENGAGEMENT_MODEL_REGISTRY.csv",
        "[ ] Open LEARNING_OPS_BACKLOG.csv — ensure cohort row or append via operator PR",
        f"[ ] Set cohort_id={args.cohort_id}; methodology_version_at_onboarding=methodology-anchor",
        "[ ] Assign curriculum path: Learning/canonicals/curriculum/HOLISTIK_RESEARCHER_ONBOARDING_CURRICULUM.md",
        "[ ] Verify Think Big engagement folder uses WORKSPACE_BLUEPRINT _engagement-template/ shape",
    ]
    print("\n  Apprentice curriculum assignment (operator checklist)\n")
    for line in checklist:
        print(f"  {line}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
