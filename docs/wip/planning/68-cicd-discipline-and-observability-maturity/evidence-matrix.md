---
linked_initiative: I68
last_review: 2026-05-10
---

# I68 Evidence Matrix

Mapping decisions and risks to artefacts.

| Decision / Risk | Source artefact | Status |
|:---|:---|:---|
| D-IH-68-A (visual regression tool) | P1 research report + Argos PoC PR-comment screenshot + Lost Pixel HTML report comparison | charter — closed in P1 |
| D-IH-68-B (multi-viewport set) | `akos-deploy-health.mdc` §"Step 3" + P2 canonical template `_templates/playwright.config.ts.tmpl` | charter — closed in P2 |
| D-IH-68-C (Sentry sample rates) | I66 P5 `boilerplate/next.config.mjs` (preview-skip pattern already implemented) + P4 `validate_sentry_release_format.py` | partial — closed in P4 |
| D-IH-68-D (CI baseline) | P5 deliverable: `SOP-CICD_BASELINE_001.md` v0.9.0 (review) â†’ v1.0.0 (active P8) | charter — closed in P5 |
| D-IH-68-E (build-time target) | I66 P5 `boilerplate` build at 2m44s after deploy-fix sequence + P6 measured per-repo deltas in `reports/p6-build-time-delta-2026-05-NN.csv` | benchmark established — closed in P6 |
| D-IH-68-F (InfraMonitor v0 location) | I62 Mission Control + I65 Planning Workspace as paradigm precedent + D-IH-68-K reframe places it under product-brand namespace | precedent established — closed in P7 |
| D-IH-68-G (vendor-managed vs self-hosted obs) | P4 cost analysis + Sentry monthly event volume + €500/mo + sovereignty trigger | charter — interim close in P4 |
| D-IH-68-H (visual regression baseline storage) | Vendor selection (D-IH-68-A); cloud-stored via Argos | charter — closed in P1 |
| D-IH-68-I (cross-repo release SHA) | I63 `REPOSITORY_REGISTRY.csv` (consumer-repo source-of-truth) + P4 `validate_sentry_release_format.py` enforces `{repo_slug}@{sha_short}` | foundation established — closed in P4 |
| D-IH-68-J (per-repo opt-out) | P5 SOP YAML opt-out matrix + `REPOSITORY_REGISTRY.csv ci_baseline_optouts` JSON column | charter — closed in P5 |
| **D-IH-68-K NEW (Round 2)** (InfraMonitor architectural reframe) | [BRAND_ARCHITECTURE.md](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md) Branded House tree + this master-roadmap §0.1 reframe + `decision-log.md` D-IH-68-K full record + `risk-register.md` R-IH-68-11 NEW | **closed in P0** (this plan) |
| **D-IH-68-L NEW (Round 2)** (route namespace `/operator/infra-monitor/`) | This master-roadmap §0.1 + §1.1 + `decision-log.md` D-IH-68-L full record; operationalised in P7 TSX route files under `hlk-erp/app/operator/infra-monitor/` | **closed in P0** (this plan); operationalised in P7 |
| R-IH-68-1 (vendor lock-in) | D-IH-68-A export-path criterion + Lost Pixel fallback documented in P1 vendor research report | covered |
| R-IH-68-2 (build-time unachievable) | I66 P5 incident catalogue + `akos-deploy-health.mdc` Failure 1-5 + P6 per-repo `build_time_target_seconds` | covered |
| R-IH-68-3 (Sentry quota) | D-IH-68-C sample rate tuning + Sentry Team plan ($26/mo for 50k events) trigger | covered |
| R-IH-68-4 (InfraMonitor scope creep) | Master-roadmap §1.2 explicit out-of-scope + P7 strictly read-only + actions feature triggers I69 charter | covered |
| R-IH-68-5 (visual regression false positives) | D-IH-68-A vendor selection (mature diff algo criterion) + P3 threshold tuning + per-page overrides | covered |
| R-IH-68-6 (CI baseline breaks existing) | D-IH-68-J opt-out criteria + P5 per-repo PR rollout (boilerplate canary â†’ hlk-erp â†’ kirbe-platform) | covered |
| R-IH-68-7 (Sentry storage costs) | P4 release-lifecycle standardisation (delete > 90 days) + Sentry tier monitoring | covered |
| R-IH-68-8 (preview protection blocks CI) | P3 `pull_request_target` + `VERCEL_AUTOMATION_BYPASS_SECRET` + `x-vercel-protection-bypass` header pattern documented in `SOP-CICD_BASELINE_001.md` | charter — closed in P3 stub + P5 full |
| R-IH-68-9 (operator burnout) | Charter status `charter` not `active`; I66 closed 2026-05-09; I68 promoted active 2026-05-10 with only 4 explicit operator pause-points | covered (mitigated) |
| R-IH-68-10 (vendor API rate limit) | P7 5-min in-memory TTL via Next.js `cache()` + per-vendor try/catch graceful degradation in `health-aggregator.ts` | charter — closed in P7 |
| **R-IH-68-11 NEW (Round 2)** (InfraMonitor module-namespace prematurely couples with future SaaS multi-tenancy) | D-IH-68-K reframe + master-roadmap §0.1 + R-IH-68-11 NEW mitigation in `risk-register.md`: v0 single-tenant; modules ESM-bundled per route; multi-tenant boundary is I69 P0; chassis sharing structural not hierarchical | covered (Round-2 NEW) |
| **R-IH-68-12 NEW (Round 2)** (Argos GitHub App PR-from-fork permission constraint) | P3 workflow `pull_request_target` + `vetted-by-owner` label pattern; Holistika repos currently zero open community PRs across `boilerplate` + `hlk-erp` + `kirbe-platform` | covered (Round-2 NEW) |
