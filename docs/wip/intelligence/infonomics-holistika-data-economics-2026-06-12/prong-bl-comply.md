---
intellectual_kind: research_prong
prong: BL-COMPLY
topic_cluster: dama-dmbok
parent_pack: infonomics-holistika-data-economics-2026-06-12
authored: 2026-06-13
status: active
language: en
downstream_decision: D-INF-ECON
linked_research_sources:
  - SRC-INF-INT-241
  - SRC-INF-INT-008
  - SRC-INF-EXT-417
  - SRC-INF-EXT-201
  - SRC-INF-EXT-498
---

# Prong BL-COMPLY — People / Compliance (canonical mint cost)

> Per [`SOP-RESEARCH_PRONG_SYNTHESIS_001.md`](../../../references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_PRONG_SYNTHESIS_001.md). Feeds **D-INF-ECON**: economic model for compliance SSOT, operator gates, and registry audit labour.

## Header

| Field | Value |
|:---|:---|
| Baseline prong | `BL-COMPLY` — People / Compliance consumer |
| Ledger rows | **139** cumulative (63 CORPINT + 76 OSINT) — largest prong in pack |
| Skeptic / tradeoff voices | **10** rows |
| Downstream decision | **D-INF-ECON** — price governance inventory before enterprise doctrine mint |

## Narrative findings

### C.1 Holistika compliance estate is already a dense, priced asset graph

Sixty-three CORPINT rows map canonical/mirrored registries: CANONICAL_REGISTRY (`SRC-INF-INT-008`), CANONICAL_GOVERNANCE_REGISTRY (`SRC-INF-INT-010`), DECISION_REGISTER (`SRC-INF-INT-033`), INITIATIVE_REGISTRY (`SRC-INF-INT-009`), dimension registries (AUDIENCE `SRC-INF-INT-037`, CAPABILITY `SRC-INF-INT-039`, AIC `SRC-INF-INT-035`), and PRECEDENCE (`SRC-INF-INT-241`). PROCESS_LIST + BASELINE_ORGANISATION (`SRC-INF-INT-200`, `SRC-INF-INT-224`) encode operator-approval labour per mint. **Infonomics insight:** each registry row is a **maintained asset** with validator + mirror emit cost — not a one-time document.

### C.2 DAMA-DMBOK external canon aligns on metadata-as-asset — but Holistika is more operator-gated

OSINT DAMA sources (`SRC-INF-EXT-417` DAMA International, `SRC-INF-EXT-418` governance guide, `SRC-INF-EXT-419` DAMA vs DCAM, `SRC-INF-EXT-420` framework overview) describe knowledge areas, lineage, and scalable governance. External posture: enterprise metadata catalogs. Holistika delta: **git-canonical CSV + AskQuestion gates** (`PRECEDENCE` `SRC-INF-INT-241`) make mint cost explicit in operator time, not only platform license fees.

### C.3 Four-registry audit loop (SSOT discipline) is compliance Infonomics backbone

CANONICAL_RELATIONSHIP_REGISTRY (`SRC-INF-INT-020`) and automation (`validate_canonical_governance_registry` `SRC-INF-INT-251`, seed scripts `SRC-INF-INT-250`) mechanize audit. FINOPS counterparty register under Compliance (`SRC-INF-INT-003`) links people/compliance plane to economic counterparty identity. D-INF-ECON should treat **failed validator cycles** as depreciation events on registry asset value.

### C.4 Skeptic voices warn against audit theatre and platform sprawl

Audit fatigue (`SRC-INF-EXT-201`, HBR skeptic), audit automation limits (`SRC-INF-EXT-211`), and data-governance platform skeptic (`SRC-INF-EXT-498`, The Register) caution that more controls ≠ more value. Holistika's deterministic release-gate (`SRC-INF-INT-251` family) is the counter-weight — Infonomics should reward **PASS validators**, not row count.

### C.5 Initiative + decision registers make governance spend traceable

INITIATIVE_REGISTRY (`SRC-INF-INT-009`, holistika reliability 5 / external 4) and DECISION_REGISTER (`SRC-INF-INT-033`) tie spend to ratified decisions — direct input for attributing Infonomics implementation tranches (I97 P6) to decision IDs rather than anonymous overhead.

