---
Item Name: PMO vault promotion gate (Trello and WIP to process_list)
Item Number: SOP-PMO_VAULT_PROMOTION_GATE_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Think Big
Area Owner: Operations
Associated Workstream: Think Big Operational Excellence
Version: 1.0
Revision Date: 2026-04-14
---

## Purpose

Define how PMO moves **stable operating intent** from **Trello**, **board JSON imports**, and **`docs/wip/`** into the canonical registry **`docs/references/hlk/compliance/process_list.csv`** without mixing backlog columns or scratch notes into compliance SSOT.

## Preconditions

- Card or theme has a **clear `role_owner`** from `baseline_organisation.csv`.
- Scope is **repeatable** (not a one-off scratch item).
- **English** `item_name` and parent workstream exist or are drafted in the harmonization matrix (`docs/wip/planning/02-hlk-on-akos-madeira/reports/trello-list-to-workstream-matrix.md`).

## Steps

1. Keep execution in **Trello** or **WIP** until the item passes preconditions.
2. For **bulk task promotion** (more than a handful of cards in one tranche), define or reuse English **cluster** `process` rows (`gtm_cl_*`) so each promoted leaf has **`item_parent_1`** = cluster `item_name` and **`item_parent_2`** = workstream `item_name` (see `docs/wip/planning/02-hlk-on-akos-madeira/reports/trello-list-to-workstream-matrix.md` Pattern 2). Then draft CSV row(s): `item_id`, `item_granularity`, harmonized parents, metadata (`description`, `confidence`, `frequency`, `quality`).
3. Map Trello **`list.name`** to a registered English **workstream** `item_name`; never use `To Do`, `Done`, or `Viejo` as parents.
4. Obtain **operator approval** on the tranche (see planning `canonical-csv-tranche-operator-approval-template.md`).
5. Merge into `process_list.csv` and run **`py scripts/validate_hlk.py`** until PASS; sync ARCHITECTURE / USER_GUIDE counts when project or item totals change. After large GTM merges, run **`py scripts/refine_gtm_process_hierarchy.py --write`** when clustering or `item_name` cleanup rules change.
6. Whenever **`item_parent_1`** or **`item_parent_2`** is set on a non-project row, ensure the corresponding **`item_parent_1_id`** / **`item_parent_2_id`** columns are populated with the parent row’s canonical **`item_id`** after merge tools run (use **`py scripts/backfill_process_parent_ids.py --write`** when bulk-upgrading, or rely on writers that call **`akos.hlk_process_csv.resolve_all_parent_ids`**). Omit parent IDs only when the parent **`item_name`** is intentionally ambiguous (duplicate display names in the same file—registry debt tracked in validator output). Project rows must leave both parent-id columns empty.

## Out of scope

- Editing `Research & Logic` historical trees.
- Treating **KiRBe** or **Drive** as authoring surfaces for `process_list` rows (canonical CSV first per PRECEDENCE).

## Registry cross-reference

Optional anchor process row: **PMO vault promotion gate** (`gtm_pm_st_promo`) under **Think Big Operational Excellence** — points agents to this SOP via `hlk_process`.
