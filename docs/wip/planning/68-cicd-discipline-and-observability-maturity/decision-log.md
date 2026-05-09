---
linked_initiative: I68
last_review: 2026-05-09
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
