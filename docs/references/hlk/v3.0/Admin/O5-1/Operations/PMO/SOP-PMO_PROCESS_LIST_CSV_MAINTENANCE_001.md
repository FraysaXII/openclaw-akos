---
Item Name: PMO process_list.csv maintenance and column contract
Item Number: SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001
Object Class: Guideline and Procedure
Confidence Level: Safe
Security Level: 2 (Internal Use)
Entity Owner: Think Big
Area Owner: Operations
Associated Workstream: Think Big Operational Excellence
Version: 1.0
Revision Date: 2026-04-15
---

## Purpose

Define how operators and integrators **maintain** the canonical process registry **`docs/references/hlk/compliance/process_list.csv`** after initial promotion from Trello or WIP (see **SOP-PMO_VAULT_PROMOTION_GATE_001**). Covers **column schema**, **parent identifiers**, **unique display names**, **forks and older checkouts**, and **recovery from duplicate `item_name` collisions**.

## Canonical authority

- **SSOT:** `process_list.csv` per [PRECEDENCE.md](../../../../compliance/PRECEDENCE.md).
- **Schema authority in code:** `PROCESS_LIST_FIELDNAMES` in `akos/hlk_process_csv.py` (column order, header names). Do not fork a parallel column list in application code.

## Column contract (current baseline)

The file is UTF-8 CSV with a **single header row**. The authoritative column list is **`PROCESS_LIST_FIELDNAMES`** (today **21** columns), including:

- `item_parent_2`, `item_parent_2_id`, `item_parent_1`, `item_parent_1_id`, `item_name`, `item_id`, …

**Never hard-code a column count** (for example 19) in scripts or notebooks: always read the CSV header, or import `PROCESS_LIST_FIELDNAMES` from this repository.

## Forks and older checkouts (mitigation)

| Risk | Mitigation |
|------|------------|
| A branch predates `item_parent_*_id` columns | **Merge or rebase onto current `main`** before editing `process_list.csv`. |
| Header row does not match `PROCESS_LIST_FIELDNAMES` | Run **`py scripts/check_process_list_header.py`** after merge; fix header/columns before running writers or **`backfill_process_parent_ids`**. |
| Local script assumes legacy width | Replace fixed `FIELDNAMES` lists with `akos.hlk_process_csv` helpers (`normalize_process_row`, `write_process_csv`, `resolve_all_parent_ids`). |

## Invariants (must hold before merge)

1. **`item_name` uniqueness:** each non-empty `item_name` maps to **at most one** `item_id`. Enforced by **`py scripts/validate_hlk.py`** (check **Unique item_name**).
2. **Parent pointers:** for non-**project** rows, if `item_parent_1` / `item_parent_2` is set, the matching **`item_parent_1_id`** / **`item_parent_2_id`** must be set and must reference the parent row’s `item_id` whose `item_name` matches. **Project** rows leave both parent-id columns empty.
3. **Graph:** every `item_parent_1` / `item_parent_2` name must exist as some row’s `item_name` (where used); non-project rows are not orphans.

## Operator tooling (repo scripts)

| Script | Role |
|--------|------|
| `scripts/validate_hlk.py` | **Mandatory gate** before commit; runs parse, graph, uniqueness, parent-id consistency. |
| `scripts/check_process_list_header.py` | Header equals `PROCESS_LIST_FIELDNAMES` (fork drift). |
| `scripts/backfill_process_parent_ids.py` | Recompute `item_parent_*_id` from names; fails if duplicate `item_name` remains. |
| `scripts/dedupe_ambiguous_process_item_names.py` | **`--report`**: list duplicate groups. **`--suggest`**: print starter `RENAMES_BY_ITEM_ID` lines (machine keeper rule). **`--write`**: apply the hand-curated map in that script + `resolve_all_parent_ids`. |
| `scripts/merge_gtm_into_process_list.py` | GTM candidate merge (operator-approved tranche). |
| `scripts/refine_gtm_process_hierarchy.py` | Pattern 2 clusters / GTM rewiring. |
| `scripts/migrate_process_list_program_layer.py` | Pattern 3 `hlk_prog_*` program layer. |
| `scripts/ingest-trello.py` | Trello → candidate CSV (not canonical until merged). |

## Routine edit workflow

1. Edit **`process_list.csv`** (prefer UTF-8–safe editor; avoid Excel unless you preserve encoding and all columns).
2. **`py scripts/validate_hlk.py`** until **PASS**.
3. If you only changed parent **names**, run **`py scripts/backfill_process_parent_ids.py --write`** then **`validate_hlk`** again.
4. If you **renamed** an `item_name` that others use as `item_parent_1` / `item_parent_2`, update those parent strings (or re-run the appropriate merge/refine script).
5. Restart or reload services that cache the registry if applicable (see USER_GUIDE §24.4).

## Duplicate `item_name` response (new collision shapes)

When **`validate_hlk`** or **`backfill_process_parent_ids`** reports duplicate display names:

1. **`py scripts/dedupe_ambiguous_process_item_names.py --report`** — lists each `item_name` and conflicting `item_id` set.
2. **`py scripts/dedupe_ambiguous_process_item_names.py --suggest`** — prints a **starter** Python dict of `item_id` → proposed `item_name` using the **keeper** rule (highest `item_granularity` rank, then smallest `item_id`). **Review and replace** mechanical suffixes with operator-meaningful names (entity, program, vault path) before committing.
3. Merge reviewed lines into **`RENAMES_BY_ITEM_ID`** inside **`scripts/dedupe_ambiguous_process_item_names.py`** (curated map is intentional; auto-write without review is not allowed for production semantics).
4. **`py scripts/dedupe_ambiguous_process_item_names.py --write`** — applies map and re-resolves parent ids.
5. **`py scripts/validate_hlk.py`** again.

**Why not only `--suggest`?** Trello/GTM collisions often need **human** disambiguation (e.g. which “Engage” is Think Big vs Holistika). The suggest output is scaffolding, not the final operator decision.

## Spreadsheet and merge hazards

- **Excel:** can alter long text, dates, and encoding; prefer a text editor or CSV-aware tool.
- **Git merge conflicts** on this file: resolve carefully; re-run **`validate_hlk.py`**; watch for duplicated lines or duplicated `item_id`.

## Related documents

- **Promotion into canonical CSV:** [SOP-PMO_VAULT_PROMOTION_GATE_001.md](SOP-PMO_VAULT_PROMOTION_GATE_001.md)
- **Operator guide:** `docs/USER_GUIDE.md` §24.3–24.4 (HLK operator model)
- **Architecture / API:** `docs/ARCHITECTURE.md` (HLK registry, operator script table)
- **Semantic review example:** `docs/wip/planning/02-hlk-on-akos-madeira/reports/process-list-parent-id-semantic-review-20260415.md`
