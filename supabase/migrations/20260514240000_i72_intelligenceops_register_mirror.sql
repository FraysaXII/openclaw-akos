-- Initiative 72 P6 — INTELLIGENCEOPS_REGISTER mirror table
-- D-IH-72-H: sibling canonical CSV (NOT GOI_POI col-extension).
-- D-IH-72-I: regulator-relationship roadmap = generic SOP + ENISA worked example.
-- D-IH-72-J: media-counterparty-onboarding = Storytelling charter cross-link + register row.
-- D-IH-72-K: recruiter onboarding = register row + I73 People Operations onboarding SOP.
--
-- Cross-references:
--   docs/references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv
--   akos/hlk_intelligenceops_register_csv.py (Pydantic-style SSOT)
--   scripts/validate_intelligenceops_register.py (validator)
--   scripts/validate_hlk.py (aggregate dispatcher integration)

CREATE TABLE IF NOT EXISTS compliance.intelligenceops_register_mirror (
    register_id                       TEXT PRIMARY KEY,
    target_id                         TEXT,                  -- FK-by-convention to compliance.goi_poi_register_mirror.ref_id; nullable + TODO[OPERATOR-...] markers allowed
    target_class                      TEXT NOT NULL,         -- enum competitor_intelligence_target | regulator | media | recruiter
    cadence                           TEXT NOT NULL,         -- enum on_demand | scheduled | event_triggered | gated_operator (per D-IH-72-Q)
    source_type                       TEXT NOT NULL,         -- enum HUMINT | OSINT | TECHINT | hybrid (per HUMINT FM 2-22.3)
    reliability                       TEXT NOT NULL,         -- enum A | B | C | D | E (HUMINT FM 2-22.3 reliability rating)
    output_artifact                   TEXT,
    responsible_role                  TEXT NOT NULL,         -- FK-by-convention to compliance.baseline_organisation_mirror.role_name
    lifecycle_status                  TEXT NOT NULL,         -- enum active | scaffold | deprecated
    intro_decision_id                 TEXT,                  -- FK-by-convention to compliance.decision_register_mirror.decision_id
    linked_sop_path                   TEXT,
    linked_runbook_path               TEXT,
    notes                             TEXT,
    last_review_at                    DATE,
    last_review_by                    TEXT,
    last_review_decision_id           TEXT,
    methodology_version_at_review     TEXT
);

COMMENT ON TABLE compliance.intelligenceops_register_mirror IS
  'D-IH-72-H: Sibling canonical to GOI_POI_REGISTER. Captures the operational contract for systematic intelligence collection (cadence + source type + reliability + output artifact + responsible role) against named identity-side targets. Mirrors INTELLIGENCEOPS_REGISTER.csv at docs/references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/dimensions/.';
COMMENT ON COLUMN compliance.intelligenceops_register_mirror.target_class IS
  'D-IH-72-H: enum target class. competitor_intelligence_target | regulator | media | recruiter — seeded from D-IH-70-AC GOI/POI hunt enum extension.';
COMMENT ON COLUMN compliance.intelligenceops_register_mirror.reliability IS
  'D-IH-72-H: HUMINT FM 2-22.3 §B-2 source-reliability rating. A (completely reliable) through E (unreliable). C is the default for unknown sources.';
COMMENT ON COLUMN compliance.intelligenceops_register_mirror.source_type IS
  'D-IH-72-H: HUMINT FM 2-22.3 source typology. HUMINT (interviews/conversations) | OSINT (public web/registries/journalism) | TECHINT (code/infra/telemetry) | hybrid.';
COMMENT ON COLUMN compliance.intelligenceops_register_mirror.cadence IS
  'D-IH-72-Q + D-IH-72-H: cadence taxonomy. on_demand | scheduled | event_triggered | gated_operator.';

CREATE INDEX IF NOT EXISTS intelligenceops_register_mirror_target_class_idx
  ON compliance.intelligenceops_register_mirror (target_class);
CREATE INDEX IF NOT EXISTS intelligenceops_register_mirror_lifecycle_status_idx
  ON compliance.intelligenceops_register_mirror (lifecycle_status);
CREATE INDEX IF NOT EXISTS intelligenceops_register_mirror_responsible_role_idx
  ON compliance.intelligenceops_register_mirror (responsible_role);
CREATE INDEX IF NOT EXISTS intelligenceops_register_mirror_target_id_idx
  ON compliance.intelligenceops_register_mirror (target_id);

ALTER TABLE compliance.intelligenceops_register_mirror ENABLE ROW LEVEL SECURITY;

CREATE POLICY intelligenceops_register_mirror_read
  ON compliance.intelligenceops_register_mirror
  FOR SELECT
  USING (true);

COMMENT ON POLICY intelligenceops_register_mirror_read ON compliance.intelligenceops_register_mirror IS
  'D-IH-72-H: read-only mirror. Writes happen via compliance_mirror_emit Edge Function (CSV-as-SSOT pattern per akos-governance-remediation.mdc).';
