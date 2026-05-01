---
language: en
status: complete
initiative: 32-holistik-ops-maturation
report_kind: phase-report
phase: P3
program_id: shared
plane: ops
authority: PMO + System Owner
last_review: 2026-04-30
---

# P3 — Touchpoint-kit cell registry

**Date:** 2026-04-30
**Status:** COMPLETED. Topic registry now at 25. **15/15 P3 tests PASS** including both keystone planted-phantom regressions.

## Action items

| ID | Action | Status | Evidence |
|:---|:-------|:-------|:---------|
| **P3-A1** | Schema + akos contract | DONE | [`akos/hlk_touchpoint_kit_cell_csv.py`](../../../../akos/hlk_touchpoint_kit_cell_csv.py): 10-field tuple + ALLOWED_LANGUAGES + VALID_LIFECYCLE_STATUSES + VALID_DISTANCE_BANDS + TOUCHPOINT_KIT_ROOT constants. |
| **P3-A2** | Validator with FS-drift invariant | DONE | [`scripts/validate_touchpoint_kit_cells.py`](../../../../scripts/validate_touchpoint_kit_cells.py): full schema check + FK resolution against PERSONA_REGISTRY, CHANNEL_TOUCHPOINT_REGISTRY, TOPIC_REGISTRY + **FS-vs-CSV drift detector** scanning `<TKIT_ROOT>/<persona>/<channel>/intro_message_<lang>.md`. Reports both `missing_in_csv` and `phantom_in_csv` separately. |
| **P3-A3** | Mirror DDL | DONE (staged) | [`supabase/migrations/20260430233200_i32_touchpoint_kit_cell_mirror.sql`](../../../../supabase/migrations/20260430233200_i32_touchpoint_kit_cell_mirror.sql): same governance pattern; 5 indexes (synced_at, persona, channel, language, lifecycle); RLS deny anon + authenticated; service_role only. |
| **P3-A4** | 15 seed rows mirroring filesystem | DONE | [`TOUCHPOINT_KIT_CELL_REGISTRY.csv`](../../../references/hlk/compliance/dimensions/TOUCHPOINT_KIT_CELL_REGISTRY.csv): 15 rows. 8 distinct (persona × channel) combinations (the I31 P4 cell count). Each row mirrors one MD file; `distance_variants_in_file` derived from each file's frontmatter `distance_variants_covered`. |
| **P3-A5** | topic_touchpoint_kit_cell_registry row | DONE | Topic registry now at **25 rows**. |
| **P3-A6** | FS-drift planted-phantom test | DONE | Two keystone tests in [`tests/test_touchpoint_kit_cell_registry.py`](../../../../tests/test_touchpoint_kit_cell_registry.py): `test_planted_phantom_csv_row_is_caught` (CSV row → no file) AND `test_planted_missing_csv_row_is_caught` (file → no CSV row). Both use a tmp_path swap pattern that restores the canonical CSV in a `finally` block. |

## Verification

- `py scripts/validate_touchpoint_kit_cells.py` → PASS at 15 rows; CSV cells = 15; FS cells = 15
- `py scripts/validate_topic_registry.py` → PASS at 25 rows
- `py scripts/validate_hlk.py` → PASS; new line: "TOUCHPOINT_KIT_CELL_REGISTRY: PASS"
- `py -m pytest tests/test_touchpoint_kit_cell_registry.py -v` → **15 passed in 3.61s**

## Notes

- **The 15-row vs 8-cells reconciliation**: I31 P4 framed the kit as 8 cells (one per persona × channel). I32 P3 turns each cell into one CSV row per language variant. 8 × (1 to 2 languages each) = 15 rows. The `(persona_id, channel_id)` group-by yields the original 8.
- **FS-drift detector is the architectural value-add**. Today it caught zero drift (CSV is fresh). Future regressions where someone adds an MD file without a CSV row OR removes an MD file without removing the CSV row will trip immediately under `validate_hlk.py`.
- The 2 keystone planted-phantom tests use the `shutil.copy(...) → finally: shutil.copy(backup, real)` pattern to ensure the CSV is restored even on test failure. They take ~1.6s combined (subprocess invocation cost) and run on every CI sweep.
- `topic_ids` already populated for every row (preview of axis 6 propagation; P5 makes this column FK-required across all dimension CSVs).
- Cells for KiRBe-prospect carry both `topic_holistik_ops_discovery` AND `topic_kirbe_billing_plane_routing` — first cross-axis topic-multi-binding example.

## Next phase

P4 — Policy register (RLS + service_role rotation + redaction policies as one CSV).
