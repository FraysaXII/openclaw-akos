# GTM process_list semantic review (2026-04-14)

## Scope

Post–Pattern 2 pass on `docs/references/hlk/compliance/process_list.csv`: cluster layer (`gtm_cl_*`), parent rewiring, and `item_name` sanitization for `gtm_*` rows. Driver: `scripts/refine_gtm_process_hierarchy.py --write`.

## Checks performed

| Gate | Result |
|------|--------|
| Parent chain: every `gtm_*` non-project row has `item_parent_1` and `item_parent_2` in the global `item_name` set | Pass (scripted policy check) |
| `py scripts/validate_hlk.py` | Pass |
| Orphans / broken `item_parent_1` refs | Pass (validator) |
| Cluster rows: `item_granularity` = `process`, `item_parent_1` = workstream, `item_parent_2` = project | Pass by construction |

## Issues found and mitigations

1. **Empty `item_parent_2` on GTM workstreams and leaves** — Fixed: workstreams use duplicate project pattern (`item_parent_1` = `item_parent_2` = project); leaves use cluster + workstream; PMO anchor uses `Think Big Operational Excellence` as `item_parent_2` under `Engage`.
2. **Code-like DevOps / LlamaIndex `item_name` values** — Mitigated: 110 rows renamed to English prose; original symbols prepended to `description` where replaced.
3. **Pipeline vs playlist research branch** — Preserved: six pipeline tasks remain under `Research material pipeline execution`; playlist processes share one cluster keyed on Trello `Research Material` path.
4. **Spanish Trello path segments** — Cluster **English** titles use a small gloss map for common first segments; full Spanish path remains in `addundum_extras` / cluster description for traceability. Residual risk: long or rare Spanish fragments may still appear abbreviated in the auto title; operators can adjust titles in a future tranche if needed.

## Residual risks

- **Semantic mis-bucket from source data:** One candidate row (`gtm_madeira_dtp_224`, “Benchmarker - AI Ethics” process) still resolves under **MADEIRA product planning** workstream because the historical Trello path was `MADEIRA Project`-only; correcting the owning workstream would be a separate data fix, not a hierarchy-engine change.
- **Cluster title collisions** — Disambiguated with numeric suffix when an English title collides with an existing `item_name` (rare).

## Verification commands

```text
py scripts/validate_hlk.py
py -m pytest tests/test_hlk.py -v
```
