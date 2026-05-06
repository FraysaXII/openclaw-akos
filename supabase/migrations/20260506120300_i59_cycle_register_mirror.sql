-- Initiative 59 P1.4 — compliance.cycle_register_mirror
-- D-IH-59-A: HLK governance promotion model — five dimensions land atomically.
-- Cycles like I57/I58/I59 coordinate multiple sub-initiatives via FK joins
-- (e.g., I58 coordinated I28/I29/I30/I31). Makes the relationship queryable.

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.cycle_register_mirror (
  cycle_id                          TEXT NOT NULL,
  title                             TEXT NOT NULL,
  coordinating_initiative_id        TEXT NOT NULL,
  coordinated_initiative_ids        TEXT,    -- semicolon-list FK to INITIATIVE_REGISTRY
  status                            TEXT NOT NULL CHECK (status IN ('active', 'closed', 'archived')),
  started_at                        DATE,
  closed_at                         DATE,
  scope_summary                     TEXT,
  verification_matrix_count          INTEGER,
  operator_approval_gates_count      INTEGER,
  linked_topic_ids                  TEXT,
  notes                             TEXT,
  source_git_sha                    TEXT NOT NULL,
  synced_at                         TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (cycle_id)
);

COMMENT ON TABLE compliance.cycle_register_mirror IS
  'Initiative 59 P1.4 — projection of CYCLE_REGISTER.csv. SSOT is the git CSV.';

CREATE INDEX IF NOT EXISTS cycle_register_mirror_synced_at_idx
  ON compliance.cycle_register_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS cycle_register_mirror_status_idx
  ON compliance.cycle_register_mirror (status);
CREATE INDEX IF NOT EXISTS cycle_register_mirror_coordinating_idx
  ON compliance.cycle_register_mirror (coordinating_initiative_id);

ALTER TABLE compliance.cycle_register_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS cycle_register_mirror_deny_authenticated ON compliance.cycle_register_mirror;
DROP POLICY IF EXISTS cycle_register_mirror_deny_anon ON compliance.cycle_register_mirror;
CREATE POLICY cycle_register_mirror_deny_authenticated
  ON compliance.cycle_register_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY cycle_register_mirror_deny_anon
  ON compliance.cycle_register_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.cycle_register_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.cycle_register_mirror TO service_role;
