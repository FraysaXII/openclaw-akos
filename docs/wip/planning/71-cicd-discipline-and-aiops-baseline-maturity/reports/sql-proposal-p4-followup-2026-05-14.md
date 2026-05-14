# I71 P4 follow-up — SQL proposal (review-stamp expansion + Artifact standalone-table)

> Authored 2026-05-14 BEFORE the Supabase migration applies. Operator SQL Gate audit trail per `.cursor/rules/akos-holistika-operations.mdc` §"Operator SQL gate": discover (read-only via MCP) → propose (DDL + rollback + RLS + PII notes in this doc) → execute → pre-push parity check. The operator's blanket trust signal pre-approves the execute step; this doc is the audit trail. Sibling to [`p4-followup-design-2026-05-14.md`](p4-followup-design-2026-05-14.md) (verdict + per-mirror table + validator extension plan) and the migration file `supabase/migrations/<ts>_i71_p4_followup_review_stamp_expansion.sql`.

## 1. Discover (MCP read-only; 2026-05-14)

### 1.1 Project + schema state

- **Supabase project**: `MasterData` (id `swrmqpelgoblaquequzb`; org `cpibdpgaarsbfnamudya`; region `eu-central-1`; status `ACTIVE_HEALTHY`; postgres 15.8.1.111).
- **Schema in scope**: `compliance` (mirrored canonical CSVs from `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/`).
- **Discovery method**: MCP `list_tables` with `schemas: ["compliance"]` + `verbose: false`.

### 1.2 Mirror table inventory (relevant rows from list_tables 2026-05-14)

| Mirror | Rows | RLS | Already extended at P4? | Disposition at follow-up |
|--------|-----:|:---:|:-----------------------:|--------------------------|
| `compliance.process_list_mirror` | 1100 | ✅ | YES (P4) | Skip (already extended) |
| `compliance.decision_register_mirror` | 51 | ✅ | YES (P4) | Skip (already extended) |
| `compliance.initiative_registry_mirror` | 51 | ✅ | YES (P4) | Skip (already extended) |
| `compliance.ops_register_mirror` | 22 | ✅ | YES (P4) | Skip (already extended) |
| `compliance.baseline_organisation_mirror` | 65 | ✅ | NO | **EXTEND at this commit** |
| `compliance.finops_counterparty_register_mirror` | 2 | ✅ | NO | **EXTEND** |
| `compliance.goipoi_register_mirror` | 6 | ✅ | NO | **EXTEND** |
| `compliance.adviser_engagement_disciplines_mirror` | 6 | ✅ | NO | **EXTEND** |
| `compliance.adviser_open_questions_mirror` | 12 | ✅ | NO | **EXTEND** |
| `compliance.founder_filed_instruments_mirror` | 1 | ✅ | NO | **EXTEND** |
| `compliance.program_registry_mirror` | 12 | ✅ | NO | **EXTEND** |
| `compliance.topic_registry_mirror` | 28 | ✅ | NO | **EXTEND** |
| `compliance.persona_registry_mirror` | 16 | ✅ | NO | **EXTEND** |
| `compliance.persona_scenario_registry_mirror` | 329 | ✅ | NO | **EXTEND** |
| `compliance.channel_touchpoint_registry_mirror` | 10 | ✅ | NO | **EXTEND** |
| `compliance.sourcing_register_mirror` | 1 | ✅ | NO | **EXTEND** |
| `compliance.skill_registry_mirror` | 5 | ✅ | NO | **EXTEND** |
| `compliance.touchpoint_kit_cell_mirror` | 15 | ✅ | NO | **EXTEND** |
| `compliance.policy_register_mirror` | 33 | ✅ | NO | **EXTEND** |
| `compliance.repo_health_snapshot_mirror` | 6 | ✅ | NO | **EXTEND** |
| `compliance.repository_registry_mirror` | 6 | ✅ | NO | **EXTEND** |
| `compliance.access_level` (lookup) | 7 | ✅ | N/A | **Exclude** — taxonomy lookup; not a CSV mirror. |
| `compliance.confidence_level` (lookup) | 3 | ✅ | N/A | **Exclude** — same. |
| `compliance.source_category` (lookup) | 6 | ✅ | N/A | **Exclude** — same. |
| `compliance.source_level` (lookup) | 18 | ✅ | N/A | **Exclude** — same. |
| `compliance.validation_runs` (operational) | 0 | ✅ | N/A | **Exclude** — operational fact (NOT git SSOT). |
| `compliance.eval_run` (operational) | 0 | ✅ | N/A | **Exclude** — same. |
| `compliance.dossier_run` (operational) | 0 | ✅ | N/A | **Exclude** — same. |

