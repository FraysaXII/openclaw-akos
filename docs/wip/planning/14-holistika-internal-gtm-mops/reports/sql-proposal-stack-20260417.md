# SQL proposal — Supabase stack (Phase 3) — **proposal only**

**Date:** 2026-04-17  
**Status:** Awaiting operator approval before `supabase db push`, `apply_migration`, or `execute_sql` against production.

**Governance:** This file is the **authoritative DDL/DML intent** for Initiative 14 Phase 3. No production mutation until: backup, staging verification, and operator sign-off per [`operator-sql-gate.md`](operator-sql-gate.md).

---

## 1. Objectives (mapped to `item_id`)

| Objective | `process_list` / initiative anchor | Notes |
|-----------|-----------------------------------|--------|
| Git-backed **compliance mirrors** with provenance | `holistika_gtm_dtp_001`–`003`, governance | `source_git_sha`, `synced_at` on every row |
| **Holistika company** billing / Stripe **customer** plane (not KiRBe SaaS product subs) | Initiative 14 Phase 3b | Schema `holistika_ops`; **no** reuse of `kirbe.subscriptions` |
| **Deprecate** legacy `public` objects | [`deprecate-legacy-public-proposal.md`](deprecate-legacy-public-proposal.md) | Rename + view shim; cutover after backup |

---

## 2. Preconditions

1. **Extensions** (if not already enabled): `pgcrypto` (for `gen_random_uuid()` if used).
2. **Roles:** `service_role` for batch/sync jobs; `authenticated` for RLS-bound app users; **no** anon read on compliance or `holistika_ops` without explicit policy.
3. **CSV column SSOT:** Mirror tables use **TEXT** for all columns sourced from [`akos/hlk_process_csv.py`](../../../../../akos/hlk_process_csv.py) `PROCESS_LIST_FIELDNAMES` and `baseline_organisation.csv` headers (string-safe; cast in views if needed).

---

## 3. Migration order (do not reorder without updating rollback)

| Step | Name | Idempotent |
|------|------|------------|
| 3.1 | `compliance` schema + mirrors | Yes |
| 3.2 | Indexes on mirrors | Yes |
| 3.3 | RLS + grants | Yes |
| 3.4 | `holistika_ops` schema + company billing stub | Yes |
| 3.5 | Legacy `public` deprecation (separate maintenance window) | Yes (rename) |

---

## 4. DDL — `compliance` mirrors

### 4.1 Schema

```sql
CREATE SCHEMA IF NOT EXISTS compliance;
COMMENT ON SCHEMA compliance IS 'HLK git-backed projections; SSOT remains docs/references/hlk/compliance/*.csv';
```

### 4.2 `compliance.process_list_mirror`

Columns match `PROCESS_LIST_FIELDNAMES` **plus** provenance:

```sql
CREATE TABLE IF NOT EXISTS compliance.process_list_mirror (
  type                    TEXT,
  orientation             TEXT,
  entity                  TEXT,
  area                    TEXT,
  role_parent_1           TEXT,
  role_owner              TEXT,
  item_parent_2           TEXT,
  item_parent_2_id        TEXT,
  item_parent_1           TEXT,
  item_parent_1_id        TEXT,
  item_name               TEXT,
  item_id                 TEXT NOT NULL,
  item_granularity        TEXT,
  time_hours_par          TEXT,
  description             TEXT,
  instructions            TEXT,
  addundum_extras         TEXT,
  confidence              TEXT,
  count_name              TEXT,
  frequency               TEXT,
  quality                 TEXT,
  source_git_sha          TEXT NOT NULL,
  synced_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (item_id)
);

CREATE INDEX IF NOT EXISTS process_list_mirror_parent1_idx
  ON compliance.process_list_mirror (item_parent_1_id);
CREATE INDEX IF NOT EXISTS process_list_mirror_synced_at_idx
  ON compliance.process_list_mirror (synced_at DESC);
```

**Upsert contract (batch job):** `INSERT ... ON CONFLICT (item_id) DO UPDATE SET` all CSV columns + `source_git_sha`, `synced_at = now()`. **Generator in repo:** [`scripts/sync_compliance_mirrors_from_csv.py`](../../../../../scripts/sync_compliance_mirrors_from_csv.py) (`--count-only`, `--output`, `--process-list-only`, `--baseline-only`) — emits SQL for operator review; does not connect to Supabase.

### 4.3 `compliance.baseline_organisation_mirror`

Headers from [`baseline_organisation.csv`](../../../../references/hlk/compliance/baseline_organisation.csv):

```sql
CREATE TABLE IF NOT EXISTS compliance.baseline_organisation_mirror (
  org_uuid                TEXT NOT NULL,
  role_name               TEXT,
  role_description        TEXT,
  role_full_description   TEXT,
  access_level            TEXT,
  reports_to              TEXT,
  area                    TEXT,
  entity                  TEXT,
  org_id                  TEXT,
  sop_url                 TEXT,
  responsible_processes   TEXT,
  components_used         TEXT,
  source_git_sha          TEXT NOT NULL,
  synced_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (org_uuid)
);

CREATE INDEX IF NOT EXISTS baseline_org_mirror_synced_at_idx
  ON compliance.baseline_organisation_mirror (synced_at DESC);
```

---

## 5. DDL — `holistika_ops` (company billing plane; **not** KiRBe product)

**Naming:** Final schema name may be `holistika_ops` or `holistika_company`; pick one before first migration and keep it stable.

### 5.1 Schema + minimal tables

