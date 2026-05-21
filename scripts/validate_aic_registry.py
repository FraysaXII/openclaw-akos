"""Validate AIC_REGISTRY.csv per I82 P4 + D-IH-82-S (Wave Q CSV 4 parent).

Checks:

1. Header matches ``AIC_REGISTRY_FIELDNAMES`` SSOT.
2. Every row passes the Pydantic contract (AICRegistryRow).
3. ``aic_id`` uniqueness.
4. ``substrate_id`` FK-resolves into SUBSTRATE_REGISTRY.csv.
5. ``last_review_decision_id`` references a row in DECISION_REGISTER.csv.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from pydantic import ValidationError

from akos.hlk_aic_registry_csv import (
    AIC_REGISTRY_FIELDNAMES,
    CSV_PATH_RELATIVE,
    AICRegistryRow,
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

    expected = list(AIC_REGISTRY_FIELDNAMES)
    if header != expected:
        errors.append(f"header mismatch: got {header} expected {expected}")
        return False, errors

    root = _repo_root()
    substrate_ids = _load_lookup(
        root
        / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
        / "dimensions/SUBSTRATE_REGISTRY.csv",
        "substrate_id",
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
            AICRegistryRow(**raw)
        except (ValidationError, ValueError) as exc:
            errors.append(f"row {idx} ({raw.get('aic_id', '?')}): {exc}")
            continue

        aid = raw["aic_id"]
        if aid in seen_ids:
            errors.append(f"row {idx}: duplicate aic_id '{aid}'")
        seen_ids.add(aid)

        sub_id = raw["substrate_id"]
        if substrate_ids and sub_id not in substrate_ids:
            errors.append(
                f"row {idx} ({aid}): substrate_id '{sub_id}' does not resolve to SUBSTRATE_REGISTRY"
            )

        dec_id = raw.get("last_review_decision_id", "")
        if dec_id and decision_ids and dec_id not in decision_ids:
            errors.append(
                f"row {idx} ({aid}): last_review_decision_id '{dec_id}' missing from DECISION_REGISTER"
            )

    return not errors, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        default=str(_repo_root() / CSV_PATH_RELATIVE),
        help="Path to AIC_REGISTRY.csv",
    )
    args = parser.parse_args(argv)

    ok, errors = validate(Path(args.csv))
    if ok:
        print(f"validate_aic_registry: PASS ({args.csv})")
        return 0
    print(f"validate_aic_registry: FAIL ({len(errors)} errors)")
    for err in errors[:50]:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
