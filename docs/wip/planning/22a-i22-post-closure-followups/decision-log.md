---
language: en
status: active
initiative: 22a-i22-post-closure-followups
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder + System Owner
last_review: 2026-05-04
---

# Initiative 22a — Decision log

## D-IH-OPS-1 — Full-parity Supabase reconciliation approved

**Decision (2026-05-04):** Run the full-parity Supabase reconciliation against the **MasterData** project (`swrmqpelgoblaquequzb`):

1. Apply the two LOCAL-ONLY migrations (I49 + I51).
2. Reconcile the `20260418165339` content divergence by **renaming the I14-phase-3 git file to `20260503190000_…`** (post-current-tail) and **reverse-importing the kirbe.monitoring_logs_retention body** into a new git file at the original `20260418165339` timestamp. Both are idempotent.
3. Re-emit the compliance mirror DML (`py scripts/verify.py compliance_mirror_emit`) and apply per-table batches via MCP `execute_sql` to bring all drifted mirrors (especially `persona_scenario_registry_mirror`, currently 0 rows vs canonical ~329) back in sync. Skip GOI/POI which is already in sync.

**Rationale:** Per [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) the operator SQL gate requires explicit operator approval before mutating remote schema. The operator selected this path in Plan-mode AskQuestion (questions `i14_165339_strategy=rename_and_reapply`, `persona_scenario_mirror_sync=sync_all_drifted_mirrors`) on 2026-05-04 after reviewing the parity matrix in [`reports/sql-proposal-supabase-parity-20260504.md`](reports/sql-proposal-supabase-parity-20260504.md). End state is **full parity** — no orphan ledger rows, no orphan schema state, no drifted mirrors. The reverse-import path makes git the SSOT for the kirbe-retention body that previously lived only on the remote ledger; the rename path closes the I14-phase-3 ledger gap with an idempotent reapply.

**Reversibility:**

- `db push` is forward-only; rollback is an explicit `--down` migration pair (none authored for this cycle; not requested).
- File rename: `git revert` restores the previous filename; the new ledger row at `20260503190000` would remain unless explicitly removed (low cost, documentation only).
- Mirror DML: re-run `compliance_mirror_emit` from any prior canonical-CSV git sha and re-apply; or row-level DELETE + re-UPSERT. Both fully reversible.

**Safety stop conditions:**

- Any new ERROR-level advisor on `compliance` / `finops` / `holistika_ops` after the apply STOPS phase H pending operator triage.
- Any unexpected schema state mismatch in `list_tables(verbose=true)` STOPS phase H.

**Cross-references:**

- [SQL proposal](reports/sql-proposal-supabase-parity-20260504.md)
- [supabase/migrations/README.md](../../../../supabase/migrations/README.md)
- [docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md)
- akos-planning-traceability rule § Decision log: [.cursor/rules/akos-planning-traceability.mdc](../../../../.cursor/rules/akos-planning-traceability.mdc)

---

## D-IH-OPS-2 — Rename I14-phase-3 migration to a clean tail timestamp

**Decision (2026-05-04):** Rename `supabase/migrations/20260418165339_i14_phase3_compliance_and_holistika_ops.sql` → `supabase/migrations/20260503190000_i14_phase3_compliance_and_holistika_ops.sql`. Header comment expanded with the reconciliation note pointing back to the proposal report.

**Rationale:** The original timestamp `20260418165339` is occupied on the remote ledger by an unrelated `kirbe.monitoring_logs_retention` body that was applied via Dashboard. The I14 phase 3 DDL is on the database (tables exist with rows) but is not in the ledger. `supabase migration repair --status applied 20260418165339` cannot mark the I14-phase-3 body as applied at that version because the version slot is taken. The cleanest, lowest-risk reconciliation is to rename to a clean post-current-tail timestamp and rely on the body's idempotency (every statement uses `IF NOT EXISTS` / `DROP POLICY IF EXISTS` / `GRANT`) so the reapply produces zero schema delta and the ledger gains the missing row.

**Reversibility:** High — `git revert` restores the previous filename. The ledger row at `20260503190000` would persist unless explicitly deleted by an operator; that is documentation-only impact.

**Cross-reference:** [supabase/migrations/20260503190000_i14_phase3_compliance_and_holistika_ops.sql](../../../../supabase/migrations/20260503190000_i14_phase3_compliance_and_holistika_ops.sql) header comment.

---

## D-IH-OPS-3 — Reverse-import kirbe.monitoring_logs_retention to git

**Decision (2026-05-04):** Reverse-import the body of `supabase_migrations.schema_migrations[20260418165339].statements` from the remote ledger into a new git file `supabase/migrations/20260418165339_kirbe_monitoring_logs_retention.sql`. The body creates an index on `kirbe.monitoring_logs(created_at desc)` and a `kirbe.cleanup_monitoring_logs(retention_days, batch_limit)` security-definer function with `revoke from public; grant execute to service_role`. Idempotent (`CREATE INDEX IF NOT EXISTS` / `CREATE OR REPLACE FUNCTION`).

**Rationale:** Once D-IH-OPS-2 frees up the I14-phase-3 body from this timestamp, the timestamp is still live on the remote ledger but has no git counterpart. Per [`supabase/migrations/README.md`](../../../../supabase/migrations/README.md) and the operator SQL gate, git is the SSOT for forward DDL. Reverse-importing the body closes that gap without re-executing anything: `supabase db push` will skip the version because remote already has it. Future operators reviewing this folder see the body that produced the live function on remote.

**Reversibility:** High — deleting the file is reversible by re-pulling from the remote ledger via the same MCP `execute_sql(SELECT statements FROM supabase_migrations.schema_migrations WHERE version='20260418165339')` query.

**Cross-reference:** [supabase/migrations/20260418165339_kirbe_monitoring_logs_retention.sql](../../../../supabase/migrations/20260418165339_kirbe_monitoring_logs_retention.sql).
