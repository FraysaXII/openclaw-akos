# Planning backlog registry (cross-initiative SSOT)

**Initiative:** `06-planning-backlog-registry`  
**Status:** Active  
**Role:** Single in-repo index for open and promoted work spanning `docs/wip/planning/01`–`05`, plus **in_scope_major** programs. Does not replace canonical HLK compliance SSOT ([PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md)).

**Traceability:** Non-canonical planning copy per [.cursor/rules/akos-planning-traceability.mdc](../../../.cursor/rules/akos-planning-traceability.mdc).

---

## Registry schema

| Column | Meaning |
|:-------|:--------|
| `ID` | Stable registry id (`REG.*`) |
| `class` | `active` · `deferred_initiative` · `in_scope_major` · `operator_env` · `historical` · `non_program` |
| `owner` | Initiative folder (`01-` … `05-`) or `06` |
| `source` | Primary doc |
| `next_action` | One-line owner |
| `verification_when_done` | Gates (see [DEVELOPER_CHECKLIST.md](../../../docs/DEVELOPER_CHECKLIST.md)) |

---

## Backlog table

| ID | class | owner | source | next_action | verification_when_done |
|:---|:------|:------|:-------|:------------|:------------------------|
| REG.001 | active | 02 | [MADEIRA_HARDENING_CONSOLIDATED_PLAN.md](../02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md) | Lane B agent-proxy evidence + mirror row | Mirror + [hlk_admin_smoke.md](../../../uat/hlk_admin_smoke.md) browser subsection |
| REG.002 | active | 02 | [master-roadmap.md](../02-hlk-on-akos-madeira/master-roadmap.md) | Reconciled with consolidated plan + mirror (no contradictory “active flagship” vs closure) | Doc review + link check |
| REG.003 | deferred_initiative | 02 | [next-baseline-kirbe-sync-boundary-proposal.md](../02-hlk-on-akos-madeira/reports/next-baseline-kirbe-sync-boundary-proposal.md) | NBT.1–NBT.5 owned by KiRBe sync phase plan | `validate_hlk.py` when vault paths change |
| REG.004 | in_scope_major | 02 | [phase-madeira-write-browser-plan.md](../02-hlk-on-akos-madeira/phase-madeira-write-browser-plan.md) | Executor+HITL; widen gateway allowlist in controlled phases | Full matrix + inventory + drift |
| REG.005 | in_scope_major | 02 | [phase-kirbe-sync-daemons-plan.md](../02-hlk-on-akos-madeira/phase-kirbe-sync-daemons-plan.md) | Design replayable sync + drift evidence | Full matrix; PRECEDENCE canonical-wins |
| REG.006 | in_scope_major | 02 | [phase-canonical-csv-tranche-plan.md](../02-hlk-on-akos-madeira/phase-canonical-csv-tranche-plan.md) | Operator-approved CSV batch + docs | **Operator approval** + `validate_hlk.py` + USER_GUIDE/ARCHITECTURE |
| REG.007 | active | 03 | [km-plan-followup-checklist.md](../03-hlk-km-knowledge-base/reports/km-plan-followup-checklist.md) | Run rows only on triggers (Trello, manifests, CSV) | `validate_hlk_km_manifests.py` / `validate_hlk.py` per trigger |
| REG.008 | active | 04 | [phase-1-plan.md](../04-holistika-company-formation/phase-1-plan.md) | Promoted program: incorporation / adviser follow-through | Doc review; legal commits gated out-of-repo as needed |
| REG.009 | active | 05 | [REPOSITORIES_REGISTRY.md](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) | `openclaw-akos` + `FraysaXII/kirbe` set; **client-delivery** row still placeholder until engagement remote known | `py scripts/validate_hlk.py` |
| REG.010 | operator_env | 02 | [madeira-flagship-hardening-report.md](../02-hlk-on-akos-madeira/reports/madeira-flagship-hardening-report.md) | Langfuse **project visibility** vs MCP account (if traces missing) | Langfuse MCP + `scripts/test-langfuse-trace.py` |
| REG.011 | historical | 02 | [master-roadmap.md](../02-hlk-on-akos-madeira/master-roadmap.md) § Phase 1 gap | Pre-remediation baseline gaps; read with phase-1-report | N/A |
| REG.012 | non_program | 99 | `docs/wip/planning/99-proposals/*.plan.md` | Experiments; promote via README rules before execution | N/A |

---

## Decision log

| ID | Question | Decision |
|:---|:-----------|:---------|
| D-REG-1 | Where is cross-initiative backlog SSOT? | This `06` registry + initiative `master-roadmap` / phase plans. |
| D-REG-2 | Madeira read-only vs write/browser expansion | Read-only hardening remains **closed record**; expansion is **additive** phase plan ([phase-madeira-write-browser-plan.md](../02-hlk-on-akos-madeira/phase-madeira-write-browser-plan.md)). |

---

## Verification matrix (registry maintenance)

When **only** this folder’s markdown changes: spot-check links. When any linked initiative ships code/config: full [DEVELOPER_CHECKLIST.md](../../../docs/DEVELOPER_CHECKLIST.md) matrix.

---

## Reports

See [reports/](reports/) for dated proxy-UAT and registry audit notes.
