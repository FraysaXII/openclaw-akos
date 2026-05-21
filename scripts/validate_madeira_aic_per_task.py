"""Validate MADEIRA_AIC_PER_TASK_REGISTRY.csv per I82 P4 + D-IH-82-S (Wave Q CSV 4 child).

Checks:

1. Header matches ``MADEIRA_AIC_PER_TASK_FIELDNAMES`` SSOT.
2. Every row passes the Pydantic contract (MadeiraAICPerTaskRow).
3. ``task_id`` uniqueness.
4. ``aic_id`` FK-resolves into AIC_REGISTRY.csv AND must match ``AIC-MADEIRA-*``.
5. ``last_review_decision_id`` references a row in DECISION_REGISTER.csv.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from pydantic import ValidationError

from akos.hlk_madeira_aic_per_task_csv import (
    CSV_PATH_RELATIVE,
    MADEIRA_AIC_PER_TASK_FIELDNAMES,
    MadeiraAICPerTaskRow,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_lookup(path: Path, key: str) -> set[str]:
    if not path.exists():
        return set()
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return {row[key] for row in reader if row.get(key)}


def validate(csv_path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if not csv_path.exists():
        return False, [f"missing CSV: {csv_path}"]

    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        rows = list(reader)

    expected = list(MADEIRA_AIC_PER_TASK_FIELDNAMES)
    if header != expected:
        errors.append(f"header mismatch: got {header} expected {expected}")
        return False, errors

    root = _repo_root()
    aic_ids = _load_lookup(
        root
        / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
        / "dimensions/AIC_REGISTRY.csv",
        "aic_id",
    )
    decision_ids = _load_lookup(
        root
        / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
        / "DECISION_REGISTER.csv",
        "decision_id",
    )

    seen_ids: set[str] = set()
    for idx, raw in enumerate(rows, start=2):
        try:
            MadeiraAICPerTaskRow(**raw)
        except (ValidationError, ValueError) as exc:
            errors.append(f"row {idx} ({raw.get('task_id', '?')}): {exc}")
            continue

        tid = raw["task_id"]
        if tid in seen_ids:
            errors.append(f"row {idx}: duplicate task_id '{tid}'")
        seen_ids.add(tid)

        aid = raw["aic_id"]
        if aic_ids and aid not in aic_ids:
            errors.append(
                f"row {idx} ({tid}): aic_id '{aid}' does not resolve to AIC_REGISTRY"
            )

        dec_id = raw.get("last_review_decision_id", "")
        if dec_id and decision_ids and dec_id not in decision_ids:
            errors.append(
                f"row {idx} ({tid}): last_review_decision_id '{dec_id}' missing from DECISION_REGISTER"
            )

    return not errors, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        default=str(_repo_root() / CSV_PATH_RELATIVE),
        help="Path to MADEIRA_AIC_PER_TASK_REGISTRY.csv",
    )
    args = parser.parse_args(argv)

    ok, errors = validate(Path(args.csv))
    if ok:
        print(f"validate_madeira_aic_per_task: PASS ({args.csv})")
        return 0
    print(f"validate_madeira_aic_per_task: FAIL ({len(errors)} errors)")
    for err in errors[:50]:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
