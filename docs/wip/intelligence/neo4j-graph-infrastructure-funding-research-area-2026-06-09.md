---
intellectual_kind: research_master_synthesis
parent_initiative: INIT-OPENCLAW_AKOS-95
related_initiatives: [07, 46, 53, 91, 95]
authored: 2026-06-09
authored_by: Execution seat (Composer) — PKT-N4J-RA-1..4 per thinking-seat c9a7f50b
status: active
language: en
audience: J-OP;J-AIC
named_decision: D-IH-95-M
source_ledger: neo4j-graph-infrastructure-funding-source-ledger.csv
source_count: 52
control_confidence_level: Safe
linked_research_sources:
  - docs/wip/intelligence/neo4j-graph-infrastructure-funding-source-ledger.csv
ratifying_decisions:
  - D-IH-95-L
  - D-IH-95-M
volatility_class: medium
staleness_days: 0
staleness_posture: fresh
next_verify_by: 2026-09-09
---

# Neo4j graph-infrastructure funding — research area master synthesis (2026-06-09)

> Full research-area treatment (area-completeness precedent) for graph store **funding posture**, not a one-line “apply to Neo4j Startup.” Rolls up 52 rated sources across five prongs into a ranked option set that fed **AskQuestion #2**; the operator closed it the same day — **D-IH-95-M ratified 2026-06-09** (FQ-1 = D; FQ-4 ordered sequence; see [`i95-fq2-ratification-2026-06-09.md`](../planning/95-canonical-articulation-model/reports/i95-fq2-ratification-2026-06-09.md)).

## 1. Executive summary

Holistika’s graph layer is a **bounded-context harness for semantic sprawl** — not “we need a database.” The HLK CSV vault remains SSOT; Neo4j is a rebuildable read index (use-case A governance KG, use-case B GraphRAG PoC) whose **2026 economics** are:

| Layer | Posture | Cash |
|:---|:---|:---|
| **Incident + daily ops** | Aura Free + keepalive + **F6 backup restore** (D-IH-95-L) | $0 |
| **Vendor credits (FQ-1 open)** | Neo4j Startup up to **$16K Aura credits** | $0 if approved |
| **EU public (FQ-2 ratified)** | **EIC Accelerator Open** primary | Grant/equity track |
| **Post-credits ops (FQ-3 ratified)** | **Self-hosted VM ~$30/mo** default | ~$30/mo infra |
| **Aura Professional** | **Deferred 2026** | ~$65/mo — funding-gated appendix only |

GTM framing for any application: **AI knowledge infrastructure for regulated SME engagements** (NEO4J_STRATEGY use-cases A/B), not generic database spend.

---

## 2. Binding 2026 posture table

| Tier | Trigger | Cash | Binding source |
|:---|:---|:---|:---|
| Free + keepalive | Now (2026) | $0 | D-IH-95-G keepalive; 72h pause doctrine |
| F6 backup restore | Credential/incident class | $0 | D-IH-95-L; charter F6-R0..R7 |
| Neo4j Startup credits | FQ-1 approval | $0 → Pro tier credits | SRC-N4J-F03, SRC-N4J-26 |
| EIC Accelerator Open | FQ-2 ratified | Grant + equity | SRC-N4J-F01, SRC-N4J-F02 |
| **Self-hosted VM** | Credits exhausted OR revenue gate | **~$30/mo** | FQ-3 ratified; SRC-N4J-F04, SRC-N4J-27 |
| Aura Professional | Explicit funding reversal | ~$65/mo | **Deferred 2026** per D-IH-95-L |

`finops_neo4j` counterparty row stays **AuraDB free tier** in canonical CSV until a separate operator gate — spend forecast lives in the fused radar doc.

---

## 3. Prong A — Internal KB fusion

| Finding | Sources | Implication |
|:---|:---|:---|
| Three use-cases: A governance KG (built), B GraphRAG PoC, C agent memory (deferred) | SRC-N4J-07, SRC-N4J-20 | Funding narrative anchors on A+B not C |
| CSV vault SSOT; Neo4j rebuildable from projection | SRC-N4J-07, SRC-N4J-13 | F5 rebuild path always available; backup preserves non-CSV state |
| I91 multi-store matrix; Neo4j P1 **blocked** on `NEO4J_*` | SRC-N4J-21, SRC-N4J-23 | Funding unlocks ops path but does not auto-unblock without env contract |
| HCAM graph as DTO / verb-taxonomy harness | SRC-N4J-22, SRC-N4J-25, SRC-N4J-40 | Cross-topic context engineering doctrine improves when graph store is funded |
| I07 env contract: `neo4j+s`, `~/.openclaw/.env` | SRC-N4J-16 | Self-hosted spike must preserve same contract shape |
| F6 incident path supersedes Professional for 2026 | SRC-N4J-17, SRC-N4J-18, SRC-N4J-19, D-IH-95-L | Professional charter → `deferred-funding` appendix |

