-- Initiative 62 P1.3 — Mission Control RBAC schema
-- D-IH-62-A: Supabase Auth as identity provider.
-- D-IH-62-B: Map each authenticated user to AKOS baseline_organisation.access_level (0-6).
-- D-IH-62-J: Founder impersonation audited via holistika_ops.audit_log.
--
-- Tables:
--   * holistika_ops.user_role_mapping  — auth.users.id <-> baseline_organisation.role_id + access_level
--   * holistika_ops.audit_log          — every confidential read + impersonation start/stop + sign-in
--   * holistika_ops.user_preferences   — theme/density/locale/saved_views/starred_ids
--   * holistika_ops.notifications      — Realtime-subscribed in-app drawer source

CREATE SCHEMA IF NOT EXISTS holistika_ops;

-- =============================================================================
-- 1. user_role_mapping
-- =============================================================================
CREATE TABLE IF NOT EXISTS holistika_ops.user_role_mapping (
  user_id            UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email              TEXT NOT NULL,
  role_id            TEXT NOT NULL,                                  -- FK to compliance.baseline_organisation_mirror.role_id
  access_level       SMALLINT NOT NULL CHECK (access_level BETWEEN 0 AND 6),
  display_name       TEXT,
  status             TEXT NOT NULL DEFAULT 'active'
                     CHECK (status IN ('active', 'pending', 'disabled')),
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_seen_at       TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS user_role_mapping_role_id_idx
  ON holistika_ops.user_role_mapping (role_id);
CREATE INDEX IF NOT EXISTS user_role_mapping_access_level_idx
  ON holistika_ops.user_role_mapping (access_level);
CREATE INDEX IF NOT EXISTS user_role_mapping_email_idx
  ON holistika_ops.user_role_mapping (lower(email));

COMMENT ON TABLE  holistika_ops.user_role_mapping IS
  'I62 P1.3 — auth.users -> AKOS access_level mapping. Sourced from baseline_organisation.csv (canonical) via daily sync; manually patchable.';
COMMENT ON COLUMN holistika_ops.user_role_mapping.access_level IS
  'AKOS baseline_organisation.access_level (0..6). 6 = founder/system-owner; 4 = operator; 1 = advisor.';

ALTER TABLE holistika_ops.user_role_mapping ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS user_role_mapping_self_read ON holistika_ops.user_role_mapping;
CREATE POLICY user_role_mapping_self_read
  ON holistika_ops.user_role_mapping FOR SELECT TO authenticated
  USING (auth.uid() = user_id);

DROP POLICY IF EXISTS user_role_mapping_admin_read ON holistika_ops.user_role_mapping;
CREATE POLICY user_role_mapping_admin_read
  ON holistika_ops.user_role_mapping FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM holistika_ops.user_role_mapping urm2
      WHERE urm2.user_id = auth.uid() AND urm2.access_level >= 6
    )
  );

DROP POLICY IF EXISTS user_role_mapping_service_role_all ON holistika_ops.user_role_mapping;
CREATE POLICY user_role_mapping_service_role_all
  ON holistika_ops.user_role_mapping FOR ALL TO service_role USING (true) WITH CHECK (true);

-- =============================================================================
-- 2. audit_log
-- =============================================================================
CREATE TABLE IF NOT EXISTS holistika_ops.audit_log (
  id                 BIGSERIAL PRIMARY KEY,
  occurred_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  actor_user_id      UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  actor_email        TEXT,
  actor_access_level SMALLINT,
  action             TEXT NOT NULL,                                  -- e.g. 'auth.sign_in', 'impersonate.start', 'data.confidential_read'
  resource_kind      TEXT,                                           -- e.g. 'goi_poi_register_mirror'
  resource_id        TEXT,                                           -- row PK or other handle
  metadata           JSONB NOT NULL DEFAULT '{}'::jsonb,
  ip_address         TEXT,
  user_agent         TEXT
);

CREATE INDEX IF NOT EXISTS audit_log_actor_user_id_idx ON holistika_ops.audit_log (actor_user_id);
CREATE INDEX IF NOT EXISTS audit_log_action_idx        ON holistika_ops.audit_log (action);
CREATE INDEX IF NOT EXISTS audit_log_occurred_at_idx   ON holistika_ops.audit_log (occurred_at DESC);

COMMENT ON TABLE holistika_ops.audit_log IS
  'I62 P1.3 / P1.5 — Mission Control audit trail. 365-day retention then cold archive (P8.1).';

ALTER TABLE holistika_ops.audit_log ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS audit_log_admin_read ON holistika_ops.audit_log;
CREATE POLICY audit_log_admin_read
  ON holistika_ops.audit_log FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM holistika_ops.user_role_mapping urm
      WHERE urm.user_id = auth.uid() AND urm.access_level >= 6
    )
  );

DROP POLICY IF EXISTS audit_log_service_role_all ON holistika_ops.audit_log;
CREATE POLICY audit_log_service_role_all
  ON holistika_ops.audit_log FOR ALL TO service_role USING (true) WITH CHECK (true);

