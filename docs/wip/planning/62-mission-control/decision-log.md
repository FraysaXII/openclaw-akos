---
language: en
status: active
initiative: 62-mission-control
report_kind: decision-log
last_review: 2026-05-06
---

# I62 Decision Log

Format: ID · question · options considered · decision · rationale · date · status.

## D-IH-62-A — Auth provider

- **Q.** Which auth provider for the operator-only `erp.holistika.com` surface?
- **Options.** (1) Supabase Auth (email + OAuth providers); (2) Auth.js (NextAuth); (3) Clerk; (4) Roll-our-own with NextAuth + Drizzle.
- **Decision.** Supabase Auth (Google Workspace + Microsoft 365 + email magic-link).
- **Rationale.** `@supabase/supabase-js` is already a dep; the same provider stores `holistika_ops.*` operational facts; one vendor; SSO covers the Holistika team's likely identity providers; magic-link covers emergency operator access; portable to Auth.js later if needed without a data migration.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-B — RBAC backbone

- **Q.** What is authoritative for "who sees what"?
- **Options.** (1) New ERP-canonical `roles` enum invented locally; (2) Map to AKOS `baseline_organisation.access_level` (0-6); (3) Group-based (Google Workspace groups).
- **Decision.** Map to AKOS `baseline_organisation.access_level` (0-6), persisted in `holistika_ops.user_role_mapping`.
- **Rationale.** Canonical doctrine already in [`baseline_organisation.csv`](../../../references/hlk/compliance/baseline_organisation.csv); zero new IDs; respects [`akos-mirror.mdc`](https://github.com/FraysaXII/hlk-erp/blob/main/.cursor/rules/akos-mirror.mdc); resync via daily job from `compliance.baseline_organisation_mirror`.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-C — Demo data location

- **Q.** Where does the showcase mode get its data?
- **Options.** (1) Hardcoded JSON in code; (2) Separate `demo.*` schema in the same Supabase project; (3) Separate Supabase project entirely.
- **Decision.** Separate `demo.*` Postgres schema in the same Supabase project; views in `erp.*` route to `demo.*` or `compliance.*` based on session GUC `app.data_mode`.
- **Rationale.** One view definition, two data sources; no duplication; idempotent seeder runs in CI; cheaper than a second Supabase project; isolation enforced by GRANTs (anon can only `SELECT erp.vw_public_health`); future option to split if confidentiality matters more than cost.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-D — Showcase domain

- **Q.** Which subdomain hosts the show-off URL?
- **Options.** (1) `showcase.holistika.com`; (2) `demo.holistika.com`; (3) `madeira.holistika.com`; (4) sub-path on `holistika.com/showcase`.
- **Decision.** `madeira.holistika.com` (memorable, ties to platform name, brand-clean).
- **Rationale.** Memorable for advisors/investors; ties to the platform name visible on `app/tech-lab/project-madeira/page.tsx`; verified `MADEIRA` is **not** in the [`BRAND_JARGON_AUDIT.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md) §4 forbidden list (`AKOS`, `holistika_ops.*`, `topic_*`, `plane`, `*OPS` are forbidden externally; `MADEIRA` is not). Hard isolation from production via separate Vercel project + no `SUPABASE_SERVICE_ROLE_KEY`.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-E — State management library

- **Q.** Server-state and UI-state primitives.
- **Options.** (1) Pure React Context everywhere; (2) Redux Toolkit; (3) TanStack Query + Zustand; (4) SWR + Zustand.
- **Decision.** TanStack Query for server state, Zustand for UI-only state, React Context for auth/locale/density.
- **Rationale.** Industry-standard, dedupe-by-default, server-component-friendly (`@tanstack/react-query` with `HydrationBoundary` for App Router); Zustand is the lightest UI store; React Context is the right tool for cross-tree singletons that don't need a store.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-F — i18n strategy

- **Q.** How do we ship en / es / fr without reaching for `next-intl`?
- **Options.** (1) `next-intl`; (2) Inline JSON dictionary like the Madeira control plane; (3) `react-i18next`.
- **Decision.** Inline `en | es | fr` JSON dictionary, locale toggle in header, default from `navigator.language`.
- **Rationale.** Audience-canonical exception per [`SOP-HLK_LOCALISATION_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_LOCALISATION_001.md); same pattern as `static/madeira_control.html` shape report (I49); no new dependency; portable to `next-intl` later if route-level locale prefixes become important.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-G — Error monitoring

- **Q.** Crash reporting + slow-transaction telemetry.
- **Options.** (1) Sentry free tier; (2) Datadog; (3) Self-hosted GlitchTip.
- **Decision.** Sentry free tier (5k events/mo) with PII scrubber; only crashes + 5xx + slow-transaction alerts.
- **Rationale.** Production hygiene without paying yet; Sentry MCP installed; PII scrubber off by default needs configuration; portable to Datadog later if scale demands it.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-H — Performance budget

- **Q.** What numerical targets enforce in CI?
- **Options.** (1) Lighthouse score ≥ 90 only; (2) Specific Web Vitals + bundle size budgets.
- **Decision.** LCP < 2.5s p75, CLS < 0.1, TBT < 300ms, JS bundle < 250KB gzipped per route, < 100KB per shared chunk.
- **Rationale.** Lighthouse v12 thresholds; Core Web Vitals are the user-facing perf truth; bundle budget prevents accidental dependency bloat; enforced via `@lhci/cli` in CI.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-I — First three personas

- **Q.** Which roles do we design for first?
- **Options.** (1) All 65 baseline_organisation roles; (2) The three most distinct (Founder, Operator, Advisor); (3) Just one (Founder).
- **Decision.** Founder/System Owner (level 6), Operator/PMO (level 4), Advisor (level 1, distance-band-gated, read-only).
- **Rationale.** Covers "my team uses it" + "I show advisors" + "I run it as Founder" — three concrete journeys, one access-level matrix to test against; rest backfills from `baseline_organisation.csv` automatically since RBAC is level-driven.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-J — Founder impersonation

- **Q.** How does the Founder QA the access matrix?
- **Options.** (1) Manage real test users; (2) Built-in "View as <role>" with audit log; (3) Skip it.
- **Decision.** Built-in "View as <role>" in user-nav, amber banner, audit-log entry on start/stop, only available to access_level 6.
- **Rationale.** No fake users; no leaked test credentials; audit trail proves no abuse; common pattern for owner-class apps.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-K — Demo data refresh

- **Q.** How does the demo schema stay non-stale?
- **Options.** (1) Manual seed; (2) Idempotent CI script on every deploy; (3) Scheduled weekly refresh.
- **Decision.** `npm run seed:demo` reads a YAML scenario file and idempotently upserts to `demo.*`; runs in CI on every preview deploy and on showcase deploy.
- **Rationale.** Demos always pristine; no rotting fictional data; idempotency guarantees re-running is safe; YAML scenario file is the single source of truth.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-L — Default theme

- **Q.** Which `ThemeProvider` theme is default?
- **Options.** (1) `system`; (2) `dark-blue` for Mission Control hero, `system` everywhere else.
- **Decision.** `dark-blue` for the Mission Control hero band, `system` for everything else; theme switcher persisted to `holistika_ops.user_preferences`.
- **Rationale.** Mission Control deserves a dramatic hero (per [`DESIGN.md`](../../../../DESIGN.md) tokens); rest follows OS preference; persisted per user so demos look consistent.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-M — Brand-jargon scope

- **Q.** Where does the brand-jargon CI lint apply?
- **Options.** (1) Everywhere; (2) Showcase + marketing surfaces only; (3) Manual review.
- **Decision.** CI gate on `app/showcase/**`, `app/(marketing)/**`, public meta tags, public OG images. Operator surfaces under `app/(operator)/**` are unrestricted.
- **Rationale.** Honors [`BRAND_JARGON_AUDIT.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_JARGON_AUDIT.md) §3 register split (operator surfaces internal, jargon allowed; showcase external, jargon forbidden).
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-N — AI assist surface

- **Q.** Should we wire a chat overlay in v1?
- **Options.** (1) Skip; (2) Cmd+J overlay with Madeira agent backend; (3) Full-screen chat page.
- **Decision.** Small Cmd+J chat overlay grounded in current view via Supabase RPC `mission_control_ask`; backed by AKOS Madeira agent endpoint when configured (env `MADEIRA_AGENT_URL`); falls back gracefully (overlay hidden) when not configured.
- **Rationale.** Optional for v1 capability; designing the surface and API now avoids retrofitting; degrades cleanly when Madeira agent isn't reachable.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-O — Mobile breakpoints

- **Q.** Mobile-first or desktop-first?
- **Options.** (1) Desktop-only; (2) Mobile-first with 320px minimum.
- **Decision.** Mobile-first, 320px minimum, Tailwind sm/md/lg/xl breakpoints; Mission Control "Today" works on a phone with cards stacking vertically.
- **Rationale.** Operators on mobile sometimes (during meetings, in-transit); Tailwind defaults are sensible; not a dramatic cost when shadcn primitives already responsive-aware.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-P — Subdomain layout

- **Q.** Which subdomains exist + governance for new ones.
- **Options.** (1) Sub-paths on `holistika.com`; (2) Per-subdomain Vercel projects; (3) Mix.
- **Decision.** Per-subdomain Vercel projects governed by new canonical AKOS asset `SUBDOMAINS_REGISTRY.md`. Active rows: `madeira.holistika.com` (showcase), `erp.holistika.com` (production), `status.holistika.com` (public health). Reserved (no DNS yet): `api.holistika.com`, `docs.holistika.com`, `kirbe.holistika.com`.
- **Rationale.** Memorable show-off URL distinct from auth-gated production; clean separation; cross-link UX (sign-in CTA on demo, demo CTA on sign-in); future subdomains follow same approval flow as Figma files via PR-to-registry.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-Q — ERP read-side schema

- **Q.** Where do the projection views live?
- **Options.** (1) `compliance.*` (pollutes the canonical mirror schema); (2) `holistika_ops.*` (mixes write-side facts with read-side projections); (3) New `erp.*` schema.
- **Decision.** New `erp.*` schema dedicated to projection views (`erp.vw_*`); `holistika_ops.*` keeps the write-side ERP-canonical tables (`user_role_mapping`, `audit_log`, `user_preferences`, `notifications`); demo mode uses session GUC `app.data_mode` to route the same views to `demo.*` source tables.
- **Rationale.** Verified at planning time via `Glob` over `supabase/migrations/` that `erp.*` doesn't yet exist; one schema = one role; `GRANT SELECT ON ALL TABLES IN SCHEMA erp TO authenticated` is a single statement; keeps `compliance.*` / `finops.*` / `holistika_ops.*` semantically clean.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-R — MCP toolchain

- **Q.** Are any MCPs missing for this initiative?
- **Options.** (1) Request additional MCPs (Cloudflare DNS, GitHub); (2) Use what's installed.
- **Decision.** All required MCPs already installed (Supabase ×2, Sentry, Vercel, Stripe, Langfuse, RunPod, Slack, browser, Postman). No new MCP requests at planning time.
- **Rationale.** Lean execution; if a new need emerges (e.g., Cloudflare DNS during P10.5), surface in the affected phase report and request then.
- **Date.** 2026-05-06 · **Status.** Active.

## D-IH-62-W — P2 deferred pending mirror DDL

- **Q.** Apply the I62 P2 `erp.*` projection-views migration on 2026-05-07 against `MasterData` Supabase project, given prerequisite mirrors are missing?
- **Options.** (1) Apply P2 as-written (fails); (2) Adapt P2 to current schema (column harmonisation) but still missing two mirror tables; (3) Defer P2, apply P1 + P3 only, queue a follow-up (P11) for mirror DDL + view re-application.
- **Decision.** Option 3 — apply P1 (RBAC) + P3 (demo schema) only. Defer P2 pending creation of `compliance.initiative_registry_mirror` and `compliance.ops_register_mirror`. Queue OPS-62-P11.
- **Rationale.** P1 + P3 are independent and self-contained; P2 hits two missing tables (`initiative_registry_mirror`, `ops_register_mirror`) and at least 7 column mismatches; rushing P2 risks polluting `erp.*` with views that always 500. The hlk-erp Mission Control already gracefully degrades when `vw_*` returns nothing (renders Demo banner). Better to land the dependency mirrors first via a clean migration that survives release-gate. See [`reports/migration-application-2026-05-07.md`](reports/migration-application-2026-05-07.md) for the gap detail.
- **Date.** 2026-05-07 · **Status.** Active.
