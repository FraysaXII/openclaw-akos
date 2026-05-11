---
linked_initiative: I68
last_review: 2026-05-10
governed_by: docs/references/hlk/compliance/PRECEDENCE.md
---

# I68 Asset Classification

Per `PRECEDENCE.md`, every asset I68 will touch is classified canonical / mirrored / reference. Edits flow canonical-first; mirrored derivations resync; reference-only docs are read.

## Canonical (edit here first)

| Asset | Why canonical |
|:---|:---|
| [`.cursor/rules/akos-deploy-health.mdc`](../../../../.cursor/rules/akos-deploy-health.mdc) | Discipline-layer canonical; I68 extends with new failure patterns + tooling references discovered in P1+. |
| `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORY_REGISTRY.csv` | Source of truth for consumer-repo + hosting-platform mapping. P5 extends with `ci_baseline_version` + `build_time_target_seconds` + `ci_baseline_optouts` columns (PAUSE POINT #3 — canonical CSV gate per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc)). |
| `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-CICD_BASELINE_001.md` (NEW, P5; status `review` at land time, promoted to `active` in P8) | Per-consumer-repo baseline CI workflow definition + per-class baselines (`platform` / `reference` / `internal` / `client-delivery`) + per-platform sections (Vercel + Render) + per-repo opt-out matrix (D-IH-68-J). |
| `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/playwright.config.ts.tmpl` (NEW, P2) | Canonical Playwright config template carrying the 5 standard viewports per `akos-deploy-health.mdc` §"Step 3". |
| `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/github-workflows/ci-baseline.yml.tmpl` (NEW, P5) | GitHub Actions canonical CI baseline workflow template using matrix strategy for Node versions; pulls Playwright config + Sentry release format check + AKOS validators. |
| `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/render/render-baseline.yaml.tmpl` (NEW, P5) | Render canonical YAML stub for `kirbe-platform`-class repos; documents build-cache + healthcheck patterns per `akos-deploy-health.mdc`. |
| `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/SENTRY_DASHBOARD_HOLISTIKA.md` (NEW, P4) | Operator-runbook canonical describing the Sentry deploy-health dashboard; markdown-as-config block operator pastes into Sentry UI dashboard editor. |
| `docs/references/hlk/compliance/process_list.csv` | New rows for ongoing CICD-discipline + observability-monitoring + visual-regression-triage processes (P5: 3 new `env_tech_*` rows; PAUSE POINT #3 — canonical CSV gate). |
| `akos/playwright_baseline.py` (NEW, P2) | Pydantic models `PlaywrightProject` + `PlaywrightBaselineConfig` per [`CONTRIBUTING.md`](../../../../CONTRIBUTING.md) §"Python Code Standards". |
| `akos/sentry_release.py` (NEW, P4) | Pydantic model `SentryReleaseFormatRule` enforcing `{repo_slug}@{sha_short}` template per D-IH-68-I. |
| `akos/cicd_baseline.py` (NEW, P5) | Pydantic model `CICDBaselineRule` reading `REPOSITORY_REGISTRY.csv` extended schema. |
| `akos/repository_registry.py` (extended, P5) | Pydantic schema for `REPOSITORY_REGISTRY.csv` extended with 3 new fields. |

## Mirrored / derived

| Asset | Where it derives from |
|:---|:---|
| Per-consumer-repo `.github/workflows/*.yml` (CI) | Mirrors the SOP-CICD_BASELINE_001 baseline plus per-repo customisations. Drift detected by `check_external_repo_ci_posture.py` (extended in P5). |
| Per-consumer-repo `playwright.config.ts` | Mirrors `_templates/playwright.config.ts.tmpl` (added in P2). Drift detected by `validate_playwright_baseline.py` (P2). |
| Per-consumer-repo Sentry config (`sentry.client.config.ts`, `sentry.server.config.ts`, `next.config.mjs` `withSentryConfig`) | Mirrors the canonical pattern documented in `SENTRY_DASHBOARD_HOLISTIKA.md` (P4). Drift detected by `validate_sentry_release_format.py` (P4). |
| Per-consumer-repo `render.yaml` (Render-hosted repos: `kirbe-platform`) | Mirrors `_templates/render/render-baseline.yaml.tmpl` (P5). |
| Argos baseline storage | Vendor cloud; not in git; correlated via release SHA. |
| Sentry release records | Vendor cloud; correlated via D-IH-68-I cross-repo strategy `{repo_slug}@{sha_short}`. |
| `hlk-erp/app/operator/infra-monitor/page.tsx` (NEW, P7; D-IH-68-K + D-IH-68-L) | InfraMonitor namespace shell (module-picker home + verdict band + future-module placeholder cards). |
| `hlk-erp/app/operator/infra-monitor/health/page.tsx` (NEW, P7) | InfraHealth module landing (per-repo cards + aggregated 3-repo verdict). |
| `hlk-erp/app/operator/infra-monitor/health/[repo-slug]/page.tsx` (NEW, P7) | InfraHealth per-repo drill-in (timeline + recent errors + build-time chart + click-through to vendor consoles). |
| `hlk-erp/lib/infra-monitor/health-aggregator.ts` (NEW, P7) | Stateless server-side aggregator reading Vercel API + Render API + Sentry API; 5-min in-memory TTL via Next.js `cache()`; reads `REPOSITORY_REGISTRY.csv` via `compliance.repository_registry_mirror` Supabase view (no fresh git fetch on every render). |
| `hlk-erp/middleware.ts` (extended, P7) | RBAC for `/operator/infra-monitor/*` at `access_level >= 4` per I62 RBAC matrix; audit-log entry on every load via existing `holistika_ops.audit_log`. |

## Reference-only (read; do not edit here)

- I66 master-roadmap + decision-log (motivation context).
- I63 bless-pattern documentation + scaffolder script (consumer-repo registry foundation).
- Vercel + Render + Sentry vendor docs.
- Visual-regression vendor docs (Argos / Percy / Chromatic / Lost Pixel — for P1 research).
