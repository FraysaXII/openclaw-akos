---
authored: 2026-06-10
tranche: I95-T5
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L1-EG-3
---

# I95 Tranche 5 session doctrine (L1 EG-3)

Binding rule/skill card for this execution session. Refer back at each major action.

| When I touch… | Load… | One-line when |
|:---|:---|:---|
| EG-3 scope | [`SUPABASE_ECOSYSTEM_GOVERNANCE.md`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/SUPABASE_ECOSYSTEM_GOVERNANCE.md) §3 EG-3 | Edge/cron/extension registries close SUPA-MOD-11/14/15/19 |
| EG-2 precedent | [`SUPABASE_API_EXPOSURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/SUPABASE_API_EXPOSURE.md) | Markdown + CSV SSOT + module-registry promotion pattern |
| Module inventory | [`SUPABASE_MODULE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_MODULE_REGISTRY.csv) | Promote rows after registry mint |
| P0 evidence before edits | [`akos-applied-research-discipline.mdc`](../../../../.cursor/rules/akos-applied-research-discipline.mdc) | Internal sweep mandatory; external optional (refinement) |
| Operator gate (CSV fork) | [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) | Only if net-new governed rows need approval |
| Holistika DDL | [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) | **Out of scope** — no migrations this tranche |
| Cluster burndown rank 3b | [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md) | Exit: EG-3 registries minted + validators PASS |
| Planning traceability | [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) | `files-modified.csv` + cluster map on touch |

## Tranche 5 action checklist

1. P0 research mint (`i95-p0-research-l1-eg3-registries-2026-06-10.md`) — **before** edits
2. Mint `SUPABASE_EDGE_FUNCTION_REGISTRY.csv` (3 live functions)
3. Mint `SUPABASE_CRON_REGISTRY.csv` (2 cron jobs from I81 migrations)
4. Mint `SUPABASE_EXTENSION_MANIFEST.md` (pg_cron / pg_net / pgmq / wrappers / vector posture)
5. Pydantic + validators; wire `validate_hlk.py`
6. Update `SUPABASE_MODULE_REGISTRY.csv` + `SUPABASE_ECOSYSTEM_GOVERNANCE.md` + `PRECEDENCE.md`
7. Cluster map rank 3b → DONE; `files-modified.csv`; CHANGELOG
8. Validators: `validate_hlk.py`, `verify.py pre_commit_fast`
9. Single commit: `docs(i95): tranche-5 L1 EG-3 Supabase registries`

## Gates honored

- No `process_list.csv` / `baseline_organisation.csv` edits
- No Supabase DDL migrations
- Document existing live surface only — no over-mint
- **Next tranche (do not start):** OPS-95-2 → PMO sweep