**Discovery verdict**: 17 mirrors to extend at this follow-up. `compliance.canonical_registry_mirror` does NOT exist (CANONICAL_REGISTRY truly unmirrored), confirming the standalone-table path applies for the Artifact subject class.

### 1.3 Existing column drift state (compliance schema)

- `validate_compliance_schema_drift.py` registry: 22 canonical CSVs tuple-aligned with `akos.*` SSOT modules (current state).
- The 17 newly-extended canonicals are all on the registry.
- Pre-follow-up baseline: column-aligned per the latest release-gate run (P4 commit `bb04f08`).
- Post-follow-up expectation: column-aligned with 4 new trailing review-stamp columns per CSV; tuple updates land same-commit.

## 2. Propose (DDL + rollback + RLS + PII)

### 2.1 Per-mirror DDL (forward migration)

Authored as a single transaction in `supabase/migrations/<ts>_i71_p4_followup_review_stamp_expansion.sql`. The pattern repeats per the 17 mirror tables (verbatim DDL excerpt; full file in the migration):

```sql
BEGIN;

-- (1) baseline_organisation_mirror — Org-row subject class
ALTER TABLE compliance.baseline_organisation_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- (2 through 17) — same 4-column shape for the remaining 16 mirrors
-- ... see migration file for full enumeration ...

-- Standalone-table for the Artifact subject class (CANONICAL_REGISTRY canonicals)
CREATE TABLE IF NOT EXISTS compliance.review_stamps_standalone (
  id BIGSERIAL PRIMARY KEY,
  subject_kind TEXT NOT NULL CHECK (subject_kind IN ('canonical_md', 'standalone_csv', 'sop_md')),
  subject_path TEXT NOT NULL,
  subject_id TEXT,
  last_review_at DATE NOT NULL,
  last_review_by TEXT,
  last_review_decision_id TEXT,
  methodology_version_at_review TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (subject_kind, subject_path)
);

ALTER TABLE compliance.review_stamps_standalone ENABLE ROW LEVEL SECURITY;
CREATE POLICY review_stamps_standalone_service_role_all
  ON compliance.review_stamps_standalone
  FOR ALL TO service_role
  USING (true) WITH CHECK (true);

-- Backfill from CANONICAL_REGISTRY.csv last_review (subset where last_review is non-empty)
INSERT INTO compliance.review_stamps_standalone
    (subject_kind, subject_path, subject_id, last_review_at)
VALUES
    ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_VISION.md', 'brand_vision', '2026-05-12'),
    -- ... (additional rows for every CANONICAL_REGISTRY row with a non-empty last_review) ...
ON CONFLICT (subject_kind, subject_path) DO NOTHING;

COMMIT;
```

**Total DDL statements**: 17 ALTER TABLE × 4 ADD COLUMN = 68 ADD COLUMN + 1 CREATE TABLE + 1 ALTER TABLE ENABLE RLS + 1 CREATE POLICY + 17 documented no-op UPDATEs + 1 INSERT (multi-row) for backfill + transaction begin/commit. All in one atomic transaction.

**Pattern source**: I70 P8.2 baseline `ADD COLUMN IF NOT EXISTS` (`20260513140000_i70_p82_baseline_sub_area_status.sql`); I71 P4 (`20260514193709_i71_p4_review_stamp.sql`). Additive-nullable + idempotent + minimal-blast-radius.

**`NOT VALID + VALIDATE CONSTRAINT` not invoked**: pattern applies to CHECK constraint additions where existing rows must validate after constraint binds. The standalone-table CHECK on `subject_kind` is on a brand-new column in a brand-new table (no existing rows to validate against — backfill obeys the CHECK by construction).

### 2.2 Rollback DDL (reverse migration)

If the migration must be reversed, the operator runs the following SQL via `apply_migration` on the next free timestamp (e.g. `<ts+1>_i71_p4_followup_review_stamp_expansion_rollback.sql`):

