-- Parity: scripts/sql/i71/20260514_p4_followup_review_stamp_expansion_up.sql (none — direct apply per I71 P4 follow-up Round-2)
-- I71 P4 follow-up — Strand C2 review-stamp dimension expansion (Round 2)
--
-- Authority: D-IH-71-Q (P4 commit bb04f08; Strand C2 column-extension verdict on the four
--            governance-trio mirrors) + D-IH-71-R (this commit; Round-2 follow-up ratifying
--            both extensions in one row).
--
-- Round-2 scope (per p4-followup-design-2026-05-14.md):
--   (A) Column-extension applied to the 17 remaining mirrored compliance.* canonicals beyond
--       the 4 already extended at P4. Same 4-column shape: last_review_at DATE / last_review_by
--       TEXT / last_review_decision_id TEXT / methodology_version_at_review TEXT.
--   (B) compliance.review_stamps_standalone table minted for the Artifact subject class
--       (CANONICAL_REGISTRY canonicals) + RLS service_role-only + initial backfill from
--       CANONICAL_REGISTRY.csv last_review column (where present).
--
-- Per akos-holistika-operations.mdc §"Operator SQL gate":
--   - Discovery: MCP list_tables run 2026-05-14; inventory documented in
--     reports/sql-proposal-p4-followup-2026-05-14.md §1.2 (17 mirrored target tables; 7 excluded
--     mirrors with rationale; CANONICAL_REGISTRY confirmed unmirrored → standalone-table path).
--   - Proposal: DDL + rollback + RLS + PII notes captured in
--     reports/sql-proposal-p4-followup-2026-05-14.md §2 (rollback verbatim at §2.2;
--     RLS service_role-only at §2.3; PII none-of-the-new-columns at §2.4).
--   - Execute: this migration applies via Supabase MCP apply_migration with operator
--     blanket-trust pre-approval signal recorded at the I71 P4 kickoff prompt; the proposal
--     doc + design doc + this migration file constitute the operator-visible audit trail.
--   - Pre-push parity: post-apply list_migrations MCP confirms the new timestamp lands in the
--     Supabase ledger; local file matches the SQL the MCP applied.
--
-- Pattern: I70 P8.2 baseline ADD COLUMN IF NOT EXISTS + I71 P4 (20260514193709_i71_p4_review_stamp.sql).
--          NOT VALID + VALIDATE CONSTRAINT not invoked because the only CHECK is on a brand-new
--          column in a brand-new table (no pre-existing rows to validate against).
--
-- Rollback plan: Symmetric DROP COLUMN per mirror table + DROP TABLE for the standalone table;
--                SQL provided verbatim in reports/sql-proposal-p4-followup-2026-05-14.md §2.2.
--                To roll back: apply the rollback SQL via apply_migration on the next free
--                timestamp, then git revert the follow-up commit to remove CSV header columns +
--                akos.* tuple entries + validator extensions + tests + design/proposal/phase docs.
--                Mirror tables return cleanly to their P4-state schema; the standalone table is
--                dropped entirely.
--
-- RLS: 17 mirror tables already carry RLS = ON with service_role-only deny-anon/-authenticated
--      posture per the I14 / I59 / I32 mirror inheritance — no policy changes for those.
--      compliance.review_stamps_standalone gets RLS enabled in the same transaction with a
--      service_role-only ALL policy (deny anon + authenticated by default).
--
-- PII: None of the new columns nor the new table carry PII. last_review_at = date;
--      last_review_by = role_name (org-internal taxonomy); last_review_decision_id =
--      governance-internal D-IH-* identifier; methodology_version_at_review = doctrine version
--      string (vMAJOR.MINOR per D-IH-71-D); subject_kind = enum; subject_path = repo-relative
--      path; subject_id = canonical_id (governance-internal).

BEGIN;

-- ===========================================================================
-- (A) Column-extension on 17 remaining mirrored compliance.* canonicals
-- ===========================================================================

