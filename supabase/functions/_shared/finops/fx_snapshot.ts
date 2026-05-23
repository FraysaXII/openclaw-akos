/**
 * FX snapshot — TypeScript mirror of compute_fx_snapshot() in akos/hlk_finops_ledger.py §5.
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W, 2026-05-23).
 *
 * R2 (ECB-authoritative + Stripe FX Quote sidecar) — see Bundle B-2 architecture report §3.2.
 *
 * Fallback ladder (highest authority first):
 *   1. identity_eur                — currency='EUR' → no conversion needed.
 *   2. ecb_daily                   — holistika_ops.fx_rate_cache hit on (currency_pair, effective_date).
 *   3. ecb_previous_day_fallback   — hit on (currency_pair, effective_date - 1d). Emits FX_CACHE_STALE OPS row.
 *   4. stripe_fx_quote             — ECB cache >1d stale; fall back to caller-provided Stripe Quote rate.
 *                                    Emits FX_CACHE_STALE + FX_DIVERGENCE OPS rows (if both rates present).
 *   5. (return manual_override)    — no path available; caller decides to write UNRESOLVED or raise.
 *
 * Divergence policy (per architecture report §3.2 R3 risk):
 *   When fx_rate_ecb AND fx_rate_stripe are both available, the worker compares them post-snapshot
 *   and emits FX_DIVERGENCE_THRESHOLD_EXCEEDED OPS row when |ecb - stripe| / ecb > 0.5% (5e-3).
 *   That divergence-check is in the worker (finops-writer-worker/index.ts), not in this function,
 *   because the function returns the snapshot and the worker owns the OPS emit decision.
 */

