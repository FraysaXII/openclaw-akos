"""Validate CAPABILITY_CONFIDENCE_REGISTRY.csv per I82 P3 + D-IH-82-Q.

Checks:

1. Header matches ``CAPABILITY_CONFIDENCE_FIELDNAMES`` SSOT.
2. Every row passes the Pydantic contract (CapabilityConfidenceRow), including
   the aggregate_confidence-equals-mean invariant from HOLISTIKA_CAPABILITY_DOCTRINE.md §6.
3. ``confidence_id`` uniqueness (no duplicate confidence rows for same capability + date).
4. ``capability_id`` FK-resolves into CAPABILITY_REGISTRY.csv.
5. ``last_review_decision_id`` references a row in DECISION_REGISTER.csv when non-empty.
6. ``rated_by`` references a role_name in baseline_organisation.csv.

Exit 0 on PASS; 1 on FAIL.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from pydantic import ValidationError

from akos.hlk_capability_confidence_csv import (
    CAPABILITY_CONFIDENCE_FIELDNAMES,
    CSV_PATH_RELATIVE,
    CapabilityConfidenceRow,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader), reader.fieldnames or []


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

    rows, header = _load_csv(csv_path)
    expected = list(CAPABILITY_CONFIDENCE_FIELDNAMES)
    if header != expected:
        errors.append(f"header mismatch: got {header} expected {expected}")
        return False, errors

    root = _repo_root()
    capability_ids = _load_lookup(
        root
        / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
        / "dimensions/CAPABILITY_REGISTRY.csv",
        "capability_id",
    )
    decision_ids = _load_lookup(
        root
        / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
        / "DECISION_REGISTER.csv",
        "decision_id",
    )
    baseline_roles = _load_lookup(
        root
        / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
        / "baseline_organisation.csv",
        "role_name",
    )

    seen_ids: set[str] = set()
    for idx, raw in enumerate(rows, start=2):
        try:
            normalised = {
                k: int(v) if k.endswith("_score") and v != "" else v
                for k, v in raw.items()
            }
            if "aggregate_confidence" in normalised and normalised["aggregate_confidence"] != "":
                normalised["aggregate_confidence"] = float(normalised["aggregate_confidence"])
            CapabilityConfidenceRow(**normalised)
        except (ValidationError, ValueError) as exc:
            errors.append(f"row {idx} ({raw.get('confidence_id', '?')}): {exc}")
            continue

        cid = raw["confidence_id"]
        if cid in seen_ids:
            errors.append(f"row {idx}: duplicate confidence_id '{cid}'")
        seen_ids.add(cid)

        cap_id = raw["capability_id"]
        if capability_ids and cap_id not in capability_ids:
            errors.append(
                f"row {idx} ({cid}): capability_id '{cap_id}' does not resolve to CAPABILITY_REGISTRY"
            )

        dec_id = raw.get("last_review_decision_id", "")
        if dec_id and decision_ids and dec_id not in decision_ids:
            errors.append(
                f"row {idx} ({cid}): last_review_decision_id '{dec_id}' missing from DECISION_REGISTER"
            )

        rated_by = raw.get("rated_by", "")
        if rated_by and baseline_roles and rated_by not in baseline_roles:
            errors.append(
                f"row {idx} ({cid}): rated_by '{rated_by}' not in baseline_organisation roles"
            )

    return not errors, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        default=str(_repo_root() / CSV_PATH_RELATIVE),
        help="Path to CAPABILITY_CONFIDENCE_REGISTRY.csv",
    )
    args = parser.parse_args(argv)

    ok, errors = validate(Path(args.csv))
    if ok:
        print(f"validate_capability_confidence_registry: PASS ({args.csv})")
        return 0
    print(f"validate_capability_confidence_registry: FAIL ({len(errors)} errors)")
    for err in errors[:50]:
        print(f"  - {err}")
    if len(errors) > 50:
        print(f"  ... and {len(errors) - 50} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
