#!/usr/bin/env python3
"""Plane-1↔Plane-2 emit contract: CSV row counts must match emitted INSERT counts (DATA-02).

Holistic offline guard for the mirror-sync pipeline. Emits the full mirror SQL (main + OPS-86-15
gap mirrors spliced, same as the GitHub workflow), counts INSERT statements per
``compliance.<table>``, and compares to canonical CSV row counts.

Registry-driven since P95-GOV-3: emit-contract rows and workflow path filters load from
``CANONICAL_GOVERNANCE_REGISTRY.csv`` (not a hardcoded Compliance folder list).

Also verifies workflow wiring (gap splice, enum parity preflight, single-transaction apply,
delete-reconcile, registry path-filter parity).

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
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_canonical_governance_registry_csv import (  # noqa: E402
    CSV_PATH_RELATIVE,
    iter_emit_contract_rows,
    load_registry_rows,
    mirror_table_short_name,
    plane2_workflow_path_union,
)

SYNC = REPO_ROOT / "scripts/sync_compliance_mirrors_from_csv.py"
WORKFLOW = REPO_ROOT / ".github/workflows/supabase-mirror-sync.yml"
REGISTRY = REPO_ROOT / CSV_PATH_RELATIVE
RECONCILE = REPO_ROOT / "scripts/emit_mirror_delete_reconcile.py"
ENUM_PARITY = REPO_ROOT / "scripts/validate_mirror_enum_parity.py"

_INSERT_COUNT_RE = re.compile(
    r"^INSERT INTO compliance\.(?P<tbl>[a-z0-9_]+) ",
    re.IGNORECASE,
)

_WORKFLOW_PATH_RE = re.compile(r'^\s+-\s+"([^"]+)"\s*$')


def _csv_row_count(csv_path: Path) -> int:
    """Rows eligible for mirror emit (matches sync_compliance_mirrors_from_csv.py filters)."""
    if not csv_path.is_file():
        return -1
    if csv_path.name == "baseline_organisation.csv":
        with csv_path.open(encoding="utf-8", newline="") as fh:
            return sum(
                1 for r in csv.DictReader(fh) if (r.get("org_uuid") or "").strip()
            )
    with csv_path.open(encoding="utf-8", newline="") as fh:
        return sum(1 for _ in csv.reader(fh)) - 1  # minus header


def _emit_full_sql(out_path: Path) -> None:
    subprocess.run(
        [sys.executable, str(SYNC), "--output", str(out_path), "--git-sha", "emit-contract"],
        check=True,
        cwd=str(REPO_ROOT),
    )
    gap = out_path.with_suffix(".gap.sql")
    subprocess.run(
        [
            sys.executable,
            str(SYNC),
            "--ops8615-gap-mirrors-only",
            "--no-begin-commit",
            "--output",
            str(gap),
            "--git-sha",
            "emit-contract",
        ],
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


def _parse_workflow_push_paths() -> set[str]:
    if not WORKFLOW.is_file():
        return set()
    in_paths = False
    found: set[str] = set()
    for line in WORKFLOW.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\s+paths:\s*$", line):
            in_paths = True
            continue
        if in_paths:
            m = _WORKFLOW_PATH_RE.match(line)
            if m:
                found.add(m.group(1))
                continue
            if line.strip() and not line.startswith(" " * 6):
                break
    return found


def _check_workflow_wiring(registry_rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    if not WORKFLOW.is_file():
        return ["missing supabase-mirror-sync.yml"]
    text = WORKFLOW.read_text(encoding="utf-8")
    required = (
        ("ops8615-gap-mirrors-only", "gap mirror splice"),
        ("validate_mirror_enum_parity.py", "enum parity preflight"),
        ("--single-transaction", "atomic apply"),
        ("emit_mirror_delete_reconcile.py", "delete-reconcile step"),
        ("validate_canonical_governance_registry.py", "governance registry preflight"),
    )
    for needle, label in required:
        if needle not in text:
            errors.append(f"workflow missing {label} ({needle})")

    try:
        expected_paths = set(plane2_workflow_path_union(registry_rows))
    except ValueError as exc:
        errors.append(str(exc))
        expected_paths = set()

    workflow_paths = _parse_workflow_push_paths()
    if expected_paths and workflow_paths != expected_paths:
        missing = sorted(expected_paths - workflow_paths)
        extra = sorted(workflow_paths - expected_paths)
        if missing:
            errors.append(
                f"workflow paths missing {len(missing)} registry path(s): {missing[:3]}"
            )
        if extra:
            errors.append(
                f"workflow paths have {len(extra)} extra path(s) vs registry: {extra[:3]}"
            )

    return errors


def _load_emit_contracts() -> list[tuple[str, str]]:
    if not REGISTRY.is_file():
        return []
    rows = iter_emit_contract_rows(load_registry_rows(REGISTRY))
    contracts: list[tuple[str, str]] = []
    for row in rows:
        csv_path = (row.get("csv_path") or "").strip()
        mirror_tbl = mirror_table_short_name(row)
        if csv_path and mirror_tbl:
            contracts.append((csv_path, mirror_tbl))
    return contracts


def run_checks() -> list[str]:
    errors: list[str] = []
    if not REGISTRY.is_file():
        return [f"missing registry at {CSV_PATH_RELATIVE}"]

    registry_rows = load_registry_rows(REGISTRY)
    emit_contracts = _load_emit_contracts()
    if not emit_contracts:
        errors.append("no emit-contract rows from CANONICAL_GOVERNANCE_REGISTRY")
    errors.extend(_check_workflow_wiring(registry_rows))

    for script in (SYNC, RECONCILE, ENUM_PARITY):
        if not script.is_file():
            errors.append(f"missing script {script.name}")

    with tempfile.TemporaryDirectory() as tmp:
        sql_path = Path(tmp) / "mirror-upsert.sql"
        _emit_full_sql(sql_path)
        insert_counts = _count_inserts(sql_path)

        for csv_rel, mirror_tbl in emit_contracts:
            csv_n = _csv_row_count(REPO_ROOT / csv_rel)
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
    rows = load_registry_rows(REGISTRY)
    union = plane2_workflow_path_union(rows)
    assert len(union) >= 10
    engagement = (
        "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/"
        "dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv"
    )
    assert engagement in union
    contracts = _load_emit_contracts()
    assert len(contracts) >= 10
    print("PASS: validate_mirror_emit_contract self-test")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    emit_contracts = _load_emit_contracts()
    errors = run_checks()
    if errors:
        print(f"FAIL: {len(errors)} mirror-emit-contract finding(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(
        f"PASS: mirror emit contract — {len(emit_contracts)} tables, "
        "CSV row counts match emitted INSERTs; workflow wiring OK"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
