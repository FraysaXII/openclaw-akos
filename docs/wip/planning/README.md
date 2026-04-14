# Planning initiatives (`docs/wip/planning/`)

Initiative folders under `docs/wip/planning/` use a **two-digit prefix** (`01-` … `06-`, plus `99-proposals/`) so sort order and “what came before” are obvious in the filesystem. The table below matches that layout. **Ad-hoc** `.plan.md` files live in `99-proposals/`.

| Seq | Folder | Role |
|:---:|:-------|:-----|
| **01** | [`akos-full-roadmap/`](01-akos-full-roadmap/) | AKOS-wide phased roadmap and early reports. |
| **02** | [`hlk-on-akos-madeira/`](02-hlk-on-akos-madeira/) | HLK on AKOS + Madeira: master roadmap, phase plans/reports, **Madeira read-only consolidated plan mirror** [`MADEIRA_HARDENING_CONSOLIDATED_PLAN.md`](02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md), traceability [`reports/madeira-readonly-hardening.md`](02-hlk-on-akos-madeira/reports/madeira-readonly-hardening.md). |
| **03** | [`hlk-km-knowledge-base/`](03-hlk-km-knowledge-base/) | HLK KM (Topic–Fact–Source), manifests, follow-up checklists. |
| **04** | [`holistika-company-formation/`](04-holistika-company-formation/) | **Active program:** Holistika incorporation / founder governance — [`master-roadmap.md`](04-holistika-company-formation/master-roadmap.md), [`phase-1-plan.md`](04-holistika-company-formation/phase-1-plan.md), [`reports/`](04-holistika-company-formation/reports/). |
| **05** | [`hlk-vault-envoy-repos/`](05-hlk-vault-envoy-repos/) | Envoy Tech Lab repository registry alignment with the vault (`phase-1-plan`, reports). |
| **06** | [`planning-backlog-registry/`](06-planning-backlog-registry/) | Cross-initiative backlog SSOT + agent-proxy UAT evidence pointers — [`master-roadmap.md`](06-planning-backlog-registry/master-roadmap.md), [`reports/`](06-planning-backlog-registry/reports/). |
| **—** | [`99-proposals/`](99-proposals/) | Ad-hoc `.plan.md` comparisons and tooling experiments; **not** part of the numbered program line. |

## Rules

- New **program** initiative: add the next **07**, **08**, … row here and create `planning/NN-<kebab-slug>/` (next free `NN`) with a `master-roadmap.md` per [`docs/wip/README.md`](../README.md).
- Keep long-lived **reports** under each slug’s `reports/` directory.
