/**
 * Stripe raw-event logger — Layer 1 idempotency for the 3-layer retry strategy (R3).
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W under D-IH-81-G umbrella, 2026-05-23).
 *
 * Per R3 architecture (Bundle B-2 report §3.3): the FINOPS branch of stripe-webhook-handler
 * MUST land 200-OK to Stripe within < 5s. To absorb downstream writer latency without losing
 * idempotency guarantees, every received event is INSERTed to holistika_ops.stripe_events
 * (raw payload + received_at) FIRST, then queued onto pgmq.finops_writer_queue. The worker
 * later processes events from the queue and updates stripe_events.processed_at when done.
 *
 * Idempotency layer 1: PRIMARY KEY on stripe_event_id. Duplicate Stripe deliveries are
 * absorbed by Postgres unique-constraint violation (caught + ignored as duplicate).
 *
 * Idempotency layer 2: pgmq message-visibility timeout + worker's per-event check on
 * processed_at (skip if already non-null).
 *
 * Idempotency layer 3: finops.registered_fact unique-by-source_reference constraint
 * (enforced separately by the worker pre-insert check).
 */

import type { SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";

// =============================================================================
// §1 — Raw event row shape (mirror holistika_ops.stripe_events DDL)
// =============================================================================

export interface StripeRawEvent {
  id: string; // Stripe event id (evt_xxx)
  type: string; // e.g. 'charge.succeeded'
  api_version: string | null;
  livemode: boolean;
  request?: { id?: string | null } | null;
  data: { object: Record<string, unknown> };
  // Stripe carries additional fields; we persist the whole payload as raw_payload jsonb.
  [k: string]: unknown;
}

export interface LogEventResult {
  inserted: boolean;
  duplicate: boolean;
  error: string | null;
}

// =============================================================================
// §2 — Insert raw event (idempotent via PK)
// =============================================================================

/**
 * INSERT raw Stripe event into holistika_ops.stripe_events.
 * Idempotent: returns {duplicate: true} if PK already exists (Stripe redelivery).
 * Never throws — caller (webhook handler) must always respond 200 to Stripe.
 */
export async function logStripeEvent(
  supabase: SupabaseClient,
  event: StripeRawEvent,
): Promise<LogEventResult> {
  if (!event?.id || !event?.type) {
    return { inserted: false, duplicate: false, error: "event missing id or type" };
  }

  const row = {
    stripe_event_id: event.id,
    event_type: event.type,
    api_version: event.api_version ?? null,
    livemode: Boolean(event.livemode),
    request_id: event.request?.id ?? null,
    raw_payload: event,
    received_at: new Date().toISOString(),
    process_attempts: 0,
  };

  const { error } = await supabase
    .schema("holistika_ops")
    .from("stripe_events")
    .insert(row);

  if (!error) {
    return { inserted: true, duplicate: false, error: null };
  }

  // 23505 = unique_violation in PostgreSQL → duplicate Stripe delivery; benign.
  // Supabase REST surfaces this as a 409-class error with code '23505' or message containing it.
  const msg = error.message ?? "";
  if (
    error.code === "23505" ||
    msg.toLowerCase().includes("duplicate") ||
    msg.toLowerCase().includes("unique constraint")
  ) {
    return { inserted: false, duplicate: true, error: null };
  }

  console.warn(
    JSON.stringify({
      source: "stripe_event_logger",
      note: "raw event insert failed (non-duplicate)",
      stripe_event_id: event.id,
      event_type: event.type,
      error: msg,
      code: error.code,
    }),
  );
  return { inserted: false, duplicate: false, error: msg };
}

// =============================================================================
// §3 — Queue event onto pgmq.finops_writer_queue (Layer 2 idempotency entry point)
// =============================================================================

export interface EnqueueResult {
  queued: boolean;
  msg_id: number | null;
  error: string | null;
}

/**
 * Enqueue a stripe_event_id reference onto pgmq.finops_writer_queue for the worker.
 * Payload is intentionally minimal (just the event id) so the worker re-reads the raw payload
 * from holistika_ops.stripe_events to guarantee a single source of truth.
 */
export async function enqueueFinopsEvent(
  supabase: SupabaseClient,
  stripeEventId: string,
): Promise<EnqueueResult> {
  if (!stripeEventId) {
    return { queued: false, msg_id: null, error: "stripeEventId is empty" };
  }

  // pgmq.send returns msg_id; we use the RPC bridge.
  const { data, error } = await supabase.rpc("pgmq_send_finops_writer", {
    p_event_id: stripeEventId,
  });

  if (error) {
    console.warn(
      JSON.stringify({
        source: "stripe_event_logger",
        note: "pgmq enqueue failed",
        stripe_event_id: stripeEventId,
        error: error.message,
      }),
    );
    return { queued: false, msg_id: null, error: error.message };
  }

  return { queued: true, msg_id: Number(data) || null, error: null };
}

// =============================================================================
// §4 — Mark processed (worker uses this after successful registered_fact write)
// =============================================================================

export async function markStripeEventProcessed(
  supabase: SupabaseClient,
  stripeEventId: string,
  opts: { fxRateEcb?: string | null; fxRateStripe?: string | null; fxSource?: string | null } = {},
): Promise<void> {
  const patch: Record<string, unknown> = {
    processed_at: new Date().toISOString(),
  };
  if (opts.fxRateEcb !== undefined) patch.fx_rate_ecb = opts.fxRateEcb;
  if (opts.fxRateStripe !== undefined) patch.fx_rate_stripe = opts.fxRateStripe;
  if (opts.fxSource !== undefined) patch.fx_source = opts.fxSource;

  const { error } = await supabase
    .schema("holistika_ops")
    .from("stripe_events")
    .update(patch)
    .eq("stripe_event_id", stripeEventId);

  if (error) {
    console.warn(
      JSON.stringify({
        source: "stripe_event_logger",
        note: "markStripeEventProcessed update failed",
        stripe_event_id: stripeEventId,
        error: error.message,
      }),
    );
  }
}

// =============================================================================
// §5 — Increment retry counter (worker uses this on transient errors)
// =============================================================================

export async function incrementStripeEventAttempts(
  supabase: SupabaseClient,
  stripeEventId: string,
  lastError: string,
): Promise<{ attempts: number; error: string | null }> {
  const { data: existing, error: readErr } = await supabase
    .schema("holistika_ops")
    .from("stripe_events")
    .select("process_attempts")
    .eq("stripe_event_id", stripeEventId)
    .maybeSingle();

  if (readErr || !existing) {
    return { attempts: 0, error: readErr?.message ?? "row not found" };
  }

  const attempts = (existing.process_attempts ?? 0) + 1;
  const { error: writeErr } = await supabase
    .schema("holistika_ops")
    .from("stripe_events")
    .update({ process_attempts: attempts, last_error: lastError.slice(0, 2048) })
    .eq("stripe_event_id", stripeEventId);

  return { attempts, error: writeErr?.message ?? null };
}
