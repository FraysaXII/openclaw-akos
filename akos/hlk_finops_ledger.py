"""FINOPS ledger SSOT — Pydantic chassis for finops.registered_fact + counterparty resolution + FX snapshot.

Initiative 81 Phase 2 Bundle B-2a (D-IH-81-V under D-IH-81-G umbrella, 2026-05-23).
Operator inline-ratify ratification 2026-05-23 (R1-a + R2-a + R3-a + R4-a + R5-triple per Bundle B-2 architecture report).

This module is the canonical Python contract for:

1. **RegisteredFactRow** — Pydantic frozen BaseModel mirroring the finops.registered_fact table shape
   (extended at B-2a with fx_rate_ecb + fx_rate_stripe + fx_source + amount_minor_eur columns).
2. **CounterpartyResolutionStrategy** — enum of routing strategies the writer uses to map Stripe customer
   ids (or other event sources) to FINOPS_COUNTERPARTY_REGISTER.counterparty_id. Strategy is selected
   per ENGAGEMENT_MODEL_REGISTRY.engagement_model_id (per Recommendation 1 in architecture report).
3. **resolve_counterparty_id()** — function that runs the routing logic + emits OPS_REGISTER row when
   resolution fails (per Recommendation 4 HLK-ERP convergence).
4. **compute_fx_snapshot()** — function that produces an FxSnapshot named tuple for a (currency, amount_minor,
   effective_date) triple, applying the ECB-authoritative ladder (per Recommendation 2).

The actual database write path lives in Edge Function ``finops-writer-worker`` (Bundle B-2b); this module
provides the Python-side SSOT that the worker mirrors in TypeScript + the validator (validate_finops_ledger.py)
exercises against synthetic fact streams.

Design rationale (D-IH-81-V):
- **Pydantic SSOT in akos/hlk_finops_ledger.py** (per R5 location ratification d1-finops-ledger):
  Pairs naturally with hlk_finops_counterparty_csv.py (counterparty SSOT) and hlk_engagement_model_csv.py
  (engagement model SSOT). The Edge Function (TypeScript) mirrors this contract; drift between Python and
  TypeScript types surfaces as test failures in B-2b worker tests.
- **CounterpartyResolutionStrategy enum lives here** (not in hlk_engagement_model_csv.py) because the
  resolution logic is a FINOPS concern; the ENGAGEMENT_MODEL_REGISTRY row carries the strategy *name*
  but the routing logic + fallback chain lives in this module.
- **FX snapshot via separate compute function** (not a Pydantic validator) because the FX cache lookup
  requires a database round-trip in production but a frozen lookup table in tests; separating the function
  enables clean mocking.

Decision lineage:
- D-IH-81-V (Bundle B-2a substrate; this module's mint)
- D-IH-81-G umbrella (I81 P2 layout-migration + monetary-substrate sweep)
- D-IH-81-Q (T1 FINOPS layout move; this module joins the finops/ family conceptually)
- D-IH-81-P (internal-first FINOPS posture; constrains scope to existing engagement models + bootstrapped patterns)
- D-IH-89-L (AT-Pymes Layer (a) gestoria; first downstream consumer once B-2c lands)

See ``docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/p2-bundle-b2-architecture-2026-05-23.md``
for the full architecture rationale + §5 file inventory + §6 ratify batch.

See ``supabase/migrations/20260524000000_i81_p2_b2_finops_writer_substrate.sql`` for the canonical DDL
this module mirrors.
"""

from __future__ import annotations

from typing import Literal, NamedTuple

from pydantic import BaseModel, ConfigDict, Field


# =============================================================================
# §1 — Column tuple (mirrors finops.registered_fact post-B-2a ALTER TABLE)
# =============================================================================

