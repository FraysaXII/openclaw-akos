"""Field contracts for the 5 Collaborator-Share canonical CSVs (D-IH-86-CY-A).

Canonical CSVs live under
``docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/``
per COLLABORATOR_SHARE_DOCTRINE.md §2 + D-IH-86-CY-A..D ratification.

The 5 registers are:
  1. COLLABORATOR_SHARE_REGISTRY     - per-(engagement, collaborator) share row
  2. HOLISTIKA_VENDOR_SERVICES_BILLED - per-engagement billed-vs-in-kind log
  3. PARTNER_OVERLAP_EXCLUSION_CLAUSES - named overlap-clause pattern table
  4. COLLABORATOR_MARKET_RATE_REFERENCE - role x region x experience benchmarks
  5. COLLABORATOR_RATE_OVERRIDES      - governed commercial deviations

The Pydantic models here are the SSOT for the CSV headers; the validator
``scripts/validate_collaborator_share.py`` and the runbook
``scripts/collaborator_share_calculate.py`` (both landing in Commit 2b) bind
against these models.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# =============================================================================
# 1. COLLABORATOR_SHARE_REGISTRY
# =============================================================================

COLLABORATOR_SHARE_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "share_id",
    "engagement_id",
    "collaborator_id",
    "engagement_model_id",
    "holistika_share_pct",
    "collaborator_share_pct",
    "collaborator_billed_rate",
    "collaborator_billed_rate_currency",
    "collaborator_role_class",
    "share_override_decision_id",
    "status",
    "signed_at",
    "signed_by_collaborator",
    "signed_by_holistika",
    "last_review_at",
    "notes",
)

VALID_SHARE_REGISTRY_STATUSES: frozenset[str] = frozenset({
    "draft",
    "proposed",
    "signed",
    "active",
    "settled",
    "archived",
})

DEFAULT_HOLISTIKA_SHARE_PCT: int = 65
DEFAULT_COLLABORATOR_SHARE_PCT: int = 35

CSV_PATH_RELATIVE_SHARE_REGISTRY: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "dimensions/COLLABORATOR_SHARE_REGISTRY.csv"
)


class CollaboratorShareRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    share_id: str = Field(pattern=r"^SHARE-[A-Z0-9-]+$", min_length=8, max_length=64)
    engagement_id: str = Field(min_length=1, max_length=120)
    collaborator_id: str = Field(min_length=1, max_length=64)
    engagement_model_id: str = Field(min_length=1, max_length=64)
    holistika_share_pct: int = Field(ge=0, le=100)
    collaborator_share_pct: int = Field(ge=0, le=100)
    collaborator_billed_rate: float = Field(ge=0)
    collaborator_billed_rate_currency: str = Field(
        pattern=r"^[A-Z]{3}$", min_length=3, max_length=3
    )
    collaborator_role_class: str = Field(min_length=1, max_length=120)
    share_override_decision_id: str = ""
    status: Literal[
        "draft", "proposed", "signed", "active", "settled", "archived"
    ]
    signed_at: str = Field(default="", pattern=r"^(\d{4}-\d{2}-\d{2})?$")
    signed_by_collaborator: str = ""
    signed_by_holistika: str = ""
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    notes: str = ""


# =============================================================================
# 2. HOLISTIKA_VENDOR_SERVICES_BILLED
# =============================================================================

HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES: tuple[str, ...] = (
    "vendor_billing_id",
    "engagement_id",
    "holistika_service_class",
    "bill_mode",
    "billed_hours",
    "billed_rate",
    "billed_amount_computed",
    "justification_clause_id",
    "bill_mode_decision_id",
    "status",
    "last_review_at",
    "notes",
)

VALID_HOLISTIKA_SERVICE_CLASSES: frozenset[str] = frozenset({
    "research_head_discipline",
    "mktops_marketing",
    "dataops_engineering",
    "madeira_ai_orchestration",
    "brand_render_machinery",
    "pmo_orchestration",
    "legal_template_handling",
    "front_end_engineering",
    "ai_engineering_bespoke",
    "external_research_pass",
})

VALID_BILL_MODES: frozenset[str] = frozenset({"billed", "in_kind"})

# Doctrine default bill_mode per service class (COLLABORATOR_SHARE_DOCTRINE.md
# §2.2). Deviations require ``bill_mode_decision_id`` FK to DECISION_REGISTER.
DEFAULT_BILL_MODE_PER_SERVICE_CLASS: dict[str, str] = {
    "research_head_discipline": "in_kind",
    "mktops_marketing": "in_kind",
    "dataops_engineering": "in_kind",
    "madeira_ai_orchestration": "in_kind",
    "brand_render_machinery": "in_kind",
    "pmo_orchestration": "in_kind",
    "legal_template_handling": "in_kind",  # default for standard templates
    "front_end_engineering": "billed",     # default for scope-bearing work
    "ai_engineering_bespoke": "billed",
    "external_research_pass": "billed",
}

CSV_PATH_RELATIVE_VENDOR_BILLED: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "dimensions/HOLISTIKA_VENDOR_SERVICES_BILLED.csv"
)


class HolistikaVendorServicesBilledRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    vendor_billing_id: str = Field(
        pattern=r"^VBILL-[A-Z0-9-]+$", min_length=8, max_length=64
    )
    engagement_id: str = Field(min_length=1, max_length=120)
    holistika_service_class: Literal[
        "research_head_discipline",
        "mktops_marketing",
        "dataops_engineering",
        "madeira_ai_orchestration",
        "brand_render_machinery",
        "pmo_orchestration",
        "legal_template_handling",
        "front_end_engineering",
        "ai_engineering_bespoke",
        "external_research_pass",
    ]
    bill_mode: Literal["billed", "in_kind"]
    billed_hours: float | str = ""  # empty string for in_kind rows
    billed_rate: float | str = ""
    billed_amount_computed: float | str = ""
    justification_clause_id: str = ""
    bill_mode_decision_id: str = ""
    status: Literal["draft", "active", "settled", "archived"]
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    notes: str = ""


# =============================================================================
# 3. PARTNER_OVERLAP_EXCLUSION_CLAUSES
# =============================================================================

PARTNER_OVERLAP_EXCLUSION_CLAUSES_FIELDNAMES: tuple[str, ...] = (
    "clause_id",
    "clause_name",
    "applicable_holistika_service_classes",
    "overlap_pattern_description",
    "internal_precedent",
    "industry_precedent_citation",
    "ratifying_decision_id",
    "last_review_at",
    "status",
    "notes",
)

VALID_CLAUSE_STATUSES: frozenset[str] = frozenset({
    "active",
    "planned",
    "deprecated",
    "archived",
})

CSV_PATH_RELATIVE_OVERLAP_CLAUSES: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "dimensions/PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv"
)


class PartnerOverlapExclusionClauseRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    clause_id: str = Field(pattern=r"^clause_[a-z0-9_]+$", min_length=8, max_length=120)
    clause_name: str = Field(min_length=1, max_length=200)
    applicable_holistika_service_classes: str = Field(min_length=1, max_length=400)
    overlap_pattern_description: str = Field(min_length=1, max_length=4000)
    internal_precedent: str = ""
    industry_precedent_citation: str = ""
    ratifying_decision_id: str = Field(min_length=1, max_length=32)
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    status: Literal["active", "planned", "deprecated", "archived"]
    notes: str = ""


# =============================================================================
# 4. COLLABORATOR_MARKET_RATE_REFERENCE
# =============================================================================

COLLABORATOR_MARKET_RATE_REFERENCE_FIELDNAMES: tuple[str, ...] = (
    "rate_id",
    "role_class",
    "region_code",
    "experience_band",
    "rate_currency",
    "rate_min_per_hour",
    "rate_typical_per_hour",
    "rate_max_per_hour",
    "rate_source",
    "last_review_at",
    "status",
    "notes",
)

VALID_EXPERIENCE_BANDS: frozenset[str] = frozenset({
    "junior",
    "mid",
    "senior",
    "lead",
    "expert",
})

VALID_RATE_STATUSES: frozenset[str] = frozenset({
    "active",
    "planned",
    "deprecated",
    "archived",
})

MARKET_RATE_VARIANCE_TOLERANCE_PCT: float = 25.0  # +/- 25% per CS-04 audit

CSV_PATH_RELATIVE_MARKET_RATE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "dimensions/COLLABORATOR_MARKET_RATE_REFERENCE.csv"
)


class CollaboratorMarketRateReferenceRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    rate_id: str = Field(pattern=r"^rate_[a-z0-9_]+$", min_length=6, max_length=120)
    role_class: str = Field(min_length=1, max_length=120)
    region_code: str = Field(pattern=r"^[A-Z]{2}$", min_length=2, max_length=2)
    experience_band: Literal["junior", "mid", "senior", "lead", "expert"]
    rate_currency: str = Field(pattern=r"^[A-Z]{3}$", min_length=3, max_length=3)
    rate_min_per_hour: float = Field(ge=0)
    rate_typical_per_hour: float = Field(gt=0)
    rate_max_per_hour: float = Field(gt=0)
    rate_source: str = Field(min_length=1, max_length=400)
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    status: Literal["active", "planned", "deprecated", "archived"]
    notes: str = ""


# =============================================================================
# 5. COLLABORATOR_RATE_OVERRIDES
# =============================================================================

COLLABORATOR_RATE_OVERRIDES_FIELDNAMES: tuple[str, ...] = (
    "override_id",
    "override_kind",
    "engagement_id",
    "collaborator_id",
    "reference_rate_id",
    "reference_rate_value",
    "actual_value",
    "variance_pct",
    "justification_narrative",
    "ratifying_decision_id",
    "commercial_strategy_rationale",
    "expires_at",
    "last_review_at",
    "status",
    "notes",
)

VALID_OVERRIDE_KINDS: frozenset[str] = frozenset({
    "market_rate_excursion",
    "share_split_deviation",
})

VALID_OVERRIDE_STATUSES: frozenset[str] = frozenset({
    "draft",
    "active",
    "expired",
    "archived",
})

CSV_PATH_RELATIVE_RATE_OVERRIDES: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/"
    "dimensions/COLLABORATOR_RATE_OVERRIDES.csv"
)


class CollaboratorRateOverrideRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    override_id: str = Field(
        pattern=r"^OVERRIDE-[A-Z0-9-]+$", min_length=10, max_length=64
    )
    override_kind: Literal["market_rate_excursion", "share_split_deviation"]
    engagement_id: str = Field(min_length=1, max_length=120)
    collaborator_id: str = Field(min_length=1, max_length=64)
    reference_rate_id: str = ""
    reference_rate_value: float | str = ""
    actual_value: float
    variance_pct: float
    justification_narrative: str = Field(min_length=1, max_length=2000)
    ratifying_decision_id: str = Field(min_length=1, max_length=32)
    commercial_strategy_rationale: str = Field(min_length=1, max_length=1000)
    expires_at: str = Field(default="", pattern=r"^(\d{4}-\d{2}-\d{2})?$")
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    status: Literal["draft", "active", "expired", "archived"]
    notes: str = ""


# =============================================================================
# Cross-CSV invariant helpers (consumed by validator + runbook)
# =============================================================================


def default_split_holds(holistika_pct: int, collaborator_pct: int) -> bool:
    """Return True iff (holistika_pct, collaborator_pct) matches the doctrine
    default 65/35 split. Per CS-03 audit: non-default split requires an
    OVERRIDE row + DECISION_REGISTER FK.
    """
    return (
        holistika_pct == DEFAULT_HOLISTIKA_SHARE_PCT
        and collaborator_pct == DEFAULT_COLLABORATOR_SHARE_PCT
    )


def split_sums_to_100(holistika_pct: int, collaborator_pct: int) -> bool:
    """Return True iff the share splits sum to exactly 100. Per CS-03 audit."""
    return holistika_pct + collaborator_pct == 100


def bill_mode_matches_default(service_class: str, bill_mode: str) -> bool:
    """Return True iff the row's bill_mode matches the doctrine default for
    that service class. Per CS-05 audit: deviation requires
    ``bill_mode_decision_id`` FK.
    """
    return DEFAULT_BILL_MODE_PER_SERVICE_CLASS.get(service_class) == bill_mode


def rate_within_market_band(
    actual_rate: float,
    typical_rate: float,
    tolerance_pct: float = MARKET_RATE_VARIANCE_TOLERANCE_PCT,
) -> bool:
    """Return True iff actual_rate is within +/- tolerance_pct of typical_rate.
    Per CS-04 audit: outside-band rates require an OVERRIDE row.
    """
    if typical_rate <= 0:
        return False
    variance_pct = abs((actual_rate - typical_rate) / typical_rate) * 100.0
    return variance_pct <= tolerance_pct


def variance_pct_signed(actual_value: float, reference_value: float) -> float:
    """Return the signed percentage variance of actual_value from
    reference_value. Used by the runbook when authoring OVERRIDE rows.
    """
    if reference_value == 0:
        return 0.0
    return ((actual_value - reference_value) / reference_value) * 100.0
