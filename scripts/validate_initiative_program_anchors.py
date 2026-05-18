#!/usr/bin/env python3
"""Validate program-anchors FK across INITIATIVE_REGISTRY (I86 P1 Stage A + I86 P2 Stage B).

Per **D-IH-86-H** (Stage A, 2026-05-17) initiatives with status in
{``active``, ``continuous``, ``program_line``} carried a free-text
``Program anchors: PRJ-HOL-<CODE>-<YEAR>; ...`` prefix in ``notes`` that
acted as a foreign-key carrier into
[`PROGRAM_REGISTRY.csv`](../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PROGRAM_REGISTRY.csv).

Per **D-IH-86-J** (Stage B, 2026-05-17 at I86 P2) the anchor surface moved to a first-class
``program_anchors`` semicolon-list column on
[`INITIATIVE_REGISTRY.csv`](../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv).
The notes-prefix surface is deprecated; this validator now defaults to **column-read mode** and
WARNs (informational) on any residual ``Program anchors:`` prefix in notes for one deprecation cycle.

Operator can opt back into Stage A behaviour with ``--legacy-notes-parser`` while the one-shot
conversion ([`_oneshot_anchors_notes_to_column.py`](_oneshot_anchors_notes_to_column.py)) is
pending operator ratification.

Modes:

- **column-read (default; Stage B)**: read ``program_anchors`` column directly; FK-resolve
  against PROGRAM_REGISTRY; surface a WARN line per row still carrying the notes prefix.
- **legacy-notes-parser (Stage A)**: read the notes prefix and FK-resolve; no warn on
  column-vs-notes drift.

Per [`CONTRIBUTING.md`](../CONTRIBUTING.md) "Python Code Standards":
Pydantic chassis in ``akos/hlk_initiative_program_anchors.py``; type hints
on every signature; structured logging via ``akos.log.setup_logging``;
``pathlib.Path``; no ``print()`` outside the main human summary block.

Usage::

    py scripts/validate_initiative_program_anchors.py                    # Stage B column-read (default)
    py scripts/validate_initiative_program_anchors.py --legacy-notes-parser  # Stage A behaviour
    py scripts/validate_initiative_program_anchors.py --strict           # fail-loud on cutover-hygiene WARNs
    py scripts/validate_initiative_program_anchors.py --json-log         # structured logs
    py scripts/validate_initiative_program_anchors.py --quiet            # no human summary

Exit codes:

    0 - no malformed or unknown anchors detected (WARNs do not fail unless --strict).
    1 - at least one INITIATIVE_REGISTRY row has malformed or unknown anchors (or hygiene WARN under --strict).

Cross-references:
- [`akos/hlk_initiative_program_anchors.py`](../akos/hlk_initiative_program_anchors.py) Pydantic chassis.
- [`scripts/validate_initiative_registry.py`](validate_initiative_registry.py) sibling FK block (post-P2 in column-read mode).
- I86 master-roadmap §"P2 — Stage B column promotion".
"""

from __future__ import annotations

import argparse
import csv
import logging
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_initiative_program_anchors import (  # noqa: E402
    InitiativeProgramAnchorParse,
    parse_initiative_row,
    PROGRAM_ID_PATTERN,
)
from akos.io import REPO_ROOT  # noqa: E402
from akos.log import setup_logging  # noqa: E402

logger = logging.getLogger("akos.initiative_program_anchors")

INITIATIVE_CSV: Path = (
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
    / "INITIATIVE_REGISTRY.csv"
)
PROGRAM_CSV: Path = (
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
    / "PROGRAM_REGISTRY.csv"
)

NOTES_PREFIX_RE: re.Pattern[str] = re.compile(r"Program anchors:", re.IGNORECASE)


