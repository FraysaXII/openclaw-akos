---
initiative_id: INIT-OPENCLAW_AKOS-97
authored: 2026-06-12
---

# I97 risk register

| ID | Risk | L | I | Mitigation |
|:---|:---|:---:|:---:|:---|
| **R-IH-97-1** | 800-row ledger scope explosion / dedup failure | M | H | Batch subagents by BL prong; URL dedup; baseline-state snapshot |
| **R-IH-97-2** | I96/I97 doctrine collision on Research Center economics | M | H | Scope-overlap tracker; P5 ratify (D-IH-97-D) |
| **R-IH-97-3** | Premature vault mint before govern | L | H | P5 hard stop; P6 pause; synthesis-before-tranche |
| **R-IH-97-4** | Novel doctrine without external cites | M | M | ≥3 Laney/DAMA/DCAM cites in doctrine evidence base |
| **R-IH-97-5** | Subagent output pasted raw without review | M | M | Parent loop: review → brainstorm → operator update |
| **R-IH-97-6** | INITIATIVE_DEPENDENCIES / README drift | L | M | P8 index sweep + validate_index_freshness |
| **R-IH-97-7** | Parked work goes stale under parallel initiatives | M | H | Carryover index CO-97-* + OPERATOR_STEERING contract |
