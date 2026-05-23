/**
 * Deno tests — stripe_event_logger.ts (R3 Layer 1 raw-event idempotency).
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W, 2026-05-23).
 *
 * Run: deno test --allow-env supabase/functions/_shared/finops/test_stripe_event_logger.ts
 */

import { assertEquals } from "https://deno.land/std@0.224.0/assert/mod.ts";
import {
  enqueueFinopsEvent,
  incrementStripeEventAttempts,
  logStripeEvent,
  markStripeEventProcessed,
  type StripeRawEvent,
} from "./stripe_event_logger.ts";

// -----------------------------------------------------------------------------
// Fake Supabase that records the call history.
// -----------------------------------------------------------------------------

type InsertCall = { table: string; row: Record<string, unknown> };
type UpdateCall = { table: string; patch: Record<string, unknown>; whereCol: string; whereVal: unknown };
type SelectCall = { table: string };
type RpcCall = { fn: string; args: unknown };

function makeFakeSupabase(opts: {
  insertError?: { code?: string; message: string } | null;
  rpcError?: { message: string } | null;
  rpcReturn?: number;
  readReturn?: { process_attempts?: number } | null;
} = {}) {
  const inserts: InsertCall[] = [];
  const updates: UpdateCall[] = [];
  const selects: SelectCall[] = [];
  const rpcs: RpcCall[] = [];

  const fluentForTable = (table: string) => ({
    insert: (row: Record<string, unknown>) => {
      inserts.push({ table, row });
      return Promise.resolve({ error: opts.insertError ?? null });
    },
    update: (patch: Record<string, unknown>) => ({
      eq: (col: string, val: unknown) => {
        updates.push({ table, patch, whereCol: col, whereVal: val });
        return Promise.resolve({ error: null });
      },
    }),
    select: (_cols: string) => ({
      eq: (_col: string, _val: unknown) => ({
        maybeSingle: () => {
          selects.push({ table });
          return Promise.resolve({ data: opts.readReturn ?? null, error: null });
        },
      }),
    }),
  });

  return {
    inserts,
    updates,
    selects,
    rpcs,
    client: {
      schema: (_schema: string) => ({
        from: fluentForTable,
      }),
      rpc: (fn: string, args: unknown) => {
        rpcs.push({ fn, args });
        if (opts.rpcError) return Promise.resolve({ data: null, error: opts.rpcError });
        return Promise.resolve({ data: opts.rpcReturn ?? 42, error: null });
      },
    },
  };
}

function makeEvent(overrides: Partial<StripeRawEvent> = {}): StripeRawEvent {
  return {
    id: "evt_test_123",
    type: "charge.succeeded",
    api_version: "2025-09-30.acacia",
    livemode: false,
    request: { id: "req_test" },
    data: { object: { id: "ch_test_abc", amount: 1000, currency: "usd" } },
    ...overrides,
  };
}

// -----------------------------------------------------------------------------
// logStripeEvent
// -----------------------------------------------------------------------------

Deno.test("logStripeEvent — successful insert returns inserted: true", async () => {
  const fake = makeFakeSupabase();
  // deno-lint-ignore no-explicit-any
  const result = await logStripeEvent(fake.client as any, makeEvent());
  assertEquals(result.inserted, true);
  assertEquals(result.duplicate, false);
  assertEquals(result.error, null);
  assertEquals(fake.inserts.length, 1);
  assertEquals(fake.inserts[0].table, "stripe_events");
  assertEquals(fake.inserts[0].row.stripe_event_id, "evt_test_123");
  assertEquals(fake.inserts[0].row.event_type, "charge.succeeded");
});

Deno.test("logStripeEvent — duplicate (PK violation code 23505) returns duplicate: true", async () => {
  const fake = makeFakeSupabase({
    insertError: { code: "23505", message: "duplicate key value violates unique constraint" },
  });
  // deno-lint-ignore no-explicit-any
  const result = await logStripeEvent(fake.client as any, makeEvent());
  assertEquals(result.inserted, false);
  assertEquals(result.duplicate, true);
  assertEquals(result.error, null);
});

Deno.test("logStripeEvent — duplicate (message-string fallback) returns duplicate: true", async () => {
  const fake = makeFakeSupabase({
    insertError: { message: "duplicate key value violates unique constraint" },
  });
  // deno-lint-ignore no-explicit-any
  const result = await logStripeEvent(fake.client as any, makeEvent());
  assertEquals(result.duplicate, true);
});