import type { SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";
import {
  type CurrencyCode,
  fxCurrencyPair,
  type FxSnapshot,
} from "./types.ts";

export const FX_DIVERGENCE_THRESHOLD_RATIO = 0.005; // 0.5%

/**
 * In-memory cache for tests (production worker uses SupabaseClient directly).
 * Key: `${currency_pair}|${effective_date}`. Value: decimal rate string.
 */
export type FxRateLookup = Map<string, string>;

export function fxLookupKey(currencyPair: string, effectiveDate: string): string {
  return `${currencyPair}|${effectiveDate}`;
}

/**
 * Compute one day prior in ISO YYYY-MM-DD.
 */
function previousDay(effectiveDate: string): string {
  // Parse as UTC noon to avoid TZ off-by-one on prior-day computation.
  const d = new Date(`${effectiveDate}T12:00:00Z`);
  if (Number.isNaN(d.getTime())) {
    throw new Error(`fxSnapshot: invalid effective_date '${effectiveDate}'`);
  }
  d.setUTCDate(d.getUTCDate() - 1);
  return d.toISOString().slice(0, 10);
}

function computeEurMinor(amountMinor: number, rateStr: string): number {
  const rate = Number(rateStr);
  if (!Number.isFinite(rate) || rate <= 0) {
    throw new Error(`fxSnapshot: invalid rate '${rateStr}'`);
  }
  return Math.round(amountMinor * rate);
}

// =============================================================================
// §1 — Pure function (in-memory lookup; used by tests + worker after preload)
// =============================================================================

/**
 * Pure-function form: caller pre-loads ECB lookup into a Map; this fn applies the ladder.
 * Mirrors akos/hlk_finops_ledger.compute_fx_snapshot() exactly.
 */
export function computeFxSnapshotFromLookup(
  amountMinor: number | null,
  currency: CurrencyCode,
  effectiveDate: string,
  lookup: FxRateLookup,
  stripeFxQuote: string | null = null,
): FxSnapshot {
  if (amountMinor === null || amountMinor === undefined) {
    return { fx_rate_ecb: null, fx_rate_stripe: null, fx_source: "identity_eur", amount_minor_eur: null };
  }

  // Tier 0: identity_eur — no conversion needed.
  if (currency === "EUR") {
    return {
      fx_rate_ecb: null,
      fx_rate_stripe: stripeFxQuote,
      fx_source: "identity_eur",
      amount_minor_eur: amountMinor,
    };
  }

  const pair = fxCurrencyPair(currency);

  // Tier 1: ecb_daily exact hit
  const todayKey = fxLookupKey(pair, effectiveDate);
  const todayRate = lookup.get(todayKey);
  if (todayRate) {
    return {
      fx_rate_ecb: todayRate,
      fx_rate_stripe: stripeFxQuote,
      fx_source: "ecb_daily",
      amount_minor_eur: computeEurMinor(amountMinor, todayRate),
    };
  }

  // Tier 2: ecb_previous_day_fallback
  try {
    const prevDate = previousDay(effectiveDate);
    const prevKey = fxLookupKey(pair, prevDate);
    const prevRate = lookup.get(prevKey);
    if (prevRate) {
      return {
        fx_rate_ecb: prevRate,
        fx_rate_stripe: stripeFxQuote,
        fx_source: "ecb_previous_day_fallback",
        amount_minor_eur: computeEurMinor(amountMinor, prevRate),
      };
    }
  } catch {
    /* fall through to Tier 3 */
  }

  // Tier 3: stripe_fx_quote (caller-provided)
  if (stripeFxQuote) {
    return {
      fx_rate_ecb: null,
      fx_rate_stripe: stripeFxQuote,
      fx_source: "stripe_fx_quote",
      amount_minor_eur: computeEurMinor(amountMinor, stripeFxQuote),
    };
  }

  // Tier 4: no path — manual_override (caller emits OPS row)
  return { fx_rate_ecb: null, fx_rate_stripe: null, fx_source: "manual_override", amount_minor_eur: null };
}

// =============================================================================
// §2 — Production form (Supabase-backed; queries holistika_ops.fx_rate_cache)
// =============================================================================

/**
 * Production form: queries holistika_ops.fx_rate_cache directly. Used by the worker.
 * Fetches both today + yesterday in a single round-trip (2 keys per worker call is fine).
 */
export async function computeFxSnapshotFromDb(
  supabase: SupabaseClient,
  amountMinor: number | null,
  currency: CurrencyCode,
  effectiveDate: string,
  stripeFxQuote: string | null = null,
): Promise<FxSnapshot> {
  if (amountMinor === null || currency === "EUR") {
    return computeFxSnapshotFromLookup(amountMinor, currency, effectiveDate, new Map(), stripeFxQuote);
  }

  const pair = fxCurrencyPair(currency);
  let prevDate: string;
  try {
    prevDate = previousDay(effectiveDate);
  } catch {
    return computeFxSnapshotFromLookup(amountMinor, currency, effectiveDate, new Map(), stripeFxQuote);
  }

  const { data, error } = await supabase
    .from("fx_rate_cache")
    .select("currency_pair, effective_date, rate")
    .eq("currency_pair", pair)
    .in("effective_date", [effectiveDate, prevDate]);

  if (error) {
    console.warn(
      JSON.stringify({
        source: "fx_snapshot",
        note: "fx_rate_cache lookup failed; falling back to stripe_fx_quote or manual_override",
        currency_pair: pair,
        error: error.message,
      }),
    );
    // Build empty lookup; pure fn will fall through to stripe_fx_quote or manual_override.
    return computeFxSnapshotFromLookup(amountMinor, currency, effectiveDate, new Map(), stripeFxQuote);
  }

  const lookup: FxRateLookup = new Map();
  for (const row of data ?? []) {
    if (row.rate != null) {
      lookup.set(fxLookupKey(row.currency_pair, row.effective_date), String(row.rate));
    }
  }
  return computeFxSnapshotFromLookup(amountMinor, currency, effectiveDate, lookup, stripeFxQuote);
}

// =============================================================================
// §3 — Divergence check (used by worker post-snapshot)
// =============================================================================

/**
 * Returns true when |ecb - stripe| / ecb exceeds FX_DIVERGENCE_THRESHOLD_RATIO.
 * Both inputs must be valid decimal strings; returns false if either is missing or invalid.
 */
export function fxRatesDiverge(ecbRate: string | null, stripeRate: string | null): boolean {
  if (!ecbRate || !stripeRate) return false;
  const ecb = Number(ecbRate);
  const stripe = Number(stripeRate);
  if (!Number.isFinite(ecb) || !Number.isFinite(stripe) || ecb <= 0) return false;
  return Math.abs(ecb - stripe) / ecb > FX_DIVERGENCE_THRESHOLD_RATIO;
}
