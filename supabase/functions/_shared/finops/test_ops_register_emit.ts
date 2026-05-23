/**
 * Deno tests — ops_register_emit.ts (R4 HLK-ERP convergence).
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W, 2026-05-23).
 *
 * Run: deno test --allow-env supabase/functions/_shared/finops/test_ops_register_emit.ts
 */

import { assertEquals, assertThrows } from "https://deno.land/std@0.224.0/assert/mod.ts";
import {
  buildOpsRegisterRow,
  isValidInitiativeId,
  isValidOpsActionId,
  todayIsoUtc,
  VALID_FINOPS_OPS_CLASSES,
  VALID_OPS_STATUSES,
  VALID_OWNER_CLASSES,
} from "./ops_register_emit.ts";
import type { OpsRegisterEmitPayload } from "./types.ts";

// -----------------------------------------------------------------------------
// Schema constants
// -----------------------------------------------------------------------------
Deno.test("VALID_OWNER_CLASSES — 4 entries (matches Python)", () => {
  assertEquals(VALID_OWNER_CLASSES.size, 4);
  for (const c of ["operator", "system", "agent", "shared"] as const) {
    assertEquals(VALID_OWNER_CLASSES.has(c), true);
  }
});

Deno.test("VALID_OPS_STATUSES — 5 entries (matches Python)", () => {
  assertEquals(VALID_OPS_STATUSES.size, 5);
  for (const s of ["open", "in_progress", "blocked", "closed", "cancelled"] as const) {
    assertEquals(VALID_OPS_STATUSES.has(s), true);
  }
});

Deno.test("VALID_FINOPS_OPS_CLASSES — 8 entries (matches Python)", () => {
  assertEquals(VALID_FINOPS_OPS_CLASSES.size, 8);
});

// -----------------------------------------------------------------------------
// Format validators
// -----------------------------------------------------------------------------
Deno.test("isValidOpsActionId — accepts OPS-NN-NNN; rejects malformed", () => {
  assertEquals(isValidOpsActionId("OPS-81-1"), true);
  assertEquals(isValidOpsActionId("OPS-1-9999"), true);
  assertEquals(isValidOpsActionId("OPS-81-"), false);
  assertEquals(isValidOpsActionId("OPS-81"), false);
  assertEquals(isValidOpsActionId("ops-81-1"), false);
  assertEquals(isValidOpsActionId(""), false);
});

Deno.test("isValidInitiativeId — accepts INIT-NAME-NN; rejects malformed", () => {
  assertEquals(isValidInitiativeId("INIT-OPENCLAW_AKOS-81"), true);
  assertEquals(isValidInitiativeId("INIT-A-1"), true);
  assertEquals(isValidInitiativeId("init-openclaw_akos-81"), false);
  assertEquals(isValidInitiativeId("INIT-81"), false);
  assertEquals(isValidInitiativeId(""), false);
});

Deno.test("todayIsoUtc — returns YYYY-MM-DD format", () => {
  const today = todayIsoUtc();
  assertEquals(today.length, 10);
  assertEquals(today.match(/^\d{4}-\d{2}-\d{2}$/) !== null, true);
});

// -----------------------------------------------------------------------------
// buildOpsRegisterRow — happy path + per-ops_class routing
// -----------------------------------------------------------------------------
Deno.test("buildOpsRegisterRow — counterparty_resolution_failed routes to Business Controller / operator", () => {
  const payload: OpsRegisterEmitPayload = {
    ops_class: "counterparty_resolution_failed",
    summary: "Test counterparty failure",
    severity: "high",
    stripe_customer_id: "cus_test",
  };
  const row = buildOpsRegisterRow({ payload, opsActionId: "OPS-81-100" });
  assertEquals(row.ops_action_id, "OPS-81-100");
  assertEquals(row.owner_role, "Business Controller");
  assertEquals(row.owner_class, "operator");
  assertEquals(row.status, "open");
  assertEquals(row.linked_decision_ids, "D-IH-81-W");
  assertEquals(row.originating_initiative_id, "INIT-OPENCLAW_AKOS-81");
  assertEquals(row.title, "FINOPS: counterparty resolution failed");
  assertEquals(row.notes.includes("stripe_customer_id=cus_test"), true);
  assertEquals(row.notes.includes("severity=high"), true);
});

