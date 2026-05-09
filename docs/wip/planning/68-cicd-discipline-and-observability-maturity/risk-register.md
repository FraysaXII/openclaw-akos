---
linked_initiative: I68
last_review: 2026-05-09
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
| R-IH-68-9 | Operator burnout if I68 spans concurrently with active I66 | M | M | I68 explicitly chartered, not active; gates on I66 P8 closure. |
| R-IH-68-10 | InfraMonitor v0 reads vendor APIs that rate-limit | L | M | P7 implements client-side caching (~5-min TTL) + Vercel ISR-equivalent on the dashboard. |
