# I71 P4 follow-up — Design ratification (review-stamp expansion + Artifact standalone-table)

> Authored 2026-05-14 BEFORE the Supabase migration applies. Round-2 follow-up to P4 commit `bb04f08`. Sibling to [`sql-proposal-p4-followup-2026-05-14.md`](sql-proposal-p4-followup-2026-05-14.md) (Operator SQL Gate audit trail) and the migration file `supabase/migrations/20260514_______i71_p4_followup_review_stamp_expansion.sql`. Phase report `p4-followup-review-stamp-expansion-2026-05-14.md` lands at commit time.

## 1. Authority + scope

- **`D-IH-71-Q`** (P4 commit `bb04f08`) — Strand C2 column-extension verdict on the four governance-trio mirrors (process_list / decision_register / initiative_registry / ops_register). C-71-4 default applied: column-extension where mirror exists; standalone-table for unmirrored canonicals; the standalone-table path was deferred to a follow-up commit "when first unmirrored canonical needs a stamp".
- **`D-IH-71-R`** (MINTED at this commit, 2026-05-14) — Round-2 follow-up ratification covering both extensions in a single decision row:
  - **(A) Column-extension expansion**: review-stamp 4-column shape applied to the **17 remaining mirrored compliance.* canonicals** beyond the 4 already extended at P4. Validator surface coverage grows from 4 → 21.
  - **(B) Standalone-table for the Artifact subject class**: `compliance.review_stamps_standalone` table minted (`subject_kind` + `subject_path` + 4-column stamp shape + `subject_id` cross-ref to `CANONICAL_REGISTRY.canonical_id`). Initial backfill from `CANONICAL_REGISTRY.csv` `last_review` column.
- **Operator authority** — blanket trust signal recorded at the I71 P4 kickoff prompt ("I trust you to perform all actions except informational"). Per `.cursor/rules/akos-governance-remediation.mdc` Canonical-CSV gates and `.cursor/rules/akos-holistika-operations.mdc` Operator SQL gate, the operator pre-approves the canonical-CSV header changes for the 17 newly-extended CSVs and the Supabase migration (DDL on 17 mirrored tables + 1 new standalone table). The audit trail lives in this design doc + the sibling SQL proposal doc + the migration file itself.

## 2. Mirror enumeration (Step 0 discovery)

MCP `list_tables` filtered to schema `compliance` ran 2026-05-14. Cross-referenced against the `validate_compliance_schema_drift.py` `_REGISTRY` (22 tuple-aligned canonical CSVs) and the four mirrors already extended at P4 to derive the to-extend set.

### 2.1 Mirrors extended at this commit (column-extension; 17)

