"""Validate USE_CASE_ARCHIVE.csv per I82 P4 + D-IH-82-R.

Checks:

1. Header matches ``USE_CASE_ARCHIVE_FIELDNAMES`` SSOT.
2. Every row passes the Pydantic contract (UseCaseArchiveRow).
3. ``use_case_id`` uniqueness.
4. ``capability_id`` FK-resolves into CAPABILITY_REGISTRY.csv.
5. ``engagement_id`` FK-resolves into ENGAGEMENT_REGISTRY.csv when non-empty.
6. ``last_review_decision_id`` references a row in DECISION_REGISTER.csv.
7. ``realised_by`` references a role_name in baseline_organisation.csv.

Exit 0 on PASS; 1 on FAIL. Empty CSV (header-only) is a valid PASS state
(Wave Q infrastructure mint may ship with 0 or 1 demonstrator rows).
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from pydantic import ValidationError

from akos.hlk_use_case_archive_csv import (
    CSV_PATH_RELATIVE,
    USE_CASE_ARCHIVE_FIELDNAMES,
    UseCaseArchiveRow,
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

    expected = list(USE_CASE_ARCHIVE_FIELDNAMES)
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
    engagement_ids = _load_lookup(
        root
        / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
        / "dimensions/ENGAGEMENT_REGISTRY.csv",
        "engagement_id",
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
            normalised = dict(raw)
            if normalised.get("quality_self_rating", "") != "":
                normalised["quality_self_rating"] = int(normalised["quality_self_rating"])
            UseCaseArchiveRow(**normalised)
        except (ValidationError, ValueError) as exc:
            errors.append(f"row {idx} ({raw.get('use_case_id', '?')}): {exc}")
            continue

        uid = raw["use_case_id"]
        if uid in seen_ids:
            errors.append(f"row {idx}: duplicate use_case_id '{uid}'")
        seen_ids.add(uid)

        cap_id = raw["capability_id"]
        if capability_ids and cap_id not in capability_ids:
            errors.append(
                f"row {idx} ({uid}): capability_id '{cap_id}' does not resolve to CAPABILITY_REGISTRY"
            )

        eng_id = raw.get("engagement_id", "")
        if eng_id and engagement_ids and eng_id not in engagement_ids:
            errors.append(
                f"row {idx} ({uid}): engagement_id '{eng_id}' does not resolve to ENGAGEMENT_REGISTRY"
            )

        dec_id = raw.get("last_review_decision_id", "")
        if dec_id and decision_ids and dec_id not in decision_ids:
            errors.append(
                f"row {idx} ({uid}): last_review_decision_id '{dec_id}' missing from DECISION_REGISTER"
            )

        realised_by = raw.get("realised_by", "")
        if realised_by and baseline_roles and realised_by not in baseline_roles:
            errors.append(
                f"row {idx} ({uid}): realised_by '{realised_by}' not in baseline_organisation roles"
            )

    return not errors, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        default=str(_repo_root() / CSV_PATH_RELATIVE),
        help="Path to USE_CASE_ARCHIVE.csv",
    )
    args = parser.parse_args(argv)

    ok, errors = validate(Path(args.csv))
    if ok:
        print(f"validate_use_case_archive: PASS ({args.csv})")
        return 0
    print(f"validate_use_case_archive: FAIL ({len(errors)} errors)")
    for err in errors[:50]:
        print(f"  - {err}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
