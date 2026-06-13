---
intellectual_kind: research_prong_ssot
parent_pack: infonomics-holistika-data-economics-2026-06-12
authored: 2026-06-12
last_review: 2026-06-12
language: en
discipline: RESEARCH_PRONG_LATTICE_DISCIPLINE.md
---

# Source ledger prong SSOT — Infonomics pack (2026-06-12)

> **Binding:** ledger `prong` column uses **baseline consumer IDs (`BL-*`)** only.
> Charter aliases (`P1-*` … `P14-*`) are pack-local shorthand documented here.
> Normalize at ingest via `akos.research_ledger_ops.normalize_prong()`.

## I97 alias table (14 charter aliases → 14 baseline prongs)

| Charter alias | Baseline ID | O5-1 consumer | Infonomics focus (P2–P4) |
|:---|:---|:---|:---|
| `P1-DATA` | `BL-DATA` | Data / DataOps | Asset valuation, contracts, lineage cost, mirror economics |
| `P2-FINANCE` | `BL-FIN` | Finance / FinOps | FINOPS registers, rev-rec, unit economics of data products |
| `P3-LEGAL` | `BL-LEGAL` | Legal | IP, access levels, audit trail, adviser data flows |
| `P4-MARKETING` | `BL-MKT` | Marketing / Reach | MarTech ROI, audience data, brand surface economics |
| `P5-OPS` | `BL-OPS` | Operations / PMO | Process catalog value, handoff cost, cohesion render |
| `P6-PEOPLE` | `BL-PEOPLE` | People / Quality Fabric | Regression cost, synthesis/UAT economics, share patterns |
| `P7-TECH` | `BL-TECH` | Tech / System Owner | Substrate cost, CI verify profiles, tooling TCO |
| `P8-RESEARCH` | `BL-RESEARCH` | Research / Methodology | Research Action, radar, trust-score economics |
| `P9-COMPLIANCE` | `BL-COMPLY` | People / Compliance | PRECEDENCE, CSV gates, canonical mint cost |
| `P10-INTEL` | `BL-INTEL` | Intelligence Ops | Collection target ROI, volatility/staleness economics |
| `P11-ENVOY` | `BL-ENVOY` | Envoy / MADEIRA | Agentic context/token economics, tool catalog |
| `P12-ADAPTER` | `BL-ADAPTER` | Data / RevOps adapters | Adapter lifecycle, normalized integration TCO |
| `P13-UX` | `BL-UX` | Marketing / Brand UX | Insight-machine value, operator journey economics |
| `P14-ETHICS` | `BL-ETHICS` | People / Ethics | Ethical floor vs legal minimum; reputational cost |

## Synthesis file naming (P4)

| Baseline ID | Target synthesis path |
|:---|:---|
| `BL-DATA` | `prong-bl-data.md` |
| `BL-FIN` | `prong-bl-fin.md` |
| `BL-LEGAL` | `prong-bl-legal.md` |
| `BL-MKT` | `prong-bl-mkt.md` |
| `BL-OPS` | `prong-bl-ops.md` |
| `BL-PEOPLE` | `prong-bl-people.md` |
| `BL-TECH` | `prong-bl-tech.md` |
| `BL-RESEARCH` | `prong-bl-research.md` |
| `BL-COMPLY` | `prong-bl-comply.md` |
| `BL-INTEL` | `prong-bl-intel.md` |
| `BL-ENVOY` | `prong-bl-envoy.md` |
| `BL-ADAPTER` | `prong-bl-adapter.md` |
| `BL-UX` | `prong-bl-ux.md` |
| `BL-ETHICS` | `prong-bl-ethics.md` |

## Source ID convention

| Prefix | Category | Example |
|:---|:---|:---|
| `SRC-INF-INT-*` | CORPINT internal | `SRC-INF-INT-001` |
| `SRC-INF-EXT-*` | OSINT external | `SRC-INF-EXT-001` |

## Cross-references

- Lattice discipline: [`RESEARCH_PRONG_LATTICE_DISCIPLINE.md`](../../../references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_PRONG_LATTICE_DISCIPLINE.md)
- Prong synthesis SOP: [`SOP-RESEARCH_PRONG_SYNTHESIS_001.md`](../../../references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_PRONG_SYNTHESIS_001.md)
- Pydantic schema: [`akos/hlk_research_action.py`](../../../../akos/hlk_research_action.py)
