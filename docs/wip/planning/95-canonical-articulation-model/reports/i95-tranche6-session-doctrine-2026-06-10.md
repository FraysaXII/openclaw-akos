---
authored: 2026-06-10
tranche: I95-T6
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: OPS-95-2
gate_type: inline-ratify
---

# I95 Tranche 6 session doctrine (OPS-95-2)

Binding rule/skill card for this execution session. Refer back at each major action.

| When I touch… | Load… | One-line when |
|:---|:---|:---|
| Canonical CSV gate | [`akos-baseline-governance.mdc`](../../../../.cursor/rules/akos-baseline-governance.mdc) | Operator approval **before** `ENGAGEMENT_REGISTRY.csv` edit |
| Mirror re-apply | [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) | Two-plane: CSV SSOT → emit → operator `apply_mirror_batches.ps1` |
| Inline ratify | [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) + [`inline-ratify-craft`](../../../../.cursor/skills/inline-ratify-craft/SKILL.md) | Evidence sweep **before** AskQuestion; no CSV apply without answer |
| Engagement instances SSOT | [`ENGAGEMENT_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) + [`.md` spec](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.md) | 17 cols; col 17 = `engagement_model_id` FK |
| Engagement model taxonomy | [`ENGAGEMENT_MODEL_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv) | 7-class + 3 schema-extension rows (`eng_model_*` only in mirror FK) |
| Template pairing (RevOps) | [`ENGAGEMENT_TEMPLATE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/ENGAGEMENT_TEMPLATE_REGISTRY.csv) | `tmpl_*` ≠ `eng_model_*`; prior conflation caused prod FK fail |
| OPS tracker | [`OPS_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) row **OPS-95-2** | Close on ratified backfill + mirror parity |
| Cluster burndown rank 4 | [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md) | Exit: operator-approved backfill + `validate_hlk.py` PASS |
| Planning traceability | [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) | `files-modified.csv` on touch |

## Tranche 6 action checklist

1. P0 research mint (`i95-p0-research-ops95-2-engagement-backfill-2026-06-10.md`) — **before** edits
2. Evidence packet + `i95-ops95-2-proposals.csv` — per-row `eng_model_*` options with citations
3. **Inline-ratify gate (AskQuestion)** — structural fork + per-row model class OR confirm intentional NULL
4. **If ratified:** edit `ENGAGEMENT_REGISTRY.csv` → `py scripts/validate_hlk.py` → mirror re-emit notes
5. Update cluster map rank 4, PMO sweep OPS-95-2 row, `files-modified.csv`
6. Commit **only if CSV applied:** `fix(i95): OPS-95-2 engagement_model_id backfill`

## Gates honored

- No `process_list.csv` / `baseline_organisation.csv` edits
- No Supabase DDL migrations (FK column already exists; NOT VALID until backfill)
- **No CSV apply without operator ratification** — evidence-only delivery acceptable this session
- **Next tranche (do not start):** PMO initiative sweep to reorganize