```sql
BEGIN;

-- Drop the standalone table (cascades the RLS policy)
DROP TABLE IF EXISTS compliance.review_stamps_standalone CASCADE;

-- Drop the 4 review-stamp columns from each of the 17 newly-extended mirrors
ALTER TABLE compliance.baseline_organisation_mirror
  DROP COLUMN IF EXISTS last_review_at,
  DROP COLUMN IF EXISTS last_review_by,
  DROP COLUMN IF EXISTS last_review_decision_id,
  DROP COLUMN IF EXISTS methodology_version_at_review;

-- ... (repeat for the other 16 mirrors; full enumeration in the rollback file) ...

ALTER TABLE compliance.repository_registry_mirror
  DROP COLUMN IF EXISTS last_review_at,
  DROP COLUMN IF EXISTS last_review_by,
  DROP COLUMN IF EXISTS last_review_decision_id,
  DROP COLUMN IF EXISTS methodology_version_at_review;

COMMIT;
```

Then `git revert <follow-up-commit-sha>` to remove the 17 CSV header column extensions + akos.* tuple updates + validator extensions + tests + design/proposal/phase docs. The mirror tables return to their P4-state schema cleanly; the standalone table is dropped entirely.

### 2.3 RLS posture

**No RLS policy changes on the 17 newly-extended mirrors.** All 17 already carry `RLS = ON` with `service_role`-only deny-`anon`/-`authenticated` posture per the I14 / I59 / I32 mirror inheritance. Adding 4 nullable columns inherits the existing row-level posture; no policy edits required.

**New RLS policy on `compliance.review_stamps_standalone`.** The CREATE TABLE statement is followed in the same transaction by:

1. `ALTER TABLE compliance.review_stamps_standalone ENABLE ROW LEVEL SECURITY` — enables RLS.
2. `CREATE POLICY review_stamps_standalone_service_role_all ON compliance.review_stamps_standalone FOR ALL TO service_role USING (true) WITH CHECK (true)` — `service_role` ALL access.

Equivalent to the posture every other `compliance.*` mirror table carries. The `service_role`-only access posture means stamps are written / read by sync jobs and validator scripts with `service_role` JWT, never by `anon` / `authenticated` roles.

**Confirmation method (post-apply)**: `get_advisors` MCP with `type: security` returns no new advisories attributable to the migration. (Pre-existing advisories on these tables — if any — pre-date this follow-up and stay unchanged.) The `get_advisors security` lint catches `0006_rls_disabled_in_public` / `0010_security_definer_view` / etc.; the new standalone table must NOT trigger `0010` (no SECURITY DEFINER) and MUST NOT trigger `0006` (RLS enabled in the same transaction).

### 2.4 PII analysis

**None of the new columns or the new table carry PII.**

| Surface | Column | Type | PII? | Rationale |
|---------|--------|------|:----:|-----------|
| 17 mirrors × 4 columns | `last_review_at` | DATE | No | Operational metadata (a date). |
| Same | `last_review_by` | TEXT | No | Org-internal `role_name` string (e.g. `PMO`, `System Owner`); not a personal identifier even when a role resolves to a single individual. |
| Same | `last_review_decision_id` | TEXT | No | Governance-internal identifier (`D-IH-NN-X` pattern). |
| Same | `methodology_version_at_review` | TEXT | No | Doctrine version string (`vMAJOR.MINOR`). |
| `compliance.review_stamps_standalone` | `subject_kind` | TEXT (enum-via-CHECK) | No | Enum value (`canonical_md` / `standalone_csv` / `sop_md`). |
| Same | `subject_path` | TEXT | No | Repo-relative file path. |
| Same | `subject_id` | TEXT | No | Cross-reference to `CANONICAL_REGISTRY.canonical_id` (governance-internal). |
| Same | `last_review_at` / `last_review_by` / `last_review_decision_id` / `methodology_version_at_review` | DATE / TEXT | No | Same rationale as the mirror columns. |
| Same | `id` / `created_at` / `updated_at` | BIGSERIAL / TIMESTAMPTZ | No | System-internal audit columns. |

No GDPR / CCPA / sectoral-PII triggers. Aligns with the existing P4 column-extension PII posture and the existing mirror-column posture (no `compliance.*` mirror columns carry PII today).

## 3. Execute (operator blanket-trust pre-approval)

