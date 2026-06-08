#!/usr/bin/env python3
"""I95 L3 FK->verb coverage: canonical CSV columns must map to HCAM relationship triples.

Tranche-1 scope: ``process_list`` + ``baseline_organisation`` (highest articulation value per
I95 master-roadmap L3). Also validates every *active* triple's ``current_fk`` tokens resolve to
known registry columns (or approved non-CSV surfaces).

Usage::

    py scripts/validate_fk_verb_coverage.py
    py scripts/validate_fk_verb_coverage.py --self-test
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_baseline_org_csv import BASELINE_ORGANISATION_FIELDNAMES  # noqa: E402
from akos.hlk_canonical_articulation import (  # noqa: E402
    FK_NON_CSV_REGISTRY_PREFIXES,
    L3_TRANCHE1_FK_BINDINGS,
    RELATIONSHIP_REGISTRY_FIELDNAMES,
    RELATIONSHIP_REGISTRY_PATH,
    RelationshipTripleRow,
)
from akos.hlk_process_csv import PROCESS_LIST_FIELDNAMES  # noqa: E402

# Registry slug (current_fk prefix) -> allowed column names (lowercase keys for lookup).
_FK_REGISTRY_COLUMNS: dict[str, frozenset[str]] = {
    "process_list": frozenset(c.lower() for c in PROCESS_LIST_FIELDNAMES),
    "baseline_organisation": frozenset(c.lower() for c in BASELINE_ORGANISATION_FIELDNAMES),
    "capability_registry": frozenset({
        "capability_id", "role_owner", "originating_process_ids", "skill_ids", "substrate_id",
        "data_fam", "last_review_at", "last_review_by", "last_review_decision_id",
        "methodology_version_at_review",
    }),
    "decision_register": frozenset({
        "decision_id", "linked", "linked_initiative_ids", "last_review_at",
    }),
    "initiative_registry": frozenset({"initiative_id", "program_anchors", "status"}),
    "ops_register": frozenset({"ops_action_id", "linked", "status"}),
    "topic_registry": frozenset({"topic_id", "parent"}),
    "skill_registry": frozenset({"skill_id", "owner_role"}),
    "use_case_archive": frozenset({"use_case_id", "capability_id", "engagement_id"}),
    "engagement_registry": frozenset({"engagement_id", "counterparty_org_id"}),
    "metrics_registry": frozenset({"metric_id", "source_contract_id"}),
    "bi_consumer_registry": frozenset({"consumer_id", "component_id", "data_surfaces"}),
    "data_contract_registry": frozenset({
        "contract_id", "producer_process_id", "consumer_area_ids", "data_surface",
    }),
    "area_bi_profile": frozenset({"area_id", "primary_consumer_ids"}),
    "goi_poi_register": frozenset({"goal_id", "process_item_id", "program_id"}),
    "aic_capability_implementation_matrix": frozenset({
        "matrix_id", "capability_id", "aic_id",
    }),
    "persona_scenario_registry": frozenset({"scenario_id", "persona_id"}),
}


def _normalize_registry_slug(slug: str) -> str:
    return slug.strip().lower().replace("-", "_")


def _parse_fk_token(token: str) -> tuple[str, str] | None:
    token = (token or "").strip()
    if not token or token.lower() == "new":
        return None
    if "." not in token:
        return None
    reg, col = token.split(".", 1)
    return _normalize_registry_slug(reg), col.strip().lower()


def _read_registry(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _triple_by_id(rows: list[dict[str, str]]) -> dict[str, RelationshipTripleRow]:
    out: dict[str, RelationshipTripleRow] = {}
    for raw in rows:
        row = RelationshipTripleRow(**raw)
        out[row.triple_id] = row
    return out


def run_checks(registry_path: Path = RELATIONSHIP_REGISTRY_PATH) -> list[str]:
    errors: list[str] = []
    if not registry_path.is_file():
        return [f"missing relationship registry: {registry_path}"]

    raw_rows = _read_registry(registry_path)
    triples = _triple_by_id(raw_rows)

    # L3 tranche-1: mandatory bindings
    for reg_slug, col, triple_id in L3_TRANCHE1_FK_BINDINGS:
        triple = triples.get(triple_id)
        if triple is None:
            errors.append(f"L3 binding {reg_slug}.{col} -> {triple_id}: triple missing")
            continue
        if triple.status != "active":
            errors.append(f"L3 binding {reg_slug}.{col} -> {triple_id}: triple not active")
            continue
        needle = f"{reg_slug}.{col}".lower()
        fk_blob = (triple.current_fk or "").lower()
        if needle not in fk_blob:
            errors.append(
                f"L3 binding {reg_slug}.{col} must appear in {triple_id}.current_fk "
                f"(got {triple.current_fk!r})"
            )

    # Active triples must not use placeholder FK
    for tid, triple in triples.items():
        if triple.status != "active":
            continue
        fk = (triple.current_fk or "").strip()
        if not fk or fk.lower() == "new":
            errors.append(f"{tid}: active triple has placeholder current_fk={fk!r}")

    non_csv = {_normalize_registry_slug(x) for x in FK_NON_CSV_REGISTRY_PREFIXES}

    # Parse every *active* triple current_fk token against registry column SSOT.
    for tid, triple in triples.items():
        if triple.status != "active":
            continue
        fk = (triple.current_fk or "").strip()
        if not fk or fk.lower() == "new":
            continue
        for part in fk.split(";"):
            part = part.strip()
            if not part or part.lower() == "new":
                continue
            if "." not in part:
                slug = _normalize_registry_slug(part)
                if slug in non_csv or slug in _FK_REGISTRY_COLUMNS:
                    continue
                errors.append(f"{tid}: bare registry FK {part!r} not in column SSOT map")
                continue
            parsed = _parse_fk_token(part)
            if parsed is None:
                errors.append(f"{tid}: unparseable current_fk token {part!r}")
                continue
            reg_slug, col = parsed
            if reg_slug in non_csv:
                continue
            allowed = _FK_REGISTRY_COLUMNS.get(reg_slug)
            if allowed is None:
                errors.append(f"{tid}: unknown FK registry prefix {reg_slug!r} in {part!r}")
                continue
            if col not in allowed:
                errors.append(
                    f"{tid}: column {col!r} not in registry {reg_slug!r} "
                    f"(token {part!r})"
                )

    return errors


def self_test() -> int:
    assert _parse_fk_token("process_list.role_owner") == ("process_list", "role_owner")
    assert _parse_fk_token("new") is None
    assert "process_list" in _FK_REGISTRY_COLUMNS
    assert len(L3_TRANCHE1_FK_BINDINGS) >= 10
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    errors = run_checks()
    if errors:
        print(f"FAIL: {len(errors)} FK->verb coverage finding(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(
        f"PASS: FK->verb L3 tranche-1 - {len(L3_TRANCHE1_FK_BINDINGS)} bindings, "
        f"{len(_FK_REGISTRY_COLUMNS)} registry column maps"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
