#!/usr/bin/env python3
"""Cycle staleness canary (Initiative 59 P5).

Reads ``INITIATIVE_REGISTRY.csv`` where ``status='active'`` and computes
``now - last_review`` for each row. Rows older than ``--threshold-days``
(default 14) emit a soft warning. Exit code is always 0 — this script
never blocks the release gate; it only nudges.

Optionally falls back to walking the master-roadmap folder for the most
recent ``reports/*.md`` file modification date when ``last_review`` is empty.

Usage::

    py scripts/check_active_initiative_freshness.py
    py scripts/check_active_initiative_freshness.py --threshold-days 21
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
INITIATIVE_REGISTRY_CSV = HLK_COMPLIANCE / "INITIATIVE_REGISTRY.csv"
PLANNING_DIR = REPO_ROOT / "docs" / "wip" / "planning"

DEFAULT_THRESHOLD_DAYS = 14


def _parse_date(value: str) -> date | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _latest_report_date(folder_path: str) -> date | None:
    """Walk ``reports/*.md`` under the initiative folder for the most recent mtime."""
    reports_dir = REPO_ROOT / folder_path.rstrip("/") / "reports"
    if not reports_dir.is_dir():
        return None
    latest: date | None = None
    for f in reports_dir.glob("*.md"):
        try:
            mtime = date.fromtimestamp(f.stat().st_mtime)
        except OSError:
            continue
        if latest is None or mtime > latest:
            latest = mtime
    return latest


def check_freshness(
    threshold_days: int = DEFAULT_THRESHOLD_DAYS,
    *,
    csv_path: Path | None = None,
    today: date | None = None,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Return ``(stale, fresh)`` lists of active initiative metadata dicts.

    Each dict has keys: ``initiative_id``, ``title``, ``last_review``,
    ``folder_path``, ``days_since``.
    """
    csv_path = csv_path or INITIATIVE_REGISTRY_CSV
    today = today or date.today()
    threshold = timedelta(days=threshold_days)

    if not csv_path.is_file():
        return [], []

    stale: list[dict[str, object]] = []
    fresh: list[dict[str, object]] = []

    with csv_path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if (row.get("status") or "").strip() != "active":
                continue
            iid = (row.get("initiative_id") or "").strip()
            title = (row.get("title") or "").strip()
            folder_path = (row.get("folder_path") or "").strip()
            review = _parse_date(row.get("last_review", ""))
            if review is None:
                review = _latest_report_date(folder_path)
            days_since = (today - review).days if review else None
            entry: dict[str, object] = {
                "initiative_id": iid,
                "title": title,
                "last_review": str(review) if review else "",
                "folder_path": folder_path,
                "days_since": days_since,
            }
            if days_since is None or timedelta(days=days_since) > threshold:
                stale.append(entry)
            else:
                fresh.append(entry)
    return stale, fresh


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--threshold-days",
        type=int,
        default=DEFAULT_THRESHOLD_DAYS,
        help=f"Days since last_review before flagging as stale (default {DEFAULT_THRESHOLD_DAYS}).",
    )
    args = parser.parse_args()

    stale, fresh = check_freshness(args.threshold_days)

    print()
    print("  Active initiative freshness canary (I59 P5)")
    print("  " + "=" * 40)
    print(f"  threshold:   {args.threshold_days} days")
    print(f"  active:      {len(stale) + len(fresh)}")
    print(f"  fresh:       {len(fresh)}")
    print(f"  stale:       {len(stale)}")

    if stale:
        print()
        print("  Stale (soft warning — not blocking):")
        for s in stale:
            days = s["days_since"]
            days_str = f"{days}d ago" if days is not None else "unknown"
            print(f"    - {s['initiative_id']}: last_review={s['last_review'] or '—'} ({days_str}) — {s['title']}")

    if not stale:
        print()
        print("  All active initiatives are within the freshness threshold.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
