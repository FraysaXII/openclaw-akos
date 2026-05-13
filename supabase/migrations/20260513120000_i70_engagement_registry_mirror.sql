-- Initiative 70 P8.1 — compliance.engagement_registry_mirror
-- Mirrors the canonical ENGAGEMENT_REGISTRY.csv (16 columns + bookkeeping).
-- SSOT remains docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv.
-- Same governance pattern as compliance.policy_register_mirror (deny-by-default RLS; service_role only).
-- ERP panel slot: op_pmo_engagements (consumed by HLK_ERP_ARCHITECTURE.md §4).

CREATE SCHEMA IF NOT EXISTS compliance;
CREATE SCHEMA IF NOT EXISTS governance;

CREATE TABLE IF NOT EXISTS compliance.engagement_registry_mirror (
  engagement_id        TEXT NOT NULL,
  engagement_name      TEXT NOT NULL,
  engagement_class     TEXT NOT NULL,
  counterparty_org_id  TEXT,
  owner_role           TEXT NOT NULL,
  status               TEXT NOT NULL,
  started_at           DATE,
  ended_at             DATE,
  language_primary     TEXT,
  language_secondary   TEXT,
  deliverable_path     TEXT,
  supabase_mirror      TEXT,
  panel_slot           TEXT,
  related_initiatives  TEXT,    -- semicolon-list TEXT
  classification       TEXT,    -- semicolon-list TEXT
  notes                TEXT,
  source_git_sha       TEXT NOT NULL,
  synced_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (engagement_id),
  CONSTRAINT engagement_registry_mirror_class_chk
    CHECK (engagement_class IN (
      'customer-outbound',
      'partner-outbound',
      'sister-business-outbound-internal',
      'collaborator-inbound',
      'advisor-outbound-internal',
      'internal',
      'trainee',
      'investor-inbound',
      'legal-counsel-outbound-internal'
      -- Enum extends per I70 §8.17 GOI hunt ratifications.
    )),
  CONSTRAINT engagement_registry_mirror_status_chk
    CHECK (status IN ('active', 'paused', 'archived', 'closed'))
);

COMMENT ON TABLE compliance.engagement_registry_mirror IS
  'Initiative 70 P8.1 — projection of ENGAGEMENT_REGISTRY.csv (engagement metadata for governance + ERP). SSOT is the git CSV.';

CREATE INDEX IF NOT EXISTS engagement_registry_mirror_status_idx
  ON compliance.engagement_registry_mirror (status);
CREATE INDEX IF NOT EXISTS engagement_registry_mirror_class_idx
  ON compliance.engagement_registry_mirror (engagement_class);
CREATE INDEX IF NOT EXISTS engagement_registry_mirror_owner_idx
  ON compliance.engagement_registry_mirror (owner_role);
CREATE INDEX IF NOT EXISTS engagement_registry_mirror_synced_at_idx
  ON compliance.engagement_registry_mirror (synced_at DESC);

ALTER TABLE compliance.engagement_registry_mirror ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS engagement_registry_mirror_deny_authenticated ON compliance.engagement_registry_mirror;
DROP POLICY IF EXISTS engagement_registry_mirror_deny_anon ON compliance.engagement_registry_mirror;
CREATE POLICY engagement_registry_mirror_deny_authenticated
  ON compliance.engagement_registry_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY engagement_registry_mirror_deny_anon
  ON compliance.engagement_registry_mirror FOR ALL TO anon USING (false);

REVOKE ALL ON TABLE compliance.engagement_registry_mirror FROM PUBLIC;
GRANT ALL ON TABLE compliance.engagement_registry_mirror TO service_role;

-- Operator-facing view (filters archived rows so the ERP panel shows live engagements only).
CREATE OR REPLACE VIEW governance.engagement_registry_view AS
SELECT
  engagement_id,
  engagement_name,
  engagement_class,
  counterparty_org_id,
  owner_role,
  status,
  started_at,
  ended_at,
  language_primary,
  language_secondary,
  deliverable_path,
  panel_slot,
  related_initiatives,
  classification,
  synced_at
FROM compliance.engagement_registry_mirror
WHERE status <> 'archived';

COMMENT ON VIEW governance.engagement_registry_view IS
  'Initiative 70 P8.1 — operator-facing engagement registry (active + paused + closed; archived rows hidden). Consumed by HLK-ERP panel slot op_pmo_engagements.';

-- Audit view: archived rows only, for historical review.
CREATE OR REPLACE VIEW governance.engagement_registry_archived_view AS
SELECT
  engagement_id,
  engagement_name,
  engagement_class,
  counterparty_org_id,
  owner_role,
  status,
  started_at,
  ended_at,
  language_primary,
  language_secondary,
  deliverable_path,
  panel_slot,
  related_initiatives,
  classification,
  notes,
  synced_at
FROM compliance.engagement_registry_mirror
WHERE status = 'archived';

COMMENT ON VIEW governance.engagement_registry_archived_view IS
  'Initiative 70 P8.1 — archived engagement audit view (status=archived only).';
