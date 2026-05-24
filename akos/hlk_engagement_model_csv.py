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
- D-IH-81-X (Bundle B-2c 2026-05-23: +1 column `counterparty_resolution_strategy`
  + 3 new rows `eng_model_saas_subscription` (active) + `eng_model_rpp_vendor`
  (planned) + `eng_model_one_off_invoice` (planned) extending the people-taxonomy
  to a unified counterparty-routing taxonomy. Operator ratifications: b2c-enum-a
  (NOT NULL + 4-engagement_id / 3-manual_review mapping for original 7 rows) +
  b2c-rows-c (3 new rows). New enum extensions: VALID_RETRIBUTION_PATTERNS +3
  (subscription_recurring / vendor_pass_through / one_off_ad_hoc);
  VALID_PAYMENT_CADENCES +2 (monthly_recurring / per_invoice);
  VALID_IP_CLAUSE_CLASSES +3 (saas_tos / vendor_invoice_only / none_required);
  VALID_KNOWLEDGE_ACCESS_LEVELS +1 (none). New column FK-resolves into
  VALID_RESOLUTION_STRATEGIES at akos/hlk_finops_ledger.py L110-117.)

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
    "engagement_model_id",                # PRIMARY KEY ^eng_model_[a-z0-9_]+$
    "engagement_model_name",              # human-readable
    "retribution_pattern",                # FK to VALID_RETRIBUTION_PATTERNS
    "retribution_unit",                   # free-text unit
    "typical_duration",                   # free-text duration
    "access_level_default",               # integer 0-6 per access_levels.md
    "soc_posture",                        # FK to VALID_SOC_POSTURES
    "ip_clause_class",                    # FK to VALID_IP_CLAUSE_CLASSES
    "knowledge_access_level",             # FK to VALID_KNOWLEDGE_ACCESS_LEVELS
    "onboarding_pattern",                 # free-text P3 SOP parameterization key
    "offboarding_pattern",                # free-text P3 SOP parameterization key
    "payment_cadence",                    # FK to VALID_PAYMENT_CADENCES
    "legal_template_default",             # free-text legal-template label
    "historical_examples",                # free-text case-codename reference (P4 anchor)
    "status",                             # FK to VALID_STATUSES
    "notes",                              # free-form
    "counterparty_resolution_strategy",   # B-2c (D-IH-81-X): FK to VALID_COUNTERPARTY_RESOLUTION_STRATEGIES
)


# Cross-canonical enums (frozensets for membership; matched by Literal types below)

VALID_RETRIBUTION_PATTERNS: frozenset[str] = frozenset({
    "hourly",                  # eng_model_hourly_consultant
    "milestone",               # eng_model_milestone_consultant
    "percentage",              # eng_model_percentage_collaborator
    "barter_for_training",     # eng_model_apprentice_learner
    "equity_advisor",          # eng_model_investor_advisor
    "hourly_low_trust",        # eng_model_outsourced_helper
    "operator_self",           # eng_model_operator_self
    # Bundle B-2c (D-IH-81-X) — unified counterparty-routing extensions:
    "subscription_recurring",  # eng_model_saas_subscription (KiRBe + future SaaS)
    "vendor_pass_through",     # eng_model_rpp_vendor (Revenue Pass-Through; forward-charter resolver)
    "one_off_ad_hoc",          # eng_model_one_off_invoice (irregular invoicing)
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
    # Bundle B-2c (D-IH-81-X) — unified counterparty-routing extensions:
    "saas_tos",              # eng_model_saas_subscription (SaaS Terms of Service; no SoW)
    "vendor_invoice_only",   # eng_model_rpp_vendor (vendor invoice acceptance; no Holistika-side IP)
    "none_required",         # eng_model_one_off_invoice (ad-hoc; no IP transfer)
})

VALID_KNOWLEDGE_ACCESS_LEVELS: frozenset[str] = frozenset({
    "full_by_engagement",        # hourly + percentage + investor (cleared)
    "partial_by_engagement",     # milestone (handoff-scoped)
    "training_curriculum_only",  # apprentice (curriculum-bound)
    "work_product_scope_only",   # outsourced (work-product-only handoff)
    "full_internal",             # operator_self (full)
    # Bundle B-2c (D-IH-81-X) — unified counterparty-routing extensions:
    "none",                      # SaaS customer / vendor / one-off — no KB access
})

VALID_PAYMENT_CADENCES: frozenset[str] = frozenset({
    "per_hour",
    "per_milestone",
    "per_deal_outcome",
    "barter_continuous",
    "per_round",
    "per_hour_capped",
    "none",
    # Bundle B-2c (D-IH-81-X) — unified counterparty-routing extensions:
    "monthly_recurring",   # eng_model_saas_subscription
    "per_invoice",         # eng_model_rpp_vendor + eng_model_one_off_invoice
})


# B-2c (D-IH-81-X) — counterparty routing strategies. MUST stay in lockstep with
# akos/hlk_finops_ledger.py VALID_RESOLUTION_STRATEGIES (the resolver SSOT); this
# frozenset is the per-engagement-model contract that the resolver consumes.
VALID_COUNTERPARTY_RESOLUTION_STRATEGIES: frozenset[str] = frozenset({
    "metadata_engagement_id",       # HIGH confidence; Stripe metadata.hlk_engagement_id is the lever
    "metadata_billing_plane",       # MEDIUM confidence; Stripe metadata.hlk_billing_plane
    "stripe_customer_link_lookup",  # LOW confidence; JOIN holistika_ops.stripe_customer_link
    "rpp_payout_attribution",       # FORWARD-CHARTER; not yet implemented in counterparty_resolver.ts
    "manual_review",                # No automated strategy; OPS_REGISTER row emitted on event
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
        # Bundle B-2c (D-IH-81-X):
        "subscription_recurring",
        "vendor_pass_through",
        "one_off_ad_hoc",
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
        # Bundle B-2c (D-IH-81-X):
        "saas_tos",
        "vendor_invoice_only",
        "none_required",
    ]
    knowledge_access_level: Literal[
        "full_by_engagement",
        "partial_by_engagement",
        "training_curriculum_only",
        "work_product_scope_only",
        "full_internal",
        # Bundle B-2c (D-IH-81-X):
        "none",
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
        # Bundle B-2c (D-IH-81-X):
        "monthly_recurring",
        "per_invoice",
    ]
    legal_template_default: str = Field(..., min_length=1, max_length=256)
    historical_examples: str = Field(default="", max_length=512)
    status: Literal["active", "deprecated", "planned"]
    notes: str = Field(default="", max_length=1024)
    # B-2c (D-IH-81-X) — counterparty routing strategy; NOT NULL (no default).
    counterparty_resolution_strategy: Literal[
        "metadata_engagement_id",
        "metadata_billing_plane",
        "stripe_customer_link_lookup",
        "rpp_payout_attribution",
        "manual_review",
    ]

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
