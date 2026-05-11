---
linked_initiative: I68
last_review: 2026-05-10
authority: Founder + System Owner + CTO + Brand Manager
---

# I68 Decision Log

## D-IH-68-A — Visual regression tool selection

**Question**: Which visual-regression tool does Holistika adopt for consumer-repo CICD?

**Options**: Argos / Percy / Chromatic / Lost Pixel / build-it-ourselves.

**Recommended**: **Argos** (free OSS / $19/mo small team; GitHub-acquired 2024; Playwright-native; Vercel-friendly). Fallback: Lost Pixel (self-hosted free).

**Rationale**: Stack fit (Next.js + Vercel + Playwright) + cost discipline + GitHub-native (we already use GitHub for everything else) + community momentum. Percy is solid but costs scale poorly. Chromatic is best for Storybook-driven shops; we're not Storybook-first today.

**Status**: open — finalised in P1 after deeper research + a free-tier proof-of-concept on `boilerplate`.

## D-IH-68-B — Multi-viewport set

**Question**: Which viewport sizes are mandatory for the multi-viewport Playwright suite?

**Recommended**: 5 standard viewports per `akos-deploy-health.mdc` §"Step 3" — 375×667 (iPhone SE), 414×896 (iPhone 11+), 768×1024 (iPad), 1280×800 (laptop), 1920×1080 (wide). Per-repo opt-out for irrelevant breakpoints (e.g., a desktop-only operator surface might skip mobile).

**Status**: open — finalised in P2.

## D-IH-68-C — Sentry sample-rate strategy

**Question**: Production sample rate (full vs sampled). Preview sample rate (skip vs minimal).

**Recommended (preliminary)**: Production = 1.0 sample rate (capture everything; volume is low at current scale). Preview = 0.0 sample rate (skip — already implemented in `boilerplate` per I66 P5). Re-evaluate when monthly Sentry events exceed free-tier limits.

**Status**: open — finalised in P4.

## D-IH-68-D — Baseline CI workflow contents

**Question**: What's the minimum CI test set every consumer repo must run?

**Recommended (preliminary)**: lint + type-check + unit-test + Playwright smoke + Lighthouse + brand drift gates (where applicable per `BRAND_*` canonicals). Visual regression added in P3. Per-repo augmentations allowed; the baseline is shared.

**Status**: open — finalised in P5.

## D-IH-68-E — Build-time targets

**Question**: Operator stated < 2 min for preview builds. Apply uniformly or per-repo?

**Recommended**: < 2 min for typical Next.js / SPA frontend preview builds. Backend services (Render-hosted Python / Node) get separate targets sized to their nature. Document per-repo target in `REPOSITORY_REGISTRY.csv` (new column `build_time_target_seconds`).

**Status**: open — finalised in P6.

## D-IH-68-F — InfraMonitor v0 location

**Question**: Lives in `hlk-erp` as `/operator/infra-health`, vs new dedicated repo, vs InfraMonitor product repo from day 1.

**Recommended**: `hlk-erp` operator surface for v0. Reuses existing operator-surface paradigm (Mission Control, Planning Workspace). Future full-product split-out to dedicated repo when v1 features (mobile / alerting / multi-tenancy) materialise.

**Status**: open — finalised in P7.

## D-IH-68-G — Self-hosted vs vendor-managed observability long-term

**Question**: Stay on Sentry / Vercel Analytics, or migrate to self-hosted Grafana / Prometheus / Loki at scale?

**Recommended**: Stay vendor-managed for now. Self-hosted requires ops-team capacity that Holistika doesn't have. Reconsider when monthly Sentry costs exceed €500 / month or when sovereignty concerns surface (e.g., EU customer requiring on-prem telemetry).

**Status**: open — finalised in P4 (or P8 closure).

## D-IH-68-H — Visual regression baseline storage

**Question**: Cloud-stored baselines (vendor-managed by Argos / Percy / Chromatic) vs git-stored baselines (in repo or in LFS).

**Recommended**: Cloud-stored via the chosen vendor (per D-IH-68-A). Git-stored baselines bloat repos and merge poorly. Vendor cloud is the standard.

**Status**: open — finalised in P3.

## D-IH-68-I — Cross-repo release SHA correlation

**Question**: How do we correlate a deploy event in repo A with a deploy event in repo B (e.g., when investigating a cross-repo regression)?

**Recommended**: Sentry `release` field = `<repo-slug>@<commit-sha-short>` (e.g., `boilerplate@74f9a95d`). This makes per-release queries unambiguous. Add to InfraMonitor v0 dashboard: per-repo recent releases visible.

**Status**: open — finalised in P4.

## D-IH-68-J — Per-repo opt-out criteria

**Question**: When can a consumer repo skip part of the baseline CI workflow?

