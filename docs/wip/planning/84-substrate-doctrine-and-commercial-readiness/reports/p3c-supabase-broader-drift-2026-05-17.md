---
report_id: i84-p3c-supabase-broader-drift-2026-05-17
authored: 2026-05-17
author: System Owner (with agent assistance) via I84 P3c Option H1 contract
phase: P3c-post-supabase-application
classification: blocker_note
access_level: 5
language: en
linked_decisions: [D-IH-84-A]
linked_initiatives: [INIT-OPENCLAW_AKOS-14, INIT-OPENCLAW_AKOS-16, INIT-OPENCLAW_AKOS-18, INIT-OPENCLAW_AKOS-19, INIT-OPENCLAW_AKOS-21, INIT-OPENCLAW_AKOS-23, INIT-OPENCLAW_AKOS-24, INIT-OPENCLAW_AKOS-25, INIT-OPENCLAW_AKOS-31, INIT-OPENCLAW_AKOS-32, INIT-OPENCLAW_AKOS-45, INIT-OPENCLAW_AKOS-46, INIT-OPENCLAW_AKOS-47, INIT-OPENCLAW_AKOS-48, INIT-OPENCLAW_AKOS-49, INIT-OPENCLAW_AKOS-51, INIT-OPENCLAW_AKOS-59, INIT-OPENCLAW_AKOS-62, INIT-OPENCLAW_AKOS-64, INIT-OPENCLAW_AKOS-65, INIT-OPENCLAW_AKOS-66, INIT-OPENCLAW_AKOS-70, INIT-OPENCLAW_AKOS-71, INIT-OPENCLAW_AKOS-72, INIT-OPENCLAW_AKOS-73, INIT-OPENCLAW_AKOS-79]
---

# I84 P3c — Supabase broader drift blocker note (2026-05-17)

> **Purpose.** Per I84 P3c Option H1 contract (operator-selected at the Supabase drift recovery gate): file a focused blocker note documenting the broader Supabase migration drift state surfaced during I84 mirror application + recommend phased reconciliation sequence for separate operator-coordination session. The I84-scoped path (selective MCP apply of `20260517000000_i84_substrate_registry_mirror.sql`) completed cleanly; this note covers the **out-of-I84-scope** drift that the operator chose to defer.

## 1. Drift state snapshot (2026-05-17)

`npx supabase migration list` against the **MasterData** project (`swrmqpelgoblaquequzb`) reveals:

### 1.1 Pending local migrations (30 files; not yet on remote)

Spanning ~12 prior initiatives (I59 governance dimensions, I62 ERP RBAC + schema views + demo schema, I64 governance change log, I65 planning workspace + decision register mirror, I66 brand template + intelligence views, P13.4 GOI/POI related_party, I70 engagement registry + baseline sub_area_status + GOI/POI stance enum, I71 review-stamp + followup expansion, I72 engagement template + process_list value-mapping + intelligenceops + revops_spine FK + adapter registries, I73 engagement model mirror + engagement registry FK column, I79 design pattern registry mirror + process_list inherited_pattern_id column):

