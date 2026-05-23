/**
 * FINOPS writer types — TypeScript mirror of akos/hlk_finops_ledger.py.
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W under D-IH-81-G umbrella, 2026-05-23).
 *
 * **Python is SSOT** (akos/hlk_finops_ledger.py); this file is the runtime-layer mirror that
 * Edge Functions consume. Drift between Python and TypeScript surfaces as Deno test failures
 * in test_counterparty_resolver.ts + test_fx_snapshot.ts + the worker round-trip test.
 *
 * See:
 * - supabase/migrations/20260524000000_i81_p2_b2_finops_writer_substrate.sql (canonical DDL)
 * - akos/hlk_finops_ledger.py §3 RegisteredFactRow (Pydantic SSOT)
 * - docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/p2-bundle-b2-architecture-2026-05-23.md §3
 */

// =============================================================================
// §1 — Enum literal unions (mirror Python Literal[...] frozensets)
// =============================================================================

export type FactType =
  | "reconciliation_snapshot"
  | "budget_line"
  | "contract_value_estimate"
  | "charge_succeeded"
  | "charge_refunded"
  | "invoice_paid"
  | "invoice_payment_failed"
  | "subscription_created"
  | "subscription_updated"
  | "subscription_canceled";

export type CurrencyCode = "EUR" | "USD" | "GBP" | "CHF";

export type FxSource =
  | "ecb_daily"
  | "ecb_previous_day_fallback"
  | "stripe_fx_quote"
  | "manual_override"
  | "identity_eur";

export type ResolutionStrategy =
  | "metadata_engagement_id"
  | "metadata_billing_plane"
  | "stripe_customer_link_lookup"
  | "rpp_payout_attribution"
  | "manual_review";

export type ResolutionConfidence = "high" | "medium" | "low" | "unresolved";

export type OpsOwnerClass = "operator" | "system" | "agent" | "shared";

export type OpsStatus = "open" | "in_progress" | "blocked" | "closed" | "cancelled";

// FINOPS-writer-specific ops_class subset (full catalog in OPS_REGISTER.csv).
export type FinopsOpsClass =
  | "counterparty_resolution_failed"
  | "stripe_customer_link_lookup_pending"
  | "fx_divergence_threshold_exceeded"
  | "fx_cache_stale"
  | "dlq_threshold_exceeded"
  | "dlq_event_max_retries"
  | "stripe_webhook_signature_mismatch"
  | "stripe_metadata_missing";

// =============================================================================
// §2 — Frozen enum-as-Set for runtime validation (mirrors Python frozensets)
// =============================================================================

export const VALID_FACT_TYPES: ReadonlySet<FactType> = new Set<FactType>([
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
]);

export const VALID_CURRENCY_CODES: ReadonlySet<CurrencyCode> = new Set<CurrencyCode>([
  "EUR",
  "USD",
  "GBP",
  "CHF",
]);

export const VALID_FX_SOURCES: ReadonlySet<FxSource> = new Set<FxSource>([
  "ecb_daily",
  "ecb_previous_day_fallback",
  "stripe_fx_quote",
  "manual_override",
  "identity_eur",
]);

export const VALID_RESOLUTION_STRATEGIES: ReadonlySet<ResolutionStrategy> = new Set<ResolutionStrategy>([
  "metadata_engagement_id",
  "metadata_billing_plane",
  "stripe_customer_link_lookup",
  "rpp_payout_attribution",
  "manual_review",
]);

// =============================================================================
// §3 — Row shape for finops.registered_fact (post-B-2a column extension)
// =============================================================================

/**
 * Mirror of RegisteredFactRow in akos/hlk_finops_ledger.py §3.
 * 14 columns (10 from I19 Phase 1 + 4 added at B-2a).
 *
 * Note: id is server-generated UUID; not provided on insert.
 * stripe_customer_id + stripe_subscription_id + amount_minor + amount_minor_eur + fx_rate_*
 * are nullable per the schema.
 */
export interface RegisteredFactRow {
  counterparty_id: string; // FK-by-convention to FINOPS_COUNTERPARTY_REGISTER.csv slug or 'UNRESOLVED'
  stripe_customer_id: string | null;
  stripe_subscription_id: string | null;
  fact_type: FactType;
  currency: CurrencyCode;
  amount_minor: number | null; // BIGINT in source minor units (cents)
  amount_minor_eur: number | null; // BIGINT in EUR minor units
  effective_date: string; // ISO YYYY-MM-DD
  fx_rate_ecb: string | null; // decimal string to avoid float drift
  fx_rate_stripe: string | null;
  fx_source: FxSource;
  metadata: Record<string, unknown>;
  source_reference: string;
}

// =============================================================================
// §4 — Counterparty resolution result (mirror Python CounterpartyResolutionResult NamedTuple)
// =============================================================================

export interface CounterpartyResolutionResult {
  counterparty_id: string; // resolved slug OR 'UNRESOLVED' sentinel
  strategy_used: ResolutionStrategy;
  confidence: ResolutionConfidence;
  ops_register_payload: OpsRegisterEmitPayload | null;
}

// =============================================================================
// §5 — FX snapshot result (mirror Python FxSnapshot NamedTuple)
// =============================================================================

export interface FxSnapshot {
  fx_rate_ecb: string | null;
  fx_rate_stripe: string | null;
  fx_source: FxSource;
  amount_minor_eur: number | null;
}

// =============================================================================
// §6 — OPS_REGISTER emit payload (R4 HLK-ERP convergence)
// =============================================================================

/**
 * Shape the worker passes to ops_register_emit.ts when surfacing operator actions.
 * The emit helper builds a 24-column OPS_REGISTER row from this payload + writes it
 * to compliance.ops_register_mirror via service_role.
 */
export interface OpsRegisterEmitPayload {
  ops_class: FinopsOpsClass;
  title?: string; // human-readable; auto-derived from ops_class if absent
  summary: string;
  severity: "info" | "low" | "medium" | "high" | "critical";
  evidence_path?: string;
  stripe_event_id?: string; // when emit is triggered by a webhook event
  stripe_customer_id?: string | null;
  metadata?: Record<string, unknown>;
}

// =============================================================================
// §7 — Sentinel constants
// =============================================================================

export const COUNTERPARTY_UNRESOLVED = "UNRESOLVED" as const;

// FX cache currency-pair format: SRC/EUR (always source-to-base = source currency to EUR).
export function fxCurrencyPair(currency: CurrencyCode): string {
  return `${currency}/EUR`;
}
