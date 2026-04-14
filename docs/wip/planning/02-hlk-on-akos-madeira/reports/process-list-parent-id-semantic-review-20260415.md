# Process list parent-id migration — semantic review (SR-2)

**Date:** 2026-04-15  
**Scope:** Phase 2 + Phase 3 — `item_parent_1_id` / `item_parent_2_id` columns, validator, registry, API, CSV writers, authoring policy.

## Issues found

1. **Duplicate `item_name` values** — Several display names appeared on more than one `item_id`, which blocked parent-id resolution for rows whose parent string matched that name.
2. **FastAPI route ordering** — A static path segment `id` must be registered before the generic `/hlk/processes/{item_id}` handler so `/hlk/processes/id/{item_id}/tree` is not shadowed.

## Fixes applied

- Centralized **`PROCESS_LIST_FIELDNAMES`**, **`resolve_all_parent_ids`**, and **`write_process_csv`** in `akos/hlk_process_csv.py`; merge, refine, migrate, ingest, and backfill scripts call them on write.
- **`check_parent_id_consistency`**: non-project rows with a uniquely resolvable parent name must carry the matching parent id; project rows must not set parent ids.
- **`HlkRegistry`**: `_processes_by_parent_1_id` index; **`get_process_tree`** prefers the id-keyed child list when the parent resolves; **`get_process_tree_by_parent_id`** for stable lookups.
- **API:** `GET /hlk/processes/id/{item_id}/tree` registered ahead of `/hlk/processes/{item_id}`.
- **PMO SOP** `SOP-PMO_VAULT_PROMOTION_GATE_001.md`: step 6 for operator authoring of parent ids and unique `item_name`.
- **Follow-up (2026-04-15):** **`scripts/dedupe_ambiguous_process_item_names.py --write`** renamed 23 canonical rows (by `item_id`) so **`ambiguous_item_names` is empty**; canonical CSV re-written with **`resolve_all_parent_ids`** so every non-project parent pointer has matching ids where names are set.
- **Hardening (same tranche):** **`item_name_uniqueness_errors`** in **`akos/hlk_process_csv.py`** plus **`validate_hlk`** check **Unique item_name**; **`scripts/backfill_process_parent_ids.py`** exits early with **`--report`** hint; **`scripts/dedupe_ambiguous_process_item_names.py --report`** for read-only collision listing; **`PRECEDENCE.md`** canonical table repaired (program subsection no longer split the asset table) and process row notes uniqueness.

## Verification commands run

- `py scripts/validate_hlk.py`
- `py scripts/dedupe_ambiguous_process_item_names.py --write`
- `py -m pytest tests/test_hlk.py -v`
- `py -m pytest tests/test_api.py -v` (HLK slice as part of suite when executed)

## Residual risks

- **Operator bypass:** Merges that skip **`py scripts/validate_hlk.py`** could still land duplicate `item_name` rows until CI/release-gate catches them; **`py scripts/dedupe_ambiguous_process_item_names.py --report`** is the fastest local pre-check.
- **Third-party CSV consumers** remain outside repo control; in-repo contract is **`PROCESS_LIST_FIELDNAMES`** (USER_GUIDE §24.3.4). KiRBe fingerprints hash the whole file so column drift is visible, not silent.
