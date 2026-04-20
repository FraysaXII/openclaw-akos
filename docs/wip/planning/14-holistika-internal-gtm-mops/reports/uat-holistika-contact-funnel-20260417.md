# UAT — Holistika lead funnels (mock customer E2E)

**Date:** 2026-04-17 (updated 2026-04-18)  
**Initiative:** 14 — Holistika internal GTM (GTM)  
**Runner:** Cursor browser automation + **Supabase MCP** + operator follow-up for inbox / GTM Preview / CRM.

**Public surfaces:** [Contact](https://www.holistikaresearch.com/contact) · [Make a project](https://www.holistikaresearch.com/make-a-project) (when deployed) · Services crosswalk in [`website-service-crosswalk.md`](website-service-crosswalk.md).

**Implementation reference (web team):** [`docs/web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md`](../../../../web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md) — `gtm-data-layer.ts` + `ProjectIntakeForm` Wave E1 wiring; contact API snippets in [`contact-api-implementation.md`](../../../../web/holistika-research-nextjs/contact-api-implementation.md).

---

## Mock customer profile — Alex Rivera

| Field | Value (fictional) |
|-------|-------------------|
| Name | Alex Rivera |
| Email | `alex.rivera.uat+20260418@example.com` |
| Company | Nimbus Labs SL |
| Service interest (contact) | **Marketing Operations** |
| Story | “UAT mock journey 2026-04-18: evaluating Marketing Operations and lead routing. Please discard or tag as test.” |

---

## Evidence — Supabase MCP (MasterData `swrmqpelgoblaquequzb`)

Read-only checks via **Supabase MCP** (2026-04-18):

| Check | Result |
|-------|--------|
| Project | `ACTIVE_HEALTHY`, EU Central |
| `compliance.process_list_mirror` | **1069** rows |
| `compliance.baseline_organisation_mirror` | **65** rows |
| `holistika_ops.stripe_customer_link` | **0** rows (no Holistika-plane Stripe link rows yet) |
| `holistika_ops.billing_account` | **0** rows |
| `kirbe.monitoring_logs` | **2,683,443** rows — governance backlog (retention) |
| Edge Function `stripe-webhook-handler` | **ACTIVE**, **version 5**, `verify_jwt: false` |

**Secrets:** Operators reported **Edge Function secrets** created in Dashboard. MCP **does not** return secret values; pairing **Stripe webhook signing secret** ↔ Supabase `STRIPE_WEBHOOK_SECRET` is a **Dashboard** step (see [`supabase-stripe-health-check-20260418.md`](supabase-stripe-health-check-20260418.md)).

---

## Evidence — Stripe MCP

| Check | Result |
|-------|--------|
| Account | **`acct_1O6DaPAKBWx1b32d`** — **Holistika** (`get_stripe_account_info`) |

**Limitation:** The Stripe MCP toolset in this workspace **does not** expose API operations to **list webhook endpoints**, so URL + subscribed events must be verified in [Stripe Dashboard → Webhooks](https://dashboard.stripe.com/webhooks). Expected URL: `https://swrmqpelgoblaquequzb.supabase.co/functions/v1/stripe-webhook-handler`.

---

## E2E journey A — `/contact` (lightweight form)

| Step | Layer | Expected | Result | Notes |
|------|--------|----------|--------|--------|
| A1 | Browser | Page loads; fields + submit | **PASS** | `/contact` — Name, Email, Company, Service Interest, Message, Send Message |
| A2 | Client | Submit accepted; console shows submit | **PASS** | Console: `Form submitted` / payload from contact bundle |
| A3 | GTM / GA4 / Meta | Tags see `lead_intent` or container events | **PENDING** | **GTM Preview** + **GA4 DebugView** + **Meta Test Events** — operator with access |
| A4 | Backend | Email / CRM / DB | **PENDING** | Confirm in **inbox** or **ingest** (not visible from browser alone) |
| A5 | ERP | Row in Supabase view ERP reads | **PENDING** | Only if A4 writes to MasterData; ERP does **not** get pixels directly |
| A6 | SLA | First response [D-GTM-C1](../decision-log.md) | **PENDING** | 4 business hours — qualitative |

**E2E “closed” for A:** Requires **A3 + A4 PASS** (or explicit **N/A** if stack is intentionally analytics-only). **A1–A2** are **front-end E2E** only.

---

## E2E journey B — `/make-a-project` (`ProjectIntakeForm` + `/api/project-intake`)

| Step | Layer | Expected | Result | Notes |
|------|--------|----------|--------|--------|
| B1 | Browser | Form loads; progress / validation | **PENDING** | Run Browser MCP or manual when intake is in scope for UAT |
| B2 | API | `POST /api/project-intake` returns 200 + `intakeId` | **PENDING** | Use Alex-style test data; tag as UAT |
| B3 | Measurement | After success: `pushLeadIntent` + `gtag('event','lead_intent',…)` with shared `event_id` | **PENDING** | See [`TEAM_SOTA_HLK_WEB.md`](../../../../web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md) §5.4 |
| B4 | Backend persistence | Row or email per your handler | **PENDING** | Confirm storage + PII handling |
| B5 | Supabase / ERP | Optional mirror if you pipe leads | **PENDING** | Same as A5 |

**Code contract (Wave E1):** `lib/gtm-data-layer.ts` + `pushLeadIntent` import; success block **after** API OK — documented verbatim in [`docs/web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md`](../../../../web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md).

---

## Verdict (2026-04-18)

- **Contact funnel (A1–A2):** **PASS** — mock customer can complete submit on live site; measurement and backend rows remain **PENDING** for full E2E.
- **Project intake (B):** **Not executed** in this UAT pass — schedule when `/make-a-project` + API are in regression scope.
- **Data plane:** Supabase mirrors and Edge Function **confirmed via MCP**; Stripe webhooks **Dashboard** (MCP cannot list endpoints).

---

## Round-up

- [`wave-c-d-roundup-20260417.md`](wave-c-d-roundup-20260417.md)
- Health check: [`supabase-stripe-health-check-20260418.md`](supabase-stripe-health-check-20260418.md)
