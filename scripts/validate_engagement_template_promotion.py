#!/usr/bin/env python3
"""Initiative 72 P3 — Validator paired with SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md.

Enforces the promotion gate codified in
``docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md``
per [`akos-executable-process-catalog.mdc`](../.cursor/rules/akos-executable-process-catalog.mdc)
Rule 1 (SOP + executable runbook pairing).

Schema enforcement (extends ``validate_engagement_template_registry.py``):
- Every row with ``lifecycle_status=active`` MUST have a non-empty
  ``promotion_decision_id`` that resolves to ``DECISION_REGISTER.csv``.
- ``promotion_decision_id`` for ``scaffold`` templates MUST be the bootstrap
  pointer ``D-IH-72-F`` (or a successor bootstrap decision) — never empty.
- ``last_review_decision_id`` for ``active`` templates MUST equal
  ``promotion_decision_id`` OR be a successor decision in the same decision
  family (advisory check; warning not error).
- ``deprecated`` templates MUST have a non-empty ``notes`` field describing
  the deprecation rationale + the successor template id (when applicable).

Usage::

    py scripts/validate_engagement_template_promotion.py

Wired into ``scripts/validate_hlk.py`` dispatcher per the canonical-CSV
discipline (see ``akos-governance-remediation.mdc``).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_engagement_template_registry_csv import (
    ENGAGEMENT_TEMPLATE_REGISTRY_FIELDNAMES,
    VALID_LIFECYCLE_STATUSES,
)
from akos.io import REPO_ROOT

CSV_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "RevOps"
    / "canonicals" / "dimensions" / "ENGAGEMENT_TEMPLATE_REGISTRY.csv"
)
DECISION_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People"
    / "Compliance" / "canonicals" / "DECISION_REGISTER.csv"
)

# Bootstrap promotion-decision pointers acceptable for `scaffold` rows.
# Successor initiatives may extend this set (forward-compatible).
BOOTSTRAP_PROMOTION_DECISION_IDS: frozenset[str] = frozenset({
    "D-IH-72-F",   # I72 P0 charter ratification of sibling registry pattern.
    "D-IH-72-A",   # I72 P0 inception charter.
    "D-IH-72-AH",  # I72 Round 8 Operations/RevOps area charter at P1.
})


def _load_csv_set(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8", newline="") as fh:
        return {(row.get(key) or "").strip() for row in csv.DictReader(fh) if row.get(key)}


def main() -> int:
    print("\n  ENGAGEMENT_TEMPLATE_PROMOTION Gate Validator")
    print("  " + "=" * 50)
    if not CSV_PATH.is_file():
        print("  SKIP: ENGAGEMENT_TEMPLATE_REGISTRY.csv not present")
        return 0

    decision_ids = _load_csv_set(DECISION_CSV, "decision_id")

    errors: list[str] = []
    warnings: list[str] = []
    counts: dict[str, int] = {s: 0 for s in VALID_LIFECYCLE_STATUSES}

    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != list(ENGAGEMENT_TEMPLATE_REGISTRY_FIELDNAMES):
            print("  SKIP: header mismatch (validate_engagement_template_registry.py owns header check)")
            return 0
        rows = list(reader)

    for r in rows:
        tid = (r.get("template_id") or "").strip()
        ls = (r.get("lifecycle_status") or "").strip()
        pdid = (r.get("promotion_decision_id") or "").strip()
        lrdid = (r.get("last_review_decision_id") or "").strip()
        notes = (r.get("notes") or "").strip()

        if ls not in counts:
            continue  # owned by registry validator
        counts[ls] += 1

        if ls == "active":
            if not pdid:
                errors.append(
                    f"{tid}: lifecycle_status=active requires non-empty promotion_decision_id "
                    f"per SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md §4.4"
                )
                continue
            if pdid in BOOTSTRAP_PROMOTION_DECISION_IDS:
                errors.append(
                    f"{tid}: lifecycle_status=active but promotion_decision_id={pdid} is a bootstrap pointer; "
                    f"active templates MUST carry a per-template promotion ratification decision"
                )
            if decision_ids and pdid not in decision_ids:
                errors.append(
                    f"{tid}: promotion_decision_id={pdid!r} does not resolve to DECISION_REGISTER.csv"
                )
            if lrdid and decision_ids and lrdid not in decision_ids:
                warnings.append(
                    f"{tid}: last_review_decision_id={lrdid!r} does not resolve to DECISION_REGISTER.csv"
                )

        elif ls == "scaffold":
            if not pdid:
                errors.append(
                    f"{tid}: lifecycle_status=scaffold requires non-empty promotion_decision_id "
                    f"(use bootstrap pointer like D-IH-72-F until promotion)"
                )
            elif pdid not in BOOTSTRAP_PROMOTION_DECISION_IDS and decision_ids and pdid not in decision_ids:
                errors.append(
                    f"{tid}: promotion_decision_id={pdid!r} does not resolve and is not a bootstrap pointer "
                    f"({sorted(BOOTSTRAP_PROMOTION_DECISION_IDS)})"
                )

        elif ls == "deprecated":
            if not notes:
                errors.append(
                    f"{tid}: lifecycle_status=deprecated requires non-empty notes describing rationale + successor template id"
                )

    print(f"  Templates by status:")
    for s in sorted(counts):
        print(f"    {s:<12} {counts[s]}")

    if warnings:
        print(f"  Warnings (advisory; not failing): {len(warnings)}")
        for w in warnings[:5]:
            print(f"    - {w}")
        if len(warnings) > 5:
            print(f"    ... and {len(warnings) - 5} more")

    if errors:
        print(f"  FAIL: {len(errors)} promotion-gate errors")
        for e in errors[:10]:
            print(f"    - {e}")
        if len(errors) > 10:
            print(f"    ... and {len(errors) - 10} more")
        return 1

    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
