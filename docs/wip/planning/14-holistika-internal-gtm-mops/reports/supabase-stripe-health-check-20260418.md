# Supabase + Stripe health check (2026-04-18)

**Purpose:** Snapshot after **production DDL** (Initiative 14 Phase 3) to confirm schema presence and flag remaining backlog. **Not** a full security audit.

**Method:** **Supabase MCP** (`list_projects`, `execute_sql`, `list_edge_functions`) + **Stripe MCP** (`get_stripe_account_info`). Stripe MCP does **not** currently expose webhook-endpoint list operations (see Stripe section).

---

## Supabase — project `MasterData` (EU Central)

**Project ref:** `swrmqpelgoblaquequzb` · **Region:** `eu-central-1` · **Status:** `ACTIVE_HEALTHY` (from `list_projects`).

| Check | Result |
|-------|--------|
| Project status | `ACTIVE_HEALTHY` |
| Postgres | 15.x |
| `compliance.process_list_mirror` | Present, **RLS on**, **1069** rows (`execute_sql` count — matches git `process_list.csv` count) |
| `compliance.baseline_organisation_mirror` | Present, **RLS on**, **65** rows |
| `holistika_ops.stripe_customer_link` | Present, **RLS on**, **0** rows (expected until Holistika-plane Stripe customers are linked) |
| `holistika_ops.billing_account` | Present, **RLS on**, **0** rows |
| Edge Function `stripe-webhook-handler` | **ACTIVE**, **version 5**, `verify_jwt: false` (from `list_edge_functions`) — correct for Stripe-signed requests |
| Legacy `public."Process list"` | Still **0** rows (legacy shell; canonical is git + mirrors) |
| `kirbe.monitoring_logs` | **High volume** — **2,683,443** rows (`execute_sql` count, 2026-04-18) — retention/cost governance still recommended |

**Secrets (Edge Function):** Supabase **Dashboard → Project → Edge Functions → Secrets** holds `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, etc. **MCP cannot read secret values** (by design). If secrets were created and the function was **deployed successfully**, runtime webhook verification can proceed; confirm signing secret matches Stripe’s webhook endpoint in Dashboard.

**Backlog (not “broken,” but intentional follow-up):**

1. Run **`sync_compliance_mirrors_from_csv.py`** on a schedule or after each CSV merge if you require byte-for-byte parity audits.
2. **Stripe customer links:** When `holistika_ops` customers exist in Stripe with `metadata.hlk_billing_plane=holistika_ops`, webhook events should populate `stripe_customer_link` — verify in Dashboard after test events.
3. **Legacy `public` tables** (`standard_process`, old `baseline_organisation`, etc.) — deprecation optional per [`deprecate-legacy-public-proposal.md`](deprecate-legacy-public-proposal.md) (operator gate).

---

## Link to webhook README

Full operator checklist: [`supabase/functions/stripe-webhook-handler/README.md`](../../../../../supabase/functions/stripe-webhook-handler/README.md) (repo root path).

---

## Stripe — account

| Check | Result |
|-------|--------|
| Account ID | **`acct_1O6DaPAKBWx1b32d`** (Stripe MCP `get_stripe_account_info`) |
| Display name | **Holistika** |
| API keys (human) | [Dashboard → API keys](https://dashboard.stripe.com/acct_1O6DaPAKBWx1b32d/apikeys) |

**MCP limitation:** The bundled **Stripe MCP** search/execute catalog in this workspace does **not** include operations to **list or retrieve webhook endpoints** (`/v1/webhook_endpoints`). So webhook URL + subscribed events must be confirmed in [Stripe Dashboard → Developers → Webhooks](https://dashboard.stripe.com/webhooks) (or via Stripe CLI / REST with a secret key outside MCP).

**Expected endpoint URL (production Supabase):**

`https://swrmqpelgoblaquequzb.supabase.co/functions/v1/stripe-webhook-handler`

**Backlog (operator):**

1. Dashboard: endpoint above registered; **event groups** per [`supabase/functions/stripe-webhook-handler/README.md`](../../../../supabase/functions/stripe-webhook-handler/README.md); **test vs live** mode aligned with keys.
2. Signing secret from that endpoint matches **Supabase secret** `STRIPE_WEBHOOK_SECRET` (value not visible via MCP).

---

## Verdict

- **DDL / mirrors:** **OK** — Initiative 14 mirror tables exist and are populated for process/org mirrors.
- **Holistika company billing plane:** **Ready for data**; empty link tables until real customers + webhooks flow.
- **Stripe:** Account healthy; **confirm webhook + secrets** in Dashboard as routine ops.
