"""Field contract for DATA_CONTRACT_REGISTRY.csv (Initiative 93 P2).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/dimensions/``
per DATA_CONTRACT_STANDARD.md + DATA_GOVERNANCE_POLICY.md.

Each row declares producer→consumer obligations for one data surface
(canonical CSV, Supabase mirror, FDW projection, or graph) aligned to
ODCS v3.1 vocabulary (warn-first; full YAML export forward-chartered).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DATA_CONTRACT_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "contract_id",
    "producer_process_id",
    "producer_area",
    "consumer_area_ids",
    "data_surface",
    "schema_ref",
    "semantics_ref",
    "sla_freshness",
    "sla_availability",
    "quality_rules",
    "classification",
    "retention_policy_ref",
    "version",
    "status",
    "owner_role",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
    "notes",
)

VALID_DATA_SURFACES: frozenset[str] = frozenset({
    "canonical_csv",
    "mirror_table",
    "fdw_projection",
    "graph",
})

VALID_CONTRACT_STATUSES: frozenset[str] = frozenset({
    "active",
    "draft",
    "deprecated",
})

VALID_DATAOPS_QUALITY_CODES: frozenset[str] = frozenset({
    f"DATA-{idx:02d}" for idx in range(1, 8)
})

VALID_CONSUMER_AREAS: frozenset[str] = frozenset({
    "Data",
    "Tech",
    "Finance",
    "Marketing",
    "Operations",
    "People",
    "Research",
    "Legal",
    "Compliance",
    "Admin",
})

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "dimensions/DATA_CONTRACT_REGISTRY.csv"
)


class DataContractRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    contract_id: str = Field(pattern=r"^DC-HOL-[A-Z0-9-]+$")
    producer_process_id: str = Field(min_length=1, max_length=120)
    producer_area: str = Field(min_length=1, max_length=32)
    consumer_area_ids: str = Field(min_length=1, max_length=120)
    data_surface: Literal["canonical_csv", "mirror_table", "fdw_projection", "graph"]
    schema_ref: str = Field(min_length=1, max_length=512)
    semantics_ref: str = Field(default="", max_length=512)
    sla_freshness: str = Field(default="", max_length=120)
    sla_availability: str = Field(default="", max_length=120)
    quality_rules: str = Field(min_length=1, max_length=512)
    classification: str = Field(default="internal", max_length=64)
    retention_policy_ref: str = Field(default="", max_length=512)
    version: str = Field(min_length=1, max_length=16)
    status: Literal["active", "draft", "deprecated"]
    owner_role: str = Field(min_length=1, max_length=120)
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)
    notes: str = Field(default="", max_length=2000)