Per the operator's blanket trust signal recorded at the I71 P4 kickoff prompt: the agent applies the migration via Supabase MCP `apply_migration` with this proposal doc + the design doc + the migration file constituting the audit trail.

**Apply call**:

```text
apply_migration(
  project_id="swrmqpelgoblaquequzb",
  name="i71_p4_followup_review_stamp_expansion",
  query=<contents of supabase/migrations/<ts>_i71_p4_followup_review_stamp_expansion.sql §2.1>
)
```

**Post-apply verification**:

1. `list_tables(project_id="swrmqpelgoblaquequzb", schemas=["compliance"], verbose=true)` — confirm all 17 newly-extended mirror tables carry the 4 new columns AND `compliance.review_stamps_standalone` is present with the expected 10 columns + UNIQUE constraint.
2. `list_migrations(project_id="swrmqpelgoblaquequzb")` — confirm the new migration row appears in the Supabase ledger.
3. `execute_sql` (read-only) sample SELECTs:
   - `SELECT COUNT(*) FROM compliance.review_stamps_standalone` (expected: number of CANONICAL_REGISTRY rows with non-empty `last_review` at backfill time).
   - `SELECT column_name FROM information_schema.columns WHERE table_schema='compliance' AND table_name='baseline_organisation_mirror' AND column_name LIKE 'last_review%'` (expected: 3 rows — `last_review_at`, `last_review_by`, `last_review_decision_id`).
4. `get_advisors(project_id="swrmqpelgoblaquequzb", type="security")` — confirm no new advisories attributable to the migration. Expected: zero new entries.
5. `get_advisors(project_id="swrmqpelgoblaquequzb", type="performance")` — confirm no new advisories attributable to the migration. Expected: zero new entries.

**On failure**:

1. STOP per opt-stop-report posture (`akos-governance-remediation.mdc`).
2. Author `docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/reports/p4-followup-blocker-2026-05-14.md` capturing failure detail + rollback SQL.
3. Apply rollback SQL via `apply_migration` per §2.2.
4. Return to parent for re-coordination.

## 4. Pre-push parity check

Per `.cursor/rules/akos-holistika-operations.mdc` §"Operator SQL gate" step 4: `supabase migration list` (local + remote must match). Since the agent applies via MCP `apply_migration` (the break-glass path per §"Break-glass" of the rule), the post-apply verification via `list_migrations` MCP serves the same purpose: the new migration timestamp appears in the Supabase ledger; the local `supabase/migrations/<ts>_i71_p4_followup_review_stamp_expansion.sql` file matches the SQL the MCP applied. Parity holds by construction since the MCP applies the contents of the file we author + commit.

## 5. Cross-references

- Sibling design doc: [`p4-followup-design-2026-05-14.md`](p4-followup-design-2026-05-14.md) — verdict + per-subject-class coverage + risk register + cross-references.
- P4 commit: `bb04f08` (Strand C2 column-extension on the 4 governance-trio mirrors).
- P4 sibling SQL proposal: [`sql-proposal-p4-review-stamp-2026-05-14.md`](sql-proposal-p4-review-stamp-2026-05-14.md) — the prior-round audit trail this follow-up extends.
- Migration file: `supabase/migrations/<ts>_i71_p4_followup_review_stamp_expansion.sql`.
- Phase report (post-execution): `p4-followup-review-stamp-expansion-2026-05-14.md`.
- Cursor rule: [`akos-holistika-operations.mdc`](../../../../../.cursor/rules/akos-holistika-operations.mdc) §"Operator SQL gate" + §"Two-plane model" — the doctrine this proposal operationalises.
- Cursor rule: [`akos-governance-remediation.mdc`](../../../../../.cursor/rules/akos-governance-remediation.mdc) — opt-stop-report posture for migration failures + canonical-CSV gate.
- Cursor rule: [`akos-docs-config-sync.mdc`](../../../../../.cursor/rules/akos-docs-config-sync.mdc) — CSV header + akos.* tuple + mirror DDL same-commit sync contract.
- Decision authority: `D-IH-71-Q` (P4 ratification) → `D-IH-71-R` (this follow-up; minted at this commit).
- OPS state: `OPS-71-3` already CLOSED at P4 with `closure_decision_id: D-IH-71-Q`; no OPS state change at follow-up.

End of P4 follow-up SQL proposal doc.
