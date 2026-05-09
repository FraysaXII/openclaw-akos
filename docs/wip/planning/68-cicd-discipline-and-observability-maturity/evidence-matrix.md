---
linked_initiative: I68
last_review: 2026-05-09
---

# I68 Evidence Matrix

Mapping decisions and risks to artefacts.

| Decision / Risk | Source artefact | Status |
|:---|:---|:---|
| D-IH-68-A (visual regression tool) | P1 research report (TBD) + vendor demos + cost analysis | charter |
| D-IH-68-B (multi-viewport set) | `akos-deploy-health.mdc` §"Step 3" | discipline-rule established; charter inherits |
| D-IH-68-C (Sentry sample rates) | I66 P5 `boilerplate/next.config.mjs` (preview-skip pattern already implemented) | partial — production sampling open |
| D-IH-68-D (CI baseline) | P5 deliverable: `SOP-CICD_BASELINE_001.md` | charter |
| D-IH-68-E (build-time target) | I66 P5 `boilerplate` build at 2m44s after deploy-fix sequence | benchmark established |
| D-IH-68-F (InfraMonitor v0 location) | I62 Mission Control + I65 Planning Workspace as paradigm precedent | precedent established |
| D-IH-68-G (vendor-managed vs self-hosted obs) | P4 cost analysis | charter |
| D-IH-68-H (visual regression baseline storage) | Vendor selection (D-IH-68-A) | charter |
| D-IH-68-I (cross-repo release SHA) | I63 `REPOSITORY_REGISTRY.csv` (consumer-repo source-of-truth) | foundation established |
| D-IH-68-J (per-repo opt-out) | P5 SOP + per-repo `.akos-bless/ci-posture.json` | charter |
| R-IH-68-1 (vendor lock-in) | D-IH-68-A export-path criterion | covered |
| R-IH-68-2 (build-time unachievable) | I66 P5 incident catalogue + `akos-deploy-health.mdc` Failure 1-5 | covered |
| R-IH-68-3 (Sentry quota) | D-IH-68-C sample rate tuning | covered |
| R-IH-68-4 (InfraMonitor scope creep) | Master-roadmap §1.2 explicit out-of-scope | covered |
| R-IH-68-5 (visual regression false positives) | D-IH-68-A vendor selection (mature diff algo criterion) | covered |
| R-IH-68-6 (CI baseline breaks existing) | D-IH-68-J opt-out criteria | covered |
| R-IH-68-7 (Sentry storage costs) | P4 release-lifecycle standardisation | covered |
| R-IH-68-8 (preview protection blocks CI) | P3 shareable-preview-link / bypass-secret pattern | charter |
| R-IH-68-9 (operator burnout) | Charter status `charter` not `active`; gates on I66 closure | covered |
| R-IH-68-10 (vendor API rate limit) | P7 client-side cache + ISR | charter |
