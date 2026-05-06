---
language: en
status: candidate
initiative: I60 — Process_list harmonisation (mint)
---

# I60 candidate — Process_list harmonisation (mint)

## Scope

Mint the ~15 new `process_list.csv` rows proposed in I59 P8 across 4 program
tranches (PMO, Tech, Operations, FinOps). Populate
`INITIATIVE_REGISTRY.manifests_processes` for ~47 existing initiatives.
Re-emit compliance mirrors.

## Operator gates

G-60-A through G-60-D (one per program tranche per
`.cursor/rules/akos-governance-remediation.mdc` "Canonical CSV gates").

## Effort

~1 operator sitting per tranche x 4 tranches. Heavily operator-paced.

## Prerequisites

- I59 P10 closed (all 5 governance dimensions validated + SOPs ratified).
- Operator availability for tranche reviews.

## Input

- `docs/wip/planning/59-hlk-governance-clean-slate/reports/p8-process-list-harmonisation-proposal-2026-05-06.md`
- `SOP-INITIATIVE_PROCESS_HARMONISATION_001.md` (at `status: active` after
  G-59-D ratification in I59 P9)

## Closure

Flip `SOP-INITIATIVE_PROCESS_HARMONISATION_001.md` §4 from "proposed" to
"minted". Close I60 in `INITIATIVE_REGISTRY.csv`.

## Source

Created by I59 P8 (D-IH-59-L scope decision).
