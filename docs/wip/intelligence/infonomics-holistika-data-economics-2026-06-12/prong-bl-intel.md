---
intellectual_kind: research_prong
prong: BL-INTEL
topic_cluster: research-trust-economics
parent_pack: infonomics-holistika-data-economics-2026-06-12
authored: 2026-06-13
status: active
language: en
downstream_decision: D-INF-ECON
linked_research_sources:
  - SRC-INF-INT-133
  - SRC-INF-EXT-193
  - SRC-INF-EXT-490
  - SRC-INF-EXT-491
  - SRC-INF-INT-137
---

# Prong BL-INTEL — Intelligence Ops (collection ROI / trust economics)

> Per [`SOP-RESEARCH_PRONG_SYNTHESIS_001.md`](../../../references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_PRONG_SYNTHESIS_001.md). Feeds **D-INF-ECON**: value and cost of intelligence collection, verification, and WIP synthesis cross-feeds.

## Header

| Field | Value |
|:---|:---|
| Baseline prong | `BL-INTEL` — Intelligence Ops consumer |
| Ledger rows | **28** cumulative (19 CORPINT + 9 OSINT) — **thin vs pack median** |
| Skeptic / tradeoff voices | **2** rows (`SRC-INF-EXT-490`, `SRC-INF-EXT-491`) |
| Downstream decision | **D-INF-ECON** — attribute intelligence-specific trust economics without duplicating BL-RESEARCH |

## Narrative findings

### I.1 Prong is meta-layer: WIP synthesis packs as intelligence feedstock

Nineteen CORPINT rows are predominantly **other research actions'** ledgers and syntheses: canonical articulation findings (`SRC-INF-INT-133`), collapse maps (`SRC-INF-INT-134`), agentic-os pack (`SRC-INF-INT-131`), Madeira radar synthesis (`SRC-INF-INT-106`), and this pack's own ledger (`SRC-INF-INT-137`). Intelligence Ops Infonomics is therefore **second-order**: value = f(trust of upstream packs, dedupe cost). Thin row count is structural, not a harvest failure.

### I.2 External OSINT verification canon supports collection discipline

OSINT framework (`SRC-INF-EXT-193`), Bellingcat how-tos (`SRC-INF-EXT-194`), First Draft (`SRC-INF-EXT-195`), Google Fact Check (`SRC-INF-EXT-196`), MISP (`SRC-INF-EXT-197`), OpenCTI (`SRC-INF-EXT-198`), NATO handbook (`SRC-INF-EXT-303`) define verification labour per claim. Holistika maps this to reliability grading + control confidence in Research Action — **Intel prong prices verification cycles**, not raw collection volume.

### I.3 Skeptics cap open-source intelligence ROI

Platform hype skeptic (`SRC-INF-EXT-490`, The Register) and RAND limits commentary (`SRC-INF-EXT-491`) argue diminishing returns on broad OSINT ingestion. Aligns with Holistika radar staleness posture: unverified targets are scheduled refresh, not infinite accumulate. D-INF-ECON should encode **marginal ROI collapse** after N sources per topic cluster.

### I.4 Data-governance ownership findings bridge Intel → Compliance economics

`SRC-INF-INT-133` (data governance ownership findings from canonical articulation work) ties intelligence outputs to named owners — prerequisite for Infonomics **ownership column** on intelligence-derived assets. Without owner, asset cannot be depreciated or insured in enterprise Infonomics models.

### I.5 Cross-pack ledger (`SRC-INF-INT-137`) makes this prong self-referential

The Infonomics pack ledger row under BL-INTEL documents that intelligence economics analysis consumes itself as CORPINT — meta-govern loop. Master synthesis must dedupe BL-INTEL vs BL-RESEARCH vs BL-COMPLY on trust-score vocabulary to avoid triple-counting the same `SRC-*` IDs.

## PESTEL — six viewpoints

| Letter | Viewpoint | Finding (cite `SRC-*`) |
|:---|:---|:---|
| **P** | Political / regulatory | NATO OSINT handbook (`SRC-INF-EXT-303`) and verification norms (`SRC-INF-EXT-195`) reflect geopolitical sensitivity — Intel assets carry higher Keter-class handling cost. |
| **E** | Economic | RAND ROI limits (`SRC-INF-EXT-491`) — collection spend must justify decision impact; WIP pack rows (`SRC-INF-INT-106`, `137`) are labour inventory until promoted. |
| **S** | Social | Bellingcat / First Draft (`SRC-INF-EXT-194`–`195`) socialise citizen-investigator norms; Holistika CORPINT register restricts external register on customer surfaces. |
| **T** | Technological | MISP/OpenCTI (`SRC-INF-EXT-197`–`198`) platform TCO vs git-ledger approach (`SRC-INF-INT-137`); Intel tech substitute risk (`SRC-INF-EXT-490`). |
| **E** | Environmental | Many parallel WIP ledgers (`SRC-INF-INT-131`, `136`, `137`) — environmental cost of duplicate synthesis if not deduped at master stage. |
| **L** | Legal | Verification toolchain (`SRC-INF-EXT-196`) supports lawful use; ownership findings (`SRC-INF-INT-133`) required for lawful processing narratives under GDPR-class regimes (see BL-LEGAL prong). |

## Porter — four forces + competition synthesis

| Force | Finding (cite `SRC-*`) |
|:---|:---|
| **Supplier power** | Threat intel platforms (OpenCTI `SRC-INF-EXT-198`) and OSINT SaaS (skeptic `SRC-INF-EXT-490`) control connector pricing. |
| **Buyer power** | Internal consumers (Research Center, engagement triggers) demand verified, stale-dated intel — low tolerance for ungraded WIP (`SRC-INF-INT-133`). |
| **Threat of substitutes** | Ad-hoc analyst notes substitute formal intel; ledgered packs (`SRC-INF-INT-137`) substitute with audit trail. |
| **Threat of new entrants** | Low-code OSINT aggregators — skeptic voice (`SRC-INF-EXT-490`); Holistika moat is registry-linked intelligence ops (`INTELLIGENCEOPS` on BL-RESEARCH). |
| **Competition synthesis** | Intel Infonomics competes on **verified freshness per target**, not collection breadth. Thin 28-row prong + 2 skeptics = honest scope: deepen via INTELLIGENCEOPS economics (BL-RESEARCH), not inflate BL-INTEL harvest. |

## Infonomics hook

**Economic levers:** verification labour per source, staleness refresh, WIP-to-vault promotion cost, dedupe savings when merging pack ledgers.

**Holistika delta:** intelligence value lives in **rated WIP + INTELLIGENCEOPS targets** (see `SRC-INF-INT-048` on BL-RESEARCH), not standalone Intel SKU.

**Govern options (ranked; no vault edit):**

1. **OPTION A (recommended)** — Fold Intel economics into INTELLIGENCEOPS register extensions (volatility_class × verify_cost) — single SSOT, respects thin prong.
2. **OPTION B** — Separate Intel Asset Register for promoted intel only — clearer external audit, risks duplicate IDs with Research Action ledger (`SRC-INF-INT-137`).
3. **OPTION C** — Qualitative ROI bands from skeptic corpus only (`SRC-INF-EXT-491`) — minimal schema change, weak granularity.
4. **OPTION D** — Purchase OpenCTI/MISP managed service — **scheduled** evaluation post D-INF-ECON; high substitute + platform skeptic (`SRC-INF-EXT-490`) requires operator ratify.
