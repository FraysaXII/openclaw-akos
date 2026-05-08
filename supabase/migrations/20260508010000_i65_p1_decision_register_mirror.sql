-- I65 P1.1 — compliance.decision_register_mirror
--
-- I59 chartered five governance dimensions (initiative, ops, decision, evidence,
-- risk). Initiative + ops mirrors landed in I59 P1.2 / P1.3; the decision mirror
-- was originally scheduled for the same tranche but was deferred. I65 needs joined
-- decision counts on the planning workspace view, so the decision mirror DDL lands
-- here as a P1 prerequisite (D-IH-65-D — close the I59 catch-up before adding net-
-- new joins).
--
-- Two-layer SSOT (D-IH-59-B): markdown decision-log.md prose stays canonical for
-- narrative; this CSV mirror is canonical for queryable decision metadata
-- (status, links, decision_class, decided_at).

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.decision_register_mirror (
  decision_id                 TEXT NOT NULL,
  title                       TEXT NOT NULL,
  initiating_initiative_id    TEXT,
  linked_initiative_ids       TEXT,    -- semicolon-list
  linked_ops_action_ids       TEXT,    -- semicolon-list
  linked_policies             TEXT,    -- semicolon-list
  linked_topic_ids            TEXT,    -- semicolon-list
  decision_class              TEXT NOT NULL CHECK (
    decision_class IN ('architecture', 'process', 'governance', 'finance', 'staffing', 'product', 'security', 'data', 'brand', 'continuity', 'methodology', 'closure', 'execution', 'scope')
  ),
  status                      TEXT NOT NULL CHECK (
    status IN ('active', 'archived', 'superseded', 'rescinded', 'proposed')
  ),
  reversibility               TEXT CHECK (
    reversibility IN ('low', 'medium', 'high') OR reversibility IS NULL
  ),
  decided_at                  DATE,
  decision_log_path           TEXT,
  supersedes_decision_id      TEXT,
  summary                     TEXT,
  notes                       TEXT,
  source_git_sha              TEXT NOT NULL,
  synced_at                   TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (decision_id)
);

COMMENT ON TABLE compliance.decision_register_mirror IS
  'I65 P1.1 — projection of DECISION_REGISTER.csv. Markdown decision-log.md stays canonical for prose. Joined into governance.planning_workspace_view for /operator/planning/.';

CREATE INDEX IF NOT EXISTS decision_register_mirror_initiating_idx
  ON compliance.decision_register_mirror (initiating_initiative_id);
CREATE INDEX IF NOT EXISTS decision_register_mirror_status_idx
  ON compliance.decision_register_mirror (status);
CREATE INDEX IF NOT EXISTS decision_register_mirror_decided_at_idx
  ON compliance.decision_register_mirror (decided_at DESC);
CREATE INDEX IF NOT EXISTS decision_register_mirror_synced_at_idx
  ON compliance.decision_register_mirror (synced_at DESC);

ALTER TABLE compliance.decision_register_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS decision_register_mirror_deny_authenticated ON compliance.decision_register_mirror;
DROP POLICY IF EXISTS decision_register_mirror_deny_anon ON compliance.decision_register_mirror;
CREATE POLICY decision_register_mirror_deny_authenticated
  ON compliance.decision_register_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY decision_register_mirror_deny_anon
  ON compliance.decision_register_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.decision_register_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.decision_register_mirror TO service_role;
