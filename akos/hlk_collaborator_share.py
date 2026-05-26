"""Field contracts for the 5 Collaborator-Share canonical CSVs (D-IH-86-DA).

Canonical CSVs live under
``docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/``
per COLLABORATOR_SHARE_DOCTRINE.md §2 + D-IH-86-DA..D ratification.

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
    "share_pattern",
    "share_overlay",
    "holistika_share_pct",
    "collaborator_share_pct",
    "collaborator_billed_rate",
    "collaborator_billed_rate_currency",
    "collaborator_role_class",
    "methodology_readiness",
    "share_override_decision_id",
    "status",
    "signed_at",
    "signed_by_collaborator",
    "signed_by_holistika",
    "last_review_at",
    "notes",
    "parallel_invoice_stream_indicator",
)

VALID_SHARE_REGISTRY_STATUSES: frozenset[str] = frozenset({
    "draft",
    "proposed",
    "signed",
    "active",
    "settled",
    "archived",
})

# D-IH-86-EJ (Wave R+2 Commit 2 chassis update; full rewrite supersedes
# D-IH-86-DE per operator ratification Q1=a_full_rewrite_now 2026-05-26):
# `share_pattern` is the top-level economic-model classifier per the
# rewritten COLLABORATOR_SHARE_DOCTRINE.md §2.3. The pre-rewrite 3-shape
# enum (deep_partner_65_35 / orchestration_broker_thin_margin / custom) is
# REPLACED with a 4-base + 1-stackable-overlay model. The pre-rewrite
# values `orchestration_broker_thin_margin` AND `custom` are no longer
# valid; pre-rewrite rows authored under either value MUST be migrated via
# the Commit-5 supersede SQL.
#
# Four base patterns + one stackable overlay:
#
#   - deep_partner_65_35 (PRESERVED from pre-rewrite):
#       One row per (engagement, collaborator) pair. holistika_share_pct +
#       collaborator_share_pct == 100 on the row. Default 65/35 deviation
#       requires `share_override_decision_id` FK (CS-04 audit). Used when
#       Holistika contributes the full methodology + machinery + execution
#       stack as the value of its 65% share, with the collaborator bringing
#       the deal + operating the process under a B2B partner narrative.
#       Worked precedent: Websitz / Rushly engagement.
#
#   - bd_intro_only (NEW per D-IH-86-EJ):
#       Two-row engagement: BD-introducer row (15% BD commission +
#       Holistika-corporate row (85% of revenue). Across-rows sum-to-100.
#       Used when a collaborator introduces a deal but operates as a BD /
#       account-manager only (no ongoing methodology consumption); the BD
#       partner gets 15% as long as they nurture the account, Holistika
#       delivers the full project with own resources or contracted help.
#       Worked precedent: forward-charter (no live instances yet).
#
#   - joint_venture_aventure (NEW per D-IH-86-EJ):
#       Two-row engagement: 50/50 symmetric split. Default 50/50; deviations
#       require `share_override_decision_id` FK + matching OVERRIDE row.
#       Used when Holistika + collaborator pool methodology bench
#       symmetrically into a co-created venture and revenue is split
#       proportional to ownership (not labor); methodology-readiness must
#       be `methodology_trained` (the symmetric framing assumes equal
#       methodology bench, otherwise the discipline becomes asymmetric).
#       Worked precedent: forward-charter (no live instances yet).
#
#   - consulting_direct (NEW per D-IH-86-EJ; DEFAULT when no collaborator):
#       Default Holistika own-billing pattern. Single row (when no overlay
#       present): holistika_share_pct = 100, collaborator_share_pct = 0;
#       Holistika consults the customer directly and bills 100% of the
#       project value. With `bd_commission_overlay` sibling row present:
#       base row anchors at 85/0 + overlay row at 0/15 across-rows = 100.
#       Used when Holistika delivers a consulting engagement own-account
#       and the deal source (BD-introducer) is structurally separate from
#       project delivery (commercially compensated via the overlay).
#       Worked precedent: SUEZ POC (post-recommercialisation per
#       D-IH-86-EL; Aïsha gets 15% BD commission overlay).
#
#   - bd_commission_overlay (NEW stackable overlay per D-IH-86-EJ):
#       NOT a standalone share_pattern; declared via the `share_overlay`
#       column (separate from share_pattern). Overlay row is paired with
#       a sibling base row at the same engagement_id. Overlay row's
#       collaborator_share_pct = the overlay percentage (e.g., 15);
#       holistika_share_pct = 0. CS-09 audit enforces valid base pairings:
#       overlay pairs with `consulting_direct` OR `deep_partner_65_35`;
#       FORBIDDEN pairings with `bd_intro_only` (circular — overlay would
#       restate the BD pattern) AND `joint_venture_aventure` (conflates
#       symmetry with intro asymmetry). Worked precedent: SUEZ POC
#       (Aïsha-as-BD per D-IH-86-EL).

VALID_SHARE_PATTERNS: frozenset[str] = frozenset({
    "deep_partner_65_35",
    "bd_intro_only",
    "joint_venture_aventure",
    "consulting_direct",
})

VALID_SHARE_OVERLAYS: frozenset[str] = frozenset({
    "bd_commission_overlay",
})

# Per CS-09 audit (D-IH-86-EJ): valid overlay-base pairings table. When a
# row carries a non-empty `share_overlay`, its sibling base row(s) at the
# same engagement_id must have a `share_pattern` in this overlay's set.
# Forbidden pairings produce a FAIL finding.
VALID_OVERLAY_BASE_PAIRINGS: dict[str, frozenset[str]] = {
    "bd_commission_overlay": frozenset({
        "consulting_direct",
        "deep_partner_65_35",
    }),
}

# Per D-IH-86-EN (methodology-readiness axis added at Wave R+2 Commit 1):
# share_pattern eligibility is mandatorily gated by the collaborator's
# methodology-readiness state. Prevents the "35% compromise to bridge a
# methodology gap" failure mode operator named explicitly 2026-05-26.
VALID_METHODOLOGY_READINESS: frozenset[str] = frozenset({
    "methodology_trained",
    "methodology_in_progress",
    "methodology_naive",
    "methodology_not_applicable",
})

# Per the rewritten doctrine §2.4: methodology-readiness gates which
# share_pattern values are eligible. `methodology_trained` collaborators
# unlock all 4 base patterns; `methodology_in_progress` collaborators
# exclude joint_venture_aventure (symmetric framing requires equal bench);
# `methodology_naive` collaborators exclude both deep_partner_65_35 (35%
# share requires methodology contribution) AND joint_venture_aventure;
# `methodology_not_applicable` collaborators (one-time BD-only
# introducers; not expected to learn methodology) get the same restriction
# as naive. The matrix prevents committing to share patterns the
# collaborator structurally cannot fulfil.
METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS: dict[str, frozenset[str]] = {
    "methodology_trained": frozenset({
        "deep_partner_65_35",
        "bd_intro_only",
        "joint_venture_aventure",
        "consulting_direct",
    }),
    "methodology_in_progress": frozenset({
        "deep_partner_65_35",
        "bd_intro_only",
        "consulting_direct",
    }),
    "methodology_naive": frozenset({
        "bd_intro_only",
        "consulting_direct",
    }),
    "methodology_not_applicable": frozenset({
        "bd_intro_only",
        "consulting_direct",
    }),
}

DEFAULT_SHARE_PATTERN: str = "deep_partner_65_35"

# Per-pattern default anchors (per the rewritten doctrine §3 worked
# examples). CS-04 audit fires WARN when an authored row deviates from
# the pattern's default anchor without a matching OVERRIDE row.

# deep_partner_65_35 anchor (preserved)
DEFAULT_HOLISTIKA_SHARE_PCT: int = 65
DEFAULT_COLLABORATOR_SHARE_PCT: int = 35

# bd_intro_only anchor (NEW; per doctrine §3.3)
DEFAULT_BD_INTRO_HOLISTIKA_PCT: int = 85
DEFAULT_BD_INTRO_COLLABORATOR_PCT: int = 15

# joint_venture_aventure anchor (NEW; per doctrine §3.4 — symmetric 50/50)
DEFAULT_JOINT_VENTURE_HOLISTIKA_PCT: int = 50
DEFAULT_JOINT_VENTURE_COLLABORATOR_PCT: int = 50

# consulting_direct solo anchor (no overlay sibling; per doctrine §3.2)
DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_SOLO: int = 100
DEFAULT_CONSULTING_DIRECT_COLLABORATOR_PCT_SOLO: int = 0

# consulting_direct WITH bd_commission_overlay sibling anchor (per
# doctrine §3.2 SUEZ corrected example): base row's holistika_share_pct
# drops from 100 to 85; the overlay row covers the residual 15%.
DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_WITH_OVERLAY: int = 85
DEFAULT_BD_COMMISSION_OVERLAY_PCT: int = 15

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
    share_pattern: Literal[
        "deep_partner_65_35",
        "bd_intro_only",
        "joint_venture_aventure",
        "consulting_direct",
    ]
    share_overlay: Literal["bd_commission_overlay", ""] = ""
    holistika_share_pct: int = Field(ge=0, le=100)
    collaborator_share_pct: int = Field(ge=0, le=100)
    collaborator_billed_rate: float = Field(ge=0)
    collaborator_billed_rate_currency: str = Field(
        pattern=r"^[A-Z]{3}$", min_length=3, max_length=3
    )
    collaborator_role_class: str = Field(min_length=1, max_length=120)
    methodology_readiness: Literal[
        "methodology_trained",
        "methodology_in_progress",
        "methodology_naive",
        "methodology_not_applicable",
    ]
    share_override_decision_id: str = ""
    status: Literal[
        "draft", "proposed", "signed", "active", "settled", "archived"
    ]
    signed_at: str = Field(default="", pattern=r"^(\d{4}-\d{2}-\d{2})?$")
    signed_by_collaborator: str = ""
    signed_by_holistika: str = ""
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    notes: str = ""
    # D-IH-86-EK (Wave R+2 Commit 2; post-handshake debrief 2026-05-13 grounding
    # per source-grounding-post-handshake-2026-05-26.md §3 finding F-PI-01):
    # explicit parallel-invoice-stream indicator. When True, the engagement
    # bills the customer via TWO PARALLEL invoice streams (Holistika +
    # collaborator each invoice the end customer directly for their share),
    # rather than the default single-billing-entity pattern (Holistika invoices
    # the customer for 100% and pays the collaborator). Parallel streams
    # materially change the contract shape, VAT treatment, and dispute-
    # resolution surface; the indicator MUST be explicit (never inferred) so
    # downstream settlement + invoicing tooling can branch correctly.
    # Default False = single-billing-entity (the historical default). Optional
    # because pre-rewrite rows do not carry the column; the validator's
    # CSV-header sha check (CS-01) catches the schema drift at Commit 5.
    parallel_invoice_stream_indicator: bool = False


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
    # Added at Wave R+2 Commit 2 per D-IH-86-EJ: when a
    # bd_commission_overlay row deviates from its
    # DEFAULT_BD_COMMISSION_OVERLAY_PCT (15) anchor, the override row
    # carries this kind to make the deviation auditable separately
    # from the base row's share_split_deviation.
    "overlay_pct_deviation",
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
    override_kind: Literal[
        "market_rate_excursion",
        "share_split_deviation",
        "overlay_pct_deviation",
    ]
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
    default 65/35 split for the deep_partner_65_35 share pattern. Per CS-04
    audit: non-default split on a deep_partner_65_35 row requires an
    OVERRIDE row + DECISION_REGISTER FK. CS-04 does NOT fire for
    bd_intro_only / joint_venture_aventure / consulting_direct rows
    (each has its own per-pattern default helper below).
    """
    return (
        holistika_pct == DEFAULT_HOLISTIKA_SHARE_PCT
        and collaborator_pct == DEFAULT_COLLABORATOR_SHARE_PCT
    )


