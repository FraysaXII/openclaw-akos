# Planning initiatives (`docs/wip/planning/`)

Numbered **sequence** below is the recommended reading order for “what came before”: platform roadmap first, then HLK/Madeira, then KM, company formation, and Envoy repo hub. It is **not** a rename of folders (links and git history stay stable); use this index when onboarding or tracing dependencies.

| Seq | Folder | Role |
|:---:|:-------|:-----|
| **01** | [`akos-full-roadmap/`](akos-full-roadmap/) | AKOS-wide phased roadmap and early reports. |
| **02** | [`hlk-on-akos-madeira/`](hlk-on-akos-madeira/) | HLK on AKOS + Madeira: master roadmap, phase plans/reports, **Madeira read-only consolidated plan mirror** [`MADEIRA_HARDENING_CONSOLIDATED_PLAN.md`](hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md), traceability [`reports/madeira-readonly-hardening.md`](hlk-on-akos-madeira/reports/madeira-readonly-hardening.md). |
| **03** | [`hlk-km-knowledge-base/`](hlk-km-knowledge-base/) | HLK KM (Topic–Fact–Source), manifests, follow-up checklists. |
| **04** | [`holistika-company-formation/`](holistika-company-formation/) | Founder / incorporation / governance planning. |
| **05** | [`hlk-vault-envoy-repos/`](hlk-vault-envoy-repos/) | Envoy Tech Lab repository registry alignment with the vault (`phase-1-plan`, reports). |
| **—** | [`_proposals/`](_proposals/) | Ad-hoc `.plan.md` comparisons and tooling experiments; **not** part of the numbered program line. |

## Rules

- New **program** initiative: add the next **06**, **07**, … row here and create `planning/<kebab-slug>/` with a `master-roadmap.md` per [`docs/wip/README.md`](../README.md).
- Keep long-lived **reports** under each slug’s `reports/` directory.
