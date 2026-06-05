"""Tests for the HCAM entity catalog + canonical relationship registry (I95 P1)."""
from __future__ import annotations

import csv
from pathlib import Path

from akos.hlk_canonical_articulation import (
    ENTITY_CATALOG_PATH,
    RELATIONSHIP_REGISTRY_PATH,
    VALID_ENTITY_TYPES,
    VERB_TO_NEO4J_EDGE,
    EntityCatalogRow,
    RelationshipTripleRow,
    fixture_entity_row,
    fixture_triple_row,
)
from scripts.validate_canonical_articulation import validate


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def test_fixtures_valid():
    assert fixture_entity_row().entity_type == "process"
    assert fixture_triple_row().verb == "assignment"


def test_catalog_all_rows_valid_and_known_types():
    types = set()
    for raw in _rows(ENTITY_CATALOG_PATH):
        row = EntityCatalogRow(**raw)
        assert row.entity_type in VALID_ENTITY_TYPES
        types.add(row.entity_type)
    # operator-added types must be present
    assert {"workstream", "brand"}.issubset(types)
    assert len(types) == 33


def test_registry_rows_valid_and_referentially_integral():
    catalog_types = {EntityCatalogRow(**r).entity_type for r in _rows(ENTITY_CATALOG_PATH)}
    seen = set()
    for raw in _rows(RELATIONSHIP_REGISTRY_PATH):
        row = RelationshipTripleRow(**raw)
        assert row.source_type in catalog_types
        assert row.target_type in catalog_types
        assert VERB_TO_NEO4J_EDGE[row.verb] == row.neo4j_edge_type
        seen.add(row.triple_id)
    assert len(seen) == len(_rows(RELATIONSHIP_REGISTRY_PATH))  # unique ids


def test_operator_added_triples_present():
    ids = {RelationshipTripleRow(**r).triple_id for r in _rows(RELATIONSHIP_REGISTRY_PATH)}
    # Skill->Role, Use-case->Capability, AIC->Process (operator 2026-06-05)
    assert {"HCAM-TRP-028", "HCAM-TRP-029", "HCAM-TRP-030"}.issubset(ids)


def test_validate_end_to_end_passes():
    ok, errors = validate(ENTITY_CATALOG_PATH, RELATIONSHIP_REGISTRY_PATH)
    assert ok, f"validation errors: {errors}"


def test_forked_parent_edges_collapse_to_composition():
    """The 3 forked *_PARENT_OF edges all map to one COMPOSED_OF via composition triples."""
    replaced = set()
    for raw in _rows(RELATIONSHIP_REGISTRY_PATH):
        row = RelationshipTripleRow(**raw)
        if row.replaces_edge:
            replaced.add(row.replaces_edge)
        if row.replaces_edge in {"PARENT_OF", "TOPIC_PARENT_OF"}:
            assert row.verb == "composition"
            assert row.neo4j_edge_type == "COMPOSED_OF"
    assert {"PARENT_OF", "TOPIC_PARENT_OF", "OWNED_BY"}.issubset(replaced)
