---
intellectual_kind: research_prong
prong: BL-RESEARCH
topic_cluster: infonomics-core
parent_pack: infonomics-holistika-data-economics-2026-06-12
authored: 2026-06-13
status: active
language: en
downstream_decision: D-INF-ECON
linked_research_sources:
  - SRC-INF-INT-121
  - SRC-INF-INT-048
  - SRC-INF-EXT-182
  - SRC-INF-EXT-173
  - SRC-INF-EXT-352
---

# Prong BL-RESEARCH — Research / Methodology (trust-score economics)

> Per [`SOP-RESEARCH_PRONG_SYNTHESIS_001.md`](../../../references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_PRONG_SYNTHESIS_001.md). Stage-4 synthesis citing `SRC-INF-*` only. Feeds **D-INF-ECON** (P5 govern): how Holistika prices research intake, staleness, and synthesis labour.

## Header

| Field | Value |
|:---|:---|
| Baseline prong | `BL-RESEARCH` — Research / Methodology consumer |
| Ledger rows | **54** cumulative (16 CORPINT + 38 OSINT) |
| Skeptic / tradeoff voices | **18** rows (`topic_cluster: skeptic-tradeoff` or CON notes) |
| Downstream decision | **D-INF-ECON** — enterprise Infonomics model before vault mint (P6 scheduled) |

## Narrative findings

### R.1 Research Action already encodes an information asset lifecycle — Infonomics must not duplicate it

Holistika's research-to-decision discipline (`SRC-INF-INT-121`, `RESEARCH_ACTION_DISCIPLINE`) binds an eight-stage loop (ingest → rate → rank → synthesize → govern → implement → test → iterate) with mandatory source ledgers and Holistika reliability scores. The INTELLIGENCEOPS register (`SRC-INF-INT-048`) adds volatility/staleness economics per collection target. **Delta vs external Infonomics:** Laney-style asset ledgers treat information as balance-sheet inventory; Holistika already treats rated sources as **governed inputs** with control confidence (Safe / Euclid / Keter). D-INF-ECON should extend valuation columns onto existing research registers, not mint a parallel research ledger.

### R.2 External systematic-review canon validates our rating posture — vendor discovery tools do not

Industry-grade synthesis methods — Cochrane (`SRC-INF-EXT-182`), Campbell (`SRC-INF-EXT-183`), GRADE (`SRC-INF-EXT-184`) — converge on explicit evidence grading before policy use. Open bibliographic infrastructure (Crossref `SRC-INF-EXT-171`, CORE `SRC-INF-EXT-179`, DOAJ `SRC-INF-EXT-180`) supports low-cost ingest. Skeptic rows (`SRC-INF-EXT-173` Research Rabbit, `SRC-INF-EXT-176` Elicit, `SRC-INF-EXT-175` Scite) carry vendor-hype or paywall CON notes: they accelerate discovery but **do not replace** ledger rating. Holistika's delta is deterministic validators (`validate_research_action.py`) where vendors offer opaque relevance scores.

### R.3 Radar + substrate doctrine make **staleness** a first-class economic variable

Research Radar discipline (`SRC-INF-INT-122`) and substrate audit cadence (`SRC-INF-INT-125`, `SUBSTRATE_LANDSCAPE_DOCTRINE` `SRC-INF-INT-126`) tie refresh cost to substrate drift. External agent benchmarks (`SRC-INF-EXT-352` AgentBench) and lab evals (`SRC-INF-EXT-353` OSWorld, skeptic: lab-not-ops) warn against conflating research throughput with operational ROI. **Infonomics hook:** model `next_verify_by` and ledger row count as recurring carry cost; unverified OSINT rows are **negative-value inventory** until rated.

### R.4 IntelligenceOps collection SOPs price counterparty-facing research as governed output

IO baseline assessment (`SRC-INF-INT-087`), intelligence report SOP (`SRC-INF-INT-088`), reliability grading (`SRC-INF-INT-144`), and elicitation discipline (`SRC-INF-INT-143`) define human+AIC labour per engagement artifact. Counter-intelligence doctrine (`SRC-INF-INT-085`) sets protect/recall cost. External prompt-engineering SSOT (`SRC-INF-EXT-362`, Anthropic) is adjacent: it lowers synthesis cost but increases model-spend — must appear on the same FinOps plane as research labour, not as "free" automation.

### R.5 Skeptic corpus prevents research-action ornament

Eighteen skeptic rows (e.g. `SRC-INF-EXT-188` systematic-review limits, vendor discovery tools above) argue that **more sources ≠ better decisions**. Holistika already prevents the anti-pattern via stage-5 govern gates. D-INF-ECON should cap marginal OSINT ingest when prong saturation (54 rows, 14 prongs pack-wide) yields duplicate clusters — economic signal is **dedupe before rate**, not expand harvest.

