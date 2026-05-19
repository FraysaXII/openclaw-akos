"""Validate MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv per I76 P3.

Paired runbook for `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv`
per `akos-executable-process-catalog.mdc` RULE 1. Sister validator pattern:
scripts/validate_madeira_tool_rbac.py (I76 P2 precedent) + scripts/validate_madeira_mode_parity.py (I76 P1).

Usage::

    py scripts/validate_madeira_persistence_vehicle.py [--strict]

Exit codes:
    0 - all rows parse, header matches, conditional staleness semantics PASS,
        registry-level uniqueness + depends_on closure resolve, FK-resolution
        green (advisory by default; strict promotes to FAIL).
    1 - row(s) failed Pydantic validation OR header mismatch OR registry-level
        validation failed OR (strict only) FK resolution miss against
        DECISION_REGISTER.csv / TOPIC_REGISTRY.csv.
    2 - file structure unparseable (CSV missing or unreadable header).
"""
from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_madeira_persistence_vehicle import (
    MADEIRA_PERSISTENCE_VEHICLE_FIELDNAMES,
    MadeiraPersistenceVehicleRegistry,
    MadeiraPersistenceVehicleRow,
)
from akos.io import REPO_ROOT
from akos.log import setup_logging
from pydantic import ValidationError

LOG = logging.getLogger("validate_madeira_persistence_vehicle")

CSV_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Envoy Tech Lab"
    / "canonicals"
    / "dimensions"
    / "MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv"
)

DECISION_CSV = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Compliance"
    / "canonicals"
    / "DECISION_REGISTER.csv"
)

TOPIC_CSV = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Compliance"
    / "canonicals"
    / "dimensions"
    / "TOPIC_REGISTRY.csv"
)


def _load_decision_ids() -> set[str]:
    """Read DECISION_REGISTER.csv decision_id column into a set for FK resolution."""
    if not DECISION_CSV.is_file():
        return set()
    with DECISION_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return {
            (row.get("decision_id") or "").strip()
            for row in reader
            if row.get("decision_id")
        }


def _load_topic_ids() -> set[str]:
    """Read TOPIC_REGISTRY.csv topic_id column into a set for FK resolution."""
    if not TOPIC_CSV.is_file():
        return set()
    with TOPIC_CSV.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return {
            (row.get("topic_id") or "").strip()
            for row in reader
            if row.get("topic_id")
        }


def _coerce_row(raw: dict[str, str]) -> dict[str, object]:
    """Turn raw CSV strings into Pydantic-friendly types.

    Pydantic does not auto-coerce empty CSV cells to ``None`` for ``Optional[int]``
    fields; an empty ``staleness_days`` cell would otherwise fail validation. This
    helper passes ``None`` for empty optional-int cells and leaves all other cells
    as strings.
    """
    out: dict[str, object] = {k: v for k, v in raw.items() if isinstance(k, str)}
    staleness = (raw.get("staleness_days") or "").strip()
    out["staleness_days"] = int(staleness) if staleness else None
    return out


def _load_rows() -> tuple[list[dict[str, str]], list[str]]:
    if not CSV_PATH.is_file():
        return [], [f"CSV not found at {CSV_PATH}"]
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(MADEIRA_PERSISTENCE_VEHICLE_FIELDNAMES):
            return [], [
                "header mismatch",
                f"  expected: {list(MADEIRA_PERSISTENCE_VEHICLE_FIELDNAMES)}",
                f"  got:      {reader.fieldnames}",
            ]
        return list(reader), []


def _validate(strict: bool = False) -> int:
    rows, header_errors = _load_rows()
    if header_errors:
        for line in header_errors:
            LOG.error(line)
        return 2

    if not rows:
        LOG.error("CSV has no data rows")
        return 1

    decision_ids = _load_decision_ids()
    topic_ids = _load_topic_ids()
    parsed: list[MadeiraPersistenceVehicleRow] = []
    errors: list[str] = []

    for i, raw in enumerate(rows, start=1):
        try:
            parsed.append(MadeiraPersistenceVehicleRow(**_coerce_row(raw)))
        except ValidationError as exc:
            errors.append(
                f"row {i} (vehicle_id={raw.get('vehicle_id', '<empty>')}): {exc.errors()}"
            )
            continue

        # FK resolution: last_review_decision_id -> DECISION_REGISTER.csv.
        last_review_decision_id = raw.get("last_review_decision_id", "").strip()
        if (
            decision_ids
            and last_review_decision_id
            and last_review_decision_id not in decision_ids
        ):
            msg = (
                f"row {i} (vehicle_id={raw.get('vehicle_id')}): "
                f"last_review_decision_id={last_review_decision_id!r} not found in "
                "DECISION_REGISTER.csv"
            )
            if strict:
                errors.append(msg)
            else:
                LOG.warning(msg)

        # FK resolution: topic_ids semicolon-list -> TOPIC_REGISTRY.csv.
        raw_topic_ids = (raw.get("topic_ids") or "").strip()
        if topic_ids and raw_topic_ids:
            for topic in [t.strip() for t in raw_topic_ids.split(";") if t.strip()]:
                if topic not in topic_ids:
                    msg = (
                        f"row {i} (vehicle_id={raw.get('vehicle_id')}): "
                        f"topic_id={topic!r} not found in TOPIC_REGISTRY.csv"
                    )
                    if strict:
                        errors.append(msg)
                    else:
                        LOG.warning(msg)

    if errors:
        for e in errors:
            LOG.error(e)
        return 1

    try:
        MadeiraPersistenceVehicleRegistry(rows=tuple(parsed))
    except ValidationError as exc:
        LOG.error(f"registry-level validation failed: {exc.errors()}")
        return 1

    LOG.info(
        "PASS: %d MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv rows parsed; "
        "DECISION_REGISTER + TOPIC_REGISTRY FK resolution %s.",
        len(parsed),
        "STRICT (FK miss = FAIL)" if strict else "advisory (FK miss = WARN)",
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv per I76 P3."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "FAIL on unresolved last_review_decision_id FK against DECISION_REGISTER.csv "
            "or unresolved topic_id FK against TOPIC_REGISTRY.csv "
            "(default: WARN)."
        ),
    )
    args = parser.parse_args(argv)
    setup_logging(level=logging.INFO)
    return _validate(strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
