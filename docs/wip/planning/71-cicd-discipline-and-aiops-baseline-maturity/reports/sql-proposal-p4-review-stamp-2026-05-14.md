# I71 P4 — SQL proposal (Strand C2 review-stamp dimension column-extension)

> Authored 2026-05-14 BEFORE the Supabase migration applies. Per `.cursor/rules/akos-holistika-operations.mdc` §"Operator SQL gate": discover (read-only via MCP) → propose (DDL + rollback + RLS + PII notes in this doc) → execute → pre-push parity check. The operator's blanket trust signal pre-approves the execute step; this doc is the audit trail for the pre-approval. Sibling to `p4-design-2026-05-14.md` (the design ratification doc explaining the verdict) and the migration file `supabase/migrations/20260514193709_i71_p4_review_stamp.sql` (the executable DDL). Phase report `p4-strand-c2-review-stamp-2026-05-14.md` lands at commit time.

## 1. Discover (MCP read-only; 2026-05-14)

### 1.1 Project + schema state

- **Supabase project**: `MasterData` (id `swrmqpelgoblaquequzb`; org `cpibdpgaarsbfnamudya`; region `eu-central-1`; status `ACTIVE_HEALTHY`; postgres 15.8.1.111).
- **Schema in scope**: `compliance` (mirrored canonical CSVs from `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`).
- **Discovery method**: MCP `list_tables` with `schemas: ["compliance"]` + `verbose: false`.

### 1.2 Mirror table inventory (relevant rows from list_tables output 2026-05-14)

