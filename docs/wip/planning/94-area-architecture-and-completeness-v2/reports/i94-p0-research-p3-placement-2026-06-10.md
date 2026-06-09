---
authored: 2026-06-10
tranche: I94-P3-placement
parent_initiative: INIT-OPENCLAW_AKOS-94
upstream_ssot: i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md
---

# I94 P3 placement — mini P0 research note (2026-06-10)

Bounded internal evidence sweep before P3 file moves and baseline edits.

## Questions

1. Where do `SOP-IO_*` files already live vs process_list references?
2. What fixes AREA-16 Engagement orphan without roster bloat?
3. What is safe deferral for `business-strategy` under PMO?

## Findings

| # | Finding | Disposition |
|:---:|:---|:---|
| F1 | Two `SOP-IO_*` still under `Operations/IntelligenceOps/`; two already under `Research/Intelligence/canonicals/` | `git mv` the two misplaced files; update process_list rows 396, 404–407 |
| F2 | AREA-16 scorer matches subfolder names to `baseline_organisation.sub_area` or `role_name` | Set PMO `sub_area=Engagement` (charter §2 co-ownership PMO+RevOps) |
| F3 | `PMO/canonicals/business-strategy/` is I95 L6 placement debt | Forward-charter tracker only; no mass moves in P3 |
| F4 | `process_list` lacked `sop_path`/`runbook_path` | Extend `PROCESS_LIST_FIELDNAMES`; 12 Operations pairings |

## Precedent

- D-IH-70-W — IntelligenceOps SOP migration target = Research/Intelligence
- I93/I88 — sub_area column used for RevOps/SMO folder FK
- I94 charter P3 — operator gate cleared for CSV + file moves (AskQuestion Both)

## Verification target

`validate_area_completeness.py --area Operations --matrix` — AREA-09 ≥12/46; AREA-16 orphans reduced.
