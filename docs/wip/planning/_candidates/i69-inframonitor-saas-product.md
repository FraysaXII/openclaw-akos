---
language: en
status: candidate
initiative: I69 — InfraMonitor SaaS product (placeholder; not chartered)
seeded_by: I68 P7 InfraHealth module v0 in `hlk-erp` at `/operator/infra-monitor/health/`
last_review: 2026-05-10
authority: System Owner + CBO + CTO + Brand Manager
trigger_status: pending operator decision (one of three spin-out trigger conditions below)
---

# I69 candidate — InfraMonitor SaaS product (placeholder; not chartered)

> **This is a placeholder, not a charter.** Per I60 / I61 precedent ([`i60-process-list-harmonisation.md`](./i60-process-list-harmonisation.md), [`i61-artifact-process-mapping.md`](./i61-artifact-process-mapping.md)), candidate docs in `_candidates/` are one-page placeholders that document *the next decision moment* without committing to scope or budget. I69 promotes from `candidate` to `chartered` (with a full master-roadmap, decision-log, asset-classification, evidence-matrix, risk-register, files-modified.csv) only when **operator surfaces one of the three spin-out trigger conditions** below.
>
> Scaffolded by I68 P8 closure per [I68 master-roadmap](../68-cicd-discipline-and-observability-maturity/master-roadmap.md) §"P8 — Closure ... I69 candidate scaffold" + [`decision-log.md`](../68-cicd-discipline-and-observability-maturity/decision-log.md) D-IH-68-K (InfraMonitor architectural reframe; v0 stays single-tenant in `hlk-erp`; multi-tenant SaaS spin-out is the I69 moment).

## 1. Scope (high level — refined when chartered)

InfraMonitor evolves from the I68 P7 v0 (single-tenant InfraHealth module in `hlk-erp` operator surface, observing 3 Holistika platform repos: `boilerplate`, `hlk-erp`, `kirbe-platform`) into a **multi-tenant + customer-facing + paid + multi-module SaaS product**.

The evolution path has four orthogonal axes, each of which can be promoted independently when operator decides:

### 1.1 Multi-tenancy

- **v0 (I68 P7)**: single-tenant; reads only Holistika's own Vercel + Render + Sentry data via existing API tokens.
- **I69 v1**: per-tenant Supabase project (or per-tenant `tenant_id` column with RLS on a shared Supabase project — **decision deferred to I69 P0**); per-tenant API-token storage (vault: Supabase Vault or 1Password); per-tenant audit-log scoping; GDPR-controlled customer data deletion + retention policy per tenant.
- **Decision rationale**: per-tenant Supabase project gives strongest isolation but operationally expensive (one project per customer); per-tenant `tenant_id` + RLS scales but couples customer data risk. The decision is the I69 P0 single biggest architectural choice.

### 1.2 Customer-facing surface

- **v0 (I68 P7)**: `/operator/infra-monitor/` inside `hlk-erp` (operator-only via `AccessLevel >= 4` middleware).
- **I69 v1**: public sign-up + login flow (`inframonitor.com` or `app.inframonitor.com` — domain not yet purchased; brand decision per [`BRAND_ARCHITECTURE.md`](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md) which already positions InfraMonitor as a sibling product brand under HLK Tech Lab); marketing pages; pricing page; billing flow (likely Stripe — defer to I69 P0).
- **Decision rationale**: Domain + Stripe + marketing-site stack are downstream of the multi-tenancy decision. The customer-facing surface decisions are mechanical once the tenancy boundary is set.

### 1.3 Paid

- **v0 (I68 P7)**: free; internal Holistika usage only.
- **I69 v1**: paid tier(s); Stripe billing; quota + overage; per-tenant usage metering. Pricing decision: TBD (defer to I69 P0; benchmark vs Sentry $26/mo Team plan, Datadog ~$15/host/mo, Better Uptime $30/mo).
- **Decision rationale**: Pricing is a market-validation question, not an engineering question; defer until I67 RevOps Discovery output ([`docs/wip/planning/67-revops-discovery/`](../67-revops-discovery/)) + at least 3 customer-discovery conversations have surfaced WTP signals.

### 1.4 Multi-module

