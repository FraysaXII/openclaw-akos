---
intellectual_kind: research_prong
prong: BL-ADAPTER
topic_cluster: data-mesh-products
parent_pack: infonomics-holistika-data-economics-2026-06-12
authored: 2026-06-13
status: active
language: en
downstream_decision: D-INF-ECON
linked_research_sources:
  - SRC-INF-INT-001
  - SRC-INF-INT-089
  - SRC-INF-EXT-330
  - SRC-INF-EXT-500
  - SRC-INF-EXT-121
---

# Prong BL-ADAPTER — Data / RevOps adapters (integration TCO)

> Per [`SOP-RESEARCH_PRONG_SYNTHESIS_001.md`](../../../references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_PRONG_SYNTHESIS_001.md). Feeds **D-INF-ECON**: lifecycle cost of normalized integrations across RevOps, MarTech, RPA, and billing planes.

## Header

| Field | Value |
|:---|:---|
| Baseline prong | `BL-ADAPTER` — Data / RevOps adapter consumer |
| Ledger rows | **67** cumulative (15 CORPINT + 52 OSINT) |
| Skeptic / tradeoff voices | **14** rows (vendor lock-in, RPA hype) |
| Downstream decision | **D-INF-ECON** — value adapter registries vs integration sprawl |

## Narrative findings

### A.1 Fifteen CORPINT rows prove Normalized Adapter Pattern at scale

Nine domain adapter registries — RevOps (`SRC-INF-INT-001`), Contract (`SRC-INF-INT-002`), RPA (`SRC-INF-INT-006`), Billing (`SRC-INF-INT-007`), Attribution (`SRC-INF-INT-015`), Communication/CRM/Email/Scheduling (`SRC-INF-INT-016`–`019`) — plus COMPONENT_SERVICE_MATRIX (`SRC-INF-INT-089`) and maintenance SOP (`SRC-INF-INT-153`). Validators (`SRC-INF-INT-185`, `189`) mechanize TCO of drift. Each adapter row is a **renewable integration asset** with status enum and owner — Infonomics should deprecate retired adapters explicitly.

### A.2 Enterprise Integration Patterns + data-mesh discourse frame sprawl cost

Enterprise Integration Patterns (`SRC-INF-EXT-330`) and Thoughtworks sprawl TCO (`SRC-INF-EXT-500`) quantify point-to-point explosion. Holistika's delta: adapters are **CSV-governed products** with paired SOPs, not one-off Zapier zaps. OSINT harvest of iPaaS/RPA vendors (Power Automate `SRC-INF-EXT-101`–`103`, Make `SRC-INF-EXT-104`, n8n `SRC-INF-EXT-105`, Zapier skeptic `SRC-INF-EXT-106`, UiPath skeptic `SRC-INF-EXT-107`) provides market rate cards for compare.

### A.3 Skeptic rows flag vendor-specific tax

RPA hype skeptic (`SRC-INF-EXT-121`), Power Platform DLP skeptic (`SRC-INF-EXT-103`), Zapier/UiPath/AWS Step Functions vendor CON notes — integration **list price understates exit cost**. Adapter registry must carry `license_class` + `exit_cost_band` advisory columns for D-INF-ECON.

### A.4 Automation OS harvest duplicates overlap with BL-ENVOY MCP tools

Fifty-two OSINT rows include orchestration platforms that BL-ENVOY also cites (MCP, agent frameworks). Master synthesis must allocate **integration vs agent runtime** cost to avoid double-counting the same vendor subscription across prongs.

### A.5 Component service matrix links adapters to deployable services

COMPONENT_SERVICE_MATRIX (`SRC-INF-INT-089`) connects adapter status to sibling-repo deploy health — Infonomics value realization requires **consumer repo READY** (REPOSITORY_REGISTRY on BL-COMPLY). Adapters without deployed consumer are WIP inventory.

## PESTEL — six viewpoints

| Letter | Viewpoint | Finding (cite `SRC-*`) |
|:---|:---|:---|
| **P** | Political / regulatory | Power Platform DLP (`SRC-INF-EXT-103`, skeptic) — political risk of citizen integrators bypassing compliance gates. |
| **E** | Economic | Integration sprawl TCO (`SRC-INF-EXT-500`); iPaaS pricing (Make `SRC-INF-EXT-104`, Workato `SRC-INF-EXT-109`) vs internal adapter maintenance (`SRC-INF-INT-153`). |
| **S** | Social | MarTech adapters (CRM/Email `SRC-INF-INT-017`–`018`) touch customer data — social licence tied to audience registry (BL-COMPLY). |
| **T** | Technological | EIP catalog (`SRC-INF-EXT-330`) stable patterns; RPA/UiPath (`SRC-INF-EXT-107` skeptic) brittle UI automation depreciates fast. |
| **E** | Environmental | Retired adapters left connected incur secret-scan + drift cost — validator (`SRC-INF-INT-185`) is sustainability gate. |
| **L** | Legal | Contract adapter registry (`SRC-INF-INT-002`) — integration terms are legal assets; billing adapter (`SRC-INF-INT-007`) ties revenue recognition. |

## Porter — four forces + competition synthesis

| Force | Finding (cite `SRC-*`) |
|:---|:---|
| **Supplier power** | Microsoft Power Platform (`SRC-INF-EXT-101`–`103`), UiPath (`SRC-INF-EXT-107`), hyperscaler step functions (`SRC-INF-EXT-112` skeptic) — high switching cost. |
| **Buyer power** | RevOps/SMO internal buyers can standardize on registry-approved adapters only (`SRC-INF-INT-001`, `002`). |
| **Threat of substitutes** | Custom code integration substitutes registry discipline; COMPONENT_SERVICE_MATRIX (`SRC-INF-INT-089`) substitutes with mapped services. |
| **Threat of new entrants** | n8n/Pipedream low-cost entrants (`SRC-INF-EXT-105`, `111`) — pressure license economics on premium adapters. |
| **Competition synthesis** | Adapter Infonomics competes on **governed connector cardinality** — fewer, validated adapters beat sprawl (`SRC-INF-EXT-500`). Holistika moat: nine CORPINT registries + validators vs ad-hoc iPaaS. |

## Infonomics hook

**Economic levers:** license + ops hours per adapter row, incident cost on drift FAIL, consumer-repo revenue enabled (`SRC-INF-INT-089`), decommission savings.

**Holistika delta:** adapters are **first-class CSV products** with validators — book them as amortized integration assets, not expense-only SaaS lines.

**Govern options (ranked; no vault edit):**

1. **OPTION A (recommended)** — Add `annual_cost_band`, `status`, `consumer_repo_slug`, `last_validator_pass` to each adapter registry SSOT — unified Normalized Adapter Pattern economics.
2. **OPTION B** — Central ADAPTER_FINOPS rollup CSV — easier reporting, duplicates nine registries (`SRC-INF-INT-001` family).
3. **OPTION C** — Benchmark-only model from OSINT rate cards (`SRC-INF-EXT-104`–`109`) without row linkage — fast, non-auditable.
4. **OPTION D** — Consolidate all adapters into single iPaaS vendor — skeptic risk (`SRC-INF-EXT-103`, `121`); requires operator ratify exit from multi-registry pattern.
