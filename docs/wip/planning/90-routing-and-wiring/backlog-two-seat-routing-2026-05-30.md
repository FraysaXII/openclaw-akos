---
intellectual_kind: planning_backlog
sharing_label: internal_only
initiative_id: INIT-OPENCLAW_AKOS-90
authored: 2026-05-30
last_review: 2026-06-01
language: en
linked_decisions:
  - D-IH-90-A
  - D-IH-90-H
authority: Founder + PMO
---

# Backlog — two-seat routing + cluster tranche (2026-05-30)

> **SSOT:** Cursor plan [`routing_and_wiring_788b66e3.plan.md`](file:///c:/Users/Shadow/.cursor/plans/routing_and_wiring_788b66e3.plan.md) §4 + §14. **Siblings:** I91 (graph + store-coverage), I92 (ERP reassess). **Out of scope:** brand-domain tranche (`D-IH-86-FK`, 2026-06-01) — cite only [`docs/wip/intelligence/brand-domain-naming-2026-05-31/brand-domain-options-and-governance-gap.md`](../../intelligence/brand-domain-naming-2026-05-31/brand-domain-options-and-governance-gap.md).

## P0 — charter (this thinking unit)

- Mint initiative folder + OPS reconciliation + rule/skill inventory.
- **GATE #1:** `INITIATIVE_REGISTRY` rows 90/91/92 + `D-IH-90-A..Q` (operator approval before commit).

## P1 — two-seat machinery (I90)

| ID | Deliverable | Gate |
|:---|:---|:---|
| P1a | `.cursor/agents/planner.md` (readonly) | — |
| P1b | `.cursor/agents/executor.md` (`composer-2.5`) | — |
| P1c | `reports/two-seat-setup-guide-2026-05-30.md` | optional operator skim |

## P2 — rule tier rewire (I90)

| Phase | Scope |
|:---|:---|
| P2a | `alwaysApply: false` on 19 demote-list rules (see master-roadmap §P2) |
| P2b | `alwaysApply: true` on 4 core rules only |
| P2c | Add `globs` to `akos-uat-discipline.mdc`, `akos-inter-wave-regression.mdc` |
| P2d | `akos-mirror-template.mdc` → sibling-repo copy only (remove from AKOS always-on) |
| P2e | `scripts/validate_cursor_rule_tiers.py` + pre_commit step (INFO ramp) |
| P2f | `scripts/validate_rule_skill_pairing.py` + pre_commit step |

## P3 — backlog drain (I90; post-P2)

Ordered queue from plan §4 P3 + [`86-initiative-cluster-execution-coordinator/research-rollout-backlog-2026-05-29.md`](../86-initiative-cluster-execution-coordinator/research-rollout-backlog-2026-05-29.md):

1. ~~OPS-86-16 / OPS-86-17~~ — **done** at GATE #1 (`9f7bb6e`).
2. ~~OPS-86-3~~ — **done** at GATE #1.
3. ~~OPS-86-23 notes refresh~~ — **done** 2026-06-01 ([`reports/p3-ops-backlog-drain-2026-06-01.md`](reports/p3-ops-backlog-drain-2026-06-01.md)).
4. Research legacy SSOT (OPS-86-26) — gated; do not start without operator.
5. I91 P0 charter — **in progress** (master-roadmap expanded 2026-06-01); graph execution blocked on Neo4j env until operator supplies credentials.

**GATE #2:** **PASS** 2026-06-01 ([`reports/p2-gate2-rule-tier-review-2026-06-01.md`](reports/p2-gate2-rule-tier-review-2026-06-01.md), `D-IH-90-W`). P3 routing policy sign-off complete.

## P3.5 — KiRBe production routing (2026-06-01)

| Step | OPS / decision | Status |
|:---|:---|:---|
| Ratify routing SSOT + subdomain + decision | OPS-90-1 + **D-IH-90-X** | pending GATE #3b |
| kirbe-platform runbook URL cleanup | OPS-90-2 | pending |
| hlk-erp `.env.example` + BFF doc drift | OPS-90-3 | pending |
| Render MCP / InfraMonitor kirbe row | OPS-90-4 | pending (operator creds) |
| Refresh regression report (Vercel health-only) | OPS-90-5 | pending |
| Forward vault pairing | OPS-90-6 → I81 P6 | forward |

Report: [`reports/kirbe-production-routing-ops-2026-06-01.md`](reports/kirbe-production-routing-ops-2026-06-01.md). Canonical: [`KIRBE_ROUTING_AND_HOSTING.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/Repositories/KIRBE_ROUTING_AND_HOSTING.md).

## Deferred (explicit)

- **D13 OpenClaw** — forward-charter (`D-IH-90-Q`).
- **Brand-domain** — `D-IH-86-FK` complete; no re-run.
- **Neo4j live** — driver not configured in agent session (2026-06-01 pre-flight); I91 graph phases proceed when operator supplies credentials or runs locally.