**Recommended (preliminary)**:

- **Skip Lighthouse**: backend-only services with no rendered HTML.
- **Skip visual regression**: backend services + repos with high-volatility visual surfaces (e.g., dev sandboxes).
- **Skip locale switching tests**: monolingual repos.
- Documented in each repo's `.akos-bless/ci-posture.json` (extending I63 bless metadata).

**Status**: open — finalised in P5.

## D-IH-68-K — InfraMonitor architectural reframe (Round 2 NEW; closed in P0)

**Question**: How does the I68 charter's "InfraMonitor seed dashboard" relate to the Branded House captured in [BRAND_ARCHITECTURE](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md)? Should it be a flat operator surface peer to I62 / I64 / I65, or a product-brand namespace with internal modules?

**Options**:

1. Keep as flat surface at `/operator/infra-health` peer to I62 / I64 / I65 (charter Round 1).
2. Promote InfraMonitor to product-brand namespace; ship InfraHealth as the first module under `/operator/infra-monitor/health/` (Round 2 reframe).
3. Collapse I62 / I64 / I65 under InfraMonitor as modules.

**Decision (Round 2)**: **Option 2** — InfraMonitor is the product-brand namespace; InfraHealth is its first module. v0 ships in `hlk-erp` reusing the I62 chassis structurally (auth + RBAC + audit-log + brand tokens + Cmd+K + freshness ribbon + locale + time-travel) without absorbing sibling routes. SaaS spin-out (multi-tenant + customer-facing + paid) is the **I69 candidate** scaffolded at P8.

**Rationale**:

- Aligns with the [I66 BRAND_ARCHITECTURE](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md) tree which already positions **InfraMonitor 2026** as a sibling product brand under HLK Tech Lab (alongside MADEIRA / KiRBe / ENVOY).
- Option 3 was wrong on three independent axes:
  - **Audience**: I62 / I64 / I65 serve Holistika's own System Owner (`baseline_organisation.access_level >= 4`); InfraMonitor (as product brand) serves external customers' system owners with multi-tenancy + billing + per-tenant RBAC + data-sovereignty demands.
  - **SaaS intent**: I62 / I64 / I65 are internal Holistika ops; InfraMonitor is commercial intent.
  - **Data sovereignty**: I62 / I64 / I65 read directly from AKOS canonical CSVs + `compliance.*_mirror` Supabase tables (Holistika data); InfraMonitor SaaS would need per-tenant Supabase projects + GDPR-controlled customer data deletion + audit-log scoping per tenant.
- Option 1 would have required renaming `/operator/infra-health` to a product-brand-aware namespace later anyway — the future modules (AppPulse / TenantHealth / AuditTrail / CostPulse) need a parent namespace.

**Owner**: System Owner + Brand Manager.
**Status**: closed in P0 (this plan).
**Cross-references**: [BRAND_ARCHITECTURE.md](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md), [I62 master-roadmap](../62-mission-control/master-roadmap.md), [I64 master-roadmap](../64-governance-mission-control/master-roadmap.md), [I65 master-roadmap](../65-akos-planning-workspace-panel/master-roadmap.md), I69 candidate (scaffolded P8).

## D-IH-68-L — Route namespace `/operator/infra-monitor/` shell + `/operator/infra-monitor/health/` first module sub-route (Round 2 NEW; closed in P0)

**Question**: What's the URL structure for the InfraMonitor product brand inside `hlk-erp` v0 such that future modules slot in without renames?

**Decision (Round 2)**:

- `/operator/infra-monitor/` — namespace shell (module-picker home + verdict band + future-module placeholder cards rendered as `coming with I69`).
- `/operator/infra-monitor/health/` — InfraHealth module landing (per-repo cards + aggregated 3-repo verdict).
- `/operator/infra-monitor/health/[repo-slug]/` — per-repo drill-in (timeline + recent errors + build-time chart).
- Future modules: `/operator/infra-monitor/app-pulse/`, `/operator/infra-monitor/tenant-health/`, `/operator/infra-monitor/audit-trail/`, `/operator/infra-monitor/cost-pulse/` — slot in as additional sub-routes without renaming the namespace shell or InfraHealth module.

**Rationale**: The original charter route `/operator/infra-health` would have collided with future module names (e.g., `/operator/app-pulse` peer would lose the InfraMonitor namespace context). The hierarchical `/operator/<product-brand>/<module>/` pattern is consistent with how product-brand parent + module children are named in software (Vercel `/dashboard/projects/`, Sentry `/issues/`, Stripe `/payments/customers/`).

**Owner**: System Owner.
**Status**: closed in P0 (this plan).
**Operationalised in**: P7 (TSX route files in `hlk-erp/app/operator/infra-monitor/`).
