-- Initiative 73 P1 — compliance.engagement_model_registry_mirror
-- Mirrors the canonical ENGAGEMENT_MODEL_REGISTRY.csv (16 columns + bookkeeping).
-- SSOT remains docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv.
-- Same governance pattern as compliance.engagement_registry_mirror (I70 P8.1):
--   deny-by-default RLS; service_role only; CHECK constraints on enums; companion governance view.
-- Decision lineage: D-IH-73-C (sibling-dimension placement); D-IH-73-D (7-class taxonomy);
-- D-IH-73-E (outsourced_helper separate SOC class); D-IH-73-H..M (per-class enum ratifications).

CREATE SCHEMA IF NOT EXISTS compliance;
CREATE SCHEMA IF NOT EXISTS governance;

CREATE TABLE IF NOT EXISTS compliance.engagement_model_registry_mirror (
  engagement_model_id     TEXT NOT NULL,
  engagement_model_name   TEXT NOT NULL,
  retribution_pattern     TEXT NOT NULL,
  retribution_unit        TEXT NOT NULL,
  typical_duration        TEXT NOT NULL,
  access_level_default    SMALLINT NOT NULL,
  soc_posture             TEXT NOT NULL,
  ip_clause_class         TEXT NOT NULL,
  knowledge_access_level  TEXT NOT NULL,
  onboarding_pattern      TEXT NOT NULL,
  offboarding_pattern     TEXT NOT NULL,
  payment_cadence         TEXT NOT NULL,
  legal_template_default  TEXT NOT NULL,
  historical_examples     TEXT,
  status                  TEXT NOT NULL,
  notes                   TEXT,
  source_git_sha          TEXT NOT NULL,
  synced_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (engagement_model_id),
  CONSTRAINT engagement_model_mirror_id_chk
    CHECK (engagement_model_id ~ '^eng_model_[a-z0-9_]+$'),
  CONSTRAINT engagement_model_mirror_retribution_pattern_chk
    CHECK (retribution_pattern IN (
      'hourly',
      'milestone',
      'percentage',
      'barter_for_training',
      'equity_advisor',
      'hourly_low_trust',
      'operator_self'
    )),
  CONSTRAINT engagement_model_mirror_soc_posture_chk
    CHECK (soc_posture IN (
      'standard',
      'cleared',
      'low_trust',
      'training_only',
      'internal'
    )),
  CONSTRAINT engagement_model_mirror_ip_clause_chk
    CHECK (ip_clause_class IN (
      'standard_consultant',
      'milestone_handoff',
      'collaborator_share',
      'training_recipient',
      'advisor_nda',
      'outsourced_workproduct_only',
      'operator_owns_all'
    )),
  CONSTRAINT engagement_model_mirror_knowledge_access_chk
    CHECK (knowledge_access_level IN (
      'full_by_engagement',
      'partial_by_engagement',
      'training_curriculum_only',
      'work_product_scope_only',
      'full_internal'
    )),
  CONSTRAINT engagement_model_mirror_payment_cadence_chk
    CHECK (payment_cadence IN (
      'per_hour',
      'per_milestone',
      'per_deal_outcome',
      'barter_continuous',
      'per_round',
      'per_hour_capped',
      'none'
    )),
  CONSTRAINT engagement_model_mirror_access_level_chk
    CHECK (access_level_default BETWEEN 0 AND 6),
  CONSTRAINT engagement_model_mirror_status_chk
    CHECK (status IN ('active', 'deprecated', 'planned'))
);

COMMENT ON TABLE compliance.engagement_model_registry_mirror IS
  'Initiative 73 P1 — projection of ENGAGEMENT_MODEL_REGISTRY.csv (7-class engagement-model taxonomy: retribution + SOC + IP + knowledge-access posture). SSOT is the git CSV at docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/. Sibling to compliance.engagement_registry_mirror per D-IH-73-C.';

CREATE INDEX IF NOT EXISTS engagement_model_mirror_status_idx
  ON compliance.engagement_model_registry_mirror (status);
CREATE INDEX IF NOT EXISTS engagement_model_mirror_retribution_idx
  ON compliance.engagement_model_registry_mirror (retribution_pattern);
CREATE INDEX IF NOT EXISTS engagement_model_mirror_soc_posture_idx
  ON compliance.engagement_model_registry_mirror (soc_posture);
CREATE INDEX IF NOT EXISTS engagement_model_mirror_access_level_idx
  ON compliance.engagement_model_registry_mirror (access_level_default);
CREATE INDEX IF NOT EXISTS engagement_model_mirror_synced_at_idx
  ON compliance.engagement_model_registry_mirror (synced_at DESC);

ALTER TABLE compliance.engagement_model_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS engagement_model_mirror_deny_authenticated
  ON compliance.engagement_model_registry_mirror;
DROP POLICY IF EXISTS engagement_model_mirror_deny_anon
  ON compliance.engagement_model_registry_mirror;
CREATE POLICY engagement_model_mirror_deny_authenticated
  ON compliance.engagement_model_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY engagement_model_mirror_deny_anon
  ON compliance.engagement_model_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.engagement_model_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.engagement_model_registry_mirror TO service_role;

-- Operator-facing view (filters status=active for P7 KB-views consumption).
CREATE OR REPLACE VIEW governance.engagement_model_registry_view AS
SELECT
  engagement_model_id,
  engagement_model_name,
  retribution_pattern,
  retribution_unit,
  typical_duration,
  access_level_default,
  soc_posture,
  ip_clause_class,
  knowledge_access_level,
  onboarding_pattern,
  offboarding_pattern,
  payment_cadence,
  legal_template_default,
  historical_examples,
  status,
  notes,
  synced_at
FROM compliance.engagement_model_registry_mirror
WHERE status = 'active';

COMMENT ON VIEW governance.engagement_model_registry_view IS
  'Initiative 73 P1 — operator-facing engagement-model taxonomy view (status=active only). Consumed by P7 hlk-erp KB-view panel filter routes (operator-managed / cleared-collaborator / low-trust-outsourced / apprentice).';
