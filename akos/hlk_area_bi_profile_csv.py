"""Field contract for AREA_BI_PROFILE.csv (Initiative 93 P5c).

Per-area BI consumption declarations — DATA owns the plane; areas declare consumption.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

AREA_BI_PROFILE_FIELDNAMES: tuple[str, ...] = (
    "area_id",
    "steward_role",
    "primary_bi_tiers",
    "default_engagement_stream",
    "analytics_buckets_posture",
    "primary_consumer_ids",
    "paired_sop_family",
    "contract_obligation",
    "status",
    "linked_decision_id",
    "notes",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
)

VALID_AREA_BI_STATUSES: frozenset[str] = frozenset({
    "active",
    "planned",
    "experimental",
    "deprecated",
})

VALID_BUCKETS_POSTURES: frozenset[str] = frozenset({
    "not_applicable",
    "operator_production",
    "planned",
    "experimental",
})

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/"
    "dimensions/AREA_BI_PROFILE.csv"
)


class AreaBiProfileRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    area_id: str = Field(pattern=r"^[A-Z][a-zA-Z]+$")
    steward_role: str = Field(min_length=2, max_length=80)
    primary_bi_tiers: str = Field(min_length=2, max_length=40)
    default_engagement_stream: Literal["internal", "A", "B", "C"]
    analytics_buckets_posture: Literal["not_applicable", "operator_production", "planned", "experimental"]
    primary_consumer_ids: str = Field(min_length=3, max_length=500)
    paired_sop_family: str = Field(min_length=1, max_length=500)
    contract_obligation: Literal["required", "optional", "none"]
    status: Literal["active", "planned", "experimental", "deprecated"]
    linked_decision_id: str = Field(pattern=r"^D-IH-[0-9]+-[A-Z0-9]+$")
    notes: str = ""
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=2, max_length=80)
    last_review_decision_id: str = Field(pattern=r"^D-IH-[0-9]+-[A-Z0-9]+$")
    methodology_version_at_review: str = Field(pattern=r"^v\d+\.\d+$")
