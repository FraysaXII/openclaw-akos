"""Field contract for Finance plane-2 registries (FINANCE-AREA-FULL F2a).

- ``PRICING_TIER_REGISTRY.csv`` — subscription / service tier SSOT keyed to
  ``thi_finan_dtp_203`` (trial, starter, growth, pro, plus, consultant).
- ``FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv`` — IFRS 15 performance
  obligation codes referenced by the rev-rec policy + pricing tiers.

Canonical paths live under
``docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/dimensions/``
per FINOPS_DISCIPLINE plane 2.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

PRICING_TIER_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "pricing_tier_id",
    "tier_slug",
    "display_name",
    "product_surface",
    "performance_obligation_id",
    "pmo_pricing_model_ref",
    "billing_cadence",
    "status",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
    "notes",
)

FINOPS_PERFORMANCE_OBLIGATION_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "obligation_id",
    "obligation_name",
    "ifrs15_pattern",
    "recognition_trigger",
    "policy_section_ref",
    "status",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
    "notes",
    "information_asset_ref",
)

VALID_PRICING_TIER_STATUSES: frozenset[str] = frozenset({
    "active",
    "draft",
    "deprecated",
})

VALID_PRODUCT_SURFACES: frozenset[str] = frozenset({
    "kirbe_saas",
    "service_engagement",
    "partner_channel",
    "internal_trial",
})

VALID_BILLING_CADENCES: frozenset[str] = frozenset({
    "monthly",
    "annual_prepay",
    "one_time",
    "usage_metered",
    "n_a",
})

VALID_IFRS15_PATTERNS: frozenset[str] = frozenset({
    "over_time",
    "point_in_time",
})

PRICING_TIER_CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/"
    "dimensions/PRICING_TIER_REGISTRY.csv"
)

PERF_OBLIGATION_CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/"
    "dimensions/FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv"
)


class FinopsPerformanceObligationRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    obligation_id: str = Field(pattern=r"^PO-FIN-HOL-[A-Z0-9-]+$")
    obligation_name: str = Field(min_length=1, max_length=200)
    ifrs15_pattern: Literal["over_time", "point_in_time"]
    recognition_trigger: str = Field(min_length=1, max_length=512)
    policy_section_ref: str = Field(min_length=1, max_length=512)
    status: Literal["active", "draft", "deprecated"]
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)
    notes: str = Field(default="", max_length=2000)
    information_asset_ref: str = Field(default="", max_length=120)


class PricingTierRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    pricing_tier_id: str = Field(pattern=r"^PT-FIN-HOL-[A-Z0-9-]+$")
    tier_slug: str = Field(pattern=r"^[a-z][a-z0-9_]*$", min_length=1, max_length=64)
    display_name: str = Field(min_length=1, max_length=120)
    product_surface: Literal[
        "kirbe_saas",
        "service_engagement",
        "partner_channel",
        "internal_trial",
    ]
    performance_obligation_id: str = Field(pattern=r"^PO-FIN-HOL-[A-Z0-9-]+$")
    pmo_pricing_model_ref: str = Field(default="", max_length=512)
    billing_cadence: Literal[
        "monthly",
        "annual_prepay",
        "one_time",
        "usage_metered",
        "n_a",
    ]
    status: Literal["active", "draft", "deprecated"]
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)
    notes: str = Field(default="", max_length=2000)
