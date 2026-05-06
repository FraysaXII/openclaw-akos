-- Initiative 62 P3.1 — demo.* schema for showcase mode
-- D-IH-62-C: separate schema, same Supabase project, isolated by GRANTs and RLS.
-- D-IH-62-K: idempotent seed via scripts/seed-demo.ts; runs in CI on every preview deploy.
--
-- Tables shape-match the compliance.* mirrors so erp.* views can route via session GUC.
-- NB: this migration creates EMPTY demo tables; they are populated by the seed script.

CREATE SCHEMA IF NOT EXISTS demo;

GRANT USAGE ON SCHEMA demo TO authenticated, anon, service_role;

-- =============================================================================
-- demo.initiative_registry_mirror
-- =============================================================================
CREATE TABLE IF NOT EXISTS demo.initiative_registry_mirror (
  initiative_id              TEXT PRIMARY KEY,
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
  manifests_processes        TEXT,
  linked_topic_ids           TEXT,
  notes                      TEXT,
  source_git_sha             TEXT NOT NULL DEFAULT 'demo',
  synced_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- demo.ops_register_mirror
-- =============================================================================
CREATE TABLE IF NOT EXISTS demo.ops_register_mirror (
  ops_id             TEXT PRIMARY KEY,
  title              TEXT NOT NULL,
  owner_class        TEXT NOT NULL CHECK (owner_class IN ('operator', 'mixed', 'engineering')),
  rice_score         NUMERIC,
  rice_reach         NUMERIC,
  rice_impact        NUMERIC,
  rice_confidence    NUMERIC,
  rice_effort        NUMERIC,
  initiative_id      TEXT,
  cycle_id           TEXT,
  status             TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'done', 'cancelled')),
  linked_decision_id TEXT,
  linked_report      TEXT,
  opened_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_review        DATE,
  source_git_sha     TEXT NOT NULL DEFAULT 'demo',
  synced_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- demo.persona_registry_mirror — minimal shape for showcase
-- =============================================================================
CREATE TABLE IF NOT EXISTS demo.persona_registry_mirror (
  persona_id         TEXT PRIMARY KEY,
  display_name       TEXT NOT NULL,
  archetype          TEXT,
  tier               TEXT,
  notes              TEXT,
  synced_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- demo.skill_registry_mirror
-- =============================================================================
CREATE TABLE IF NOT EXISTS demo.skill_registry_mirror (
  skill_id           TEXT PRIMARY KEY,
  display_name       TEXT NOT NULL,
  status             TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'experimental', 'retired')),
  routing_condition  TEXT,
  retrieval_mode     TEXT,
  notes              TEXT,
  synced_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =============================================================================
-- demo.eval_run + demo.dossier_run (subset of columns)
-- =============================================================================
CREATE TABLE IF NOT EXISTS demo.eval_run (
  id            BIGSERIAL PRIMARY KEY,
  kind          TEXT NOT NULL,
  verdict       TEXT NOT NULL,
  run_payload   JSONB NOT NULL DEFAULT '{}'::jsonb,
  occurred_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS demo.dossier_run (
  id            BIGSERIAL PRIMARY KEY,
  verdict       TEXT NOT NULL,
  run_payload   JSONB NOT NULL DEFAULT '{}'::jsonb,
  started_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  ended_at      TIMESTAMPTZ
);

-- =============================================================================
-- Grants — demo data is read by both anon (showcase) and authenticated (operator preview)
-- =============================================================================
GRANT SELECT ON ALL TABLES IN SCHEMA demo TO authenticated, anon;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA demo TO service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA demo GRANT SELECT ON TABLES TO authenticated, anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA demo GRANT INSERT, UPDATE, DELETE ON TABLES TO service_role;

-- Enable RLS but with permissive read policies; writes restricted to service_role.
ALTER TABLE demo.initiative_registry_mirror ENABLE ROW LEVEL SECURITY;
ALTER TABLE demo.ops_register_mirror ENABLE ROW LEVEL SECURITY;
ALTER TABLE demo.persona_registry_mirror ENABLE ROW LEVEL SECURITY;
ALTER TABLE demo.skill_registry_mirror ENABLE ROW LEVEL SECURITY;
ALTER TABLE demo.eval_run ENABLE ROW LEVEL SECURITY;
ALTER TABLE demo.dossier_run ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
  -- Permissive read for everyone (demo is fictional)
  CREATE POLICY demo_read_all ON demo.initiative_registry_mirror FOR SELECT USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE POLICY demo_read_all ON demo.ops_register_mirror       FOR SELECT USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE POLICY demo_read_all ON demo.persona_registry_mirror   FOR SELECT USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE POLICY demo_read_all ON demo.skill_registry_mirror     FOR SELECT USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE POLICY demo_read_all ON demo.eval_run                  FOR SELECT USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE POLICY demo_read_all ON demo.dossier_run               FOR SELECT USING (true);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

COMMENT ON SCHEMA demo IS
  'I62 P3.1 — fictional showcase data. Routed-to via erp._mode() = ''demo''. Seeded by scripts/seed-demo.ts (idempotent).';
