-- I95 DATA-08: extend people_design_pattern_registry_mirror.pattern_class CHECK to match
-- Pydantic VALID_PATTERN_CLASSES (I93 area_governance + I88 intent_ranked_regression_cadence).
-- Without this, mirror-sync apply fails mid-stream despite validate_hlk PASS (two-plane drift).

ALTER TABLE compliance.people_design_pattern_registry_mirror
  DROP CONSTRAINT IF EXISTS people_design_pattern_mirror_class_chk;

ALTER TABLE compliance.people_design_pattern_registry_mirror
  ADD CONSTRAINT people_design_pattern_mirror_class_chk
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
    'adapter',
    'documentation_layering',
    'output_architecture_hierarchy',
    'inter_wave_regression_cadence',
    'index_integrity_cadence',
    'quality_fabric_specialty_canonical',
    'area_governance',
    'intent_ranked_regression_cadence'
  ));