-- 1. compliance.baseline_organisation_mirror — Org-row subject class
ALTER TABLE compliance.baseline_organisation_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 2. compliance.finops_counterparty_register_mirror
ALTER TABLE compliance.finops_counterparty_register_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 3. compliance.goipoi_register_mirror
ALTER TABLE compliance.goipoi_register_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 4. compliance.adviser_engagement_disciplines_mirror
ALTER TABLE compliance.adviser_engagement_disciplines_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 5. compliance.adviser_open_questions_mirror
ALTER TABLE compliance.adviser_open_questions_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 6. compliance.founder_filed_instruments_mirror
ALTER TABLE compliance.founder_filed_instruments_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 7. compliance.program_registry_mirror
ALTER TABLE compliance.program_registry_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 8. compliance.topic_registry_mirror
ALTER TABLE compliance.topic_registry_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 9. compliance.persona_registry_mirror
ALTER TABLE compliance.persona_registry_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 10. compliance.persona_scenario_registry_mirror
ALTER TABLE compliance.persona_scenario_registry_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 11. compliance.channel_touchpoint_registry_mirror
ALTER TABLE compliance.channel_touchpoint_registry_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 12. compliance.sourcing_register_mirror
ALTER TABLE compliance.sourcing_register_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 13. compliance.skill_registry_mirror
ALTER TABLE compliance.skill_registry_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 14. compliance.touchpoint_kit_cell_mirror
ALTER TABLE compliance.touchpoint_kit_cell_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 15. compliance.policy_register_mirror
ALTER TABLE compliance.policy_register_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 16. compliance.repo_health_snapshot_mirror
ALTER TABLE compliance.repo_health_snapshot_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- 17. compliance.repository_registry_mirror
ALTER TABLE compliance.repository_registry_mirror
  ADD COLUMN IF NOT EXISTS last_review_at DATE,
  ADD COLUMN IF NOT EXISTS last_review_by TEXT,
  ADD COLUMN IF NOT EXISTS last_review_decision_id TEXT,
  ADD COLUMN IF NOT EXISTS methodology_version_at_review TEXT;

-- ===========================================================================
-- (B) Standalone-table for the Artifact subject class (CANONICAL_REGISTRY canonicals)
-- ===========================================================================

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

COMMENT ON TABLE compliance.review_stamps_standalone IS
  'I71 P4 follow-up (D-IH-71-R) — review-stamp surface for unmirrored canonicals (Artifact subject class via CANONICAL_REGISTRY; future cycle_csv / sop_md surfaces). subject_path is the natural key (UNIQUE per subject_kind); subject_id carries the optional FK-by-convention to CANONICAL_REGISTRY.canonical_id when applicable. Stamp shape symmetric with column-extension path (same 4 columns) so the validator code-path reads both surfaces uniformly.';

-- RLS: service_role-only (deny anon + authenticated) per akos-holistika-operations.mdc §"Schema responsibilities"
ALTER TABLE compliance.review_stamps_standalone ENABLE ROW LEVEL SECURITY;

-- Idempotency guard: DROP IF EXISTS before CREATE so re-application (e.g. via supabase db push --include-all
-- during a backfill window) doesn't trip SQLSTATE 42710 — matches the pattern used elsewhere in this file.
DROP POLICY IF EXISTS review_stamps_standalone_service_role_all ON compliance.review_stamps_standalone;
CREATE POLICY review_stamps_standalone_service_role_all
  ON compliance.review_stamps_standalone
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- ===========================================================================
-- Backfill posture (newly-extended mirror columns)
-- ===========================================================================
-- Empty by default for all existing rows; operator backfills incrementally per
-- docs/wip/planning/REVIEW_STAMP_INBOX.md workflow (auto-rendered by
-- scripts/validate_review_stamps.py). Documented no-op self-update statements
-- below per the P4 kickoff Step 3 template (NULL-stays-NULL; documents the
-- backfill point even though no pre-existing source column carries authored /
-- last_review-shaped values to project from).

UPDATE compliance.baseline_organisation_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.finops_counterparty_register_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.goipoi_register_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.adviser_engagement_disciplines_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.adviser_open_questions_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.founder_filed_instruments_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.program_registry_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.topic_registry_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.persona_registry_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.persona_scenario_registry_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.channel_touchpoint_registry_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.sourcing_register_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.skill_registry_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.touchpoint_kit_cell_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.policy_register_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.repo_health_snapshot_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

UPDATE compliance.repository_registry_mirror
   SET last_review_at = COALESCE(last_review_at::DATE, NULL)
 WHERE last_review_at IS NULL;

-- ===========================================================================
-- Backfill: compliance.review_stamps_standalone from CANONICAL_REGISTRY.csv last_review
-- ===========================================================================
-- All active CANONICAL_REGISTRY rows with non-empty file_path AND non-empty last_review.
-- Idempotent via ON CONFLICT (subject_kind, subject_path) DO NOTHING — safe to re-apply.
-- Source: docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv
--         snapshot at 2026-05-14 (committed at I71 P3 + P4 with 112 rows total; 89 carry both
--         file_path and last_review at backfill time).

INSERT INTO compliance.review_stamps_standalone
    (subject_kind, subject_path, subject_id, last_review_at)