| Timestamp | Filename | Initiative |
|:---|:---|:---|
| 20260506120000 | i59_repository_registry_mirror.sql | I59 |
| 20260506120100 | i59_initiative_registry_mirror.sql | I59 |
| 20260506120200 | i59_ops_register_mirror.sql | I59 |
| 20260506120300 | i59_cycle_register_mirror.sql | I59 |
| 20260506120400 | i59_decision_register_mirror.sql | I59 |
| 20260506130000 | i62_p1_holistika_ops_rbac.sql | I62 |
| 20260506130100 | i62_p2_erp_schema_views.sql | I62 |
| 20260506130200 | i62_p3_demo_schema.sql | I62 |
| 20260508000000 | i62_p2_erp_schema_views_v2.sql | I62 |
| 20260508010000 | i65_p1_decision_register_mirror.sql | I65 |
| 20260508010100 | i65_p1_governance_planning_workspace.sql | I65 |
| 20260508020000 | i64_p1_governance_canonical_change_log.sql | I64 |
| 20260509213000 | i66_p6_brand_template_and_intelligence_views.sql | I66 |
| 20260511020000 | p13_4_goipoi_related_party.sql | P13.4 (I20-ish; doctrine drift) |
| 20260511030000 | release_gate_hygiene_baseline_rates.sql | Release gate hygiene |
| 20260513120000 | i70_engagement_registry_mirror.sql | I70 |
| 20260513140000 | i70_p82_baseline_sub_area_status.sql | I70 |
| 20260513150000 | i70_p85_goipoi_stance_and_class_enum_extension.sql | I70 |
| 20260514193709 | i71_p4_review_stamp.sql | I71 |
| 20260514202912 | i71_p4_followup_review_stamp_expansion.sql | I71 |
| 20260514220000 | i72_engagement_template_registry_mirror.sql | I72 |
| 20260514230000 | i72_process_list_value_mapping_columns.sql | I72 |
| 20260514240000 | i72_intelligenceops_register_mirror.sql | I72 |
| 20260514250000 | i72_revops_spine_finops_fk_columns.sql | I72 |
| 20260514260000 | i72_adapter_registries_mirrors.sql | I72 |
| 20260515180000 | i73_compliance_engagement_model_mirror.sql | I73 |
| 20260515180001 | i73_engagement_registry_add_engagement_model_id.sql | I73 |
| 20260516000000 | i79_compliance_design_pattern_registry_mirror.sql | I79 |
| 20260516010000 | i79_process_list_inherited_pattern_id_column.sql | I79 |

(I84 migration `20260517000000_i84_substrate_registry_mirror.sql` is **APPLIED** per the I84-scoped path; not part of this drift list.)

### 1.2 Remote-only migrations (12; on remote but not in local git)

These were applied to remote at some point (likely via dashboard or MCP apply_migration emergency paths) without a matching local migration file:

| Remote timestamp |
|:---|
| 20260507010953 |
| 20260507011236 |
| 20260508000209 |
| 20260508000224 |
| 20260508001128 |
| 20260508001539 |
| 20260508003238 |
| 20260508003307 |
| 20260508011055 |
| 20260508011309 |
| 20260514174346 |
| 20260514183314 |

The CLI's diagnostic recommendation per `npx supabase db push --dry-run --include-all`:

```
supabase migration repair --status reverted 20260507010953 20260507011236 20260508000209 20260508000224 20260508001128 20260508001539 20260508003238 20260508003307 20260508011055 20260508011309 20260514174346 20260514183314
supabase db pull
```

## 2. Why blind `supabase db push` is not safe