- **v0 (I68 P7)**: 1 active module (InfraHealth) + 4 placeholder cards rendered as `coming with I69` (AppPulse / TenantHealth / AuditTrail / CostPulse).
- **I69 v1**: each module candidate gets its own charter when operator promotes (the I69 candidate doc *does not* charter the modules; it scaffolds the namespace + meta-product structure that the modules slot into).
- **Module candidates** (one-line scope each; full charter later):
  - **AppPulse** — application-level performance metrics (P50 / P95 / P99 latency per route; error rates; throughput); reads Vercel Analytics + Sentry transactions API. Adjacency: Datadog APM, New Relic, Honeycomb. Differentiator: deeply integrated with InfraHealth deploy view (correlate latency regression with deploy SHA).
  - **TenantHealth** — per-tenant SaaS application health (per-customer error rate, per-customer login success rate, per-customer feature usage). Adjacency: PostHog, Mixpanel, Segment. Differentiator: structured around the tenant abstraction the SaaS already needs internally.
  - **AuditTrail** — per-tenant compliance audit log surface; reads `holistika_ops.audit_log`-equivalent in customer Supabase projects. Adjacency: Drata, Vanta, Tugboat Logic (compliance-focused). Differentiator: read-only audit surface; not a full compliance platform — just the audit-log projection.
  - **CostPulse** — multi-vendor cost projection + alerting (Vercel + Render + Sentry + Stripe + Supabase + AWS); compares actual to budget per service. Adjacency: Vantage, CloudZero, Holori. Differentiator: integrates with the same vendor APIs InfraHealth already reads (no new auth surface).

## 2. Spin-out trigger conditions (any one of three; operator decides)

Per [I68 master-roadmap](../68-cicd-discipline-and-observability-maturity/master-roadmap.md) §"Successor — I69 InfraMonitor SaaS product (candidate; scaffolded P8)":

### 2.1 First paying customer ask

A customer (existing Holistika engagement counterparty or inbound prospect) explicitly asks: *"Can we use your InfraMonitor for our system?"*

- **Recognition signal**: A second message from the same counterparty within 30 days re-asking specifically about InfraMonitor (not generic interest).
- **Action**: Operator promotes I69 candidate to chartered initiative + scopes I69 P0 around the specific customer's stack (Vercel? Render? Sentry? other?) to validate the v1 scope is realistic.

### 2.2 First compliance demand for per-tenant data isolation

An ENISA / ICEX / EU customer requires per-tenant data isolation (per-customer Supabase project; per-customer audit-log boundary; per-customer GDPR-deletion path) that the single-tenant `hlk-erp` namespace cannot satisfy.

- **Recognition signal**: A formal compliance question on a sales / advisory call asking *"Where is our data stored? Can it be deleted on request? Is it isolated from other customers?"* and the answer for the v0 single-tenant InfraMonitor is unsatisfactory.
- **Action**: Operator promotes I69 candidate to chartered initiative + scopes I69 P0 around the multi-tenancy decision (per-tenant Supabase project vs `tenant_id` + RLS) FIRST before any other module work.

### 2.3 Internal scale where Holistika self-monitors > 10 systems

Holistika's own platform-repo count grows past 10 (current: 3 platform repos + ~5 internal repos + some `client-delivery` repos = ~10-15 today); per-system dashboarding becomes a productivity tax even for the operator.

- **Recognition signal**: Operator opens InfraHealth module 3+ times in a week and says *"this is too many cards; I need a way to filter / group / search across systems"*.
- **Action**: Operator promotes I69 candidate to chartered initiative + scopes I69 P0 around the **search + grouping + filtering** UX upgrade (which is a multi-tenant primitive even when used internally — the underlying data model becomes "many tenants, filter to one or many" rather than "show all 3 hardcoded").

## 3. Architecture-extraction scope (anticipated when chartered)

When I69 charters, the `hlk-erp` operator-surface chassis (auth + RBAC + audit-log + brand tokens + Cmd+K + freshness ribbon + locale + time-travel — all I62 deliverables) needs **extraction** into a reusable shared module so InfraMonitor SaaS can consume it without copying-and-pasting from `hlk-erp`. Two options:

