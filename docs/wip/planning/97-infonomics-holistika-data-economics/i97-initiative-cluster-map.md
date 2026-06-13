---
parent_initiative: INIT-OPENCLAW_AKOS-97
authored: 2026-06-12
---

# I97 initiative cluster map

## Diagram

```mermaid
flowchart TB
  I97[I97 Infonomics Program]
  I96[I96 Research Center]
  I93[I93 Data Area closed]
  I94[I94 Area Architecture]
  I95[I95 HCAM]
  I88[I88 Cross-Area Ops]
  I75[I75 Research Gov]
  I86[I86 Cluster]
  PACK[Infonomics intelligence pack]

  I86 --> I97
  I97 --> I93
  I97 --> I94
  I97 --> I95
  I97 --> I88
  I97 --> I75
  I97 -. overlap .-> I96
  I97 --> PACK
  PACK --> I96
```

## Table

| ID | I97 consumes | I97 produces |
|:---|:---|:---|
| **I93** | DAMA/Data canon (closed) | Citations only — no rewrite |
| **I94** | Area maturity grid | Optional economic-value component (P6c) |
| **I95** | HCAM entity patterns | Information-asset wiring (P6) |
| **I88** | FINOPS / RevOps examples | BL-FIN / BL-OPS ledger rows |
| **I96** | Research Center UX context | Overlap ratify at P5 — not duplicate Track D |
| **I75** | Methodology + radar posture | Research Action rows |
| **I86** | Wave-close cadence | Program-line tracking |
| **I17** | Context economics | BL-ENVOY prong |
| **I67** | Pricing narrative | Forward consumer handoff |

Overlap tracker: [`../_trackers/i96-i97-infonomics-scope-overlap-tracker.md`](../_trackers/i96-i97-infonomics-scope-overlap-tracker.md).
