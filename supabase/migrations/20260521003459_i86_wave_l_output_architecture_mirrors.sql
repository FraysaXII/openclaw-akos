-- Initiative 86 Wave L (D-IH-86-BG, 2026-05-21) - 4-layer output architecture mirrors.
-- Mirrors the 3 canonical CSVs minted at Wave K (D-IH-86-BB) below the 5-axis Quality Fabric:
--   Layer 1 - OUTPUT_TYPE_REGISTRY.csv          (medium / shape)
--   Layer 2 - ARTIFACT_CLASS_REGISTRY.csv       (named purpose)
--   Layer 3 - COMPONENT_PRIMITIVE_REGISTRY.csv  (Shadcn-shape granular primitives)
-- SSOT remains the git CSVs at
-- docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/.
--
-- Same governance pattern as compliance.people_design_pattern_registry_mirror (I79 P2):
--   deny-by-default RLS; service_role only; CHECK constraints on enums; companion governance views.
--
-- Decision lineage:
--   D-IH-86-BB (Wave K - 4-layer architecture mint).
--   D-IH-86-BG (Wave L - Pydantic + composite validator + Supabase mirrors; this migration).

CREATE SCHEMA IF NOT EXISTS compliance;
CREATE SCHEMA IF NOT EXISTS governance;

-- ===================================================================================
-- Layer 1 - OUTPUT_TYPE_REGISTRY mirror
-- ===================================================================================

CREATE TABLE IF NOT EXISTS compliance.output_type_registry_mirror (
  output_type_code               TEXT NOT NULL,
  name                           TEXT NOT NULL,
  medium_class                   TEXT NOT NULL,
  render_targets                 TEXT NOT NULL,
  authoring_tool                 TEXT NOT NULL,
  accessibility_concerns         TEXT NOT NULL,
  brand_visual_anchor            TEXT NOT NULL,
  status                         TEXT NOT NULL,
  added_at                       DATE NOT NULL,
  last_review_at                 DATE NOT NULL,
  last_review_by                 TEXT NOT NULL,
  last_review_decision_id        TEXT NOT NULL,
  methodology_version_at_review  TEXT NOT NULL,
  notes                          TEXT,
  source_git_sha                 TEXT NOT NULL,
  synced_at                      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (output_type_code),
  CONSTRAINT output_type_mirror_code_chk
    CHECK (output_type_code ~ '^OT-[A-Z0-9][A-Z0-9-]+$'),
  CONSTRAINT output_type_mirror_medium_chk
    CHECK (medium_class IN ('text', 'visual', 'multimedia', 'interactive', 'document')),
  CONSTRAINT output_type_mirror_status_chk
    CHECK (status IN ('active', 'inactive', 'planned', 'deprecated', 'experimental')),
  CONSTRAINT output_type_mirror_decision_fk_chk
    CHECK (last_review_decision_id ~ '^D-IH-\d+-[A-Z0-9_]+$'),
  CONSTRAINT output_type_mirror_methodology_chk
    CHECK (methodology_version_at_review ~ '^v\d+\.\d+$')
);

COMMENT ON TABLE compliance.output_type_registry_mirror IS
  'I86 Wave L (D-IH-86-BG) - projection of OUTPUT_TYPE_REGISTRY.csv (Layer 1 of the 4-layer output architecture beneath the 5-axis Quality Fabric). Names the medium / shape of every output Holistika emits. SSOT is the git CSV at docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/.';

CREATE INDEX IF NOT EXISTS output_type_mirror_status_idx
  ON compliance.output_type_registry_mirror (status);
CREATE INDEX IF NOT EXISTS output_type_mirror_medium_idx
  ON compliance.output_type_registry_mirror (medium_class);
CREATE INDEX IF NOT EXISTS output_type_mirror_synced_at_idx
  ON compliance.output_type_registry_mirror (synced_at DESC);

ALTER TABLE compliance.output_type_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS output_type_mirror_deny_authenticated
  ON compliance.output_type_registry_mirror;
DROP POLICY IF EXISTS output_type_mirror_deny_anon
  ON compliance.output_type_registry_mirror;
CREATE POLICY output_type_mirror_deny_authenticated
  ON compliance.output_type_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY output_type_mirror_deny_anon
  ON compliance.output_type_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.output_type_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.output_type_registry_mirror TO service_role;

