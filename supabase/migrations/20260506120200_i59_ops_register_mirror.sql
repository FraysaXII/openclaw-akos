-- Initiative 59 P1.3 — compliance.ops_register_mirror
-- D-IH-59-A: HLK governance promotion model — five dimensions land atomically.
-- Formalizes OPS-XX-Y items previously scattered across master-roadmap.md +
-- CHANGELOG entries. OPERATOR_INBOX.md (Initiative 59 P4) is auto-rendered
-- from this dimension where status=open AND owner_class IN (operator, mixed).

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.ops_register_mirror (
  ops_action_id                  TEXT NOT NULL,
  title                          TEXT NOT NULL,
  originating_initiative_id      TEXT NOT NULL,
  forwarded_to_initiative_id     TEXT,
  owner_class                    TEXT NOT NULL CHECK (owner_class IN ('operator', 'engineering', 'mixed')),
  owner_role                     TEXT NOT NULL,
  status                         TEXT NOT NULL CHECK (
    status IN ('open', 'in_progress', 'closed', 'cancelled', 'superseded')
  ),
  rice_reach                     INTEGER,
  rice_impact                    NUMERIC,
  rice_confidence_pct            INTEGER,
  rice_effort_person_weeks       NUMERIC,
  rice_score                     NUMERIC,
  gate_id                        TEXT,
  linked_decision_ids            TEXT,    -- semicolon-list FK to DECISION_REGISTER
  summary                        TEXT,
  operator_runbook_path          TEXT,
  evidence_path                   TEXT,
  opened_at                      DATE,
  closed_at                      DATE,
  notes                          TEXT,
  source_git_sha                 TEXT NOT NULL,
  synced_at                      TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (ops_action_id)
);

COMMENT ON TABLE compliance.ops_register_mirror IS
  'Initiative 59 P1.3 — projection of OPS_REGISTER.csv. SSOT is the git CSV. OPERATOR_INBOX.md auto-renders the operator-class subset (status=open AND owner_class IN (operator, mixed) ORDER BY rice_score DESC).';

CREATE INDEX IF NOT EXISTS ops_register_mirror_synced_at_idx
  ON compliance.ops_register_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS ops_register_mirror_status_idx
  ON compliance.ops_register_mirror (status);
CREATE INDEX IF NOT EXISTS ops_register_mirror_owner_class_idx
  ON compliance.ops_register_mirror (owner_class);
CREATE INDEX IF NOT EXISTS ops_register_mirror_originating_idx
  ON compliance.ops_register_mirror (originating_initiative_id);
CREATE INDEX IF NOT EXISTS ops_register_mirror_rice_score_idx
  ON compliance.ops_register_mirror (rice_score DESC NULLS LAST);

ALTER TABLE compliance.ops_register_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS ops_register_mirror_deny_authenticated ON compliance.ops_register_mirror;
DROP POLICY IF EXISTS ops_register_mirror_deny_anon ON compliance.ops_register_mirror;
CREATE POLICY ops_register_mirror_deny_authenticated
  ON compliance.ops_register_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY ops_register_mirror_deny_anon
  ON compliance.ops_register_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.ops_register_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.ops_register_mirror TO service_role;
