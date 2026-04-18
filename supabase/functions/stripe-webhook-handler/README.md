# `stripe-webhook-handler` (Supabase Edge Function)

Implements **Initiative 14 Wave B3** routing: **KiRBe product** (`kirbe.*`) vs **Holistika company** (`holistika_ops.*`). See [`stripe-billing-two-planes.md`](../../../docs/wip/planning/14-holistika-internal-gtm-mops/reports/stripe-billing-two-planes.md).

## Stripe metadata contract

| Metadata key | Values | Used on |
|--------------|--------|---------|
| `akos_billing_plane` | `kirbe` (default if omitted on subs), `holistika_ops` | `Customer`, `Subscription` |

**Holistika company customers:** set `metadata.akos_billing_plane=holistika_ops` (and optional `org_label`) on the Stripe Customer. The handler upserts `holistika_ops.stripe_customer_link`.

**Subscriptions:** if `metadata.akos_billing_plane=holistika_ops` on the subscription, the handler **does not** write `kirbe.subscriptions` (stub logs only). Implement KiRBe SaaS subscription persistence in the same function for `kirbe` plane when your `kirbe` schema is deployed.

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

Register the function URL in [Stripe webhooks](https://dashboard.stripe.com/webhooks) and send test events with Stripe CLI (`stripe listen` / `stripe trigger`).

## Preconditions

- Phase 3 DDL applied (`holistika_ops.stripe_customer_link` exists). See [`scripts/sql/i14_phase3_staging/`](../../../scripts/sql/i14_phase3_staging/README.md).
