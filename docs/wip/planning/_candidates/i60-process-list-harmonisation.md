---
language: en
status: superseded
superseded_by: I79 P6
superseded_date: 2026-05-15
superseded_decision: D-IH-79-K
initiative: I60 — Process_list harmonisation (mint)
---

> **SUPERSEDED — 2026-05-15.** This candidate is **substantively absorbed by Initiative 79 Phase 6** (`process_list.csv` 8th column for `inherited_pattern_id` Foreign Key into `PEOPLE_DESIGN_PATTERN_REGISTRY.csv` + the accompanying baseline tranche). Per **D-IH-79-K** (I79 P5 cluster C bookmark), do not reopen this candidate as a fresh initiative. The structural mechanism that I60 contemplated (process_list grooming + tranche-paced operator review) is now executed under I79 P6's process-singularity gate, and any residual program-tranche backlog folds into successor initiatives' standard CSV-tranche pause-point discipline.
>
> **Reference cross-link:** [`docs/wip/planning/79-people-manifesto-and-pattern-library/master-roadmap.md`](../79-people-manifesto-and-pattern-library/master-roadmap.md) §P6.

# I60 candidate — Process_list harmonisation (mint) [SUPERSEDED]

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
