-- Initiative 32 P4 — compliance.policy_register_mirror
-- D-IH-32-Q4: scope is RLS + service_role rotation + redaction + pii_scope.
-- Same governance pattern as compliance.skill_registry_mirror.

CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'HLK git-backed projections; SSOT remains docs/references/hlk/compliance/*.csv';

CREATE TABLE IF NOT EXISTS compliance.policy_register_mirror (
  policy_id            TEXT NOT NULL,
  policy_class         TEXT NOT NULL,
  applies_to_schema    TEXT NOT NULL,
  applies_to_table     TEXT NOT NULL,
  policy_text          TEXT,
  cadence              TEXT,
  owner_role           TEXT,
  last_review          DATE,
  next_review          DATE,
  topic_ids            TEXT,    -- semicolon-list TEXT
  notes                TEXT,
  source_git_sha       TEXT NOT NULL,
  synced_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (policy_id)
);

COMMENT ON TABLE compliance.policy_register_mirror IS
  'Initiative 32 P4 — projection of POLICY_REGISTER.csv (RLS rules, service_role rotation cadences, redaction policies, PII scope). SSOT is the git CSV.';

CREATE INDEX IF NOT EXISTS policy_register_mirror_synced_at_idx
  ON compliance.policy_register_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS policy_register_mirror_class_idx
  ON compliance.policy_register_mirror (policy_class);
CREATE INDEX IF NOT EXISTS policy_register_mirror_schema_idx
  ON compliance.policy_register_mirror (applies_to_schema);
CREATE INDEX IF NOT EXISTS policy_register_mirror_next_review_idx
  ON compliance.policy_register_mirror (next_review)
  WHERE cadence IN ('quarterly', 'annual');

ALTER TABLE compliance.policy_register_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS policy_register_mirror_deny_authenticated ON compliance.policy_register_mirror;
DROP POLICY IF EXISTS policy_register_mirror_deny_anon ON compliance.policy_register_mirror;
CREATE POLICY policy_register_mirror_deny_authenticated
  ON compliance.policy_register_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY policy_register_mirror_deny_anon
  ON compliance.policy_register_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.policy_register_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.policy_register_mirror TO service_role;
