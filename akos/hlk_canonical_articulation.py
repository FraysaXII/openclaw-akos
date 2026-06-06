"""Pydantic SSOT for the Holistika Canonical Articulation Model (HCAM).

I95 P1 (D-IH-95-B). HCAM is the **entity-and-relationship tier** of the Holistika
Semantic Layer (``SEMANTIC_LAYER.md``) — the enterprise ontology that says, for every
canonical artifact type, *what it is* (entity catalog) and *how it links* (closed
ArchiMate verb set + valid-triple registry). It is the missing semantic layer of the
existing three-tier Data Architecture (T1 git CSV SSOT → T2 Supabase → T3 Neo4j).

Two registries (both Data-Architecture canonicals, sibling to ``METRICS_REGISTRY.csv``):

* ``ENTITY_CATALOG.csv`` — one row per canonical artifact type, mapped to one ArchiMate
  aspect + one Zachman cell + its SSOT + its Neo4j label + owning area.
* ``CANONICAL_RELATIONSHIP_REGISTRY.csv`` — the valid ``(source_type, verb, target_type)``
  triples (ArchiMate's relationship matrix as a queryable CSV = an ISO/IEC 39075:2024 GQL
  *graph type*). The ``neo4j_edge_type`` column pre-wires the I91 graph unify (C): forked
  edges (PARENT_OF / PROGRAM_PARENT_OF / TOPIC_PARENT_OF) collapse to one COMPOSITION edge.

Ownership: Data-federated (D-IH-95-A/B). Data Architect authors; Data Governance Office owns
the relationship registry; Data Steward operates; CDO chairs the Semantic Council.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from akos.io import REPO_ROOT

# --- closed sets -------------------------------------------------------------

# The 42 canonical artifact types: 31 ratified + Workstream + Brand (operator 2026-06-05) +
# 9 Data-area types (I95 data-area sweep 2026-06-05: the db/model/ERP/UI/analytics/KPI/
# glossary/catalogue gap the operator flagged).
VALID_ENTITY_TYPES: frozenset[str] = frozenset({
    # Who — active structure
    "role", "aic", "persona", "entity", "channel", "sourcing",
    # How — behavior
    "process", "pattern", "engagement", "capability", "skill", "use_case",
    "persona_scenario",
    # What — passive structure
    "topic", "component", "canonical", "metric", "artifact_class", "output_type",
    "substrate", "source_fact", "touchpoint_kit_cell", "brand",
    # Why — motivation
    "decision", "policy", "goal_poi", "audience",
    # When — implementation / time
    "initiative", "program", "workstream", "ops_action", "calendar_cadence",
    # Where — bounded context
    "area",
    # Data area (I95 data-area sweep): data products + contracts + stores + models +
    # BI/analytics consumers + integration adapters + catalog + glossary + applications/ERP.
    "data_contract", "data_product", "data_store", "data_model", "bi_consumer",
    "adapter", "data_catalog", "glossary_term", "application",
})

# The closed ArchiMate relationship verb set (10) + association (last-resort catch-all).
VALID_VERBS: frozenset[str] = frozenset({
    "composition",     # strong whole-part (part dies with whole)
    "aggregation",     # weak whole-part (part lives independently)
    "assignment",      # performs / owns / accountable
    "realization",     # concrete realizes abstract
    "serving",         # provides function to a consumer
    "access",          # reads/writes a passive object
    "influence",       # affects a motivation element
    "triggering",      # temporal/causal sequence
    "flow",            # transfer between elements
    "specialization",  # "is a kind of"
    "association",     # last-resort; flagged for Semantic Council review
})

VALID_ARCHIMATE_ASPECTS: frozenset[str] = frozenset({
    "active_structure", "behavior", "passive_structure", "motivation",
    "strategy", "implementation", "technology", "time", "composite",
})

VALID_ZACHMAN_CELLS: frozenset[str] = frozenset({
    "who", "how", "what", "why", "when", "where",
})

VALID_CARDINALITIES: frozenset[str] = frozenset({"1:1", "1:N", "N:1", "N:N"})

VALID_TRIPLE_STATUS: frozenset[str] = frozenset({"active", "planned", "deprecated"})

# Unified Neo4j edge types (UPPER_SNAKE of the verb) — the I91 (C) migration target.
# Forked edges collapse here; the node labels disambiguate context.
VERB_TO_NEO4J_EDGE: dict[str, str] = {
    "composition": "COMPOSED_OF",
    "aggregation": "AGGREGATES",
    "assignment": "ASSIGNED_TO",
    "realization": "REALIZES",
    "serving": "SERVES",
    "access": "ACCESSES",
    "influence": "INFLUENCES",
    "triggering": "TRIGGERS",
    "flow": "FLOWS_TO",
    "specialization": "SPECIALIZES",
    "association": "ASSOCIATED_WITH",
}

ENTITY_CATALOG_FIELDNAMES: tuple[str, ...] = (
    "entity_type", "entity_label", "ssot_path", "archimate_aspect", "zachman_cell",
    "neo4j_label", "owning_area", "status", "notes",
)

RELATIONSHIP_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "triple_id", "source_type", "verb", "target_type", "cardinality",
    "current_fk", "neo4j_edge_type", "replaces_edge", "status", "notes",
)

ENTITY_CATALOG_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Data"
    / "Architecture" / "canonicals" / "dimensions" / "ENTITY_CATALOG.csv"
)
RELATIONSHIP_REGISTRY_PATH = (
    REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Data"
    / "Architecture" / "canonicals" / "dimensions" / "CANONICAL_RELATIONSHIP_REGISTRY.csv"
)


class EntityCatalogRow(BaseModel):
    """One canonical artifact type in the HCAM entity catalog."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    entity_type: str = Field(min_length=2, max_length=40)
    entity_label: str = Field(min_length=1, max_length=80)
    ssot_path: str = Field(min_length=1, max_length=300)
    archimate_aspect: Literal[
        "active_structure", "behavior", "passive_structure", "motivation",
        "strategy", "implementation", "technology", "time", "composite",
    ]
    zachman_cell: Literal["who", "how", "what", "why", "when", "where"]
    neo4j_label: str = Field(default="", max_length=40)
    owning_area: str = Field(min_length=1, max_length=60)
    status: Literal["active", "planned", "deprecated"] = "active"
    notes: str = Field(default="", max_length=400)

    @field_validator("entity_type")
    @classmethod
    def entity_type_known(cls, value: str) -> str:
        if value not in VALID_ENTITY_TYPES:
            raise ValueError(f"unknown entity_type: {value!r}")
        return value