# Keep in sync with finops.registered_fact (post-B-2a extension at
# supabase/migrations/20260524000000_i81_p2_b2_finops_writer_substrate.sql §4).
# 14 columns: 10 from I19 Phase 1 + 4 added at B-2a (amount_minor_eur + fx_rate_ecb + fx_rate_stripe + fx_source).
REGISTERED_FACT_FIELDNAMES: tuple[str, ...] = (
    "id",                       # UUID primary key (server-side default)
    "counterparty_id",          # FK-by-convention to FINOPS_COUNTERPARTY_REGISTER.counterparty_id slug
    "stripe_customer_id",       # Stripe customer id (nullable; present for Stripe-origin facts)
    "stripe_subscription_id",   # Stripe subscription id (nullable)
    "fact_type",                # discriminator: reconciliation_snapshot | budget_line | contract_value_estimate | charge_succeeded | invoice_paid | subscription_event
    "currency",                 # ISO 4217 (default 'USD' per I19 schema; B-2 routes both USD and EUR)
    "amount_minor",             # BIGINT in source currency minor units (cents); nullable for non-amount facts
    "amount_minor_eur",         # BIGINT in EUR minor units (cents); computed via fx_rate_ecb; nullable for non-amount facts
    "effective_date",           # DATE this fact is authoritative for (drives fx_rate_ecb lookup)
    "fx_rate_ecb",              # NUMERIC(18,8) ECB daily rate at effective_date (NULL for EUR-native facts)
    "fx_rate_stripe",           # NUMERIC(18,8) Stripe FX Quote at effective_date (audit sidecar; NULL when not applicable)
    "fx_source",                # provenance enum (see VALID_FX_SOURCES)
    "metadata",                 # JSONB free-form metadata
    "source_reference",         # human-readable pointer (e.g. 'stripe_event:evt_xxx' or 'contract_doc:.../foo.pdf')
)


# =============================================================================
# §2 — Frozensets for governed enums (mirror DB CHECK semantics + drive tests)
# =============================================================================

VALID_FACT_TYPES: frozenset[str] = frozenset({
    # I19 Phase 1 originals (operator-recorded):
    "reconciliation_snapshot",
    "budget_line",
    "contract_value_estimate",
    # B-2 Stripe-origin (system-recorded via finops-writer-worker):
    "charge_succeeded",
    "charge_refunded",
    "invoice_paid",
    "invoice_payment_failed",
    "subscription_created",
    "subscription_updated",
    "subscription_canceled",
    # B-2c will extend per engagement model (e.g. revenue_share_payout for percentage_collaborator).
})


VALID_FX_SOURCES: frozenset[str] = frozenset({
    "ecb_daily",                    # normal path: ECB cache hit on effective_date
    "ecb_previous_day_fallback",    # ECB cache miss on effective_date; used yesterday's rate (Tier-2 ladder)
    "stripe_fx_quote",              # ECB cache stale > 2 days; fell back to Stripe FX Quote API (Tier-3 ladder)
    "manual_override",              # operator-set via runbook; emits OPS_REGISTER alert
    "identity_eur",                 # currency == 'EUR'; no conversion needed
})


VALID_RESOLUTION_STRATEGIES: frozenset[str] = frozenset({
    # Per R1 (engagement-model-aware router) — see Bundle B-2 architecture report §3.1:
    "metadata_engagement_id",       # Stripe metadata.hlk_engagement_id → counterparty_id (highest confidence)
    "metadata_billing_plane",       # Stripe metadata.hlk_billing_plane → counterparty_id (medium confidence; SaaS path)
    "stripe_customer_link_lookup",  # JOIN holistika_ops.stripe_customer_link by stripe_customer_id (existing pattern; I14)
    "rpp_payout_attribution",       # B-2c forward-charter: Revenue Pass-Through vendor payout attribution
    "manual_review",                # No strategy matched → OPS_REGISTER row + finops.registered_fact written with counterparty_id='UNRESOLVED'
})


VALID_CURRENCY_CODES: frozenset[str] = frozenset({
    # ISO 4217 — restricted to currencies Holistika actually transacts in (per FINOPS internal-first
    # posture D-IH-81-P; extend as engagement footprint grows).
    "EUR", "USD", "GBP", "CHF",
})


# =============================================================================
# §3 — Pydantic frozen BaseModel for one finops.registered_fact row
# =============================================================================


