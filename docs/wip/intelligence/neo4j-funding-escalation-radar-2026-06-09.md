---
report_type: intelligence-radar
parent_initiative: INIT-OPENCLAW_AKOS-95
topic: neo4j-graph-infrastructure-funding
authored: 2026-06-09
authored_by: Execution seat (Composer) — PKT-N4J-RA-3 fuse per thinking-seat c9a7f50b
status: active
volatility_class: medium
staleness_days: 0
staleness_posture: fresh
next_verify_by: 2026-09-09
linked_research_sources:
  - docs/wip/intelligence/neo4j-graph-infrastructure-funding-source-ledger.csv
  - docs/wip/intelligence/neo4j-graph-infrastructure-funding-research-area-2026-06-09.md
ratifying_decisions:
  - D-IH-95-L
  - D-IH-95-M
---

# Neo4j graph-infrastructure funding radar (2026-06-09)

Public + private funding scan for graph/data-platform components; **Free → funded production** escalation ladder tied to bootstrapping GTM and [`NEO4J_STRATEGY.md`](../../references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/NEO4J_STRATEGY.md).

**Fused with full research area:** [`neo4j-graph-infrastructure-funding-research-area-2026-06-09.md`](neo4j-graph-infrastructure-funding-research-area-2026-06-09.md) (52-source ledger). Prior 6-row planning ledger remains cross-linked only — not duplicate SSOT.

**Canonical finops posture:** `finops_neo4j` counterparty row remains **AuraDB free tier** in [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv) until operator funding gate — **no CSV edit in this tranche**.

---

## Escalation ladder (binding 2026)

| Tier | Trigger | Cash cost | Notes |
|:---|:---|:---|:---|
| **Free + keepalive** | **Now (2026)** | $0 | D-IH-95-G keepalive; 72h pause doctrine |
| **F6 backup restore** | Incident / credential class | $0 | D-IH-95-L primary path; charter F6-R0..R7 |
| **Neo4j Startup credits** | FQ-1 approved | $0 → Pro tier credits | **Funding gate #1** — up to $16K Aura credits |
| **Self-hosted Neo4j VM** | Credits exhausted OR revenue gate | **~$30/mo** | **FQ-3 ratified default** — NEO4J_STRATEGY scale trigger; portable Cypher |
| **Aura Professional** | Explicit funding reversal | ~$65/mo | **Deferred 2026** per D-IH-95-L — appendix only |

> **FQ-3 change (2026-06-09):** Post-credits default is **self-hosted VM ~$30/mo**, not Aura Professional first. Professional remains funding-gated appendix per D-IH-95-L.

---

## Public / EU funding (graph + data-platform + AI GTM)

| Source | Fit for Holistika | Notes |
|:---|:---|:---|
| **EIC Accelerator Open 2026** | **Primary (FQ-2 ratified)** | Up to €2.5M grant + €10M equity; cut-offs Jan/Mar/May/Jul/Sep/Nov |
| **EIC Accelerator Challenges 2026** | Thematic only if 2026 challenge matches | €220M thematic; verify Work Programme PDF before applying |
| **EIC Pre-Accelerator** | Early TRL screen | Up to €500K; lower-innovation-performance countries |
| **EIC Transition** | TRL validation bridge | Research → commercial graph platform; secondary |
| **Digital Europe Programme** | SME digital / AI adoption | National EDIH hubs; complements bootstrap GTM |
| **Eurostars / Horizon consortium** | Graph-RAG PoC wedge | ~€500K/SME international R&D; opportunistic |
| **NGI (Next Generation Internet)** | Smaller graph/open-data | €5K–€200K rolling |

**GTM framing:** Fund as **AI knowledge infrastructure for regulated SME engagements** (NEO4J_STRATEGY use-cases A/B), not "we need a database."

---

## Vendor / private lever (Neo4j — independent of EU)

| Source | Lever | Notes |
|:---|:---|:---|
| **Neo4j Startup Program** | Up to **$16K Aura credits** | Redeems on Professional or Business Critical; Series B or earlier; FQ-1 open |
| **Neo4j Community Edition** | Self-hosted default post-credits | GPL3 free; GCP/AWS/Azure marketplace one-click; ops shift |
| **Google Cloud + Neo4j marketplace** | Stackable cloud + Neo4j credits | Precedent for combined startup credits |
| **Aura promotional credits** | Episodic (courses/hackathons) | Opportunistic; not baseline |

Terms: [Neo4j Startup Program Aura terms](https://neo4j.com/legal-terms/startup-program-aura/)

---

## finops_neo4j link (read-only)

| Field | Current canonical value |
|:---|:---|
| Counterparty id | `finops_neo4j` |
| Notes (excerpt) | "Likely AuraDB free tier or self-hosted at current volume" |
| CSV edit gate | Operator approval required per baseline governance |

Spend forecast lives in **this radar doc** + master synthesis (non-canonical); funding posture ratified via **D-IH-95-M** (2026-06-09) — `finops_neo4j` CSV edit still requires its own operator gate.

---

## Funding AskQuestion #2 — CLOSED (D-IH-95-M, 2026-06-09)

All four FQs ratified by the operator; full record at [`i95-fq2-ratification-2026-06-09.md`](../planning/95-canonical-articulation-model/reports/i95-fq2-ratification-2026-06-09.md).

| ID | Question | Ratified choice |
|:---|:---|:---|
| **FQ-1** | Apply to Neo4j Startup Program for up to $16K Professional credits? | **D — Apply + parallel EIC Pre-Accelerator screen** `(ratified D-IH-95-M)` |
| **FQ-2** | First EU public track for graph/data-platform GTM? | **A: EIC Accelerator Open** `(ratified)` |
| **FQ-3** | When credits exhaust, default escalation? | **A: Self-hosted VM ~$30/mo** `(ratified)` |
| **FQ-4** | Next execution charter? | **Custom ordered sequence** `(ratified)` — F6 restore → self-hosted spike → EIC Open LOI → Startup pack → I95 remainder |

Full evidence: [`neo4j-graph-infrastructure-funding-research-area-2026-06-09.md`](neo4j-graph-infrastructure-funding-research-area-2026-06-09.md) §8.

---

## Cross-references

- **Master synthesis:** [`neo4j-graph-infrastructure-funding-research-area-2026-06-09.md`](neo4j-graph-infrastructure-funding-research-area-2026-06-09.md)
- **Source ledger (SSOT):** [`neo4j-graph-infrastructure-funding-source-ledger.csv`](neo4j-graph-infrastructure-funding-source-ledger.csv)
- F6 restore charter: [`i95-neo4j-free-backup-restore-charter-2026-06-09.md`](../planning/95-canonical-articulation-model/reports/i95-neo4j-free-backup-restore-charter-2026-06-09.md)
- Prior planning ledger (cross-link): [`i95-neo4j-funding-escalation-source-ledger.csv`](../planning/95-canonical-articulation-model/reports/i95-neo4j-funding-escalation-source-ledger.csv)
- Decision: **D-IH-95-L** — R2-09 Professional arm deferred 2026; F6 primary
- Decision: **D-IH-95-M** — funding posture 2026 closure (**ratified 2026-06-09**; FQ-1=D + FQ-4 sequence) — [`i95-fq2-ratification-2026-06-09.md`](../planning/95-canonical-articulation-model/reports/i95-fq2-ratification-2026-06-09.md)
