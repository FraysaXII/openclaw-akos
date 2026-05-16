#!/usr/bin/env python3
"""Validator for SUBSTRATE_REGISTRY.csv (Initiative 84 P3).

Per `D-IH-84-F` (18-column schema + 8 enum frozensets) +
`akos-holistika-operations.mdc` §"New git-canonical compliance registers" pattern.

Validates:
- CSV header matches SUBSTRATE_REGISTRY_FIELDNAMES tuple exactly (drift gate).
- Each row Pydantic-validates against SubstrateRegistryRow (Literal enums + slug
  regex on substrate_id + ISO date on last_audit_date + length bounds).
- substrate_id is unique across rows.
- Each enum column value is in its corresponding VALID_* frozenset (defensive
  even though Pydantic Literal already enforces).

Exit codes:
    0 — PASS (header + all rows valid)
    1 — FAIL (header drift or row validation errors)
    2 — internal error (CSV missing, import failure)

Usage (repo root):

    py scripts/validate_substrate_registry.py
    py scripts/validate_substrate_registry.py --json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_substrate_registry_csv import (  # noqa: E402
    CSV_PATH_RELATIVE,
    SUBSTRATE_REGISTRY_FIELDNAMES,
    VALID_AIC_PATTERN_ROLES,
    VALID_AKOS_INTEGRATION_STATES,
    VALID_COST_CLASSES,
    VALID_LICENSE_CLASSES,
    VALID_MADEIRA_PRODUCTIZATION_ROLES,
    VALID_PERSISTENCE_MODELS,
    VALID_RUNTIME_SHAPES,
    VALID_STATUSES,
    VALID_TOOL_PROTOCOLS,
    SubstrateRegistryRow,
)
from pydantic import ValidationError  # noqa: E402


def _validate_csv(csv_path: Path) -> tuple[list[str], list[str], dict[str, int]]:
    """Returns (errors, warnings, status_counts)."""
    errors: list[str] = []
    warnings: list[str] = []
    status_counts: dict[str, int] = {s: 0 for s in sorted(VALID_STATUSES)}

    if not csv_path.is_file():
        errors.append(f"SUBSTRATE_REGISTRY.csv missing at {csv_path.relative_to(REPO_ROOT)}")
        return errors, warnings, status_counts

    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        header = tuple(reader.fieldnames or ())
        if header != SUBSTRATE_REGISTRY_FIELDNAMES:
            errors.append(
                f"Header mismatch: got {header!r}; expected {list(SUBSTRATE_REGISTRY_FIELDNAMES)!r}"
            )
            return errors, warnings, status_counts

        seen_ids: set[str] = set()
        for line_no, row in enumerate(reader, start=2):
            sid = row.get("substrate_id", "")
            if sid in seen_ids:
                errors.append(f"L{line_no}: duplicate substrate_id {sid!r}")
            else:
                seen_ids.add(sid)

            try:
                SubstrateRegistryRow(**row)  # type: ignore[arg-type]
            except ValidationError as exc:
                for err in exc.errors():
                    loc = ".".join(str(p) for p in err.get("loc", ()))
                    msg = err.get("msg", "")
                    errors.append(f"L{line_no} {sid}: {loc}: {msg}")
                continue

            # Defensive frozenset re-check (Pydantic Literal already enforces).
            for col, valid_set in (
                ("runtime_shape", VALID_RUNTIME_SHAPES),
                ("persistence_model", VALID_PERSISTENCE_MODELS),
                ("tool_protocol", VALID_TOOL_PROTOCOLS),
                ("license_class", VALID_LICENSE_CLASSES),
                ("status", VALID_STATUSES),
                ("cost_class", VALID_COST_CLASSES),
                ("akos_integration_state", VALID_AKOS_INTEGRATION_STATES),
                ("madeira_productization_role", VALID_MADEIRA_PRODUCTIZATION_ROLES),
                ("aic_pattern_role", VALID_AIC_PATTERN_ROLES),
            ):
                val = row.get(col, "")
                if val not in valid_set:
                    errors.append(
                        f"L{line_no} {sid}: {col}={val!r} not in {sorted(valid_set)}"
                    )

            st = row.get("status", "")
            if st in status_counts:
                status_counts[st] += 1

    return errors, warnings, status_counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate SUBSTRATE_REGISTRY.csv (Initiative 84 P3)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON summary alongside human-readable output",
    )
    args = parser.parse_args(argv)

    csv_path = REPO_ROOT / CSV_PATH_RELATIVE
    errors, warnings, status_counts = _validate_csv(csv_path)

    print()
    print("  SUBSTRATE_REGISTRY Validator")
    print("  " + "=" * 32)
    print(f"  Path: {CSV_PATH_RELATIVE}")
    print(f"  Status counts: {status_counts}")
    print(f"  Total rows scanned: {sum(status_counts.values())}")
    if warnings:
        print()
        print(f"  Warnings: {len(warnings)} (informational)")
        for w in warnings:
            print(f"    - {w}")
    if errors:
        print()
        print(f"  ERRORS ({len(errors)}):")
        for e in errors:
            print(f"    - {e}")
        print("  FAIL")
        verdict = "FAIL"
        exit_code = 1
    else:
        print("  PASS")
        verdict = "PASS"
        exit_code = 0

    if args.json:
        summary: dict[str, Any] = {
            "validator": "validate_substrate_registry",
            "path": CSV_PATH_RELATIVE,
            "status_counts": status_counts,
            "total_rows": sum(status_counts.values()),
            "warnings_count": len(warnings),
            "errors_count": len(errors),
            "verdict": verdict,
        }
        print()
        print(json.dumps(summary, indent=2, sort_keys=True))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
