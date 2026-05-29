-- I80 / I86 class-enum extension for compliance.people_design_pattern_registry_mirror.
-- Prod-resync failure (2026-05-29):
--   people_design_pattern_mirror_class_chk rejects `documentation_layering`.
--
-- Cross-references:
--   docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv
--   akos/hlk_design_pattern_csv.py VALID_PATTERN_CLASSES
--   supabase/migrations/20260516000000_i79_compliance_design_pattern_registry_mirror.sql

ALTER TABLE compliance.people_design_pattern_registry_mirror
  DROP CONSTRAINT IF EXISTS people_design_pattern_mirror_class_chk;

ALTER TABLE compliance.people_design_pattern_registry_mirror
  ADD CONSTRAINT people_design_pattern_mirror_class_chk
  CHECK (
    pattern_class IN (
      'register_dimension',
      'paired_sop_runbook',
      'lifecycle_taxonomy',
      'cross_area_propagation',
      'classification_lattice',
      'dual_register',
      'drift_gate',
      'inline_ratify',
      'forward_layout',
      'adapter',
      'documentation_layering',
      'inter_wave_regression_cadence',
      'quality_fabric_specialty_canonical',
      'index_integrity_cadence',
      'output_architecture_hierarchy'
    )
  );