---

## 4. Prong B — Vendor economics

| Lever | Fit | Notes |
|:---|:---|:---|
| **Neo4j Startup Program** | High if ≤Series B + graph-AI narrative | Up to $16K credits; redeems on Professional/BC only (SRC-N4J-F03, SRC-N4J-26) |
| **Community Edition self-hosted** | **Default post-credits** (FQ-3) | GPL3 free; ops shift to operator; marketplace one-click deploy (SRC-N4J-27, SRC-N4J-28) |
| **Google Cloud + Neo4j marketplace** | Stackable | Cloud credits + vendor credits; not substitute for Startup application (SRC-N4J-29) |
| **Aura Professional ~$65/mo** | Deferred | Backup retention + daily schedules; only if funding gate re-opens (SRC-N4J-06, SRC-N4J-10) |
| **TCO hidden labor** | Caution on self-hosted | Community “free” still carries VM + patching labor (SRC-N4J-42, SRC-N4J-43) |

---

## 5. Prong C — EU public funding

**Primary track (FQ-2 ratified): EIC Accelerator Open 2026** — up to €2.5M grant + €10M equity; cut-offs Jan/Mar/May/Jul/Sep/Nov (SRC-N4J-F01, SRC-N4J-F02).

| Track | Role 2026 | Sources |
|:---|:---|:---|
| **EIC Accelerator Open** | **Primary** | SRC-N4J-F02 |
| EIC Accelerator Challenges | Thematic only if 2026 challenge matches | SRC-N4J-46 |
| EIC Pre-Accelerator | Early TRL screen; parallel to Startup? | SRC-N4J-32 |
| EIC Transition | Secondary / deferred | SRC-N4J-33 |
| Digital Europe (AI Continent, EDIH) | SME AI adoption complement | SRC-N4J-30, SRC-N4J-31 |
| Eurostars / NGI | Opportunistic PoC wedge | SRC-N4J-34, SRC-N4J-35 |

---

## 6. Prong D — KG / GraphRAG / personal KM landscape

| Tool / pattern | Holistika posture | Sources |
|:---|:---|:---|
| `neo4j-graphrag-python` (LightRAG hybrid) | **Chosen** for use-case B (D-IH-46-A) | SRC-N4J-36 |
| LightRAG (HKUDS) | Pattern reference | SRC-N4J-38 |
| LlamaIndex KG index | Alternative; not primary | SRC-N4J-37 |
| Obsidian graph view | **Secondary nav** only (D-IH-12) | SRC-N4J-39 |
| I53 GraphRAG PoC risks | Ship vs no-ship gate still open | SRC-N4J-24 |

---

## 7. Prong E — Context-engineering doctrine delta

Graph projection is the **bounded-context harness** that keeps agent context from semantic sprawl across HCAM verb taxonomy, initiative lineage, and multi-store I91 inventory:

- **Singularity/DTO framing** (I95 round-2 synthesis) treats the graph as a queryable semantic layer over canonical CSVs, not a second SSOT (SRC-N4J-41).
- **Forked PARENT_OF edges** in `hlk_graph_model.py` are the smoking gun for why graph rework and funding posture are coupled (SRC-N4J-22).
- Funding that lands on **self-hosted CE** preserves Cypher portability and aligns with NEO4J_STRATEGY scale trigger — better doctrine fit than Aura Pro as default escalation.

---

## 8. Ranked option set (feeds AskQuestion #2)

| ID | Question | Options |
|:---|:---|:---|
| **FQ-1** | Neo4j Startup Program (~$16K Aura credits)? | **A:** Apply now after eligibility check **(recommended if ≤Series B)** / **B:** Defer Q3 pending EIC LOI / **C:** Decline Free+F6 only 2026 / **D:** Apply + parallel EIC Pre-Accelerator screen |
| **FQ-2** | Primary EU track? | **A: EIC Accelerator Open** `(ratified-at-planning)` / B: Transition / C: Eurostars / D: None 2026 |
| **FQ-3** | Post-credits default? | **A: Self-hosted VM ~$30/mo** `(ratified-at-planning)` / B: Aura Professional ~$65/mo / C: Re-apply vendor credits |
| **FQ-4** | Next execution charter? | **A:** Self-hosted spike charter (I95 follow-on) / **B:** EIC Open LOI draft / **C:** Neo4j Startup application pack / **D:** Hold — F6 restore only |

