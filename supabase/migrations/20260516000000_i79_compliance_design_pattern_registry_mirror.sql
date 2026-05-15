-- Initiative 79 P2 - compliance.people_design_pattern_registry_mirror
-- Mirrors the canonical PEOPLE_DESIGN_PATTERN_REGISTRY.csv (15 columns + bookkeeping).
-- SSOT remains docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv.
-- Same governance pattern as compliance.engagement_model_registry_mirror (I73 P1):
--   deny-by-default RLS; service_role only; CHECK constraints on enums; companion governance view.
-- Decision lineage: D-IH-79-A (mega scope); D-IH-79-C (pattern library shape: CSV + MD paired);
-- D-IH-79-D (CSV registry home); D-IH-79-E (process_list 8th column FK target); D-IH-79-N (anti-jargon drift gate).

CREATE SCHEMA IF NOT EXISTS compliance;
CREATE SCHEMA IF NOT EXISTS governance;

CREATE TABLE IF NOT EXISTS compliance.people_design_pattern_registry_mirror (
  pattern_id                       TEXT NOT NULL,
  pattern_name                     TEXT NOT NULL,
  pattern_class                    TEXT NOT NULL,
  discipline_origin                TEXT NOT NULL,
  consumer_areas                   TEXT NOT NULL,
  ratifying_decision_id            TEXT NOT NULL,
  originating_initiative_id        TEXT NOT NULL,
  pattern_md_anchor                TEXT NOT NULL,
  canonical_artifact_path          TEXT NOT NULL,
  acceptance_criteria_human        TEXT NOT NULL,
  acceptance_criteria_automation   TEXT NOT NULL,
  status                           TEXT NOT NULL,
  last_review                      DATE NOT NULL,
  last_review_by                   TEXT NOT NULL,
  notes                            TEXT,
  source_git_sha                   TEXT NOT NULL,
  synced_at                        TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (pattern_id),
  CONSTRAINT people_design_pattern_mirror_id_chk
    CHECK (pattern_id ~ '^pattern_[a-z0-9_]+$'),
  CONSTRAINT people_design_pattern_mirror_class_chk
    CHECK (pattern_class IN (
      'register_dimension',
      'paired_sop_runbook',
      'lifecycle_taxonomy',
      'cross_area_propagation',
      'classification_lattice',
      'dual_register',
      'drift_gate',
      'inline_ratify',
      'forward_layout',
      'adapter'
    )),
  CONSTRAINT people_design_pattern_mirror_discipline_chk
    CHECK (discipline_origin IN (
      'compliance',
      'ethics',
      'learning',
      'people_operations',
      'cross_people'
    )),
  CONSTRAINT people_design_pattern_mirror_status_chk
    CHECK (status IN ('active', 'inactive', 'planned', 'deprecated', 'experimental')),
  CONSTRAINT people_design_pattern_mirror_decision_fk_chk
    CHECK (ratifying_decision_id ~ '^D-IH-\d+-[A-Z0-9_]+$'),
  CONSTRAINT people_design_pattern_mirror_initiative_fk_chk
    CHECK (originating_initiative_id ~ '^INIT-OPENCLAW_AKOS-\d+$'),
  CONSTRAINT people_design_pattern_mirror_anchor_chk
    CHECK (pattern_md_anchor ~ '^#pattern-[a-z0-9-]+$')
);

COMMENT ON TABLE compliance.people_design_pattern_registry_mirror IS
  'Initiative 79 P2 - projection of PEOPLE_DESIGN_PATTERN_REGISTRY.csv (cross-area design pattern library; the consulting design patterns People mints for other areas to inherit). SSOT is the git CSV at docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/. Paired Markdown narrative at PEOPLE_DESIGN_PATTERN_LIBRARY.md (anchors are the join key). Per D-IH-79-A/C/D/E.';

CREATE INDEX IF NOT EXISTS people_design_pattern_mirror_status_idx
  ON compliance.people_design_pattern_registry_mirror (status);
CREATE INDEX IF NOT EXISTS people_design_pattern_mirror_class_idx
  ON compliance.people_design_pattern_registry_mirror (pattern_class);
CREATE INDEX IF NOT EXISTS people_design_pattern_mirror_discipline_idx
  ON compliance.people_design_pattern_registry_mirror (discipline_origin);
CREATE INDEX IF NOT EXISTS people_design_pattern_mirror_initiative_idx
  ON compliance.people_design_pattern_registry_mirror (originating_initiative_id);
CREATE INDEX IF NOT EXISTS people_design_pattern_mirror_synced_at_idx
  ON compliance.people_design_pattern_registry_mirror (synced_at DESC);

ALTER TABLE compliance.people_design_pattern_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS people_design_pattern_mirror_deny_authenticated
  ON compliance.people_design_pattern_registry_mirror;
DROP POLICY IF EXISTS people_design_pattern_mirror_deny_anon
  ON compliance.people_design_pattern_registry_mirror;
CREATE POLICY people_design_pattern_mirror_deny_authenticated
  ON compliance.people_design_pattern_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY people_design_pattern_mirror_deny_anon
  ON compliance.people_design_pattern_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.people_design_pattern_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.people_design_pattern_registry_mirror TO service_role;

-- Operator-facing view (filters status=active for cross-area consumer queries).
CREATE OR REPLACE VIEW governance.people_design_pattern_registry_view AS
SELECT
  pattern_id,
  pattern_name,
  pattern_class,
  discipline_origin,
  consumer_areas,
  ratifying_decision_id,
  originating_initiative_id,
  pattern_md_anchor,
  canonical_artifact_path,
  acceptance_criteria_human,
  acceptance_criteria_automation,
  status,
  last_review,
  last_review_by,
  notes,
  synced_at
FROM compliance.people_design_pattern_registry_mirror
WHERE status = 'active';

COMMENT ON VIEW governance.people_design_pattern_registry_view IS
  'Initiative 79 P2 - operator-facing design pattern library view (status=active only). Consumed by consuming areas resolving inherited_pattern_id FK on process_list.csv (P6 schema extension per D-IH-79-E).';