def split_sums_to_100(holistika_pct: int, collaborator_pct: int) -> bool:
    """Return True iff the per-row share splits sum to exactly 100. Per CS-03
    audit: applies row-locally for share_pattern == 'deep_partner_65_35'.
    For 'consulting_direct' WITHOUT overlay, also applies row-locally
    (100/0). For 'bd_intro_only' and 'joint_venture_aventure', the invariant
    applies ACROSS-ROWS for the same engagement_id (see
    ``across_rows_sum_to_100``). For 'consulting_direct' WITH a
    bd_commission_overlay sibling row, the invariant also applies
    across-rows (85+0 + 0+15 == 100).
    """
    return holistika_pct + collaborator_pct == 100


def across_rows_sum_to_100(
    rows_for_engagement: list[tuple[int, int]],
) -> bool:
    """Return True iff the across-rows sum-to-100 invariant holds for a
    multi-row engagement. Per CS-03 across-rows variant: this sum must equal
    exactly 100 for any engagement composed of multiple SHARE_REGISTRY rows
    (bd_intro_only / joint_venture_aventure / consulting_direct+overlay).

    Args:
        rows_for_engagement: List of (holistika_share_pct, collaborator_share_pct)
            tuples, one per registry row + overlay-row sharing the same
            engagement_id.

    Returns:
        True iff (sum(holistika_pcts) + sum(collaborator_pcts)) == 100.
    """
    if not rows_for_engagement:
        return False
    total_holistika = sum(row[0] for row in rows_for_engagement)
    total_collaborator = sum(row[1] for row in rows_for_engagement)
    return (total_holistika + total_collaborator) == 100


