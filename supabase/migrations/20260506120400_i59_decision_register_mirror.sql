-- Initiative 59 P1.5 — compliance.decision_register_mirror
-- D-IH-59-E: DECISION_REGISTER folded into I59 (vs I60 deferral) so
-- INITIATIVE_REGISTRY.inception_decision_id and closure_decision_id can be
-- real FKs (not strings ALTER TABLE'd later).
-- D-IH-59-B: Per-initiative decision-log.md stays canonical for prose; this
-- CSV is canonical for queryable metadata + cross-references as real FKs.

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.decision_register_mirror (
  decision_id                  TEXT NOT NULL,
  title                        TEXT NOT NULL,
  initiating_initiative_id     TEXT NOT NULL,
  linked_initiative_ids        TEXT,    -- semicolon-list FK to INITIATIVE_REGISTRY
  linked_ops_action_ids        TEXT,    -- semicolon-list FK to OPS_REGISTER
  linked_policies              TEXT,    -- semicolon-list FK to POLICY_REGISTER
  linked_topic_ids             TEXT,    -- semicolon-list FK to TOPIC_REGISTRY
  decision_class               TEXT NOT NULL CHECK (
    decision_class IN ('architecture', 'governance', 'scope', 'execution', 'closure')
  ),
  status                       TEXT NOT NULL CHECK (status IN ('active', 'superseded', 'retired')),
  reversibility                TEXT NOT NULL CHECK (reversibility IN ('high', 'medium', 'low')),
  decided_at                   DATE NOT NULL,
  decision_log_path             TEXT,
  supersedes_decision_id       TEXT,
  summary                      TEXT,
  notes                        TEXT,
  source_git_sha               TEXT NOT NULL,
  synced_at                    TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (decision_id)
);

COMMENT ON TABLE compliance.decision_register_mirror IS
  'Initiative 59 P1.5 — projection of DECISION_REGISTER.csv. Per-initiative decision-log.md stays canonical for prose (D-IH-59-B).';

CREATE INDEX IF NOT EXISTS decision_register_mirror_synced_at_idx
  ON compliance.decision_register_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS decision_register_mirror_initiating_idx
  ON compliance.decision_register_mirror (initiating_initiative_id);
CREATE INDEX IF NOT EXISTS decision_register_mirror_decision_class_idx
  ON compliance.decision_register_mirror (decision_class);
CREATE INDEX IF NOT EXISTS decision_register_mirror_status_idx
  ON compliance.decision_register_mirror (status);
CREATE INDEX IF NOT EXISTS decision_register_mirror_decided_at_idx
  ON compliance.decision_register_mirror (decided_at DESC);

ALTER TABLE compliance.decision_register_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS decision_register_mirror_deny_authenticated ON compliance.decision_register_mirror;
DROP POLICY IF EXISTS decision_register_mirror_deny_anon ON compliance.decision_register_mirror;
CREATE POLICY decision_register_mirror_deny_authenticated
  ON compliance.decision_register_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY decision_register_mirror_deny_anon
  ON compliance.decision_register_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.decision_register_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.decision_register_mirror TO service_role;
