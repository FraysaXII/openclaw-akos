/**
 * Stripe webhook — two billing planes (Initiative 14 Wave B3).
 *
 * - **kirbe** (default): KiRBe SaaS product billing — extend here with `kirbe.*` upserts
 *   in the deployment that owns those tables.
 * - **holistika_ops**: company plane — `customer.*` events with
 *   `metadata.akos_billing_plane=holistika_ops` update `holistika_ops.stripe_customer_link` only.
 *
 * Subscription lifecycle events with `holistika_ops` plane must **not** write `kirbe.subscriptions`.
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

function subscriptionPlane(sub: Stripe.Subscription): "kirbe" | "holistika_ops" {
  const m = sub.metadata?.akos_billing_plane?.trim().toLowerCase();
  if (m === "holistika_ops" || m === "holistika") return "holistika_ops";
  return "kirbe";
}

function customerPlane(c: Stripe.Customer): "kirbe" | "holistika_ops" | "unset" {
  const m = c.metadata?.akos_billing_plane?.trim().toLowerCase();
  if (m === "holistika_ops" || m === "holistika") return "holistika_ops";
  if (m === "kirbe") return "kirbe";
  return "unset";
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
        if (customerPlane(customer) === "holistika_ops") {
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
        break;
      }

      case "customer.subscription.created":
      case "customer.subscription.updated":
      case "customer.subscription.deleted": {
        const sub = event.data.object as Stripe.Subscription;
        const plane = subscriptionPlane(sub);
        if (plane === "holistika_ops") {
          console.log(
            "stripe webhook: holistika_ops subscription event — skipping kirbe.subscriptions",
            sub.id,
          );
          break;
        }
        // kirbe plane: integrate with kirbe.subscriptions in the KiRBe-owns deployment.
        console.log("stripe webhook: kirbe plane subscription event (routing stub)", sub.id);
        break;
      }

      default:
        break;
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
