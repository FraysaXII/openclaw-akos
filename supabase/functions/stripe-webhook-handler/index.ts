/**
 * Stripe webhook — two billing planes (Initiative 14 Wave B3) + GTM / marketing ops events.
 *
 * - **kirbe** (default): KiRBe SaaS product billing — extend with `kirbe.*` upserts in deployment.
 * - **holistika_ops**: company plane — upserts `holistika_ops.stripe_customer_link` when Customer
 *   metadata `hlk_billing_plane=holistika_ops` (or holistika). Legacy `akos_billing_plane` still read.
 *
 * Subscription lifecycle on holistika plane must **not** write `kirbe.subscriptions`.
 */
import { createClient, SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";
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

/** Canonical Stripe metadata: `hlk_billing_plane`. Falls back to `akos_billing_plane` (deprecated). */
function billingPlaneRaw(metadata: Stripe.Metadata | null | undefined): string | undefined {
  return (
    metadata?.hlk_billing_plane?.trim().toLowerCase() ??
    metadata?.akos_billing_plane?.trim().toLowerCase()
  );
}

function subscriptionPlane(sub: Stripe.Subscription): "kirbe" | "holistika_ops" {
  const m = billingPlaneRaw(sub.metadata);
  if (m === "holistika_ops" || m === "holistika") return "holistika_ops";
  return "kirbe";
}

function customerPlane(c: Stripe.Customer): "kirbe" | "holistika_ops" | "unset" {
  const m = billingPlaneRaw(c.metadata);
  if (m === "holistika_ops" || m === "holistika") return "holistika_ops";
  if (m === "kirbe") return "kirbe";
  return "unset";
}

/** Structured log for Langfuse / Supabase Edge logs (no PII beyond Stripe ids). */
function logRoute(payload: Record<string, unknown>) {
  console.log(JSON.stringify({ source: "stripe_webhook", ...payload }));
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

/** Invoice / checkout / payment events: resolve Customer and upsert if Holistika company plane. */
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

Deno.serve(async (req) => {
  if (req.method !== "POST") {
    return new Response("method not allowed", { status: 405 });
  }

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
    console.error("stripe signature verification failed:", msg);
    return new Response(`webhook signature error: ${msg}`, { status: 400 });
  }

  try {
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
        const plane = subscriptionPlane(sub);
        logRoute({ event_type: event.type, subscription_id: sub.id, plane });
        if (plane === "holistika_ops") {
          logRoute({
            event_type: event.type,
            note: "holistika_ops subscription — skipping kirbe.subscriptions",
            subscription_id: sub.id,
          });
          break;
        }
        logRoute({ event_type: event.type, note: "kirbe_plane_subscription_stub", subscription_id: sub.id });
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

    return new Response(JSON.stringify({ received: true }), {
      headers: { "Content-Type": "application/json" },
      status: 200,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error("stripe webhook handler error:", msg);
    return new Response(`handler error: ${msg}`, { status: 500 });
  }
});