def bd_intro_default_split_holds(holistika_pct: int, collaborator_pct: int) -> bool:
    """Return True iff a bd_intro_only row matches the 85/15 default anchor.
    Per CS-04 audit for bd_intro_only: deviation requires an OVERRIDE row.
    """
    return (
        holistika_pct == DEFAULT_BD_INTRO_HOLISTIKA_PCT
        and collaborator_pct == DEFAULT_BD_INTRO_COLLABORATOR_PCT
    )


def joint_venture_default_split_holds(holistika_pct: int, collaborator_pct: int) -> bool:
    """Return True iff a joint_venture_aventure row matches the 50/50 default
    anchor. Per CS-04 audit for joint_venture_aventure: deviation requires
    an OVERRIDE row.
    """
    return (
        holistika_pct == DEFAULT_JOINT_VENTURE_HOLISTIKA_PCT
        and collaborator_pct == DEFAULT_JOINT_VENTURE_COLLABORATOR_PCT
    )


def consulting_direct_solo_default_holds(holistika_pct: int, collaborator_pct: int) -> bool:
    """Return True iff a consulting_direct row WITHOUT an overlay sibling
    matches the 100/0 solo default anchor. Per CS-04 audit for
    consulting_direct (solo): deviation requires an OVERRIDE row.
    """
    return (
        holistika_pct == DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_SOLO
        and collaborator_pct == DEFAULT_CONSULTING_DIRECT_COLLABORATOR_PCT_SOLO
    )


