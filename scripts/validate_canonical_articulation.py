"""Validate the HCAM entity catalog + canonical relationship registry (I95 P1, D-IH-95-B).

Checks:
  1. Every ENTITY_CATALOG row conforms to ``EntityCatalogRow`` (Pydantic).
  2. Every CANONICAL_RELATIONSHIP_REGISTRY row conforms to ``RelationshipTripleRow``.
  3. Referential integrity: every triple's source_type + target_type exists in the catalog.
  4. neo4j_edge_type is the unified edge for its verb (VERB_TO_NEO4J_EDGE) — pre-wires I91 (C).
  5. triple_id + entity_type uniqueness.
  6. Catalog covers all 6 Zachman cells (coverage lattice) — advisory.

Usage:
  py scripts/validate_canonical_articulation.py
  py scripts/validate_canonical_articulation.py --self-test
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_canonical_articulation import (  # noqa: E402
    ENTITY_CATALOG_PATH,
    RELATIONSHIP_REGISTRY_PATH,
    VALID_ZACHMAN_CELLS,
    VERB_TO_NEO4J_EDGE,
    EntityCatalogRow,
    RelationshipTripleRow,
    fixture_entity_row,
    fixture_triple_row,
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def validate(entity_path: Path, registry_path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []

    entity_rows = _read_csv(entity_path)
    registry_rows = _read_csv(registry_path)

    catalog_types: set[str] = set()
    seen_types: set[str] = set()
    zachman_seen: set[str] = set()
    for i, raw in enumerate(entity_rows, start=2):
        try:
            row = EntityCatalogRow(**raw)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"ENTITY_CATALOG L{i}: {exc}")
            continue
        if row.entity_type in seen_types:
            errors.append(f"ENTITY_CATALOG L{i}: duplicate entity_type {row.entity_type!r}")
        seen_types.add(row.entity_type)
        catalog_types.add(row.entity_type)
        zachman_seen.add(row.zachman_cell)

    seen_triple_ids: set[str] = set()
    for i, raw in enumerate(registry_rows, start=2):
        try:
            row = RelationshipTripleRow(**raw)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"RELATIONSHIP_REGISTRY L{i}: {exc}")
            continue
        if row.triple_id in seen_triple_ids:
            errors.append(f"RELATIONSHIP_REGISTRY L{i}: duplicate triple_id {row.triple_id!r}")
        seen_triple_ids.add(row.triple_id)
        if row.source_type not in catalog_types:
            errors.append(
                f"RELATIONSHIP_REGISTRY L{i}: source_type {row.source_type!r} not in ENTITY_CATALOG"
            )
        if row.target_type not in catalog_types:
            errors.append(
                f"RELATIONSHIP_REGISTRY L{i}: target_type {row.target_type!r} not in ENTITY_CATALOG"
            )
        if VERB_TO_NEO4J_EDGE.get(row.verb) != row.neo4j_edge_type:
            errors.append(
                f"RELATIONSHIP_REGISTRY L{i}: neo4j_edge_type {row.neo4j_edge_type!r} "
                f"!= unified edge {VERB_TO_NEO4J_EDGE.get(row.verb)!r} for verb {row.verb!r}"
            )

    missing_cells = VALID_ZACHMAN_CELLS - zachman_seen
    advisory = ""
    if missing_cells:
        advisory = f" (advisory: Zachman cells not yet covered: {sorted(missing_cells)})"

    ok = not errors
    if ok:
        print(
            f"PASS: HCAM articulation ({len(catalog_types)} entity types; "
            f"{len(seen_triple_ids)} valid triples; Zachman cells covered="
            f"{len(zachman_seen)}/6){advisory}"
        )
    else:
        print(f"FAIL: HCAM articulation ({len(errors)} error(s))")
        for e in errors:
            print(f"  - {e}")
    return ok, errors


def self_test() -> bool:
    """Validate fixtures + the round-trip of the unified edge map."""
    try:
        e = fixture_entity_row()
        t = fixture_triple_row()
    except Exception as exc:  # noqa: BLE001
        print(f"validate_canonical_articulation: self-test FAIL ({exc})")
        return False
    assert VERB_TO_NEO4J_EDGE[t.verb] == t.neo4j_edge_type, "fixture edge mismatch"
    assert e.entity_type == "process", "fixture entity unexpected"
    print("validate_canonical_articulation: self-test PASS")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate HCAM entity catalog + relationship registry")
    ap.add_argument("--self-test", action="store_true", help="run fixture self-test only")
    ap.add_argument("--entity-catalog", default=str(ENTITY_CATALOG_PATH))
    ap.add_argument("--relationship-registry", default=str(RELATIONSHIP_REGISTRY_PATH))
    args = ap.parse_args()

    if args.self_test:
        return 0 if self_test() else 1

    ok, _ = validate(Path(args.entity_catalog), Path(args.relationship_registry))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
