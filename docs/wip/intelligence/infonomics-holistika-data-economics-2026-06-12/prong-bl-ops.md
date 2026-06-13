---
intellectual_kind: research_prong
prong: BL-OPS
topic_cluster: revops-value-map
parent_pack: infonomics-holistika-data-economics-2026-06-12
authored: 2026-06-13
status: active
language: en
linked_decisions:
  - D-INF-ECON
---

# Prong BL-OPS — Operations / PMO consumer

> **Baseline prong:** `BL-OPS` (O5-1 Operations / PMO)  
> **Ledger coverage:** 68 rows (27 CORPINT + 41 OSINT); **0 dedicated skeptic** rows in prong tag *(RevOps/maturity skeptics exist cross-prong)*  
> **Downstream decision:** **D-INF-ECON** (P5 govern)

## Narrative findings

### 1. RevOps spine already maps value across the engagement lifecycle

**RevOps Area Charter** (`SRC-INF-INT-076`), **RevOps Process Catalog** (`SRC-INF-INT-077`), and **Engagement Template Registry** (`SRC-INF-INT-047`) tie delivery templates to revenue motion. **UNIT ECONOMICS** (`SRC-INF-INT-111`) and **Pricing Model** (`SRC-INF-INT-109`) are the closest Holistika comes to an **information value P&L** at ops layer. External Gartner RevOps definition (`SRC-INF-EXT-493`) and HubSpot/Salesforce playbooks (`SRC-INF-EXT-145`, `SRC-INF-EXT-146`) confirm industry treats RevOps as **cross-functional data orchestration for revenue** — structurally aligned with Infonomics.

### 2. WSJF and OKR harvests supply prioritization economics

OSINT rows for **WSJF** (`SRC-INF-EXT-054`, `SRC-INF-EXT-055`) and **OKR** definitions (`SRC-INF-EXT-060`, `SRC-INF-EXT-061`) embed **cost of delay** in prioritization — the same lever Infonomics uses to rank information investments. Holistika **Strategy Decision Log** (`SRC-INF-INT-110`) captures choices but does not always attach **EUR cost of delay** to deferred mirror or research work.

### 3. Mirror emit and cohesion render carry hidden handoff cost

**SOP-OPS_MIRROR_EMIT_TRIGGER_001** (`SRC-INF-INT-108`) and **KM Channel Value Narrative** (`SRC-INF-INT-107`) document operational triggers when canonical data moves to mirrors — each emit is an **information transfer transaction** with compute and verification cost. **Collaborator market rate reference** (`SRC-INF-INT-082`) links ops staffing economics to FIN share splits (`SRC-INF-INT-004`).

### 4. DORA and Accelerate connect delivery performance to business value

**Accelerate DORA research** (`SRC-INF-EXT-302`) and RevOps council maturity (`SRC-INF-EXT-150`) show deployment frequency and lead time correlate with revenue outcomes — Tech CI baseline (`SRC-INF-INT-174`) is an Ops-relevant **information pipeline** metric. Infonomics should not treat "data" separately from **delivery throughput** of governed artifacts.

### 5. Digital twin and DTO literature extends enterprise modeling economics

Infonomics-core harvest includes **Digital Twins of an Organization** (`SRC-INF-EXT-428`), Gartner DTO platforms (`SRC-INF-EXT-429`), and semantic DTO (`SRC-INF-EXT-430`) — external frame for modeling Holistika's three-plane architecture as **simulatable enterprise asset**. Holistika has fragments (engagement templates, process catalog) without a unified DTO cost/benefit case.

## PESTEL — six viewpoints

| Letter | Viewpoint | Finding (cite `SRC-*`) |
|:---|:---|:---|
| **P** | Political | **SOP-REVOPS_REGULATOR_CHECKPOINT_001** (`SRC-INF-INT-081`) embeds regulatory gates in revenue process — political risk priced as schedule delay in WSJF terms (`SRC-INF-EXT-054`). |
| **E** | Economic | Gartner RevOps (`SRC-INF-EXT-493`) + UNIT ECONOMICS (`SRC-INF-INT-111`) define revenue-side value of information handoffs; WSJF (`SRC-INF-EXT-055`) quantifies deferral cost. |
| **S** | Social | QBR SOP (`SRC-INF-INT-080`) and media review SOP (`SRC-INF-INT-079`) socialize value narratives to clients — information value realized only when **shared**. |
| **T** | Technological | DORA metrics (`SRC-INF-EXT-302`) + mirror emit automation (`SRC-INF-INT-108`) — tech change alters cost per governed handoff; DTO platforms (`SRC-INF-EXT-429`) compete as enterprise models. |
| **E** | Environmental | Low direct force; cloud-heavy mirror cadence interacts with FinOps data-transfer (`SRC-INF-EXT-480`). |
| **L** | Legal | Regulator checkpoint SOP (`SRC-INF-INT-081`) and engagement model registry (`SRC-INF-INT-084`) bind legal engagement types to ops templates — unlawful data in RevOps flow creates liability beyond ops KPI miss. |

## Porter — four forces + competition synthesis

| Force | Finding (cite `SRC-*`) |
|:---|:---|
| **Supplier power** | CRM/rev platforms (`SRC-INF-EXT-146`, `SRC-INF-EXT-145`) and DTO vendors (`SRC-INF-EXT-429`) extract subscription rent; collaborator rate tables (`SRC-INF-INT-082`) set labor supplier terms. |
| **Buyer power** | Clients drive QBR evidence (`SRC-INF-INT-080`); Definition of Done vs AC guides (`SRC-INF-EXT-051`, `SRC-INF-EXT-052`) let buyers reject "information complete" without acceptance. |
| **Threat of substitutes** | Ad-hoc PMO spreadsheets substitute for engagement template registry (`SRC-INF-INT-047`) at lower setup cost, higher drift cost. |
| **Threat of new entrants** | RevOps-as-a-service consultancies ship playbooks (`SRC-INF-EXT-493`) without Holistika-grade canonical depth — compete on narrative velocity. |
| **Competition synthesis** | Holistika wins when **handoff cost per governed artifact** (mirror emit + UAT + rev-rec) is visible and lower than substitute consulting stacks. Ops Infonomics = price the pipeline, not just the warehouse. |

## Infonomics hook

**Economic levers for Operations/PMO:** engagement templates as reusable information SKUs; WSJF/cost-of-delay on research and mirror deferrals; UNIT ECONOMICS as rollup surface; DORA metrics as throughput value; mirror emit as internal transfer pricing event.

**Holistika delta vs external Infonomics posture:** strong **value-map narrative** (RevOps charter, unit economics doc); weak **automated COGS allocation** per handoff. External RevOps (`SRC-INF-EXT-493`) assumes CRM telemetry — Holistika adds vault + compliance telemetry not yet in one dashboard.

**Govern options (ranked):**

1. **Append "information handoff COGS" table to UNIT ECONOMICS** (`SRC-INF-INT-111`) — mirror emit, verify profile, research ledger mint, UAT hour defaults. *(recommended)*
2. **WSJF calculator extension for initiative deferrals** — tie carryover index to EUR delay (`SRC-INF-EXT-054`); planning tool, not vault.
3. **DTO pilot charter** referencing DTO OSINT (`SRC-INF-EXT-428`) — high scope; schedule P6c or forward-charter per I97 roadmap.
4. **Ops-only Infonomics SOP** — duplicates RevOps process catalog; lowest integration, highest doc sprawl risk.

## Cross-references

- [`source-ledger-prong-ssot-2026-06-12.md`](source-ledger-prong-ssot-2026-06-12.md) · [`charter.md`](charter.md)
