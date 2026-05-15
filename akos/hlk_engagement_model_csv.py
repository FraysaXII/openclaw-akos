"""Field contract for ENGAGEMENT_MODEL_REGISTRY.csv (Initiative 73 P1).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/``
per D-IH-73-C sibling-dimension placement (Operations/PMO owns the active
engagement *instance* registry under ``Compliance/canonicals/dimensions/``;
People Operations owns the engagement *model* taxonomy here).

Mirrored to ``compliance.engagement_model_registry_mirror`` on Supabase per
the pattern established by Initiative 32 P2 (skill_registry_mirror) and
Initiative 70 P8.1 (engagement_registry_mirror).

ENGAGEMENT_MODEL_REGISTRY = the canonical taxonomy of 7 retribution-pattern
classes that codify HOW engagements are structured (retribution + SOC + IP +
knowledge-access). Sibling to ENGAGEMENT_REGISTRY.csv (which holds engagement
*instances*); per D-IH-73-C this is a SIBLING canonical (NOT a column-extension
on ENGAGEMENT_REGISTRY.csv) — engagement instances and engagement models have
distinct lifecycles, distinct ownership, and distinct mirror tables.

Decision lineage:
- D-IH-73-A (mega scope; charter)
- D-IH-73-C (sibling-dimension placement)
- D-IH-73-D (7-class taxonomy)
- D-IH-73-E (outsourced helper separate SOC class)
- D-IH-73-H..M (per-class enum ratifications at P1)
- D-IH-73-N (ENGAGEMENT_REGISTRY 17-col extension at P1)

See [`docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.md`](
the canonical schema spec) for the column-by-column contract and the
seven-class taxonomy table.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Keep in sync with the canonical CSV header row at
# docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv
ENGAGEMENT_MODEL_FIELDNAMES: tuple[str, ...] = (
    "engagement_model_id",        # PRIMARY KEY ^eng_model_[a-z0-9_]+$
    "engagement_model_name",      # human-readable
    "retribution_pattern",        # FK to VALID_RETRIBUTION_PATTERNS
    "retribution_unit",           # free-text unit
    "typical_duration",           # free-text duration
    "access_level_default",       # integer 0-6 per access_levels.md
    "soc_posture",                # FK to VALID_SOC_POSTURES
    "ip_clause_class",            # FK to VALID_IP_CLAUSE_CLASSES
    "knowledge_access_level",     # FK to VALID_KNOWLEDGE_ACCESS_LEVELS
    "onboarding_pattern",         # free-text P3 SOP parameterization key
    "offboarding_pattern",        # free-text P3 SOP parameterization key
    "payment_cadence",            # FK to VALID_PAYMENT_CADENCES
    "legal_template_default",     # free-text legal-template label
    "historical_examples",        # free-text case-codename reference (P4 anchor)
    "status",                     # FK to VALID_STATUSES
    "notes",                      # free-form
)


# Cross-canonical enums (frozensets for membership; matched by Literal types below)

VALID_RETRIBUTION_PATTERNS: frozenset[str] = frozenset({
    "hourly",                 # eng_model_hourly_consultant
    "milestone",              # eng_model_milestone_consultant
    "percentage",             # eng_model_percentage_collaborator
    "barter_for_training",    # eng_model_apprentice_learner
    "equity_advisor",         # eng_model_investor_advisor
    "hourly_low_trust",       # eng_model_outsourced_helper
    "operator_self",          # eng_model_operator_self
})

VALID_SOC_POSTURES: frozenset[str] = frozenset({
    "standard",         # legacy / not currently used (reserved for forward classes)
    "cleared",          # cleared-collaborator (full KB-access by engagement)
    "low_trust",        # outsourced_helper (scoped-redacted; no methodology exposure)
    "training_only",    # apprentice_learner (under training; curriculum-bound)
    "internal",         # operator_self (full internal)
})

VALID_IP_CLAUSE_CLASSES: frozenset[str] = frozenset({
    "standard_consultant",
    "milestone_handoff",
    "collaborator_share",
    "training_recipient",
    "advisor_nda",
    "outsourced_workproduct_only",
    "operator_owns_all",
})

VALID_KNOWLEDGE_ACCESS_LEVELS: frozenset[str] = frozenset({
    "full_by_engagement",        # hourly + percentage + investor (cleared)
    "partial_by_engagement",     # milestone (handoff-scoped)
    "training_curriculum_only",  # apprentice (curriculum-bound)
    "work_product_scope_only",   # outsourced (work-product-only handoff)
    "full_internal",             # operator_self (full)
})

VALID_PAYMENT_CADENCES: frozenset[str] = frozenset({
    "per_hour",
    "per_milestone",
    "per_deal_outcome",
    "barter_continuous",
    "per_round",
    "per_hour_capped",
    "none",
})

VALID_STATUSES: frozenset[str] = frozenset({
    "active",
    "deprecated",
    "planned",
})


class EngagementModelRow(BaseModel):
    """Pydantic frozen BaseModel for one row of ENGAGEMENT_MODEL_REGISTRY.csv.

    Per [`CONTRIBUTING.md`](../CONTRIBUTING.md) §"Python Code Standards":
    frozen BaseModel + type hints on every field + Literal enums for governed
    enum columns + integer constraint on access_level_default + slug regex on
    engagement_model_id.
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    engagement_model_id: str = Field(
        ...,
        pattern=r"^eng_model_[a-z0-9_]+$",
        min_length=11,
        max_length=64,
        description="Stable slug; matches ^eng_model_[a-z0-9_]+$",
    )
    engagement_model_name: str = Field(..., min_length=1, max_length=128)
    retribution_pattern: Literal[
        "hourly",
        "milestone",
        "percentage",
        "barter_for_training",
        "equity_advisor",
        "hourly_low_trust",
        "operator_self",
    ]
    retribution_unit: str = Field(..., min_length=1, max_length=64)
    typical_duration: str = Field(..., min_length=1, max_length=64)
    access_level_default: int = Field(..., ge=0, le=6)
    soc_posture: Literal[
        "standard",
        "cleared",
        "low_trust",
        "training_only",
        "internal",
    ]
    ip_clause_class: Literal[
        "standard_consultant",
        "milestone_handoff",
        "collaborator_share",
        "training_recipient",
        "advisor_nda",
        "outsourced_workproduct_only",
        "operator_owns_all",
    ]
    knowledge_access_level: Literal[
        "full_by_engagement",
        "partial_by_engagement",
        "training_curriculum_only",
        "work_product_scope_only",
        "full_internal",
    ]
    onboarding_pattern: str = Field(..., min_length=1, max_length=128)
    offboarding_pattern: str = Field(..., min_length=1, max_length=128)
    payment_cadence: Literal[
        "per_hour",
        "per_milestone",
        "per_deal_outcome",
        "barter_continuous",
        "per_round",
        "per_hour_capped",
        "none",
    ]
    legal_template_default: str = Field(..., min_length=1, max_length=256)
    historical_examples: str = Field(default="", max_length=512)
    status: Literal["active", "deprecated", "planned"]
    notes: str = Field(default="", max_length=1024)

    @field_validator("access_level_default", mode="before")
    @classmethod
    def _coerce_access_level_int(cls, v: object) -> int:
        """CSV cells arrive as strings; coerce digit-strings to int before bounds check.

        Rejects non-digit strings via ValueError so the validator surfaces
        the offending row clearly (per CONTRIBUTING.md §"Python Code Standards"
        — Pydantic for CSV validation; no hand-written assert chains).
        """
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                raise ValueError("access_level_default empty (required 0-6)")
            try:
                return int(stripped)
            except ValueError as exc:
                raise ValueError(
                    f"access_level_default {stripped!r} not parseable as int 0-6"
                ) from exc
        raise TypeError(f"access_level_default unsupported type: {type(v).__name__}")
