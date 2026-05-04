---
language: en
status: active
initiative: 22a-i22-post-closure-followups
report_kind: sql-proposal
program_id: shared
plane: ops
authority: Founder + System Owner
last_review: 2026-05-04
related_ops: OPS-22a-1
project_ref: swrmqpelgoblaquequzb
project_name: MasterData
---

# SQL proposal — full Supabase parity reconciliation (MasterData)

Per [`docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md`](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md) the operator gate flow is **discover → read → propose → operator approval → execute → verify**. This report is the **propose** step; operator approval is recorded in the new [`decision-log.md`](../decision-log.md) under **D-IH-OPS-1**.

## Scope

- **Project:** `swrmqpelgoblaquequzb` (MasterData), eu-central-1, postgres 15.8.1.111, ACTIVE_HEALTHY.
- **Operator-chosen scope:** `full_parity` — apply pending DDL, reconcile content divergence at `20260418165339`, re-emit drifted compliance mirror DML across all 16 mirror tables.
- **Out of scope:** `bfsdsrqktampahhkxzoe` (hlk-shopify-cart-drawer) — separate project; not touched.

## Discovery summary (read-only MCP probes, this turn)

### Migration ledger parity (git ↔ remote)

| Status | Count | Detail |
|---|---|---|
| EXACT match | 24 / 27 | i16 / i18 / i19 / i21x4 / i23 / i24 / i25 / i31 / i32x5 / i45x2 / i46 / i47x2 / i48 |
| LOCAL-ONLY (apply on `db push`) | 2 | `20260503120000_i49_persona_scenario_registry_priority_columns.sql`, `20260503180000_i51_persona_scenario_target_difficulty_band.sql` |
| CONTENT DIVERGENCE | 1 | `20260418165339` — see below |
| NAME-SUFFIX-ONLY drift | 2 | `20260418183239`, `20260418193915` (cosmetic; bodies match) |

#### `20260418165339` divergence

- **Git body** ([`supabase/migrations/20260418165339_i14_phase3_compliance_and_holistika_ops.sql`](../../../../supabase/migrations/20260418165339_i14_phase3_compliance_and_holistika_ops.sql)): I14 phase 3 scaffold — creates `compliance` + `holistika_ops` schemas, `process_list_mirror`, `baseline_organisation_mirror`, `stripe_customer_link`, `billing_account`; RLS + deny-policies + grants. Idempotent (`IF NOT EXISTS` / `DROP POLICY IF EXISTS` / `GRANT`).
- **Remote ledger body** at the same timestamp: `kirbe.monitoring_logs_retention` — index on `kirbe.monitoring_logs(created_at desc)` plus `kirbe.cleanup_monitoring_logs(retention_days, batch_limit)` security-definer function. Idempotent (`CREATE INDEX IF NOT EXISTS` / `CREATE OR REPLACE FUNCTION`).
- **Schema state on remote:** all four I14 phase 3 tables EXIST with rows (`process_list_mirror=1093`, `baseline_organisation_mirror=65`, `stripe_customer_link=0`, `billing_account=0`). The kirbe retention function also exists. Conclusion: **both bodies were applied to the database, but only one (the kirbe one) is recorded in `supabase_migrations.schema_migrations` at version `20260418165339`**. The I14 phase 3 DDL was applied via Dashboard / break-glass without going through `supabase db push`.

### Mirror DML state vs canonical CSVs

| Mirror table | Remote rows | Status |
|:---|---:|:---|
| `compliance.goipoi_register_mirror` | 6 | ✓ in sync (all 6 voice + distance columns populated and match GOI_POI_REGISTER.csv exactly) |
| `compliance.persona_scenario_registry_mirror` | 0 | **catch-up needed**: canonical CSV has ~329 rows; mirror has never been populated |
| `compliance.process_list_mirror` | 1093 | possible drift; canonical may be ~1100 (verify via `validate_hlk.py` before H6) |
| `compliance.topic_registry_mirror` | 23 | possible drift; canonical may be ~28 |
| `compliance.policy_register_mirror` | 25 | possible drift; canonical includes I55 `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` (ensure synced) |
| All other 12 mirrors | match | ✓ |

