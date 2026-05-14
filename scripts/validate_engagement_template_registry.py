#!/usr/bin/env python3
"""Initiative 72 P2 — Validator for ENGAGEMENT_TEMPLATE_REGISTRY.csv.

Schema enforcement:
- Required header matches ``ENGAGEMENT_TEMPLATE_REGISTRY_FIELDNAMES``.
- ``template_id`` matches ``^tmpl_[a-z0-9_]{4,80}_v\\d+$``; unique.
- ``engagement_class`` is in ``VALID_ENGAGEMENT_CLASSES``.
- ``owner_role`` resolves against ``baseline_organisation.csv`` role_name.
- ``discipline_mix`` (semicolon list) — each entry in ``VALID_MARKETING_DISCIPLINES``.
- ``duration_target_days`` parses as positive integer.
- ``value_band_eur`` is in ``VALID_VALUE_BANDS``.
- ``billing_cadence`` is in ``VALID_BILLING_CADENCES``.
- ``contract_kind`` is in ``VALID_CONTRACT_KINDS``.
- ``counterparty_class`` is in ``VALID_COUNTERPARTY_CLASSES``.
- ``lifecycle_status`` is in ``VALID_LIFECYCLE_STATUSES``.
- ``promotion_decision_id`` resolves against ``DECISION_REGISTER.csv`` decision_id (when non-empty).
- ``ssot_path`` exists on disk (when non-empty).
- ``version`` matches semver.
- audit-trail columns present + non-empty ``last_review_at`` parses as ISO date.

Usage::

    py scripts/validate_engagement_template_registry.py

Wired into ``scripts/validate_hlk.py`` dispatcher per the canonical-CSV
discipline (see ``akos-governance-remediation.mdc``).
"""

from __future__ import annotations

import csv
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_engagement_template_registry_csv import (
    ENGAGEMENT_TEMPLATE_REGISTRY_FIELDNAMES,
    VALID_BILLING_CADENCES,
    VALID_CONTRACT_KINDS,
    VALID_COUNTERPARTY_CLASSES,
    VALID_ENGAGEMENT_CLASSES,
    VALID_LIFECYCLE_STATUSES,
    VALID_MARKETING_DISCIPLINES,
    VALID_VALUE_BANDS,
)
from akos.io import REPO_ROOT

CSV_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "RevOps"
    / "canonicals" / "dimensions" / "ENGAGEMENT_TEMPLATE_REGISTRY.csv"
)
ORG_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "baseline_organisation.csv"
DECISION_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "DECISION_REGISTER.csv"

TEMPLATE_ID_RE = re.compile(r"^tmpl_[a-z0-9_]{4,80}_v\d+$")
SEMVER_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def _split_semi(value: str) -> list[str]:
    return [s.strip() for s in (value or "").split(";") if s.strip()]


