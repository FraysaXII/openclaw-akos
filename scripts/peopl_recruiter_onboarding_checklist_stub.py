"""Bootstrap ASCII checklist for recruiter onboarding brief (I73 closure).

Thin paired runbook for process_list row tbi_peopl_dtp_recruiter_onboarding_001.
Always exits 0.

Paired SOP: docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/SOP-RECRUITER_ONBOARDING_001.md
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

ITEM_ID = "tbi_peopl_dtp_recruiter_onboarding_001"
SOP_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "SOP-RECRUITER_ONBOARDING_001.md"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Recruiter onboarding brief checklist (stub)")
    parser.parse_args()

    setup_logging(json_output=False)
    logger = logging.getLogger("scripts.peopl_recruiter_onboarding_checklist_stub")
    log_runbook_pairing(logger, script=Path(__file__).name, sop_path=SOP_PATH, item_id=ITEM_ID)

    checklist = [
        "[ ] Roles-needed table (title / seniority / must-have)",
        "[ ] Urgency + hiring-manager availability",
        "[ ] Channel: own-site vs portal-mediated",
        "[ ] engagement_model_id preset from ENGAGEMENT_MODEL_REGISTRY",
        "[ ] Outsourced SOC note if portal / low-trust flow",
        "[ ] IntelligenceOps IO-REC-PLACEHOLDER-001 output_artifact path reserved",
    ]

    print("\n  Recruiter onboarding brief (bootstrap checklist)\n")
    for line in checklist:
        print(f"  {line}")
    print("\n  See SOP-RECRUITER_ONBOARDING_001.md for full RACI + cross-links.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
