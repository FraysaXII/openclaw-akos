"""Field contract for SERVICE_CATALOG.csv (Operations/SMO; I70 P8 / P95-GOV-4).

Canonical CSV at ``docs/references/hlk/v3.0/Admin/O5-1/Operations/SMO/canonicals/SERVICE_CATALOG.csv``.
Git-only SSOT per D-IH-70-AB + D-IH-95-B; validated with ``scripts/validate_service_catalog.py``.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

SERVICE_CATALOG_FIELDNAMES: tuple[str, ...] = (
    "service_id",
    "name",
    "customer_facing_description",
    "delivery_role_primary",
    "delivery_role_secondary",
    "cost_model",
    "sla_tier",
    "active_engagements",
    "status",
    "notes",
)

CANONICAL_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/Operations/SMO/canonicals/SERVICE_CATALOG.csv"
)

VALID_SERVICE_STATUSES: frozenset[str] = frozenset({
    "pre-sold",
    "active",
    "deprecated",
    "planned",
})

VALID_SLA_TIERS: frozenset[str] = frozenset({
    "Tier 1 (Premium)",
    "Tier 2 (Standard)",
    "Tier 3 (Light)",
    "per-engagement (default Tier 2)",
    "per-engagement",
})

# Engagement-specific delivery labels not yet normalized to baseline role_name rows.
DELIVERY_ROLE_ALIASES: frozenset[str] = frozenset({
    "EFA Academie partner-lead",
    "Holistika Research",
})

SERVICE_ID_RE = re.compile(r"^SVC-\d{3}$")


class ServiceCatalogRow(BaseModel):
    """Pydantic model for one row of SERVICE_CATALOG.csv."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    service_id: str
    name: str = Field(min_length=1, max_length=120)
    customer_facing_description: str = Field(min_length=1, max_length=500)
    delivery_role_primary: str = Field(min_length=1, max_length=80)
    delivery_role_secondary: str = Field(default="", max_length=120)
    cost_model: str = Field(min_length=1, max_length=300)
    sla_tier: str
    active_engagements: str = Field(min_length=1, max_length=120)
    status: Literal["pre-sold", "active", "deprecated", "planned"]
    notes: str = Field(default="", max_length=500)

    @field_validator("service_id")
    @classmethod
    def service_id_shape(cls, value: str) -> str:
        if not SERVICE_ID_RE.match(value):
            raise ValueError("service_id must match SVC-NNN")
        return value

    @field_validator("sla_tier")
    @classmethod
    def sla_tier_enum(cls, value: str) -> str:
        if value not in VALID_SLA_TIERS:
            raise ValueError(f"sla_tier must be one of {sorted(VALID_SLA_TIERS)}")
        return value
