/**
 * Deno tests — fx_snapshot.ts (R2 ECB-authoritative ladder).
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W, 2026-05-23).
 *
 * Run: deno test --allow-env supabase/functions/_shared/finops/test_fx_snapshot.ts
 */

import { assertEquals } from "https://deno.land/std@0.224.0/assert/mod.ts";
import {
  computeFxSnapshotFromLookup,
  FX_DIVERGENCE_THRESHOLD_RATIO,
  type FxRateLookup,
  fxLookupKey,
  fxRatesDiverge,
} from "./fx_snapshot.ts";

function makeLookup(entries: Array<[string, string, string]>): FxRateLookup {
  const m: FxRateLookup = new Map();
  for (const [pair, date, rate] of entries) m.set(fxLookupKey(pair, date), rate);
  return m;
}

// -----------------------------------------------------------------------------
// Tier 0 — identity_eur
// -----------------------------------------------------------------------------
Deno.test("Tier 0 — EUR currency returns identity_eur snapshot", () => {
  const snap = computeFxSnapshotFromLookup(1000, "EUR", "2026-05-23", new Map());
  assertEquals(snap.fx_source, "identity_eur");
  assertEquals(snap.amount_minor_eur, 1000);
  assertEquals(snap.fx_rate_ecb, null);
});

Deno.test("Tier 0 — null amount returns null amount_minor_eur", () => {
  const snap = computeFxSnapshotFromLookup(null, "USD", "2026-05-23", new Map());
  assertEquals(snap.amount_minor_eur, null);
  assertEquals(snap.fx_source, "identity_eur");
});

// -----------------------------------------------------------------------------
// Tier 1 — ecb_daily exact hit
// -----------------------------------------------------------------------------
Deno.test("Tier 1 — ecb_daily exact hit returns ecb_daily snapshot", () => {
  const lookup = makeLookup([["USD/EUR", "2026-05-23", "0.92500000"]]);
  const snap = computeFxSnapshotFromLookup(10000, "USD", "2026-05-23", lookup);
  assertEquals(snap.fx_source, "ecb_daily");
  assertEquals(snap.fx_rate_ecb, "0.92500000");
  assertEquals(snap.amount_minor_eur, 9250); // 10000 * 0.925 = 9250
});

// -----------------------------------------------------------------------------
// Tier 2 — ecb_previous_day_fallback
// -----------------------------------------------------------------------------
Deno.test("Tier 2 — previous-day fallback when today missing", () => {
  const lookup = makeLookup([["GBP/EUR", "2026-05-22", "1.15000000"]]);
  const snap = computeFxSnapshotFromLookup(5000, "GBP", "2026-05-23", lookup);
  assertEquals(snap.fx_source, "ecb_previous_day_fallback");
  assertEquals(snap.fx_rate_ecb, "1.15000000");
  assertEquals(snap.amount_minor_eur, 5750); // 5000 * 1.15
});

Deno.test("Tier 2 — previous-day fallback respects UTC date arithmetic across month boundary", () => {
  const lookup = makeLookup([["USD/EUR", "2026-04-30", "0.93000000"]]);
  const snap = computeFxSnapshotFromLookup(1000, "USD", "2026-05-01", lookup);
  assertEquals(snap.fx_source, "ecb_previous_day_fallback");
  assertEquals(snap.fx_rate_ecb, "0.93000000");
});

// -----------------------------------------------------------------------------
// Tier 3 — stripe_fx_quote fallback
// -----------------------------------------------------------------------------
Deno.test("Tier 3 — stripe_fx_quote when ECB cache misses both days", () => {
  const snap = computeFxSnapshotFromLookup(2000, "CHF", "2026-05-23", new Map(), "0.97000000");
  assertEquals(snap.fx_source, "stripe_fx_quote");
  assertEquals(snap.fx_rate_stripe, "0.97000000");
  assertEquals(snap.fx_rate_ecb, null);
  assertEquals(snap.amount_minor_eur, 1940); // 2000 * 0.97
});

// -----------------------------------------------------------------------------
// Tier 4 — manual_override
// -----------------------------------------------------------------------------
Deno.test("Tier 4 — manual_override when ECB cache + Stripe quote both missing", () => {
  const snap = computeFxSnapshotFromLookup(1000, "USD", "2026-05-23", new Map(), null);
  assertEquals(snap.fx_source, "manual_override");
  assertEquals(snap.amount_minor_eur, null);
  assertEquals(snap.fx_rate_ecb, null);
  assertEquals(snap.fx_rate_stripe, null);
});

// -----------------------------------------------------------------------------
// Sidecar — Stripe rate is captured even when ECB wins
// -----------------------------------------------------------------------------
Deno.test("ECB hit + Stripe quote both present — Stripe captured as sidecar", () => {
  const lookup = makeLookup([["USD/EUR", "2026-05-23", "0.92500000"]]);
  const snap = computeFxSnapshotFromLookup(10000, "USD", "2026-05-23", lookup, "0.93100000");
  assertEquals(snap.fx_source, "ecb_daily");
  assertEquals(snap.fx_rate_ecb, "0.92500000");
  assertEquals(snap.fx_rate_stripe, "0.93100000");
});

// -----------------------------------------------------------------------------
// Divergence check — 0.5% threshold (FX_DIVERGENCE_THRESHOLD_RATIO)
// -----------------------------------------------------------------------------
Deno.test("fxRatesDiverge — threshold is 0.5% (FX_DIVERGENCE_THRESHOLD_RATIO)", () => {
  assertEquals(FX_DIVERGENCE_THRESHOLD_RATIO, 0.005);
});

Deno.test("fxRatesDiverge — 0.4% delta does NOT diverge", () => {
  // ECB 1.0000, Stripe 1.0040 → 0.4% delta
  assertEquals(fxRatesDiverge("1.0000", "1.0040"), false);
});

Deno.test("fxRatesDiverge — 0.6% delta DOES diverge", () => {
  // ECB 1.0000, Stripe 1.0060 → 0.6% delta
  assertEquals(fxRatesDiverge("1.0000", "1.0060"), true);
});

Deno.test("fxRatesDiverge — missing rates return false", () => {
  assertEquals(fxRatesDiverge(null, "1.0"), false);
  assertEquals(fxRatesDiverge("1.0", null), false);
  assertEquals(fxRatesDiverge(null, null), false);
});

Deno.test("fxRatesDiverge — invalid rates return false (defensive)", () => {
  assertEquals(fxRatesDiverge("not-a-number", "1.0"), false);
  assertEquals(fxRatesDiverge("1.0", "not-a-number"), false);
  assertEquals(fxRatesDiverge("0", "1.0"), false); // zero ECB
});
