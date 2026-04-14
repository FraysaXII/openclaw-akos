# Process list parent-id migration — semantic review (SR-2)

**Date:** 2026-04-15  
**Scope:** Phase 2 + Phase 3 — `item_parent_1_id` / `item_parent_2_id` columns, validator, registry, API, CSV writers, authoring policy.

## Issues found

1. **Duplicate `item_name` values** — Several display names appear on more than one `item_id`. Parent-id resolution intentionally leaves `item_parent_*_id` empty when the parent name is ambiguous; `scripts/validate_hlk.py` does not require ids in that case.
2. **FastAPI route ordering** — A static path segment `id` must be registered before the generic `/hlk/processes/{item_id}` handler so `/hlk/processes/id/{item_id}/tree` is not shadowed.

## Fixes applied

- Centralized **`PROCESS_LIST_FIELDNAMES`**, **`resolve_all_parent_ids`**, and **`write_process_csv`** in `akos/hlk_process_csv.py`; merge, refine, migrate, ingest, and backfill scripts call them on write.
- **`check_parent_id_consistency`**: non-project rows with a uniquely resolvable parent name must carry the matching parent id; project rows must not set parent ids.
- **`HlkRegistry`**: `_processes_by_parent_1_id` index; **`get_process_tree`** prefers the id-keyed child list when the parent resolves; **`get_process_tree_by_parent_id`** for stable lookups.
- **API:** `GET /hlk/processes/id/{item_id}/tree` registered ahead of `/hlk/processes/{item_id}`.
- **PMO SOP** `SOP-PMO_VAULT_PROMOTION_GATE_001.md`: step 6 for operator authoring of parent ids.

## Verification commands run

- `py scripts/validate_hlk.py`
- `py -m pytest tests/test_hlk.py -v`
- `py -m pytest tests/test_api.py -v` (HLK slice as part of suite when executed)

## Residual risks

- Rows whose parent is an **ambiguous `item_name`** remain without parent ids until duplicate names are disambiguated in the CSV.
- External tools that assume the legacy 19-column header must be updated to accept the two new columns.