Per [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Operator SQL gate" Step 4 ("Pre-push"): *"`supabase migration list`: local and remote **must match** (no drift); then `supabase db push`"*. The precondition is violated.

Blind `supabase db push --include-all` would:
1. Push all 30 pending local migrations as a single atomic batch (`db push` operates as a transaction over the set).
2. Touch DDL across 12 initiatives that have not had operator-side approval for application (some may have been deferred intentionally; some may carry unresolved issues; some may break against current production state due to dependency drift since they were authored).
3. Carry HIGH BLAST RADIUS to production-grade infrastructure used by `kirbe.*` + `holistika_ops.*` + `compliance.*` + `finops.*` schemas across all live operator surfaces.

## 3. Recommended phased reconciliation sequence

For a dedicated operator-coordination session (separate from I84):

### Phase A — Remote-only reconciliation (~30 min)

Per the CLI's recommendation:

1. `npx supabase migration repair --status reverted <12 timestamps>` to clear the remote-only entries from local's view.
2. `npx supabase db pull` to download remote schema state into new local migration files. This generates new `supabase/migrations/<timestamp>_remote_schema.sql` files reflecting the divergent state.
3. Review the pulled migrations; categorize by which initiative they originally belonged to; rename for clarity if appropriate (per `akos-holistika-operations.mdc` migration-naming convention `<timestamp>_<purpose>.sql`).
4. Commit the pulled files to git so they're version-controlled going forward.

### Phase B — Per-initiative review of pending locals (~2–4 hours; depends on operator-context-of-record availability)

For each of the 30 pending local migrations (grouped by initiative per the table in §1.1), per-initiative-owner reviews:

1. Does this migration's intent still match current operator decisions (decision-log / DECISION_REGISTER.csv)?
2. Has anything else changed since authoring that this DDL depends on?
3. Should the migration be applied as-is, modified, or superseded?
4. If superseded: file a successor migration with the correct DDL; mark the old one for removal.

This is genuine per-initiative-owner work — multiple operators across initiatives may need to weigh in (CTO/Tech Lead for I62/I71/I72 stack; Compliance Officer for I59/I65/I79 governance; KM Officer for I70 doctrine drift; etc).

### Phase C — Tranched application (~30 min per tranche)

Group reviewed-and-approved migrations into ~5–7 tranches by:
- Initiative coherence (apply all I59 governance dimensions together; all I72 RevOps adapters together; etc).
- Dependency order (mirrors before FK additions; tables before views).
- Operator gating discipline (apply mirrors that touch canonical CSV data only after CSV is in current state).

For each tranche:
1. `npx supabase db push --include-all` (after each tranche the parity should improve; eventually `db push` becomes safe).
2. Verify via `supabase migration list` parity check + spot-check via `execute_sql` on mirror tables.
3. Record application in a per-tranche pause-record under appropriate initiative's `reports/` folder.

### Phase D — Final parity verification (~15 min)

1. `npx supabase migration list` — confirm local and remote match completely.
2. Run `py scripts/sync_compliance_mirrors_from_csv.py --count-only` and apply any rows-out-of-sync via `--<initiative>-only` flags.
3. Update `supabase/migrations/README.md` parity map with final state.
4. Close the broader drift via a focused chore commit + close-out note.

## 4. Effort estimate

| Phase | Effort | Calendar |
|:---|:---|:---|
| Phase A | ~30 min | Same session |
| Phase B | 2-4 hours | Same session OR distributed across initiative owners |
| Phase C | 3-5 hours (depending on tranche count) | Same session |
| Phase D | ~15 min | Same session |
| **Total** | **~6-10 engineer-hours** | **1-2 calendar days** |

Could be done in a focused operator session OR distributed work-block.

## 5. I84-scoped status (separate from this drift)

The I84 P3c mirror application path completed cleanly via the operator-approved Option H1 (selective MCP apply):

- `compliance.substrate_registry_mirror` table exists on remote MasterData project (`swrmqpelgoblaquequzb`).
- 18 substrate rows seeded via MCP execute_sql batches.
- Migration ledger harmonized to canonical file timestamp `20260517000000`.
- 28/28 substrate tests passing.
- All I84 validators green.

I84 is **complete from the canonical mint chain perspective**. The broader drift documented in this note is **out-of-I84-scope** infrastructure debt that warrants its own focused operator-coordination session.

## 6. Cross-references

- I84 master-roadmap: [`../master-roadmap.md`](../master-roadmap.md)
- I84 self-checkpoint (with §2.3 Supabase application trail): [`checkpoints/sc-i84-p1p2-complete-2026-05-17.md`](checkpoints/sc-i84-p1p2-complete-2026-05-17.md)
- AKOS Holistika operations rule: [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Operator SQL gate" + §"Two-plane model"
- AKOS Governance Remediation rule: [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"HLK compliance governance"
- AKOS Inline-Ratification rule: [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) §"When NOT to use" — STOP-AND-CLARIFY for blockers; this note is that documentation.
- Supabase migrations README: [`supabase/migrations/README.md`](../../../../supabase/migrations/README.md) — parity map (will need update at Phase D)

## 7. Provenance

Filed at I84 P3c post-Supabase-application per operator H1 selection contract. Not a P0/master-roadmap deliverable; out-of-scope-of-I84 deferred work for a separate operator-coordination session. Classified `access_level: 5` per Tier-1 WIP convention; not promoted to canonical (no canonical promotion path; this is operator-coordination evidence).
