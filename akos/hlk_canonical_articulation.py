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

# I95 L3 tranche-1 (R2-05 / P5): high-signal CSV FK columns -> HCAM triple_id.
# Each binding must appear in the triple's ``current_fk`` column (semicolon-separated).
L3_TRANCHE1_FK_BINDINGS: tuple[tuple[str, str, str], ...] = (
    ("process_list", "role_owner", "HCAM-TRP-001"),
    ("process_list", "item_parent_1_id", "HCAM-TRP-005"),
    ("process_list", "item_parent_2_id", "HCAM-TRP-005"),
    ("process_list", "inherited_pattern_id", "HCAM-TRP-007"),
    ("process_list", "engagement_template_id", "HCAM-TRP-008"),
    ("process_list", "persona_id", "HCAM-TRP-009"),
    ("baseline_organisation", "reports_to", "HCAM-TRP-002"),
    ("baseline_organisation", "area", "HCAM-TRP-004"),
    ("baseline_organisation", "sub_area", "HCAM-TRP-003"),
    ("baseline_organisation", "components_used", "HCAM-TRP-027"),
)

# I95 L3 tranche-2 (R2-05 / P5b): capability + decision + ops register FK columns.
L3_TRANCHE2_FK_BINDINGS: tuple[tuple[str, str, str], ...] = (
    ("capability_registry", "role_owner", "HCAM-TRP-039"),
    ("capability_registry", "skill_ids", "HCAM-TRP-040"),
    ("capability_registry", "substrate_id", "HCAM-TRP-041"),
    ("capability_registry", "originating_process_ids", "HCAM-TRP-006"),
    ("decision_register", "linked", "HCAM-TRP-016"),
    ("decision_register", "linked", "HCAM-TRP-017"),
    ("decision_register", "linked_initiative_ids", "HCAM-TRP-018"),
    ("ops_register", "linked", "HCAM-TRP-020"),
)

# I95 L3 tranche-3 (R2-05 / P5c): workstream layer composition via process_list.
L3_TRANCHE3_FK_BINDINGS: tuple[tuple[str, str, str], ...] = (
    ("process_list", "item_granularity", "HCAM-TRP-031"),
    ("process_list", "item_parent_1_id", "HCAM-TRP-031"),
    ("process_list", "item_granularity", "HCAM-TRP-032"),
    ("process_list", "item_parent_1_id", "HCAM-TRP-032"),
)

# I95 L3 tranche-4A (R2-05 / P5d): data-plane — AIC matrix, data contracts, topic tree.
L3_TRANCHE4A_FK_BINDINGS: tuple[tuple[str, str, str], ...] = (
    ("aic_capability_implementation_matrix", "capability_id", "HCAM-TRP-038"),
    ("aic_capability_implementation_matrix", "aic_id", "HCAM-TRP-038"),
    ("data_contract_registry", "producer_process_id", "HCAM-TRP-045"),
    ("data_contract_registry", "consumer_area_ids", "HCAM-TRP-046"),
    ("data_contract_registry", "data_surface", "HCAM-TRP-047"),
    ("topic_registry", "parent", "HCAM-TRP-021"),
)

# I95 L3 tranche-4B (R2-05 / P5d): engagement cluster — TRP-008 deduped (tranche-1).
L3_TRANCHE4B_FK_BINDINGS: tuple[tuple[str, str, str], ...] = (
    ("engagement_registry", "counterparty_org_id", "HCAM-TRP-012"),
    ("use_case_archive", "capability_id", "HCAM-TRP-029"),
    ("use_case_archive", "engagement_id", "HCAM-TRP-042"),
    ("initiative_registry", "program_anchors", "HCAM-TRP-015"),
    ("goi_poi_register", "process_item_id", "HCAM-TRP-043"),
    ("goi_poi_register", "program_id", "HCAM-TRP-044"),
)

# I95 L3 tranche-5 (R2-05 / F-11): 10 active triples without L3 bindings post tranche-4.
L3_TRANCHE5_FK_BINDINGS: tuple[tuple[str, str, str], ...] = (
    ("policy_register", "", "HCAM-TRP-019"),
    ("intelligence_matrix", "", "HCAM-TRP-022"),
    ("channel_touchpoint_registry", "", "HCAM-TRP-023"),
    ("frontmatter", "inherited_pattern_id", "HCAM-TRP-024"),
    ("persona_scenario_registry", "persona_id", "HCAM-TRP-025"),
    ("metrics_registry", "source_contract_id", "HCAM-TRP-026"),
    ("skill_registry", "owner_role", "HCAM-TRP-028"),
    ("bi_consumer_registry", "component_id", "HCAM-TRP-048"),
    ("bi_consumer_registry", "data_surfaces", "HCAM-TRP-049"),
    ("area_bi_profile", "primary_consumer_ids", "HCAM-TRP-050"),
)

L3_FK_BINDINGS: tuple[tuple[str, str, str], ...] = (
    *L3_TRANCHE1_FK_BINDINGS,
    *L3_TRANCHE2_FK_BINDINGS,
    *L3_TRANCHE3_FK_BINDINGS,
    *L3_TRANCHE4A_FK_BINDINGS,
    *L3_TRANCHE4B_FK_BINDINGS,
    *L3_TRANCHE5_FK_BINDINGS,
)

# Non-CSV FK surfaces (markdown frontmatter, semantic layer SQL, etc.) — advisory only.
FK_NON_CSV_REGISTRY_PREFIXES: frozenset[str] = frozenset({
    "frontmatter",
    "semantic_layer",
    "semantic_layer_binding",
    "engagement_model",
    "policy_register",
    "intelligence_matrix",
    "openmetadata_projection",
    "openmetadata_glossary",
    "dama_conceptual_logical_physical",
    "integration_plane_rule",
    "data_fam_umbrella",
    "erp_reads_warehouse",
    "component_service_matrix",
    "capability_map",
    "area_model",
    "brand_architecture",
    "channel_touchpoint_registry",
    "rpa_adapter_registry",
})


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
