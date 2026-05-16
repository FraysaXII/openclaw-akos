"""Validator for AUDIENCE_REGISTRY.csv (Initiative 85 P1).

Per D-IH-85-A (narrow FK index pattern) + D-IH-85-B (YAML list multi-audience
encoding).

Enforces:
1. Schema (header column order + completeness) per
   ``akos.hlk_audience_csv.AUDIENCE_REGISTRY_FIELDNAMES``.
2. ``audience_code`` regex ``^J-[A-Z]{2,8}$`` (e.g. J-IN, J-ENISA).
3. ``audience_code`` uniqueness (no duplicates).
4. Enum constraints on ``register_side`` and ``status``.
5. ``last_review_by`` FK-by-convention to ``baseline_organisation.csv`` ``role_name``
   (warning only — initial mint may precede role-name canonicalization).
6. ``last_review_decision_id`` and ``linked_decision_id`` FK-by-convention to
   ``DECISION_REGISTER.csv`` ``decision_id``.
7. ``name``, ``intent_summary``, ``typical_surfaces``, ``bridge_anchor``,
   ``added_at``, ``last_review_at``, ``methodology_version_at_review``
   non-empty.
8. ``added_at`` and ``last_review_at`` parseable as ``YYYY-MM-DD``.
9. ``methodology_version_at_review`` matches ``^v\\d+\\.\\d+$`` per D-IH-71-D.

Rows in ``status=deprecated`` are exempt from typical_surfaces non-empty check
(deprecated rows are historical record only).

Exit code: 0 PASS, 1 FAIL.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_audience_csv import (  # noqa: E402
    AUDIENCE_REGISTRY_FIELDNAMES,
    CANONICAL_PATH,
    VALID_REGISTER_SIDES,
    VALID_STATUSES,
)

REGISTRY_PATH = REPO_ROOT / CANONICAL_PATH
DECISION_REGISTER_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "Compliance" / "canonicals" / "DECISION_REGISTER.csv"
)
BASELINE_ORG_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "Compliance" / "canonicals" / "baseline_organisation.csv"
)

AUDIENCE_CODE_RE = re.compile(r"^J-[A-Z]{2,8}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
METHODOLOGY_VERSION_RE = re.compile(r"^v\d+\.\d+$")


def _load_csv_column(path: Path, column: str) -> set[str]:
    if not path.exists():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return {row[column] for row in reader if row.get(column)}


def main() -> int:
    if not REGISTRY_PATH.exists():
        print(f"FAIL: AUDIENCE_REGISTRY.csv not found at {REGISTRY_PATH}")
        return 1

    decision_ids = _load_csv_column(DECISION_REGISTER_PATH, "decision_id")
    role_names = _load_csv_column(BASELINE_ORG_PATH, "role_name")

    errors: list[str] = []
    warnings: list[str] = []
    rows_seen = 0
    by_status: dict[str, int] = {}
    by_register_side: dict[str, int] = {}
    audience_codes: set[str] = set()

    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != AUDIENCE_REGISTRY_FIELDNAMES:
            errors.append(
                f"Schema mismatch: header={reader.fieldnames!r} "
                f"expected={list(AUDIENCE_REGISTRY_FIELDNAMES)!r}"
            )
        for line_no, row in enumerate(reader, start=2):
            rows_seen += 1
            code = row.get("audience_code", "")

            if not AUDIENCE_CODE_RE.match(code):
                errors.append(
                    f"L{line_no}: audience_code {code!r} fails regex {AUDIENCE_CODE_RE.pattern}"
                )
            if code in audience_codes:
                errors.append(f"L{line_no}: duplicate audience_code {code!r}")
            audience_codes.add(code)

            rs = row.get("register_side", "")
            if rs not in VALID_REGISTER_SIDES:
                errors.append(
                    f"L{line_no} {code}: register_side {rs!r} not in {sorted(VALID_REGISTER_SIDES)}"
                )
            else:
                by_register_side[rs] = by_register_side.get(rs, 0) + 1

            status = row.get("status", "")
            if status not in VALID_STATUSES:
                errors.append(
                    f"L{line_no} {code}: status {status!r} not in {sorted(VALID_STATUSES)}"
                )
            else:
                by_status[status] = by_status.get(status, 0) + 1

            for required in ("name", "intent_summary", "bridge_anchor", "added_at",
                             "last_review_at", "methodology_version_at_review"):
                if not row.get(required, "").strip():
                    errors.append(f"L{line_no} {code}: {required} must be non-empty")

            # typical_surfaces required except for deprecated
            if status != "deprecated" and not row.get("typical_surfaces", "").strip():
                errors.append(
                    f"L{line_no} {code}: typical_surfaces must be non-empty for non-deprecated rows"
                )

            for date_col in ("added_at", "last_review_at"):
                val = row.get(date_col, "")
                if val and not DATE_RE.match(val):
                    errors.append(
                        f"L{line_no} {code}: {date_col} {val!r} not in YYYY-MM-DD format"
                    )

            mvar = row.get("methodology_version_at_review", "")
            if mvar and not METHODOLOGY_VERSION_RE.match(mvar):
                errors.append(
                    f"L{line_no} {code}: methodology_version_at_review {mvar!r} "
                    f"not in vMAJOR.MINOR format"
                )

            review_by = row.get("last_review_by", "")
            if role_names and review_by and review_by not in role_names:
                warnings.append(
                    f"L{line_no} {code}: last_review_by {review_by!r} "
                    f"not in baseline_organisation role_name set"
                )

            for did_col in ("last_review_decision_id", "linked_decision_id"):
                did = row.get(did_col, "")
                if decision_ids and did and did not in decision_ids:
                    errors.append(
                        f"L{line_no} {code}: {did_col} {did!r} "
                        f"not in DECISION_REGISTER decision_id set"
                    )

    if errors:
        print("FAIL: AUDIENCE_REGISTRY validation errors:")
        for e in errors:
            print(f"  {e}")
        for w in warnings:
            print(f"  [WARN] {w}")
        return 1

    summary_by_status = ", ".join(f"{k}={v}" for k, v in sorted(by_status.items()))
    summary_by_register = ", ".join(f"{k}={v}" for k, v in sorted(by_register_side.items()))
    print(
        f"PASS: AUDIENCE_REGISTRY validated "
        f"({rows_seen} rows; by_status={{{summary_by_status}}}; "
        f"by_register_side={{{summary_by_register}}})"
    )
    for w in warnings:
        print(f"  [WARN] {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
