-- Initiative 32 P2 — compliance.skill_registry_mirror
-- D-IH-32-B: Skill registry as 7th canonical dimension. Tenant-aware schema
-- per D-IH-32-J. Same governance pattern as compliance.persona_registry_mirror
-- (Initiative 31 P2.1).

CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'HLK git-backed projections; SSOT remains docs/references/hlk/compliance/*.csv';

CREATE TABLE IF NOT EXISTS compliance.skill_registry_mirror (
  skill_id                TEXT NOT NULL,
  name                    TEXT,
  agents_supported        TEXT,    -- semicolon-list TEXT (DAMA-pure projection of CSV)
  axes_consumed           TEXT,    -- semicolon-list TEXT
  tools_required          TEXT,    -- semicolon-list TEXT
  version                 TEXT,
  owner_role              TEXT,
  eval_baseline_pct       NUMERIC,
  langfuse_trace_pattern  TEXT,
  tenant_scope            TEXT NOT NULL DEFAULT 'shared',
  lifecycle_status        TEXT,
  topic_ids               TEXT,    -- semicolon-list TEXT (axis 6, populated in P5)
  description             TEXT,
  notes                   TEXT,
  source_git_sha          TEXT NOT NULL,
  synced_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (skill_id)
);

COMMENT ON TABLE compliance.skill_registry_mirror IS
  'Initiative 32 P2 — projection of SKILL_REGISTRY.csv. SSOT is the git CSV.';
COMMENT ON COLUMN compliance.skill_registry_mirror.tenant_scope IS
  'D-IH-32-J: only "shared" valid until Initiative 34 opens tenant scopes.';

CREATE INDEX IF NOT EXISTS skill_registry_mirror_synced_at_idx
  ON compliance.skill_registry_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS skill_registry_mirror_lifecycle_idx
  ON compliance.skill_registry_mirror (lifecycle_status);
CREATE INDEX IF NOT EXISTS skill_registry_mirror_owner_role_idx
  ON compliance.skill_registry_mirror (owner_role);
CREATE INDEX IF NOT EXISTS skill_registry_mirror_tenant_scope_idx
  ON compliance.skill_registry_mirror (tenant_scope);

ALTER TABLE compliance.skill_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS skill_registry_mirror_deny_authenticated ON compliance.skill_registry_mirror;
DROP POLICY IF EXISTS skill_registry_mirror_deny_anon ON compliance.skill_registry_mirror;
CREATE POLICY skill_registry_mirror_deny_authenticated
  ON compliance.skill_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY skill_registry_mirror_deny_anon
  ON compliance.skill_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.skill_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.skill_registry_mirror TO service_role;