Deno.test("logStripeEvent — non-duplicate error surfaces error string", async () => {
  const fake = makeFakeSupabase({
    insertError: { code: "08006", message: "connection failure" },
  });
  // deno-lint-ignore no-explicit-any
  const result = await logStripeEvent(fake.client as any, makeEvent());
  assertEquals(result.inserted, false);
  assertEquals(result.duplicate, false);
  assertEquals(result.error, "connection failure");
});

Deno.test("logStripeEvent — missing event.id returns error without crashing", async () => {
  const fake = makeFakeSupabase();
  // deno-lint-ignore no-explicit-any
  const result = await logStripeEvent(fake.client as any, { id: "", type: "charge.succeeded" } as any);
  assertEquals(result.inserted, false);
  assertEquals(result.error, "event missing id or type");
});

// -----------------------------------------------------------------------------
// enqueueFinopsEvent
// -----------------------------------------------------------------------------

Deno.test("enqueueFinopsEvent — calls pgmq_send_finops_writer RPC", async () => {
  const fake = makeFakeSupabase({ rpcReturn: 99 });
  // deno-lint-ignore no-explicit-any
  const result = await enqueueFinopsEvent(fake.client as any, "evt_q_test");
  assertEquals(result.queued, true);
  assertEquals(result.msg_id, 99);
  assertEquals(fake.rpcs.length, 1);
  assertEquals(fake.rpcs[0].fn, "pgmq_send_finops_writer");
  // deno-lint-ignore no-explicit-any
  assertEquals((fake.rpcs[0].args as any).p_event_id, "evt_q_test");
});

Deno.test("enqueueFinopsEvent — empty event id returns error", async () => {
  const fake = makeFakeSupabase();
  // deno-lint-ignore no-explicit-any
  const result = await enqueueFinopsEvent(fake.client as any, "");
  assertEquals(result.queued, false);
  assertEquals(result.msg_id, null);
});

Deno.test("enqueueFinopsEvent — RPC error surfaces but doesn't throw", async () => {
  const fake = makeFakeSupabase({ rpcError: { message: "pgmq not installed" } });
  // deno-lint-ignore no-explicit-any
  const result = await enqueueFinopsEvent(fake.client as any, "evt_x");
  assertEquals(result.queued, false);
  assertEquals(result.error, "pgmq not installed");
});

// -----------------------------------------------------------------------------
// markStripeEventProcessed
// -----------------------------------------------------------------------------

Deno.test("markStripeEventProcessed — updates processed_at + FX columns", async () => {
  const fake = makeFakeSupabase();
  await markStripeEventProcessed(
    // deno-lint-ignore no-explicit-any
    fake.client as any,
    "evt_done",
    { fxRateEcb: "0.925", fxRateStripe: "0.931", fxSource: "ecb_daily" },
  );
  assertEquals(fake.updates.length, 1);
  assertEquals(fake.updates[0].whereCol, "stripe_event_id");
  assertEquals(fake.updates[0].whereVal, "evt_done");
  assertEquals(fake.updates[0].patch.fx_rate_ecb, "0.925");
  assertEquals(fake.updates[0].patch.fx_source, "ecb_daily");
  assertEquals(typeof fake.updates[0].patch.processed_at, "string");
});

// -----------------------------------------------------------------------------
// incrementStripeEventAttempts
// -----------------------------------------------------------------------------

Deno.test("incrementStripeEventAttempts — bumps attempts by 1; persists last_error", async () => {
  const fake = makeFakeSupabase({ readReturn: { process_attempts: 2 } });
  // deno-lint-ignore no-explicit-any
  const result = await incrementStripeEventAttempts(fake.client as any, "evt_retry", "transient timeout");
  assertEquals(result.attempts, 3);
  assertEquals(result.error, null);
  assertEquals(fake.updates.length, 1);
  assertEquals(fake.updates[0].patch.process_attempts, 3);
  assertEquals(fake.updates[0].patch.last_error, "transient timeout");
});

Deno.test("incrementStripeEventAttempts — starts at 1 when row has no prior attempts", async () => {
  const fake = makeFakeSupabase({ readReturn: { process_attempts: undefined } });
  // deno-lint-ignore no-explicit-any
  const result = await incrementStripeEventAttempts(fake.client as any, "evt_first", "first failure");
  assertEquals(result.attempts, 1);
});

Deno.test("incrementStripeEventAttempts — missing row returns attempts=0 + error", async () => {
  const fake = makeFakeSupabase({ readReturn: null });
  // deno-lint-ignore no-explicit-any
  const result = await incrementStripeEventAttempts(fake.client as any, "evt_missing", "x");
  assertEquals(result.attempts, 0);
  assertEquals(result.error, "row not found");
});
