---
candidate_id: I-NN-RESEARCH-DATA-MANAGEMENT
title: Research Data-Management (DAMA) + multi-channel research-feed delivery — the STORE/RECALL/SHARE data layer of the CORPINT lifecycle operationalized
status: candidate
authored: 2026-05-29
last_review: 2026-05-29
parent_initiatives: [86]
related_initiatives: [75, 83, 88]
priority: 1
language: en
audience: J-OP;J-AIC
access_level: 5
parent_lane: I86 Wave R+5 C6 rollout backlog (Theme C) — operator DAMA framing 2026-05-29
charter_decisions:
  - D-IH-75-G
forward_charter_authority: |
  Operator framing 2026-05-29 (post the CORPINT lifecycle logic change D-IH-75-G): "i'm thinking
  about DAMA for all of this ... we already have data consumers or etls that wire here — KiRBe and
  its ever growing sources, ERP, KB, Supabase, our orchestration systems, RPAs — that i'd like to
  e.g. get a proper research feed in my inbox or pushed through other media like Discord, Slack,
  Telegram." This candidate operationalizes the STORE -> RECALL -> SHARE data layer of the lifecycle
  as real data products with real delivery, under a DAMA-DMBOK lens. Data-ops acknowledged
  not-yet-ready; this candidate is the honest path to readiness.
linked_canonicals:
  - docs/references/hlk/v3.0/Research/canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
linked_ops_action_ids:
  - OPS-86-29
  - OPS-86-30
external_research_sources:
  # DAMA-DMBOK 2.0 (the 11 knowledge areas) — the doctrinal anchor for the data-management lens
  - https://www.dama.org/cpages/body-of-knowledge
  # Intelligence cycle + KM lifecycle (shared with RESEARCH_LIFECYCLE_DOCTRINE.md evidence base)
  - https://en.wikipedia.org/wiki/Intelligence_cycle_management
sibling_candidates:
  - i-nn-research-ops-substrate.md  # 10-pillar ReOps frame; pillars 3 (Tools) + 4 (KM) + 7 (Comms) overlap this candidate's data layer
---

# I-NN-RESEARCH-DATA-MANAGEMENT — DAMA data layer + research-feed delivery

> **Spawned by the CORPINT lifecycle logic change (`D-IH-75-G`, 2026-05-29) + the operator's DAMA
> framing the same day.** The lifecycle doctrine named **STORE → RECALL → SHARE** as the data layer
> of Research, with named cross-area joins to Tech (the store + retrieval infra) and Marketing
> (the dissemination register). This candidate operationalizes that layer: a **DAMA-DMBOK lens** on
> the research data flow + the concrete **data-consumer/ETL wiring** Holistika already runs + a
> **multi-channel research-feed delivery** (the operator's named want: a proper feed in the inbox or
> pushed via Discord / Slack / Telegram).

## 1. What this is (one paragraph)

Research produces knowledge; that knowledge has to be **stored, found, and delivered** to the people
and systems that act on it — and **protected** along the way. Today the *crafts* exist (the four
disciplines) and the *spine* exists (the lifecycle), but the **data-management plumbing** is
partial: there are data consumers and ETLs already wired in (KiRBe + its growing sources, the ERP,
the KB, Supabase, orchestration systems, RPAs), yet there is no inventory of them, no governed
research-feed product, and no honest data-ops readiness map. This candidate applies the
**DAMA-DMBOK** discipline (the industry-standard data-management body of knowledge) to the research
data layer so the operator can *manage* it — and gets a research feed that actually reaches them.

## 2. The CORPINT lifecycle × DAMA-DMBOK map (the bridge)

| Lifecycle stage | DAMA knowledge area(s) | What it means here |
|:---|:---|:---|
| ACQUIRE | Data Integration & Interoperability; Data Quality | ingest from human + open sources; quality at source |
| PROCESS | Data Quality; Metadata; Reference & Master Data | classify, score, corroborate; the canonical registries |
| **STORE** | Data Storage & Operations; Data Architecture; Document & Content Mgmt | KM Topic-Fact-Source; Supabase mirrors; Neo4j; KiRBe |
| **RECALL** | Data Warehousing & BI; Metadata (findability) | query surfaces; the register as a queryable index |
| **SHARE** | Data Integration & Interoperability (delivery); Document & Content Mgmt | **the research feed: inbox / Discord / Slack / Telegram** |
| PROTECT | Data Security; Data Governance | access levels; confidence; redaction; RLS |

The **bold** stages are this candidate's core scope; the others are governed by the lifecycle
doctrine + the four disciplines + the radar/research-action disciplines.

## 3. Data-consumer / ETL inventory (the wiring that already exists) — `OPS-86-29`

