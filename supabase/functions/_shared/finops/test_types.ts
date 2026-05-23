/**
 * Deno tests — types.ts schema-mirror assertions.
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W, 2026-05-23).
 *
 * Run: deno test --allow-env supabase/functions/_shared/finops/test_types.ts
 *
 * Drift between Python SSOT (akos/hlk_finops_ledger.py) and this TypeScript mirror should
 * surface as test failures in this file. When Python adds a new fact_type / fx_source /
 * resolution_strategy literal, update the corresponding Set here in the same commit.
 */

import { assertEquals, assertThrows } from "https://deno.land/std@0.224.0/assert/mod.ts";
import {
  COUNTERPARTY_UNRESOLVED,
  fxCurrencyPair,
  VALID_CURRENCY_CODES,
  VALID_FACT_TYPES,
  VALID_FX_SOURCES,
  VALID_RESOLUTION_STRATEGIES,
} from "./types.ts";

Deno.test("VALID_FACT_TYPES — 10 fact types (matches Python frozenset)", () => {
  assertEquals(VALID_FACT_TYPES.size, 10);
  for (const t of [
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
  ] as const) {
    assertEquals(VALID_FACT_TYPES.has(t), true, `${t} should be valid`);
  }
});

Deno.test("VALID_CURRENCY_CODES — 4 currencies (matches Python frozenset)", () => {
  assertEquals(VALID_CURRENCY_CODES.size, 4);
  for (const c of ["EUR", "USD", "GBP", "CHF"] as const) {
    assertEquals(VALID_CURRENCY_CODES.has(c), true);
  }
});

Deno.test("VALID_FX_SOURCES — 5 sources (matches Python frozenset)", () => {
  assertEquals(VALID_FX_SOURCES.size, 5);
  for (const s of [
    "ecb_daily",
    "ecb_previous_day_fallback",
    "stripe_fx_quote",
    "manual_override",
    "identity_eur",
  ] as const) {
    assertEquals(VALID_FX_SOURCES.has(s), true);
  }
});

Deno.test("VALID_RESOLUTION_STRATEGIES — 5 strategies (matches Python frozenset)", () => {
  assertEquals(VALID_RESOLUTION_STRATEGIES.size, 5);
  for (const s of [
    "metadata_engagement_id",
    "metadata_billing_plane",
    "stripe_customer_link_lookup",
    "rpp_payout_attribution",
    "manual_review",
  ] as const) {
    assertEquals(VALID_RESOLUTION_STRATEGIES.has(s), true);
  }
});

Deno.test("COUNTERPARTY_UNRESOLVED — sentinel string", () => {
  assertEquals(COUNTERPARTY_UNRESOLVED, "UNRESOLVED");
});

Deno.test("fxCurrencyPair — format SRC/EUR", () => {
  assertEquals(fxCurrencyPair("USD"), "USD/EUR");
  assertEquals(fxCurrencyPair("GBP"), "GBP/EUR");
  assertEquals(fxCurrencyPair("CHF"), "CHF/EUR");
  assertEquals(fxCurrencyPair("EUR"), "EUR/EUR");
});