| Mirror table | Row count | RLS | Mirrored from canonical CSV | Initiative source |
|:---|:---:|:---:|:---|:---|
| `compliance.process_list_mirror` | 1100 | ✅ | `process_list.csv` (1145 rows; some rows skipped per business filters at sync time) | I14 phase 3 (`20260503190000_i14_phase3_compliance_and_holistika_ops.sql`) |
| `compliance.decision_register_mirror` | 51 | ✅ | `DECISION_REGISTER.csv` (133 rows; 51 sync'd by latest emit; gap is sync-cadence not schema) | I59 P1.5 + I65 P1.1 (`20260506120400_i59_decision_register_mirror.sql` + `20260508010000_i65_p1_decision_register_mirror.sql`) |
| `compliance.initiative_registry_mirror` | 51 | ✅ | `INITIATIVE_REGISTRY.csv` (58 rows; 51 sync'd by latest emit) | I59 P1.2 (`20260506120100_i59_initiative_registry_mirror.sql`) |
| `compliance.ops_register_mirror` | 22 | ✅ | `OPS_REGISTER.csv` (30 rows; 22 sync'd) | I59 P1.3 (`20260506120200_i59_ops_register_mirror.sql`) |

**Discovery verdict**: 4 of the 5 candidate canonicals (process_list / decision_register / initiative_registry / ops_register / canonical_registry) are mirrored as `compliance.*_mirror` tables. The 5th candidate `CANONICAL_REGISTRY.csv` is **NOT mirrored** — no `compliance.canonical_registry_mirror` exists. Per C-71-4 default, the 4 mirrored canonicals get column-extension at P4; the unmirrored Artifact class (CANONICAL_REGISTRY) gets deferred to a separate-table follow-up commit when the first standalone canonical needs a stamp.

### 1.3 Existing column drift state (compliance schema)

- Per `validate_compliance_schema_drift.py` registry: 22 canonical CSVs are tuple-aligned with their `akos.*` SSOT modules.
- The 4 mirrored canonicals in P4 scope are all on the registry (process_list / decision_register / initiative_registry / ops_register).
- Pre-P4 baseline: column-aligned per latest release-gate run.
- Post-P4 expectation: column-aligned with 4 new trailing review-stamp columns per CSV; tuple updates land same-commit.

## 2. Propose (DDL + rollback + RLS + PII)

### 2.1 Per-mirror DDL (forward migration)

Authored as a single transaction in `supabase/migrations/20260514193709_i71_p4_review_stamp.sql`. Verbatim DDL:

```sql
BEGIN;

-- 1. compliance.process_list_mirror — Process subject class
ALTER TABLE compliance.process_list_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 2. compliance.decision_register_mirror — Decision subject class
ALTER TABLE compliance.decision_register_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 3. compliance.initiative_registry_mirror — Registry-row subject class (governance trio: initiatives)
ALTER TABLE compliance.initiative_registry_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 4. compliance.ops_register_mirror — Registry-row subject class (governance trio: ops actions)
ALTER TABLE compliance.ops_register_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- Backfill posture: empty by default; operator backfills incrementally per
-- REVIEW_STAMP_INBOX.md workflow. Documented no-op self-update statement
-- below per the kickoff Step 3 template (NULL-stays-NULL; documents the
-- backfill point even though no source column carries pre-existing data).
UPDATE compliance.process_list_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;
UPDATE compliance.decision_register_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;
UPDATE compliance.initiative_registry_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;
UPDATE compliance.ops_register_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

COMMIT;
```

**Total DDL statements**: 16 ALTER TABLE ADD COLUMN (4 tables × 4 columns) + 4 documented no-op UPDATE statements + transaction begin/commit. All in one atomic transaction.

**Pattern source**: I70 P8.2 baseline `ADD COLUMN IF NOT EXISTS` (`20260513140000_i70_p82_baseline_sub_area_status.sql`). The pattern is additive-nullable + idempotent + minimal-blast-radius.

**`NOT VALID + VALIDATE CONSTRAINT` not invoked**: that pattern (per I70 P8.5 precedent at `20260513150000_i70_p85_goipoi_stance_and_class_enum_extension.sql`) applies to CHECK constraint additions where existing rows must validate after the constraint binds. P4 adds no CHECK constraints, so the simpler `ADD COLUMN IF NOT EXISTS` form covers the safety guarantee (never breaks existing rows; idempotent on re-apply).

### 2.2 Rollback DDL (reverse migration)

If the migration must be reversed, the operator runs the following SQL via `apply_migration` on the next free timestamp (e.g. `20260514193710_i71_p4_review_stamp_rollback.sql`):

```sql
BEGIN;

ALTER TABLE compliance.process_list_mirror
  DROP COLUMN IF EXISTS last_review_at,
  DROP COLUMN IF EXISTS last_review_by,
  DROP COLUMN IF EXISTS last_review_decision_id,
  DROP COLUMN IF EXISTS methodology_version_at_review;

ALTER TABLE compliance.decision_register_mirror
  DROP COLUMN IF EXISTS last_review_at,
  DROP COLUMN IF EXISTS last_review_by,
  DROP COLUMN IF EXISTS last_review_decision_id,
  DROP COLUMN IF EXISTS methodology_version_at_review;

ALTER TABLE compliance.initiative_registry_mirror
  DROP COLUMN IF EXISTS last_review_at,
  DROP COLUMN IF EXISTS last_review_by,
  DROP COLUMN IF EXISTS last_review_decision_id,
  DROP COLUMN IF EXISTS methodology_version_at_review;

ALTER TABLE compliance.ops_register_mirror
  DROP COLUMN IF EXISTS last_review_at,
  DROP COLUMN IF EXISTS last_review_by,
  DROP COLUMN IF EXISTS last_review_decision_id,
  DROP COLUMN IF EXISTS methodology_version_at_review;

COMMIT;
```

Then `git revert <P4-commit-sha>` to remove the CSV header columns + akos.* tuple entries + validator + tests + design/proposal/phase docs. The mirror tables return to their P3-state schema cleanly.

### 2.3 RLS posture (no policy changes)

All four mirror tables already carry `RLS = ON` with `service_role`-only access (deny `anon` / `authenticated`) per the I14 / I59 mirror inheritance. Postgres column-level RLS does not exist as a separate concept; RLS policies match rows via WHERE-clause predicates and apply to the entire row. Adding 4 nullable columns inherits the existing row-level posture with no policy edits required.

**Confirmation method (post-apply)**: `get_advisors` MCP with `type: security` returns no new advisories attributable to the migration. (Pre-existing advisories on these tables — if any — pre-date P4 and stay unchanged.)

### 2.4 PII analysis (none)

No GDPR / CCPA / sectoral-PII triggers from the new columns:

| Column | Type | PII? | Rationale |
|:---|:---|:---:|:---|
| `last_review_at` | DATE | No | Operational metadata (a date). |
| `last_review_by` | TEXT | No | Org-internal `role_name` string (e.g. `PMO`, `System Owner`); not a personal identifier even when a role resolves to a single individual (the SSOT is the org-internal `baseline_organisation.csv` taxonomy). |
| `last_review_decision_id` | TEXT | No | Governance-internal identifier (`D-IH-NN-X` pattern). |
| `methodology_version_at_review` | TEXT | No | Doctrine version string (`vMAJOR.MINOR`). |

Aligns with the existing mirror-column posture: none of the existing process_list / decision_register / initiative_registry / ops_register columns carry PII either.

## 3. Execute (operator blanket-trust pre-approval)

Per the operator's blanket trust signal: the agent applies the migration via Supabase MCP `apply_migration` with this proposal doc + the design doc + the migration file constituting the audit trail.

**Apply call** (post-stash, pre-edit):

```
apply_migration(
  project_id="swrmqpelgoblaquequzb",
  name="i71_p4_review_stamp",
  query=<contents of supabase/migrations/20260514193709_i71_p4_review_stamp.sql §2.1>
)
```

**Post-apply verification**:

1. `list_tables(project_id="swrmqpelgoblaquequzb", schemas=["compliance"], verbose=true)` — confirm all 4 mirror tables now carry the 4 new columns.
2. `list_migrations(project_id="swrmqpelgoblaquequzb")` — confirm the new migration row appears in the Supabase ledger.
3. `get_advisors(project_id="swrmqpelgoblaquequzb", type="security")` — confirm no new advisories attributable to the migration.
4. `get_advisors(project_id="swrmqpelgoblaquequzb", type="performance")` — confirm no new advisories attributable to the migration.

**On failure**:

1. STOP per opt-stop-report posture (`akos-governance-remediation.mdc`).
2. Author `docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p4-blocker-2026-05-14.md` capturing failure detail + rollback SQL.
3. Apply rollback SQL via `apply_migration` per §2.2.
4. Return to parent for re-coordination.

## 4. Pre-push parity check

Per `.cursor/rules/akos-holistika-operations.mdc` §"Operator SQL gate" step 4: `supabase migration list` (local + remote must match). Since the agent applies via MCP `apply_migration` (which is the break-glass path per §"Break-glass" of the rule), the post-apply verification via `list_migrations` MCP serves the same purpose: the new migration timestamp appears in the Supabase ledger; the local `supabase/migrations/20260514193709_i71_p4_review_stamp.sql` file matches the SQL the MCP applied. Parity holds by construction since the MCP applies the contents of the file we author + commit.

## 5. Cross-references

- Sibling design doc: [`p4-design-2026-05-14.md`](p4-design-2026-05-14.md) — the column-vs-table verdict + per-subject-class coverage + risk register + cross-references.
- Migration file: `supabase/migrations/20260514193709_i71_p4_review_stamp.sql` — the executable DDL.
- Phase report (post-execution): `p4-strand-c2-review-stamp-2026-05-14.md` — to be authored at commit time with the verification matrix outcomes.
- Cursor rule: [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Operator SQL gate" + §"Two-plane model" — the doctrine this proposal operationalises.
- Cursor rule: [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) — opt-stop-report posture for migration failures + canonical-CSV gate.
- Cursor rule: [`akos-docs-config-sync.mdc`](../../../../.cursor/rules/akos-docs-config-sync.mdc) — CSV header + akos.* tuple + mirror DDL same-commit sync contract.
- Decision authority: `D-IH-71-E` (P0; 4-column shape proposal) → `D-IH-71-Q` (P4 ratification minted at this commit).
- OPS closure: `OPS-71-3` closes with `closure_decision_id: D-IH-71-Q` + `closed_at: 2026-05-14`.

End of P4 SQL proposal doc.
