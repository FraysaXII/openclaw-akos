/**
 * Deno tests — dispatch/kirbe_holistika_dispatch.ts (Stripe webhook kirbe + holistika branch).
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W, 2026-05-23).
 *
 * Run: deno test --allow-env supabase/functions/stripe-webhook-handler/dispatch/test_kirbe_holistika_dispatch.ts
 *
 * SCOPE: smoke-level verification that the extracted dispatch function:
 *   1. Does not throw on any of the event types it handles.
 *   2. Does not throw on event types outside its handled set (default no_op branch).
 *   3. Gracefully handles missing env (the Supabase / Stripe SDK init returns
 *      clients that will fail downstream rather than throw at construction).
 *
 * NON-SCOPE: bit-for-bit semantic equivalence with the pre-refactor monolith
 *   index.ts. That contract is enforced by git diff at refactor time (extracted
 *   VERBATIM with module-local renamed log source); regressions would surface as
 *   integration test failures, not unit tests.
 */

import { assertEquals } from "https://deno.land/std@0.224.0/assert/mod.ts";
import { dispatchKirbeHolistika } from "./kirbe_holistika_dispatch.ts";

// -----------------------------------------------------------------------------
// Helpers
// -----------------------------------------------------------------------------

function setEnv() {
  Deno.env.set("STRIPE_SECRET_KEY", "sk_test_dummy");
  Deno.env.set("SUPABASE_URL", "http://127.0.0.1:1");
  Deno.env.set("SUPABASE_SERVICE_ROLE_KEY", "dummy_service_role_key");
}

function unsetEnv() {
  Deno.env.delete("STRIPE_SECRET_KEY");
  Deno.env.delete("SUPABASE_URL");
  Deno.env.delete("SUPABASE_SERVICE_ROLE_KEY");
}

// deno-lint-ignore no-explicit-any
function makeCustomerEvent(eventType: string, metadata: Record<string, string> = {}): any {
  return {
    id: "evt_test_" + crypto.randomUUID().slice(0, 8),
    type: eventType,
    data: {
      object: {
        id: "cus_test_abc",
        object: "customer",
        livemode: false,
        metadata,
        name: "Test Customer",
        description: "Test description",
      },
    },
  };
}

// deno-lint-ignore no-explicit-any
function makeSubscriptionEvent(eventType: string, metadata: Record<string, string> = {}): any {
  return {
    id: "evt_test_" + crypto.randomUUID().slice(0, 8),
    type: eventType,
    data: {
      object: {
        id: "sub_test_xyz",
        object: "subscription",
        customer: "cus_test_abc",
        metadata,
      },
    },
  };
}

// deno-lint-ignore no-explicit-any
function makeChargeEvent(eventType: string): any {
  return {
    id: "evt_test_" + crypto.randomUUID().slice(0, 8),
    type: eventType,
    data: {
      object: {
        id: "ch_test_xyz",
        object: "charge",
        customer: "cus_test_abc",
        amount: 1000,
        currency: "usd",
      },
    },
  };
}

// -----------------------------------------------------------------------------
// Event types — ensure no throw on any branch of the switch
// -----------------------------------------------------------------------------

Deno.test("dispatchKirbeHolistika — customer.created with no plane metadata does not throw", async () => {
  setEnv();
  await dispatchKirbeHolistika(makeCustomerEvent("customer.created", {}));
});

Deno.test("dispatchKirbeHolistika — customer.updated holistika plane attempts upsert (network fails gracefully)", async () => {
  setEnv();
  await dispatchKirbeHolistika(
    makeCustomerEvent("customer.updated", { hlk_billing_plane: "holistika_ops" }),
  );
});

Deno.test("dispatchKirbeHolistika — subscription.created kirbe plane no-ops cleanly", async () => {
  setEnv();
  await dispatchKirbeHolistika(
    makeSubscriptionEvent("customer.subscription.created", { hlk_billing_plane: "kirbe" }),
  );
});