-- =============================================================================
-- 3. user_preferences
-- =============================================================================
CREATE TABLE IF NOT EXISTS holistika_ops.user_preferences (
  user_id            UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  theme              TEXT NOT NULL DEFAULT 'system'
                     CHECK (theme IN ('light', 'dark', 'dark-blue', 'light-blue', 'brown', 'white', 'system')),
  density            TEXT NOT NULL DEFAULT 'standard'
                     CHECK (density IN ('compact', 'standard', 'comfortable')),
  locale             TEXT NOT NULL DEFAULT 'en'
                     CHECK (locale IN ('en', 'es', 'fr')),
  saved_views        JSONB NOT NULL DEFAULT '[]'::jsonb,
  starred_ids        JSONB NOT NULL DEFAULT '[]'::jsonb,
  expanded_sections  JSONB NOT NULL DEFAULT '{}'::jsonb,
  recent_searches    JSONB NOT NULL DEFAULT '[]'::jsonb,
  notification_settings JSONB NOT NULL DEFAULT '{}'::jsonb,
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE holistika_ops.user_preferences IS
  'I62 P1 / P7 — per-user UX preferences for Mission Control. Theme/density/locale/saved_views/starred_ids/notification_settings.';

ALTER TABLE holistika_ops.user_preferences ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS user_preferences_self_select ON holistika_ops.user_preferences;
CREATE POLICY user_preferences_self_select
  ON holistika_ops.user_preferences FOR SELECT TO authenticated USING (auth.uid() = user_id);

DROP POLICY IF EXISTS user_preferences_self_modify ON holistika_ops.user_preferences;
CREATE POLICY user_preferences_self_modify
  ON holistika_ops.user_preferences FOR ALL TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS user_preferences_service_role_all ON holistika_ops.user_preferences;
CREATE POLICY user_preferences_service_role_all
  ON holistika_ops.user_preferences FOR ALL TO service_role USING (true) WITH CHECK (true);

-- =============================================================================
-- 4. notifications
-- =============================================================================
CREATE TABLE IF NOT EXISTS holistika_ops.notifications (
  id                 BIGSERIAL PRIMARY KEY,
  user_id            UUID REFERENCES auth.users(id) ON DELETE CASCADE,        -- NULL = broadcast to all
  category           TEXT NOT NULL
                     CHECK (category IN ('ops_open', 'validation_failure', 'three_lights_flip', 'cycle_closure', 'system')),
  severity           TEXT NOT NULL DEFAULT 'info'
                     CHECK (severity IN ('info', 'warn', 'error')),
  title              TEXT NOT NULL,
  body               TEXT,
  link               TEXT,
  metadata           JSONB NOT NULL DEFAULT '{}'::jsonb,
  read_at            TIMESTAMPTZ,
  snoozed_until      TIMESTAMPTZ,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS notifications_user_id_idx     ON holistika_ops.notifications (user_id);
CREATE INDEX IF NOT EXISTS notifications_category_idx    ON holistika_ops.notifications (category);
CREATE INDEX IF NOT EXISTS notifications_unread_idx      ON holistika_ops.notifications (user_id, read_at) WHERE read_at IS NULL;

COMMENT ON TABLE holistika_ops.notifications IS
  'I62 P7.3 — in-app notifications drawer source. Subscribed via Supabase Realtime; broadcast (user_id NULL) or per-user.';

ALTER TABLE holistika_ops.notifications ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS notifications_self_or_broadcast_read ON holistika_ops.notifications;
CREATE POLICY notifications_self_or_broadcast_read
  ON holistika_ops.notifications FOR SELECT TO authenticated
  USING (user_id IS NULL OR user_id = auth.uid());

DROP POLICY IF EXISTS notifications_self_modify ON holistika_ops.notifications;
CREATE POLICY notifications_self_modify
  ON holistika_ops.notifications FOR UPDATE TO authenticated
  USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());

DROP POLICY IF EXISTS notifications_service_role_all ON holistika_ops.notifications;
CREATE POLICY notifications_service_role_all
  ON holistika_ops.notifications FOR ALL TO service_role USING (true) WITH CHECK (true);

-- =============================================================================
-- 5. Helper function: current_access_level()
-- =============================================================================
CREATE OR REPLACE FUNCTION holistika_ops.current_access_level()
RETURNS SMALLINT
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public, holistika_ops, auth
AS $$
  SELECT COALESCE(
    (SELECT access_level FROM holistika_ops.user_role_mapping WHERE user_id = auth.uid()),
    0
  )::SMALLINT;
$$;

COMMENT ON FUNCTION holistika_ops.current_access_level IS
  'I62 P1.4 — returns the access_level (0..6) for the calling auth user; 0 if no mapping exists. SECURITY DEFINER so RLS does not gate it.';

GRANT EXECUTE ON FUNCTION holistika_ops.current_access_level() TO authenticated, anon, service_role;
