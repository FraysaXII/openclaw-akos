# `stripe-webhook-handler` (Supabase Edge Function)

Implements **Initiative 14 Wave B3** routing: **KiRBe product** (`kirbe.*`) vs **Holistika company** (`holistika_ops.*`). See [`stripe-billing-two-planes.md`](../../../docs/wip/planning/14-holistika-internal-gtm-mops/reports/stripe-billing-two-planes.md).

## Stripe metadata contract

| Metadata key | Values | Used on |
|--------------|--------|---------|
| **`hlk_billing_plane`** | `kirbe` (default if omitted on subs), `holistika_ops`, `holistika` | `Customer`, `Subscription` |

**Holistika company customers:** set `metadata.hlk_billing_plane=holistika_ops` (and optional `org_label`) on the Stripe Customer. The handler upserts `holistika_ops.stripe_customer_link`.

**Subscriptions:** if `metadata.hlk_billing_plane=holistika_ops` on the subscription, the handler **does not** write `kirbe.subscriptions` (stub logs only). Implement KiRBe SaaS subscription persistence in the same function for `kirbe` plane when your `kirbe` schema is deployed.

### How to set `hlk_billing_plane` (operators)

Use **test mode** or **live mode** consistently with your keys and webhook endpoint.

**1. Stripe Dashboard — existing Customer**