def consulting_direct_with_overlay_default_holds(
    holistika_pct: int, collaborator_pct: int
) -> bool:
    """Return True iff a consulting_direct base row WITH a sibling
    bd_commission_overlay matches the 85/0 anchor. The overlay row carries
    the residual 0/15. Per CS-04 audit for consulting_direct+overlay:
    deviation requires an OVERRIDE row.
    """
    return (
        holistika_pct == DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_WITH_OVERLAY
        and collaborator_pct == 0
    )


def bd_commission_overlay_default_holds(
    holistika_pct: int, collaborator_pct: int
) -> bool:
    """Return True iff a bd_commission_overlay row matches the 0/15 anchor.
    Per CS-04 audit for overlay rows: deviation requires an OVERRIDE row
    with override_kind == 'overlay_pct_deviation'.
    """
    return (
        holistika_pct == 0
        and collaborator_pct == DEFAULT_BD_COMMISSION_OVERLAY_PCT
    )


def share_pattern_is_valid(share_pattern: str) -> bool:
    """Return True iff share_pattern is a recognised enum value per
    VALID_SHARE_PATTERNS. Per CS-08 audit: unknown values fail immediately.
    """
    return share_pattern in VALID_SHARE_PATTERNS


def share_overlay_is_valid(share_overlay: str) -> bool:
    """Return True iff share_overlay is a recognised enum value per
    VALID_SHARE_OVERLAYS, OR the empty string (no overlay declared). Per
    CS-08 audit extension: unknown non-empty values fail immediately.
    """
    return share_overlay == "" or share_overlay in VALID_SHARE_OVERLAYS


