-- Parity: scripts/sql/i71/20260514_p4_review_stamp_up.sql (none — direct apply per I71 P4 atomic discipline)
-- I71 P4 — Strand C2 review-stamp dimension (column-extension on mirrored canonicals)
--
-- Authority: D-IH-71-E (P0 review-stamp dimension proposal) + D-IH-71-D (P0 release-taxonomy
--            three-lane ratification operationalising the methodology version naming) +
--            D-IH-71-P (P3 customer-invisible versioning posture; release-taxonomy SOP) +
--            D-IH-71-Q (this P4: column-vs-table ratification; column-extension verdict;
--            migration applied; validator live; OPS-71-3 closes).
--
-- C-71-4 verdict (ratified inline at P4 execution; default applied):
--   - column-extension where compliance mirror exists (4 mirrored canonicals: process_list +
--     decision_register + initiative_registry + ops_register; 4 columns × 4 tables = 16 ALTERs)
--   - separate-table for unmirrored canonicals (CANONICAL_REGISTRY = Artifact class; deferred
--     to follow-up commit when the first standalone canonical needs a stamp; standalone-table
--     path materialises as compliance.review_stamps_standalone with file_path FK at that time)
--
-- Per akos-holistika-operations.mdc §"Operator SQL gate":
--   - Discovery: MCP list_tables run 2026-05-14; inventory documented in
--     reports/sql-proposal-p4-review-stamp-2026-05-14.md §1.2 (4 mirrored target tables;
--     1 unmirrored deferral).
--   - Proposal: DDL + rollback + RLS + PII notes captured in
--     reports/sql-proposal-p4-review-stamp-2026-05-14.md §2 (rollback verbatim at §2.2;
--     RLS no-change verdict at §2.3; PII none-of-the-4-columns at §2.4).
--   - Execute: this migration applies via Supabase MCP apply_migration with operator
--     blanket-trust pre-approval signal recorded at the I71 P4 kickoff prompt (operator
--     authorised "all actions except informational"); the proposal doc + design doc +
--     this migration file constitute the operator-visible audit trail.
--   - Pre-push parity: post-apply list_migrations MCP confirms the new timestamp lands
--     in the Supabase ledger; local file matches the SQL the MCP applied (parity by
--     construction since MCP applies the contents of this file).
--
-- Pattern: I70 P8.2 baseline_sub_area_status (ADD COLUMN IF NOT EXISTS for nullable additive
--          columns; idempotent on re-apply). NOT VALID + VALIDATE CONSTRAINT pattern (I70 P8.5)
--          NOT invoked because P4 adds no CHECK constraints.
--
-- Rollback plan: Symmetric DROP COLUMN per mirror table; SQL provided verbatim in
--                reports/sql-proposal-p4-review-stamp-2026-05-14.md §2.2. To roll back: apply
--                the rollback SQL via apply_migration on the next free timestamp, then
--                git revert the P4 commit to remove CSV header columns + akos.* tuple entries
--                + validator + tests + design/proposal/phase docs. Mirror tables return
--                cleanly to their P3-state schema.
--
-- RLS: No policy changes. All 4 mirror tables already carry RLS = ON with service_role-only
--      deny-anon/-authenticated posture per I14 / I59 mirror inheritance. New columns inherit
--      row-level posture; no column-level RLS in Postgres.
--
-- PII: None of the 4 new columns carry PII. last_review_at = date; last_review_by = role_name
--      (org-internal taxonomy); last_review_decision_id = governance-internal D-IH-* identifier;
--      methodology_version_at_review = doctrine version string (vMAJOR.MINOR per D-IH-71-D).

BEGIN;

-- 1. compliance.process_list_mirror — Process subject class (1100 rows; mirrored I14 phase 3)
ALTER TABLE compliance.process_list_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 2. compliance.decision_register_mirror — Decision subject class (51 rows; mirrored I59 P1.5 + I65 P1.1)
ALTER TABLE compliance.decision_register_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 3. compliance.initiative_registry_mirror — Registry-row subject class (governance trio: initiatives; 51 rows; mirrored I59 P1.2)
ALTER TABLE compliance.initiative_registry_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 4. compliance.ops_register_mirror — Registry-row subject class (governance trio: ops actions; 22 rows; mirrored I59 P1.3)
ALTER TABLE compliance.ops_register_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- Backfill posture: empty by default for all existing rows; operator backfills incrementally
-- per docs/wip/planning/REVIEW_STAMP_INBOX.md workflow (sidecar to OPERATOR_INBOX.md;
-- auto-rendered by scripts/validate_review_stamps.py). Documented no-op self-update statements
-- below per the kickoff Step 3 template (NULL-stays-NULL; documents the backfill point even
-- though no pre-existing source column carries authored / last_review-shaped values to project
-- from). The validator surfaces missing-stamp rows as INFO advisories until backfill completes.

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
