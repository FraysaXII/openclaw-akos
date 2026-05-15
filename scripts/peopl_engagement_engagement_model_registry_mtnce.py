"""Quarterly ENGAGEMENT_MODEL_REGISTRY maintenance checklist (I73 P3).

Paired SOP: docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.md
process_list_id: tbi_peopl_dtp_engagement_model_registry_mtnce_001
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

ITEM_ID = "tbi_peopl_dtp_engagement_model_registry_mtnce_001"
SOP_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "SOP-ENGAGEMENT_MODEL_REGISTRY_MAINTENANCE_001.md"
)


def main() -> int:
    parser = argparse.ArgumentParser(description="ENGAGEMENT_MODEL_REGISTRY quarterly checklist")
    parser.add_argument("--operator", default="People Operations Lead", help="accountable role label")
    args = parser.parse_args()

    setup_logging(json_output=False)
    logger = logging.getLogger("scripts.peopl_engagement_engagement_model_registry_mtnce")
    log_runbook_pairing(logger, script=Path(__file__).name, sop_path=SOP_PATH, item_id=ITEM_ID)

    checklist = [
        "[ ] py scripts/validate_engagement_model_registry.py — PASS",
        "[ ] Scan historical_examples vs internal trajectory codex (no external-register leakage)",
        "[ ] Spot-check ENGAGEMENT_REGISTRY engagement_model_id FK slugs",
        "[ ] If net-new class needed — canonical-CSV pause + operator approval first",
        f"[ ] Accountable role: {args.operator}",
    ]
    print("\n  Engagement model registry maintenance (operator checklist)\n")
    for line in checklist:
        print(f"  {line}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
