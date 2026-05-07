---
language: en
status: active
initiative: 65-akos-planning-workspace-panel
report_kind: evidence-matrix
last_review: 2026-05-07
---

# Evidence matrix — Initiative 65

| Id | Claim | Evidence (artefact path) | Status |
|:---|:---|:---|:---|
| E1 | Panel surfaces every initiative folder under `docs/wip/planning/**` without duplication | `app/operator/planning/page.tsx` reads from `governance.planning_workspace_view` joined with GitHub Contents directory listing | charter |
| E2 | 5 user journeys complete in their stated time budgets | `reports/journeys-2026-05-07.md` + Playwright e2e per journey | charter |
| E3 | Markdown rendering is live (not stale) and has graceful fallback | `lib/planning/github-reader.ts` + 5-min Supabase fallback cache; banner copy verified | not yet shipped |
| E4 | Operator-only RBAC enforced on `/operator/planning/*` | Existing middleware + `tests/e2e/planning-rbac.spec.ts` | not yet shipped |
| E5 | Time-travel via `?ref=<sha>` returns historical state without writing to canonical mirrors | Playwright e2e + RLS audit | not yet shipped |
| E6 | Cross-references (`D-IH-NN-X`, `OPS-NN-X`, `INIT-OPENCLAW_AKOS-NN`) resolve to in-app URLs | Unit test on `lib/planning/cross-references.ts` | not yet shipped |
| E7 | i18n parity (en + es) maintained | `pnpm check-i18n-parity` passes | not yet shipped |
| E8 | Lighthouse perf/a11y ≥90 desktop and mobile | Lighthouse CI per-route | not yet shipped |
| E9 | MADEIRA MC hero chip routes to `/operator/planning/` and shows 3 numbers | Playwright link + DOM | not yet shipped |
| E10 | Audit log captures planning report reads | Supabase `holistika_ops.audit_log` row count after Playwright walk | not yet shipped |
| E11 | UAT walks every panel against the live workspace | `reports/uat-i65-2026-05-XX.md` | not yet shipped |
