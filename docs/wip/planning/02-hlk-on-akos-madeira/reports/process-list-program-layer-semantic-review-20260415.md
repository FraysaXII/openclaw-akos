# process_list program layer semantic review (2026-04-15)

## Scope

Pattern 3: insertion of **`hlk_prog_*`** program **workstream** rows under **MADEIRA Platform** and **Think Big Operational Excellence**, and re-parenting of nine GTM workstreams per [trello-list-to-workstream-matrix.md](trello-list-to-workstream-matrix.md). Driver: `scripts/migrate_process_list_program_layer.py --write`.

## Checks performed

| Gate | Result |
|------|--------|
| `py scripts/validate_hlk.py` | PASS |
| Parent names: every non-empty `item_parent_1` / `item_parent_2` resolves to an existing `item_name` in the CSV | PASS (validator) |
| Projects have ≥1 direct child via `item_parent_1` | PASS (program rows use `item_parent_1` = `item_parent_2` = project name) |
| **Engage** / **PMO vault promotion gate** (`gtm_pm_st_promo`) | Unchanged: `gtm_pm_st_promo` remains under **Engage** with `item_parent_2` = Think Big Operational Excellence |
| GTM **clusters** (`gtm_cl_*`) | Still reference workstream `item_name` in `item_parent_1` and project in `item_parent_2`; workstream names unchanged |

## Issues found and mitigations

1. **Flat MADEIRA GTM workstreams** — Mitigated: six MADEIRA workstreams now sit under two program workstreams; three Think Big GTM workstreams sit under one program workstream.
2. **Non-GTM MADEIRA children** (SSE streaming, Archivist, SOP rows) — **Operator decision (default):** left as **direct** children of **MADEIRA Platform**; documented in matrix and this report.
3. **Residual risk:** `get_project_summary` counts only **direct** children by name; MADEIRA Platform’s direct child list now includes program rows plus legacy rows—expected. Deeper navigation uses program then workstream.

## Verification commands

```text
py scripts/migrate_process_list_program_layer.py
py scripts/migrate_process_list_program_layer.py --write
py scripts/validate_hlk.py
py -m pytest tests/test_hlk.py -v
```
