"""Validator for RENDERING_PIPELINE_REGISTRY.csv (Initiative 77 P4.C).

Per `D-IH-77-I` (visual UAT rendering discipline + orphan-rendering-pipeline
governance discovery).

Enforces:
1. Schema (header column order + completeness) per
   ``akos.hlk_rendering_pipeline_csv.RENDERING_PIPELINE_FIELDNAMES``.
2. ``pipeline_id`` regex ``^[a-z0-9_]{3,80}$``.
3. Enum constraints on ``trigger_type`` / ``status`` /
   ``governance_class`` / ``brand_tokens_consumed``.
4. ``owning_role`` FK-by-convention to ``baseline_organisation.csv`` ``role_name``.
5. ``linked_decision_id`` FK-by-convention to ``DECISION_REGISTER.csv``.
6. ``sop_path`` and ``runbook_path`` exist on disk OR carry ``TODO[I-NN-...]``
   marker (per ``akos-executable-process-catalog.mdc`` Rule 1: every governed
   pipeline must have a paired SOP + runbook, with TODO marker accepted as
   forward-charter scaffold per D-IH-72-W feature-flag pattern).
7. ``trigger_command`` non-empty.
8. ``input_paths`` + ``output_paths`` non-empty (every pipeline has at least
   one input source and one output destination).

Pipelines in ``status=deprecated`` are exempt from SOP/runbook existence
checks (deprecated rows are historical record only).

Exit code: 0 PASS, 1 FAIL.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_rendering_pipeline_csv import (  # noqa: E402
    CANONICAL_PATH,
    RENDERING_PIPELINE_FIELDNAMES,
    VALID_BRAND_TOKENS_CONSUMED,
    VALID_GOVERNANCE_CLASSES,
    VALID_STATUSES,
    VALID_TRIGGER_TYPES,
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

PIPELINE_ID_RE = re.compile(r"^[a-z0-9_]{3,80}$")
TODO_MARKER_RE = re.compile(r"^TODO\[[A-Za-z0-9_\-:]+\]$")


def _load_csv_column(path: Path, column: str) -> set[str]:
    if not path.exists():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return {row[column] for row in reader if row.get(column)}


def _check_path_or_todo(value: str, *, must_exist: bool) -> str | None:
    """Return None if OK, else error string."""
    if not value:
        return "empty value"
    if TODO_MARKER_RE.match(value):
        return None
    if must_exist:
        candidate = (REPO_ROOT / value).resolve()
        if not candidate.exists():
            return f"path does not exist: {value!r}"
    return None


def main() -> int:
    if not REGISTRY_PATH.exists():
        print(f"FAIL: RENDERING_PIPELINE_REGISTRY.csv not found at {REGISTRY_PATH}")
        return 1

    decision_ids = _load_csv_column(DECISION_REGISTER_PATH, "decision_id")
    role_names = _load_csv_column(BASELINE_ORG_PATH, "role_name")

    errors: list[str] = []
    warnings: list[str] = []
    rows_seen = 0
    by_status: dict[str, int] = {}
    by_governance: dict[str, int] = {}
    pipeline_ids: set[str] = set()

    with REGISTRY_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != RENDERING_PIPELINE_FIELDNAMES:
            errors.append(
                f"Schema mismatch: header={reader.fieldnames!r} "
                f"expected={list(RENDERING_PIPELINE_FIELDNAMES)!r}"
            )
        for line_no, row in enumerate(reader, start=2):
            rows_seen += 1
            pid = row.get("pipeline_id", "")

            if not PIPELINE_ID_RE.match(pid):
                errors.append(
                    f"L{line_no}: pipeline_id {pid!r} fails regex {PIPELINE_ID_RE.pattern}"
                )
            if pid in pipeline_ids:
                errors.append(f"L{line_no}: duplicate pipeline_id {pid!r}")
            pipeline_ids.add(pid)

            tt = row.get("trigger_type", "")
            if tt not in VALID_TRIGGER_TYPES:
                errors.append(
                    f"L{line_no} {pid}: trigger_type {tt!r} not in {sorted(VALID_TRIGGER_TYPES)}"
                )

            status = row.get("status", "")
            if status not in VALID_STATUSES:
                errors.append(
                    f"L{line_no} {pid}: status {status!r} not in {sorted(VALID_STATUSES)}"
                )
            else:
                by_status[status] = by_status.get(status, 0) + 1

            gc = row.get("governance_class", "")
            if gc not in VALID_GOVERNANCE_CLASSES:
                errors.append(
                    f"L{line_no} {pid}: governance_class {gc!r} not in {sorted(VALID_GOVERNANCE_CLASSES)}"
                )
            else:
                by_governance[gc] = by_governance.get(gc, 0) + 1

            btc = row.get("brand_tokens_consumed", "")
            if btc not in VALID_BRAND_TOKENS_CONSUMED:
                errors.append(
                    f"L{line_no} {pid}: brand_tokens_consumed {btc!r} not in {sorted(VALID_BRAND_TOKENS_CONSUMED)}"
                )

            if not row.get("trigger_command", "").strip():
                errors.append(f"L{line_no} {pid}: trigger_command must be non-empty")
            if not row.get("input_paths", "").strip():
                errors.append(f"L{line_no} {pid}: input_paths must be non-empty")
            if not row.get("output_paths", "").strip():
                errors.append(f"L{line_no} {pid}: output_paths must be non-empty")

            owning_role = row.get("owning_role", "")
            if role_names and owning_role and owning_role not in role_names:
                warnings.append(
                    f"L{line_no} {pid}: owning_role {owning_role!r} "
                    f"not in baseline_organisation role_name set"
                )

            ldid = row.get("linked_decision_id", "")
            if decision_ids and ldid and ldid not in decision_ids:
                errors.append(
                    f"L{line_no} {pid}: linked_decision_id {ldid!r} "
                    f"not in DECISION_REGISTER decision_id set"
                )

            # SOP + runbook path validation (skip for deprecated rows)
            if status != "deprecated":
                sop_err = _check_path_or_todo(row.get("sop_path", ""), must_exist=True)
                if sop_err:
                    errors.append(f"L{line_no} {pid}: sop_path {sop_err}")
                rb_err = _check_path_or_todo(row.get("runbook_path", ""), must_exist=True)
                if rb_err:
                    errors.append(f"L{line_no} {pid}: runbook_path {rb_err}")

    if errors:
        print("FAIL: RENDERING_PIPELINE_REGISTRY validation errors:")
        for e in errors:
            print(f"  {e}")
        for w in warnings:
            print(f"  [WARN] {w}")
        return 1

    summary_by_status = ", ".join(f"{k}={v}" for k, v in sorted(by_status.items()))
    summary_by_governance = ", ".join(f"{k}={v}" for k, v in sorted(by_governance.items()))
    print(
        f"PASS: RENDERING_PIPELINE_REGISTRY validated "
        f"({rows_seen} rows; by_status={{{summary_by_status}}}; "
        f"by_governance={{{summary_by_governance}}})"
    )
    for w in warnings:
        print(f"  [WARN] {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
