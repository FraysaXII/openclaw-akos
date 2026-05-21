"""Seed CAPABILITY_CONFIDENCE_REGISTRY.csv at baseline ``seed_v1_unrated``.

Per D-IH-82-Q (Wave Q CSV 2 seed posture): every capability_id in
CAPABILITY_REGISTRY.csv gets one confidence row at:

- rating_method = seed_v1_unrated
- all 5 axis scores = 1
- aggregate_confidence = 1.0
- rated_by = Capability Curator
- rated_at = today (or override via --as-of)
- last_review_decision_id = D-IH-82-Q

This is the doctrinally-honest seed: no capability has been reviewed; the
infrastructure exists for the I82 P3 quarterly review to flip scores to real
values via ``rating_method=numeric_v1`` (or scp_cameo / plain_register
addendum variants once Marketing/Brand co-signs).

Usage::

    py scripts/seed_capability_confidence_baseline.py --write
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from akos.hlk_capability_confidence_csv import (
    CAPABILITY_CONFIDENCE_FIELDNAMES,
    CSV_PATH_RELATIVE,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_capability_ids(root: Path) -> list[str]:
    cap_csv = (
        root
        / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
        / "dimensions/CAPABILITY_REGISTRY.csv"
    )
    with cap_csv.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return [row["capability_id"] for row in reader]


def build_rows(capability_ids: list[str], as_of: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    suffix = as_of.replace("-", "")
    for cap_id in capability_ids:
        rows.append({
            "confidence_id": f"CONF-{cap_id}-{suffix}",
            "capability_id": cap_id,
            "substrate_score": "1",
            "repeatability_score": "1",
            "quality_score": "1",
            "translatability_score": "1",
            "auditability_score": "1",
            "aggregate_confidence": "1.0",
            "rating_method": "seed_v1_unrated",
            "rated_at": as_of,
            "rated_by": "Capability Curator",
            "notes": (
                "Baseline seed per D-IH-82-Q (Wave Q CSV 2). "
                "Awaits I82 P3 quarterly review for first real rating."
            ),
            "last_review_at": as_of,
            "last_review_by": "Capability Curator",
            "last_review_decision_id": "D-IH-82-Q",
            "methodology_version_at_review": "v3.1",
        })
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default="2026-05-22")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write rows to canonical CSV path (otherwise dry-run prints count).",
    )
    parser.add_argument("--out", default=None, help="Override output path.")
    args = parser.parse_args(argv)

    root = _repo_root()
    capability_ids = _load_capability_ids(root)
    rows = build_rows(capability_ids, args.as_of)

    if not args.write:
        print(f"dry-run: would seed {len(rows)} confidence rows for {len(capability_ids)} capabilities")
        return 0

    out_path = Path(args.out) if args.out else root / CSV_PATH_RELATIVE
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(CAPABILITY_CONFIDENCE_FIELDNAMES))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"seeded {len(rows)} rows -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