Deno.test("buildOpsRegisterRow — fx_cache_stale routes to System Owner / system", () => {
  const payload: OpsRegisterEmitPayload = {
    ops_class: "fx_cache_stale",
    summary: "ECB cache stale",
    severity: "medium",
  };
  const row = buildOpsRegisterRow({ payload, opsActionId: "OPS-81-101" });
  assertEquals(row.owner_role, "System Owner");
  assertEquals(row.owner_class, "system");
});

Deno.test("buildOpsRegisterRow — dlq_threshold_exceeded routes to System Owner / operator", () => {
  const payload: OpsRegisterEmitPayload = {
    ops_class: "dlq_threshold_exceeded",
    summary: "DLQ depth > 10",
    severity: "critical",
  };
  const row = buildOpsRegisterRow({ payload, opsActionId: "OPS-81-102" });
  assertEquals(row.owner_role, "System Owner");
  assertEquals(row.owner_class, "operator");
});

Deno.test("buildOpsRegisterRow — caller-supplied title overrides default", () => {
  const row = buildOpsRegisterRow({
    payload: {
      ops_class: "fx_cache_stale",
      title: "Custom title",
      summary: "summary",
      severity: "low",
    },
    opsActionId: "OPS-81-103",
  });
  assertEquals(row.title, "Custom title");
});

Deno.test("buildOpsRegisterRow — metadata serialized into notes", () => {
  const row = buildOpsRegisterRow({
    payload: {
      ops_class: "stripe_metadata_missing",
      summary: "missing metadata",
      severity: "low",
      metadata: { event_type: "charge.succeeded", missing_keys: ["hlk_billing_plane"] },
    },
    opsActionId: "OPS-81-104",
  });
  assertEquals(row.notes.includes("metadata="), true);
  assertEquals(row.notes.includes("hlk_billing_plane"), true);
});

// -----------------------------------------------------------------------------
// Validation errors
// -----------------------------------------------------------------------------
Deno.test("buildOpsRegisterRow — invalid ops_action_id throws", () => {
  assertThrows(
    () =>
      buildOpsRegisterRow({
        payload: { ops_class: "fx_cache_stale", summary: "x", severity: "low" },
        opsActionId: "MALFORMED",
      }),
    Error,
    "ops_action_id",
  );
});

Deno.test("buildOpsRegisterRow — invalid originating_initiative_id throws", () => {
  assertThrows(
    () =>
      buildOpsRegisterRow({
        payload: { ops_class: "fx_cache_stale", summary: "x", severity: "low" },
        opsActionId: "OPS-81-1",
        originatingInitiativeId: "malformed",
      }),
    Error,
    "originating_initiative_id",
  );
});

Deno.test("buildOpsRegisterRow — invalid ops_class throws", () => {
  assertThrows(
    () =>
      buildOpsRegisterRow({
        // deno-lint-ignore no-explicit-any
        payload: { ops_class: "not_a_real_class" as any, summary: "x", severity: "low" },
        opsActionId: "OPS-81-1",
      }),
    Error,
    "ops_class",
  );
});

// -----------------------------------------------------------------------------
// Field truncation
// -----------------------------------------------------------------------------
Deno.test("buildOpsRegisterRow — title truncated to 240 chars", () => {
  const longTitle = "x".repeat(300);
  const row = buildOpsRegisterRow({
    payload: { ops_class: "fx_cache_stale", title: longTitle, summary: "s", severity: "low" },
    opsActionId: "OPS-81-1",
  });
  assertEquals(row.title.length, 240);
});

Deno.test("buildOpsRegisterRow — summary truncated to 2048 chars", () => {
  const longSummary = "x".repeat(3000);
  const row = buildOpsRegisterRow({
    payload: { ops_class: "fx_cache_stale", summary: longSummary, severity: "low" },
    opsActionId: "OPS-81-1",
  });
  assertEquals(row.summary.length, 2048);
});

Deno.test("buildOpsRegisterRow — notes truncated to 2048 chars", () => {
  const bigMeta: Record<string, unknown> = {};
  for (let i = 0; i < 200; i++) bigMeta[`k${i}`] = "x".repeat(20);
  const row = buildOpsRegisterRow({
    payload: { ops_class: "fx_cache_stale", summary: "s", severity: "low", metadata: bigMeta },
    opsActionId: "OPS-81-1",
  });
  assertEquals(row.notes.length <= 2048, true);
});
