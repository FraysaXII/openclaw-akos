#!/usr/bin/env python3
"""Plane-1↔Plane-2 emit contract: CSV row counts must match emitted INSERT counts (DATA-02).

Holistic offline guard for the mirror-sync pipeline. Emits the full mirror SQL (main + OPS-86-15
gap mirrors spliced, same as the GitHub workflow), counts INSERT statements per
``compliance.<table>``, and compares to canonical CSV row counts.

Also verifies workflow wiring (gap splice, enum parity preflight, single-transaction apply,
delete-reconcile).

Usage::

    py scripts/validate_mirror_emit_contract.py
    py scripts/validate_mirror_emit_contract.py --self-test
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICALS = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals"
SYNC = REPO_ROOT / "scripts/sync_compliance_mirrors_from_csv.py"
WORKFLOW = REPO_ROOT / ".github/workflows/supabase-mirror-sync.yml"
RECONCILE = REPO_ROOT / "scripts/emit_mirror_delete_reconcile.py"
ENUM_PARITY = REPO_ROOT / "scripts/validate_mirror_enum_parity.py"

_INSERT_COUNT_RE = re.compile(
    r"^INSERT INTO compliance\.(?P<tbl>[a-z0-9_]+) ",
    re.IGNORECASE,
)

# Milestone BT-09 counts + other high-signal mirrors (csv_rel_under_canonicals, mirror_table)
_EMIT_CONTRACTS: tuple[tuple[str, str], ...] = (
    ("process_list.csv", "process_list_mirror"),
    ("dimensions/CAPABILITY_REGISTRY.csv", "capability_registry_mirror"),
    ("dimensions/CAPABILITY_CONFIDENCE_REGISTRY.csv", "capability_confidence_registry_mirror"),
    ("dimensions/TOPIC_REGISTRY.csv", "topic_registry_mirror"),
    ("DECISION_REGISTER.csv", "decision_register_mirror"),
    ("dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv", "people_design_pattern_registry_mirror"),
    ("dimensions/AIC_REGISTRY.csv", "aic_registry_mirror"),
    ("dimensions/AUDIENCE_REGISTRY.csv", "audience_registry_mirror"),
    ("baseline_organisation.csv", "baseline_organisation_mirror"),
    ("OPS_REGISTER.csv", "ops_register_mirror"),
    ("INITIATIVE_REGISTRY.csv", "initiative_registry_mirror"),
)


def _csv_row_count(rel: str) -> int:
    """Rows eligible for mirror emit (matches sync_compliance_mirrors_from_csv.py filters)."""
    path = CANONICALS / rel
    if not path.is_file():
        return -1
    if rel == "baseline_organisation.csv":
        with path.open(encoding="utf-8", newline="") as fh:
            return sum(
                1 for r in csv.DictReader(fh) if (r.get("org_uuid") or "").strip()
            )
    with path.open(encoding="utf-8", newline="") as fh:
        return sum(1 for _ in csv.reader(fh)) - 1  # minus header


def _emit_full_sql(out_path: Path) -> None:
    subprocess.run(
        [sys.executable, str(SYNC), "--output", str(out_path), "--git-sha", "emit-contract"],
        check=True,
        cwd=str(REPO_ROOT),
    )
    gap = out_path.with_suffix(".gap.sql")
    subprocess.run(
        [sys.executable, str(SYNC), "--ops8615-gap-mirrors-only", "--no-begin-commit", "--output", str(gap), "--git-sha", "emit-contract"],
        check=True,
        cwd=str(REPO_ROOT),
    )
    main = out_path.read_text(encoding="utf-8")
    gap_text = gap.read_text(encoding="utf-8")
    idx = main.rfind("COMMIT;")
    if idx == -1:
        out_path.write_text(main + "\n" + gap_text, encoding="utf-8")
    else:
        out_path.write_text(
            main[:idx] + "\n-- gap mirrors\n" + gap_text + "\n" + main[idx:],
            encoding="utf-8",
        )
    gap.unlink(missing_ok=True)


def _count_inserts(sql_path: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for line in sql_path.read_text(encoding="utf-8").splitlines():
        m = _INSERT_COUNT_RE.match(line.strip())
        if m:
            counts[m.group("tbl")] = counts.get(m.group("tbl"), 0) + 1
    return counts


def _check_workflow_wiring() -> list[str]:
    errors: list[str] = []
    if not WORKFLOW.is_file():
        return ["missing supabase-mirror-sync.yml"]
    text = WORKFLOW.read_text(encoding="utf-8")
    required = (
        ("ops8615-gap-mirrors-only", "gap mirror splice"),
        ("validate_mirror_enum_parity.py", "enum parity preflight"),
        ("--single-transaction", "atomic apply"),
        ("emit_mirror_delete_reconcile.py", "delete-reconcile step"),
    )
    for needle, label in required:
        if needle not in text:
            errors.append(f"workflow missing {label} ({needle})")
    return errors


def run_checks() -> list[str]:
    errors: list[str] = []
    errors.extend(_check_workflow_wiring())

    for script in (SYNC, RECONCILE, ENUM_PARITY):
        if not script.is_file():
            errors.append(f"missing script {script.name}")

    with tempfile.TemporaryDirectory() as tmp:
        sql_path = Path(tmp) / "mirror-upsert.sql"
        _emit_full_sql(sql_path)
        insert_counts = _count_inserts(sql_path)

        for csv_rel, mirror_tbl in _EMIT_CONTRACTS:
            csv_n = _csv_row_count(csv_rel)
            emit_n = insert_counts.get(mirror_tbl, 0)
            if csv_n < 0:
                errors.append(f"{mirror_tbl}: CSV missing {csv_rel}")
                continue
            if emit_n != csv_n:
                errors.append(
                    f"{mirror_tbl}: emit INSERT count {emit_n} != CSV rows {csv_n} "
                    f"({csv_rel})"
                )

    return errors


def self_test() -> int:
    assert _INSERT_COUNT_RE.match("INSERT INTO compliance.process_list_mirror (")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    errors = run_checks()
    if errors:
        print(f"FAIL: {len(errors)} mirror-emit-contract finding(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(
        f"PASS: mirror emit contract — {len(_EMIT_CONTRACTS)} tables, "
        "CSV row counts match emitted INSERTs; workflow wiring OK"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
