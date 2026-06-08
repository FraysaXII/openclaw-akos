#!/usr/bin/env python3
"""Plane-1 structural integrity: canonical CSV row-width + typed-column guard (DATA-05).

Catches the D-IH-95-A class of bug BEFORE mirror apply: a stray empty field (``summary.",,"notes"``)
shifts columns so free text lands in a DATE column. ``validate_decision_register.py`` checks the
header row; this script checks EVERY data row has exactly ``len(FIELDNAMES)`` fields and that
known DATE columns match ``YYYY-MM-DD`` (or are empty).

Wired into ``validate_hlk.py`` and ``dataops_quality_check.py`` (DATA-05-SCHEMA-DRIFT probe).

Usage::

    py scripts/validate_csv_column_alignment.py
    py scripts/validate_csv_column_alignment.py --self-test
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICALS = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_baseline_org_csv import BASELINE_ORGANISATION_FIELDNAMES  # noqa: E402
from akos.hlk_buildout_backlog_csv import BUILDOUT_BACKLOG_FIELDNAMES  # noqa: E402
from akos.hlk_capability_registry_csv import CAPABILITY_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_capability_confidence_csv import CAPABILITY_CONFIDENCE_FIELDNAMES  # noqa: E402
from akos.hlk_cycle_register_csv import CYCLE_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_decision_register_csv import DECISION_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_design_pattern_csv import DESIGN_PATTERN_FIELDNAMES  # noqa: E402
from akos.hlk_initiative_registry_csv import INITIATIVE_REGISTRY_FIELDNAMES  # noqa: E402
from akos.hlk_ops_register_csv import OPS_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_process_csv import PROCESS_LIST_FIELDNAMES  # noqa: E402
from akos.hlk_topic_registry_csv import TOPIC_REGISTRY_FIELDNAMES  # noqa: E402

_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Registry slug -> (relative path, fieldnames, date columns, required PK column or "")
_CANONICAL_ROW_CONTRACTS: tuple[tuple[str, Path, tuple[str, ...], frozenset[str], str], ...] = (
    (
        "DECISION_REGISTER",
        Path("DECISION_REGISTER.csv"),
        DECISION_REGISTER_FIELDNAMES,
        frozenset({"decided_at", "last_review_at"}),
        "",
    ),
    (
        "INITIATIVE_REGISTRY",
        Path("INITIATIVE_REGISTRY.csv"),
        INITIATIVE_REGISTRY_FIELDNAMES,
        frozenset({"inception_date", "last_review", "closed_at", "archived_at", "last_review_at"}),
        "",
    ),
    (
        "OPS_REGISTER",
        Path("OPS_REGISTER.csv"),
        OPS_REGISTER_FIELDNAMES,
        frozenset({"opened_at", "closed_at", "last_review_at"}),
        "",
    ),
    (
        "CYCLE_REGISTER",
        Path("CYCLE_REGISTER.csv"),
        CYCLE_REGISTER_FIELDNAMES,
        frozenset({"started_at", "closed_at"}),
        "",
    ),
    (
        "process_list",
        Path("process_list.csv"),
        PROCESS_LIST_FIELDNAMES,
        frozenset({"last_review_at"}),
        "",
    ),
    (
        "baseline_organisation",
        Path("baseline_organisation.csv"),
        BASELINE_ORGANISATION_FIELDNAMES,
        frozenset({"last_review_at"}),
        "org_uuid",
    ),
    (
        "CAPABILITY_REGISTRY",
        Path("dimensions/CAPABILITY_REGISTRY.csv"),
        CAPABILITY_REGISTRY_FIELDNAMES,
        frozenset({"last_review_at"}),
        "",
    ),
    (
        "CAPABILITY_CONFIDENCE_REGISTRY",
        Path("dimensions/CAPABILITY_CONFIDENCE_REGISTRY.csv"),
        CAPABILITY_CONFIDENCE_FIELDNAMES,
        frozenset({"last_review_at"}),
        "",
    ),
    (
        "TOPIC_REGISTRY",
        Path("dimensions/TOPIC_REGISTRY.csv"),
        TOPIC_REGISTRY_FIELDNAMES,
        frozenset({"last_review_at"}),
        "",
    ),
    (
        "PEOPLE_DESIGN_PATTERN_REGISTRY",
        Path("dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv"),
        DESIGN_PATTERN_FIELDNAMES,
        frozenset({"last_review"}),
        "",
    ),
    (
        "BUILDOUT_BACKLOG",
        Path("dimensions/BUILDOUT_BACKLOG.csv"),
        BUILDOUT_BACKLOG_FIELDNAMES,
        frozenset({"last_review_at"}),
        "",
    ),
)


def _check_csv(
    slug: str,
    path: Path,
    fieldnames: tuple[str, ...],
    date_cols: frozenset[str],
    required_pk_col: str = "",
) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"{slug}: missing file {path}"]
    expected = len(fieldnames)
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration:
            return [f"{slug}: empty file"]
        if list(header) != list(fieldnames):
            errors.append(f"{slug}: header drift (expected {expected} cols)")
            return errors
        for line_no, row in enumerate(reader, start=2):
            if not any(cell.strip() for cell in row):
                continue
            if len(row) != expected:
                pk = row[0][:48] if row else "?"
                errors.append(
                    f"{slug}: line {line_no} has {len(row)} fields, expected {expected} "
                    f"(column-shift risk; pk={pk!r})"
                )
                if len(errors) >= 25:
                    errors.append(f"{slug}: ...truncated after 25 row-width errors")
                    break
                continue
            for col in date_cols:
                if col not in fieldnames:
                    continue
                idx = fieldnames.index(col)
                val = (row[idx] or "").strip()
                if val and not _ISO_DATE.match(val):
                    pk = row[0][:48]
                    errors.append(
                        f"{slug}: line {line_no} col {col!r} value {val[:60]!r} is not YYYY-MM-DD "
                        f"(pk={pk!r}; likely column shift)"
                    )
                    if len(errors) >= 25:
                        errors.append(f"{slug}: ...truncated after 25 date-format errors")
                        break
            if required_pk_col and required_pk_col in fieldnames:
                pk_idx = fieldnames.index(required_pk_col)
                pk_val = (row[pk_idx] or "").strip()
                if not pk_val:
                    role = row[fieldnames.index("role_name")] if "role_name" in fieldnames else "?"
                    errors.append(
                        f"{slug}: line {line_no} missing {required_pk_col!r} "
                        f"(role_name={role!r}; row will not mirror-emit)"
                    )
    return errors


def run_checks() -> list[str]:
    all_errors: list[str] = []
    for slug, rel, fieldnames, date_cols, required_pk in _CANONICAL_ROW_CONTRACTS:
        all_errors.extend(
            _check_csv(slug, CANONICALS / rel, fieldnames, date_cols, required_pk)
        )
    return all_errors


def self_test() -> int:
    # Synthetic bad row detection logic
    assert _ISO_DATE.match("2026-06-08")
    assert not _ISO_DATE.match("Operator chose D")
    assert len(_CANONICAL_ROW_CONTRACTS) >= 10
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    errors = run_checks()
    if errors:
        print(f"FAIL: {len(errors)} column-alignment finding(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(
        f"PASS: column alignment - {len(_CANONICAL_ROW_CONTRACTS)} canonical CSVs, "
        "row-width + DATE columns OK"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
