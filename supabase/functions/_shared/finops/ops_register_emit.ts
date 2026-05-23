/**
 * OPS_REGISTER emit helper — TypeScript mirror of akos/hlk_ops_register_emit.py.
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W under D-IH-81-G umbrella, 2026-05-23).
 *
 * Per R4 (HLK-ERP observability convergence): worker writes directly to
 * compliance.ops_register_mirror via service_role. The CSV-side SSOT is updated by the
 * weekly OPS_REGISTER review cadence (operator runbook); the mirror is the live runtime
 * surface that scripts/render_operator_inbox.py reads.
 *
 * Drift between this file and akos/hlk_ops_register_emit.py surfaces as worker test
 * failure (test_ops_register_emit.ts validates the same schema constants).
 */

import type { SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";
import type {
  FinopsOpsClass,
  OpsOwnerClass,
  OpsRegisterEmitPayload,
  OpsStatus,
} from "./types.ts";

// =============================================================================
// §1 — 24-column row shape (mirror Python OpsRegisterRow schema)
// =============================================================================

export interface OpsRegisterRow {
  ops_action_id: string;
  title: string;
  originating_initiative_id: string;
  forwarded_to_initiative_id: string;
  owner_class: OpsOwnerClass;
  owner_role: string;
  status: OpsStatus;
  rice_reach: string;
  rice_impact: string;
  rice_confidence_pct: string;
  rice_effort_person_weeks: string;
  rice_score: string;
  gate_id: string;
  linked_decision_ids: string;
  summary: string;
  operator_runbook_path: string;
  evidence_path: string;
  opened_at: string;
  closed_at: string;
  notes: string;
  last_review_at: string;
  last_review_by: string;
  last_review_decision_id: string;
  methodology_version_at_review: string;
}

export const VALID_OWNER_CLASSES: ReadonlySet<OpsOwnerClass> = new Set<OpsOwnerClass>([
  "operator",
  "system",
  "agent",
  "shared",
]);

export const VALID_OPS_STATUSES: ReadonlySet<OpsStatus> = new Set<OpsStatus>([
  "open",
  "in_progress",
  "blocked",
  "closed",
  "cancelled",
]);

export const VALID_FINOPS_OPS_CLASSES: ReadonlySet<FinopsOpsClass> = new Set<FinopsOpsClass>([
  "counterparty_resolution_failed",
  "stripe_customer_link_lookup_pending",
  "fx_divergence_threshold_exceeded",
  "fx_cache_stale",
  "dlq_threshold_exceeded",
  "dlq_event_max_retries",
  "stripe_webhook_signature_mismatch",
  "stripe_metadata_missing",
]);

// =============================================================================
// §2 — ops_class → owner_role + owner_class routing
// =============================================================================

/**
 * Per R4 routing matrix: each FINOPS ops_class deterministically maps to an owner_role
 * (FK-by-convention to baseline_organisation.csv role_name) + owner_class for the rendered
 * OPERATOR_INBOX surface. The matrix is deliberately small (8 entries) so the worker can
 * resolve routing without consulting external config.
 */
const OPS_CLASS_ROUTING: Record<
  FinopsOpsClass,
  { owner_role: string; owner_class: OpsOwnerClass; default_title: string }
> = {
  counterparty_resolution_failed: {
    owner_role: "Business Controller",
    owner_class: "operator",
    default_title: "FINOPS: counterparty resolution failed",
  },
  stripe_customer_link_lookup_pending: {
    owner_role: "Business Controller",
    owner_class: "system",
    default_title: "FINOPS: stripe_customer_link lookup pending",
  },
  fx_divergence_threshold_exceeded: {
    owner_role: "Business Controller",
    owner_class: "operator",
    default_title: "FINOPS: FX divergence threshold exceeded (>0.5%)",
  },
  fx_cache_stale: {
    owner_role: "System Owner",
    owner_class: "system",
    default_title: "FINOPS: ECB FX cache stale; used fallback",
  },
  dlq_threshold_exceeded: {
    owner_role: "System Owner",
    owner_class: "operator",
    default_title: "FINOPS: DLQ depth threshold exceeded",
  },
  dlq_event_max_retries: {
    owner_role: "System Owner",
    owner_class: "operator",
    default_title: "FINOPS: DLQ event exhausted retry budget",
  },
  stripe_webhook_signature_mismatch: {
    owner_role: "System Owner",
    owner_class: "operator",
    default_title: "FINOPS: Stripe webhook signature mismatch",
  },
  stripe_metadata_missing: {
    owner_role: "Business Controller",
    owner_class: "system",
    default_title: "FINOPS: Stripe event missing hlk_* metadata",
  },
};

// =============================================================================
// §3 — Format validators (mirror Python regex pattern checks)
// =============================================================================

const OPS_ACTION_ID_RE = /^OPS-\d{1,3}-\d{1,4}$/;
const INITIATIVE_ID_RE = /^INIT-[A-Z_]+-\d{1,3}$/;
const ISO_DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

export function isValidOpsActionId(s: string): boolean {
  return OPS_ACTION_ID_RE.test(s);
}

export function isValidInitiativeId(s: string): boolean {
  return INITIATIVE_ID_RE.test(s);
}

export function todayIsoUtc(): string {
  return new Date().toISOString().slice(0, 10);
}

// =============================================================================
// §4 — Build OPS_REGISTER row from EmitPayload
// =============================================================================

export interface BuildOpsRowArgs {
  payload: OpsRegisterEmitPayload;
  opsActionId: string; // caller must provide; sequence uniqueness is caller responsibility
  originatingInitiativeId?: string; // defaults to INIT-OPENCLAW_AKOS-81
  linkedDecisionIds?: string; // semicolon-list; defaults to D-IH-81-W
  openedAt?: string; // ISO YYYY-MM-DD; defaults to today UTC
  operatorRunbookPath?: string;
}

export function buildOpsRegisterRow(args: BuildOpsRowArgs): OpsRegisterRow {
  const {
    payload,
    opsActionId,
    originatingInitiativeId = "INIT-OPENCLAW_AKOS-81",
    linkedDecisionIds = "D-IH-81-W",
    openedAt,
    operatorRunbookPath = "",
  } = args;

  if (!isValidOpsActionId(opsActionId)) {
    throw new Error(`ops_action_id must match OPS-<num>-<seq>; got '${opsActionId}'`);
  }
  if (!isValidInitiativeId(originatingInitiativeId)) {
    throw new Error(
      `originating_initiative_id must match INIT-<NAME>-<num>; got '${originatingInitiativeId}'`,
    );
  }
  if (!VALID_FINOPS_OPS_CLASSES.has(payload.ops_class)) {
    throw new Error(`ops_class '${payload.ops_class}' not in VALID_FINOPS_OPS_CLASSES`);
  }

  const routing = OPS_CLASS_ROUTING[payload.ops_class];
  const opened = openedAt && ISO_DATE_RE.test(openedAt) ? openedAt : todayIsoUtc();
  const title = payload.title ?? routing.default_title;

  // Merge stripe_event_id + stripe_customer_id + metadata into notes for downstream audit.
  const notesParts: string[] = [];
  if (payload.stripe_event_id) notesParts.push(`stripe_event_id=${payload.stripe_event_id}`);
  if (payload.stripe_customer_id) notesParts.push(`stripe_customer_id=${payload.stripe_customer_id}`);
  if (payload.metadata && Object.keys(payload.metadata).length > 0) {
    notesParts.push(`metadata=${JSON.stringify(payload.metadata)}`);
  }
  notesParts.push(`severity=${payload.severity}`);
  notesParts.push(`source=finops-writer-worker`);

  return {
    ops_action_id: opsActionId,
    title: title.slice(0, 240),
    originating_initiative_id: originatingInitiativeId,
    forwarded_to_initiative_id: "",
    owner_class: routing.owner_class,
    owner_role: routing.owner_role,
    status: "open",
    rice_reach: "",
    rice_impact: "",
    rice_confidence_pct: "",
    rice_effort_person_weeks: "",
    rice_score: "",
    gate_id: "",
    linked_decision_ids: linkedDecisionIds,
    summary: payload.summary.slice(0, 2048),
    operator_runbook_path: operatorRunbookPath,
    evidence_path: payload.evidence_path ?? "",
    opened_at: opened,
    closed_at: "",
    notes: notesParts.join("; ").slice(0, 2048),
    last_review_at: "",
    last_review_by: "",
    last_review_decision_id: "",
    methodology_version_at_review: "",
  };
}

// =============================================================================
// §5 — Insert into compliance.ops_register_mirror (DB write)
// =============================================================================

/**
 * Allocate a fresh OPS-81-<seq> id by querying the current max ops_action_id where
 * originating_initiative_id = INIT-OPENCLAW_AKOS-81 + ops_action_id LIKE 'OPS-81-%'.
 *
 * Caller is responsible for ensuring sequence uniqueness under concurrency
 * (the worker is single-instance per current architecture; concurrency revisited at scale).
 */
export async function nextOpsActionId(
  supabase: SupabaseClient,
  initiativeNum: number = 81,
): Promise<string> {
  const prefix = `OPS-${initiativeNum}-`;
  const { data, error } = await supabase
    .schema("compliance")
    .from("ops_register_mirror")
    .select("ops_action_id")
    .like("ops_action_id", `${prefix}%`)
    .order("ops_action_id", { ascending: false })
    .limit(1);

  if (error) {
    throw new Error(`nextOpsActionId: query failed: ${error.message}`);
  }

  let nextSeq = 1;
  if (data && data.length > 0 && data[0].ops_action_id) {
    const m = data[0].ops_action_id.match(/^OPS-\d+-(\d+)$/);
    if (m) nextSeq = parseInt(m[1], 10) + 1;
  }
  return `${prefix}${nextSeq}`;
}

export interface EmitResult {
  ops_action_id: string;
  inserted: boolean;
  error: string | null;
}

/**
 * Emit one OPS_REGISTER row to compliance.ops_register_mirror.
 *
 * Returns {ops_action_id, inserted, error}. Never throws — emit failures must not crash
 * the worker (a missed OPS row is operator-visible via DLQ inspection; a crashed worker
 * is invisible and blocks all FINOPS event processing).
 */
export async function emitOpsRegisterRow(
  supabase: SupabaseClient,
  payload: OpsRegisterEmitPayload,
  opts: {
    initiativeNum?: number;
    linkedDecisionIds?: string;
    operatorRunbookPath?: string;
  } = {},
): Promise<EmitResult> {
  const initiativeNum = opts.initiativeNum ?? 81;
  let opsActionId: string;
  try {
    opsActionId = await nextOpsActionId(supabase, initiativeNum);
  } catch (err) {
    return {
      ops_action_id: "",
      inserted: false,
      error: `nextOpsActionId failed: ${err instanceof Error ? err.message : String(err)}`,
    };
  }

  let row: OpsRegisterRow;
  try {
    row = buildOpsRegisterRow({
      payload,
      opsActionId,
      originatingInitiativeId: `INIT-OPENCLAW_AKOS-${initiativeNum}`,
      linkedDecisionIds: opts.linkedDecisionIds,
      operatorRunbookPath: opts.operatorRunbookPath,
    });
  } catch (err) {
    return {
      ops_action_id: opsActionId,
      inserted: false,
      error: `buildOpsRegisterRow failed: ${err instanceof Error ? err.message : String(err)}`,
    };
  }

  const { error } = await supabase
    .schema("compliance")
    .from("ops_register_mirror")
    .insert(row);

  if (error) {
    console.warn(
      JSON.stringify({
        source: "ops_register_emit",
        note: "insert into compliance.ops_register_mirror failed",
        ops_action_id: opsActionId,
        ops_class: payload.ops_class,
        error: error.message,
      }),
    );
    return { ops_action_id: opsActionId, inserted: false, error: error.message };
  }

  console.log(
    JSON.stringify({
      source: "ops_register_emit",
      note: "OPS row emitted",
      ops_action_id: opsActionId,
      ops_class: payload.ops_class,
      severity: payload.severity,
    }),
  );

  return { ops_action_id: opsActionId, inserted: true, error: null };
}
