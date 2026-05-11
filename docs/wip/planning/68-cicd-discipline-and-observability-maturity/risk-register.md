---
linked_initiative: I68
last_review: 2026-05-10
---

# I68 Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---:|:---:|:---|
| R-IH-68-1 | Vendor lock-in on chosen visual-regression tool | M | M | P1 chooses a tool with cleanest export path (baselines + history exportable). Argos GitHub-acquisition is a small risk vector if GitHub deprecates. Lost Pixel as fallback (open-source escape hatch). |
| R-IH-68-2 | Build-time target unachievable for some repos | M | L | Per-repo target in `REPOSITORY_REGISTRY.csv` (D-IH-68-E). Legacy `/dashboard` tree in `boilerplate` is decommission-queued; not a hard blocker. |
| R-IH-68-3 | Sentry quota exhaustion at high traffic | L | M | P4 sample-rate strategy (D-IH-68-C). Monitor monthly events; switch to Sentry's Team plan ($26/mo for 50k events) if free tier breached. |
| R-IH-68-4 | InfraMonitor seed scope creep into full product mid-initiative | M | H | Explicit out-of-scope list in master-roadmap §1.2. P7 strictly read-only; any "actions" feature triggers a new I-NN charter. |
| R-IH-68-5 | Visual regression false positives blocking PRs | H | M | P3 includes threshold tuning + per-page overrides + ignore-anti-aliasing options. P1 picks a tool with mature diff algorithms. |
| R-IH-68-6 | CI baseline applied retroactively breaks existing tests | M | M | P5 rolls out as PRs per repo, not bulk apply. Each PR validated independently. Per-repo opt-out documented (D-IH-68-J). |
| R-IH-68-7 | Sentry source-map storage costs as repo count grows | L | L | P4 standardises release lifecycle (delete releases > 90 days). Negligible at current scale. |
| R-IH-68-8 | Vercel preview-protection blocks visual-regression CI from accessing previews | M | H | P3 documents shareable-preview-link OR vercel-bypass-secret pattern. Reusable in CI. |
| R-IH-68-9 | Operator burnout if I68 spans concurrently with active I66 | M | M | I68 explicitly chartered, not active; gates on I66 P8 closure. (**Mitigated** 2026-05-09 — I66 closed; I68 promoted active 2026-05-10.) |
| R-IH-68-10 | InfraMonitor v0 reads vendor APIs that rate-limit | L | M | P7 implements client-side caching (~5-min TTL) + Vercel ISR-equivalent on the dashboard. |
| **R-IH-68-11 NEW (Round 2; 2026-05-10)** | InfraMonitor module-namespace prematurely couples with future SaaS multi-tenancy (D-IH-68-K reframe risk) | M | M | v0 stays single-tenant; modules ESM-bundled per route (no shared global state across modules); the multi-tenant boundary is the I69 candidate's first phase; chassis sharing with I62/I64/I65 is **structural** (middleware + brand tokens + audit-log) not **hierarchical** (no shared module data store). The route namespace `/operator/infra-monitor/<module>/` is forward-compatible with module spin-out into a separate Next.js app router shared module or npm package when the I69 spin-out trigger fires. |
| **R-IH-68-12 NEW (Round 2; 2026-05-10)** | Argos GitHub App PR-from-fork permission constraint blocks visual-regression on community PRs | L | M | P3 documents the `pull_request_target` workflow trigger + `vetted-by-owner` PR label pattern; the workflow refuses to run when `github.event.pull_request.head.repo.fork=true` unless the PR carries the vetted label. For the foreseeable future Holistika repos are not community-contribution-heavy so this is a low-volume edge case (currently zero open community PRs across `boilerplate` + `hlk-erp` + `kirbe-platform`). |
