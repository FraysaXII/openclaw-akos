-- Initiative 72 P2 — compliance.engagement_template_registry_mirror
-- D-IH-72-F: Engagement template registry as sibling canonical (NOT column-extension on
-- ENGAGEMENT_REGISTRY). D-IH-72-Y: source CSV at Operations/RevOps/canonicals/dimensions/.
-- Same governance pattern as compliance.skill_registry_mirror (Initiative 32 P2).

CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'HLK git-backed projections; SSOT remains docs/references/hlk/v3.0/Admin/O5-1/.../canonicals/*.csv';

CREATE TABLE IF NOT EXISTS compliance.engagement_template_registry_mirror (
  template_id                    TEXT NOT NULL,
  name                           TEXT,
  engagement_class               TEXT,
  owner_role                     TEXT,
  discipline_mix                 TEXT,    -- semicolon-list TEXT (DAMA-pure projection of CSV)
  duration_target_days           INTEGER,
  value_band_eur                 TEXT,
  billing_cadence                TEXT,
  contract_kind                  TEXT,
  counterparty_class             TEXT,
  artifact_path_pattern          TEXT,
  supabase_mirror                TEXT,
  panel_slot                     TEXT,
  lifecycle_status               TEXT,
  promotion_decision_id          TEXT,
  ssot_path                      TEXT,
  version                        TEXT,
  notes                          TEXT,
  last_review_at                 DATE,
  last_review_by                 TEXT,
  last_review_decision_id        TEXT,
  methodology_version_at_review  TEXT,
  source_git_sha                 TEXT NOT NULL,
  synced_at                      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (template_id)
);

COMMENT ON TABLE compliance.engagement_template_registry_mirror IS
  'Initiative 72 P2 — projection of ENGAGEMENT_TEMPLATE_REGISTRY.csv. SSOT is the git CSV at Operations/RevOps/canonicals/dimensions/.';
COMMENT ON COLUMN compliance.engagement_template_registry_mirror.lifecycle_status IS
  'scaffold (authored, awaiting promotion) | active (promoted via SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md) | deprecated (retired).';
COMMENT ON COLUMN compliance.engagement_template_registry_mirror.promotion_decision_id IS
  'D-IH-72-F: scaffold templates carry the bootstrap charter decision id (D-IH-72-F); promoted templates carry the per-template promotion decision (minted via P3 SOP).';

CREATE INDEX IF NOT EXISTS engagement_template_registry_mirror_synced_at_idx
  ON compliance.engagement_template_registry_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS engagement_template_registry_mirror_lifecycle_idx
  ON compliance.engagement_template_registry_mirror (lifecycle_status);
CREATE INDEX IF NOT EXISTS engagement_template_registry_mirror_owner_role_idx
  ON compliance.engagement_template_registry_mirror (owner_role);
CREATE INDEX IF NOT EXISTS engagement_template_registry_mirror_engagement_class_idx
  ON compliance.engagement_template_registry_mirror (engagement_class);
CREATE INDEX IF NOT EXISTS engagement_template_registry_mirror_value_band_idx
  ON compliance.engagement_template_registry_mirror (value_band_eur);

ALTER TABLE compliance.engagement_template_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS engagement_template_registry_mirror_deny_authenticated ON compliance.engagement_template_registry_mirror;
DROP POLICY IF EXISTS engagement_template_registry_mirror_deny_anon ON compliance.engagement_template_registry_mirror;
CREATE POLICY engagement_template_registry_mirror_deny_authenticated
  ON compliance.engagement_template_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY engagement_template_registry_mirror_deny_anon
  ON compliance.engagement_template_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.engagement_template_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.engagement_template_registry_mirror TO service_role;