@dataclass
class ValidationOutcome:
    mode: str  # "column-read" or "legacy-notes-parser"
    rows_scanned: int
    rows_with_column: int
    rows_with_notes_prefix: int
    malformed_count: int
    unknown_count: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _load_program_ids(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {
            (row.get("program_id") or "").strip()
            for row in csv.DictReader(fh)
            if (row.get("program_id") or "").strip()
        }


def _load_initiative_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def _evaluate_column_read(
    rows: list[dict[str, str]],
    program_ids: set[str],
) -> ValidationOutcome:
    rows_with_column = 0
    rows_with_notes_prefix = 0
    errors: list[str] = []
    warnings: list[str] = []
    malformed_total = 0
    unknown_total = 0
    for row in rows:
        iid = (row.get("initiative_id") or "").strip()
        if not iid:
            continue
        col = (row.get("program_anchors") or "").strip()
        if col:
            rows_with_column += 1
            anchors = _split_semi(col)
            malformed = [a for a in anchors if not PROGRAM_ID_PATTERN.match(a)]
            well_formed = [a for a in anchors if PROGRAM_ID_PATTERN.match(a)]
            unknown = [a for a in well_formed if program_ids and a not in program_ids]
            if malformed:
                malformed_total += len(malformed)
                errors.append(
                    f"{iid}: malformed anchor(s) in program_anchors column: {malformed!r} "
                    f"(expect PRJ-HOL-<CODE>-<YEAR>)"
                )
            if unknown:
                unknown_total += len(unknown)
                errors.append(
                    f"{iid}: unknown anchor(s) in program_anchors column: {unknown!r} "
                    f"not found in PROGRAM_REGISTRY.csv"
                )
        notes = row.get("notes") or ""
        if NOTES_PREFIX_RE.search(notes):
            rows_with_notes_prefix += 1
            warnings.append(
                f"{iid}: residual 'Program anchors:' prefix in notes column "
                f"(Stage B cutover hygiene; run scripts/_oneshot_anchors_notes_to_column.py --apply to clean)"
            )
    return ValidationOutcome(
        mode="column-read",
        rows_scanned=len(rows),
        rows_with_column=rows_with_column,
        rows_with_notes_prefix=rows_with_notes_prefix,
        malformed_count=malformed_total,
        unknown_count=unknown_total,
        errors=errors,
        warnings=warnings,
    )


def _evaluate_legacy_notes(
    rows: list[dict[str, str]],
    program_ids: set[str],
) -> ValidationOutcome:
    rows_with_prefix = 0
    errors: list[str] = []
    malformed_total = 0
    unknown_total = 0
    for row in rows:
        iid = (row.get("initiative_id") or "").strip()
        if not iid:
            continue
        notes = row.get("notes") or ""
        parse: InitiativeProgramAnchorParse = parse_initiative_row(iid, notes, program_ids)
        if parse.has_prefix:
            rows_with_prefix += 1
        if parse.malformed_tokens:
            malformed_total += len(parse.malformed_tokens)
            errors.append(
                f"{iid}: malformed anchor token(s) {parse.malformed_tokens!r}"
                f" (expect PRJ-HOL-<CODE>-<YEAR>)"
            )
        if parse.unknown_anchors:
            unknown_total += len(parse.unknown_anchors)
            errors.append(
                f"{iid}: unknown anchor(s) {parse.unknown_anchors!r}"
                f" not found in PROGRAM_REGISTRY.csv"
            )
    return ValidationOutcome(
        mode="legacy-notes-parser",
        rows_scanned=len(rows),
        rows_with_column=0,
        rows_with_notes_prefix=rows_with_prefix,
        malformed_count=malformed_total,
        unknown_count=unknown_total,
        errors=errors,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--legacy-notes-parser", action="store_true",
                        help="Stage A behaviour: read 'Program anchors:' prefix in notes (deprecated).")
    parser.add_argument("--strict", action="store_true",
                        help="Fail-loud (exit 1) on cutover-hygiene WARNs (notes-prefix residuals).")
    parser.add_argument("--json-log", action="store_true",
                        help="Emit structured JSON log lines.")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress human summary output.")
    args = parser.parse_args(argv)

    setup_logging(json_output=args.json_log)

    if not args.quiet:
        print("\n  INITIATIVE_REGISTRY program-anchors validator")
        print("  " + "=" * 50)

    if not INITIATIVE_CSV.is_file():
        if not args.quiet:
            print("  SKIP: INITIATIVE_REGISTRY.csv not present")
        logger.info(
            "skip",
            extra={"agent_role": "validator", "tool_name": "initiative_program_anchors"},
        )
        return 0

    program_ids = _load_program_ids(PROGRAM_CSV)
    rows = _load_initiative_rows(INITIATIVE_CSV)

    if args.legacy_notes_parser:
        outcome = _evaluate_legacy_notes(rows, program_ids)
    else:
        outcome = _evaluate_column_read(rows, program_ids)

    if not args.quiet:
        print(f"  Mode:                      {outcome.mode}")
        print(f"  INITIATIVE rows scanned:   {outcome.rows_scanned}")
        if outcome.mode == "column-read":
            print(f"  rows with column value:    {outcome.rows_with_column}")
            print(f"  rows with notes prefix:    {outcome.rows_with_notes_prefix}  (Stage B hygiene)")
        else:
            print(f"  rows with notes prefix:    {outcome.rows_with_notes_prefix}")
        print(f"  PROGRAM_REGISTRY ids:      {len(program_ids)}")
        print(f"  malformed tokens:          {outcome.malformed_count}")
        print(f"  unknown anchor(s):         {outcome.unknown_count}")

    if outcome.warnings and not args.quiet:
        print(f"  WARN: {len(outcome.warnings)} cutover-hygiene warning(s) (run --strict to fail-loud)")
        for w in outcome.warnings[:5]:
            print(f"    ~ {w}")
        if len(outcome.warnings) > 5:
            print(f"    ... and {len(outcome.warnings) - 5} more")

    fail = bool(outcome.errors) or (args.strict and bool(outcome.warnings))

    if fail:
        if not args.quiet:
            if outcome.errors:
                print(f"  FAIL: {len(outcome.errors)} error(s)")
                for err in outcome.errors[:10]:
                    print(f"    - {err}")
                if len(outcome.errors) > 10:
                    print(f"    ... and {len(outcome.errors) - 10} more")
            elif args.strict and outcome.warnings:
                print(f"  FAIL (--strict): {len(outcome.warnings)} hygiene warning(s)")
        logger.error(
            f"fail mode={outcome.mode} errors={len(outcome.errors)} warnings={len(outcome.warnings)}",
            extra={"agent_role": "validator", "tool_name": "initiative_program_anchors"},
        )
        return 1

    if not args.quiet:
        print("  PASS")
    logger.info(
        f"pass mode={outcome.mode} rows_scanned={outcome.rows_scanned}",
        extra={"agent_role": "validator", "tool_name": "initiative_program_anchors"},
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