class RegisteredFactRow(BaseModel):
    """Pydantic frozen BaseModel for one finops.registered_fact row (post-B-2a column extension).

    Per ``CONTRIBUTING.md`` "Python Code Standards" and
    ``akos-holistika-operations.mdc`` "New git-canonical compliance registers":
    frozen BaseModel + Literal enums for governed columns + length bounds + slug regex on
    counterparty_id (matches FINOPS_COUNTERPARTY_REGISTER.csv slug pattern).

    Used by:
    - ``scripts/validate_finops_ledger.py`` (validator exercising synthetic fact streams)
    - ``tests/test_validate_finops_ledger.py`` (FK resolution + enum + round-trip JSON tests)
    - ``akos/hlk_fx_rate.py`` (cross-reference for fx_source enum)
    - Edge Function ``finops-writer-worker`` (TypeScript mirror; type drift surfaces as test failure)
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    counterparty_id: str = Field(
        ...,
        pattern=r"^[a-z0-9_]+$|^UNRESOLVED$",
        min_length=2,
        max_length=64,
        description=(
            "FK-by-convention to FINOPS_COUNTERPARTY_REGISTER.csv counterparty_id slug; "
            "'UNRESOLVED' sentinel allowed for facts written before counterparty resolution completes "
            "(triggers OPS_REGISTER row for operator review per R4 HLK-ERP convergence)."
        ),
    )
    stripe_customer_id: str | None = Field(
        None,
        max_length=64,
        description="Stripe customer id (cus_xxx); nullable for non-Stripe facts.",
    )
    stripe_subscription_id: str | None = Field(
        None,
        max_length=64,
        description="Stripe subscription id (sub_xxx); nullable for one-off charges + non-Stripe facts.",
    )
    fact_type: Literal[
        "reconciliation_snapshot",
        "budget_line",
        "contract_value_estimate",
        "charge_succeeded",
        "charge_refunded",
        "invoice_paid",
        "invoice_payment_failed",
        "subscription_created",
        "subscription_updated",
        "subscription_canceled",
    ]
    currency: Literal["EUR", "USD", "GBP", "CHF"] = Field(
        "EUR",
        description="ISO 4217 currency code. Restricted to currencies Holistika actually transacts in per D-IH-81-P internal-first scope.",
    )
    amount_minor: int | None = Field(
        None,
        ge=0,
        description="Source-currency minor units (cents). NULL for non-amount metadata facts.",
    )
    amount_minor_eur: int | None = Field(
        None,
        ge=0,
        description="EUR-equivalent minor units computed via fx_rate_ecb at effective_date. NULL when amount_minor is NULL OR when currency='EUR' (use amount_minor directly).",
    )
    effective_date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="ISO date YYYY-MM-DD; drives fx_rate_ecb lookup in holistika_ops.fx_rate_cache.",
    )
    fx_rate_ecb: str | None = Field(
        None,
        description="ECB daily rate at effective_date as decimal string (e.g. '0.92500000'). NULL for currency='EUR'. Stored as string to avoid float drift.",
    )
    fx_rate_stripe: str | None = Field(
        None,
        description="Stripe FX Quote API rate at effective_date (audit sidecar). NULL when not applicable.",
    )
    fx_source: Literal[
        "ecb_daily",
        "ecb_previous_day_fallback",
        "stripe_fx_quote",
        "manual_override",
        "identity_eur",
    ] = Field(
        "identity_eur",
        description="Provenance of fx_rate_ecb. 'identity_eur' when currency='EUR'.",
    )
    metadata: dict = Field(default_factory=dict)
    source_reference: str = Field(
        ...,
        min_length=1,
        max_length=480,
        description="Human-readable pointer to fact origin (e.g. 'stripe_event:evt_xxx' or 'contract_doc:./foo.pdf').",
    )


# =============================================================================
# §4 — Counterparty resolution (R1 engagement-model-aware router)
# =============================================================================


class CounterpartyResolutionResult(NamedTuple):
    """Result of resolving a Stripe-origin (or other-origin) event to a FINOPS counterparty_id.

    - ``counterparty_id`` is the resolved slug, OR the sentinel ``'UNRESOLVED'`` if no strategy matched.
    - ``strategy_used`` records which strategy in VALID_RESOLUTION_STRATEGIES produced the resolution.
    - ``confidence`` is one of 'high' / 'medium' / 'low' / 'unresolved' (drives OPS_REGISTER row severity).
    - ``ops_register_payload`` is non-None when resolution failed OR confidence='low'; caller emits to compliance.ops_register_mirror.
    """

    counterparty_id: str
    strategy_used: str
    confidence: Literal["high", "medium", "low", "unresolved"]
    ops_register_payload: dict | None


def resolve_counterparty_id(
    stripe_customer_id: str | None,
    stripe_metadata: dict | None,
    engagement_model_id: str | None = None,
) -> CounterpartyResolutionResult:
    """Resolve a Stripe event source to a FINOPS counterparty_id slug using the R1 engagement-model-aware router.

    Resolution ladder (highest confidence first):

    1. **metadata_engagement_id**: ``stripe_metadata['hlk_engagement_id']`` directly maps to counterparty_id
       (highest confidence; recommended pattern for B-2c forward).
    2. **metadata_billing_plane**: ``stripe_metadata['hlk_billing_plane']`` (e.g. 'holistika' / 'kirbe' /
       '<counterparty_slug>') routes to the corresponding counterparty (medium confidence; existing I14
       pattern). When 'kirbe' or 'holistika' — sentinel non-counterparty values, fall through.
    3. **stripe_customer_link_lookup**: in production, the worker JOINs holistika_ops.stripe_customer_link
       by stripe_customer_id to find finops_counterparty_id. This Python stub returns UNRESOLVED with the
       lookup recommendation; the actual SQL lookup runs in the Edge Function (B-2b worker).
    4. **manual_review fallback**: no strategy matched → return UNRESOLVED + ops_register_payload for
       operator review.

    Per R1 (engagement-model-aware router) — see Bundle B-2 architecture report §3.1 + R4 (HLK-ERP
    convergence) for the OPS_REGISTER emission policy. The actual finops_counterparty_id column on
    holistika_ops.stripe_customer_link was added at I81 P2 T1 via ALTER TABLE IF NOT EXISTS.

    Args:
        stripe_customer_id: Stripe customer id (cus_xxx) or None.
        stripe_metadata: full Stripe ``metadata`` dict from the event payload (or None).
        engagement_model_id: optional override for testing; in production the worker derives this from
            stripe_metadata or from the holistika_ops.stripe_customer_link.engagement_model_id column.

    Returns:
        CounterpartyResolutionResult with the resolution outcome.
    """

    stripe_metadata = stripe_metadata or {}

    # Strategy 1: direct engagement_id metadata (highest confidence)
    if "hlk_engagement_id" in stripe_metadata:
        engagement_id = str(stripe_metadata["hlk_engagement_id"]).strip().lower()
        if engagement_id and engagement_id.replace("_", "").replace("-", "").isalnum():
            return CounterpartyResolutionResult(
                counterparty_id=engagement_id,
                strategy_used="metadata_engagement_id",
                confidence="high",
                ops_register_payload=None,
            )

    # Strategy 2: billing_plane routing (medium confidence; legacy I14 pattern)
    billing_plane = stripe_metadata.get("hlk_billing_plane", "").strip().lower()
    if billing_plane and billing_plane not in {"holistika", "kirbe", ""}:
        # billing_plane carries a counterparty slug directly (e.g. 'rcdlegal_2024_engagement_001')
        if billing_plane.replace("_", "").replace("-", "").isalnum():
            return CounterpartyResolutionResult(
                counterparty_id=billing_plane,
                strategy_used="metadata_billing_plane",
                confidence="medium",
                ops_register_payload=None,
            )

    # Strategy 3: stripe_customer_link lookup (recommendation; actual SQL in Edge Function)
    # In Python (this function), we surface the lookup recommendation; the Edge Function
    # finops-writer-worker performs the actual SELECT.
    if stripe_customer_id and stripe_customer_id.startswith("cus_"):
        # Return UNRESOLVED with the lookup hint; the worker will retry after DB lookup.
        return CounterpartyResolutionResult(
            counterparty_id="UNRESOLVED",
            strategy_used="stripe_customer_link_lookup",
            confidence="low",
            ops_register_payload={
                "ops_class": "stripe_customer_link_lookup_pending",
                "stripe_customer_id": stripe_customer_id,
                "hint": "Run SELECT finops_counterparty_id FROM holistika_ops.stripe_customer_link WHERE stripe_customer_id = $1 in worker.",
                "severity": "info",
            },
        )

    # Strategy 4: manual_review fallback (no strategy matched)
    return CounterpartyResolutionResult(
        counterparty_id="UNRESOLVED",
        strategy_used="manual_review",
        confidence="unresolved",
        ops_register_payload={
            "ops_class": "counterparty_resolution_failed",
            "stripe_customer_id": stripe_customer_id,
            "stripe_metadata_keys": sorted(stripe_metadata.keys()) if stripe_metadata else [],
            "engagement_model_id_hint": engagement_model_id,
            "severity": "high",
            "operator_action": "Add hlk_engagement_id or hlk_billing_plane to Stripe customer metadata; OR add row to holistika_ops.stripe_customer_link with finops_counterparty_id set.",
        },
    )


# =============================================================================
# §5 — FX snapshot (R2 ECB-authoritative ladder)
# =============================================================================


class FxSnapshot(NamedTuple):
    """Result of computing the FX rate snapshot for a (currency, effective_date) pair.

    All rates returned as strings (decimal preserved) to avoid float drift on round-trip to/from
    the database. Caller converts to Decimal for arithmetic when needed.
    """

    fx_rate_ecb: str | None              # decimal string e.g. '0.92500000'; None if currency='EUR'
    fx_rate_stripe: str | None           # decimal string from Stripe FX Quote API; None if not fetched
    fx_source: str                       # one of VALID_FX_SOURCES
    amount_minor_eur: int | None         # computed EUR minor units; None if amount_minor is None


def compute_fx_snapshot(
    amount_minor: int | None,
    currency: str,
    effective_date: str,
    ecb_rate_lookup: dict[tuple[str, str], str] | None = None,
    stripe_fx_quote: str | None = None,
) -> FxSnapshot:
    """Compute the FX snapshot for a fact's (currency, amount_minor, effective_date) triple.

    Per R2 (ECB-authoritative + Stripe FX Quote sidecar) — see Bundle B-2 architecture report §3.2.

    Fallback ladder:
    1. **identity_eur**: currency == 'EUR' → return amount unchanged with fx_source='identity_eur'.
    2. **ecb_daily**: lookup (currency_pair, effective_date) in ecb_rate_lookup → compute EUR + return.
    3. **ecb_previous_day_fallback**: lookup (currency_pair, effective_date - 1) → use yesterday's rate +
       emit OPS_REGISTER row (caller responsibility; signaled via fx_source).
    4. **stripe_fx_quote**: ECB > 2 days stale → fall back to provided stripe_fx_quote + emit OPS_REGISTER.
    5. **manual_override** is operator-set via runbook (not produced by this function); shows up via
       direct insert + OPS_REGISTER row.

    Args:
        amount_minor: source-currency minor units (cents). NULL passes through unchanged.
        currency: ISO 4217 code (must be in VALID_CURRENCY_CODES).
        effective_date: ISO date YYYY-MM-DD.
        ecb_rate_lookup: optional dict for testing/preloaded cache. In production the worker queries
            holistika_ops.fx_rate_cache directly; tests provide a frozen lookup table.
        stripe_fx_quote: optional pre-fetched Stripe FX Quote rate as decimal string.

    Returns:
        FxSnapshot with computed fields.
    """

    if amount_minor is None:
        return FxSnapshot(None, None, "identity_eur", None)

    if currency == "EUR":
        return FxSnapshot(None, stripe_fx_quote, "identity_eur", amount_minor)

    currency_pair = f"{currency}/EUR"
    lookup = ecb_rate_lookup or {}

    # Tier 1: ecb_daily (exact effective_date hit)
    if (currency_pair, effective_date) in lookup:
        rate_str = lookup[(currency_pair, effective_date)]
        amount_eur = int(round(amount_minor * float(rate_str)))
        return FxSnapshot(rate_str, stripe_fx_quote, "ecb_daily", amount_eur)

    # Tier 2: ecb_previous_day_fallback (try yesterday)
    from datetime import datetime, timedelta
    try:
        eff = datetime.strptime(effective_date, "%Y-%m-%d").date()
        prev = (eff - timedelta(days=1)).strftime("%Y-%m-%d")
        if (currency_pair, prev) in lookup:
            rate_str = lookup[(currency_pair, prev)]
            amount_eur = int(round(amount_minor * float(rate_str)))
            return FxSnapshot(rate_str, stripe_fx_quote, "ecb_previous_day_fallback", amount_eur)
    except ValueError:
        pass

    # Tier 3: stripe_fx_quote (ECB cache fully stale; use Stripe's quote)
    if stripe_fx_quote:
        amount_eur = int(round(amount_minor * float(stripe_fx_quote)))
        return FxSnapshot(None, stripe_fx_quote, "stripe_fx_quote", amount_eur)

    # No fallback available — caller decides whether to write UNRESOLVED or raise
    return FxSnapshot(None, None, "manual_override", None)


# =============================================================================
# §6 — CSV path constant (mirror governance lookup; not currently consumed by validator)
# =============================================================================
# finops.registered_fact has no CSV SSOT (it's an operational table, not a git-canonical CSV).
# This constant is kept for cross-reference symmetry with sibling modules.
DDL_PATH_RELATIVE: str = (
    "supabase/migrations/20260524000000_i81_p2_b2_finops_writer_substrate.sql"
)
