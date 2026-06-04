"""Field contract for METRICS_REGISTRY.csv (Initiative 93 P4).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/``
per SEMANTIC_LAYER.md + DATA_ARCHITECTURE.md.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

METRICS_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "metric_id",
    "metric_name",
    "definition_sql_ref",
    "grain",
    "dimensions",
    "owner_business_role",
    "owner_technical_role",
    "source_contract_id",
    "access_level",
    "status",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
    "notes",
)

VALID_METRIC_STATUSES: frozenset[str] = frozenset({
    "active",
    "draft",
    "deprecated",
})

VALID_ACCESS_LEVELS: frozenset[str] = frozenset({
    "3",
    "4",
    "5",
})

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/"
    "dimensions/METRICS_REGISTRY.csv"
)


class MetricsRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    metric_id: str = Field(pattern=r"^MET-HOL-[A-Z0-9-]+$")
    metric_name: str = Field(min_length=1, max_length=200)
    definition_sql_ref: str = Field(min_length=1, max_length=512)
    grain: str = Field(min_length=1, max_length=120)
    dimensions: str = Field(default="", max_length=512)
    owner_business_role: str = Field(min_length=1, max_length=120)
    owner_technical_role: str = Field(min_length=1, max_length=120)
    source_contract_id: str = Field(default="", max_length=64)
    access_level: Literal["3", "4", "5"]
    status: Literal["active", "draft", "deprecated"]
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)
    notes: str = Field(default="", max_length=2000)
