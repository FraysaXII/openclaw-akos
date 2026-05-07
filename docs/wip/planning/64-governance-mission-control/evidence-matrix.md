---
language: en
status: charter
initiative: 64-governance-mission-control
report_kind: evidence-matrix
last_review: 2026-05-07
---

# Evidence matrix — Initiative 64

| Id | Claim | Evidence (artefact path) | Status |
|:---|:---|:---|:---|
| E1 | Dashboard surfaces canonical AKOS data, not duplicates | `app/operator/governance/external-repos/page.tsx` reads from `compliance.*` mirrors via `lib/governance/data.ts` | charter |
| E2 | Six panels match the operator-stated need | `reports/page-spec-2026-05-06.md` panel-by-panel design + screenshots | charter |
| E3 | Write actions trigger AKOS scripts via GH Actions, not re-implement | `.github/workflows/governance-*.yml` in AKOS | charter |
| E4 | Operator-only RBAC enforced | Playwright e2e in `tests/e2e/governance-rbac.spec.ts` | not yet shipped |
| E5 | Drift-detection signal = same SHA logic as release-gate | `lib/governance/drift.ts` re-uses the same SHA256 stamps from `.akos-bless/*.sha256` | charter |
| E6 | Audit log every write action | Supabase `governance.action_audit` rows | not yet shipped |
| E7 | Demo data mode works without secrets | Existing hlk-erp demo toggle + fixture data in `lib/governance/fixtures.ts` | not yet shipped |
| E8 | i18n parity (en + es) maintained | `pnpm check-i18n-parity` passes | not yet shipped |
| E9 | Lighthouse perf/a11y ≥90 | Lighthouse CI report | not yet shipped |
| E10 | UAT walks every panel against real loops | `reports/uat-i64-2026-05-XX.md` | not yet shipped |
