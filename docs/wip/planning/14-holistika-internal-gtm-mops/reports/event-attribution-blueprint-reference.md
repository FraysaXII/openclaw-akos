# Event and attribution blueprint — reference only (Initiative 14)

**Classification:** Reference — **not** canonical process or schema authority. Production DDL follows [`sql-proposal-stack-20260417.md`](sql-proposal-stack-20260417.md) and operator SQL gate ([`operator-sql-gate.md`](operator-sql-gate.md)).

**Stripe billing:** Two planes — [`stripe-billing-two-planes.md`](stripe-billing-two-planes.md); Edge handler [`supabase/functions/stripe-webhook-handler/README.md`](../../../../../supabase/functions/stripe-webhook-handler/README.md).

**ERP:** [TEAM_SOTA_HLK_ERP.md](TEAM_SOTA_HLK_ERP.md) — internal shell reads mirrors / `holistika_ops`; marketing pixels are **not** required on ERP.

---

## Implementation homes

| Layer | Location | Role |
|-------|----------|------|
| Public marketing site | `root_cd/boilerplate` (Next.js 14) | GTM, `dataLayer` / `gtag`, Meta pixel, forms |
| Holistika ERP | `root_cd/hlk-erp` (Next.js 14) | Operator UI; optional **internal-only** product analytics — **do not** send ERP user behavior to ad pixels without policy |
| Data plane | **Holistika Supabase / company data repo** (this monorepo’s Edge + SQL) | `holistika_ops`, compliance mirrors, Stripe Edge webhooks |

---

## 1. Next.js + data layer

- Prefer **structured** pushes (`dataLayer.push` where GTM expects it) for named events (e.g. lead intent, content download) instead of **DOM-only** scraping.
- Align event **names and parameters** with a single taxonomy ([`env_tech_dtp_243`](../../../../references/hlk/compliance/process_list.csv) discipline; Growth/CMO owner).
- Respect Core Web Vitals: validate how GTM loads (e.g. `@next/third-parties/google`) against your Next.js version.

## 2. sGTM + Meta CAPI (optional, Wave E3)

- **Server-side GTM** can reduce client blocking and support consent flows; requires ops ownership and hosting choice.
- **Meta:** use a shared event taxonomy with GA4 where possible; **`event_id`** for browser + server **deduplication** on the same conversion.
- **GDPR / consent:** document legal basis, consent mode, and retention before scaling server-side tags.

## 3. Server-to-database (optional, Wave E3)

- Writing behavioral events from tags into **PostgreSQL** requires **authenticated** endpoints, **RLS**, PII classification, and **no** unauthenticated public inserts.
- Prefer a **SQL proposal** + staging validation before prod.

## 4. Stripe Checkout — marketing linkage

- Pass **`client_reference_id`** and/or **metadata** on Checkout Session / Customer for first-party marketing or session correlation (alongside existing `hlk_billing_plane` — see webhook README).
- **Company plane** facts belong in **`holistika_ops`**; **KiRBe SaaS** product billing stays in **`kirbe.*`**.

## 5. Webhooks (Supabase Edge, company repo)

- Handle `checkout.session.completed` and related events in Edge Functions; **idempotent** processing, signature verification.
- Map Stripe fields into **`holistika_ops`** (or approved schema) — extend README when new columns are added via migration.

## 6. CRM activation (Wave E4)

- **Bi-directional CRM sync** (vendor TBD) is a **decision-log + integration catalog** item—not a default. Field map must align with [`crm-minimum-fields-supabase.md`](crm-minimum-fields-supabase.md).
- **High-intent routing:** any SLA **stricter** than [D-GTM-C1](../decision-log.md) (4 business hours first response) requires an explicit **new** decision row.

## Phased execution (Wave E)

| Phase | Focus |
|-------|--------|
| E1 | Structured data layer + taxonomy + Meta `event_id` dedupe on marketing site |
| E2 | Stripe `client_reference_id` / metadata + webhook persistence into `holistika_ops` per SQL proposal |
| E3 | Optional sGTM + optional server-to-Postgres path (security review) |
| E4 | CRM bi-sync + vendor choice |

---

## Verification

This reference file alone does not trigger `validate_hlk.py`. If you add `process_list` rows or change v3.0 links in the same change set, run [`docs/DEVELOPER_CHECKLIST.md`](../../../../DEVELOPER_CHECKLIST.md).
