---
report_type: operator-ratification
parent_initiative: INIT-OPENCLAW_AKOS-95
phase: P95-FQ-closure
authored: 2026-06-09
authored_by: Execution seat (Composer)
closure_decision_source: operator_explicit
status: ratified
ratifying_decisions:
  - D-IH-95-M
  - D-IH-95-L
linked_research_sources:
  - docs/wip/intelligence/neo4j-graph-infrastructure-funding-research-area-2026-06-09.md
  - docs/wip/intelligence/neo4j-graph-infrastructure-funding-source-ledger.csv
---

# I95 funding AskQuestion #2 — operator ratification (2026-06-09)

**Initiative:** INIT-OPENCLAW_AKOS-95 (Canonical Articulation Model / the Singularity)  
**Context:** Full research-area synthesis + 52-row source ledger; prior incident correction **D-IH-95-L** (F6 primary; Professional deferred 2026).  
**Minted decision:** **D-IH-95-M** — graph-infrastructure **funding posture 2026** closure.

---

## Binding operator choices

| FQ | Question | Choice | Notes |
|:---|:---|:---|:---|
| **FQ-1** | Neo4j Startup Program (~$16K Aura credits)? | **D** | Apply now **+** parallel **EIC Pre-Accelerator** eligibility screen |
| **FQ-2** | Primary EU public track? | **A — EIC Accelerator Open** | Ratified-at-planning (unchanged) |
| **FQ-3** | Post-credits default? | **A — Self-hosted VM ~$30/mo** | Ratified-at-planning (unchanged) |
| **FQ-4** | Next execution sequence? | **Custom sequence** (below) | Supersedes single-charter options A/B/C/D |

---

## FQ-4 execution sequence (binding)

Operator ratified this **ordered** sequence (not parallel charters):

| Order | Charter / lane | Purpose |
|:---|:---|:---|
| **1** | **F6 Neo4j restore** | [`i95-neo4j-free-backup-restore-charter-2026-06-09.md`](i95-neo4j-free-backup-restore-charter-2026-06-09.md) F6-R0..R7 — restore operator export on Aura Free; get lay of land |
| **2** | **Self-hosted spike** | Spike charter after restore + probe/CQ — validate ~$30/mo CE VM path (FQ-3 default) |
| **3** | **EIC Accelerator Open LOI draft** | Primary EU track (FQ-2); external-register prose |
| **4** | **Neo4j Startup application pack** | Vendor credits (FQ-1 D); use-cases A/B narrative |
| **5** | **I95 remainder** | L3 bundle C · EG-3 · orphan burn-down · full `pre_commit` |

**Hard gates before step 2:** F6-R4 probe exit **0**; CQ UAT PASS at F6-R5.

---

## Constraints preserved

- **`finops_neo4j` CSV** — no edit without separate operator gate.
- **`.backup` binaries** — never commit; operator vault only.
- **D-IH-95-L** — F6 incident path + Professional deferred 2026 **unchanged**; D-IH-95-M adds funding-application sequence only.

---

## Cross-references

- Decision register row: `D-IH-95-M` in [`DECISION_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv)
- Initiative decision log: [`decision-log.md`](../decision-log.md)
- PMO sweep: [`i95-pmo-status-sweep-2026-06-09.md`](i95-pmo-status-sweep-2026-06-09.md)
- Master roadmap queue pointer: [`master-roadmap.md`](../master-roadmap.md) §"Master execution queue"
