# Initiative 14 — Wave B round-up (2026-04-17)

**Purpose:** Single place to see what landed in git for **Wave B** and what still needs a human operator / live systems — before **Waves C–D** (business SOP execution and UAT/KM).

## Delivered in repository (Wave B)

| Area | Location | Notes |
|------|----------|--------|
| **B1 — DDL §4–§6** | [`scripts/sql/i14_phase3_staging/20260417_i14_phase3_up.sql`](../../../../../scripts/sql/i14_phase3_staging/20260417_i14_phase3_up.sql) | `compliance` mirrors + `holistika_ops` stub + RLS + grants (idempotent policies). |
| Rollback | [`20260417_i14_phase3_rollback.sql`](../../../../../scripts/sql/i14_phase3_staging/20260417_i14_phase3_rollback.sql) | Destructive — review before use. |
| §8 verification | [`verify_staging.sql`](../../../../../scripts/sql/i14_phase3_staging/verify_staging.sql) | Counts + `pg_tables.rowsecurity`. |
| Verify helper | [`scripts/verify_phase3_mirror_schema.py`](../../../../../scripts/verify_phase3_mirror_schema.py) | Wraps `verify_staging.sql` via `psql` when `DATABASE_URL` / `SUPABASE_DB_URL` is set. |
| **B2 — Legacy deprecation** | [`20260417_deprecate_legacy_public_optional.sql`](../../../../../scripts/sql/i14_phase3_staging/20260417_deprecate_legacy_public_optional.sql) | Commented template; adjust names per DB. |
| **B3 — Stripe routing** | [`supabase/functions/stripe-webhook-handler/`](../../../../../supabase/functions/stripe-webhook-handler/README.md) | `metadata.akos_billing_plane`; `holistika_ops` customer upsert; subscription events skip `kirbe` when plane is Holistika. |

## Operator / staging checklist (not automated here)

1. **Backup** staging (or dedicated pre-prod) Supabase project.
2. **Execute** `20260417_i14_phase3_up.sql` in SQL editor or migration pipeline.
3. **Load mirrors:** `py scripts/sync_compliance_mirrors_from_csv.py --output mirrors.sql` → review → execute.
4. **Verify:** `py scripts/verify_phase3_mirror_schema.py` or paste `verify_staging.sql`.
5. **B2 (optional):** Edit and run deprecation SQL after inventory of real `public` object names.
6. **B3:** `supabase functions deploy stripe-webhook-handler`, set secrets, register URL in Stripe, **`stripe listen` / `stripe trigger`** for regression.

## Waves C–D (next)

| Wave | Focus | Backlog |
|------|--------|---------|
| **C** | Numeric SLA, CRM fields, weekly metrics forum | [`EXECUTION-BACKLOG.md`](EXECUTION-BACKLOG.md) C1–C3 |
| **D** | Contact funnel UAT, KM manifests | [`EXECUTION-BACKLOG.md`](EXECUTION-BACKLOG.md) D1–D2 |

**Governance:** Production DDL remains separate sign-off per [`operator-sql-gate.md`](operator-sql-gate.md) and [`decision-log.md`](../decision-log.md) **D-GTM-3-1**.
