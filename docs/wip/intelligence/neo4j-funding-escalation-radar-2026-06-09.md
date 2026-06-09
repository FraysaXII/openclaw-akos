---
report_type: intelligence-radar
parent_initiative: INIT-OPENCLAW_AKOS-95
topic: neo4j-funding-escalation
authored: 2026-06-09
authored_by: Execution seat (Composer) — PKT-I95-F6-DOCS per thinking-seat 7b6fffee
status: active
volatility_class: medium
staleness_days: 0
staleness_posture: fresh
next_verify_by: 2026-09-09
linked_research_sources:
  - docs/wip/planning/95-canonical-articulation-model/reports/i95-neo4j-funding-escalation-source-ledger.csv
ratifying_decisions:
  - D-IH-95-L
---

# Neo4j funding escalation radar (2026-06-09)

Public + private funding scan for graph/data-platform components; **Free → funded production** escalation ladder tied to bootstrapping GTM and [`NEO4J_STRATEGY.md`](../../references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/NEO4J_STRATEGY.md).

**Canonical finops posture:** `finops_neo4j` counterparty row remains **AuraDB free tier** in [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv) until operator funding gate — **no CSV edit in this tranche**.

---

## Escalation ladder (binding 2026)

| Tier | Trigger | Cash cost | Notes |
|:---|:---|:---|:---|
| **Free + keepalive** | **Now (2026)** | $0 | D-IH-95-G keepalive; 72h pause doctrine |
| **Neo4j Startup credits** | Application approved | $0 → Pro tier | **Funding gate #1** — up to $16K Aura credits |
| **Aura Professional** | Credits exhausted OR revenue gate | ~$65/mo | **Deferred 2026** per D-IH-95-L |
| **Self-hosted Neo4j VM** | NEO4J_STRATEGY scale trigger (>200k nodes or Aura >$50/mo) | ~$30/mo | Portable Cypher; ops shift |

---

## Public / EU funding (graph + data-platform + AI GTM)

| Source | Fit for Holistika | Notes |
|:---|:---|:---|
| **EIC Accelerator Open 2026** | Graph-AI / governance-KG narrative | Up to €2.5M grant + €10M equity; cut-offs Jan/Mar/May/Jul/Sep/Nov |
| **EIC Accelerator Challenges 2026** | Thematic only if 2026 challenge matches | €220M thematic; verify Work Programme PDF before applying |
| **EIC Pre-Accelerator** | Early TRL | Up to €500K; lower-innovation-performance countries |
| **EIC Transition** | TRL validation bridge | Research → commercial graph platform |
| **Digital Europe Programme** | SME digital / AI adoption | National hubs; complements bootstrap GTM |
| **Eurostars / Horizon consortium** | Graph-RAG PoC wedge | ~€500K/SME international R&D |
| **NGI (Next Generation Internet)** | Smaller graph/open-data | €5K–€200K rolling |

**GTM framing:** Fund as **AI knowledge infrastructure for regulated SME engagements** (NEO4J_STRATEGY use-cases A/B), not "we need a database."

---

## Vendor / private lever (Neo4j — independent of EU)

| Source | Lever | Notes |
|:---|:---|:---|
| **Neo4j Startup Program** | Up to **$16K Aura credits** | Redeems on Professional or Business Critical; Series B or earlier |
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

Spend forecast lives in **this radar doc** (non-canonical) until funding ratified.

---

## Funding-only AskQuestion (post-docs)

| ID | Question | Options |
|:--|:---------|:--------|
| **FQ-1** | Apply to Neo4j Startup Program for up to $16K Professional credits? | A: Apply now / B: Defer Q3 2026 / C: Decline — Free-only 2026 |
| **FQ-2** | First EU public track for graph/data-platform GTM? | A: EIC Accelerator Open / B: EIC Transition / C: Eurostars / D: None 2026 |
| **FQ-3** | When credits exhaust, default escalation? | A: Professional ~$65/mo / B: Self-hosted VM ~$30/mo / C: Re-apply vendor credits |

---

## Cross-references

- F6 restore charter: [`i95-neo4j-free-backup-restore-charter-2026-06-09.md`](../planning/95-canonical-articulation-model/reports/i95-neo4j-free-backup-restore-charter-2026-06-09.md)
- Source ledger: [`i95-neo4j-funding-escalation-source-ledger.csv`](../planning/95-canonical-articulation-model/reports/i95-neo4j-funding-escalation-source-ledger.csv)
- Decision: **D-IH-95-L** — R2-09 Professional arm deferred 2026; F6 primary