CREATE OR REPLACE VIEW governance.output_type_registry_view AS
SELECT
  output_type_code,
  name,
  medium_class,
  render_targets,
  authoring_tool,
  accessibility_concerns,
  brand_visual_anchor,
  status,
  added_at,
  last_review_at,
  last_review_by,
  last_review_decision_id,
  methodology_version_at_review,
  notes,
  synced_at
FROM compliance.output_type_registry_mirror
WHERE status = 'active';

COMMENT ON VIEW governance.output_type_registry_view IS
  'I86 Wave L (D-IH-86-BG) - operator-facing OUTPUT_TYPE_REGISTRY view (status=active only). Forward-charter: HLK-ERP planning panel /planning/registries/output-architecture/output-types reads this view (Wave M / I-NN-OUTPUT-ARCHITECTURE).';

-- ===================================================================================
-- Layer 2 - ARTIFACT_CLASS_REGISTRY mirror
-- ===================================================================================

CREATE TABLE IF NOT EXISTS compliance.artifact_class_registry_mirror (
  artifact_class_code            TEXT NOT NULL,
  name                           TEXT NOT NULL,
  output_type_codes              TEXT NOT NULL,
  typical_audience_codes         TEXT NOT NULL,
  typical_channel_codes          TEXT NOT NULL,
  render_script_path             TEXT,
  exemplar_path                  TEXT,
  doctrine_owner_role            TEXT NOT NULL,
  quality_fabric_invocation      TEXT NOT NULL,
  status                         TEXT NOT NULL,
  added_at                       DATE NOT NULL,
  last_review_at                 DATE NOT NULL,
  last_review_by                 TEXT NOT NULL,
  last_review_decision_id        TEXT NOT NULL,
  methodology_version_at_review  TEXT NOT NULL,
  notes                          TEXT,
  source_git_sha                 TEXT NOT NULL,
  synced_at                      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (artifact_class_code),
  CONSTRAINT artifact_class_mirror_code_chk
    CHECK (artifact_class_code ~ '^AC-[A-Z0-9][A-Z0-9-]+$'),
  CONSTRAINT artifact_class_mirror_status_chk
    CHECK (status IN ('active', 'inactive', 'planned', 'deprecated', 'experimental')),
  CONSTRAINT artifact_class_mirror_decision_fk_chk
    CHECK (last_review_decision_id ~ '^D-IH-\d+-[A-Z0-9_]+$'),
  CONSTRAINT artifact_class_mirror_methodology_chk
    CHECK (methodology_version_at_review ~ '^v\d+\.\d+$')
);

COMMENT ON TABLE compliance.artifact_class_registry_mirror IS
  'I86 Wave L (D-IH-86-BG) - projection of ARTIFACT_CLASS_REGISTRY.csv (Layer 2 of the 4-layer output architecture beneath the 5-axis Quality Fabric). Names the named purpose of every output Holistika emits (dossier / cover-email / intro-message / decks / UAT-report / SOP / etc).';

CREATE INDEX IF NOT EXISTS artifact_class_mirror_status_idx
  ON compliance.artifact_class_registry_mirror (status);
CREATE INDEX IF NOT EXISTS artifact_class_mirror_owner_idx
  ON compliance.artifact_class_registry_mirror (doctrine_owner_role);
CREATE INDEX IF NOT EXISTS artifact_class_mirror_synced_at_idx
  ON compliance.artifact_class_registry_mirror (synced_at DESC);

ALTER TABLE compliance.artifact_class_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS artifact_class_mirror_deny_authenticated
  ON compliance.artifact_class_registry_mirror;
DROP POLICY IF EXISTS artifact_class_mirror_deny_anon
  ON compliance.artifact_class_registry_mirror;
CREATE POLICY artifact_class_mirror_deny_authenticated
  ON compliance.artifact_class_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY artifact_class_mirror_deny_anon
  ON compliance.artifact_class_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.artifact_class_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.artifact_class_registry_mirror TO service_role;

CREATE OR REPLACE VIEW governance.artifact_class_registry_view AS
SELECT
  artifact_class_code,
  name,
  output_type_codes,
  typical_audience_codes,
  typical_channel_codes,
  render_script_path,
  exemplar_path,
  doctrine_owner_role,
  quality_fabric_invocation,
  status,
  added_at,
  last_review_at,
  last_review_by,
  last_review_decision_id,
  methodology_version_at_review,
  notes,
  synced_at
FROM compliance.artifact_class_registry_mirror
WHERE status = 'active';

COMMENT ON VIEW governance.artifact_class_registry_view IS
  'I86 Wave L (D-IH-86-BG) - operator-facing ARTIFACT_CLASS_REGISTRY view (status=active only). Forward-charter: HLK-ERP planning panel reads this view (Wave M / I-NN-OUTPUT-ARCHITECTURE).';

