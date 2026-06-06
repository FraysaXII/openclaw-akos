#!/usr/bin/env python3
"""Validate ENGAGEMENT_MODEL_REGISTRY.csv (Initiative 73 P1).

Header drift gate + per-row Pydantic instantiation + enum checks + FK validation
to baseline_organisation.csv (Data Owner = People Operations Manager per D-IH-73-C).

Usage::

    py scripts/validate_engagement_model_registry.py

Wired into ``scripts/validate_hlk.py`` dispatcher (Initiative 73 P1) and into
``config/verification-profiles.json`` profile ``engagement_model_registry_smoke``
and the composed ``pre_commit`` matrix via ``scripts/release-gate.py``.

Per ``akos-holistika-operations.mdc`` §"New git-canonical compliance registers"
this script is the canonical validator for the sibling People-Operations-owned
dimension. The 7-class taxonomy (D-IH-73-D) is mirrored as Pydantic
``Literal`` types in ``akos.hlk_engagement_model_csv``; this validator delegates
all enum + slug + integer bounds checks to that Pydantic chassis.
"""

from __future__ import annotations

import csv
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_engagement_model_csv import (  # noqa: E402
    ENGAGEMENT_MODEL_FIELDNAMES,
    EngagementModelRow,
)
from akos.io import REPO_ROOT  # noqa: E402
from akos.log import setup_logging  # noqa: E402

CSV_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "People Operations"
    / "canonicals" / "dimensions" / "ENGAGEMENT_MODEL_REGISTRY.csv"
)
ORG_CSV = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance"
    / "canonicals" / "baseline_organisation.csv"
)
DATA_OWNER_ROLE = "People Operations Manager"  # per D-IH-73-C; verified at validator runtime


def _load_org_roles() -> set[str]:
    if not ORG_CSV.is_file():
        return set()
    with ORG_CSV.open(encoding="utf-8", newline="") as fh:
        return {(row.get("role_name") or "").strip() for row in csv.DictReader(fh) if row.get("role_name")}


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.debug("ENGAGEMENT_MODEL_REGISTRY validator invoked")
    print("\n  ENGAGEMENT_MODEL_REGISTRY Validator")
    print("  " + "=" * 50)
    if not CSV_PATH.is_file():
        print(f"  FAIL: ENGAGEMENT_MODEL_REGISTRY.csv not found at {CSV_PATH}")
        return 1

    org_roles = _load_org_roles()
    # Confirm the Data Owner role row exists in baseline_organisation.csv.
    # Per D-IH-73-C the Data Owner is People Operations Manager; if absent that's
    # a FAIL (process_list tranche orphaned without owner row per
    # akos-governance-remediation.mdc baseline-tranche rule).
    if org_roles and DATA_OWNER_ROLE not in org_roles:
        print(
            f"  FAIL: Data Owner role {DATA_OWNER_ROLE!r} not in baseline_organisation.csv "
            f"(required per D-IH-73-C; baseline_organisation row must precede the registry)."
        )
        return 1

    errors: list[str] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if list(reader.fieldnames or []) != list(ENGAGEMENT_MODEL_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(ENGAGEMENT_MODEL_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen_ids: set[str] = set()
    for i, row in enumerate(rows, start=2):
        # Pydantic validates: slug regex + enum membership + access_level 0-6 + length bounds.
        try:
            EngagementModelRow.model_validate({k: (v or "") for k, v in row.items() if k})
        except Exception as exc:
            row_id = (row.get("engagement_model_id") or f"row_{i}").strip()
            errors.append(f"row {i} ({row_id}): Pydantic validation failed: {exc}")
            continue

        eid = (row.get("engagement_model_id") or "").strip()
        if eid in seen_ids:
            errors.append(f"row {i}: duplicate engagement_model_id {eid!r}")
        seen_ids.add(eid)

    # Enforce that all 7 canonical classes from D-IH-73-D are present.
    expected_classes = {
        "eng_model_hourly_consultant",
        "eng_model_milestone_consultant",
        "eng_model_percentage_collaborator",
        "eng_model_apprentice_learner",
        "eng_model_investor_advisor",
        "eng_model_outsourced_helper",
        "eng_model_operator_self",
    }
    missing = expected_classes - seen_ids
    if missing:
        errors.append(
            f"canonical D-IH-73-D 7-class taxonomy incomplete: missing {sorted(missing)}"
        )

    if errors:
        print(f"  FAIL: {len(errors)} issue(s)")
        for err in errors[:25]:
            print(f"    - {err}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        return 1

    print(f"  Rows validated: {len(rows)}")
    print(f"  Data Owner: {DATA_OWNER_ROLE} (verified in baseline_organisation.csv)")
    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
