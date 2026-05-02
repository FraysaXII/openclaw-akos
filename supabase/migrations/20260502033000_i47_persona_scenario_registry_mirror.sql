-- Initiative 47 P1 — compliance.persona_scenario_registry_mirror
--
-- D-IH-47-A: PERSONA_SCENARIO_REGISTRY.csv as canonical SSOT; this is the
-- queryable mirror. Same governance pattern as compliance.skill_registry_mirror
-- (I32 P2). Extends with tenant_id (D-IH-47-K) for multi-tenant readiness:
-- NULL default = "shared scenario applies to all tenants"; non-NULL string =
-- tenant-scoped scenario (future I34 cross-tenant fan-out).

CREATE SCHEMA IF NOT EXISTS compliance;

CREATE TABLE IF NOT EXISTS compliance.persona_scenario_registry_mirror (
  scenario_id                TEXT NOT NULL,
  persona_id                 TEXT NOT NULL,
  skill_id                   TEXT NOT NULL,
  tenant_id                  TEXT,                  -- D-IH-47-K: NULL = shared
  tier                       TEXT NOT NULL,
  scenario_class             TEXT NOT NULL,
  difficulty_class           TEXT NOT NULL,
  prompt_text                TEXT NOT NULL,
  expected_route             TEXT NOT NULL,
  expected_keywords          TEXT,                  -- semicolon-list
  forbidden_keywords         TEXT,                  -- semicolon-list
  expected_outcome_class     TEXT NOT NULL,
  language                   TEXT NOT NULL,
  topic_ids                  TEXT,                  -- semicolon-list
  lifecycle_status           TEXT NOT NULL DEFAULT 'active',
  notes                      TEXT,
  source_git_sha             TEXT NOT NULL,
  synced_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (scenario_id)
);

COMMENT ON TABLE compliance.persona_scenario_registry_mirror IS
  'Initiative 47 P1 — projection of PERSONA_SCENARIO_REGISTRY.csv. SSOT is the git CSV. Joins persona_id (PERSONA_REGISTRY) x skill_id (SKILL_REGISTRY) x topic_ids (TOPIC_REGISTRY) for the persona-driven UAT scenario library.';

COMMENT ON COLUMN compliance.persona_scenario_registry_mirror.tenant_id IS
  'D-IH-47-K (RICE C): NULL = shared scenario applies to all tenants; non-NULL = tenant-scoped (future I34 multi-tenant cross-tenant fan-out).';

COMMENT ON COLUMN compliance.persona_scenario_registry_mirror.difficulty_class IS
  'D-IH-47-C: trivial | moderate | hard | impossible. Auto-classified by scripts/calibrate_scenarios.py at P0 + P10 + P15. Target distribution 40/40/10/10 within tolerance ±5%.';

CREATE INDEX IF NOT EXISTS persona_scenario_registry_mirror_synced_at_idx
  ON compliance.persona_scenario_registry_mirror (synced_at DESC);
CREATE INDEX IF NOT EXISTS persona_scenario_registry_mirror_lifecycle_idx
  ON compliance.persona_scenario_registry_mirror (lifecycle_status);

-- D-IH-47-K: composite (persona_id, tenant_id) index for the multi-tenant
-- query pattern. Partial index on non-NULL tenant_id is the I34-prep slot;
-- NULL rows still served by the persona-only index pattern.
CREATE INDEX IF NOT EXISTS persona_scenario_registry_mirror_persona_tenant_idx
  ON compliance.persona_scenario_registry_mirror (persona_id, tenant_id);

CREATE INDEX IF NOT EXISTS persona_scenario_registry_mirror_skill_idx
  ON compliance.persona_scenario_registry_mirror (skill_id);

CREATE INDEX IF NOT EXISTS persona_scenario_registry_mirror_difficulty_idx
  ON compliance.persona_scenario_registry_mirror (difficulty_class);

CREATE INDEX IF NOT EXISTS persona_scenario_registry_mirror_tenant_partial_idx
  ON compliance.persona_scenario_registry_mirror (tenant_id)
  WHERE tenant_id IS NOT NULL;

ALTER TABLE compliance.persona_scenario_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS persona_scenario_registry_mirror_deny_authenticated ON compliance.persona_scenario_registry_mirror;
DROP POLICY IF EXISTS persona_scenario_registry_mirror_deny_anon ON compliance.persona_scenario_registry_mirror;
CREATE POLICY persona_scenario_registry_mirror_deny_authenticated
  ON compliance.persona_scenario_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY persona_scenario_registry_mirror_deny_anon
  ON compliance.persona_scenario_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.persona_scenario_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.persona_scenario_registry_mirror TO service_role;
