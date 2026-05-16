#!/usr/bin/env python3
"""Validate KNOWLEDGE_PAIRING_REGISTRY.csv (Initiative 80 P6.5).

Mints the documentation-relationship registry that codifies the operator's
2026-05-16 framing (paired files, indices, doctrine companions, and any other
canonical-asset relationship are governed via this CSV; PRECEDENCE.md remains
the human-readable companion). Registry is consumed by:

- DAMA Metadata Management knowledge area (per `D-IH-80-G` Pydantic + validator
  + mirror pattern parity).
- Supabase mirror ``compliance.knowledge_pairing_registry_mirror`` (forward).
- hlk-erp Knowledge panels (forward; per area-owned panel design).
- AI Archivist / KiRBe ingestor (I83 candidate; consumes the registry to know
  which files are paired so it can return body+addendum together when an
  operator asks a depth question).

Validation rules (per `D-IH-80-H`):

1. **Header drift gate** — CSV header must equal ``KNOWLEDGE_PAIRING_FIELDNAMES``
   exactly; any drift = FAIL.

2. **Per-row Pydantic instantiation** — every row passes through
   ``KnowledgePairingRow`` (extra='forbid'); Pydantic validation errors
   propagate as FAIL with row-index detail.

3. **pairing_id uniqueness** — no two rows share the same ``pairing_id``.

4. **parent_doc_path resolution** — every ``parent_doc_path`` MUST exist on
   disk (workspace-relative). Missing files = FAIL.

5. **companion_doc_paths resolution** — every path in the semicolon-list MUST
   exist on disk. Empty entries skipped; missing files = FAIL.

6. **pattern_id FK resolution** — every ``pattern_id`` MUST resolve to a row
   in ``PEOPLE_DESIGN_PATTERN_REGISTRY.csv``. Missing FK = FAIL.

7. **last_review_decision_id FK resolution** — every ``last_review_decision_id``
   MUST resolve to a row in ``DECISION_REGISTER.csv``. Missing FK = FAIL.

Wired into ``scripts/validate_hlk.py`` dispatcher and
``config/verification-profiles.json`` profile ``pre_commit``.

Usage::

    py scripts/validate_knowledge_pairing_registry.py

Exit codes::

    0 — PASS (registry valid; all FKs resolve; all referenced files exist).
    1 — FAIL (any rule violated).

Cross-references: ``akos-holistika-operations.mdc`` §"New git-canonical compliance
registers (pattern)" (this validator follows that pattern); ``akos-executable-process-catalog.mdc``
RULE 1 (paired SOP+runbook is one of the seven pairing_class values registered);
``akos-planning-traceability.mdc`` (initiative-meta context).
"""

from __future__ import annotations

import csv
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_knowledge_pairing_csv import (  # noqa: E402
    KNOWLEDGE_PAIRING_FIELDNAMES,
    KnowledgePairingRow,
)
from pydantic import ValidationError  # noqa: E402

logger = logging.getLogger("validate_knowledge_pairing_registry")
logging.basicConfig(level=logging.INFO, format="%(message)s")

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_PAIRING_REGISTRY_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Compliance"
    / "canonicals"
    / "dimensions"
    / "KNOWLEDGE_PAIRING_REGISTRY.csv"
)
DESIGN_PATTERN_REGISTRY_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Compliance"
    / "canonicals"
    / "dimensions"
    / "PEOPLE_DESIGN_PATTERN_REGISTRY.csv"
)
DECISION_REGISTER_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Compliance"
    / "canonicals"
    / "DECISION_REGISTER.csv"
)


def _load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _load_pattern_ids() -> set[str]:
    return {row["pattern_id"] for row in _load_csv_rows(DESIGN_PATTERN_REGISTRY_PATH)}


def _load_decision_ids() -> set[str]:
    return {row["decision_id"] for row in _load_csv_rows(DECISION_REGISTER_PATH)}


def validate_knowledge_pairing_registry() -> int:
    if not KNOWLEDGE_PAIRING_REGISTRY_PATH.exists():
        logger.error("FAIL: KNOWLEDGE_PAIRING_REGISTRY.csv not found at %s", KNOWLEDGE_PAIRING_REGISTRY_PATH)
        return 1

    errors: list[str] = []

    with KNOWLEDGE_PAIRING_REGISTRY_PATH.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        actual_fieldnames = tuple(reader.fieldnames or ())
        if actual_fieldnames != KNOWLEDGE_PAIRING_FIELDNAMES:
            errors.append(
                f"Header drift: expected {KNOWLEDGE_PAIRING_FIELDNAMES!r}, "
                f"got {actual_fieldnames!r}"
            )
            logger.error("\n".join(errors))
            return 1
        rows = list(reader)

    pattern_ids = _load_pattern_ids()
    decision_ids = _load_decision_ids()

    seen_ids: set[str] = set()

    for idx, row in enumerate(rows, start=2):
        try:
            KnowledgePairingRow(**row)
        except ValidationError as exc:
            errors.append(f"Row {idx} ({row.get('pairing_id', '<missing>')}): {exc}")
            continue

        pairing_id = row["pairing_id"]
        if pairing_id in seen_ids:
            errors.append(f"Row {idx}: duplicate pairing_id '{pairing_id}'")
        else:
            seen_ids.add(pairing_id)

        parent_path = REPO_ROOT / row["parent_doc_path"]
        if not parent_path.exists():
            errors.append(
                f"Row {idx} ({pairing_id}): parent_doc_path '{row['parent_doc_path']}' "
                f"does not exist on disk"
            )

        companion_paths_raw = row["companion_doc_paths"].strip()
        if companion_paths_raw:
            for comp_rel in [p.strip() for p in companion_paths_raw.split(";") if p.strip()]:
                comp_path = REPO_ROOT / comp_rel
                if not comp_path.exists():
                    errors.append(
                        f"Row {idx} ({pairing_id}): companion_doc_path '{comp_rel}' "
                        f"does not exist on disk"
                    )

        if row["pattern_id"] not in pattern_ids:
            errors.append(
                f"Row {idx} ({pairing_id}): pattern_id '{row['pattern_id']}' "
                f"does not resolve in PEOPLE_DESIGN_PATTERN_REGISTRY.csv"
            )

        if row["last_review_decision_id"] not in decision_ids:
            errors.append(
                f"Row {idx} ({pairing_id}): last_review_decision_id "
                f"'{row['last_review_decision_id']}' does not resolve in DECISION_REGISTER.csv"
            )

    print()
    print("  KNOWLEDGE_PAIRING_REGISTRY Validator")
    print("  " + "=" * 50)
    print(f"  Rows validated: {len(rows)}")
    pairing_classes = sorted({r["pairing_class"] for r in rows})
    print(f"  Pairing classes:    {pairing_classes}")
    areas = sorted({r["area"] for r in rows})
    print(f"  Areas:              {areas}")
    if errors:
        print(f"  FAIL: {len(errors)} errors")
        for err in errors:
            print(f"    - {err}")
        return 1
    print("  PASS")
    return 0


def main() -> int:
    return validate_knowledge_pairing_registry()


if __name__ == "__main__":
    sys.exit(main())