Stores **Holistika legal entity ↔ Stripe customer** linkage and optional invoice pointers. **No** card PAN, no full payment method payloads.

```sql
CREATE SCHEMA IF NOT EXISTS holistika_ops;
COMMENT ON SCHEMA holistika_ops IS 'Holistika company CRM/billing; distinct from kirbe SaaS product schema';

CREATE TABLE IF NOT EXISTS holistika_ops.stripe_customer_link (
  id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_label               TEXT NOT NULL,
  stripe_customer_id      TEXT NOT NULL UNIQUE,
  livemode                BOOLEAN NOT NULL DEFAULT false,
  created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  notes                   TEXT
);

CREATE TABLE IF NOT EXISTS holistika_ops.billing_account (
  id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  legal_entity_name       TEXT NOT NULL,
  currency                TEXT NOT NULL DEFAULT 'usd',
  stripe_customer_link_id UUID REFERENCES holistika_ops.stripe_customer_link(id),
  created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS billing_account_stripe_fk_idx
  ON holistika_ops.billing_account (stripe_customer_link_id);
```

**Stripe two-plane rule:** Webhook handlers for **KiRBe product** vs **Holistika company** must route to **different** tables (`kirbe.*` vs `holistika_ops.*`); document in app config.

---

## 6. RLS and grants

### 6.1 Enable RLS

```sql
ALTER TABLE compliance.process_list_mirror ENABLE ROW LEVEL SECURITY;
ALTER TABLE compliance.baseline_organisation_mirror ENABLE ROW LEVEL SECURITY;
ALTER TABLE holistika_ops.stripe_customer_link ENABLE ROW LEVEL SECURITY;
ALTER TABLE holistika_ops.billing_account ENABLE ROW LEVEL SECURITY;
```

### 6.2 Policy pattern (default deny; service_role for sync)

**Authenticated users:** only if a future dashboard needs read — add **named** policies (e.g. `USING (auth.uid() IS NOT NULL)` plus org membership table). Until then:

```sql
-- Deny all for anon + authenticated on mirrors (sync uses service_role bypass)
CREATE POLICY process_list_mirror_deny_authenticated
  ON compliance.process_list_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY process_list_mirror_deny_anon
  ON compliance.process_list_mirror FOR ALL TO anon USING (false);

CREATE POLICY baseline_org_mirror_deny_authenticated
  ON compliance.baseline_organisation_mirror FOR ALL TO authenticated USING (false);
CREATE POLICY baseline_org_mirror_deny_anon
  ON compliance.baseline_organisation_mirror FOR ALL TO anon USING (false);
```

**`holistika_ops`:** Same deny pattern for `anon`/`authenticated` until app-specific membership exists; **`service_role`** used by Edge Functions / workers with key rotation.

### 6.3 Grants (minimal)

```sql
GRANT USAGE ON SCHEMA compliance TO service_role;
GRANT ALL ON ALL TABLES IN SCHEMA compliance TO service_role;
GRANT USAGE ON SCHEMA holistika_ops TO service_role;
GRANT ALL ON ALL TABLES IN SCHEMA holistika_ops TO service_role;
```

Do **not** grant `anon` SELECT on these schemas without explicit policy review.

---

## 7. Legacy `public` deprecation (separate cutover)

**Intent:** Align with [`deprecate-legacy-public-proposal.md`](deprecate-legacy-public-proposal.md). Example pattern (adjust to actual object names in target DB):

```sql
-- After full backup; run in maintenance window
ALTER TABLE IF EXISTS public."Process list" RENAME TO "Process list_deprecated_20260417";
-- Optional: CREATE VIEW public."Process list" AS SELECT ... FROM compliance.process_list_mirror;
```

**Rollback:** `ALTER TABLE ... RENAME TO` original name; drop shim view if created.

---

## 8. Verification queries (staging)

```sql
SELECT COUNT(*) AS process_rows, MAX(synced_at) AS last_sync
FROM compliance.process_list_mirror;
SELECT COUNT(*) AS org_rows FROM compliance.baseline_organisation_mirror;
SELECT tablename, rowsecurity FROM pg_tables
WHERE schemaname IN ('compliance', 'holistika_ops');
```

Expect `rowsecurity = true` on all four tables. Spot-check **`item_id`** values `holistika_gtm_dtp_001`–`003` exist after sync.

---

## 9. Rollback (clean)

| Step | Action |
|------|--------|
| RLS | `DROP POLICY ...` then `ALTER TABLE ... DISABLE ROW LEVEL SECURITY` |
| Tables | `DROP TABLE IF EXISTS holistika_ops.billing_account CASCADE;` then `stripe_customer_link`; `DROP SCHEMA holistika_ops CASCADE;` |
| Compliance | `DROP TABLE IF EXISTS compliance.process_list_mirror CASCADE;` `DROP TABLE IF EXISTS compliance.baseline_organisation_mirror CASCADE;` |
| Schema | `DROP SCHEMA IF EXISTS compliance CASCADE;` (only if no other objects) |

---

## 10. PII and retention

- **Marketing leads** (future tables): document lawful basis, retention, and RLS per Legal; never log email/phone in application logs.
- **Mirrors:** CSV-derived; treat `instructions` / `addundum_extras` as potentially sensitive — same RLS as rest.

---

## 11. Bibliography (pre-read)

- [Supabase shared responsibility](https://supabase.com/docs/guides/platform/shared-responsibility-model)
- [Going into prod](https://supabase.com/docs/guides/platform/going-into-prod)