### Advisor baseline

| Type | ERROR | WARN | INFO | On schemas we touch (compliance / finops / holistika_ops) |
|:---|---:|---:|---:|:---|
| Security | 46 | 146 | 19 | **0 ERRORs** (all 46 in `kirbe` or `public`; pre-existing; out of scope for this gate) |
| Performance | 0 | 79 | 138 | 73 INFO/WARN (`multiple_permissive_policies` / `unused_index`; cosmetic) |

## Reconciliation strategy (operator-chosen)

### Migrations

1. **`20260418165339`** — operator chose `rename_and_reapply` (per AskQuestion in Plan mode):
   - Rename git file → `supabase/migrations/20260503190000_i14_phase3_compliance_and_holistika_ops.sql` (post-current-tail timestamp). Body is fully idempotent → re-apply on `db push` does not change schema state, ledger gains the row.
   - Reverse-import the remote-only `kirbe.monitoring_logs_retention` body to a new git file `supabase/migrations/20260418165339_kirbe_monitoring_logs_retention.sql`. CLI will skip on `db push` because that version is already in the remote ledger; git becomes SSOT for the body going forward.
   - Update [`supabase/migrations/README.md`](../../../../supabase/migrations/README.md) reconciliation log.
2. **Local-only migrations** (apply on `db push`):
   - `20260503120000_i49_persona_scenario_registry_priority_columns.sql`
   - `20260503180000_i51_persona_scenario_target_difficulty_band.sql`
3. **`20260418183239` + `20260418193915`** — name-suffix-only drift; cosmetic; **no action**. CLI compares by version (timestamp), not name. The supabase/migrations/README.md "name-suffix" note can be added if desired but is not required.

Net: `db push` will materialize 3 new ledger rows (I49 + I51 + I14-phase-3-reapply at the new tail timestamp). The kirbe-retention reverse-import file just becomes documentation.

### Mirror DML

1. Run `py scripts/verify.py compliance_mirror_emit` → produces `artifacts/sql/compliance_mirror_upsert.sql` (gitignored).
2. Inspect per-table row count summary; show operator the diff (e.g. `persona_scenario_registry_mirror: 329 inserts, process_list_mirror: 7 deltas, …`).
3. Apply table-by-table in operator-reviewed batches via MCP `execute_sql`. One transaction per table to keep blast radius small. If a single table's batch is > ~50 KB, split further.
4. **GOI/POI: skip** (already verified in sync; emit is idempotent so running it changes nothing for that table; explicitly skip to avoid noise).
5. Verify post-counts: `SELECT 'persona_scenario_registry_mirror', COUNT(*) FROM compliance.persona_scenario_registry_mirror UNION ALL …` matches canonical.

### RLS posture (no change)

All `compliance.*_mirror` tables already have RLS enabled with `deny_anon` + `deny_authenticated` policies. Service-role access (used by sync jobs) bypasses RLS by Supabase platform default. Voice / distance / persona / topic / policy columns added by I24, I31, I47, I49, I51 inherit table-level RLS automatically; no per-column additions required.

### PII notes

- `compliance.goipoi_register_mirror` carries operator-managed entity / display-name / language / pronoun fields. RLS + deny-anon + deny-authenticated remains in force.
- `compliance.persona_scenario_registry_mirror` rows use `persona_id` slugs from `PERSONA_REGISTRY.csv`; no raw PII is stored in this mirror.
- `compliance.policy_register_mirror` carries POLICY_REGISTER rows; no PII.
- All other drifted mirrors: no new PII surface.

### Rollback path