1. Open [Customers](https://dashboard.stripe.com/test/customers) (switch **Test mode** top right if needed).
2. Click the customer → scroll to **Metadata** → **Add metadata** (or **Edit**).
3. **Key:** `hlk_billing_plane`  
   **Value:** `holistika_ops` (Holistika company / CRM billing) or `kirbe` (KiRBe SaaS product).  
4. Save. This fires `customer.updated` and the webhook can upsert `holistika_ops.stripe_customer_link` when the value is `holistika_ops`.

**2. Stripe Dashboard — existing Subscription**

1. Open [Subscriptions](https://dashboard.stripe.com/test/subscriptions) → select the subscription.
2. Find **Metadata** on the subscription object → add `hlk_billing_plane` = `holistika_ops` or `kirbe`.
3. Save. Subscription events will route per this plane (Holistika subs do not write `kirbe.*` in the handler).

**3. New Checkout / Payment Links (server-side)**

When you create a Checkout Session, pass metadata so the **Subscription** or **Customer** inherits it, for example:

- `subscription_data.metadata[hlk_billing_plane]=kirbe` (typical KiRBe SaaS checkout), or  
- Set the **Customer**’s `hlk_billing_plane` before checkout if you already know the plane.

Payment Links: edit the link in the Dashboard and add metadata under the link’s subscription/customer options if your flow supports it, or create customers first with metadata (step 1).

**4. Stripe CLI** (after [`stripe login`](https://stripe.com/docs/stripe-cli))

```bash
stripe customers update cus_REPLACE_ME --metadata hlk_billing_plane=holistika_ops
stripe subscriptions update sub_REPLACE_ME --metadata hlk_billing_plane=kirbe
```

**5. Repo helper (stdlib, no Stripe CLI)**

With `STRIPE_SECRET_KEY` in your shell (same secret key as in Supabase functions):

```bash
py scripts/stripe_set_billing_plane.py --customer cus_XXX --plane holistika_ops --org-label "Staging"
py scripts/stripe_set_billing_plane.py --subscription sub_XXX --plane kirbe
```

**6. Stripe API** (any client library)

Update the Customer or Subscription object with `metadata.hlk_billing_plane` set to `holistika_ops` or `kirbe`. Do **not** set secret keys in git; use env vars or Dashboard [API keys](https://dashboard.stripe.com/apikeys).

### After `STRIPE_SECRET_KEY` + `STRIPE_WEBHOOK_SECRET` are set in Supabase

1. **Webhook URL in Stripe** must be exactly:  
   `https://<project-ref>.supabase.co/functions/v1/stripe-webhook-handler`  
   (same project you deployed to). **Test mode** webhook if using `sk_test_`.
2. **Events:** enable at least the groups in the table below (Dashboard → Webhooks → your endpoint → **Add events**).
3. **`STRIPE_WEBHOOK_SECRET`:** must be the signing secret **for that endpoint** (`whsec_...` shown in the Dashboard for this URL — not the Stripe CLI forwarding secret).
4. **Redeploy** the function after code changes:  
   `npm run supabase -- functions deploy stripe-webhook-handler --no-verify-jwt`
5. **Smoke test:** Dashboard → Webhooks → endpoint → **Send test event** (e.g. `customer.updated`), or `stripe trigger customer.updated` — then **Supabase → Edge Functions → Logs** → expect **200** and JSON logs with `"source":"stripe_webhook"`.
6. **Database (Holistika plane):** after a `customer.updated` for a customer with `hlk_billing_plane=holistika_ops`, check `holistika_ops.stripe_customer_link`.

### Recommended Stripe webhook events (GTM / marketing ops)

Subscribe to these in [Stripe → Developers → Webhooks](https://dashboard.stripe.com/webhooks) so **revenue, funnel, and lifecycle** signals reach Supabase Edge logs (structured JSON) and **Holistika** customers stay linked.

| Group | Event | Why |
|-------|--------|-----|
| **CRM / company billing** | `customer.created`, `customer.updated` | Source of truth for `holistika_ops.stripe_customer_link` when `hlk_billing_plane=holistika_ops`. |
| **SaaS lifecycle** | `customer.subscription.created`, `updated`, `deleted` | KiRBe vs Holistika routing; no `kirbe` writes for Holistika plane. |
| **Cash & dunning** | `invoice.paid`, `invoice.payment_failed`, `invoice.finalized` | MRR / AR signals; handler resolves **Customer** and upserts Holistika link when plane matches. |
| **Acquisition** | `checkout.session.completed` | Funnel / campaign attribution (pair with Checkout `metadata` in your Payment Links or Checkout API). |
| **Payments** | `payment_intent.succeeded`, `payment_intent.payment_failed` | Conversion and failure analytics; same Customer resolution. |
| **Disputes / charges** | `charge.succeeded`, `charge.failed` | Optional operational visibility. |
| **Self-serve** | `billing_portal.session.created` | Portal usage (observability log only; no DB write). |

**Campaign / UTM (optional):** set `metadata` on **Checkout Sessions** or **Payment Links** (e.g. `utm_campaign`, `lead_source`) in Stripe; the handler forwards **structured logs** you can correlate in Edge logs or later ETL—no extra columns required on `stripe_customer_link` until you add a dedicated staging table.

## Supabase CLI on Windows (this repo)

**Do not use** `pip install supabase` — that is the **Python API client**, not the CLI. The CLI is installed here as a **Node devDependency**:

```bash
npm install
```

Then use `npm run supabase -- <command>` (or `npx supabase@latest <command>`). **Global** `npm install -g supabase` is **not supported** by upstream.

### Auth (pick one)

1. **Browser:** `npm run supabase -- login` — complete the browser prompt.
2. **CI / non-interactive:** create a **personal access token** at [Supabase Account → Access Tokens](https://supabase.com/dashboard/account/tokens), then in PowerShell:

   ```powershell
   $env:SUPABASE_ACCESS_TOKEN="sbp_..."
   ```

### Link and deploy

From the **repository root** (where `package.json` and `supabase/` live):

```bash
npm run supabase -- link --project-ref <YOUR_PROJECT_REF>
npm run supabase -- secrets set STRIPE_SECRET_KEY=sk_test_...
npm run supabase -- secrets set STRIPE_WEBHOOK_SECRET=whsec_...
npm run supabase -- functions deploy stripe-webhook-handler
```

1. Register the function URL in [Stripe webhooks](https://dashboard.stripe.com/webhooks) — use the **recommended events** table above (minimum: all rows in the first three groups for parity with `index.ts`).
2. Copy the endpoint **Signing secret** (`whsec_...`) and run `npm run supabase -- secrets set STRIPE_WEBHOOK_SECRET=whsec_...`, then redeploy if needed.
3. Send test events with Stripe CLI (`stripe trigger customer.created`, etc.) and confirm **200** and structured JSON in Edge logs.

## Preconditions

- Phase 3 DDL applied (`holistika_ops.stripe_customer_link` exists). See [`scripts/sql/i14_phase3_staging/`](../../../scripts/sql/i14_phase3_staging/README.md).
