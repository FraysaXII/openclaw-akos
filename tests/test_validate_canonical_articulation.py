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
    # Data-area sweep types (I95 2026-06-05): db/model/ERP/UI/analytics/catalogue/glossary gap
    assert {
        "data_contract", "data_product", "data_store", "data_model", "bi_consumer",
        "adapter", "data_catalog", "glossary_term", "application",
    }.issubset(types)
    assert len(types) == 42


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


# --- P2/C graph articulation (legacy edge -> unified verb-edge) ---------------

def test_every_legacy_edge_maps_to_a_verb():
    from akos.hlk_graph_articulation import assert_edge_coverage
    summary = assert_edge_coverage()
    assert summary["legacy_edge_count"] == 13
    # 13 forked legacy edges collapse to 6 unified verb-edges
    assert summary["unified_edge_count"] == 6


def test_parent_of_forks_unify_to_composed_of():
    from akos.hlk_graph_articulation import LEGACY_EDGE_TO_UNIFIED
    for forked in ("PARENT_OF", "PROGRAM_PARENT_OF", "TOPIC_PARENT_OF"):
        assert LEGACY_EDGE_TO_UNIFIED[forked] == "COMPOSED_OF"
    assert LEGACY_EDGE_TO_UNIFIED["OWNED_BY"] == "ASSIGNED_TO"


def test_five_competency_questions_defined():
    from akos.hlk_graph_articulation import COMPETENCY_QUESTIONS
    ids = {cq["id"] for cq in COMPETENCY_QUESTIONS}
    assert ids == {"CQ1", "CQ2", "CQ3", "CQ4", "CQ5"}
    for cq in COMPETENCY_QUESTIONS:
        assert cq["cypher"] and cq["question"] and cq["derivation"]


def test_dual_emit_doubles_edge_rows():
    from akos.hlk_graph_model import GraphEdge, dual_emit_edge_rows

    edges = [
        GraphEdge("REPORTS_TO", "Role", "A", "Role", "B"),
        GraphEdge("PARENT_OF", "Process", "p1", "Process", "p2"),
    ]
    rows = dual_emit_edge_rows(edges)
    assert len(rows) == 4
    assert rows[0]["etype"] == "REPORTS_TO"
    assert rows[2]["etype"] == "COMPOSED_OF"
    assert rows[3]["etype"] == "COMPOSED_OF"


# --- area-completeness v3 articulation mode (D-IH-95-D) -----------------------

def test_articulation_report_finance_fully_wired():
    from scripts.validate_canonical_articulation import articulation_report
    ok, report = articulation_report("Finance", ENTITY_CATALOG_PATH, RELATIONSHIP_REGISTRY_PATH)
    assert report["area"] == "Finance"
    assert report["owned_types"] >= 1
    assert not report["orphans"]
    assert ok


def test_articulation_report_data_flags_planned_orphans():
    from scripts.validate_canonical_articulation import articulation_report
    ok, report = articulation_report("Data", ENTITY_CATALOG_PATH, RELATIONSHIP_REGISTRY_PATH)
    # the planned, not-yet-active Data types should surface as orphans (advisory signal)
    assert "data_product" in report["orphans"]
    assert not ok  # has orphans


def test_articulation_gold_layer_matrix():
    """The gold-layer scorecard returns consistent enterprise rollup metrics (D-IH-95-E)."""
    from scripts.validate_canonical_articulation import articulation_matrix
    m = articulation_matrix(ENTITY_CATALOG_PATH, RELATIONSHIP_REGISTRY_PATH)
    assert m["entity_types"] == 42
    assert m["zachman_covered"] == 6
    assert 0 <= m["entity_coverage_pct"] <= 100
    assert m["active_triples"] <= m["total_triples"]
    assert m["dq_badge"] in {"GREEN", "AMBER", "RED"}
    assert m["per_area"], "per-area rows present"
