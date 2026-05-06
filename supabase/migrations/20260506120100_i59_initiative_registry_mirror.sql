-- Initiative 59 P1.2 — compliance.initiative_registry_mirror
-- D-IH-59-A: HLK governance promotion model — five dimensions land atomically.
-- D-IH-59-B: Two-layer SSOT — markdown master-roadmap.md prose stays canonical;
-- this CSV is canonical for governed metadata (FK joins / lifecycle).
-- D-IH-59-D: Status taxonomy enforced by CHECK constraint (seven values).
-- D-IH-59-G: manifests_processes nullable receiver column for I60 mints.

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.initiative_registry_mirror (
  initiative_id              TEXT NOT NULL,
  repo_slug                  TEXT NOT NULL,
  folder_path                TEXT NOT NULL,
  title                      TEXT NOT NULL,
  status                     TEXT NOT NULL CHECK (
    status IN ('closed', 'archived', 'active', 'continuous', 'program_line', 'gated_external', 'gated_operator')
  ),
  cycle_id                   TEXT,
  owner_role                 TEXT NOT NULL,
  inception_date             DATE,
  last_review                DATE,
  closed_at                  DATE,
  archived_at                DATE,
  superseded_by              TEXT,
  continuous_rationale       TEXT,
  cadence                    TEXT,
  gated_on                   TEXT,
  operator_action            TEXT,
  inception_decision_id      TEXT,
  closure_decision_id        TEXT,
  manifests_processes        TEXT,    -- semicolon-list FK to process_list.csv item_id (D-IH-59-G; nullable)
  linked_topic_ids           TEXT,
  notes                      TEXT,
  source_git_sha             TEXT NOT NULL,
  synced_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (initiative_id)
);

COMMENT ON TABLE compliance.initiative_registry_mirror IS
  'Initiative 59 P1.2 — projection of INITIATIVE_REGISTRY.csv. Markdown master-roadmap.md stays canonical for prose (D-IH-59-B).';
COMMENT ON COLUMN compliance.initiative_registry_mirror.manifests_processes IS
  'D-IH-59-G nullable receiver column; populated in I60 candidate process_list mints with G-60-N tranche gates.';

CREATE INDEX IF NOT EXISTS initiative_registry_mirror_synced_at_idx
  ON compliance.initiative_registry_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS initiative_registry_mirror_status_idx
  ON compliance.initiative_registry_mirror (status);
CREATE INDEX IF NOT EXISTS initiative_registry_mirror_repo_slug_idx
  ON compliance.initiative_registry_mirror (repo_slug);
CREATE INDEX IF NOT EXISTS initiative_registry_mirror_cycle_id_idx
  ON compliance.initiative_registry_mirror (cycle_id);
CREATE INDEX IF NOT EXISTS initiative_registry_mirror_last_review_idx
  ON compliance.initiative_registry_mirror (last_review);

ALTER TABLE compliance.initiative_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS initiative_registry_mirror_deny_authenticated ON compliance.initiative_registry_mirror;
DROP POLICY IF EXISTS initiative_registry_mirror_deny_anon ON compliance.initiative_registry_mirror;
CREATE POLICY initiative_registry_mirror_deny_authenticated
  ON compliance.initiative_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY initiative_registry_mirror_deny_anon
  ON compliance.initiative_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.initiative_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.initiative_registry_mirror TO service_role;