The operator named these as already wired. The first deliverable is to **inventory** them honestly:
what each consumes/produces, in what shape, with what freshness, under what access.

| Consumer / ETL | Role in the research data flow | DAMA concern |
|:---|:---|:---|
| **KiRBe** (+ growing sources) | ingests + serves research/intelligence; the productized KB | Data Integration; Storage & Ops |
| **ERP** (hlk-erp) | operator-facing surfaces; research panels (forward) | Document & Content Mgmt; BI |
| **KB** (Obsidian / KM Topic-Fact-Source) | the canonical knowledge store | Document & Content Mgmt; Metadata |
| **Supabase** | mirrors of the canonical registries; the data plane | Storage & Ops; Data Architecture |
| **Orchestration systems** | move/transform data between surfaces | Data Integration & Interoperability |
| **RPAs** | automated collection + delivery actors | Data Integration; Data Quality |

## 4. Multi-channel research-feed delivery (the operator's named want) — `OPS-86-30`

The **SHARE** stage as a *delivered data product*: a proper research feed that reaches the operator
where they already are.

- **Channels:** operator **inbox** (email) + **Discord** + **Slack** + **Telegram** + other media as
  they earn their keep. Channel definitions can reuse the
  [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv)
  pattern.
- **Per-channel format + cadence:** a digest format per channel (short push vs full brief); a cadence
  per target volatility (reuse the Research Radar freshness primitive — fast targets push sooner).
- **Source of the feed:** the Research Action govern stage + the radar STALE/DUE queue → a packaged
  digest (Research Output Packaging capability) → channel adapters.
- **Recipient-fallback** (per external-render discipline): even if the operator doesn't watch a
  channel, the feed lands somewhere durable (inbox + a stored digest).

## 5. Data-ops readiness (honest gap) — part of `OPS-86-29`

The operator said it plainly: *"we still don't have data ops ready."* This candidate does **not**
pretend otherwise. Deliverable: a readiness map naming what must exist before the feed is
trustworthy — minimum data-quality bar at STORE, metadata/findability at RECALL, access/redaction at
PROTECT, and a single owner for the data plane. The feed ships incrementally as readiness clears, not
all at once.

## 6. Activation gates

- **A1.** Operator confirms scope + priority (this candidate is P1 in the rollout backlog).
- **A2.** Data-consumer/ETL inventory (`OPS-86-29`) complete enough to design against.
- **A3.** A named owner for the research data plane (System Owner interim; Research Director / Data
  steward when activated).
- **A4.** Composes with I83 (AI-archivist + KiRBe ingestor) — the KiRBe wiring is shared; avoid
  duplicate ingestion design.
- **A5.** External grounding ≥ 3 sources per `akos-applied-research-discipline.mdc` RULE 2 at
  activation (DAMA-DMBOK + the lifecycle doctrine's evidence base + one feed-delivery/ETL practitioner
  source to be sourced at activation).

## 7. Relationship to siblings

- [`RESEARCH_LIFECYCLE_DOCTRINE.md`](../../../references/hlk/v3.0/Research/canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md) — the parent: this candidate operationalizes its STORE/RECALL/SHARE layer + the Tech/Marketing joins.
- [`i-nn-research-ops-substrate.md`](i-nn-research-ops-substrate.md) — the 10-pillar ReOps frame; this candidate is the data-plumbing of its pillars 3 (Tools & Infrastructure) + 4 (Knowledge Management) + 7 (Internal Communications & Advocacy = the feed).
- **I83 (AI-archivist + KiRBe ingestor)** — shares the KiRBe wiring; the research-feed is a KiRBe-served product.
- **I88 (cross-area Ops wiring review)** — the data-consumer inventory is a cross-area wiring artifact.
- **I75 (Research area governance)** — the substantive Research-area home; this candidate may fold in as a data-management phase.

## 8. Cross-references

- Rollout backlog (the managed path): [`research-rollout-backlog-2026-05-29.md`](../86-initiative-cluster-execution-coordinator/research-rollout-backlog-2026-05-29.md) Theme C.
- OPS actions: `OPS-86-29` (data-consumer/ETL inventory) + `OPS-86-30` (multi-channel feed delivery) in [`OPS_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv).
- Spawning decision: `D-IH-75-G` (CORPINT lifecycle logic change).
- DAMA-DMBOK 2.0 — the data-management body of knowledge (the 11 knowledge areas) that frames this candidate.
- Governing rules: [`akos-holistika-operations.mdc`](../../../.cursor/rules/akos-holistika-operations.mdc) (DAMA alignment posture + Supabase two-plane), [`akos-research-area.mdc`](../../../.cursor/rules/akos-research-area.mdc) (Research area identity), [`akos-applied-research-discipline.mdc`](../../../.cursor/rules/akos-applied-research-discipline.mdc) (grounding at activation).