class RelationshipTripleRow(BaseModel):
    """One valid ``(source_type, verb, target_type)`` articulation triple."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    triple_id: str = Field(min_length=1, max_length=40)
    source_type: str = Field(min_length=2, max_length=40)
    verb: Literal[
        "composition", "aggregation", "assignment", "realization", "serving",
        "access", "influence", "triggering", "flow", "specialization", "association",
    ]
    target_type: str = Field(min_length=2, max_length=40)
    cardinality: Literal["1:1", "1:N", "N:1", "N:N"]
    current_fk: str = Field(default="", max_length=120)
    neo4j_edge_type: str = Field(min_length=1, max_length=40)
    replaces_edge: str = Field(default="", max_length=120)
    status: Literal["active", "planned", "deprecated"] = "active"
    notes: str = Field(default="", max_length=400)

    @field_validator("triple_id")
    @classmethod
    def triple_id_shape(cls, value: str) -> str:
        if not value.startswith("HCAM-TRP-"):
            raise ValueError("triple_id must start with HCAM-TRP-")
        return value

    @field_validator("source_type", "target_type")
    @classmethod
    def endpoint_known(cls, value: str) -> str:
        if value not in VALID_ENTITY_TYPES:
            raise ValueError(f"unknown entity endpoint: {value!r}")
        return value

    @field_validator("neo4j_edge_type")
    @classmethod
    def edge_matches_verb(cls, value: str) -> str:
        if value not in VERB_TO_NEO4J_EDGE.values():
            raise ValueError(f"neo4j_edge_type {value!r} not in unified edge set")
        return value


def fixture_entity_row() -> EntityCatalogRow:
    """Return one valid entity-catalog row for validator self-tests."""

    return EntityCatalogRow(
        entity_type="process",
        entity_label="Process",
        ssot_path="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv",
        archimate_aspect="behavior",
        zachman_cell="how",
        neo4j_label="Process",
        owning_area="per-area",
        status="active",
        notes="item_granularity project/process/activity/task = intra-type layers",
    )


def fixture_triple_row() -> RelationshipTripleRow:
    """Return one valid relationship triple for validator self-tests."""

    return RelationshipTripleRow(
        triple_id="HCAM-TRP-001",
        source_type="role",
        verb="assignment",
        target_type="process",
        cardinality="N:N",
        current_fk="process_list.role_owner",
        neo4j_edge_type="ASSIGNED_TO",
        replaces_edge="OWNED_BY",
        status="active",
        notes="role performs/owns process",
    )
