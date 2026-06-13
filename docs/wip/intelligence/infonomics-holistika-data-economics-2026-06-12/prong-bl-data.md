---
intellectual_kind: research_prong
prong: BL-DATA
topic_cluster: dama-dmbok
parent_pack: infonomics-holistika-data-economics-2026-06-12
authored: 2026-06-13
status: active
language: en
linked_decisions:
  - D-INF-ECON
---

# Prong BL-DATA — Data / DataOps consumer

> **Baseline prong:** `BL-DATA` (O5-1 Data / DataOps)  
> **Ledger coverage:** 152 rows (32 CORPINT + 120 OSINT); **3 skeptic** voices  
> **Downstream decision:** **D-INF-ECON** — what economic model Holistika adopts for information assets (P5 govern gate)

## Narrative findings

### 1. Holistika already treats data as a contract-bound asset, not a file dump

The vault encodes data products through governed registers rather than ad-hoc folders. The **Data Contract Registry** (`SRC-INF-INT-012`) pairs with maintenance SOP (`SRC-INF-INT-022`) and the **Data Contract Standard** (`SRC-INF-INT-054`), while **Data Governance Policy** (`SRC-INF-INT-055`) and **Semantic Council SOP** (`SRC-INF-INT-056`) name ownership and change control. **BI Consumer Registry** (`SRC-INF-INT-042`) and **Metrics Registry** (`SRC-INF-INT-021`) make downstream consumers explicit — the same "who consumes what" posture Douglas Laney's Infonomics canon requires before any valuation exercise (`SRC-INF-EXT-477`, `SRC-INF-EXT-478`).

**Delta vs Infonomics canon:** we have *governance* and *contract* surfaces; we lack a **monetization ledger** (no row ties contract breach cost, mirror lag cost, or semantic drift to EUR/USD).

### 2. Industry maturity models score *components × levels* — our bar is flatter

External canon converges on multi-dimensional maturity: **DAMA-DMBOK** knowledge areas (`SRC-INF-EXT-001`) and **EDM Council DCAM** with eight components, 34 capabilities, and six-level scoring (`SRC-INF-EXT-004`, `SRC-INF-EXT-005`). DCAM v3.1 adds a Business Data Knowledge component and consolidation patterns (`SRC-INF-EXT-006`). Holistika's **SSOT Registry Audit Discipline** (`SRC-INF-INT-057`) and **Entity Catalog** (`SRC-INF-INT-127`) mirror the *inventory* slice of DCAM but not the *level* axis — a `pass` on area completeness is terminal, not a rung toward quantitatively managed value.

### 3. Data mesh economics push domain ownership — we are half-mesh already

Dehghani's data mesh principles (`SRC-INF-EXT-481`) and lineage tooling in the harvest (Atlas `SRC-INF-EXT-123`, DataHub `SRC-INF-EXT-124`, Marquez `SRC-INF-EXT-125`) assume **domain-owned data products** with versioned contracts and SLOs. Holistika's adapter registries (RPA `SRC-INF-INT-006`, billing `SRC-INF-INT-007`) and Supabase module registry (`SRC-INF-INT-053`) already decentralize *integration* economics; **DataOps Discipline** (`SRC-INF-INT-128`) and **Semantic Layer** (`SRC-INF-INT-090`) carry the serving plane. The gap is explicit **product P&L** per domain (cost of mirror emit + verify profile + operator toil).

### 4. Skeptic voices warn against asset metaphors and mesh overreach

InfoQ's data mesh tradeoff framing (`SRC-INF-EXT-482`) and Wired's "data is the new oil" critique (`SRC-INF-EXT-483`) argue that valuation rhetoric outruns measurable benefit — mesh without federated governance becomes "distributed data swamp." A dedicated mesh skeptic row (`SRC-INF-EXT-139`) reinforces the same posture. Holistika should treat Infonomics as **evidence-backed cost/benefit**, not slogan adoption.

### 5. Observability and quality tooling carry hidden TCO

The infonomics-core harvest includes **Great Expectations** (`SRC-INF-EXT-126`), **Soda** (`SRC-INF-EXT-127`), **OpenTelemetry gen-AI semconv** (`SRC-INF-EXT-347`), and **GraphRAG** research (`SRC-INF-EXT-368`) — each adds license, compute, and operator-attention cost. **Area BI Profile** (`SRC-INF-INT-091`) names consumption patterns but not unit economics per check.

## PESTEL — six viewpoints

