# Initiative 18 — FINOPS counterparty mirror + cutover (staging)

Operator-approved targets only. Promote to `supabase/migrations/` after `operator-sql-gate.md` sign-off.

| File | Intent |
|------|--------|
| [`20260423_i18_finops_counterparty_mirror_up.sql`](20260423_i18_finops_counterparty_mirror_up.sql) | Create `compliance.finops_counterparty_register_mirror`, migrate from `finops_vendor_register_mirror`, drop vendor mirror, add `holistika_ops.stripe_customer_link.finops_counterparty_id`, optional `stripe_gtm` hardening |
| [`20260423_i18_finops_counterparty_mirror_rollback.sql`](20260423_i18_finops_counterparty_mirror_rollback.sql) | Break-glass rollback (recreate empty vendor mirror; drop counterparty; drop bridge column) — **data loss** without backup |

**Governance:** CSV SSOT is [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../../../docs/references/hlk/compliance/FINOPS_COUNTERPARTY_REGISTER.csv). DML upserts stay out of migrations—use `py scripts/verify.py compliance_mirror_emit`.
