#!/usr/bin/env python3
"""Validate LEARNING_OPS_BACKLOG.csv (People/Learning; I73 P2 / P95-GOV-4).

Header drift gate + Pydantic row validation + unique cohort_id +
engagement_model_id FK to ENGAGEMENT_MODEL_REGISTRY.csv.

Usage::

    py scripts/validate_learning_ops_backlog.py
    py scripts/validate_learning_ops_backlog.py --self-test
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_learning_ops_backlog_csv import (  # noqa: E402
    CANONICAL_PATH,
    LEARNING_OPS_BACKLOG_FIELDNAMES,
    LearningOpsBacklogRow,
)
from akos.io import REPO_ROOT  # noqa: E402
from akos.log import setup_logging  # noqa: E402

CSV_PATH = REPO_ROOT / CANONICAL_PATH
ENGAGEMENT_MODEL_PATH = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions"
    / "ENGAGEMENT_MODEL_REGISTRY.csv"
)


def _load_engagement_model_ids() -> set[str]:
    if not ENGAGEMENT_MODEL_PATH.is_file():
        return set()
    with ENGAGEMENT_MODEL_PATH.open(encoding="utf-8", newline="") as fh:
        return {
            (row.get("engagement_model_id") or "").strip()
            for row in csv.DictReader(fh)
            if row.get("engagement_model_id")
        }


def validate(path: Path = CSV_PATH) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return False, [f"LEARNING_OPS_BACKLOG.csv not found at {path}"]

    model_ids = _load_engagement_model_ids()
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if list(reader.fieldnames or []) != list(LEARNING_OPS_BACKLOG_FIELDNAMES):
            return False, [
                "header mismatch: expected "
                f"{list(LEARNING_OPS_BACKLOG_FIELDNAMES)}, got {reader.fieldnames}"
            ]
        rows = list(reader)

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        try:
            LearningOpsBacklogRow.model_validate({k: (v or "") for k, v in row.items() if k})
        except Exception as exc:  # noqa: BLE001
            cid = (row.get("cohort_id") or f"row_{i}").strip()
            errors.append(f"row {i} ({cid}): {exc}")
            continue

        cid = (row.get("cohort_id") or "").strip()
        if cid in seen:
            errors.append(f"row {i}: duplicate cohort_id {cid!r}")
        seen.add(cid)

        emid = (row.get("engagement_model_id") or "").strip()
        if model_ids and emid not in model_ids:
            errors.append(f"row {i} ({cid}): engagement_model_id {emid!r} not in ENGAGEMENT_MODEL_REGISTRY")

    return not errors, errors


def self_test() -> int:
    ok_row = LearningOpsBacklogRow.model_validate({
        "cohort_id": "cohort_test_001",
        "engagement_model_id": "eng_model_apprentice_learner",
        "methodology_version_at_onboarding": "methodology-anchor",
        "start_date": "2026-05-15",
        "status": "planned",
        "notes": "",
    })
    assert ok_row.cohort_id == "cohort_test_001"
    try:
        LearningOpsBacklogRow.model_validate({
            "cohort_id": "bad",
            "engagement_model_id": "eng_model_apprentice_learner",
            "methodology_version_at_onboarding": "methodology-anchor",
            "start_date": "2026-05-15",
            "status": "planned",
            "notes": "",
        })
        return 1
    except Exception:
        pass
    print("PASS: validate_learning_ops_backlog self-test")
    return 0


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description="Validate LEARNING_OPS_BACKLOG.csv")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    logger.debug("LEARNING_OPS_BACKLOG validator invoked")
    print("\n  LEARNING_OPS_BACKLOG Validator")
    print("  " + "=" * 50)
    ok, errors = validate()
    if ok:
        with CSV_PATH.open(encoding="utf-8", newline="") as fh:
            count = sum(1 for _ in csv.DictReader(fh))
        print(f"  PASS: LEARNING_OPS_BACKLOG ({count} rows)")
        return 0
    print(f"  FAIL: LEARNING_OPS_BACKLOG ({len(errors)} error(s))")
    for err in errors:
        print(f"    - {err}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