| Letter | Viewpoint | Finding (cite `SRC-*`) |
|:---|:---|:---|
| **P** | Political / regulatory | EU data governance and AI Act pressure raise the cost of *uncontracted* data flows; Holistika's contract registry (`SRC-INF-INT-012`) is the compliance-facing asset, while GDPR legal-basis guidance in the Legal prong (`SRC-INF-EXT-241`) sets the penalty floor for mishandling. |
| **E** | Economic | Laney's Infonomics frame (`SRC-INF-EXT-477`, `SRC-INF-EXT-478`) treats information as balance-sheet-worthy when monetization, management, and measurement align; DCAM (`SRC-INF-EXT-004`) adds auditable capability scoring — Holistika has management/measurement fragments without monetization rows. |
| **S** | Social | Data mesh assumes **domain literacy** among product owners (`SRC-INF-EXT-481`); Holistika's Semantic Council (`SRC-INF-INT-056`) socializes semantics but does not yet price the council's meeting cost against rework avoided. |
| **T** | Technological | Lineage stack options (Atlas `SRC-INF-EXT-123`, DataHub `SRC-INF-EXT-124`) and semantic-layer comparisons (`SRC-INF-EXT-443`) compete on integration TCO; Supabase module registry (`SRC-INF-INT-053`) locks our persistence economics to Postgres mirror emit. |
| **E** | Environmental | Cloud data transfer and idle mirror storage (FinOps data-transfer working group `SRC-INF-EXT-480`, cited from FIN prong) inflate the **carbon-adjacent** cost of over-replication — relevant when three-plane architecture duplicates ledger → vault → mirror. |
| **L** | Legal | Data contracts (`SRC-INF-INT-054`) are the legal-technical handshake; DPA templates live under Legal (`SRC-INF-INT-165`) — economic valuation must respect **lawful basis** before any external data product pricing. |

## Porter — four forces + competition synthesis

| Force | Finding (cite `SRC-*`) |
|:---|:---|
| **Supplier power** | Lineage/quality vendors (Expectations `SRC-INF-EXT-126`, Soda `SRC-INF-EXT-127`) and cloud persistence (Supabase modules `SRC-INF-INT-053`) set switching cost once contracts embed in CI; semantic-layer platforms (`SRC-INF-EXT-443`) raise exit cost if ontology lives off-repo. |
| **Buyer power** | BI consumers registered (`SRC-INF-INT-042`) can demand SLAs; Gartner/Forrester actionable-analytics definitions (`SRC-INF-EXT-464`, `SRC-INF-EXT-465`) raise the bar for "insight" deliverables — buyers treat dashboards as commodities unless tied to decisions. |
| **Threat of substitutes** | Manual CSV governance + spreadsheet metrics substitute for full DCAM (`SRC-INF-EXT-004`) at lower upfront cost; mesh skeptics (`SRC-INF-EXT-482`) argue federated architecture substitutes for central warehouse with *political* not technical savings. |
| **Threat of new entrants** | GraphRAG (`SRC-INF-EXT-368`) and gen-AI observability (`SRC-INF-EXT-347`) let newcomers ship "good enough" retrieval without Holistika-grade contract discipline — speed substitutes for trust if buyers skip reliability grading. |
| **Competition synthesis** | Holistika competes on **governed trust** (contracts + reliability scores + mirror parity) not raw data volume. External players compete on time-to-insight. The win condition is making contract-breach and mirror-drift **visible in economic terms** before buyers default to faster, looser substitutes. |

## Infonomics hook

**Economic levers for Data/DataOps:** contract registry as asset inventory; mirror/verify **run-cost** as carrying cost; semantic drift as depreciation; consumer registry as revenue-attribution spine; DCAM-style **level** as value unlock roadmap.

**Holistika delta vs external Infonomics posture:** strong on *management* (CORPINT registers, SOPs) and *measurement* (validators, BI profile); weak on *monetization* (no priced data products, no breach-cost register). Skeptics (`SRC-INF-EXT-482`, `SRC-INF-EXT-483`) caution against naming assets without cash-flow linkage.

**Govern options (ranked — P5 inline-ratify; no vault edit here):**

1. **Extend DATA_CONTRACT_REGISTRY with economic columns** (estimated mirror cost, verify cost, consumer count, breach severity €) — lowest doctrine churn; piggybacks existing maintenance SOP (`SRC-INF-INT-022`). *(recommended — preserves SSOT, testable in FINOPS recon.)*
2. **Mint lightweight `DATA_ASSET_VALUATION_REGISTER.csv`** as Plane-1 CSV per DCAM component map (`SRC-INF-EXT-004`) — higher operator gate; enables Laney-style monetization rows without rewriting Data Governance Policy.
3. **Defer valuation to I96 Research Center economics** — absorb Track D overlap via scope-overlap tracker; Data prong stays governance-only until Research Center ships consumer inventory (scheduled, not dropped).
4. **Adopt full DCAM 6-level scoring in area completeness** — largest lift; aligns with area-completeness precedent (`SRC-AREA-EXT-*` harvest) but risks pause fatigue before P6 vault tranche.

## Cross-references

- Prong SSOT: [`source-ledger-prong-ssot-2026-06-12.md`](source-ledger-prong-ssot-2026-06-12.md)
- Charter: [`charter.md`](charter.md) · Planning: [`../../planning/97-infonomics-holistika-data-economics/master-roadmap.md`](../../planning/97-infonomics-holistika-data-economics/master-roadmap.md)
