"""HCAM ↔ Neo4j graph articulation (I95 P2/C, D-IH-95-C).

Bridges the legacy graph projection (``akos/hlk_graph_model.py`` — 13 ad-hoc edge types,
grown per-initiative) to the HCAM verb taxonomy (``akos/hlk_canonical_articulation.py``).

This module is **additive and non-destructive**: it does NOT mutate the emitted edges (the
live projection + parity assertions + ``sync_hlk_neo4j.py`` stay intact while I91 keeps Neo4j
preflight-blocked). It provides:

  * ``LEGACY_EDGE_TO_VERB`` — every legacy edge → its ArchiMate verb (the de-fork map).
  * ``unified_edge(legacy)`` — the unified Neo4j edge type for the cutover.
  * ``COMPETENCY_QUESTIONS`` — the 5 acceptance queries (unified-edge Cypher sketches).
  * ``assert_edge_coverage()`` — proves every legacy ``EdgeType`` maps to a valid verb.

The actual Neo4j edge rename is a **gated cutover** (Semantic Council + I91 unblock); this
module is the migration map + derivation specs that make the cutover mechanical and safe.
The headline result: the 13 forked legacy edges collapse to 6 unified verb-edges — the three
``*_PARENT_OF`` forks all become one ``COMPOSED_OF``.
"""
from __future__ import annotations

from typing import get_args

from akos.hlk_canonical_articulation import VERB_TO_NEO4J_EDGE
from akos.hlk_graph_model import EdgeType

# Each legacy edge type → its ArchiMate verb. Derived from CANONICAL_RELATIONSHIP_REGISTRY's
# replaces_edge column + the verb taxonomy. This is the de-fork: REPORTS_TO / PARENT_OF /
# PROGRAM_PARENT_OF / UNDER_PROGRAM / TOPIC_PARENT_OF all reduce to composition.
LEGACY_EDGE_TO_VERB: dict[str, str] = {
    "REPORTS_TO": "composition",        # org hierarchy (role whole-part)
    "PARENT_OF": "composition",          # process layers (project>process>activity>task)
    "PROGRAM_PARENT_OF": "composition",  # program tree  (FORK of PARENT_OF)
    "UNDER_PROGRAM": "composition",      # thing under a program = part of it
    "TOPIC_PARENT_OF": "composition",    # topic tree    (FORK of PARENT_OF)
    "OWNED_BY": "assignment",            # process owned/performed by role
    "PROGRAM_SUBSUMES": "aggregation",   # program aggregates initiatives
    "TOPIC_SUBSUMES": "aggregation",     # topic aggregates sub-topics
    "UNDER_TOPIC": "aggregation",        # cross-axis node aggregated by a topic
    "CONSUMES": "flow",                  # consumer reads producer (data transfer)
    "PRODUCES_FOR": "flow",              # producer transfers to consumer
    "DEPENDS_ON": "serving",             # depended-upon serves the dependent
    "RELATED_TO": "association",         # generic (last-resort; flag for Council review)
}


def unified_edge(legacy_edge_type: str) -> str:
    """Return the unified Neo4j edge type for a legacy edge (the cutover target)."""
    verb = LEGACY_EDGE_TO_VERB[legacy_edge_type]
    return VERB_TO_NEO4J_EDGE[verb]


# Map a legacy edge straight to its unified Neo4j edge label (convenience).
LEGACY_EDGE_TO_UNIFIED: dict[str, str] = {
    legacy: VERB_TO_NEO4J_EDGE[verb] for legacy, verb in LEGACY_EDGE_TO_VERB.items()
}


# The 5 competency questions (HCAM acceptance test). Cypher sketches use the UNIFIED edges,
# so they are valid against the post-cutover graph; ArchiMate derivation (weakest-link)
# underpins CQ1–CQ3. These are specs, not executed here (Neo4j preflight-blocked per I91).
COMPETENCY_QUESTIONS: list[dict[str, str]] = [
    {
        "id": "CQ1",
        "question": "Which processes is role R assigned to, and which capabilities do those realize?",
        "cypher": "MATCH (r:Role {id:$role})-[:ASSIGNED_TO]->(p:Process)-[:REALIZES]->(c:Capability) RETURN p, c",
        "derivation": "assignment ∘ realization (role contributes-to capability)",
    },
    {
        "id": "CQ2",
        "question": "What serves engagement E end-to-end, back to the roles that perform it?",
        "cypher": "MATCH (e:Engagement {id:$eng})<-[:SERVES]-(p:Process)<-[:ASSIGNED_TO]-(r:Role) RETURN p, r",
        "derivation": "serving + dynamic transfer over assignment",
    },
    {
        "id": "CQ3",
        "question": "If capability C is retired, which areas/roles/engagements are impacted?",
        "cypher": "MATCH (c:Capability {id:$cap})<-[:REALIZES]-(p:Process)<-[:ASSIGNED_TO]-(r:Role) OPTIONAL MATCH (p)-[:SERVES]->(e:Engagement) RETURN r, e",
        "derivation": "realization impact analysis (reverse)",
    },
    {
        "id": "CQ4",
        "question": "Show process P's full layer path (project -> ... -> task).",
        "cypher": "MATCH path=(root:Process {id:$proc})-[:COMPOSED_OF*]->(leaf:Process) RETURN path",
        "derivation": "composition transitive closure",
    },
    {
        "id": "CQ5",
        "question": "Is every canonical in area A wired (no orphans; valid triples only)?",
        "cypher": "MATCH (n) WHERE n.area=$area AND NOT (n)--() RETURN n AS orphan",
        "derivation": "articulation-completeness check (area-completeness v3)",
    },
]


def assert_edge_coverage() -> dict[str, object]:
    """Prove every legacy EdgeType maps to a valid verb + unified edge.

    Raises AssertionError on any uncovered legacy edge or invalid mapping.
    Returns a summary dict (legacy count, unified set, collapse ratio).
    """
    legacy_edges = set(get_args(EdgeType))
    mapped = set(LEGACY_EDGE_TO_VERB)
    missing = legacy_edges - mapped
    assert not missing, f"legacy edges with no verb mapping: {sorted(missing)}"
    extra = mapped - legacy_edges
    assert not extra, f"mapping references unknown edges: {sorted(extra)}"
    for legacy, verb in LEGACY_EDGE_TO_VERB.items():
        assert verb in VERB_TO_NEO4J_EDGE, f"{legacy} -> unknown verb {verb!r}"
    unified = set(LEGACY_EDGE_TO_UNIFIED.values())
    return {
        "legacy_edge_count": len(legacy_edges),
        "unified_edge_count": len(unified),
        "unified_edges": sorted(unified),
        "composition_collapse": sorted(
            e for e, v in LEGACY_EDGE_TO_VERB.items() if v == "composition"
        ),
    }
