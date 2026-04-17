# Planning initiatives (`docs/wip/planning/`)

Initiative folders under `docs/wip/planning/` use a **two-digit prefix** (`01-` … `13-`, plus `99-proposals/`) so sort order and “what came before” are obvious in the filesystem. The table below matches that layout. **Ad-hoc** `.plan.md` files live in `99-proposals/`.

| Seq | Folder | Role |
|:---:|:-------|:-----|
| **01** | [`akos-full-roadmap/`](01-akos-full-roadmap/) | AKOS-wide phased roadmap and early reports. |
| **02** | [`hlk-on-akos-madeira/`](02-hlk-on-akos-madeira/) | HLK on AKOS + Madeira: master roadmap, phase plans/reports, **Madeira read-only consolidated plan mirror** [`MADEIRA_HARDENING_CONSOLIDATED_PLAN.md`](02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md), traceability [`reports/madeira-readonly-hardening.md`](02-hlk-on-akos-madeira/reports/madeira-readonly-hardening.md). |
| **03** | [`hlk-km-knowledge-base/`](03-hlk-km-knowledge-base/) | HLK KM (Topic–Fact–Source), manifests, follow-up checklists. |
| **04** | [`holistika-company-formation/`](04-holistika-company-formation/) | **Active program:** Holistika incorporation / founder governance — [`master-roadmap.md`](04-holistika-company-formation/master-roadmap.md), [`phase-1-plan.md`](04-holistika-company-formation/phase-1-plan.md), [`reports/`](04-holistika-company-formation/reports/). |
| **05** | [`hlk-vault-envoy-repos/`](05-hlk-vault-envoy-repos/) | Envoy Tech Lab repository registry alignment with the vault (`phase-1-plan`, reports). |
| **06** | [`planning-backlog-registry/`](06-planning-backlog-registry/) | Cross-initiative backlog SSOT + agent-proxy UAT evidence pointers — [`master-roadmap.md`](06-planning-backlog-registry/master-roadmap.md), [`reports/`](06-planning-backlog-registry/reports/). |
| **07** | [`hlk-neo4j-graph-projection/`](07-hlk-neo4j-graph-projection/) | Optional Neo4j mirror of HLK CSVs + v3.0 link hygiene + graph MCP/API/Streamlit explorer — [`master-roadmap.md`](07-hlk-neo4j-graph-projection/master-roadmap.md), [`reports/`](07-hlk-neo4j-graph-projection/reports/). |
| **08** | [`python-runtime-deployment/`](08-python-runtime-deployment/) | **Infra harmonization:** Python pins, pip profiles (gpu / openstack), operator + test journey, `serve-api` graph supervisor (auto Streamlit + mirror sync), CI/DX — [`master-roadmap.md`](08-python-runtime-deployment/master-roadmap.md), [`reports/`](08-python-runtime-deployment/reports/). |
| **09** | [`openclaw-hygiene/`](09-openclaw-hygiene/) | Gateway SSOT schema alignment (`openclaw.json.example`), security-audit operator guidance, SOUL/bootstrap file path, `openclaw update` checklist — [`master-roadmap.md`](09-openclaw-hygiene/master-roadmap.md), [`reports/`](09-openclaw-hygiene/reports/). |
| **10** | [`madeira-eval-hardening/`](10-madeira-eval-hardening/) | **Closed (2026-04-15):** Madeira Path B+C (sandbox + exec, strip web tools from orch/arch), SOTA prompts/dev-local defaults, eval harness + Langfuse metadata, Windows/Docker operator runway — [`master-roadmap.md`](10-madeira-eval-hardening/master-roadmap.md), [`reports/phase-completion-report.md`](10-madeira-eval-hardening/reports/phase-completion-report.md), **Phase 6 UAT:** [`reports/uat-madeira-path-bc-browser-20260416.md`](10-madeira-eval-hardening/reports/uat-madeira-path-bc-browser-20260416.md). |
| **11** | [`madeira-ops-copilot/`](11-madeira-ops-copilot/) | **Active:** Madeira day-to-day ops support (drafts, checklists, handoff packs) governance-safe — [`master-roadmap.md`](11-madeira-ops-copilot/master-roadmap.md), [`reports/uat-madeira-ops-copilot-20260415.md`](11-madeira-ops-copilot/reports/uat-madeira-ops-copilot-20260415.md). |
| **12** | [`madeira-research-request/`](12-madeira-research-request/) | **Handoff:** External research-team request (use cases, tech, frameworks, journeys) — [`research-request-madeira.md`](12-madeira-research-request/research-request-madeira.md). |
| **13** | [`madeira-research-followthrough/`](13-madeira-research-followthrough/) | **Active:** Implement triage outcomes (intent, escalation copy, docs) — [`master-roadmap.md`](13-madeira-research-followthrough/master-roadmap.md), [`reports/`](13-madeira-research-followthrough/reports/). |
| **—** | [`99-proposals/`](99-proposals/) | Ad-hoc `.plan.md` comparisons and tooling experiments; **not** part of the numbered program line. |

## Rules

- New **program** initiative: add the next free **NN** row here and create `planning/NN-<kebab-slug>/` with a `master-roadmap.md` per [`docs/wip/README.md`](../README.md).
- Keep long-lived **reports** under each slug’s `reports/` directory.
