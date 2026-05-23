/**
 * Deno tests — counterparty_resolver.ts (R1 router).
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W, 2026-05-23).
 *
 * Run: deno test --allow-env supabase/functions/_shared/finops/test_counterparty_resolver.ts
 *
 * Mirror the test surface in tests/test_hlk_finops_ledger.py §counterparty_resolver to keep
 * the Python SSOT + TypeScript runtime in sync.
 */

import { assertEquals, assertNotEquals } from "https://deno.land/std@0.224.0/assert/mod.ts";
import { resolveCounterpartyId } from "./counterparty_resolver.ts";

// -----------------------------------------------------------------------------
// In-memory fake Supabase for Strategy 3 testing.
// -----------------------------------------------------------------------------
type StripeCustomerLinkRow = { stripe_customer_id: string; finops_counterparty_id: string; org_label?: string };

function makeFakeSupabase(rows: StripeCustomerLinkRow[]): {
  from: (table: string) => unknown;
} {
  return {
    from: (_table: string) => ({
      select: (_cols: string) => ({
        eq: (_col: string, value: string) => ({
          maybeSingle: () => {
            const found = rows.find((r) => r.stripe_customer_id === value);
            return Promise.resolve({ data: found ?? null, error: null });
          },
        }),
      }),
    }),
  };
}

// -----------------------------------------------------------------------------
// Strategy 1: metadata_engagement_id (HIGH)
// -----------------------------------------------------------------------------
Deno.test("R1 Strategy 1 — metadata_engagement_id resolves HIGH confidence", async () => {
  // deno-lint-ignore no-explicit-any
  const result = await resolveCounterpartyId(null as any, null, { hlk_engagement_id: "acme_corp" });
  assertEquals(result.counterparty_id, "acme_corp");
  assertEquals(result.strategy_used, "metadata_engagement_id");
  assertEquals(result.confidence, "high");
  assertEquals(result.ops_register_payload, null);
});

Deno.test("R1 Strategy 1 — invalid slug falls through to next strategy", async () => {
  // deno-lint-ignore no-explicit-any
  const result = await resolveCounterpartyId(null as any, null, { hlk_engagement_id: "INVALID!CHARS" });
  // Falls through; with no other signal, ends at manual_review
  assertEquals(result.strategy_used, "manual_review");
  assertEquals(result.confidence, "unresolved");
});

// -----------------------------------------------------------------------------
// Strategy 2: metadata_billing_plane (MEDIUM)
// -----------------------------------------------------------------------------
Deno.test("R1 Strategy 2 — metadata_billing_plane resolves MEDIUM confidence", async () => {
  // deno-lint-ignore no-explicit-any
  const result = await resolveCounterpartyId(null as any, null, { hlk_billing_plane: "stripe" });
  assertEquals(result.counterparty_id, "stripe");
  assertEquals(result.strategy_used, "metadata_billing_plane");
  assertEquals(result.confidence, "medium");
});

Deno.test("R1 Strategy 2 — 'holistika' sentinel does NOT resolve (falls through)", async () => {
  // deno-lint-ignore no-explicit-any
  const r1 = await resolveCounterpartyId(null as any, null, { hlk_billing_plane: "holistika" });
  assertEquals(r1.strategy_used, "manual_review");
  // deno-lint-ignore no-explicit-any
  const r2 = await resolveCounterpartyId(null as any, null, { hlk_billing_plane: "kirbe" });
  assertEquals(r2.strategy_used, "manual_review");
});

// -----------------------------------------------------------------------------
// Strategy 3: stripe_customer_link_lookup (LOW; DB-backed)
// -----------------------------------------------------------------------------
Deno.test("R1 Strategy 3 — stripe_customer_link_lookup resolves LOW confidence", async () => {
  const fake = makeFakeSupabase([
    { stripe_customer_id: "cus_test123", finops_counterparty_id: "vendor_x" },
  ]);
  // deno-lint-ignore no-explicit-any
  const result = await resolveCounterpartyId(fake as any, "cus_test123", {});
  assertEquals(result.counterparty_id, "vendor_x");
  assertEquals(result.strategy_used, "stripe_customer_link_lookup");
  assertEquals(result.confidence, "low");
});

Deno.test("R1 Strategy 3 — no link match falls to manual_review", async () => {
  const fake = makeFakeSupabase([]);
  // deno-lint-ignore no-explicit-any
  const result = await resolveCounterpartyId(fake as any, "cus_missing", {});
  assertEquals(result.strategy_used, "manual_review");
  assertEquals(result.confidence, "unresolved");
});

// -----------------------------------------------------------------------------
// Strategy 4: manual_review fallback with OPS_REGISTER payload
// -----------------------------------------------------------------------------
Deno.test("R1 Strategy 4 — manual_review fires + emits counterparty_resolution_failed OPS", async () => {
  // deno-lint-ignore no-explicit-any
  const result = await resolveCounterpartyId(null as any, null, {});
  assertEquals(result.counterparty_id, "UNRESOLVED");
  assertEquals(result.strategy_used, "manual_review");
  assertEquals(result.confidence, "unresolved");
  assertNotEquals(result.ops_register_payload, null);
  assertEquals(result.ops_register_payload?.ops_class, "counterparty_resolution_failed");
  assertEquals(result.ops_register_payload?.severity, "high");
});

// -----------------------------------------------------------------------------
// Ladder ordering — Strategy 1 wins over Strategy 2 wins over Strategy 3
// -----------------------------------------------------------------------------
Deno.test("R1 ladder ordering — engagement_id beats billing_plane beats link_lookup", async () => {
  const fake = makeFakeSupabase([
    { stripe_customer_id: "cus_x", finops_counterparty_id: "from_link" },
  ]);
  // deno-lint-ignore no-explicit-any
  const result = await resolveCounterpartyId(fake as any, "cus_x", {
    hlk_engagement_id: "from_eng",
    hlk_billing_plane: "from_plane",
  });
  assertEquals(result.counterparty_id, "from_eng");
  assertEquals(result.strategy_used, "metadata_engagement_id");
});