- **`db push` is forward-only.** No native rollback step. Schema rollback (if ever required) is an explicit `--up`/`--down` migration pair authored separately.
- **Migration rename:** git revert restores the previous filename; it does not affect remote (the renamed migration body is idempotent and was already applied; the new ledger row at `20260503190000` would remain unless an explicit DELETE on `supabase_migrations.schema_migrations` is executed by an operator with privileges).
- **Mirror DML rollback:** re-run `compliance_mirror_emit` from the previous canonical CSV git sha and re-apply; alternative is row-level DELETE then re-UPSERT. Both are reversible by re-emitting from the canonical CSV.
- **Safety stop conditions:** any new ERROR-level advisor on `compliance` / `finops` / `holistika_ops` after `db push` STOPS phase H pending operator triage.

### Idempotency confirmation (line-by-line)

The renamed I14 phase 3 reapply body uses:

- `CREATE SCHEMA IF NOT EXISTS compliance` ✓
- `CREATE SCHEMA IF NOT EXISTS holistika_ops` ✓
- `CREATE TABLE IF NOT EXISTS compliance.process_list_mirror (…)` ✓
- `CREATE TABLE IF NOT EXISTS compliance.baseline_organisation_mirror (…)` ✓
- `CREATE TABLE IF NOT EXISTS holistika_ops.stripe_customer_link (…)` ✓
- `CREATE TABLE IF NOT EXISTS holistika_ops.billing_account (…)` ✓
- `CREATE INDEX IF NOT EXISTS …` (multiple) ✓
- `ALTER TABLE … ENABLE ROW LEVEL SECURITY` ✓ (idempotent)
- `DROP POLICY IF EXISTS … CREATE POLICY …` ✓ (drop-then-create pattern is idempotent)
- `GRANT USAGE ON SCHEMA …` ✓ (idempotent)
- `GRANT ALL ON ALL TABLES IN SCHEMA …` ✓ (idempotent)

Verdict: every statement is idempotent; reapply at the new timestamp produces zero schema deltas.

## Verification matrix

Pre-execution (already done in pre-flight, this turn):

- [x] MCP `list_projects` → confirm `swrmqpelgoblaquequzb` MasterData ACTIVE_HEALTHY
- [x] MCP `list_migrations` → 25 entries
- [x] MCP `list_tables(schemas=[compliance, holistika_ops, finops, kirbe, stripe_gtm])` → mirror state map
- [x] MCP `execute_sql(SELECT)` → column inventory on `compliance.goipoi_register_mirror`; row contents on the 6 GOI/POI rows
- [x] MCP `get_advisors(security)` + `get_advisors(performance)` → baseline counts captured

Post-execution (Phase H5 + H7):

- [ ] MCP `list_migrations` → 28 entries (24 + I49 + I51 + I14-phase-3-reapply)
- [ ] MCP `list_tables(verbose=true)` → I49 priority + I51 target_difficulty_band columns visible on `persona_scenario_registry_mirror`
- [ ] MCP `get_advisors` → diff vs baseline; STOP if any new ERROR on schemas we touched
- [ ] `py scripts/validate_hlk.py` → PASS
- [ ] Mirror row-count assertions match canonical CSV counts

## Operator approval

Operator approved the strategy in Plan mode (AskQuestion 2026-05-04):

- Question `i14_165339_strategy` → `rename_and_reapply` (with kirbe reverse-import).
- Question `persona_scenario_mirror_sync` → `sync_all_drifted_mirrors`.

Decision recorded as **D-IH-OPS-1** in [`decision-log.md`](../decision-log.md).

## Cross-references

- Operator SQL gate workflow: [docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md)
- Migrations folder canonical: [supabase/migrations/README.md](../../../../supabase/migrations/README.md)
- I22a master-roadmap: [master-roadmap.md](../master-roadmap.md)
- I24 master-roadmap: [docs/wip/planning/24-hlk-communication-methodology/master-roadmap.md](../../24-hlk-communication-methodology/master-roadmap.md)
- Akos-holistika-operations rule: [.cursor/rules/akos-holistika-operations.mdc](../../../../.cursor/rules/akos-holistika-operations.mdc)