| # | Mirror | Canonical CSV | `akos.*` SSOT tuple | Pre cols | Post cols | Rationale |
|---|--------|---------------|---------------------|---------:|----------:|-----------|
| 1 | `compliance.baseline_organisation_mirror` | `baseline_organisation.csv` | `BASELINE_ORGANISATION_FIELDNAMES` | 17 | 21 | Org / role doctrine; review cadence anchors to v3.x methodology version. |
| 2 | `compliance.finops_counterparty_register_mirror` | `FINOPS_COUNTERPARTY_REGISTER.csv` | `FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES` | 17 | 21 | Counterparty metadata — review on contract anniversary. |
| 3 | `compliance.goipoi_register_mirror` | `dimensions/GOI_POI_REGISTER.csv` | `GOIPOI_REGISTER_FIELDNAMES` | 20 | 24 | Knowledge dimension; quarterly distance-reassessment per SOP-HLK_GOIPOI. |
| 4 | `compliance.adviser_engagement_disciplines_mirror` | `ADVISER_ENGAGEMENT_DISCIPLINES.csv` | `ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES` | 8 | 12 | ADVOPS lookup table; review on discipline expansion. |
| 5 | `compliance.adviser_open_questions_mirror` | `ADVISER_OPEN_QUESTIONS.csv` | `ADVISER_OPEN_QUESTIONS_FIELDNAMES` | 11 | 15 | ADVOPS open queue; review when row is closed or ages > target_date. |
| 6 | `compliance.founder_filed_instruments_mirror` | `FOUNDER_FILED_INSTRUMENTS.csv` | `FOUNDER_FILED_INSTRUMENTS_FIELDNAMES` | 13 | 17 | Legal instruments; review on filing-anniversary or supersedes event. |
| 7 | `compliance.program_registry_mirror` | `dimensions/PROGRAM_REGISTRY.csv` | `PROGRAM_REGISTRY_FIELDNAMES` | 15 | 19 | Program portfolio; review on lifecycle_status transition. |
| 8 | `compliance.topic_registry_mirror` | `dimensions/TOPIC_REGISTRY.csv` | `TOPIC_REGISTRY_FIELDNAMES` | 14 | 18 | KM topic axis; review on edge graph re-projection. |
| 9 | `compliance.persona_registry_mirror` | `dimensions/PERSONA_REGISTRY.csv` | `PERSONA_REGISTRY_FIELDNAMES` | 13 | 17 | Persona archetypes; review on touchpoint-kit refresh. |
| 10 | `compliance.persona_scenario_registry_mirror` | `dimensions/PERSONA_SCENARIO_REGISTRY.csv` | `PERSONA_SCENARIO_REGISTRY_FIELDNAMES` | 20 | 24 | UAT scenario library; review on baseline calibration. |
| 11 | `compliance.channel_touchpoint_registry_mirror` | `dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv` | `CHANNEL_TOUCHPOINT_REGISTRY_FIELDNAMES` | 11 | 15 | Touchpoint registry; review on channel-strategy update. |
| 12 | `compliance.sourcing_register_mirror` | `dimensions/SOURCING_REGISTER.csv` | `SOURCING_REGISTER_FIELDNAMES` | 12 | 16 | Vendor / sourcing log; review on quality_band re-grade. |
| 13 | `compliance.skill_registry_mirror` | `dimensions/SKILL_REGISTRY.csv` | `SKILL_REGISTRY_FIELDNAMES` | 17 | 21 | Skill versioning; review on skill graduation gate. |
| 14 | `compliance.touchpoint_kit_cell_mirror` | `dimensions/TOUCHPOINT_KIT_CELL_REGISTRY.csv` | `TOUCHPOINT_KIT_CELL_FIELDNAMES` | 10 | 14 | Cell registry already carries `last_review`; new dimension is doctrine-review-cadence (orthogonal). |
| 15 | `compliance.policy_register_mirror` | `dimensions/POLICY_REGISTER.csv` | `POLICY_REGISTER_FIELDNAMES` | 11 | 15 | Already carries `last_review` + `next_review`; new dimension is methodology-version anchored review. |
| 16 | `compliance.repo_health_snapshot_mirror` | `REPO_HEALTH_SNAPSHOT.csv` | `REPO_HEALTH_SNAPSHOT_FIELDNAMES` | 16 | 20 | Cross-repo snapshots; review on bless-pattern roll-out. |
| 17 | `compliance.repository_registry_mirror` | `REPOSITORY_REGISTRY.csv` | `REPOSITORY_REGISTRY_FIELDNAMES` | 13 | 17 | Repo registry; review on cross-repo CI baseline bump. |

**Total**: 17 ALTER TABLE statements × 4 columns each = 68 `ADD COLUMN` operations. Same 4-column shape as P4 (`last_review_at` DATE / `last_review_by` TEXT / `last_review_decision_id` TEXT / `methodology_version_at_review` TEXT). All `ADD COLUMN IF NOT EXISTS` for idempotency.

### 2.2 Mirrors not extended at this commit (rationale)

| Mirror | Class | Reason |
|--------|-------|--------|
| `compliance.access_level` (7 rows) | Lookup taxonomy | Not a CSV mirror; mirrored from `access_levels.md` doctrine. Stamp-shape doesn't apply. |
| `compliance.confidence_level` (3 rows) | Lookup taxonomy | Same rationale. |
| `compliance.source_category` (6 rows) | Lookup taxonomy | Same rationale. |
| `compliance.source_level` (18 rows) | Lookup taxonomy | Same rationale. |
| `compliance.validation_runs` (0 rows) | Operational fact | Explicit comment in `list_tables`: "NOT git SSOT". Append-only audit log of validator runs; per-row review is meaningless. |
| `compliance.eval_run` (0 rows) | Operational fact | Same rationale; append-only eval history. |
| `compliance.dossier_run` (0 rows) | Operational fact | Same rationale; append-only dossier render history. |