def overlay_base_pairing_is_valid(
    share_overlay: str, base_share_patterns: list[str]
) -> bool:
    """Return True iff every base share_pattern in ``base_share_patterns`` is
    a permissible pairing for the declared ``share_overlay``. Used by CS-09
    audit to validate that overlay rows only pair with allowed base
    patterns. Empty overlay or empty base list returns True (no overlay
    means no pairing constraint applies).
    """
    if share_overlay == "":
        return True
    if share_overlay not in VALID_OVERLAY_BASE_PAIRINGS:
        return False
    if not base_share_patterns:
        return False
    permitted = VALID_OVERLAY_BASE_PAIRINGS[share_overlay]
    return all(base in permitted for base in base_share_patterns)


def methodology_readiness_is_valid(methodology_readiness: str) -> bool:
    """Return True iff methodology_readiness is a recognised enum value per
    VALID_METHODOLOGY_READINESS. Used by CS-08 audit extension.
    """
    return methodology_readiness in VALID_METHODOLOGY_READINESS


def methodology_permits_share_pattern(
    methodology_readiness: str, share_pattern: str
) -> bool:
    """Return True iff the collaborator's methodology_readiness state
    structurally permits the engagement's share_pattern per the doctrine
    §2.4 permissibility matrix. The matrix prevents committing to share
    patterns the collaborator cannot fulfil (e.g., a methodology_naive
    collaborator cannot anchor at deep_partner_65_35 because the 35% share
    presumes methodology contribution).
    """
    if methodology_readiness not in METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS:
        return False
    if share_pattern not in VALID_SHARE_PATTERNS:
        return False
    permitted = METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS[methodology_readiness]
    return share_pattern in permitted


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


# =============================================================================
# Audit-report Pydantic models (consumed by validate_collaborator_share.py)
# =============================================================================
# Mirrors the IndexFreshnessRow / IndexFreshnessReport shape from
# akos/hlk_index_integrity.py so the validator + release-gate report surfaces
# stay structurally consistent across Quality Fabric specialties.

VALID_COLLABORATOR_SHARE_CHECK_CODES: frozenset[str] = frozenset({
    "CS-01-STRUCTURAL-VALIDATION",
    "CS-02-CROSS-CSV-FK-RESOLUTION",
    "CS-03-SPLIT-SUMS-TO-100",
    "CS-04-DEFAULT-65-35-AUDIT",
    "CS-05-BILL-MODE-DEFAULT-CONSISTENCY",
    "CS-06-RATE-WITHIN-MARKET-BAND",
    "CS-07-OVERRIDE-EXPIRY-AUDIT",
    # Added at Commit 2b-ext (D-IH-86-DE; extended at Wave R+2 Commit 2
    # per D-IH-86-EJ): validates share_pattern + share_overlay +
    # methodology_readiness enum memberships + applies pattern-conditional
    # logic to CS-03 + CS-04.
    "CS-08-SHARE-PATTERN-ENUM-VALIDITY",
    # Added at Wave R+2 Commit 2 per D-IH-86-EJ: validates overlay-base
    # pairing matrix. Overlay rows must pair with a permitted base
    # share_pattern at the same engagement_id; forbidden pairings
    # (bd_intro_only + bd_commission_overlay; joint_venture_aventure +
    # bd_commission_overlay) produce FAIL findings.
    "CS-09-OVERLAY-BASE-PAIRING-VALIDITY",
})


