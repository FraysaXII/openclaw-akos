---
language: en
status: draft
initiative: 32-holistik-ops-maturation
report_kind: external-team-bundle-index
program_id: shared
plane: ops
authority: Founder + System Owner
last_review: 2026-04-30
audience: ERP team lead + ERP engineering
---

# ERP handoff bundle — Initiative 32 P8 (2026-04-30)

This folder is the dated read-side handoff bundle for the `hlk-erp` repository. 7 documents total. AKOS stays SSOT; ERP consumes via `compliance.*_mirror` tables (RLS read-only) or via this dated bundle when no Postgres access is available.

## Bundle contents

| # | File | Purpose |
|---|------|---------|
| **00** | `00-README.md` (this file) | Bundle index |
| **01** | `01-mirror-schema-map.md` | All 16 compliance mirrors with one example query each |
| **02** | `02-five-axis-integration-spec.md` | One-pager: how ERP screens consume `persona_registry_mirror × channel_touchpoint_registry_mirror` |
| **03** | `03-operator-sql-gate-pointer.md` | Pointer to the operator SQL gate runbook |
| **04** | `04-localisation-policy-pointer.md` | Pointer to the relocated localisation policy SOP |
| **05** | `05-changelog-snippet.md` | I31 + I32 highlights for the ERP team (jargon-audit clean) |
| **06** | `06-team-sota-pointer.md` | Pointer to `TEAM_SOTA_HLK_ERP.md` |

Plus separate companion files in the parent `reports/` folder:

- ERP architecture audit memo: [`../erp-architecture-audit-2026-04-30.md`](../erp-architecture-audit-2026-04-30.md) — uses E13 (`data-ssot.mdc` drift) and E14 (stale `other_documentation/`) findings to recommend the Q10 supersession path + 6 deltas
- 3-PR seed patch for the ERP repo: [`../external-repo-seed-prs/hlk-erp.patch`](../external-repo-seed-prs/hlk-erp.patch)
- Bilingual cover-emails (D-IH-32-P): [`../external-repo-seed-prs/hlk-erp-cover-email-en.md`](../external-repo-seed-prs/hlk-erp-cover-email-en.md) + [`hlk-erp-cover-email-es.md`](../external-repo-seed-prs/hlk-erp-cover-email-es.md)

## Acceptance

ERP team replies on the GitHub PR thread or via direct email (operator forwards) acknowledging:

1. Receipt of this bundle.
2. The Q10 supersession recommendation (akos-mirror.mdc takes precedence over local `data-ssot.mdc`) is acceptable, or proposes an alternative.
3. Schedule for the 6 architecture-level deltas in the audit memo (non-blocking timeline).

## Cross-references

- Initiative 32 master roadmap: [`../../master-roadmap.md`](../../master-roadmap.md)
- Initiative 33 (deferred): ERP prod-readiness gates 1-3 (auth, tenancy RLS, rollback runbook)
- Initiative 44 (deferred): full rewrite of HLK-ERP `data-ssot.mdc` after a clean quarter under supersession
