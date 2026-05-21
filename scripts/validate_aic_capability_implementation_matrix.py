"""Validate AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv per I86 Wave R + D-IH-86-CQ.

Checks:

1. Header matches ``AIC_CAPABILITY_IMPLEMENTATION_MATRIX_FIELDNAMES`` SSOT.
2. Every row passes the Pydantic contract (AICCapabilityImplementationMatrixRow).
3. ``matrix_id`` uniqueness.
4. ``capability_id`` FK-resolves into CAPABILITY_REGISTRY.csv.
5. ``aic_id`` FK-resolves into AIC_REGISTRY.csv.
6. ``paired_madeira_task_id`` (when non-empty) FK-resolves into
   MADEIRA_AIC_PER_TASK_REGISTRY.csv AND the matching ``aic_id`` matches the
   task row's ``aic_id`` (no cross-AIC leakage).
7. ``realisation_refs`` (when non-empty; semicolon-list) each FK-resolves into
   USE_CASE_ARCHIVE.csv.
8. ``last_review_decision_id`` references a row in DECISION_REGISTER.csv.
9. (capability_id, aic_id) pair uniqueness (no duplicate cells).
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from pydantic import ValidationError

from akos.hlk_aic_capability_implementation_matrix_csv import (
    AIC_CAPABILITY_IMPLEMENTATION_MATRIX_FIELDNAMES,
    CSV_PATH_RELATIVE,
    AICCapabilityImplementationMatrixRow,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_lookup(path: Path, key: str) -> set[str]:
    if not path.exists():
        return set()
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return {row[key] for row in reader if row.get(key)}


def _load_madeira_task_to_aic(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return {row["task_id"]: row["aic_id"] for row in reader if row.get("task_id")}


def validate(csv_path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if not csv_path.exists():
        return False, [f"missing CSV: {csv_path}"]

    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        rows = list(reader)

    expected = list(AIC_CAPABILITY_IMPLEMENTATION_MATRIX_FIELDNAMES)
    if header != expected:
        errors.append(f"header mismatch: got {header} expected {expected}")
        return False, errors

    root = _repo_root()
    canonicals = root / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
    capability_ids = _load_lookup(canonicals / "dimensions/CAPABILITY_REGISTRY.csv", "capability_id")
    aic_ids = _load_lookup(canonicals / "dimensions/AIC_REGISTRY.csv", "aic_id")
    use_case_ids = _load_lookup(canonicals / "dimensions/USE_CASE_ARCHIVE.csv", "use_case_id")
    madeira_task_to_aic = _load_madeira_task_to_aic(
        canonicals / "dimensions/MADEIRA_AIC_PER_TASK_REGISTRY.csv"
    )
    decision_ids = _load_lookup(canonicals / "DECISION_REGISTER.csv", "decision_id")

    seen_ids: set[str] = set()
    seen_pairs: set[tuple[str, str]] = set()
    for idx, raw in enumerate(rows, start=2):
        try:
            AICCapabilityImplementationMatrixRow(**raw)
        except (ValidationError, ValueError) as exc:
            errors.append(f"row {idx} ({raw.get('matrix_id', '?')}): {exc}")
            continue

        mid = raw["matrix_id"]
        if mid in seen_ids:
            errors.append(f"row {idx}: duplicate matrix_id '{mid}'")
        seen_ids.add(mid)

        cap_id = raw["capability_id"]
        aic_id = raw["aic_id"]
        pair = (cap_id, aic_id)
        if pair in seen_pairs:
            errors.append(
                f"row {idx} ({mid}): duplicate (capability_id, aic_id) pair {pair}"
            )
        seen_pairs.add(pair)

        if capability_ids and cap_id not in capability_ids:
            errors.append(
                f"row {idx} ({mid}): capability_id '{cap_id}' does not resolve to CAPABILITY_REGISTRY"
            )

        if aic_ids and aic_id not in aic_ids:
            errors.append(
                f"row {idx} ({mid}): aic_id '{aic_id}' does not resolve to AIC_REGISTRY"
            )

        task_id = raw.get("paired_madeira_task_id", "")
        if task_id:
            if madeira_task_to_aic and task_id not in madeira_task_to_aic:
                errors.append(
                    f"row {idx} ({mid}): paired_madeira_task_id '{task_id}' does not resolve to MADEIRA_AIC_PER_TASK_REGISTRY"
                )
            elif madeira_task_to_aic and madeira_task_to_aic[task_id] != aic_id:
                errors.append(
                    f"row {idx} ({mid}): paired_madeira_task_id '{task_id}' belongs to "
                    f"AIC '{madeira_task_to_aic[task_id]}' not '{aic_id}'"
                )

        refs = raw.get("realisation_refs", "")
        if refs and use_case_ids:
            for ref in [r.strip() for r in refs.split(";") if r.strip()]:
                if ref not in use_case_ids:
                    errors.append(
                        f"row {idx} ({mid}): realisation_ref '{ref}' does not resolve to USE_CASE_ARCHIVE"
                    )

        dec_id = raw.get("last_review_decision_id", "")
        if dec_id and decision_ids and dec_id not in decision_ids:
            errors.append(
                f"row {idx} ({mid}): last_review_decision_id '{dec_id}' missing from DECISION_REGISTER"
            )

    return not errors, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        default=str(_repo_root() / CSV_PATH_RELATIVE),
        help="Path to AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv",
    )
    args = parser.parse_args(argv)

    ok, errors = validate(Path(args.csv))
    if ok:
        print(f"validate_aic_capability_implementation_matrix: PASS ({args.csv})")
        return 0
    print(f"validate_aic_capability_implementation_matrix: FAIL ({len(errors)} errors)")
    for err in errors[:50]:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