VALID_AUDIT_VERDICTS: frozenset[str] = frozenset({
    "pass",
    "warn",
    "fail",
    "skip",
})


VALID_AUDIT_SEVERITIES: frozenset[str] = frozenset({
    "low",
    "medium",
    "high",
})


VALID_AUDIT_TRIGGERS: frozenset[str] = frozenset({
    "pre_commit_self_test",
    "csv_mint",
    "wave_close",
    "on_demand",
})


COLLABORATOR_SHARE_AUDIT_ROW_FIELDNAMES: tuple[str, ...] = (
    "check_code",
    "subject_path",
    "subject_row_id",
    "verdict",
    "drift_summary",
    "proposed_fix_action",
    "severity",
    "candidate_decision_id",
    "notes",
)


COLLABORATOR_SHARE_AUDIT_REPORT_FIELDNAMES: tuple[str, ...] = (
    "report_id",
    "audit_trigger",
    "audited_at",
    "audited_by",
    "findings",
    "pass_count",
    "warn_count",
    "fail_count",
    "skip_count",
    "total_findings",
)


class CollaboratorShareAuditRow(BaseModel):
    """One audit finding from a single CS-* check.

    A clean audit emits one ``verdict='pass'`` row per check. A non-clean
    audit emits one row per surfaced issue; each non-clean row becomes one
    triage gate option per the doctrine §5 ramp posture
    (deterministic-fix-now vs ratify-as-canon vs forward-charter).
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    check_code: Literal[
        "CS-01-STRUCTURAL-VALIDATION",
        "CS-02-CROSS-CSV-FK-RESOLUTION",
        "CS-03-SPLIT-SUMS-TO-100",
        "CS-04-DEFAULT-65-35-AUDIT",
        "CS-05-BILL-MODE-DEFAULT-CONSISTENCY",
        "CS-06-RATE-WITHIN-MARKET-BAND",
        "CS-07-OVERRIDE-EXPIRY-AUDIT",
        "CS-08-SHARE-PATTERN-ENUM-VALIDITY",
        "CS-09-OVERLAY-BASE-PAIRING-VALIDITY",
    ]
    subject_path: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description=(
            "Repo-root-relative POSIX path of the CSV this finding concerns "
            "(or a synthetic identifier for cross-CSV findings)."
        ),
    )
    subject_row_id: str = Field(
        default="",
        max_length=128,
        description=(
            "ID of the offending row when applicable (share_id / "
            "vendor_billing_id / clause_id / rate_id / override_id). "
            "Empty for structural / CSV-level findings."
        ),
    )
    verdict: Literal["pass", "warn", "fail", "skip"]
    drift_summary: str = Field(default="", max_length=1024)
    proposed_fix_action: str = Field(default="", max_length=1024)
    severity: Literal["low", "medium", "high"]
    candidate_decision_id: str | None = Field(
        default=None,
        pattern=r"^D-IH-\d+-[A-Z0-9_]+$",
        min_length=8,
        max_length=64,
    )
    notes: str = Field(default="", max_length=2048)


class CollaboratorShareAuditReport(BaseModel):
    """Aggregate report for one 7-check collaborator-share audit run."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    report_id: str = Field(
        ...,
        pattern=r"^collaborator-share-audit-\d{4}-\d{2}-\d{2}(-[a-z0-9]+)?$",
        min_length=29,
        max_length=80,
    )
    audit_trigger: Literal[
        "pre_commit_self_test",
        "csv_mint",
        "wave_close",
        "on_demand",
    ]
    audited_at: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    audited_by: str = Field(..., min_length=1, max_length=128)
    findings: list[CollaboratorShareAuditRow]
    pass_count: int = Field(..., ge=0)
    warn_count: int = Field(..., ge=0)
    fail_count: int = Field(..., ge=0)
    skip_count: int = Field(..., ge=0)
    total_findings: int = Field(..., ge=0)