-- ===================================================================================
-- Layer 3 - COMPONENT_PRIMITIVE_REGISTRY mirror
-- ===================================================================================

CREATE TABLE IF NOT EXISTS compliance.component_primitive_registry_mirror (
  component_primitive_code       TEXT NOT NULL,
  name                           TEXT NOT NULL,
  kind                           TEXT NOT NULL,
  parent_artifact_class_codes    TEXT NOT NULL,
  research_dimensions            TEXT NOT NULL,
  a11y_dimensions                TEXT NOT NULL,
  brand_dimensions               TEXT NOT NULL,
  doctrine_path                  TEXT NOT NULL,
  status                         TEXT NOT NULL,
  added_at                       DATE NOT NULL,
  last_review_at                 DATE NOT NULL,
  last_review_by                 TEXT NOT NULL,
  last_review_decision_id        TEXT NOT NULL,
  methodology_version_at_review  TEXT NOT NULL,
  notes                          TEXT,
  source_git_sha                 TEXT NOT NULL,
  synced_at                      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (component_primitive_code),
  CONSTRAINT component_primitive_mirror_code_chk
    CHECK (component_primitive_code ~ '^CP-[A-Z0-9][A-Z0-9-]+$'),
  CONSTRAINT component_primitive_mirror_status_chk
    CHECK (status IN ('active', 'inactive', 'planned', 'deprecated', 'experimental')),
  CONSTRAINT component_primitive_mirror_decision_fk_chk
    CHECK (last_review_decision_id ~ '^D-IH-\d+-[A-Z0-9_]+$'),
  CONSTRAINT component_primitive_mirror_methodology_chk
    CHECK (methodology_version_at_review ~ '^v\d+\.\d+$')
  -- NOTE: kind is a semicolon-list (e.g., 'prose;visual'); per-token validation
  -- against VALID_KINDS frozenset {'prose','visual','interactive','mixed'} is
  -- enforced at the validator layer (scripts/validate_output_architecture_registries.py),
  -- not at the DB layer, so PostgreSQL CHECK is intentionally absent.
);

COMMENT ON TABLE compliance.component_primitive_registry_mirror IS
  'I86 Wave L (D-IH-86-BG) - projection of COMPONENT_PRIMITIVE_REGISTRY.csv (Layer 3 of the 4-layer output architecture beneath the 5-axis Quality Fabric). Names the Shadcn-shape granular primitives that compose every output (greeting / hook / body / CTA / signature / slide-hero / slide-compare / mermaid-flowchart / data-table / form-field / dashboard-card / etc).';

CREATE INDEX IF NOT EXISTS component_primitive_mirror_status_idx
  ON compliance.component_primitive_registry_mirror (status);
CREATE INDEX IF NOT EXISTS component_primitive_mirror_kind_idx
  ON compliance.component_primitive_registry_mirror (kind);
CREATE INDEX IF NOT EXISTS component_primitive_mirror_synced_at_idx
  ON compliance.component_primitive_registry_mirror (synced_at DESC);

ALTER TABLE compliance.component_primitive_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS component_primitive_mirror_deny_authenticated
  ON compliance.component_primitive_registry_mirror;
DROP POLICY IF EXISTS component_primitive_mirror_deny_anon
  ON compliance.component_primitive_registry_mirror;
CREATE POLICY component_primitive_mirror_deny_authenticated
  ON compliance.component_primitive_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY component_primitive_mirror_deny_anon
  ON compliance.component_primitive_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.component_primitive_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.component_primitive_registry_mirror TO service_role;

CREATE OR REPLACE VIEW governance.component_primitive_registry_view AS
SELECT
  component_primitive_code,
  name,
  kind,
  parent_artifact_class_codes,
  research_dimensions,
  a11y_dimensions,
  brand_dimensions,
  doctrine_path,
  status,
  added_at,
  last_review_at,
  last_review_by,
  last_review_decision_id,
  methodology_version_at_review,
  notes,
  synced_at
FROM compliance.component_primitive_registry_mirror
WHERE status = 'active';

COMMENT ON VIEW governance.component_primitive_registry_view IS
  'I86 Wave L (D-IH-86-BG) - operator-facing COMPONENT_PRIMITIVE_REGISTRY view (status=active only). Forward-charter: HLK-ERP planning panel reads this view; primitive composition surfacing per Wave M / I-NN-OUTPUT-ARCHITECTURE.';
