# MADEIRA program index — cross-initiative map

Single landing page for the nine MADEIRA-touching governance and engineering initiatives. Canonical execution detail lives in each folder’s `master-roadmap.md`.

| Seq | Folder | Focus | Typical follow-up doc |
|:---:|:-------|:------|:-----------------------|
| **02** | [hlk-on-akos-madeira](../02-hlk-on-akos-madeira/) | HLK runtime on AKOS + read-only MADEIRA hardened plan | [`MADEIRA_HARDENING_CONSOLIDATED_PLAN.md`](../02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md) |
| **10** | [madeira-eval-hardening](../10-madeira-eval-hardening/) | Sandbox/exec path eval + Langfuse operator runway | `reports/` |
| **11** | [madeira-ops-copilot](../11-madeira-ops-copilot/) | Governance-safe MADEIRA ops drafts and handoffs | `master-roadmap.md` |
| **13** | [madeira-research-followthrough](../13-madeira-research-followthrough/) | Implement research triage (intent/docs) | `reports/` |
| **17** | [madeira-cursor-mode-parity](../17-madeira-cursor-mode-parity/) | Ask / Plan interactions, control plane UC matrix | [`coverage-matrix.md`](../17-madeira-cursor-mode-parity/coverage-matrix.md) |
| **32** | [32-holistik-ops-maturation](../32-holistik-ops-maturation/) | SKILL_REGISTRY and Holistik Ops maturation (consumes MADEIRA UAT hooks) | `reports/madeira-runtime-uat-*` pattern |
| **45** | [45-live-eval-harness](../45-live-eval-harness/) | Unified eval harness, cassettes, Tier B weekly | [`master-roadmap.md`](../45-live-eval-harness/master-roadmap.md) |
| **46** | [46-neo4j-strategic-posture](../46-neo4j-strategic-posture/) | Neo4j / GraphRAG posture impacting MADEIRA context | [`master-roadmap.md`](../46-neo4j-strategic-posture/master-roadmap.md) |
| **47** | [47-user-centric-uat](../47-user-centric-uat/) | PERSONA_SCENARIO_REGISTRY persona library + calibration | [`reports/uat-i47-user-centric-uat-2026-05-02.md`](../47-user-centric-uat/reports/uat-i47-user-centric-uat-2026-05-02.md) |
| **49** | [49-madeira-management-rollup](.) | **Current:** verdict rollup + SOPs + dossier MADEIRA flavor + control plane UX | [`master-roadmap.md`](master-roadmap.md) |

**Runtime entrypoints:**

- Dashboard WebChat: `http://127.0.0.1:18789/chat?session=agent:madeira:main`
- Control plane companion: AKOS `/madeira/control` serves [`static/madeira_control.html`](../../../static/madeira_control.html)
- Dossier: `py scripts/render_uat_dossier.py --filter madeira --mode snapshot --format md` (once I49 tooling lands)
