---
intellectual_kind: gap_analysis
phase: post_sweep
authored: 2026-06-15
baseline: capability-registry-gap-analysis-pre-sweep-2026-06-15.md
operator_gate: mint-gate-packet-gci-capability-tranche-2026-06-15.md
---

# Capability registry — post-sweep gap analysis

> Compares **pre-sweep baseline** to **proposed mint state** after semantic review + crosswalk draft. Does not reflect committed vault CSV until operator ratifies mint packet.

## Metric delta

| Metric | Pre-sweep | Post-sweep (proposed) | Δ |
|:---|:---:|:---:|:---:|
| Registry rows | 99 | **103** (+4 net-new) | +4 |
| Empty `substrate_id` (all rows) | 99 (100%) | **85 (~82%)** | −18 backfilled |
| Empty `substrate_id` (active Applied AI & MADEIRA) | 8 (100%) | **0** | −8 |
| ACIM rows | 7 | **30** | +23 |
| Alpha crosswalk edges | 0 formal | **36** | +36 |
| Net-new CAP-* rows | — | **4** | modes, RBAC, Research Center, context economics |
| Methodology v3.2 on touched rows | 2 | **~25** | refresh |
| Validator substrate FAIL (active MADEIRA) | No | **Yes** (same commit) | GCI-04 |

## Governance lattice — after proposed mint

| Layer | Pre-sweep gap | Post-sweep posture |
|:---|:---|:---|
| Capability FK | Hollow | 18 alpha-critical substrates populated |
| Alpha ↔ vault join | Informal matrix only | Crosswalk CSV + optional `alpha_inventory_refs` column |
| Implementation proof | 7/99 | 30/99 (alpha cluster covered) |
| Context economics | Spec ratified; no CAP row | `CAP-MADEIRA-CONTEXT-ECONOMICS` planned → T2 |
| Infonomics (M15) | Partial | Maps to `CAP-DATA-PLATFORM-PRODUCTS`; I97 join **scheduled** |
| Multi-tenant voice (M27) | Gap | **Scheduled** CO-MBH-008 — unchanged |

## Residual gaps (scheduled, not dropped)

| Gap | Carryover / trigger | Owner |
|:---|:---|:---|
| Substrate FK for non-alpha 81 rows | Area-by-area I95 continuation | Capability Curator |
| CAP-M27 multi-tenant voice | CO-MBH-008 post-α2 | I76/I74 |
| T2 context economics code | CO-MBH-001/002 after this mint | I76 |
| Supabase capability mirror DML | Holistika ops lattice | Data Governance |
| Full 1112-row process re-collapse | I95 area tranches | PMO |

## Verification matrix (post-mint target)

```powershell
py scripts/validate_capability_registry.py
py scripts/validate_aic_capability_implementation_matrix.py
py scripts/validate_hlk.py
```

## Next gate

Operator ratify: `mint-gate-packet-gci-capability-tranche-2026-06-15.md` → AIC commits CSV tranche + validator ramp.
