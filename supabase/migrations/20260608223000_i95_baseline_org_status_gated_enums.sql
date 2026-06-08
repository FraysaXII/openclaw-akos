-- I95 DATA-08: extend baseline_organisation_mirror.status CHECK for I72 gated roles.
-- RevOps Manager/Analyst use gated_operator; CRO uses gated_ahead_of_executive_activation.
-- Preflight (validate_mirror_enum_parity.py) failed apply until this lands on live DB.

ALTER TABLE compliance.baseline_organisation_mirror
  DROP CONSTRAINT IF EXISTS baseline_organisation_mirror_status_check;

ALTER TABLE compliance.baseline_organisation_mirror
  ADD CONSTRAINT baseline_organisation_mirror_status_check
  CHECK (
    status IS NULL
    OR status = ''
    OR status IN (
      'active',
      'deprecated',
      'pending',
      'planned',
      'gated_operator',
      'gated_ahead_of_executive_activation'
    )
  );

COMMENT ON COLUMN compliance.baseline_organisation_mirror.status IS
  'Soft-state: active | deprecated | pending | planned | gated_operator | gated_ahead_of_executive_activation. NULL/empty allowed for legacy rows.';
