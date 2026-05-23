/**
 * Edge Function — finops-writer-worker
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W under D-IH-81-G umbrella, 2026-05-23).
 *
 * The worker side of the 3-layer retry architecture (R3):
 *   Webhook handler enqueues stripe_event_id onto pgmq.finops_writer_queue (200 to Stripe < 5s).
 *   THIS WORKER reads from the queue, joins raw payload from holistika_ops.stripe_events,
 *   resolves counterparty (R1), computes FX snapshot (R2), and writes one row to
 *   finops.registered_fact. Failures: increment retry counter, fail-fast on Nth attempt,
 *   archive to finops_writer_dlq + emit OPS_REGISTER row.
 *
 * INVOCATION: scheduled via Supabase cron (recommended: every 60 seconds).
 *   curl -X POST -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
 *        https://<project>.supabase.co/functions/v1/finops-writer-worker
 *
 * CONCURRENCY: single-instance only. The visibility-timeout in pgmq.read prevents
 *   another invocation from picking up the same message during the worker's window.
 *
 * SUPPORTED EVENT TYPES (Bundle B-2b initial scope):
 *   - charge.succeeded       → fact_type = 'charge_succeeded'
 *   - charge.refunded        → fact_type = 'charge_refunded'
 *   - invoice.paid           → fact_type = 'invoice_paid'
 *   - invoice.payment_failed → fact_type = 'invoice_payment_failed'
 *   - subscription.created   → fact_type = 'subscription_created'
 *   - subscription.updated   → fact_type = 'subscription_updated'
 *   - subscription.deleted   → fact_type = 'subscription_canceled'
 *
 *   Other Stripe events are queued + processed (raw_payload stays in stripe_events) but
 *   do NOT produce a registered_fact row; the worker marks them processed_at + skips
 *   the registered_fact INSERT. This keeps the queue clean while preserving event log.
 *
 * BUDGETS:
 *   - MAX_BATCH = 25 messages per invocation
 *   - VISIBILITY_TIMEOUT_S = 90 (must exceed worst-case worker latency)
 *   - MAX_RETRIES = 5 (then archive to DLQ + emit dlq_event_max_retries OPS row)
 */

