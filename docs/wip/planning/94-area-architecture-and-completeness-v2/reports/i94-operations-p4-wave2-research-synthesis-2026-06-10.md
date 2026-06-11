---
parent_initiative: INIT-OPENCLAW_AKOS-94
authored: 2026-06-10
intellectual_kind: research_master_synthesis
pack_id: i94-operations-p4-wave-2026-06-10
control_confidence_level: Safe
feeds_phase: P4-P8
source_ledger: i94-operations-area-source-ledger-p4-wave-2026-06-10.csv
---

# Master synthesis — I94 Operations P4 wave-2 research (2026-06-10)

## Executive summary

Operations has **closed the critical tier** (crit@L3 10/10, 93% score) but has **not**
closed the **automation depth** bar that makes a solo operator + AIC pair truly hands-off.
The mechanical scorer says COMPLETE; the **operational reality** is 12/53 paired processes
and a missing cross-area handoff canonical. This wave applies the **I93 Data diligence
pattern**: vault inventory + cross-area map + 428-source ledger + phased mint plan.

**Recommendation:** Execute **P4 handoffs → P5 I88 wiring → P6 UAT (PWF on AREA-09)**,
then **P7–P8 AREA-09 tranches** as operator-gated CSV commits — do not block P6 on 53/53 pairing.

## Research corpus

| Corpus | Count | Validator |
|:---|---:|:---|
| P0 ledger (reuse) | 366 | prior PASS |
| **P4 wave ledger** | **428** (308 internal + 120 external) | **PASS** |
| Combined unique topics | 49 | — |

Internal sweep covered: full Operations vault (65 assets), all 83 `process_list` Operations
rows, 12 catalog runbooks, I94 planning corpus, I88/I93 cross-initiative ops reports,
WIP intelligence ops-touching notes.

External prongs grounded: PMBOK 7/8 performance domains, ITIL 4 SVS + continual improvement,
RevOps/GTM ops, PMO maturity, SLA/SRE, RACI handoffs, solo-founder cadence (Shape Up, EOS,
Lean), DORA, FinOps bridge, DAMA consumer posture.

## Operational-only conclusions (DO vs REGISTER)

1. **PMO is the automation spine** — daily inbox + weekly WIP + quarterly cohesion already
   scripted; this is the highest-leverage solo-operator surface.
2. **RevOps is the revenue execution bridge** — scaffold + QBR + FINOPS bridge are paired;
   CRM sync and template promotion remain T2 pairing targets.
3. **SMO is the thinnest sub-area** — one catalog row, one SOP; service-mode delivery is
   documented but not yet executable-catalog depth.
4. **Engagement is client-DO** — SOP set exists; pairing to `process_list` is the AREA-09 gap.
5. **Cross-area handoffs are implicit** — mirror emit, FINOPS, compliance CSV gates, and
   fleet hygiene are scattered across SOPs; P4 must **name triggers once** so AIC stops
   re-deriving.
6. **IntelligenceOps is no longer Operations** — post OPS-86-26, handoff doc cites Research only.
7. **business-strategy under PMO is register debt** — I95 L6 tracker; Operations executes via
   Marketing/Finance/RevOps elsewhere.

## Scattered intent reconciliation

| Operator intent (from charter + synthesis) | Status | Next action |
|:---|:---|:---|
| Full sweep until GTM | P0–P3 done | P4–P6 |
| Automation-first | 12/12 catalog T1 done | AREA-09 T2–T4 |
| Solo + AIC hands-off | Partial (renders work) | Handoffs + pairing cliff |
| Seamless when people join | Not designed | P8 RACI overlay (post-P6) |
| Don't care about ops mechanics | Requires P4 handoffs + inbox discipline | Mint + wire |
| Sister areas govern their stuff | DO vs REGISTER in charter | P4 canonical |

## Design principles (from external + internal evidence)

| Principle | Source cluster | Operations application |
|:---|:---|:---|
| Performance domains over process silos | PMBOK 7 | `OPERATIONS_DELIVERY_DISCIPLINE` §2 — already minted |
| Continual improvement as meta-practice | ITIL 4 CI | AREA sweep + OPS_REGISTER inbox |
| Trigger not duplicate | DAMA / I93 map | Handoffs doc — no Data doctrine in Ops |
| WIP limits + visual management | Kanban / inbox | `render_operator_inbox.py` RICE sort |
| Delivery measurement | DORA | Pre-commit-fast + deploy-health Step 0 |
| Small-team cadence | Shape Up / EOS | Daily/weekly/quarterly spine in cross-area map |

## Risks

| ID | Risk | Mitigation |
|:---|:---|:---|
| R-OPS-01 | AREA-09 12/53 blocks "done" feeling | P6 PASS-WITH-FOLLOWUP + pairing tracker |
| R-OPS-02 | business-strategy mis-home confuses AIC | I95 L6 forward-charter; README callout |
| R-OPS-03 | Parallel I94 roadmap P4 (People) name collision | Ops sweep uses **ops-P4** slug; People uses main-roadmap P4 |
| R-OPS-04 | CSV gate fatigue | Batch AREA-09 in 3 tranches max (20+20+21) |

## Feeds

- Vault inventory: [`i94-operations-vault-lay-of-land-2026-06-10.md`](i94-operations-vault-lay-of-land-2026-06-10.md)
- Cross-area map: [`i94-operations-cross-area-execution-map-2026-06-10.md`](i94-operations-cross-area-execution-map-2026-06-10.md)
- Master plan: [`i94-operations-master-sweep-design-2026-06-10.md`](i94-operations-master-sweep-design-2026-06-10.md)