- **Option A — Extract to a shared npm package** (`@holistika/operator-chassis` or similar). Pro: clean dependency boundary; clear versioning. Con: package release discipline overhead; major refactor of `hlk-erp` to consume its own chassis as a published package.
- **Option B — Monorepo** (`hlk-erp` + `inframonitor-platform` + future SaaS products as workspaces in a Turborepo/Nx monorepo). Pro: chassis stays in-repo; cross-product refactors are atomic. Con: monorepo tooling overhead; CI complexity; operator-surface chassis becomes shared code that all products depend on (coupling risk).

The decision is the I69 P0 second biggest architectural choice (after multi-tenancy in §1.1).

This is itself a major engineering initiative (multi-week extraction; Stripe billing integration; per-tenant secret vault; multi-tenant Supabase migration; GDPR deletion path). It is **explicitly out of scope** for I68 v0.

## 4. Cross-references

- I68 master-roadmap (the parent initiative that scaffolded this candidate): [`docs/wip/planning/68-cicd-discipline-and-observability-maturity/master-roadmap.md`](../68-cicd-discipline-and-observability-maturity/master-roadmap.md).
- I68 P7 page-spec (the v0 surface this evolves from): [`docs/wip/planning/68-cicd-discipline-and-observability-maturity/reports/p7-page-spec-impeccable-2026-05-10.md`](../68-cicd-discipline-and-observability-maturity/reports/p7-page-spec-impeccable-2026-05-10.md).
- I68 decision-log D-IH-68-K (the architectural reframe that frames this candidate): [`docs/wip/planning/68-cicd-discipline-and-observability-maturity/decision-log.md`](../68-cicd-discipline-and-observability-maturity/decision-log.md).
- BRAND_ARCHITECTURE (positions InfraMonitor as sibling product brand under HLK Tech Lab; primary brand-side input when chartered): [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md`](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md).
- I67 RevOps Discovery (the candidate that surfaces WTP signals before I69 paid-tier pricing decision): [`docs/wip/planning/67-revops-discovery/`](../67-revops-discovery/).
- Sibling candidate docs (precedent for the one-page format): [`i60-process-list-harmonisation.md`](./i60-process-list-harmonisation.md), [`i61-artifact-process-mapping.md`](./i61-artifact-process-mapping.md).
- INITIATIVE_REGISTRY (no row yet — added when chartered): [`docs/references/hlk/compliance/INITIATIVE_REGISTRY.csv`](../../references/hlk/compliance/INITIATIVE_REGISTRY.csv).

## 5. Closure (the candidate file's own lifecycle)

This file stays at `status: candidate` until one of:

- **Promote** — operator decides one of the §2 trigger conditions has fired; this file moves to `docs/wip/planning/69-inframonitor-saas-product/master-roadmap.md` (full charter); a new INITIATIVE_REGISTRY row is added at `status: chartered`; this candidate file is moved to `docs/wip/planning/_candidates/_promoted/i69-inframonitor-saas-product.md` for traceability.
- **Defer** — operator decides the trigger conditions have not fired after 12 months from this file's creation date (2026-05-10 + 12 months = 2027-05-10); this file is amended with a deferral note + `last_review` is bumped; the trigger conditions are re-evaluated.
- **Cancel** — operator decides InfraMonitor v0 is sufficient indefinitely + no SaaS spin-out is desired; this file moves to `docs/wip/planning/_candidates/_cancelled/i69-inframonitor-saas-product.md` with a cancellation rationale.

The candidate file does NOT auto-promote based on the trigger conditions; promotion is always an operator decision.

## 6. What this candidate explicitly is NOT

- **Not a charter** — no master-roadmap, no decision-log, no risk-register, no files-modified.csv. Those land when promoted.
- **Not a budget commitment** — operator has not allocated time / money to this.
- **Not a brand commitment** — `inframonitor.com` is not purchased; the SaaS spin-out brand decision is fresh at I69 P0.
- **Not a competitor analysis** — the §1.4 "Adjacency" lines are sketches, not comparative analysis. Full competitive analysis lands at I69 P0.
- **Not a tech-stack commitment** — Next.js + Supabase + Vercel/Render is the assumed starting point because it's the I68 v0 stack; that decision is re-opened at I69 P0.

## 7. Source

Created by I68 P8 closure (D-IH-68-K + the §"Successor — I69 InfraMonitor SaaS product (candidate; scaffolded P8)" instruction in [I68 master-roadmap](../68-cicd-discipline-and-observability-maturity/master-roadmap.md)).
