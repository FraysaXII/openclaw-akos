---
intellectual_kind: ops_reconciliation
sharing_label: internal_only
initiative_id: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
language: en
linked_decisions:
  - D-IH-90-H
linked_ops_action_ids:
  - OPS-86-3
  - OPS-86-16
  - OPS-86-17
  - OPS-86-23
  - OPS-86-26
---

# OPS row reconciliation — routing cluster P0 (2026-06-01)

> Evidence sweep: git CSVs + Supabase MCP `list_tables` on `compliance` (project `gynxsbvnoagvxcjsfnne`, 2026-06-01). **GATE #1 applied** (`9f7bb6e`): OPS-86-3/16/17 closed. **P3 applied** (2026-06-01): OPS-86-23 notes refreshed — see [`p3-ops-backlog-drain-2026-06-01.md`](p3-ops-backlog-drain-2026-06-01.md).

## Summary table

| OPS ID | Current status | Evidence today | Proposed disposition at GATE #1 |
|:---|:---|:---|:---|
| **OPS-86-3** | `open` | Migration `20260517163635_i86_p2_program_anchors_column.sql` + view `20260517163648_i86_p3_initiative_program_rollup_view.sql`; `validate_initiative_program_anchors.py` in repo; I86 pause record cited in coordinator roadmap | **Close** — substance shipped; residual = operator `db push` + mirror reseed per OPS-86-32..34 cluster note (forward to OPS if mirror stale) |
| **OPS-86-16** | `open` | Supabase `compliance.artifact_class_registry_mirror` **exists** (21 rows); emit in `sync_compliance_mirrors_from_csv.py`; `validate_output_architecture_registries.py` | **Close** — notes: mirror + validator present; remaining work = mirror **data** freshness (operator emit), not DDL |
| **OPS-86-17** | `open` | Supabase `compliance.component_primitive_registry_mirror` **exists** (25 rows); same emit path | **Close** — same pattern as OPS-86-16 |
| **OPS-86-23** | `open` | DIM-04 backlog **6 CSVs** (artifact/component mirrors exist) | **Keep open** — notes refreshed P3 2026-06-01; re-run inter-wave DIM-04 at next wave-close |
| **OPS-86-26** | `open` | Research legacy SSOT migration — no P0 scope change | **Keep open** — unchanged; gated per plan |

## Cursor rule inventory (33 rules — mechanical counts)

Measured 2026-06-01 via PowerShell on `.cursor/rules/*.mdc`.

| Rule file | alwaysApply | Lines |
|:---|:---|---:|
| akos-adviser-engagement.mdc | false | 101 |
| akos-agent-checkpoint-discipline.mdc | true | 113 |
| akos-aic-delegation.mdc | false | 128 |
| akos-applied-research-discipline.mdc | true | 164 |
| akos-brand-baseline-reality.mdc | true | 98 |
| akos-collaborator-share.mdc | true | 394 |
| akos-conflict-surfacing-and-blocker-trackers.mdc | true | 172 |
| akos-dataops-discipline.mdc | false | 98 |
| akos-deploy-health.mdc | true | 219 |
| akos-docs-config-sync.mdc | true | 190 |
| akos-executable-process-catalog.mdc | true | 131 |
| akos-external-render-discipline.mdc | true | 159 |
| akos-frontend-design.mdc | false | 66 |
| akos-governance-remediation.mdc | true | 84 |
| akos-holistika-operations.mdc | true | 119 |
| akos-index-integrity.mdc | true | 193 |
| akos-inline-ratification.mdc | true | 110 |
| akos-inter-wave-regression.mdc | true | 128 |
| akos-madeira-management.mdc | true | 95 |
| akos-mirror-template.mdc | true | 62 |
| akos-mktops-discipline.mdc | false | 106 |
| akos-operator-communication.mdc | true | 64 |
| akos-people-discipline-of-disciplines.mdc | true | 104 |
| akos-planning-traceability.mdc | true | 353 |
| akos-pwf-governance.mdc | true | 205 |
| akos-quality-fabric.mdc | true | 144 |
| akos-research-action.mdc | true | 190 |
| akos-research-area.mdc | true | 57 |
| akos-research-radar.mdc | true | 64 |
| akos-synthesis-before-tranche.mdc | true | 332 |
| akos-techops-discipline.mdc | false | 108 |
| akos-uat-discipline.mdc | true | 336 |
| akos-ux-discipline.mdc | false | 107 |

**Totals:** 33 rules; **25** `alwaysApply: true` today (plan target after P2: **4** core always-on + globs for UAT/inter-wave).

## Skills inventory

| Count | Notes |
|:---|:---|
| **21** | `SKILL.md` under `.cursor/skills/` (plan cited 20; `brand-naming-craft` is the +1) |

Pairing gaps (P2f target): rules without paired skills per plan — to be enumerated in `validate_rule_skill_pairing.py` first run.

## Self-critique (pre-GATE)

- OPS-86-16/17 closure assumes operator accepts **DDL done, data stale OK** as separate OPS-86-32..34 hygiene — if operator wants mirror row-count parity before close, choose **defer-OPS** instead.
- Rule line counts are file-size proxies, not token budgets — P2 rewire still needs per-rule glob authoring review.
- Neo4j not verified this session — does not block P0 GATE #1.