**Gate (closed):** FQ-2 and FQ-3 were `ratified-at-planning`; **FQ-1 closed at AskQuestion #2 with option D** (apply now + parallel EIC Pre-Accelerator screen) and FQ-4 closed with the custom ordered sequence — all under **D-IH-95-M** (2026-06-09).

---

## 9. Stage 8 disposition

| Topic cluster | Disposition |
|:---|:---|
| `aura_f6_backup_restore` | **promoted** — binding incident path |
| `neo4j_funding_escalation` | **promoted** — fused into this research area |
| `vendor_economics` | **on-radar** — FQ-1 gates Startup application |
| `eu_public_funding` | **on-radar** — EIC Open LOI/application cadence TBD |
| `post_credit_escalation` | **promoted** — self-hosted default ratified |
| `aura_professional_restore` | **deferred** — appendix only 2026 |
| `kg_graphrag_landscape` | **on-radar** — I53 closure separate |
| `context_engineering_doctrine` | **promoted** — links HCAM + I91 + funding |

---

## 10. Appendix A — TOPIC_REGISTRY proposal (operator CSV gate)

> **Proposal only** — do not commit to `TOPIC_REGISTRY.csv` without operator approval.

| Field | Proposed value |
|:---|:---|
| `topic_id` | `topic_neo4j_graph_infrastructure_funding` |
| `title` | Neo4j graph infrastructure funding & escalation (2026) |
| `lifecycle_status` | `active` |
| `primary_owner_role` | Business Controller |
| `steward_role` | System Owner |
| `program_id` | `shared` |
| `plane` | `techops` |
| `parent_topic` | `topic_holistik_ops_discovery` |
| `related_topics` | `topic_holistik_ops_discovery` |
| `working_area_path` | `docs/wip/intelligence/neo4j-graph-infrastructure-funding-research-area-2026-06-09.md` |
| `notes` | Fused research area; INIT-07/46/91/95 lineage; D-IH-95-L binding; D-IH-95-M pending FQ closure |

---

## 11. Appendix B — INTELLIGENCEOPS_REGISTER proposals (operator CSV gate)

> **Proposal only** — do not commit without operator approval.

| register_id | target_id | volatility_class | staleness_days | staleness_posture | next_verify_by | notes |
|:---|:---|:---|:---:|:---|:---|:---|
| `IO-VEND-NEO4J-STARTUP-2026` | `topic_neo4j_graph_infrastructure_funding` | medium | 90 | cite_and_flag | 2026-09-09 | block_govern until FQ-1 closes |
| `IO-REG-EIC-ACCEL-OPEN-2026` | `topic_neo4j_graph_infrastructure_funding` | fast | 45 | block_govern | 2026-07-15 | Cut-off calendar driven; FQ-2 primary |

Both rows would cite `SOP-RESEARCH_RADAR_001` + `scripts/research_radar_sweep.py` per existing register pattern.

---

## 12. Cross-references

- Source ledger (SSOT): [`neo4j-graph-infrastructure-funding-source-ledger.csv`](neo4j-graph-infrastructure-funding-source-ledger.csv)
- Fused radar: [`neo4j-funding-escalation-radar-2026-06-09.md`](neo4j-funding-escalation-radar-2026-06-09.md)
- Doctrine: [`NEO4J_STRATEGY.md`](../../references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/NEO4J_STRATEGY.md)
- Prior thin ledger (cross-link only): [`i95-neo4j-funding-escalation-source-ledger.csv`](../planning/95-canonical-articulation-model/reports/i95-neo4j-funding-escalation-source-ledger.csv)
- Decisions: **D-IH-95-L** (ratified); **D-IH-95-M** (**ratified 2026-06-09** — [`i95-fq2-ratification-2026-06-09.md`](../planning/95-canonical-articulation-model/reports/i95-fq2-ratification-2026-06-09.md))
- I95 decision log: [`decision-log.md`](../planning/95-canonical-articulation-model/decision-log.md)
