/**
 * Counterparty resolver — TypeScript mirror of resolve_counterparty_id() in akos/hlk_finops_ledger.py §4.
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W, 2026-05-23).
 *
 * R1 (engagement-model-aware router) — see Bundle B-2 architecture report §3.1.
 *
 * Resolution ladder (highest confidence first):
 *   1. metadata_engagement_id  — stripe_metadata.hlk_engagement_id → counterparty_id  (HIGH)
 *   2. metadata_billing_plane  — stripe_metadata.hlk_billing_plane → counterparty_id  (MEDIUM)
 *   3. stripe_customer_link_lookup  — JOIN holistika_ops.stripe_customer_link        (LOW; resolved via DB)
 *   4. manual_review fallback  — UNRESOLVED + ops_register_payload                   (UNRESOLVED)
 *
 * IMPORTANT: Strategy 3 differs from the Python stub: Python returns UNRESOLVED + a hint,
 * because Python can't easily query Supabase mid-function. THIS TypeScript implementation
 * actually performs the SQL lookup against holistika_ops.stripe_customer_link.
 */

import type { SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";
import {
  COUNTERPARTY_UNRESOLVED,
  type CounterpartyResolutionResult,
  type OpsRegisterEmitPayload,
} from "./types.ts";

// Slug regex (mirror Python RegisteredFactRow.counterparty_id pattern).
const SLUG_RE = /^[a-z0-9_]+$/;

function isValidSlug(s: string): boolean {
  return SLUG_RE.test(s) && s.length >= 2 && s.length <= 64;
}

function normalizeMetaValue(v: unknown): string {
  return String(v ?? "").trim().toLowerCase();
}

/**
 * Resolve a Stripe-origin event to a FINOPS counterparty_id.
 *
 * @param supabase Supabase client with `holistika_ops` schema access (service_role).
 * @param stripeCustomerId Stripe customer id (cus_xxx) or null.
 * @param stripeMetadata Stripe event metadata dict.
 * @param engagementModelIdHint Optional override for testing or worker-side propagation.
 */
export async function resolveCounterpartyId(
  supabase: SupabaseClient | null,
  stripeCustomerId: string | null,
  stripeMetadata: Record<string, unknown> | null,
  engagementModelIdHint?: string,
): Promise<CounterpartyResolutionResult> {
  const meta = stripeMetadata ?? {};

  // -----------------------------------------------------------------
  // Strategy 1: metadata_engagement_id (HIGH confidence)
  // -----------------------------------------------------------------
  if ("hlk_engagement_id" in meta && meta.hlk_engagement_id != null) {
    const engagementId = normalizeMetaValue(meta.hlk_engagement_id);
    if (isValidSlug(engagementId)) {
      return {
        counterparty_id: engagementId,
        strategy_used: "metadata_engagement_id",
        confidence: "high",
        ops_register_payload: null,
      };
    }
  }

  // -----------------------------------------------------------------
  // Strategy 2: metadata_billing_plane (MEDIUM confidence)
  // 'holistika' / 'kirbe' are sentinel non-counterparty values; fall through.
  // -----------------------------------------------------------------
  const billingPlane = normalizeMetaValue(meta.hlk_billing_plane);
  if (billingPlane && !["holistika", "holistika_ops", "kirbe"].includes(billingPlane)) {
    if (isValidSlug(billingPlane)) {
      return {
        counterparty_id: billingPlane,
        strategy_used: "metadata_billing_plane",
        confidence: "medium",
        ops_register_payload: null,
      };
    }
  }

  // -----------------------------------------------------------------
  // Strategy 3: stripe_customer_link_lookup (LOW confidence; DB lookup)
  // -----------------------------------------------------------------
  if (stripeCustomerId && stripeCustomerId.startsWith("cus_") && supabase) {
    try {
      const { data, error } = await supabase
        .from("stripe_customer_link")
        .select("finops_counterparty_id, org_label")
        .eq("stripe_customer_id", stripeCustomerId)
        .maybeSingle();

      if (error) {
        // DB error → fall through to manual_review (don't crash worker on transient DB hiccup).
        console.warn(
          JSON.stringify({
            source: "counterparty_resolver",
            note: "stripe_customer_link lookup failed",
            stripe_customer_id: stripeCustomerId,
            error: error.message,
          }),
        );
      } else if (data && data.finops_counterparty_id) {
        const cid = String(data.finops_counterparty_id).trim().toLowerCase();
        if (isValidSlug(cid)) {
          return {
            counterparty_id: cid,
            strategy_used: "stripe_customer_link_lookup",
            confidence: "low",
            ops_register_payload: null,
          };
        }
      }
    } catch (err) {
      console.warn(
        JSON.stringify({
          source: "counterparty_resolver",
          note: "stripe_customer_link lookup threw",
          stripe_customer_id: stripeCustomerId,
          error: err instanceof Error ? err.message : String(err),
        }),
      );
    }
  }

  // -----------------------------------------------------------------
  // Strategy 4: manual_review fallback (UNRESOLVED + OPS_REGISTER emit)
  // -----------------------------------------------------------------
  const opsPayload: OpsRegisterEmitPayload = {
    ops_class: "counterparty_resolution_failed",
    title: "Counterparty resolution failed for Stripe event",
    summary:
      `Counterparty resolution router exhausted all 3 strategies (metadata_engagement_id, metadata_billing_plane, stripe_customer_link_lookup) for ` +
      `stripe_customer_id=${stripeCustomerId ?? "null"}. ` +
      `Add hlk_engagement_id or hlk_billing_plane to Stripe customer metadata; OR add row to holistika_ops.stripe_customer_link with finops_counterparty_id set; OR insert FINOPS_COUNTERPARTY_REGISTER.csv row.`,
    severity: "high",
    stripe_customer_id: stripeCustomerId,
    metadata: {
      stripe_metadata_keys: Object.keys(meta).sort(),
      engagement_model_id_hint: engagementModelIdHint,
    },
  };

  return {
    counterparty_id: COUNTERPARTY_UNRESOLVED,
    strategy_used: "manual_review",
    confidence: "unresolved",
    ops_register_payload: opsPayload,
  };
}