## PESTEL — six viewpoints

| Letter | Viewpoint | Finding (cite `SRC-*`) |
|:---|:---|:---|
| **P** | Political / regulatory | Regulator relationship SOP (`SRC-INF-INT-145`) and GOI/POI stance (`SRC-INF-INT-142`) tie research output to compliance-facing audiences; Infonomics must respect access-level gates on rated sources. |
| **E** | Economic | Cochrane/Campbell/GRADE canon (`SRC-INF-EXT-182`–`184`) treats synthesis labour as explicit cost; vendor discovery tools (`SRC-INF-EXT-173`–`176`, skeptic) externalize that cost as SaaS — compare TCO vs internal Research Action loop. |
| **S** | Social | Open-access directories (`SRC-INF-EXT-179`, `SRC-INF-EXT-180`) widen participant pool; reliability grading SOP (`SRC-INF-INT-144`) prevents crowd wisdom from bypassing Holistika trust scores. |
| **T** | Technological | Crossref API (`SRC-INF-EXT-171`), Connected Papers (`SRC-INF-EXT-172`), AgentBench (`SRC-INF-EXT-352`) enable automated ingest/ranking; Research Action validator chassis (`SRC-INF-INT-121`) is the internal tech moat. |
| **E** | Environmental | Substrate landscape doctrine (`SRC-INF-INT-126`) maps persistence substrates — research asset depreciation follows mirror/validator drift, not calendar time alone. |
| **L** | Legal | Counter-intelligence discipline (`SRC-INF-INT-085`) and intelligence charter (`SRC-INF-INT-086`) bound lawful collection; rated OSINT rows remain Euclid/Keter until operator promote. |

## Porter — four forces + competition synthesis

| Force | Finding (cite `SRC-*`) |
|:---|:---|
| **Supplier power** | Bibliographic/API suppliers (Crossref `SRC-INF-EXT-171`, CORE `SRC-INF-EXT-179`) and model vendors (prompt SSOT `SRC-INF-EXT-362`) can raise ingest/synthesis unit cost; INTELLIGENCEOPS register (`SRC-INF-INT-048`) is internal supplier catalog. |
| **Buyer power** | Engagement triggers (`SRC-INF-INT-282`) and IO report SOP (`SRC-INF-INT-088`) define downstream consumers; they will prefer shorter ledgers with higher mean reliability — pressure to prune low-score OSINT. |
| **Threat of substitutes** | Vendor research assistants (`SRC-INF-EXT-173`–`176`, skeptic CON) substitute discovery, not govern; substituting full Research Action loop loses audit trail (`SRC-INF-INT-121`). |
| **Threat of new entrants** | Agent eval frameworks (`SRC-INF-EXT-352`, `SRC-INF-EXT-353` skeptic) lower barrier to automated research — Holistika differentiates on CSV/registry coupling and validator FAIL gates. |
| **Competition synthesis** | Holistika competes on **governed trust scores + staleness loops**, not raw source volume. External Infonomics vendors sell dashboards; Holistika sells rated, decision-ready inventory wired to vault mint gates. Pack 54-row depth supports per-cluster valuation in master synthesis; skeptic 18-row floor prevents over-investment in discovery SaaS. |

## Infonomics hook

**Economic levers:** source-row TCO (ingest + rate + verify), staleness carry (`next_verify_by`), synthesis labour per prong, marginal value of nth OSINT row in saturated cluster.

**Holistika delta vs external Infonomics:** assets are already **`SRC-*` ledger rows** with Holistika reliability and control confidence — not abstract "data products." Extend registers; do not fork a second research asset taxonomy.

**Govern options (ranked for D-INF-ECON inline-ratify; no vault edit here):**

1. **OPTION A (recommended for P5 evidence packet)** — Attach Infonomics columns to INTELLIGENCEOPS + Research Action ledger schema (`holistika_asset_class`, `verify_cost_band`, `staleness_carry_usd_equiv` advisory); reuse existing rating enums (`SRC-INF-INT-121`).
2. **OPTION B** — Standalone Research Asset Register CSV (new canonical) mirroring ledger IDs — higher audit clarity, higher mint gate + duplicate maintenance (`SRC-INF-INT-048` overlap risk).
3. **OPTION C** — FinOps-only roll-up: aggregate research spend from model + labour tags without per-source valuation — fast P6 start, weak def-valuation for D-INF-ECON skeptics (`SRC-INF-EXT-188`).
4. **OPTION D** — Defer research-specific valuation to I96 Research Center data plane — **scheduled**, not dropped; activates after Research Center SSOT promotion path closes (carryover posture per I97 roadmap).
