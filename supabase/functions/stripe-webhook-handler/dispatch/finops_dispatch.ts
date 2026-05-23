/**
 * Dispatch — FINOPS branch of the Stripe webhook handler.
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W under D-IH-81-G umbrella, 2026-05-23).
 *
 * Per R3 architecture (3-layer retry): the FINOPS branch absorbs every Stripe event into
 * holistika_ops.stripe_events (raw payload + received_at), then enqueues the event id
 * onto pgmq.finops_writer_queue. The handler MUST return 200 to Stripe within < 5s, so
 * THIS dispatch is the only critical-path work — actual fact-row writes happen async in
 * supabase/functions/finops-writer-worker/index.ts.
 *
 * EVENT TYPES THAT ENQUEUE:
 *   - charge.succeeded
 *   - charge.refunded
 *   - invoice.paid
 *   - invoice.payment_failed
 *   - customer.subscription.created
 *   - customer.subscription.updated
 *   - customer.subscription.deleted
 *
 *   Other events are still INSERTed to stripe_events (for audit trail) but NOT enqueued.
 *
 * IDEMPOTENCY: PK on stripe_events.stripe_event_id absorbs duplicate Stripe deliveries
 *   (Stripe redelivers on transient failures); duplicate events are recognized via the
 *   unique-violation error code (23505) and skipped without enqueueing again.
 */

import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";
import type Stripe from "https://esm.sh/stripe@14.21.0?target=deno";
import {
  enqueueFinopsEvent,
  logStripeEvent,
  type StripeRawEvent,
} from "../../_shared/finops/stripe_event_logger.ts";

const FINOPS_ENQUEUE_EVENT_TYPES: ReadonlySet<string> = new Set([
  "charge.succeeded",
  "charge.refunded",
  "invoice.paid",
  "invoice.payment_failed",
  "customer.subscription.created",
  "customer.subscription.updated",
  "customer.subscription.deleted",
]);

export interface FinopsDispatchOutcome {
  logged: boolean;
  duplicate: boolean;
  enqueued: boolean;
  enqueue_skipped_reason?: string;
  error: string | null;
}

function logFinops(payload: Record<string, unknown>) {
  console.log(JSON.stringify({ source: "stripe_webhook.finops", ...payload }));
}

/**
 * Main dispatch entry. Logs the raw event to holistika_ops.stripe_events + enqueues
 * onto pgmq.finops_writer_queue when applicable. Never throws (caller must respond 200).
 */
export async function dispatchFinops(event: Stripe.Event): Promise<FinopsDispatchOutcome> {
  const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "";
  const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
  const outcome: FinopsDispatchOutcome = {
    logged: false,
    duplicate: false,
    enqueued: false,
    error: null,
  };

  if (!supabaseUrl || !supabaseServiceKey) {
    outcome.error = "missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY";
    logFinops({ event_type: event.type, note: outcome.error, severity: "high" });
    return outcome;
  }

  const supabase = createClient(supabaseUrl, supabaseServiceKey);

  // Step 1: persist raw event (idempotency layer 1)
  const rawEvent: StripeRawEvent = event as unknown as StripeRawEvent;
  const logResult = await logStripeEvent(supabase, rawEvent);
  outcome.logged = logResult.inserted;
  outcome.duplicate = logResult.duplicate;
  if (logResult.error) {
    outcome.error = `log: ${logResult.error}`;
    logFinops({ event_type: event.type, stripe_event_id: event.id, note: "raw event log failed", error: logResult.error });
    return outcome;
  }
  if (logResult.duplicate) {
    logFinops({ event_type: event.type, stripe_event_id: event.id, note: "duplicate Stripe delivery; not re-enqueuing" });
    outcome.enqueue_skipped_reason = "duplicate_delivery";
    return outcome;
  }

  // Step 2: enqueue only when event is in the FINOPS writer scope
  if (!FINOPS_ENQUEUE_EVENT_TYPES.has(event.type)) {
    outcome.enqueue_skipped_reason = "event_type_out_of_writer_scope";
    logFinops({ event_type: event.type, stripe_event_id: event.id, note: "logged; not enqueued (out of writer scope)" });
    return outcome;
  }

  const enqResult = await enqueueFinopsEvent(supabase, event.id);
  outcome.enqueued = enqResult.queued;
  if (enqResult.error) {
    outcome.error = `enqueue: ${enqResult.error}`;
    logFinops({ event_type: event.type, stripe_event_id: event.id, note: "pgmq enqueue failed", error: enqResult.error });
    return outcome;
  }
  logFinops({
    event_type: event.type,
    stripe_event_id: event.id,
    note: "logged + enqueued",
    msg_id: enqResult.msg_id,
  });
  return outcome;
}
