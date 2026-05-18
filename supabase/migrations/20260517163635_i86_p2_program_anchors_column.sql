-- Parity: scripts/sql/i86/20260517_p2_program_anchors_column_up.sql (none — direct apply per the I71-precedent idempotent additive pattern)
-- I86 P2 — Stage B promotion of program-anchors from INITIATIVE_REGISTRY.notes prefix to a
--          first-class semicolon-list FK column (compliance.initiative_registry_mirror.program_anchors).
--
-- Authority: D-IH-86-H (Stage A "Program anchors:" prefix-in-notes shipped 2026-05-17 at I86 P1) +
--            D-IH-86-J (Stage B column-promotion verdict — extend INITIATIVE_REGISTRY.csv + mirror with
--                       a first-class `program_anchors` semicolon-list column; cutover validator default
--                       to column-read; one-cycle `--legacy-notes-parser` deprecation window).
--            D-IH-86-I (charter-scope amendment — minting governance tooling under I86 is allowed
--                       even though I86 charter says "mints no new SSOT"; program_anchors is FK
--                       infrastructure not new SSOT — PROGRAM_REGISTRY remains the program SSOT).
--
-- Per akos-holistika-operations.mdc §"Operator SQL gate":
--   - Discovery: MCP list_tables (already inventoried at I59 P1.2 mirror creation 2026-05-06;
--     compliance.initiative_registry_mirror schema confirmed at 22 columns + 2 sync columns
--     post-I71 P4 review-stamp expansion 2026-05-14).
--   - Proposal: DDL + rollback + RLS + PII notes captured inline below (P2 is a single-column ALTER;
--     no separate proposal markdown necessary per I71 P4 atomic-discipline precedent).
--   - Execute: this migration applies via Supabase MCP apply_migration after the operator ratifies
--     the P2 pause-record at reports/p2-pause-record-2026-05-17.md. Operator-applied (not agent-applied)
--     per the akos-holistika-operations.mdc "I propose; operator applies" posture for canonical CSV gates.
--   - Pre-push parity: post-apply, operator runs `supabase migration list` + verifies new timestamp
--     lands in the Supabase ledger; local file matches MCP-applied content by construction.
--
-- Pattern: I71 P4 review-stamp (`ADD COLUMN IF NOT EXISTS` for nullable additive columns; idempotent
--          on re-apply). NOT VALID + VALIDATE CONSTRAINT pattern (I70 P8.5) NOT invoked because P2
--          adds no CHECK constraints; FK-by-convention to PROGRAM_REGISTRY.csv enforced at the CSV
--          validator layer (scripts/validate_initiative_registry.py), not at the Postgres layer (the
--          PROGRAM_REGISTRY mirror lives in compliance.* but FKs across semicolon-list-decoded columns
--          would require a join trigger; CSV-side validation is cheaper + sufficient per D-IH-86-J).
--
-- Rollback plan: `ALTER TABLE compliance.initiative_registry_mirror DROP COLUMN IF EXISTS program_anchors;`
--                Then drop the index. Then git revert the P2 commit to remove the CSV header column,
--                akos.* tuple entry, validator block, cutover flag, and one-shot script. Mirror table
--                returns cleanly to its post-I71-P4 schema.
--
-- RLS: No policy changes. Existing RLS on compliance.initiative_registry_mirror (deny anon / deny
--      authenticated; service_role only) inherits to the new column. No column-level RLS in Postgres.
--
-- PII: None. `program_anchors` carries semicolon-list of `PRJ-HOL-<CODE>-<YEAR>` ids that resolve to
--      governance-internal program identifiers (PROGRAM_REGISTRY.csv); not personal data; not external
--      identifiers; classification = Internal Use per Confidence Levels SOP.

BEGIN;

ALTER TABLE compliance.initiative_registry_mirror
  ADD COLUMN IF NOT EXISTS program_anchors TEXT;

COMMENT ON COLUMN compliance.initiative_registry_mirror.program_anchors IS
  'I86 P2 (D-IH-86-J): semicolon-list FK to PROGRAM_REGISTRY.csv program_id (PRJ-HOL-<CODE>-<YEAR>). Stage B promotion from the Stage A "Program anchors:" prefix in notes. FK enforcement lives in scripts/validate_initiative_registry.py (CSV side) not Postgres-side (semicolon-list decoding pattern matches linked_topic_ids).';

-- Index for rollup queries (e.g. governance.initiative_program_rollup_view at P3) — supports
-- LIKE '%PRJ-HOL-XYZ%' lookups against the unsplit string; semicolon-list arity is small (≤5
-- anchors per initiative in current data) so btree-on-text is sufficient. P3 view will use
-- string_to_array() for join arity.
CREATE INDEX IF NOT EXISTS initiative_registry_mirror_program_anchors_idx
  ON compliance.initiative_registry_mirror (program_anchors);

-- Backfill posture: column is empty-by-default for all existing rows; CSV-side one-shot conversion
-- (scripts/_oneshot_anchors_notes_to_column.py --apply) populates the canonical CSV before the
-- operator re-runs `compliance_mirror_emit` to refresh the mirror. No data UPDATE in this migration;
-- the next CSV→SQL sync run after the one-shot rewrite of INITIATIVE_REGISTRY.csv carries the values
-- (UPSERT via _emit_initiative_registry_upserts in scripts/sync_compliance_mirrors_from_csv.py).

COMMIT;
