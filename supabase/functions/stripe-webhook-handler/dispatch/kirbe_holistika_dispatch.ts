/**
 * Dispatch — kirbe + holistika_ops branches of the Stripe webhook handler.
 *
 * Initiative 81 Phase 2 Bundle B-2b refactor (D-IH-81-W, 2026-05-23). EXTRACTED VERBATIM
 * from the original Deno.serve switch statement in supabase/functions/stripe-webhook-handler/index.ts
 * (commit lineage at git blame); behavior preserved bit-for-bit.
 *
 * WHY EXTRACTED: per b2b-wh-b ratification (2026-05-23), the handler became a dispatch
 * orchestrator: FINOPS branch runs FIRST + mandatory (raw event log + pgmq enqueue);
 * kirbe + holistika_ops branches run AFTER + best-effort. This file is the kirbe + holistika
 * branch logic — unchanged semantics, just isolated in its own module so the orchestrator
 * can wrap it in try/catch independent of the FINOPS branch.
 *
 * CONTRACT: dispatchKirbeHolistika(event) is called AFTER signature verification AFTER
 * the FINOPS branch has run. Any throw here is logged but does NOT prevent 200 to Stripe.
 */

import { createClient, type SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";
import Stripe from "https://esm.sh/stripe@14.21.0?target=deno";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY") ?? "", {
  apiVersion: "2024-11-20.acacia",
  httpClient: Stripe.createFetchHttpClient(),
});

function supabaseForSchema(schema: string): SupabaseClient {
  const url = Deno.env.get("SUPABASE_URL") ?? "";
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
  return createClient(url, key, { db: { schema } });
}

function billingPlaneRaw(metadata: Stripe.Metadata | null | undefined): string | undefined {
  return metadata?.hlk_billing_plane?.trim().toLowerCase();
}

function subscriptionCustomerId(sub: Stripe.Subscription): string | null {
  const c = sub.customer;
  if (typeof c === "string") return c;
  if (c && typeof c === "object" && "deleted" in c && (c as Stripe.DeletedCustomer).deleted) {
    return null;
  }
  if (c && typeof c === "object" && "id" in c && typeof (c as Stripe.Customer).id === "string") {
    return (c as Stripe.Customer).id;
  }
  return null;
}

async function resolveSubscriptionPlane(sub: Stripe.Subscription): Promise<{
  plane: "kirbe" | "holistika_ops";
  source: "subscription_metadata" | "customer_inherit" | "default_kirbe";
}> {
  const onSub = billingPlaneRaw(sub.metadata);
  if (onSub === "holistika_ops" || onSub === "holistika") {
    return { plane: "holistika_ops", source: "subscription_metadata" };
  }
  if (onSub === "kirbe") {
    return { plane: "kirbe", source: "subscription_metadata" };
  }
  const cid = subscriptionCustomerId(sub);
  if (!cid) {
    return { plane: "kirbe", source: "default_kirbe" };
  }
  const cust = await fetchCustomer(cid);
  if (!cust) {
    return { plane: "kirbe", source: "default_kirbe" };
  }
  const cp = customerPlane(cust);
  if (cp === "holistika_ops") {
    return { plane: "holistika_ops", source: "customer_inherit" };
  }
  return { plane: "kirbe", source: "customer_inherit" };
}

function customerPlane(c: Stripe.Customer): "kirbe" | "holistika_ops" | "unset" {
  const m = billingPlaneRaw(c.metadata);
  if (m === "holistika_ops" || m === "holistika") return "holistika_ops";
  if (m === "kirbe") return "kirbe";
  return "unset";
}

function logRoute(payload: Record<string, unknown>) {
  console.log(JSON.stringify({ source: "stripe_webhook.kirbe_holistika", ...payload }));
}

async function fetchCustomer(customerId: string): Promise<Stripe.Customer | null> {
  try {
    const c = await stripe.customers.retrieve(customerId);
    if (c.deleted) return null;
    return c as Stripe.Customer;
  } catch {
    return null;
  }
}

function customerIdFromStripeObject(obj: { customer?: string | Stripe.Customer | null }): string | null {
  const c = obj.customer;
  if (typeof c === "string") return c;
  if (c && typeof c === "object" && "id" in c && typeof c.id === "string") return c.id;
  return null;
}

