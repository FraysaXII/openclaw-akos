---
intellectual_kind: timing_doctrine
authored: 2026-06-15
audience: J-OP, J-AIC
operator_correction: 2026-06-15
---

# Agent run timing vs human calendar (info economics)

## Binding distinction

| Unit | Meaning | Typical magnitude |
|:---|:---|:---|
| **Agent run** | One AIC execution block in Cursor (this session's mechanical work) | **5–15 min** (occasionally up to ~90 min for huge pre-tranche e2e) |
| **Human calendar tranche** | When the operator expects to **ratify, review, or deploy** | Days to weeks on their schedule |
| **Initiative phase** | Governed planning commit boundary | Per `master-roadmap.md` |

**Do not label agent runs as "Week-1" / "Week-2".** Use **tranche IDs** (R1, R2, T1, T1b) for agent work; use **human calendar** only in carryover `next_review_date` and operator-facing schedules.

## Applied to this pack

| Label | What it actually is |
|:---|:---|
| **Refresh tranche R1** | Substrate reliability ingest + P-I synthesis + mint gate draft (~one agent run block) |
| **Mint tranche T1b** | CSV commit after operator ratify (human gate + one agent run) |
| **I96 L3 capture** | One agent run once `hlk-erp` dev is up |

## Carryover dating

`next_review_date` on carryover rows = **operator calendar**, not "when the agent will finish."
