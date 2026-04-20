# CRM minimum fields — qualification + BD handoff (Supabase mapping)

**Date:** 2026-04-17  
**Backlog:** [EXECUTION-BACKLOG.md](EXECUTION-BACKLOG.md) **C2**  
**Sources:** [SOP-GTM_INBOUND_SLA_001.md](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Growth/SOP-GTM_INBOUND_SLA_001.md) (CRM minimum table), [SOP-GTM_BD_HANDOFF_001.md](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Growth/SOP-GTM_BD_HANDOFF_001.md) (minimum data + handoff SLA).

## Field dictionary (logical)

| Logical field | SOP anchor | Purpose |
|---------------|------------|---------|
| `source` / UTM | Inbound SLA | Attribution |
| `intent` | Inbound SLA, BD handoff | `services` vs `product` (or team enum) |
| `consent_scope` | Inbound SLA | Lawful basis / comms scope |
| `first_human_touch_at` | Inbound SLA | SLA measurement |
| `assigned_owner` | Inbound SLA | Growth / routing owner |
| Contact | BD handoff §1 | Email / name |
| Company | BD handoff §1 | B2B; optional for sole prop |
| `source_channel` | BD handoff §1 | Align with `source` / UTM |
| Qualification status | BD handoff | e.g. `new` → `qualified` |
| Qualification score / tags | BD handoff §2 | Rubric |
| `bd_owner` | BD handoff | After qualification |
| `qualified_at` | BD handoff §4 | Handoff SLA window |
| `crm_deep_link` | BD handoff runbook | Notify BD |

## Supabase mapping (proposal)

**Status:** Documentation only — **no migration** until operator-approved DDL (same gate as [`sql-proposal-stack-20260417.md`](sql-proposal-stack-20260417.md)).

| Approach | When to use |
|----------|----------------|
| **A — Dedicated table** `holistika_ops.lead_intake` | Company CRM is Postgres-first; dashboard and Edge actions read/write one row per lead. |
| **B — JSONB envelope** | Same table with `payload JSONB` for channel-specific fields (Mailchimp, form vendors) plus indexed keys above. |

Proposed columns (Approach A + optional B):

| Column | Type | Notes |
|--------|------|--------|
| `id` | `UUID` | PK |
| `created_at` | `TIMESTAMPTZ` | Receipt |
| `source` | `TEXT` | UTM / campaign summary |
| `intent` | `TEXT` | Check constraint or enum in app layer |
| `consent_scope` | `TEXT` | |
| `first_human_touch_at` | `TIMESTAMPTZ` | Nullable until triage |
| `assigned_owner` | `TEXT` | Org user id or email |
| `contact_email` | `TEXT` | |
| `contact_name` | `TEXT` | Nullable |
| `company_name` | `TEXT` | Nullable |
| `qualification_status` | `TEXT` | |
| `qualification_tags` | `TEXT[]` or `JSONB` | |
| `bd_owner` | `TEXT` | Nullable until qualified |
| `qualified_at` | `TIMESTAMPTZ` | Nullable |
| `vendor_payload` | `JSONB` | Optional (Approach B) |

**Evidence:** Link this file from [evidence-matrix.md](../evidence-matrix.md).

**Contact funnel (2026-04-18):** Signed-off process spec [`contact-lead-ingest-spec.md`](contact-lead-ingest-spec.md); DDL base [`20260418_holistika_ops_lead_intake_up.sql`](../../../../scripts/sql/i14_phase3_staging/20260418_holistika_ops_lead_intake_up.sql); CAPTCHA audit columns (Phase B) [`20260419_holistika_ops_lead_intake_captcha_columns_up.sql`](../../../../scripts/sql/i14_phase3_staging/20260419_holistika_ops_lead_intake_captcha_columns_up.sql). **Frontend implementation (separate doc tree):** [`docs/web/holistika-research-nextjs/contact-api-implementation.md`](../../../../web/holistika-research-nextjs/contact-api-implementation.md).
