# TEAM SOTA — Holistika ERP (`hlk-erp` repo)

**Audience:** Engineers working on the Holistika ERP shell (`c:\Users\Shadow\cd_shadow\root_cd\hlk-erp` or team clone).  
**Standalone:** This document is sufficient to operate without opening the Initiative 14 Cursor plan. **Git CSVs in openclaw-akos** remain SSOT for process/org ([`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md)).

## 1. Purpose of Holistika ERP

Internal **operator UI** for process registry, organization, components, sales overview, documentation entry points, and app grid. It is **not** a replacement for canonical **`process_list.csv`** / **`baseline_organisation.csv`** or v3.0 vault SOPs.

## 2. Data rules

- **Read** org/process data from **Supabase views** that project **`compliance.*_mirror`** tables (or equivalent) loaded from **git CSVs**—never hand-edit production rows as SSOT.
- **Legacy `public` tables** (`"Process list"` v2.4, `standard_process`, …) are **deprecated**—do not build new features on them; use mirrors after cutover.
- **RLS:** App uses **JWT**-scoped client for human users; batch/sync jobs use **service role** only where documented. Never log secret values—key paths/categories only.

## 3. SQL and migrations

- **No** ad-hoc production DDL. Proposals go to openclaw-akos or KiRBe initiative **`reports/sql-proposal-*.md`** → operator approval → versioned migration.
- **Staging first** for destructive changes; include rollback and index list.

## 4. Schema map (conceptual)

| Postgres schema | Belongs to | Notes |
|-----------------|------------|--------|
| `compliance` | Taxonomy + **mirrors** of git CSVs | Join keys for ERP screens |
| `holistika_ops` (or name chosen) | **Company** commercial CRM/revenue | Not KiRBe SaaS product billing |
| `kirbe` | KiRBe product runtime | Do not put Holistika company billing here |
| `public` | Legacy / transitional | Deprecating |

ERP **`search_path`** / API layer should document which schema each module hits.

## 5. Auth

- Document **OAuth/OIDC** or Supabase Auth integration per deployment.
- Role labels should map to **`role_owner`** in `baseline_organisation.csv` where possible.

## 6. Local dev

- Clone ERP repo; point env at **staging** Supabase when available; never commit secrets.
- Run ERP unit/e2e tests before release; cross-link SOP deep links to **`docs/references/hlk/v3.0/`** paths in-repo (openclaw-akos submodule or URL per team practice).

## 7. Release order (typical)

1. CSV merge + `validate_hlk.py` in openclaw-akos.
2. Mirror ingest job (idempotent).
3. ERP deploy consuming views.
4. Cutover legacy reads off.

## 8. Security

- **SOC:** No API keys or PII in logs; follow workspace security rules for `[config/schema]` warnings.
- **Webhooks:** Verify signatures; idempotent handlers.

## 9. Related (optional)

- Sibling doc: [`TEAM_SOTA_KIRBE.md`](TEAM_SOTA_KIRBE.md) for KiRBe product repo.
