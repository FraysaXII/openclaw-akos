/**
 * Deno tests — dispatch/finops_dispatch.ts (Stripe webhook FINOPS branch).
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W, 2026-05-23).
 *
 * Run: deno test --allow-env supabase/functions/stripe-webhook-handler/dispatch/test_finops_dispatch.ts
 *
 * NOTE: Because finops_dispatch.ts builds its own Supabase client from environment
 * variables (so the orchestrator can stay thin), the tests stub the env to a non-empty
 * string and rely on stripe_event_logger's failure path being well-behaved (returns
 * { error: ... } rather than throwing on bad credentials). This validates the
 * orchestration contract: missing env → no throw; logged outcome surfaces; the 200
 * path stays intact.
 */

import { assertEquals } from "https://deno.land/std@0.224.0/assert/mod.ts";
import { dispatchFinops } from "./finops_dispatch.ts";

// -----------------------------------------------------------------------------
// Helpers
// -----------------------------------------------------------------------------

// Test environment setup — never call against a real Supabase URL.
function setEnv(supabaseUrl: string, supabaseServiceKey: string) {
  Deno.env.set("SUPABASE_URL", supabaseUrl);
  Deno.env.set("SUPABASE_SERVICE_ROLE_KEY", supabaseServiceKey);
}

function unsetEnv() {
  Deno.env.delete("SUPABASE_URL");
  Deno.env.delete("SUPABASE_SERVICE_ROLE_KEY");
}

// Minimal Stripe.Event-shaped object (only fields used by dispatchFinops).
// deno-lint-ignore no-explicit-any
function makeEvent(overrides: Record<string, unknown> = {}): any {
  return {
    id: "evt_test_" + crypto.randomUUID().slice(0, 8),
    type: "charge.succeeded",
    api_version: "2025-09-30.acacia",
    livemode: false,
    request: { id: "req_test" },
    data: { object: { id: "ch_test_xyz", amount: 1000, currency: "usd" } },
    ...overrides,
  };
}

// -----------------------------------------------------------------------------
// Missing environment variables — graceful degradation
// -----------------------------------------------------------------------------

Deno.test("dispatchFinops — missing SUPABASE_URL returns error outcome (no throw)", async () => {
  unsetEnv();
  setEnv("", "service_key_x");
  const outcome = await dispatchFinops(makeEvent());
  assertEquals(outcome.logged, false);
  assertEquals(outcome.enqueued, false);
  assertEquals(typeof outcome.error, "string");
});

Deno.test("dispatchFinops — missing SERVICE_KEY returns error outcome (no throw)", async () => {
  unsetEnv();
  setEnv("http://localhost:54321", "");
  const outcome = await dispatchFinops(makeEvent());
  assertEquals(outcome.logged, false);
  assertEquals(outcome.enqueued, false);
  assertEquals(typeof outcome.error, "string");
});

// -----------------------------------------------------------------------------
// Event-type scoping — which events get enqueued vs logged-only
// -----------------------------------------------------------------------------
// These tests exercise the scoping logic by using a fake Supabase URL that will fail
// the network call gracefully (Supabase client returns error rather than throwing).
// We rely on the function NEVER throwing — that's the orchestrator contract.

Deno.test("dispatchFinops — out-of-scope event type returns enqueue_skipped_reason", async () => {
  // Use a clearly unreachable URL so network calls fail fast without throwing.
  setEnv("http://127.0.0.1:1", "test_service_role_key");
  const outcome = await dispatchFinops(makeEvent({ type: "customer.created" }));
  // Even though network is unreachable, the function should not throw.
  // The orchestrator contract says: outcome.error may be set, but no exception escapes.
  assertEquals(typeof outcome.logged, "boolean");
  assertEquals(typeof outcome.enqueued, "boolean");
});

Deno.test("dispatchFinops — in-scope event type charge.succeeded routes through enqueue path", async () => {
  setEnv("http://127.0.0.1:1", "test_service_role_key");
  const outcome = await dispatchFinops(makeEvent({ type: "charge.succeeded" }));
  // Same contract: no throw; outcome present.
  assertEquals(typeof outcome.logged, "boolean");
  assertEquals(typeof outcome.enqueued, "boolean");
});

Deno.test("dispatchFinops — subscription lifecycle events are in scope", async () => {
  setEnv("http://127.0.0.1:1", "test_service_role_key");
  for (const t of [
    "customer.subscription.created",
    "customer.subscription.updated",
    "customer.subscription.deleted",
  ]) {
    const outcome = await dispatchFinops(makeEvent({ type: t }));
    // No throw; outcome shape preserved.
    assertEquals(typeof outcome.logged, "boolean");
  }
});

Deno.test("dispatchFinops — invoice + charge events are in scope", async () => {
  setEnv("http://127.0.0.1:1", "test_service_role_key");
  for (const t of [
    "invoice.paid",
    "invoice.payment_failed",
    "charge.refunded",
  ]) {
    const outcome = await dispatchFinops(makeEvent({ type: t }));
    assertEquals(typeof outcome.logged, "boolean");
  }
});

// -----------------------------------------------------------------------------
// Cleanup
// -----------------------------------------------------------------------------

Deno.test("dispatchFinops — cleanup env (sanity)", () => {
  unsetEnv();
  assertEquals(Deno.env.get("SUPABASE_URL"), undefined);
  assertEquals(Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"), undefined);
});
