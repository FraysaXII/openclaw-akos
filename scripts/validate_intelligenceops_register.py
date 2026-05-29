"""Validator for INTELLIGENCEOPS_REGISTER.csv (Initiative 72 P6).

Per `D-IH-72-H` (sibling canonical CSV) + `D-IH-72-I` (regulator-relationship
roadmap) + `D-IH-72-J` (media-counterparty-onboarding) + `D-IH-72-K`
(recruiter onboarding cross-link).

Enforces:
1. Schema (header column order + completeness) per
   ``akos.hlk_intelligenceops_register_csv.INTELLIGENCEOPS_REGISTER_FIELDNAMES``.
2. ``register_id`` regex ``^IO-[A-Z0-9-]{4,80}$``.
3. Enum constraints on ``target_class``, ``cadence``, ``source_type``,
   ``reliability``, ``lifecycle_status`` (per the akos SSOT module).
4. ``target_id`` FK-by-convention to ``GOI_POI_REGISTER.csv ref_id`` —
   accepts ``TODO[OPERATOR-...]`` markers per akos-governance-remediation.mdc
   precedent (operator-visible scaffolds).
5. ``intro_decision_id`` FK-by-convention to ``DECISION_REGISTER.csv``.
6. ``responsible_role`` FK-by-convention to ``baseline_organisation.csv``
   ``role_name``.
7. ``linked_sop_path`` and ``linked_runbook_path`` accept ``TODO[I73-...]``
   markers for forward-charters per `D-IH-72-W` feature-flag pattern
   (akos-executable-process-catalog.mdc Rule 1 satisfied via TODO marker
   when downstream initiative will author the artifact).

Exit code: 0 PASS, 1 FAIL.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_intelligenceops_register_csv import (  # noqa: E402
    INTELLIGENCEOPS_REGISTER_FIELDNAMES,
    VALID_CADENCES,
    VALID_LIFECYCLE_STATUSES,
    VALID_RELIABILITY_GRADES,
    VALID_SOURCE_TYPES,
    VALID_STALENESS_POSTURES,
    VALID_TARGET_CLASSES,
    VALID_VOLATILITY_CLASSES,
)

REGISTER_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "Research" / "Intelligence" / "canonicals" / "dimensions"
    / "INTELLIGENCEOPS_REGISTER.csv"
)
GOI_POI_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "Compliance" / "canonicals" / "dimensions"
    / "GOI_POI_REGISTER.csv"
)
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

REGISTER_ID_RE = re.compile(r"^IO-[A-Z0-9-]{4,80}$")
TODO_MARKER_RE = re.compile(r"^TODO\[[A-Za-z0-9_\-:]+\]$")


def _load_csv_column(path: Path, column: str) -> set[str]:
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return {row[column] for row in reader if row.get(column)}


def main() -> int:
    if not REGISTER_PATH.exists():
        print(f"FAIL: INTELLIGENCEOPS_REGISTER.csv not found at {REGISTER_PATH}")
        return 1

    goi_ids = _load_csv_column(GOI_POI_PATH, "ref_id")
    decision_ids = _load_csv_column(DECISION_REGISTER_PATH, "decision_id")
    org_role_names = _load_csv_column(BASELINE_ORG_PATH, "role_name")

    errors: list[str] = []
    warnings: list[str] = []
    rows_seen = 0
    by_class: dict[str, int] = {}

    with REGISTER_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != INTELLIGENCEOPS_REGISTER_FIELDNAMES:
            errors.append(
                f"Schema mismatch: header={reader.fieldnames!r} expected={list(INTELLIGENCEOPS_REGISTER_FIELDNAMES)!r}"
            )
        for line_no, row in enumerate(reader, start=2):
            rows_seen += 1
            rid = row.get("register_id", "")
            if not REGISTER_ID_RE.match(rid):
                errors.append(f"L{line_no}: register_id {rid!r} fails regex {REGISTER_ID_RE.pattern}")
            tc = row.get("target_class", "")
            if tc not in VALID_TARGET_CLASSES:
                errors.append(f"L{line_no} {rid}: target_class {tc!r} not in {sorted(VALID_TARGET_CLASSES)}")
            else:
                by_class[tc] = by_class.get(tc, 0) + 1
            cad = row.get("cadence", "")
            if cad not in VALID_CADENCES:
                errors.append(f"L{line_no} {rid}: cadence {cad!r} not in {sorted(VALID_CADENCES)}")
            st = row.get("source_type", "")
            if st not in VALID_SOURCE_TYPES:
                errors.append(f"L{line_no} {rid}: source_type {st!r} not in {sorted(VALID_SOURCE_TYPES)}")
            rel = row.get("reliability", "")
            if rel not in VALID_RELIABILITY_GRADES:
                errors.append(f"L{line_no} {rid}: reliability {rel!r} not in {sorted(VALID_RELIABILITY_GRADES)}")
            ls = row.get("lifecycle_status", "")
            if ls not in VALID_LIFECYCLE_STATUSES:
                errors.append(f"L{line_no} {rid}: lifecycle_status {ls!r} not in {sorted(VALID_LIFECYCLE_STATUSES)}")
            tid = row.get("target_id", "")
            if tid and not TODO_MARKER_RE.match(tid):
                if tid not in goi_ids:
                    errors.append(f"L{line_no} {rid}: target_id {tid!r} not found in GOI_POI_REGISTER.csv ref_id")
            elif tid and TODO_MARKER_RE.match(tid):
                if ls != "scaffold":
                    warnings.append(
                        f"L{line_no} {rid}: TODO target_id {tid!r} should pair with lifecycle_status=scaffold (got {ls!r})"
                    )
            did = row.get("intro_decision_id", "")
            if did and did not in decision_ids:
                errors.append(f"L{line_no} {rid}: intro_decision_id {did!r} not found in DECISION_REGISTER.csv")
            rr = row.get("responsible_role", "")
            if rr and rr not in org_role_names:
                errors.append(f"L{line_no} {rid}: responsible_role {rr!r} not found in baseline_organisation.csv role_name")
            sp = row.get("linked_sop_path", "")
            if sp and not TODO_MARKER_RE.match(sp):
                sop_p = REPO_ROOT / sp
                if not sop_p.exists():
                    errors.append(f"L{line_no} {rid}: linked_sop_path {sp!r} does not resolve")
            rp = row.get("linked_runbook_path", "")
            if rp and not TODO_MARKER_RE.match(rp):
                rb_p = REPO_ROOT / rp
                if not rb_p.exists():
                    errors.append(f"L{line_no} {rid}: linked_runbook_path {rp!r} does not resolve")
            vc = row.get("volatility_class", "")
            if vc and vc not in VALID_VOLATILITY_CLASSES:
                errors.append(
                    f"L{line_no} {rid}: volatility_class {vc!r} not in {sorted(VALID_VOLATILITY_CLASSES)}"
                )
            sp_posture = row.get("staleness_posture", "")
            if sp_posture and sp_posture not in VALID_STALENESS_POSTURES:
                errors.append(
                    f"L{line_no} {rid}: staleness_posture {sp_posture!r} not in {sorted(VALID_STALENESS_POSTURES)}"
                )
            sd = row.get("staleness_days", "").strip()
            if sp_posture == "none" and sd:
                errors.append(f"L{line_no} {rid}: staleness_posture=none requires empty staleness_days")
            if sp_posture in {"cite_and_flag", "block_govern"} and not sd:
                errors.append(
                    f"L{line_no} {rid}: staleness_posture={sp_posture!r} requires staleness_days"
                )

    print()
    print("  INTELLIGENCEOPS_REGISTER Validator")
    print("  =" * 25)
    print(f"  Rows validated: {rows_seen}")
    print(f"  By class: {by_class}")
    if warnings:
        print()
        print("  Warnings:")
        for w in warnings:
            print(f"    - {w}")
    if errors:
        print()
        print("  ERRORS:")
        for e in errors:
            print(f"    - {e}")
        print("  FAIL")
        return 1
    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
