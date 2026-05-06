-- Initiative 59 P1.1 — compliance.repository_registry_mirror
-- D-IH-59-A: HLK governance promotion model — five dimensions land atomically.
-- D-IH-59-C: REPOSITORY_REGISTRY.csv promotes the existing markdown SSOT to a
-- governed dimension. Both stay canonical-class; sync validator enforces.

CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'HLK git-backed projections; SSOT remains docs/references/hlk/compliance/*.csv';

CREATE TABLE IF NOT EXISTS compliance.repository_registry_mirror (
  repo_slug             TEXT NOT NULL,
  github_url            TEXT NOT NULL,
  class                 TEXT NOT NULL CHECK (class IN ('platform', 'internal', 'client-delivery', 'reference')),
  primary_owner_role    TEXT NOT NULL,
  topic_ids             TEXT,    -- semicolon-list TEXT (DAMA-pure projection of CSV)
  vault_doc_root        TEXT,
  api_spec_pointer      TEXT,
  api_topic_id          TEXT,
  lifecycle_status      TEXT NOT NULL CHECK (lifecycle_status IN ('active', 'archived', 'reference')),
  notes                 TEXT,
  source_git_sha        TEXT NOT NULL,
  synced_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (repo_slug)
);

COMMENT ON TABLE compliance.repository_registry_mirror IS
  'Initiative 59 P1.1 — projection of REPOSITORY_REGISTRY.csv. SSOT is the git CSV (D-IH-59-C).';

CREATE INDEX IF NOT EXISTS repository_registry_mirror_synced_at_idx
  ON compliance.repository_registry_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS repository_registry_mirror_class_idx
  ON compliance.repository_registry_mirror (class);
CREATE INDEX IF NOT EXISTS repository_registry_mirror_lifecycle_idx
  ON compliance.repository_registry_mirror (lifecycle_status);

ALTER TABLE compliance.repository_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS repository_registry_mirror_deny_authenticated ON compliance.repository_registry_mirror;
DROP POLICY IF EXISTS repository_registry_mirror_deny_anon ON compliance.repository_registry_mirror;
CREATE POLICY repository_registry_mirror_deny_authenticated
  ON compliance.repository_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY repository_registry_mirror_deny_anon
  ON compliance.repository_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.repository_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.repository_registry_mirror TO service_role;
