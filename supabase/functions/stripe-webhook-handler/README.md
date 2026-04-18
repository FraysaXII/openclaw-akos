# `stripe-webhook-handler` (Supabase Edge Function)

Implements **Initiative 14 Wave B3** routing: **KiRBe product** (`kirbe.*`) vs **Holistika company** (`holistika_ops.*`). See [`stripe-billing-two-planes.md`](../../../docs/wip/planning/14-holistika-internal-gtm-mops/reports/stripe-billing-two-planes.md).

## Stripe metadata contract

| Metadata key | Values | Used on |
|--------------|--------|---------|
| `akos_billing_plane` | `kirbe` (default if omitted on subs), `holistika_ops` | `Customer`, `Subscription` |

**Holistika company customers:** set `metadata.akos_billing_plane=holistika_ops` (and optional `org_label`) on the Stripe Customer. The handler upserts `holistika_ops.stripe_customer_link`.

**Subscriptions:** if `metadata.akos_billing_plane=holistika_ops` on the subscription, the handler **does not** write `kirbe.subscriptions` (stub logs only). Implement KiRBe SaaS subscription persistence in the same function for `kirbe` plane when your `kirbe` schema is deployed.

### Recommended Stripe webhook events (GTM / marketing ops)

Subscribe to these in [Stripe → Developers → Webhooks](https://dashboard.stripe.com/webhooks) so **revenue, funnel, and lifecycle** signals reach Supabase Edge logs (structured JSON) and **Holistika** customers stay linked.

| Group | Event | Why |
|-------|--------|-----|
| **CRM / company billing** | `customer.created`, `customer.updated` | Source of truth for `holistika_ops.stripe_customer_link` when `akos_billing_plane=holistika_ops`. |
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
