---
authored: 2026-06-14
lane: DG-B
parent: t0-c-execution-spec
---

# Infonomics × substrate join (+ FINOPS) — T0 DG-B

## Purpose

Run **parallel** to DG-A: value context and tokens as **economic assets** (Initiative 97 infonomics doctrine) while substrate adapters stay visible (DG-A).

## Join matrix

| Economic signal | Data source | Surface | FINOPS link |
|:---|:---|:---|:---|
| Token spend per MADEIRA session | Langfuse | Dossier / internal dashboard | FINOPS_COUNTERPARTY_REGISTER |
| Context volume (KiRBe chunks) | Index stats | Research Center freshness strip | PRICING_TIER hypothesis for alpha |
| Source trust score | Source ledger | Research Center panel | Infonomics valuation input |
| Cache savings | Provider `cached_tokens` | T2 telemetry (gap) | Unit cost reduction narrative |
| Adapter migration cost | SUBSTRATE audit | PMO report | RevOps engagement template |

## FINOPS extensions (FULL bundle — operator selected)

| Register | Alpha use |
|:---|:---|
| `FINOPS_COUNTERPARTY_REGISTER` | Map API providers → cohort billing |
| `PRICING_TIER_REGISTRY` | Design-partner tier hypothesis (α1) |
| `FINOPS_PERFORMANCE_OBLIGATION_REGISTRY` | What we owe alpha partners (support SLA) |

## I96 × I97 overlap (CO-97-004 superseded posture)

Research Center **freshness strip** is not decoration — it is the **economic signal** that context is current and trustworthy. Track in:

- `docs/wip/planning/_trackers/i96-i97-infonomics-scope-overlap-tracker.md` (touch note T0)
- WIP column proposal on `MADEIRA_AIC_PER_TASK_REGISTRY`: `budget_class`, `economic_consumer`

## METRICS_REGISTRY proposals (Research Center)

| metric_id | plain name | formula sketch |
|:---|:---|:---|
| `MET-RC-FRESHNESS-HOURS` | Hours since last index refresh | BFF `freshness` field |
| `MET-RC-TRUST-MEAN` | Mean ledger trust in panel scope | Source ledger aggregate |
| `MET-RC-COST-PER-SESSION` | Langfuse cost / session tag | Trace export |

## DATA_CONTRACT consumer chain

```
SUBSTRATE_REGISTRY → DC-HOL-SUBSTRATE-ADAPTER-001 → BI_CONSUMER → FINOPS counterparty
KiRBe index → DC-HOL-DATA-* → Research Center → METRICS_REGISTRY → infonomics narrative
```

## T0 non-actions

- No INFONOMICS_DISCIPLINE edit (vault minted P6b)
- No CSV tranche until operator gate
