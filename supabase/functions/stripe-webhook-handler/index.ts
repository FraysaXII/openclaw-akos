/**
 * Stripe webhook handler — dispatch-pattern orchestrator (refactored at I81 P2 B-2b, 2026-05-23).
 *
 * Initiative 14 Wave B3 (original kirbe + holistika_ops branches; commit lineage preserved
 * in git blame) + Initiative 81 Phase 2 Bundle B-2b refactor (D-IH-81-W under D-IH-81-G
 * umbrella, 2026-05-23).
 *
 * ARCHITECTURE — DISPATCH PATTERN per b2b-wh-b operator ratification:
 *
 *   ┌───────────────────────────────────────────────────────────────────────────────┐
 *   │ Stripe POST /functions/v1/stripe-webhook-handler                              │
 *   └───────────────────────────────────────────────────────────────────────────────┘
 *                                       │
 *                                       ▼
 *   ┌───────────────────────────────────────────────────────────────────────────────┐
 *   │ §1 — Signature verification (REQUIRED; 400 on failure)                        │
 *   └───────────────────────────────────────────────────────────────────────────────┘
 *                                       │
 *                                       ▼
 *   ┌───────────────────────────────────────────────────────────────────────────────┐
 *   │ §2 — FINOPS dispatch (MANDATORY; raw event log + pgmq enqueue)                │
 *   │      Critical path; absorbs every event into holistika_ops.stripe_events.     │
 *   └───────────────────────────────────────────────────────────────────────────────┘
 *                                       │
 *                                       ▼
 *   ┌───────────────────────────────────────────────────────────────────────────────┐
 *   │ §3 — Kirbe + Holistika dispatch (BEST-EFFORT; preserved pre-refactor logic)   │
 *   │      Wrapped in try/catch; throws are logged but do NOT prevent 200 to Stripe. │
 *   └───────────────────────────────────────────────────────────────────────────────┘
 *                                       │
 *                                       ▼
 *   ┌───────────────────────────────────────────────────────────────────────────────┐
 *   │ §4 — Return 200 OK to Stripe (target < 5s end-to-end)                         │
 *   └───────────────────────────────────────────────────────────────────────────────┘
 *
 * RATIONALE for FINOPS-FIRST ordering:
 *   - FINOPS raw event log is the audit trail — must NEVER be lost.
 *   - Kirbe dispatch can make Stripe API calls (customer retrieval) which can be slow;
 *     putting FINOPS first guarantees the audit trail is captured even if kirbe times out.
 *   - Both dispatches are wrapped in try/catch independently so one branch's failure
 *     never cascades to the other.
 *
 * BEHAVIOR PRESERVATION:
 *   The kirbe + holistika_ops branches were EXTRACTED verbatim into
 *   dispatch/kirbe_holistika_dispatch.ts. No semantic changes; behavior bit-for-bit
 *   identical to pre-refactor. Git blame on the extracted file shows the original lineage.
 */

import Stripe from "https://esm.sh/stripe@14.21.0?target=deno";
import { dispatchKirbeHolistika } from "./dispatch/kirbe_holistika_dispatch.ts";
import { dispatchFinops } from "./dispatch/finops_dispatch.ts";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY") ?? "", {
  apiVersion: "2024-11-20.acacia",
  httpClient: Stripe.createFetchHttpClient(),
});

Deno.serve(async (req) => {
  if (req.method !== "POST") {
    return new Response("method not allowed", { status: 405 });
  }

  // §1 — Signature verification (mandatory; 400 on failure)
  const signature = req.headers.get("stripe-signature");
  const webhookSecret = Deno.env.get("STRIPE_WEBHOOK_SECRET");
  if (!signature || !webhookSecret) {
    return new Response("missing stripe-signature or STRIPE_WEBHOOK_SECRET", { status: 400 });
  }

  const body = await req.text();
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error(
      JSON.stringify({
        source: "stripe_webhook.orchestrator",
        note: "signature verification failed",
        error: msg,
      }),
    );
    return new Response(`webhook signature error: ${msg}`, { status: 400 });
  }

  // §2 — FINOPS dispatch (mandatory; raw event log + pgmq enqueue).
  //      Always await this — never want to return 200 without capturing the audit trail.
  let finopsOutcome;
  try {
    finopsOutcome = await dispatchFinops(event);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error(
      JSON.stringify({
        source: "stripe_webhook.orchestrator",
        note: "FINOPS dispatch threw (returning 200 anyway; audit trail incomplete)",
        stripe_event_id: event.id,
        event_type: event.type,
        error: msg,
      }),
    );
    finopsOutcome = { logged: false, duplicate: false, enqueued: false, error: msg };
  }

  // §3 — Kirbe + Holistika dispatch (best-effort).
  //      Pre-refactor logic preserved bit-for-bit.
  try {
    await dispatchKirbeHolistika(event);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error(
      JSON.stringify({
        source: "stripe_webhook.orchestrator",
        note: "kirbe+holistika dispatch threw (best-effort; 200 to Stripe regardless)",
        stripe_event_id: event.id,
        event_type: event.type,
        error: msg,
      }),
    );
  }

  // §4 — Return 200 to Stripe
  return new Response(
    JSON.stringify({
      received: true,
      stripe_event_id: event.id,
      event_type: event.type,
      finops: {
        logged: finopsOutcome.logged,
        duplicate: finopsOutcome.duplicate,
        enqueued: finopsOutcome.enqueued,
      },
    }),
    {
      headers: { "Content-Type": "application/json" },
      status: 200,
    },
  );
});