async function upsertHolistikaStripeCustomerLink(customer: Stripe.Customer): Promise<void> {
  if (customerPlane(customer) !== "holistika_ops") return;
  const sb = supabaseForSchema("holistika_ops");
  const orgLabel =
    customer.metadata?.org_label ?? customer.name ?? customer.description ?? customer.id;
  const { error } = await sb.from("stripe_customer_link").upsert(
    {
      org_label: orgLabel,
      stripe_customer_id: customer.id,
      livemode: customer.livemode,
      updated_at: new Date().toISOString(),
    },
    { onConflict: "stripe_customer_id" },
  );
  if (error) console.error("holistika_ops stripe_customer_link upsert:", error);
}

async function routeByCustomerId(
  eventType: string,
  stripeObjectId: string,
  customerId: string | null,
): Promise<void> {
  if (!customerId) {
    logRoute({ event_type: eventType, object_id: stripeObjectId, plane: "unknown", note: "no_customer" });
    return;
  }
  const customer = await fetchCustomer(customerId);
  if (!customer) {
    logRoute({ event_type: eventType, object_id: stripeObjectId, customer_id: customerId, plane: "unknown" });
    return;
  }
  const plane = customerPlane(customer);
  logRoute({
    event_type: eventType,
    object_id: stripeObjectId,
    customer_id: customerId,
    plane: plane === "unset" ? "kirbe_default" : plane,
  });
  if (plane === "holistika_ops") {
    await upsertHolistikaStripeCustomerLink(customer);
  }
}

/**
 * Main dispatch entry for the kirbe + holistika_ops branches.
 * Behavior preserved bit-for-bit from the pre-refactor index.ts switch statement.
 */
export async function dispatchKirbeHolistika(event: Stripe.Event): Promise<void> {
  switch (event.type) {
    case "customer.created":
    case "customer.updated": {
      const customer = event.data.object as Stripe.Customer;
      logRoute({
        event_type: event.type,
        customer_id: customer.id,
        plane: customerPlane(customer) === "holistika_ops" ? "holistika_ops" : "kirbe_or_unset",
      });
      if (customerPlane(customer) === "holistika_ops") {
        await upsertHolistikaStripeCustomerLink(customer);
      }
      break;
    }

    case "customer.subscription.created":
    case "customer.subscription.updated":
    case "customer.subscription.deleted": {
      const sub = event.data.object as Stripe.Subscription;
      const { plane, source } = await resolveSubscriptionPlane(sub);
      logRoute({
        event_type: event.type,
        subscription_id: sub.id,
        plane,
        subscription_plane_source: source,
      });
      if (plane === "holistika_ops") {
        logRoute({
          event_type: event.type,
          note: "holistika_ops subscription — skipping kirbe.subscriptions",
          subscription_id: sub.id,
          subscription_plane_source: source,
        });
        break;
      }
      logRoute({
        event_type: event.type,
        note: "kirbe_plane_subscription_stub",
        subscription_id: sub.id,
        subscription_plane_source: source,
      });
      break;
    }

    case "invoice.paid":
    case "invoice.payment_failed":
    case "invoice.finalized": {
      const inv = event.data.object as Stripe.Invoice;
      const cid = customerIdFromStripeObject(inv);
      await routeByCustomerId(event.type, inv.id, cid);
      break;
    }

    case "checkout.session.completed": {
      const session = event.data.object as Stripe.Checkout.Session;
      const cid = customerIdFromStripeObject(session);
      await routeByCustomerId(event.type, session.id, cid);
      break;
    }

    case "payment_intent.succeeded":
    case "payment_intent.payment_failed": {
      const pi = event.data.object as Stripe.PaymentIntent;
      const cid = customerIdFromStripeObject(pi);
      await routeByCustomerId(event.type, pi.id, cid);
      break;
    }

    case "charge.succeeded":
    case "charge.failed": {
      const ch = event.data.object as Stripe.Charge;
      const cid = customerIdFromStripeObject(ch);
      await routeByCustomerId(event.type, ch.id, cid);
      break;
    }

    case "billing_portal.session.created": {
      const portal = event.data.object as Stripe.BillingPortal.Session;
      const cid = typeof portal.customer === "string" ? portal.customer : portal.customer?.id ?? null;
      logRoute({
        event_type: event.type,
        object_id: portal.id,
        customer_id: cid,
        note: "observability_only",
      });
      break;
    }

    default:
      logRoute({ event_type: event.type, note: "no_op" });
  }
}
