---
report_kind: ops_closure_evidence
ops_action_id: OPS-86-15
initiative: INIT-OPENCLAW_AKOS-86
authored: 2026-06-05
control_confidence_level: Safe
linked_decisions:
  - D-IH-86-CR
  - D-IH-93-CLOSURE
  - D-GTM-DB-6
---

# OPS-86-15 mechanical closure — Supabase mirror migration sprint (six dimension CSVs)

## Summary

**OPS-86-15** (the Supabase mirror migration sprint for six dimension CSVs that lacked
`compliance.*_mirror` tables) is **closed** as of 2026-06-05.

Five registries were completed under **I93 P6** (DDL + batched DML via the governed
mirror apply path). **CHANNEL_TOUCHPOINT_REGISTRY** — the sixth CSV — had DDL since
Initiative 31; this closure tranche verified **emit → apply → parity** only.

## Evidence matrix

| Registry | Mirror table | CSV rows | Remote rows (2026-06-05) | Path |
|:---|:---|---:|---:|:---|
| AIC_REGISTRY | `compliance.aic_registry_mirror` | 5 | 5 | I93 P6 batches |
| AUDIENCE_REGISTRY | `compliance.audience_registry_mirror` | 9 | 9 | I93 P6 batches |
| CAPABILITY_CONFIDENCE_REGISTRY | `compliance.capability_confidence_registry_mirror` | 1119 | 1119 | I93 P6 batches |
| CAPABILITY_REGISTRY | `compliance.capability_registry_mirror` | 1119 | 1119 | I93 P6 batches |
| CHANNEL_TOUCHPOINT_REGISTRY | `compliance.channel_touchpoint_registry_mirror` | 11 | 11 | This tranche |
| COUNTRY_WORK_CALENDAR | (quartet via OPS-86-18) | — | — | Sibling OPS row |

## CHANNEL apply (this tranche)

1. **Emit:** `py scripts/sync_compliance_mirrors_from_csv.py --channel-touchpoint-registry-only --output artifacts/sql/channel_touchpoint_mirror_upsert.sql`
2. **Apply:** `npm run supabase -- db query --linked -f artifacts/sql/channel_touchpoint_mirror_upsert.sql`
3. **Verify:** `npm run supabase -- db query --linked "SELECT COUNT(*) AS n FROM compliance.channel_touchpoint_registry_mirror;"` → **11**

Governed operator path: [`docs/guides/holistika-mirror-dml-apply.md`](../../../../guides/holistika-mirror-dml-apply.md) +
vault SOP `SOP-HOLISTIKA_COMPLIANCE_MIRROR_DML_001` (**D-GTM-DB-6**).

## Register flip

`OPS_REGISTER.csv` row **OPS-86-15** → `status: closed`, `closed_at: 2026-06-05`.

**OPS-86-23** backlog note updated: DIM-04 six-CSV mirror sprint item cleared via OPS-86-15;
remaining mirror-sync hygiene lives in sibling OPS rows (OPS-86-16/17/18 closed; OPS-86-32..34
mirror row-sync where applicable).

## Explicit non-goals

- Full-fleet `compliance_mirror_emit` re-sync (not required for this closure)
- DIM-10 regression-sweep heuristic fix (retained as follow-up in original OPS-86-15 notes)

## Cross-references

- I93 closure UAT: [`docs/wip/planning/93-data-area-foundation-and-governance/reports/uat-i93-closure-2026-06-05.md`](../../93-data-area-foundation-and-governance/reports/uat-i93-closure-2026-06-05.md)
- I88 P1 entry research: [`docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/research-p1-entry-gate-2026-06-05/master-synthesis.md`](../../88-cross-area-ops-wiring-review-discipline/reports/research-p1-entry-gate-2026-06-05/master-synthesis.md)
