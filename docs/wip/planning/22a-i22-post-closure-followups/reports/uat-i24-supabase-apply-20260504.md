---
language: en
status: active
initiative: 22a-i22-post-closure-followups
report_kind: uat
program_id: shared
plane: ops
authority: Founder + System Owner
last_review: 2026-05-04
---

# UAT — Initiative 22a / Initiative 24 — Supabase MasterData parity reconciliation

**Date:** 2026-05-04
**Operator:** Founder (Holistika), via `npx supabase db push` + `supabase db query --linked` (CLI canonical) + `user-supabase` MCP (read-only verification)
**Project:** `MasterData` (`swrmqpelgoblaquequzb`, region `eu-central-1`, postgres 15.8.1.111, ACTIVE_HEALTHY)
**Decision authority:** [`D-IH-OPS-1`](../decision-log.md#d-ih-ops-1--full-parity-supabase-reconciliation-approved), [`D-IH-OPS-2`](../decision-log.md#d-ih-ops-2--rename-i14-phase-3-migration-to-a-clean-tail-timestamp), [`D-IH-OPS-3`](../decision-log.md#d-ih-ops-3--reverse-import-kirbemonitoring_logs_retention-to-git)
**Source git sha at apply:** captured in [`artifacts/sql/db-push-20260504.log`](../../../../artifacts/sql/db-push-20260504.log).

This report records the live-apply step that closed the long-deferred Supabase parity gap accumulated since the I14-phase-3 dashboard apply. Pattern follows [`p7-supabase-apply-evidence.md`](../../22-hlk-scalability-and-i21-closures/reports/p7-supabase-apply-evidence.md).

## Three-lights summary

| Stream | Light | Note |
|:-------|:-----:|:-----|
| Migration ledger parity | GREEN | 28 entries; all 4 reconciled rows present (I49, I51, I14-phase-3 reapply, kirbe-retention reverse-import). |
| Schema state (compliance / finops / holistika_ops) | GREEN | I49 priority columns + I51 `target_difficulty_band` confirmed via `list_tables(verbose=true)`. |
| Mirror DML drift | GREEN | All 16 compliance mirrors back to canonical row counts (`persona_scenario_registry_mirror` 0 → 329; `process_list_mirror` deltas closed; rest idempotent re-emit). |
| Advisor regression | GREEN | No new ERROR-level findings on `compliance` / `finops` / `holistika_ops` schemas vs pre-flight baseline. |
| HLK CSV validators | GREEN | `py scripts/validate_hlk.py` PASS post-apply. |

## Pre-flight discovery (read-only)

Tools: `list_projects`, `list_migrations`, `list_tables`, `get_advisors`, ad-hoc `execute_sql` row counts.

| Finding | Pre-apply state |
|:--------|:----------------|
| Migration ledger entries | 25 on remote (24 EXACT + 1 unrelated `kirbe.monitoring_logs_retention` at `20260418165339`); 27 on git (24 EXACT + I49 + I51 + I14-phase-3 occupying the contested timestamp). |
| LOCAL-ONLY git migrations | I49 (`20260503120000_i49_persona_scenario_registry_priority_columns.sql`), I51 (`20260503180000_i51_persona_scenario_target_difficulty_band.sql`). |
| Content divergence | `20260418165339` slot held different bodies on git (I14-phase-3) vs remote (kirbe.monitoring_logs_retention). |
| `compliance.goipoi_register_mirror` | 6/6 rows in sync; all I24 voice columns (`voice_register`, `language_preference`, `pronoun_register`) present and populated. **No DML re-emit needed.** |
| `compliance.persona_scenario_registry_mirror` | **0 rows** (mirror DML never ran since the I47 + I49 + I51 columns landed). Canonical CSV: 329 rows. |
| `process_list_mirror`, `topic_registry_mirror`, `policy_register_mirror` | A few rows behind canonical (sync_compliance_mirrors_from_csv had not been re-run since recent CSV churn). |
| Advisors (security + performance) | 0 ERROR on `compliance` / `finops` / `holistika_ops`. 46 pre-existing ERRORs on `kirbe` / `public` (out-of-scope; pre-existing, untouched). |

Operator decisions taken via Plan-mode AskQuestion (logged D-IH-OPS-1):

- `i14_165339_strategy = rename_and_reapply`
- `persona_scenario_mirror_sync = sync_all_drifted_mirrors`

Full pre-flight matrix: [`reports/sql-proposal-supabase-parity-20260504.md`](sql-proposal-supabase-parity-20260504.md).

## Apply step 1 — DDL via `npx supabase db push` (canonical CLI path)

Reconciliation edits to git **before** the push:

- **Rename** `supabase/migrations/20260418165339_i14_phase3_compliance_and_holistika_ops.sql` → `supabase/migrations/20260503190000_i14_phase3_compliance_and_holistika_ops.sql` (D-IH-OPS-2). Header comment expanded with reconciliation note.
- **Reverse-import** the remote `kirbe.monitoring_logs_retention` body to a new git file `supabase/migrations/20260418165339_kirbe_monitoring_logs_retention.sql` (D-IH-OPS-3). Body: `CREATE INDEX IF NOT EXISTS idx_monitoring_logs_created_at` + `CREATE OR REPLACE FUNCTION kirbe.cleanup_monitoring_logs(retention_days, batch_limit)` (security-definer, `revoke from public; grant execute to service_role`). All statements idempotent.
- Updated [`supabase/migrations/README.md`](../../../../supabase/migrations/README.md) parity map + reconciliation log.

`npx supabase db push` execution captured to [`artifacts/sql/db-push-20260504.log`](../../../../artifacts/sql/db-push-20260504.log).

| Local file | Remote action | Outcome |
|:-----------|:--------------|:--------|
| `20260503120000_i49_persona_scenario_registry_priority_columns.sql` | New migration applied | Ledger row created; columns `priority_score`, `safety_lane`, `release_blocking` added to `compliance.persona_scenario_registry_mirror`. |
| `20260503180000_i51_persona_scenario_target_difficulty_band.sql` | New migration applied | Ledger row created; column `target_difficulty_band` added. |
| `20260503190000_i14_phase3_compliance_and_holistika_ops.sql` | Reapply (idempotent) | Ledger row created at clean tail timestamp; zero schema delta (every statement uses `IF NOT EXISTS` / `DROP POLICY IF EXISTS` / `GRANT`). |
| `20260418165339_kirbe_monitoring_logs_retention.sql` | Skipped (already in remote ledger at this version) | Git is now SSOT for the body; `db push` correctly skipped. |

Total: **3 ledger rows gained**; 1 reverse-import file ratified.

## Apply step 2 — Compliance mirror DML batches

`py scripts/verify.py compliance_mirror_emit` regenerated `artifacts/sql/compliance_mirror_upsert.sql` (~2.85 MB, 16 mirrors).

Driver: `scripts/split_compliance_mirror_upsert.py` chunked the monolith into 85 transaction-bounded batches (each ≤ 25 statements wrapped in `BEGIN; ... COMMIT;`) under `artifacts/sql/mirror-batches/20260504/` (gitignored, regeneratable).

Apply driver: `scripts/apply_mirror_batches.ps1` ran each batch through `npx supabase db query --linked --file <chunk>`. Per-chunk apply log: [`artifacts/sql/mirror-batches-apply-20260504.log`](../../../../artifacts/sql/mirror-batches-apply-20260504.log).

| Mirror | Chunks applied | Post-apply rows | Canonical CSV rows | Match |
|:-------|:--------------:|:---------------:|:------------------:|:-----:|
| `process_list_mirror` | 51 | 1100 | 1100 | OK |
| `baseline_organisation_mirror` | 3 | 65 | 65 | OK |
| `finops_counterparty_register_mirror` | 1 | 2 | 2 | OK |
| `adviser_engagement_disciplines_mirror` | 1 | 6 | 6 | OK |
| `adviser_open_questions_mirror` | 1 | 12 | 12 | OK |
| `founder_filed_instruments_mirror` | 1 | 1 | 1 | OK |
| `program_registry_mirror` | 1 | 12 | 12 | OK |
| `topic_registry_mirror` | 2 | 28 | 28 | OK |
| `persona_registry_mirror` | 1 | 16 | 16 | OK |
| `persona_scenario_registry_mirror` | 16 | **329** (was 0) | 329 | OK |
| `channel_touchpoint_registry_mirror` | 1 | 10 | 10 | OK |
| `sourcing_register_mirror` | 1 (manually patched, see below) | 1 | 1 | OK |
| `skill_registry_mirror` | 1 (manually patched, see below) | 5 | 5 | OK |
| `touchpoint_kit_cell_mirror` | 1 | 15 | 15 | OK |
| `policy_register_mirror` | 2 | 33 | 33 | OK |
| `repo_health_snapshot_mirror` | 1 | 3 | 3 | OK |
| `goipoi_register_mirror` | (skipped — already in sync) | 6 | 6 | OK |

**Total: 17/17 mirrors back to canonical row count, including the long-deferred 329-row `persona_scenario_registry_mirror` catch-up.**

### Manual patches applied during the loop (upstream emit bugs)

Two chunks failed on first pass with deterministic, reproducible upstream bugs in `scripts/verify.py compliance_mirror_emit`. Each was patched in the local (gitignored) batch file and re-applied; the underlying defects are filed as I22a follow-ups (see [`master-roadmap.md`](../master-roadmap.md) "Open follow-ups").

| Chunk | Upstream bug | Local fix |
|:------|:-------------|:----------|
| `12-sourcing_register_mirror-chunk01.sql` | Empty CSV cell for `last_engagement_date` (DATE) emitted as `''` (Postgres rejects: `invalid input syntax for type date`). | Replaced `''` → `NULL` for the empty date cell. |
| `13-skill_registry_mirror-chunk01.sql` | Empty CSV cell for `tools_required_waived` (NOT NULL bool, no default) emitted as `NULL` (3 rows). | Replaced `, NULL, '',` → `, false, '',` for the affected position (3 occurrences). |

Both rows are idempotent on re-emit; the upstream emit fix will produce the same row state going forward (no row-level rework needed).

### Post-loop count probe

```sql
SELECT 'process_list_mirror' AS table_name, count(*)::text AS row_count FROM compliance.process_list_mirror
UNION ALL SELECT 'baseline_organisation_mirror',           count(*)::text FROM compliance.baseline_organisation_mirror
UNION ALL SELECT 'finops_counterparty_register_mirror',    count(*)::text FROM compliance.finops_counterparty_register_mirror
UNION ALL SELECT 'adviser_engagement_disciplines_mirror',  count(*)::text FROM compliance.adviser_engagement_disciplines_mirror
UNION ALL SELECT 'adviser_open_questions_mirror',          count(*)::text FROM compliance.adviser_open_questions_mirror
UNION ALL SELECT 'founder_filed_instruments_mirror',       count(*)::text FROM compliance.founder_filed_instruments_mirror
UNION ALL SELECT 'program_registry_mirror',                count(*)::text FROM compliance.program_registry_mirror
UNION ALL SELECT 'topic_registry_mirror',                  count(*)::text FROM compliance.topic_registry_mirror
UNION ALL SELECT 'persona_registry_mirror',                count(*)::text FROM compliance.persona_registry_mirror
UNION ALL SELECT 'persona_scenario_registry_mirror',       count(*)::text FROM compliance.persona_scenario_registry_mirror
UNION ALL SELECT 'channel_touchpoint_registry_mirror',     count(*)::text FROM compliance.channel_touchpoint_registry_mirror
UNION ALL SELECT 'sourcing_register_mirror',               count(*)::text FROM compliance.sourcing_register_mirror
UNION ALL SELECT 'skill_registry_mirror',                  count(*)::text FROM compliance.skill_registry_mirror
UNION ALL SELECT 'touchpoint_kit_cell_mirror',             count(*)::text FROM compliance.touchpoint_kit_cell_mirror
UNION ALL SELECT 'policy_register_mirror',                 count(*)::text FROM compliance.policy_register_mirror
UNION ALL SELECT 'repo_health_snapshot_mirror',            count(*)::text FROM compliance.repo_health_snapshot_mirror
UNION ALL SELECT 'goipoi_register_mirror',                 count(*)::text FROM compliance.goipoi_register_mirror
ORDER BY 1;
```

Probe executed 2026-05-04 18:42 UTC via MCP `execute_sql`. **Result: every row in the table above matches its canonical CSV row count exactly (17/17).** No drift remains.

## Advisor regression (post-apply)

`get_advisors --type security` and `--type performance` re-run after the full apply. **Diff vs pre-flight baseline:** zero new ERROR-level findings on `compliance`, `finops`, or `holistika_ops`. Pre-existing INFO-level lints (RLS-enabled tables in other schemas without policies, plus the 46 unrelated `kirbe`/`public` ERRORs) are unchanged and out-of-scope.

## RLS posture (unchanged)

All compliance mirrors retain deny-all RLS for `anon` + `authenticated`; only `service_role` GRANT is in place. The mirror DML batches were applied via `supabase db query --linked` which authenticates as the service-role-equivalent management context. No PII columns were exposed to a public role at any point.

## Rollback path

- **Migration ledger:** `db push` is forward-only. Rollback is an explicit `--down` migration pair (none authored for this cycle; not requested). For the rename, `git revert` restores the previous filename; the ledger row at `20260503190000` would persist unless explicitly removed (documentation-only impact).
- **Reverse-import:** Deleting the file is reversible — re-pull the remote body via MCP `execute_sql(SELECT statements FROM supabase_migrations.schema_migrations WHERE version='20260418165339')`.
- **Mirror DML:** Re-emit from any prior canonical-CSV git sha and re-apply (idempotent). Or row-level DELETE + re-UPSERT.

## Idempotency rehearsal

A single random chunk (`10-persona_scenario_registry_mirror-chunk08.sql`) was re-applied after the full loop — second apply observed zero new rows (all `INSERT ... ON CONFLICT DO UPDATE` paths) and only `synced_at` timestamps updated. Behavior matches the per-row contract.

## Cross-references

- [`reports/sql-proposal-supabase-parity-20260504.md`](sql-proposal-supabase-parity-20260504.md)
- [`decision-log.md`](../decision-log.md) — D-IH-OPS-1, D-IH-OPS-2, D-IH-OPS-3
- [`supabase/migrations/README.md`](../../../../supabase/migrations/README.md)
- [`docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md`](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md)
- [`docs/wip/planning/22-hlk-scalability-and-i21-closures/reports/p7-supabase-apply-evidence.md`](../../22-hlk-scalability-and-i21-closures/reports/p7-supabase-apply-evidence.md) (template predecessor)
- `scripts/apply_mirror_batches.ps1` (driver), `scripts/split_compliance_mirror_upsert.py` (chunker)

## Related initiative closures

- **Initiative 22a P1** (`supabase migration list` parity check) is now executed live (no longer "OPERATOR" deferred). See [`master-roadmap.md`](../master-roadmap.md) phase row update.
- **Initiative 24 P2** (`ALTER TABLE compliance.goipoi_register_mirror`) was already applied via migration `20260429172732_i24_compliance_goipoi_register_mirror_alter.sql`; this UAT confirms the mirror remains 6/6 in sync post-reconciliation.

## Operator next steps (recommended)

- When canonical CSVs change again, run `py scripts/verify.py compliance_mirror_emit` → `scripts/split_compliance_mirror_upsert.py` → `scripts/apply_mirror_batches.ps1`. The split + apply pair scales linearly and is now repeatable.
- For drift detection between cycles: `SELECT count(*) FROM compliance.<mirror>` and compare against `py scripts/sync_compliance_mirrors_from_csv.py --count-only`.
- The `artifacts/sql/mirror-batches/` directory is gitignored; treat it as a one-shot artifact per apply window.
