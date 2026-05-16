"""Field contract for SUBSTRATE_REGISTRY.csv (Initiative 84 P3).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``
per `D-IH-84-F` (CSV registry home; sibling of TOPIC_REGISTRY + PROGRAM_REGISTRY +
GOI_POI_REGISTER + ENGAGEMENT_TEMPLATE_REGISTRY + PEOPLE_DESIGN_PATTERN_REGISTRY).

Mirrored to ``compliance.substrate_registry_mirror`` on Supabase per
the pattern established by Initiative 32 P2 (skill_registry_mirror), Initiative
73 P1 (engagement_model_registry_mirror), and Initiative 79 P2
(people_design_pattern_registry_mirror). DDL lives at
``supabase/migrations/<timestamp>_i84_substrate_registry_mirror.sql`` (forthcoming
at master-roadmap §3 P2 (cascade); P3a authoring; P3c cascade lands the DDL).

SUBSTRATE_REGISTRY = the canonical state-of-record for which technical substrates
AKOS / MADEIRA / KiRBe / future-Holistika-products commit to. Each row carries
attributes used by `D-IH-84-B` (AKOS substrate-baseline), `D-IH-84-C` (AIC pattern
framing), `D-IH-84-D` (MADEIRA productization shape), `D-IH-84-E` (KiRBe framework
narrowing) ratifications + supports the quarterly Research-area substrate-audit
cadence per [`SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`](../docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md)
(forthcoming at master-roadmap §3 P6).

Decision lineage:
- D-IH-84-A (mega scope; charter)
- D-IH-84-B (AKOS substrate-baseline choice; uses these rows as input)
- D-IH-84-C (AIC framing; per-row aic_pattern_role attribute)
- D-IH-84-D (MADEIRA productization shape; per-row madeira_productization_role attribute)
- D-IH-84-E (KiRBe framework narrowing; per-row akos_integration_state attribute)
- D-IH-84-F (this column shape — 18 columns + 8 enum frozensets)
- D-IH-84-G (paired Research-area SUBSTRATE_LANDSCAPE_DOCTRINE.md)

See ``SUBSTRATE_LANDSCAPE_DOCTRINE.md`` (sibling Research-area canonical) for the
human-readable companion; CSV anchor is the join key. See
``AGENTIC_FRAMEWORK_LANDSCAPE.md`` (Tech-Lab canonical) for the operational
how-side companion.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SUBSTRATE_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "substrate_id",
    "name",
    "vendor",
    "runtime_shape",
    "persistence_model",
    "tool_protocol",
    "multi_tenant_ready",
    "license_class",
    "status",
    "cost_class",
    "pricing_unit",
    "founder_principle_alignment",
    "akos_integration_state",
    "madeira_productization_role",
    "aic_pattern_role",
    "last_audit_date",
    "audit_source_url",
    "notes",
)


VALID_RUNTIME_SHAPES: frozenset[str] = frozenset({
    "agent-sdk-typescript",
    "agent-sdk-python",
    "agent-sdk-rest",
    "framework-library-python",
    "framework-library-typescript",
    "hosted-agent-platform",
    "inference-provider",
    "orchestration-engine",
})


VALID_PERSISTENCE_MODELS: frozenset[str] = frozenset({
    "ephemeral",
    "session-scoped",
    "persistent",
    "cloud-managed",
})


VALID_TOOL_PROTOCOLS: frozenset[str] = frozenset({
    "mcp",
    "openai-functions",
    "anthropic-tools",
    "cursor-native",
    "langchain-native",
    "native-only",
})


VALID_LICENSE_CLASSES: frozenset[str] = frozenset({
    "proprietary-saas",
    "open-weights-model",
    "open-source-mit",
    "open-source-apache",
    "open-source-other",
    "commercial-license",
})


VALID_STATUSES: frozenset[str] = frozenset({
    "active",
    "candidate",
    "experimental",
    "deprecated",
    "forecasted",
})


VALID_COST_CLASSES: frozenset[str] = frozenset({
    "token-billed",
    "seat-billed",
    "gpu-hour-billed",
    "bring-your-own-key",
    "free-tier-only",
    "hybrid",
})


VALID_AKOS_INTEGRATION_STATES: frozenset[str] = frozenset({
    "in-production",
    "pilot",
    "forecasted",
    "blocked",
    "rejected",
    "candidate",
})


VALID_MADEIRA_PRODUCTIZATION_ROLES: frozenset[str] = frozenset({
    "backend-only",
    "library-import",
    "agent-runtime",
    "not-applicable",
    "forecasted",
})


VALID_AIC_PATTERN_ROLES: frozenset[str] = frozenset({
    "supervisor",
    "sub-agent",
    "peer",
    "dispatcher",
    "single-agent-rich-tools",
    "not-applicable",
})


class SubstrateRegistryRow(BaseModel):
    """Pydantic frozen BaseModel for one row of SUBSTRATE_REGISTRY.csv.

    Per ``CONTRIBUTING.md`` "Python Code Standards" and
    ``akos-holistika-operations.mdc`` "New git-canonical compliance registers":
    frozen BaseModel + Literal enums for governed columns + length bounds + slug
    regex on substrate_id.

    The 18 columns are SSOT per D-IH-84-F. Eight enum columns are constrained by
    the frozensets above and mirrored as Literal annotations here for Pydantic
    validation.
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    substrate_id: str = Field(
        ...,
        pattern=r"^SUBS-[A-Z0-9-]+$",
        min_length=8,
        max_length=96,
        description="Stable identifier; matches ^SUBS-[A-Z0-9-]+$ (e.g. SUBS-HOLISTIKA-OPENCLAW)",
    )
    name: str = Field(..., min_length=1, max_length=120)
    vendor: str = Field(..., min_length=1, max_length=120)
    runtime_shape: Literal[
        "agent-sdk-typescript",
        "agent-sdk-python",
        "agent-sdk-rest",
        "framework-library-python",
        "framework-library-typescript",
        "hosted-agent-platform",
        "inference-provider",
        "orchestration-engine",
    ]
    persistence_model: Literal[
        "ephemeral",
        "session-scoped",
        "persistent",
        "cloud-managed",
    ]
    tool_protocol: Literal[
        "mcp",
        "openai-functions",
        "anthropic-tools",
        "cursor-native",
        "langchain-native",
        "native-only",
    ]
    multi_tenant_ready: Literal["true", "false", "unknown"]
    license_class: Literal[
        "proprietary-saas",
        "open-weights-model",
        "open-source-mit",
        "open-source-apache",
        "open-source-other",
        "commercial-license",
    ]
    status: Literal[
        "active",
        "candidate",
        "experimental",
        "deprecated",
        "forecasted",
    ]
    cost_class: Literal[
        "token-billed",
        "seat-billed",
        "gpu-hour-billed",
        "bring-your-own-key",
        "free-tier-only",
        "hybrid",
    ]
    pricing_unit: str = Field("", max_length=240, description="Free text; may be empty")
    founder_principle_alignment: str = Field(
        "",
        max_length=80,
        description="FK to FOUNDER_METHODOLOGY_VERSIONING.md principles; semicolon list or single value or empty",
    )
    akos_integration_state: Literal[
        "in-production",
        "pilot",
        "forecasted",
        "blocked",
        "rejected",
        "candidate",
    ]
    madeira_productization_role: Literal[
        "backend-only",
        "library-import",
        "agent-runtime",
        "not-applicable",
        "forecasted",
    ]
    aic_pattern_role: Literal[
        "supervisor",
        "sub-agent",
        "peer",
        "dispatcher",
        "single-agent-rich-tools",
        "not-applicable",
    ]
    last_audit_date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="ISO date YYYY-MM-DD",
    )
    audit_source_url: str = Field("", max_length=480)
    notes: str = Field("", max_length=2048)


CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/SUBSTRATE_REGISTRY.csv"
)
