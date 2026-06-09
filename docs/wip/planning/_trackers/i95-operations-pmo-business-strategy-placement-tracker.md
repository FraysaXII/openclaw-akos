---
authored: 2026-06-10
language: en
tracker_class: forward-charter
parent_initiatives:
  - INIT-OPENCLAW_AKOS-94
  - INIT-OPENCLAW_AKOS-95
burndown_lane: I95-L6
---

# I95 L6 — Operations PMO business-strategy placement tracker

## Problem

`Operations/PMO/canonicals/business-strategy/` holds strategy artifacts that
**register** under Operations but **execute** via Marketing, Finance, and RevOps.
I94 P3 does **not** mass-relocate these files without a dedicated I95 tranche gate.

## Scope (forward-charter)

| Asset class | Current home | Target owner (proposed) | Gate |
|:---|:---|:---|:---|
| Business strategy briefs | `PMO/canonicals/business-strategy/` | Marketing (GTM) + Finance (revenue model) | I95 L6 operator ratify |
| Capability / portfolio narratives | same | PMO (retain register copy) | Link-only until move |
| RevOps engagement templates | RevOps/canonicals | RevOps (already correct) | No move |

## Activation criteria

1. I95 HCAM verb triples for `strategy_register` → `executes_in` area edges minted
2. AREA-15 placement-integrity sweep passes for each moved canonical
3. Operator inline-ratify on file-move list (no drive-by renames)

## Status

| Date | State | Notes |
|:---|:---|:---|
| 2026-06-10 | **OPEN** | Tracker minted at I94 P3; zero file moves |

## Next action

Schedule as I95 Tranche 6+ after I94 P4 cross-area handoff doctrine lands.
