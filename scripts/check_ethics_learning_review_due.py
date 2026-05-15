"""Advisory checklist for quarterly Ethics + Learning co-review (I73 P5).

Emits an operator-facing checklist plus a staleness advisory when
ETHICAL_AUTOMATION_POSTURE.md ``last_review`` is older than 120 days.

Paired SOP: docs/references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/SOP-ETHICS_LEARNING_REVIEW_001.md
process_list_id: hol_peopl_dtp_316
"""
from __future__ import annotations

import argparse
import logging
import re
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.log import setup_logging
from akos.peopl_engagement_runbooks import log_runbook_pairing

ITEM_ID = "hol_peopl_dtp_316"
SOP_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/"
    "SOP-ETHICS_LEARNING_REVIEW_001.md"
)
ETHICAL_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Ethics"
    / "canonicals"
    / "ETHICAL_AUTOMATION_POSTURE.md"
)
STALE_AFTER_DAYS = 120
_LAST_REVIEW_RE = re.compile(r"^last_review:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


def _parse_last_review_iso(md_path: Path) -> date | None:
    raw = md_path.read_text(encoding="utf-8", errors="replace")
    m = _LAST_REVIEW_RE.search(raw)
    if not m:
        return None
    return datetime.strptime(m.group(1), "%Y-%m-%d").date()


def main() -> int:
    parser = argparse.ArgumentParser(description="Ethics + Learning quarterly review advisory checklist")
    parser.add_argument(
        "--today",
        default="",
        help="ISO date YYYY-MM-DD for deterministic checks (default: system date)",
    )
    args = parser.parse_args()

    setup_logging(json_output=False)
    logger = logging.getLogger("scripts.check_ethics_learning_review_due")
    log_runbook_pairing(logger, script=Path(__file__).name, sop_path=SOP_PATH, item_id=ITEM_ID)

    today = date.fromisoformat(args.today) if args.today.strip() else date.today()

    last_review = _parse_last_review_iso(ETHICAL_PATH)
    delta_days = (today - last_review).days if last_review else None

    checklist = [
        "[ ] Confirm ETHICAL_AUTOMATION_POSTURE.md §2.5 quarterly cadence scheduled",
        "[ ] Confirm LEARNING_CHARTER.md methodology-anchor stamp matches doctrine expectation",
        "[ ] Learning Curator co-attendee booked / reschedule logged",
        "[ ] Escalate to founder if §5 starvation clause triggers",
    ]

    print("\n  Quarterly Ethics + Learning co-review (advisory checklist)\n")
    for line in checklist:
        print(f"  {line}")

    print("\n  Evidence:")
    print(f"  ETHICAL_AUTOMATION_POSTURE.md path: {ETHICAL_PATH.relative_to(REPO_ROOT)}")
    if last_review is None:
        print("  last_review field: MISSING (fix YAML frontmatter)")
    else:
        print(f"  last_review field: {last_review.isoformat()} ({delta_days} days before --today)")

    if delta_days is not None and delta_days >= STALE_AFTER_DAYS:
        print(
            f"\n  [ADVISORY] Posture last_review is >= {STALE_AFTER_DAYS} days stale "
            "-- queue OPERATOR_INBOX / governance review."
        )
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