def main() -> int:
    print("\n  ENGAGEMENT_TEMPLATE_REGISTRY Validator")
    print("  " + "=" * 50)
    if not CSV_PATH.is_file():
        print("  SKIP: ENGAGEMENT_TEMPLATE_REGISTRY.csv not present")
        return 0

    org_roles = _load_csv_set(ORG_CSV, "role_name")
    decision_ids = _load_csv_set(DECISION_CSV, "decision_id")

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(ENGAGEMENT_TEMPLATE_REGISTRY_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(ENGAGEMENT_TEMPLATE_REGISTRY_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    for i, r in enumerate(rows, start=2):
        tid = (r.get("template_id") or "").strip()
        if not tid:
            errors.append(f"row {i}: template_id empty")
            continue
        if not TEMPLATE_ID_RE.match(tid):
            errors.append(f"row {i}: template_id {tid!r} does not match {TEMPLATE_ID_RE.pattern}")
        if tid in seen:
            errors.append(f"row {i}: template_id {tid!r} duplicated")
        seen.add(tid)

        if not (r.get("name") or "").strip():
            errors.append(f"{tid}: name empty")

        ec = (r.get("engagement_class") or "").strip()
        if ec not in VALID_ENGAGEMENT_CLASSES:
            errors.append(f"{tid}: engagement_class {ec!r} not in {sorted(VALID_ENGAGEMENT_CLASSES)}")

        owner = (r.get("owner_role") or "").strip()
        if not owner:
            errors.append(f"{tid}: owner_role empty")
        elif org_roles and owner not in org_roles:
            errors.append(f"{tid}: owner_role {owner!r} not in baseline_organisation.csv")

        disciplines = _split_semi(r.get("discipline_mix") or "")
        if not disciplines:
            errors.append(f"{tid}: discipline_mix is empty")
        for d in disciplines:
            if d not in VALID_MARKETING_DISCIPLINES:
                errors.append(
                    f"{tid}: discipline {d!r} not in VALID_MARKETING_DISCIPLINES "
                    f"({sorted(VALID_MARKETING_DISCIPLINES)})"
                )

        dur_raw = (r.get("duration_target_days") or "").strip()
        if not dur_raw:
            errors.append(f"{tid}: duration_target_days empty")
        else:
            try:
                dur = int(dur_raw)
                if dur <= 0:
                    errors.append(f"{tid}: duration_target_days {dur} must be positive")
            except ValueError:
                errors.append(f"{tid}: duration_target_days {dur_raw!r} not parseable as int")

        vb = (r.get("value_band_eur") or "").strip()
        if vb not in VALID_VALUE_BANDS:
            errors.append(f"{tid}: value_band_eur {vb!r} not in {sorted(VALID_VALUE_BANDS)}")

        bc = (r.get("billing_cadence") or "").strip()
        if bc not in VALID_BILLING_CADENCES:
            errors.append(f"{tid}: billing_cadence {bc!r} not in {sorted(VALID_BILLING_CADENCES)}")

        ck = (r.get("contract_kind") or "").strip()
        if ck not in VALID_CONTRACT_KINDS:
            errors.append(f"{tid}: contract_kind {ck!r} not in {sorted(VALID_CONTRACT_KINDS)}")

        cc = (r.get("counterparty_class") or "").strip()
        if cc not in VALID_COUNTERPARTY_CLASSES:
            errors.append(f"{tid}: counterparty_class {cc!r} not in {sorted(VALID_COUNTERPARTY_CLASSES)}")

        ls = (r.get("lifecycle_status") or "").strip()
        if ls not in VALID_LIFECYCLE_STATUSES:
            errors.append(f"{tid}: lifecycle_status {ls!r} not in {sorted(VALID_LIFECYCLE_STATUSES)}")

        pdid = (r.get("promotion_decision_id") or "").strip()
        if pdid and decision_ids and pdid not in decision_ids:
            errors.append(f"{tid}: promotion_decision_id {pdid!r} not in DECISION_REGISTER.csv")

        ssot = (r.get("ssot_path") or "").strip()
        if ssot:
            ssot_p = REPO_ROOT / ssot
            if not ssot_p.exists():
                errors.append(f"{tid}: ssot_path {ssot!r} does not resolve to file/folder on disk")

        version = (r.get("version") or "").strip()
        if not SEMVER_RE.match(version):
            errors.append(f"{tid}: version {version!r} does not match semver")

        lra = (r.get("last_review_at") or "").strip()
        if not ISO_DATE_RE.match(lra):
            errors.append(f"{tid}: last_review_at {lra!r} not ISO YYYY-MM-DD")
        else:
            try:
                date.fromisoformat(lra)
            except ValueError:
                errors.append(f"{tid}: last_review_at {lra!r} not a valid date")

        lrby = (r.get("last_review_by") or "").strip()
        if not lrby:
            errors.append(f"{tid}: last_review_by empty")
        elif org_roles and lrby not in org_roles:
            errors.append(f"{tid}: last_review_by {lrby!r} not in baseline_organisation.csv")

        lrdid = (r.get("last_review_decision_id") or "").strip()
        if lrdid and decision_ids and lrdid not in decision_ids:
            errors.append(f"{tid}: last_review_decision_id {lrdid!r} not in DECISION_REGISTER.csv")

        mvr = (r.get("methodology_version_at_review") or "").strip()
        if not mvr:
            errors.append(f"{tid}: methodology_version_at_review empty")

    print(f"  Rows validated: {len(rows)}")
    print(f"  Templates:      {len(seen)}")

    if errors:
        print(f"  FAIL: {len(errors)} errors")
        for e in errors[:10]:
            print(f"    - {e}")
        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more")
        return 1

    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
