"""Validate MADEIRA_TOOL_RBAC.csv per I76 P2.

Paired runbook for `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/MADEIRA_TOOL_RBAC.csv`
per `akos-executable-process-catalog.mdc` RULE 1. Sister validator pattern:
scripts/validate_madeira_mode_parity.py + scripts/validate_locale_orthography.py.

Usage::

    py scripts/validate_madeira_tool_rbac.py [--strict]

Exit codes:
    0 - all rows parse, header matches, conditional-constraint semantics PASS, FK to
        DECISION_REGISTER resolves.
    1 - row(s) failed Pydantic validation OR header mismatch OR FK resolution failed.
    2 - file structure unparseable.
"""
from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_madeira_tool_rbac import (
    MADEIRA_TOOL_RBAC_FIELDNAMES,
    MadeiraToolRbacRegistry,
    MadeiraToolRbacRow,
)
from akos.io import REPO_ROOT
from akos.log import setup_logging
from pydantic import ValidationError

LOG = logging.getLogger("validate_madeira_tool_rbac")

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
    / "MADEIRA_TOOL_RBAC.csv"
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


def _load_rows() -> tuple[list[dict[str, str]], list[str]]:
    if not CSV_PATH.is_file():
        return [], [f"CSV not found at {CSV_PATH}"]
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(MADEIRA_TOOL_RBAC_FIELDNAMES):
            return [], [
                "header mismatch",
                f"  expected: {list(MADEIRA_TOOL_RBAC_FIELDNAMES)}",
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
    parsed: list[MadeiraToolRbacRow] = []
    errors: list[str] = []

    for i, raw in enumerate(rows, start=1):
        try:
            parsed.append(MadeiraToolRbacRow(**raw))
        except ValidationError as exc:
            errors.append(f"row {i} (tool_id={raw.get('tool_id', '<empty>')}): {exc.errors()}")
            continue

        last_review_decision_id = raw.get("last_review_decision_id", "").strip()
        if decision_ids and last_review_decision_id and last_review_decision_id not in decision_ids:
            msg = (
                f"row {i} (tool_id={raw.get('tool_id')}): "
                f"last_review_decision_id={last_review_decision_id!r} not found in DECISION_REGISTER.csv"
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
        MadeiraToolRbacRegistry(rows=tuple(parsed))
    except ValidationError as exc:
        LOG.error(f"registry-level validation failed: {exc.errors()}")
        return 1

    LOG.info(
        "PASS: %d MADEIRA_TOOL_RBAC.csv rows parsed; DECISION_REGISTER FK resolution %s.",
        len(parsed),
        "STRICT (failed on miss)" if strict else "advisory (warn on miss)",
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate MADEIRA_TOOL_RBAC.csv per I76 P2.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="FAIL on unresolved last_review_decision_id FK (default: WARN).",
    )
    args = parser.parse_args(argv)
    setup_logging(level=logging.INFO)
    return _validate(strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