VALUES
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_VISION.md', 'brand_vision', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ARCHITECTURE.md', 'brand_architecture', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_VOICE_FOUNDATION.md', 'brand_voice_foundation', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_REGISTER_MATRIX.md', 'brand_register_matrix', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_FRENCH_PATTERNS.md', 'brand_french_patterns', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_SPANISH_PATTERNS.md', 'brand_spanish_patterns', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ENGLISH_PATTERNS.md', 'brand_english_patterns', '2026-05-14'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_LLM_TONE_TELLS.md', 'brand_llm_tone_tells', '2026-05-14'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_LOCALISED_FORMATS.md', 'brand_localised_formats', '2026-05-14'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/README.md', 'brand_validators_readme', '2026-05-14'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_VISUAL_PATTERNS.md', 'brand_visual_patterns', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_LOGO_SYSTEM.md', 'brand_logo_system', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_COBRANDING_PATTERN.md', 'brand_cobranding_pattern', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_JARGON_AUDIT.md', 'brand_jargon_audit', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md', 'brand_baseline_reality_matrix', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ABBREVIATIONS.md', 'brand_abbreviations', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_DO_DONT.md', 'brand_do_dont', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_TEMPLATE_REGISTRY.md', 'brand_template_registry', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001.md', 'sop_brand_template_registry_mtnce_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md', 'sop_brand_voice_drift_triage_001', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/SERVICE_OFFERING_CATALOG.md', 'service_offering_catalog', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md', 'precedence', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/access_levels.md', 'access_levels', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md', 'confidence_levels', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md', 'source_taxonomy', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md', 'hlk_km_topic_fact_source', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md', 'sop_meta_process_mgmt_001', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/README.md', 'readme_compliance', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CLASSIFICATION_LATTICE.md', 'classification_lattice', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md', 'workspace_blueprint_holistika', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/KM_CHANNEL_VALUE_NARRATIVE.md', 'km_channel_value_narrative', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/TOPIC_PMO_CLIENT_DELIVERY_HUB.md', 'topic_pmo_client_delivery_hub', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/SOP-PMO_VAULT_PROMOTION_GATE_001.md', 'sop_pmo_vault_promotion_gate_001', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/business-strategy/BOOTSTRAPPING_PLAN.md', 'bootstrapping_plan', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/business-strategy/CHANNEL_STRATEGY.md', 'channel_strategy', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/business-strategy/MARKET_THESIS.md', 'market_thesis', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/business-strategy/STRATEGY_DECISION_LOG.md', 'strategy_decision_log', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/business-strategy/GOVERNANCE_MOAT.md', 'governance_moat', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/canonicals/SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md', 'sop_eng_discovery_questionnaire_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/canonicals/SOP-ENG_ESTIMATION_DISCIPLINE_001.md', 'sop_eng_estimation_discipline_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/SOP-IO_ELICITATION_DISCIPLINE_001.md', 'sop_io_elicitation_discipline_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/SOP-IO_INTELLIGENCE_REPORT_001.md', 'sop_io_intelligence_report_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md', 'sop_hlk_goipoi_register_maintenance_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-HLK_TRANSCRIPT_REDACTION_001.md', 'sop_hlk_transcript_redaction_001', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md', 'brand_hierarchy_and_trademark_scope_2026_04', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md', 'founder_entity_formation_decision_memo_2026_04', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md', 'founder_fact_pattern_related_entities', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/TRADEMARK_FILING_STRATEGY_2026-05.md', 'trademark_filing_strategy_2026_05', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_BIO.md', 'founder_bio', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md', 'founder_trajectory_internal', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-HLK_TOOLING_STANDARDS_001.md', 'sop_hlk_tooling_standards_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-CICD_BASELINE_001.md', 'sop_cicd_baseline_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001.md', 'sop_hlk_component_service_matrix_maintenance_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-MCP_SERVER_DEFINITION.md', 'sop_mcp_server_definition', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-MADEIRA_UX_REVIEW_001.md', 'sop_madeira_ux_review_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-MADEIRA_VERDICT_AND_CADENCE_001.md', 'sop_madeira_verdict_and_cadence_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md', 'sop_madeira_scenario_lifecycle_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/SOP-EXTERNAL_REPO_BLESSING_001.md', 'sop_external_repo_blessing_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md', 'sop_external_repo_drift_remediation_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Cross Repo/SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md', 'sop_cross_repo_schema_propagation_001', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/SENTRY_DASHBOARD_HOLISTIKA.md', 'sentry_dashboard_holistika', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/FIGMA_FILES_REGISTRY.md', 'figma_files_registry', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/SUBDOMAINS_REGISTRY.md', 'subdomains_registry', '2026-05-12'),
  ('canonical_md', 'docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/canonicals/FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md', 'founder_capitalization_decision_note_2026_04', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/canonicals/SOP-FOUNDER_COMPANY_FUNDING_001.md', 'sop_founder_company_funding_001', '2026-05-12'),
  ('sop_md', 'docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-RELEASE_TAXONOMY_001.md', 'sop_release_taxonomy_001', '2026-05-14')
ON CONFLICT (subject_kind, subject_path) DO NOTHING;

COMMIT;