import { createClient, type SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";
import { resolveCounterpartyId } from "../_shared/finops/counterparty_resolver.ts";
import { computeFxSnapshotFromDb, fxRatesDiverge } from "../_shared/finops/fx_snapshot.ts";
import { emitOpsRegisterRow } from "../_shared/finops/ops_register_emit.ts";
import {
  incrementStripeEventAttempts,
  markStripeEventProcessed,
} from "../_shared/finops/stripe_event_logger.ts";
import type {
  CurrencyCode,
  FactType,
  OpsRegisterEmitPayload,
  RegisteredFactRow,
} from "../_shared/finops/types.ts";

const MAX_BATCH = 25;
const VISIBILITY_TIMEOUT_S = 90;
const MAX_RETRIES = 5;
const DLQ_DEPTH_ALERT_THRESHOLD = 10;

// =============================================================================
// §1 — Event type → fact_type mapping
// =============================================================================

const EVENT_TO_FACT_TYPE: Record<string, FactType> = {
  "charge.succeeded": "charge_succeeded",
  "charge.refunded": "charge_refunded",
  "invoice.paid": "invoice_paid",
  "invoice.payment_failed": "invoice_payment_failed",
  "customer.subscription.created": "subscription_created",
  "customer.subscription.updated": "subscription_updated",
  "customer.subscription.deleted": "subscription_canceled",
};

// =============================================================================
// §2 — Extract finops-relevant fields from Stripe event raw payload
// =============================================================================

interface ExtractedFields {
  stripe_customer_id: string | null;
  stripe_subscription_id: string | null;
  amount_minor: number | null;
  currency: CurrencyCode;
  effective_date: string;
  metadata: Record<string, unknown>;
  source_reference: string;
  stripe_fx_quote: string | null;
}

function normalizeCurrency(c: unknown): CurrencyCode | null {
  if (typeof c !== "string") return null;
  const upper = c.trim().toUpperCase();
  if (upper === "EUR" || upper === "USD" || upper === "GBP" || upper === "CHF") return upper as CurrencyCode;
  return null;
}

function isoDateFromUnix(unix: unknown): string {
  if (typeof unix === "number" && Number.isFinite(unix)) {
    return new Date(unix * 1000).toISOString().slice(0, 10);
  }
  return new Date().toISOString().slice(0, 10);
}

// deno-lint-ignore no-explicit-any
function extractFields(eventType: string, payload: any): ExtractedFields | { skip: true; reason: string } {
  const obj = payload?.data?.object ?? {};
  const eventId = payload?.id ?? "unknown_evt";

  // Common
  const metadata: Record<string, unknown> = (obj.metadata && typeof obj.metadata === "object") ? obj.metadata : {};
  let stripe_customer_id: string | null = null;
  let stripe_subscription_id: string | null = null;
  let amount_minor: number | null = null;
  let currency: CurrencyCode | null = null;
  let effective_date = isoDateFromUnix(payload?.created);
  let source_reference = `stripe:${eventType}:${eventId}`;
  let stripe_fx_quote: string | null = null;

  switch (eventType) {
    case "charge.succeeded":
    case "charge.refunded": {
      stripe_customer_id = (obj.customer ?? null) as string | null;
      amount_minor = typeof obj.amount === "number" ? obj.amount : null;
      currency = normalizeCurrency(obj.currency);
      effective_date = isoDateFromUnix(obj.created ?? payload?.created);
      source_reference = `stripe:charge:${obj.id ?? eventId}`;
      // Stripe Charge object exposes balance_transaction; the actual FX rate lives there
      // but resolving it requires a follow-up API call. For now we capture exchange_rate
      // when present on the charge object (newer API versions) as the Stripe sidecar.
      if (typeof obj.exchange_rate === "number" && obj.exchange_rate > 0) {
        stripe_fx_quote = obj.exchange_rate.toFixed(8);
      }
      break;
    }
    case "invoice.paid":
    case "invoice.payment_failed": {
      stripe_customer_id = (obj.customer ?? null) as string | null;
      stripe_subscription_id = (obj.subscription ?? null) as string | null;
      amount_minor = typeof obj.amount_paid === "number"
        ? obj.amount_paid
        : (typeof obj.amount_due === "number" ? obj.amount_due : null);
      currency = normalizeCurrency(obj.currency);
      effective_date = isoDateFromUnix(obj.status_transitions?.paid_at ?? obj.created ?? payload?.created);
      source_reference = `stripe:invoice:${obj.id ?? eventId}`;
      break;
    }
    case "customer.subscription.created":
    case "customer.subscription.updated":
    case "customer.subscription.deleted": {
      stripe_customer_id = (obj.customer ?? null) as string | null;
      stripe_subscription_id = (obj.id ?? null) as string | null;
      // Subscription events do not carry a monetary amount; amount_minor stays null.
      // currency is read from items[0].plan.currency when present (used only as label).
      const firstItem = obj.items?.data?.[0];
      currency = normalizeCurrency(firstItem?.price?.currency ?? firstItem?.plan?.currency) ?? "EUR";
      effective_date = isoDateFromUnix(obj.start_date ?? obj.created ?? payload?.created);
      source_reference = `stripe:subscription:${obj.id ?? eventId}`;
      break;
    }
    default:
      return { skip: true, reason: `event_type '${eventType}' not in writer scope` };
  }

  if (!currency) {
    return { skip: true, reason: `unrecognized currency on event ${eventId}` };
  }

  return {
    stripe_customer_id,
    stripe_subscription_id,
    amount_minor,
    currency,
    effective_date,
    metadata,
    source_reference,
    stripe_fx_quote,
  };
}

// =============================================================================
// §3 — Process one queue message
// =============================================================================

interface ProcessOutcome {
  msg_id: number;
  stripe_event_id: string;
  action: "wrote_fact" | "skipped" | "duplicate" | "retried" | "archived";
  fact_type?: FactType;
  counterparty_id?: string;
  error?: string;
}

async function processMessage(
  supabase: SupabaseClient,
  msg: { msg_id: number; read_ct: number; message: { stripe_event_id?: string } },
): Promise<ProcessOutcome> {
  const stripeEventId = msg.message?.stripe_event_id ?? "";
  const outcome: ProcessOutcome = { msg_id: msg.msg_id, stripe_event_id: stripeEventId, action: "skipped" };

  if (!stripeEventId) {
    outcome.action = "archived";
    outcome.error = "queue message missing stripe_event_id";
    await supabase.rpc("pgmq_archive_finops_writer", { p_msg_id: msg.msg_id });
    return outcome;
  }

  // ---- Step 1: load raw event from holistika_ops.stripe_events
  const { data: eventRow, error: eventErr } = await supabase
    .schema("holistika_ops")
    .from("stripe_events")
    .select("event_type, raw_payload, processed_at, process_attempts")
    .eq("stripe_event_id", stripeEventId)
    .maybeSingle();

  if (eventErr || !eventRow) {
    outcome.action = "archived";
    outcome.error = `event row missing or read failed: ${eventErr?.message ?? "no row"}`;
    await supabase.rpc("pgmq_archive_finops_writer", { p_msg_id: msg.msg_id });
    return outcome;
  }

  // ---- Step 2: idempotency — already processed?
  if (eventRow.processed_at) {
    outcome.action = "duplicate";
    await supabase.rpc("pgmq_delete_finops_writer", { p_msg_id: msg.msg_id });
    return outcome;
  }

  // ---- Step 3: extract finops fields
  const extracted = extractFields(eventRow.event_type, eventRow.raw_payload);
  if ("skip" in extracted) {
    // Out-of-scope event type — mark processed, delete queue message, no fact row.
    await markStripeEventProcessed(supabase, stripeEventId);
    await supabase.rpc("pgmq_delete_finops_writer", { p_msg_id: msg.msg_id });
    outcome.action = "skipped";
    outcome.error = extracted.reason;
    return outcome;
  }

  // ---- Step 4: resolve counterparty (R1)
  const resolution = await resolveCounterpartyId(
    supabase,
    extracted.stripe_customer_id,
    extracted.metadata,
  );

  if (resolution.ops_register_payload) {
    await emitOpsRegisterRow(supabase, resolution.ops_register_payload);
  }

  // ---- Step 5: compute FX snapshot (R2)
  const fx = await computeFxSnapshotFromDb(
    supabase,
    extracted.amount_minor,
    extracted.currency,
    extracted.effective_date,
    extracted.stripe_fx_quote,
  );

  // Divergence check — emit OPS row when both rates present and outside threshold.
  if (fxRatesDiverge(fx.fx_rate_ecb, fx.fx_rate_stripe)) {
    const divergencePayload: OpsRegisterEmitPayload = {
      ops_class: "fx_divergence_threshold_exceeded",
      summary:
        `ECB rate ${fx.fx_rate_ecb} vs Stripe rate ${fx.fx_rate_stripe} for ${extracted.currency}/EUR on ${extracted.effective_date} exceeds 0.5% divergence threshold.`,
      severity: "medium",
      stripe_event_id: stripeEventId,
      stripe_customer_id: extracted.stripe_customer_id,
      metadata: { currency: extracted.currency, effective_date: extracted.effective_date, fx_source: fx.fx_source },
    };
    await emitOpsRegisterRow(supabase, divergencePayload);
  }
  if (fx.fx_source === "ecb_previous_day_fallback") {
    const stalePayload: OpsRegisterEmitPayload = {
      ops_class: "fx_cache_stale",
      summary:
        `ECB cache had no rate for ${extracted.currency}/EUR on ${extracted.effective_date}; used previous-day fallback rate ${fx.fx_rate_ecb}.`,
      severity: "low",
      stripe_event_id: stripeEventId,
      metadata: { currency: extracted.currency, effective_date: extracted.effective_date },
    };
    await emitOpsRegisterRow(supabase, stalePayload);
  }

  // ---- Step 6: build registered_fact row
  const factType = EVENT_TO_FACT_TYPE[eventRow.event_type];
  if (!factType) {
    // Should not reach here (caught at Step 3) but defensive.
    await markStripeEventProcessed(supabase, stripeEventId);
    await supabase.rpc("pgmq_delete_finops_writer", { p_msg_id: msg.msg_id });
    outcome.action = "skipped";
    outcome.error = `no fact_type mapping for ${eventRow.event_type}`;
    return outcome;
  }

  const factRow: RegisteredFactRow = {
    counterparty_id: resolution.counterparty_id,
    stripe_customer_id: extracted.stripe_customer_id,
    stripe_subscription_id: extracted.stripe_subscription_id,
    fact_type: factType,
    currency: extracted.currency,
    amount_minor: extracted.amount_minor,
    amount_minor_eur: fx.amount_minor_eur,
    effective_date: extracted.effective_date,
    fx_rate_ecb: fx.fx_rate_ecb,
    fx_rate_stripe: fx.fx_rate_stripe,
    fx_source: fx.fx_source,
    metadata: { ...extracted.metadata, stripe_event_id: stripeEventId, resolution_strategy: resolution.strategy_used, resolution_confidence: resolution.confidence },
    source_reference: extracted.source_reference,
  };

  // ---- Step 7: insert (idempotency layer 3 — source_reference unique constraint)
  const { error: insertErr } = await supabase
    .schema("finops")
    .from("registered_fact")
    .insert(factRow);

  if (insertErr) {
    const msgLower = (insertErr.message ?? "").toLowerCase();
    // Treat duplicate as success (idempotency layer 3 absorbed a re-process).
    if (insertErr.code === "23505" || msgLower.includes("duplicate") || msgLower.includes("unique constraint")) {
      await markStripeEventProcessed(supabase, stripeEventId, {
        fxRateEcb: fx.fx_rate_ecb,
        fxRateStripe: fx.fx_rate_stripe,
        fxSource: fx.fx_source,
      });
      await supabase.rpc("pgmq_delete_finops_writer", { p_msg_id: msg.msg_id });
      outcome.action = "duplicate";
      outcome.fact_type = factType;
      outcome.counterparty_id = resolution.counterparty_id;
      return outcome;
    }

    // Transient or schema error — bump attempts; archive if budget exhausted.
    const retryInfo = await incrementStripeEventAttempts(supabase, stripeEventId, insertErr.message);
    if (retryInfo.attempts >= MAX_RETRIES) {
      const dlqPayload: OpsRegisterEmitPayload = {
        ops_class: "dlq_event_max_retries",
        summary:
          `stripe_event_id ${stripeEventId} (type=${eventRow.event_type}) exhausted retry budget (${MAX_RETRIES}); archived to finops_writer_dlq. Last error: ${insertErr.message.slice(0, 400)}`,
        severity: "high",
        stripe_event_id: stripeEventId,
        stripe_customer_id: extracted.stripe_customer_id,
        metadata: { last_error: insertErr.message, event_type: eventRow.event_type, attempts: retryInfo.attempts },
      };
      await emitOpsRegisterRow(supabase, dlqPayload, {
        operatorRunbookPath: "scripts/finops_dlq_drain.py",
      });
      await supabase.rpc("pgmq_archive_finops_writer", { p_msg_id: msg.msg_id });
      outcome.action = "archived";
      outcome.error = insertErr.message;
      return outcome;
    }

    // Leave the message on the queue; pgmq visibility expires and another worker run picks it up.
    outcome.action = "retried";
    outcome.error = insertErr.message;
    return outcome;
  }

  // ---- Step 8: success path
  await markStripeEventProcessed(supabase, stripeEventId, {
    fxRateEcb: fx.fx_rate_ecb,
    fxRateStripe: fx.fx_rate_stripe,
    fxSource: fx.fx_source,
  });
  await supabase.rpc("pgmq_delete_finops_writer", { p_msg_id: msg.msg_id });

  outcome.action = "wrote_fact";
  outcome.fact_type = factType;
  outcome.counterparty_id = resolution.counterparty_id;
  return outcome;
}

// =============================================================================
// §4 — DLQ depth check (emits OPS row when threshold exceeded)
// =============================================================================

async function checkDlqDepth(supabase: SupabaseClient): Promise<{ depth: number; alerted: boolean }> {
  const { data, error } = await supabase
    .schema("pgmq")
    .from("q_finops_writer_dlq")
    .select("msg_id", { count: "exact", head: true });

  if (error) {
    console.warn(JSON.stringify({ source: "finops-writer-worker", note: "dlq depth check failed", error: error.message }));
    return { depth: 0, alerted: false };
  }

  // deno-lint-ignore no-explicit-any
  const depth = (data as any)?.count ?? 0;
  if (depth > DLQ_DEPTH_ALERT_THRESHOLD) {
    await emitOpsRegisterRow(supabase, {
      ops_class: "dlq_threshold_exceeded",
      summary: `finops_writer_dlq depth=${depth} exceeds alert threshold ${DLQ_DEPTH_ALERT_THRESHOLD}. Operator drain runbook required.`,
      severity: "critical",
      metadata: { depth, threshold: DLQ_DEPTH_ALERT_THRESHOLD },
    }, { operatorRunbookPath: "scripts/finops_dlq_drain.py" });
    return { depth, alerted: true };
  }
  return { depth, alerted: false };
}

// =============================================================================
// §5 — Deno.serve entry point
// =============================================================================

Deno.serve(async (req) => {
  const startedAt = new Date().toISOString();
  if (req.method !== "POST" && req.method !== "GET") {
    return new Response(JSON.stringify({ error: "method_not_allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json" },
    });
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL");
  const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!supabaseUrl || !supabaseServiceKey) {
    return new Response(
      JSON.stringify({ error: "missing_env", detail: "SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY required" }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }

  const supabase = createClient(supabaseUrl, supabaseServiceKey);

  // ---- Read up to MAX_BATCH messages
  const { data: messages, error: readErr } = await supabase.rpc("pgmq_read_finops_writer", {
    p_qty: MAX_BATCH,
    p_vt: VISIBILITY_TIMEOUT_S,
  });
  if (readErr) {
    return new Response(JSON.stringify({ error: "pgmq_read_failed", detail: readErr.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }

  const outcomes: ProcessOutcome[] = [];
  for (const m of messages ?? []) {
    try {
      const outcome = await processMessage(supabase, m);
      outcomes.push(outcome);
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : String(err);
      console.warn(JSON.stringify({ source: "finops-writer-worker", note: "processMessage threw", msg_id: m.msg_id, error: errMsg }));
      outcomes.push({ msg_id: m.msg_id, stripe_event_id: "", action: "retried", error: errMsg });
    }
  }

  const dlqStatus = await checkDlqDepth(supabase);

  const summary = {
    source: "finops-writer-worker",
    started_at: startedAt,
    completed_at: new Date().toISOString(),
    messages_read: outcomes.length,
    wrote_fact: outcomes.filter((o) => o.action === "wrote_fact").length,
    skipped: outcomes.filter((o) => o.action === "skipped").length,
    duplicate: outcomes.filter((o) => o.action === "duplicate").length,
    retried: outcomes.filter((o) => o.action === "retried").length,
    archived: outcomes.filter((o) => o.action === "archived").length,
    dlq_depth: dlqStatus.depth,
    dlq_alerted: dlqStatus.alerted,
  };
  console.log(JSON.stringify({ ...summary, note: "worker batch complete" }));
  return new Response(JSON.stringify(summary), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
});