## PESTEL — six viewpoints

| Letter | Viewpoint | Finding (cite `SRC-*`) |
|:---|:---|:---|
| **P** | Political / regulatory | PRECEDENCE + process_list (`SRC-INF-INT-241`, `SRC-INF-INT-200`) encode operator ratification — political cost of canonical change is explicit, unlike vendor "auto-governance." |
| **E** | Economic | DAMA-DMBOK (`SRC-INF-EXT-417`–`420`) frames metadata management TCO; Holistika adds per-row validator/mirror labour on 63 CORPINT assets. |
| **S** | Social | AUDIENCE_REGISTRY (`SRC-INF-INT-037`) and ARTIFACT_CLASS (`SRC-INF-INT-036`) socialise who may touch assets — Infonomics ownership follows audience strictness. |
| **T** | Technological | SUBSTRATE_REGISTRY (`SRC-INF-INT-011`), REPOSITORY_REGISTRY (`SRC-INF-INT-034`), AIC_REGISTRY (`SRC-INF-INT-035`) inventory tech/agent substrates — depreciation when substrate enum drifts. |
| **E** | Environmental | Canonical mint creates long-lived git artifacts; skeptic audit automation (`SRC-INF-EXT-211`) warns sustainability of manual audit expansion. |
| **L** | Legal | FINOPS counterparty register (`SRC-INF-INT-003`) and compliance vs ethics boundary (cross-prong `SRC-INF-INT-025`) separate legal minimum from ethical floor — Infonomics must not collapse them. |

## Porter — four forces + competition synthesis

| Force | Finding (cite `SRC-*`) |
|:---|:---|
| **Supplier power** | DAMA body of knowledge vendors and governance platforms (skeptic `SRC-INF-EXT-498`) supply catalog software; Holistika supplies internal SSOT labour (`SRC-INF-INT-008` stack). |
| **Buyer power** | Operator is sole buyer of mint gates — INITIATIVE_REGISTRY (`SRC-INF-INT-009`) tracks active demand; fatigue skeptics (`SRC-INF-EXT-201`) raise cost of asking too often. |
| **Threat of substitutes** | Spreadsheets or ad-hoc Notion governance substitute low upfront cost; PRECEDENCE (`SRC-INF-INT-241`) + validators substitute with audit-grade traceability. |
| **Threat of new entrants** | DCAM-style maturity vendors (`SRC-INF-EXT-419`) offer assessment products; Holistika embeds maturity in area completeness + release-gate instead. |
| **Competition synthesis** | Compliance Infonomics competition is **trust per validator run**, not registry cardinality. 139 ledger rows justify cluster-weighted valuation in master synthesis; Holistika wins when canonical+mirror parity is measurable (`SRC-INF-INT-251`). |

## Infonomics hook

**Economic levers:** cost per canonical CSV mint (operator gate + validator + mirror emit), registry row maintenance, decision/initiative linkage overhead, audit failure rework.

**Holistika delta:** compliance assets are **git-canonical with PRECEDENCE class** — valuation must split canonical vs mirrored (`SRC-INF-INT-241`) rather than treating all rows as equal book value.

**Govern options (ranked; no vault edit):**

1. **OPTION A (recommended)** — Extend CANONICAL_GOVERNANCE_REGISTRY (`SRC-INF-INT-010`) with advisory `maintenance_cost_band` + `last_validator_pass` — ties Infonomics to existing SSOT audit loop.
2. **OPTION B** — Per-registry FinOps tags in FINOPS counterparty-style satellite CSV — clearer dollars, extra CSV gate (`SRC-INF-INT-003` pattern).
3. **OPTION C** — Qualitative maturity € bands only (DAMA ladder `SRC-INF-EXT-417`) without row-level costing — fast, weak for skeptics (`SRC-INF-EXT-201`).
4. **OPTION D** — External GRC platform ledger import — high substitute risk (`SRC-INF-EXT-498`); defer unless operator ratifies vendor spine change.