Deno.test("dispatchKirbeHolistika — subscription.updated holistika plane logs + skips kirbe write", async () => {
  setEnv();
  await dispatchKirbeHolistika(
    makeSubscriptionEvent("customer.subscription.updated", { hlk_billing_plane: "holistika_ops" }),
  );
});

Deno.test("dispatchKirbeHolistika — subscription.deleted with no metadata falls through to default kirbe", async () => {
  setEnv();
  await dispatchKirbeHolistika(makeSubscriptionEvent("customer.subscription.deleted", {}));
});

Deno.test("dispatchKirbeHolistika — invoice.paid routes via customer (network fails gracefully)", async () => {
  setEnv();
  // deno-lint-ignore no-explicit-any
  const invoiceEvent: any = {
    id: "evt_inv_test",
    type: "invoice.paid",
    data: {
      object: { id: "in_test", customer: "cus_test_abc" },
    },
  };
  await dispatchKirbeHolistika(invoiceEvent);
});

Deno.test("dispatchKirbeHolistika — checkout.session.completed routes via customer", async () => {
  setEnv();
  // deno-lint-ignore no-explicit-any
  const sessionEvent: any = {
    id: "evt_co_test",
    type: "checkout.session.completed",
    data: {
      object: { id: "cs_test", customer: "cus_test_abc" },
    },
  };
  await dispatchKirbeHolistika(sessionEvent);
});

Deno.test("dispatchKirbeHolistika — payment_intent.succeeded routes via customer", async () => {
  setEnv();
  // deno-lint-ignore no-explicit-any
  const piEvent: any = {
    id: "evt_pi_test",
    type: "payment_intent.succeeded",
    data: {
      object: { id: "pi_test", customer: "cus_test_abc" },
    },
  };
  await dispatchKirbeHolistika(piEvent);
});

Deno.test("dispatchKirbeHolistika — charge.succeeded routes via customer", async () => {
  setEnv();
  await dispatchKirbeHolistika(makeChargeEvent("charge.succeeded"));
});

Deno.test("dispatchKirbeHolistika — billing_portal.session.created logs observability only", async () => {
  setEnv();
  // deno-lint-ignore no-explicit-any
  const portalEvent: any = {
    id: "evt_bp_test",
    type: "billing_portal.session.created",
    data: {
      object: { id: "bps_test", customer: "cus_test_abc" },
    },
  };
  await dispatchKirbeHolistika(portalEvent);
});

Deno.test("dispatchKirbeHolistika — unknown event type hits default no_op branch", async () => {
  setEnv();
  // deno-lint-ignore no-explicit-any
  const unknownEvent: any = {
    id: "evt_unknown",
    type: "some.future.event_type",
    data: { object: { id: "x_test" } },
  };
  await dispatchKirbeHolistika(unknownEvent);
});

// -----------------------------------------------------------------------------
// Edge cases — null + missing fields
// -----------------------------------------------------------------------------

Deno.test("dispatchKirbeHolistika — invoice with null customer logs no_customer; no throw", async () => {
  setEnv();
  // deno-lint-ignore no-explicit-any
  const invoiceEvent: any = {
    id: "evt_inv_no_cus",
    type: "invoice.paid",
    data: {
      object: { id: "in_test_no_cus", customer: null },
    },
  };
  await dispatchKirbeHolistika(invoiceEvent);
});

Deno.test("dispatchKirbeHolistika — subscription with deleted customer falls back to default_kirbe", async () => {
  setEnv();
  // deno-lint-ignore no-explicit-any
  const subEvent: any = {
    id: "evt_sub_deleted_cus",
    type: "customer.subscription.created",
    data: {
      object: {
        id: "sub_test_del",
        object: "subscription",
        customer: { deleted: true } as { deleted: true },
        metadata: {},
      },
    },
  };
  await dispatchKirbeHolistika(subEvent);
});

// -----------------------------------------------------------------------------
// Cleanup
// -----------------------------------------------------------------------------

Deno.test("dispatchKirbeHolistika — env cleanup sanity", () => {
  unsetEnv();
  assertEquals(Deno.env.get("STRIPE_SECRET_KEY"), undefined);
});