**Conservative-include posture**: per kickoff "Default = extend everything that's mirrored. If a mirror exists you're unsure should get a stamp, include it conservatively unless there's a clear reason not to." The 7 excluded mirrors all carry a clear reason: 4 are taxonomy lookups (no canonical CSV SSOT to back them), 3 are operational append-only facts (per-row stamping breaks the append-only contract). Documenting the exclusions inline so the next round of expansion (if any) inherits the rationale.

### 2.3 Unmirrored canonicals at this commit

- **`CANONICAL_REGISTRY.csv`** (Artifact subject class; 111 rows) — **standalone-table path** ships here per §3 below.
- **`CYCLE_REGISTER.csv`** (Cycle subject class; akos.* tuple exists at `akos.hlk_cycle_register_csv`; no Supabase mirror today) — **deferred**. Standalone-table path applies in principle (the new `compliance.review_stamps_standalone` table is generic enough: `subject_kind` accepts a future `cycle_csv` enum value), but the operator-driven trigger to stamp cycles has not fired. Forward-charter: when a cycle's freshness becomes a governance question, append a row to `compliance.review_stamps_standalone` with `subject_kind='cycle_csv'` and `subject_path='docs/.../CYCLE_REGISTER.csv'`. No work at this commit.

## 3. Standalone-table path (Artifact subject class)

### 3.1 Architecture verdict — `compliance.review_stamps_standalone`

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Table name | `compliance.review_stamps_standalone` | Per kickoff Step 3 template; matches the `review_stamp` semantic + `standalone` (vs column-extension) classifier. |
| Subject naming | `subject_kind` enum + `subject_path` repo-relative path | Path is the natural key for canonical .md files (CANONICAL_REGISTRY's `file_path` column). `subject_kind` (`canonical_md` / `standalone_csv` / `sop_md`) future-proofs for non-CANONICAL_REGISTRY-driven stamps (e.g. unmirrored CSVs like CYCLE_REGISTER, SOPs that aren't in the registry). |
| Cross-reference | Optional `subject_id` TEXT column | Carries `CANONICAL_REGISTRY.canonical_id` when applicable; nullable for non-registry surfaces. **Not** a hard FK — the registry CSV is git-canonical; FK enforcement requires a CANONICAL_REGISTRY mirror table that doesn't exist today. The validator cross-checks the FK by-convention (same posture as `last_review_decision_id` ↔ `DECISION_REGISTER.csv`). |
| Stamp-shape columns | Same 4 columns as column-extension path (`last_review_at` DATE / `last_review_by` TEXT / `last_review_decision_id` TEXT / `methodology_version_at_review` TEXT) | Symmetric with column-extension path; same validator code-path can read both surfaces. |
| Audit columns | `id BIGSERIAL PRIMARY KEY` + `created_at TIMESTAMPTZ NOT NULL DEFAULT now()` + `updated_at TIMESTAMPTZ NOT NULL DEFAULT now()` | Standard mirror table audit columns; consistent with `compliance.validation_runs` / `compliance.eval_run` shape. |
| Uniqueness constraint | `UNIQUE (subject_kind, subject_path)` | One stamp per (kind, path) tuple. Idempotent INSERTs use `ON CONFLICT (subject_kind, subject_path) DO NOTHING` for backfill. |
| RLS posture | `service_role` only (deny `anon` / `authenticated`); same as every `compliance.*` mirror | Per `akos-holistika-operations.mdc` §"Schema responsibilities". Stamps are governance-internal metadata. |

### 3.2 FK choice rationale (`subject_path` vs `subject_id`)

The kickoff offered both options. Verdict: **both** — `subject_path` is the natural key (UNIQUE), `subject_id` is the optional cross-reference. Rationale:

- `subject_path` is **stable across CANONICAL_REGISTRY mutations**. If a canonical_id is renamed (rare but possible), the path stays; the validator and operator queries-by-path continue to work.
- `subject_id` is the **operator's preferred lookup** in the typical case (operator searches by `canonical_id`, not by repo-relative path). Carrying it as a separate column makes both query paths first-class.
- Neither is a hard PostgreSQL FK because CANONICAL_REGISTRY is unmirrored. The validator enforces both relationships by convention (same posture as `last_review_decision_id` ↔ `DECISION_REGISTER.csv` at P4).

### 3.3 Backfill posture (initial population)

At migration time, the standalone table is backfilled from `CANONICAL_REGISTRY.csv`:

