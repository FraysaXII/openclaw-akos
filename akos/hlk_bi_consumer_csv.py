"""Field contract for BI_CONSUMER_REGISTRY.csv (Initiative 93 P5b).

Governed BI/integration consumer rows per DATA_BI_GOVERNANCE.md + D-IH-93-I amendment.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

BI_CONSUMER_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "consumer_id",
    "bi_tier",
    "tool_name",
    "component_id",
    "data_surfaces",
    "status",
    "paired_sop_path",
    "engagement_stream",
    "owner_role",
    "linked_decision_id",
    "notes",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
)

VALID_BI_TIERS: frozenset[str] = frozenset({f"T{n}" for n in range(1, 11)})

VALID_BI_CONSUMER_STATUSES: frozenset[str] = frozenset({
    "active",
    "planned",
    "experimental",
    "deprecated",
    "client_tenant",
})

VALID_ENGAGEMENT_STREAMS: frozenset[str] = frozenset({
    "internal",
    "A",
    "B",
    "C",
})

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "dimensions/BI_CONSUMER_REGISTRY.csv"
)


class BiConsumerRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    consumer_id: str = Field(pattern=r"^BI-HOL-[A-Z0-9-]+$")
    bi_tier: str
    tool_name: str = Field(min_length=2, max_length=120)
    component_id: str = Field(pattern=r"^comp_[a-z0-9_]+$")
    data_surfaces: str = Field(min_length=3, max_length=500)
    status: Literal["active", "planned", "experimental", "deprecated", "client_tenant"]
    paired_sop_path: str = Field(min_length=1, max_length=500)
    engagement_stream: Literal["internal", "A", "B", "C"]
    owner_role: str = Field(min_length=2, max_length=80)
    linked_decision_id: str = Field(pattern=r"^D-IH-[0-9]+-[A-Z0-9]+$")
    notes: str = ""
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=2, max_length=80)
    last_review_decision_id: str = Field(pattern=r"^D-IH-[0-9]+-[A-Z0-9]+$")
    methodology_version_at_review: str = Field(pattern=r"^v\d+\.\d+$")
