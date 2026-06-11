---
title: Methodology mint — cross-area wiring matrix
intellectual_kind: governance_wiring_report
status: active
decision_id: D-IH-94-A
authored: 2026-06-10
---

# Cross-area wiring — prong lattice + HxPESTAL mint

> Holistika point of view for **continuous work**, not only research ingest. Each row names the
> owning area, wiring status, and next action.

## Wired in this mint (no CSV gate)

| Area | Surface | Status |
|:---|:---|:---|
| **Research / Methodology** | `RESEARCH_PRONG_LATTICE_DISCIPLINE.md`, pillars, synthesis SOP, HxPESTAL + intent tracker | **DONE** |
| **Research / Methodology** | `Methodology/README.md`, `Pillars/README.md`, charter updates | **DONE** |
| **People / Compliance** | `PRECEDENCE.md` (+6 rows) | **DONE** |
| **Tech / System Owner** | `akos/research_ledger_ops.normalize_prong()` + tests | **DONE** |
| **Tech / System Owner** | `scripts/research_ledger.py` consumes BL-* binding | **DONE** |
| **Envoy / MADEIRA** | HxPESTAL ↔ `MADEIRA_METHODOLOGY_MODE.md` cross-link | **DONE** |
| **WIP packs** | `prong-synthesis-template.md`, `hxpestel-intent-tracking-template.md` | **DONE** |

## Deferred — operator CSV / registry gate

| Area | Surface | Gap | Proposed fix |
|:---|:---|:---|:---|
| **People / Compliance** | `process_list.csv` | `hol_resea_dtp_99`, `hol_resea_dtp_315` lack `sop_path` / `runbook_path` | Pair to `SOP-RESEARCH_PRONG_SYNTHESIS_001.md` + `scripts/validate_research_action.py` |
| **People / Compliance** | `CAPABILITY_REGISTRY.csv` | PESTEL/HxPESTAL rows still `planned` in index-derived status | Promote to `active` when operator ratifies |
| **People / Quality Fabric** | `HOLISTIKA_QUALITY_FABRIC.md` §6 | Prong lattice not yet listed as Research-action extension | Add row at next QF index sweep |
| **Data / Architecture** | `CANONICAL_GOVERNANCE_REGISTRY.csv` | New markdown canonicals not inventory rows | I95-style index tranche (Plane-1 only) |
| **Operations** | Executable process catalog | No `hol_resea_dtp_prong_synthesis_*` process row | Mint at I75 P1 or inline tranche |

## Semantic vs mechanical bar

| Layer | What “good” looks like |
|:---|:---|
| **Mechanical** | PRECEDENCE + validators PASS; ledger `BL-*`; templates aligned |
| **Semantic** | Every research pack ends with HxPESTAL master + intent tracker before govern; MADEIRA proves intent fidelity |
| **Continuous job** | Methodology mode surfaces drift when daily work contradicts H harmonisation |

## Cross-area handoffs (who consumes what)

```mermaid
flowchart TB
  subgraph research [Research]
    Lattice[BL-* lattice]
    Hx[HxPESTAL master]
  end
  subgraph tech [Tech]
    Engine[research_ledger.py]
  end
  subgraph envoy [Envoy MADEIRA]
    MM[Methodology mode]
  end
  subgraph people [People]
    PL[process_list pairing]
    QF[Quality Fabric index]
  end
  subgraph data [Data]
    CGR[CANONICAL_GOVERNANCE_REGISTRY]
  end
  Lattice --> Engine
  Hx --> MM
  Lattice --> PL
  Lattice --> QF
  Lattice --> CGR
```

## Recommended next tranche (single operator gate)

One `process_list.csv` commit pairing three rows:

1. `hol_resea_dtp_315` → PESTEL per-prong craft
2. `hol_resea_dtp_99` → HxPESTAL master craft
3. New `hol_resea_dtp_prong_synthesis_001` → umbrella SOP row (optional)

Verification: `py scripts/validate_process_list_pairing.py` + `py scripts/validate_hlk.py`.