```sql
-- Backfill from CANONICAL_REGISTRY.csv last_review column (where present)
INSERT INTO compliance.review_stamps_standalone
    (subject_kind, subject_path, subject_id, last_review_at)
SELECT 'canonical_md', file_path, canonical_id, last_review::DATE
FROM <staging_table_loaded_from_csv>
WHERE last_review IS NOT NULL AND last_review != ''
ON CONFLICT (subject_kind, subject_path) DO NOTHING;
```

Per kickoff Step 3 "Backfill initial rows from `CANONICAL_REGISTRY.csv` `last_review` column (if present) for any canonicals with that frontmatter today. Pure data move; idempotent INSERT ... ON CONFLICT DO NOTHING."

The migration file performs the backfill via inline `INSERT ... VALUES` rows (deterministic; no external CSV staging table). Each row carries `subject_kind='canonical_md'`, `subject_path` from `CANONICAL_REGISTRY.csv` `file_path`, `subject_id` from `canonical_id`, and `last_review_at` from `last_review`. Rows with empty `last_review` are skipped (the validator surfaces them as `missing-stamp` advisories on next run).

`last_review_by` / `last_review_decision_id` / `methodology_version_at_review` are NULL for backfilled rows. Operator backfills incrementally per `REVIEW_STAMP_INBOX.md` workflow (the validator's Artifact-class scan surfaces them as `missing-stamp` info advisories).

## 4. Validator extension plan (Step 6)

### 4.1 Mirror registry expansion (4 → 21 surfaces)

`scripts/validate_review_stamps.py` `_REGISTRY` grows from 4 entries (P4 baseline) to 21 entries (P4 baseline + 17 newly-extended canonicals). Each entry is a `CanonicalSpec(csv_path, fieldnames, pk_column, authored_date_column, label)` — same shape as P4. The 17 new entries:

| Spec | `pk_column` | `authored_date_column` | Notes |
|------|-------------|------------------------|-------|
| `baseline_organisation` | `org_uuid` | None | Org rows have no canonical authored-date column. |
| `finops_counterparty_register` | `counterparty_id` | None | No authored-date column; renewal_review_due is forward-looking, not retrospective. |
| `goipoi_register` | `ref_id` | `distance_assessed_date` | Quarterly cadence per SOP-HLK_GOIPOI. |
| `adviser_engagement_disciplines` | `discipline_id` | None | Lookup table; no authored-date. |
| `adviser_open_questions` | `question_id` | `target_date` | target_date is forward-looking but serves as a coarse age-proxy for the question. |
| `founder_filed_instruments` | `instrument_id` | `effective_or_filing_date` | Filing date is the canonical authored-date proxy. |
| `program_registry` | `program_id` | `start_date` | Program lifecycle. |
| `topic_registry` | `topic_id` | None | Topics have no authored-date column. |
| `persona_registry` | `persona_id` | None | Persona definitions; no authored-date. |
| `persona_scenario_registry` | `scenario_id` | None | Scenarios have no authored-date column. |
| `channel_touchpoint_registry` | `channel_id` | None | Touchpoint definitions; no authored-date. |
| `sourcing_register` | `vendor_id` | `last_engagement_date` | Engagement date doubles as activity proxy. |
| `skill_registry` | `skill_id` | None | Skill definitions; no authored-date column. |
| `touchpoint_kit_cell` | `cell_id` | `last_review` | Cell registry already carries a `last_review` column; reused as authored-date proxy (the new `last_review_at` is doctrine-review-cadence; the existing `last_review` is cell-content-review-cadence; orthogonal but the existing column proxies authoring well). |
| `policy_register` | `policy_id` | `last_review` | Same posture as touchpoint_kit_cell — existing `last_review` is the existing per-policy review cadence; new `last_review_at` is methodology-version-anchored. |
| `repo_health_snapshot` | `snapshot_date` | `snapshot_date` | Snapshot date is both PK component and authored-date. |
| `repository_registry` | `repo_slug` | None | Repo definitions; no authored-date. |

### 4.2 Artifact subject class scan (new `_scan_canonical_md_artifacts()`)

New helper walks every row in `CANONICAL_REGISTRY.csv` and emits advisories per the same 3 rule classes (stale-row / missing-stamp / invalid-decision-ref). The helper:

1. Reads `CANONICAL_REGISTRY.csv` to enumerate all (canonical_id, file_path, last_review) tuples.
2. For each row: treats `last_review` as the stamp date (`last_review_at` semantic). Applies the same 180-day stale-row threshold + 30-day missing-stamp grace.
3. Emits advisories with `canonical='canonical_registry_artifact'` and `pk=canonical_id` for traceability.

**No live Supabase query.** Per kickoff guidance: "If the existing P4 validator queries Supabase live, follow that pattern; if it reads CSVs, use the snapshot approach." The P4 validator reads CSVs (no Supabase round-trip). Therefore the Artifact scan also reads CSVs — specifically, `CANONICAL_REGISTRY.csv` as the SSOT for the file path + stamp date. The standalone table backfill at migration time is a forward-provisioning move (operator can write richer stamps via Supabase later); the validator stays CSV-driven for the hot path.

**Future enhancement (not at this commit)**: a separate `scripts/sync_review_stamps_standalone_snapshot.py` could dump `compliance.review_stamps_standalone` to a snapshot CSV when richer stamps land. The validator would prefer the snapshot over `CANONICAL_REGISTRY.last_review` if present. Out of scope at this commit; the trigger fires when the operator writes the first non-`last_review`-derived row to `compliance.review_stamps_standalone`.

### 4.3 Inbox surfacing extension

`docs/wip/planning/REVIEW_STAMP_INBOX.md` already auto-renders advisories from the P4 validator. The 21-surface expansion + Artifact scan automatically surface to the same inbox file (no new code path; the existing `_surface_to_inbox()` aggregates by rule class). Total advisory volume scales with row count: P4 baseline ~1212 info / 0 warning / 0 error across 1364 rows; post-expansion expected ~2000-2500 info advisories across ~2000 rows (until operator backfills incrementally).

## 5. Test plan (Step 7)

`tests/test_validate_review_stamps.py` extensions:

| Test cluster | Cases added | Coverage |
|--------------|------------:|----------|
| `TestColumnExtensionMigrationExpanded` | 17 | One assertion per newly-extended SSOT tuple confirms it carries the 4 review-stamp columns. Mirrors the existing 4 P4 assertions (`test_*_carries_4_review_stamp_columns`). |
| `TestRegistryExpansion` | 1-2 | Asserts `_REGISTRY` length is 21 (4 P4 + 17 follow-up) and includes the new labels. |
| `TestArtifactScan` | 4-5 | Synthetic `CANONICAL_REGISTRY.csv` fixture exercises stale / missing / fresh / invalid-decision-ref paths. |
| `TestComplianceSchemaDriftRegression` | 1 | Smoke-runs `validate_compliance_schema_drift.py` and asserts PASS across all 22 registry rows post-extension. |
| `TestRealCanonicalsSmokeExpanded` | 1 | Smoke-runs the validator against the 21 real CSVs; asserts exit 0 (no errors; advisories OK). |

Total cases added: ~25-28 (on top of P4's 29 cases). Marker stays `@pytest.mark.brand` (chassis-precedent marker; no new marker needed).

`tests/test_validate_brand_voice_register_expansion.py` (P1 chassis) must remain green (regression marker).

## 6. Migration sequencing

Single transaction in `supabase/migrations/<ts>_i71_p4_followup_review_stamp_expansion.sql`:

1. `ALTER TABLE` × 17 mirror tables (each adds 4 columns; idempotent via `IF NOT EXISTS`).
2. `CREATE TABLE IF NOT EXISTS compliance.review_stamps_standalone` (8 columns + UNIQUE constraint).
3. `ALTER TABLE compliance.review_stamps_standalone ENABLE ROW LEVEL SECURITY`.
4. `CREATE POLICY review_stamps_standalone_service_role_all` (FOR ALL TO service_role).
5. Documented no-op `UPDATE ... SET last_review_at = COALESCE(last_review_at::DATE, NULL)` for each newly-extended mirror (NULL-stays-NULL self-update; documents the backfill point per the P4 kickoff template).
6. Inline `INSERT ... VALUES ... ON CONFLICT DO NOTHING` backfill rows for `compliance.review_stamps_standalone` from `CANONICAL_REGISTRY.csv` `last_review` column (subset of rows where `last_review` is non-empty).

Pattern: Same as P4's atomic single-transaction approach; same `IF NOT EXISTS` idempotency; same backfill posture (empty-by-default for stamp columns; the standalone-table backfill from CANONICAL_REGISTRY's existing `last_review` column is a pure data move, not stamp-authoring).

## 7. Risk + rollback

| Risk | Severity | Mitigation |
|------|:--------:|------------|
| Migration partial-apply leaves some of 17 mirrors with new columns + others without | High | Single transaction (`BEGIN; ... COMMIT;`); `IF NOT EXISTS` idempotent guard. Rollback DDL provided verbatim in SQL proposal §2.2. Re-applying the same migration is a no-op for already-applied ALTERs. |
| CSV header drift between newly-extended canonicals + akos.* tuples | High | `validate_compliance_schema_drift.py` runs in release-gate and locks header ↔ tuple alignment per the I70 P8.5 + I71 P4 precedent. |
| `compliance.review_stamps_standalone` ships without RLS policy | High | Migration enables RLS + creates `service_role` ALL policy in same transaction. Post-apply `get_advisors security` confirms no RLS-missing advisory. |
| validator's Artifact scan over-flags (every CANONICAL_REGISTRY row missing `last_review` becomes an info advisory) | Medium | `missing-stamp` is `info` severity (non-blocking); release-gate wraps as INFO row (advisory only). The 30-day grace from authored-date proxy doesn't apply (CANONICAL_REGISTRY has no authored-date column), so all empty-last_review rows surface — by design, this is the operator's incremental-backfill workload. |
| Standalone-table backfill INSERT collides on UNIQUE constraint if migration re-applied | Low | `ON CONFLICT (subject_kind, subject_path) DO NOTHING` makes backfill idempotent. |
| CYCLE_REGISTER deferred but no follow-up task tracked | Low | Documented inline at §2.3; the standalone-table pattern is generic enough to absorb cycle stamps later via `subject_kind='cycle_csv'` without further DDL. |
| Sibling Vale worker push collides with this push | Medium | Wait 90s before first push; `git fetch origin main` + `git pull --rebase` if remote moved; explicit per-path stage avoids accidentally including W1 / W3 files. |

### 7.1 Rollback DDL

Symmetric DROP TABLE + DROP COLUMN per surface; verbatim in `sql-proposal-p4-followup-2026-05-14.md` §2.2. Then `git revert <follow-up-commit-sha>` to remove CSV header columns + akos.* tuple entries + validator extensions + tests + design/proposal/phase docs.

## 8. Cross-references

- Sibling SQL audit doc: [`sql-proposal-p4-followup-2026-05-14.md`](sql-proposal-p4-followup-2026-05-14.md).
- P4 commit: `bb04f08` (Strand C2 column-extension on the 4 governance-trio mirrors).
- P4 design doc: [`p4-design-2026-05-14.md`](p4-design-2026-05-14.md) (the prior-round verdict this follow-up extends).
- P4 SQL proposal doc: [`sql-proposal-p4-review-stamp-2026-05-14.md`](sql-proposal-p4-review-stamp-2026-05-14.md).
- Migration: `supabase/migrations/<ts>_i71_p4_followup_review_stamp_expansion.sql`.
- Validator: [`scripts/validate_review_stamps.py`](../../../../../scripts/validate_review_stamps.py) (extended at this commit).
- Tests: [`tests/test_validate_review_stamps.py`](../../../../../tests/test_validate_review_stamps.py) (extended at this commit).
- Sidecar inbox: [`docs/wip/planning/REVIEW_STAMP_INBOX.md`](../../../REVIEW_STAMP_INBOX.md) (auto-rendered).
- Cursor rules: [`akos-holistika-operations.mdc`](../../../../../.cursor/rules/akos-holistika-operations.mdc) (Operator SQL gate); [`akos-governance-remediation.mdc`](../../../../../.cursor/rules/akos-governance-remediation.mdc) (canonical-CSV gate; opt-stop-report posture); [`akos-docs-config-sync.mdc`](../../../../../.cursor/rules/akos-docs-config-sync.mdc) (CSV header + akos.* tuple + mirror DDL same-commit sync contract).
- Decision authority: `D-IH-71-Q` (P4 ratification) → `D-IH-71-R` (this follow-up; minted at this commit).

End of P4 follow-up design doc. Sibling: `sql-proposal-p4-followup-2026-05-14.md`. Phase report at commit time: `p4-followup-review-stamp-expansion-2026-05-14.md`.
