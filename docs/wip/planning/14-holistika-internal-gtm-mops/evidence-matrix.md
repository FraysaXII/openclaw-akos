# Evidence matrix — Initiative 14

| Claim / control | Evidence artifact | Gate |
|-----------------|-------------------|------|
| Phase 0 charter + crosswalk | [`reports/phase-0-charter.md`](reports/phase-0-charter.md), [`reports/website-service-crosswalk.md`](reports/website-service-crosswalk.md) | Initiative `reports/` |
| Phase 0 business-intent synthesis | [`reports/business-intent-synthesis.md`](reports/business-intent-synthesis.md) | Source: [`docs/references/hlk/business-intent/`](../../../references/hlk/business-intent/) |
| Phase 1 CSV merge (when approved) | `py scripts/validate_hlk.py`; git diff `process_list.csv` | [`docs/DEVELOPER_CHECKLIST.md`](../../../DEVELOPER_CHECKLIST.md) |
| Phase 2 v3.0 SOPs | Paths under `docs/references/hlk/v3.0/Admin/O5-1/...` | `validate_hlk.py`, `validate_hlk_vault_links.py` |
| Phase 3 SQL | [`reports/sql-proposal-stack-20260417.md`](reports/sql-proposal-stack-20260417.md) | Operator approval + migration file |
| Phase 3 prod DDL + health | [`decision-log.md`](decision-log.md) D-GTM-3-1; [`reports/supabase-stripe-health-check-20260418.md`](reports/supabase-stripe-health-check-20260418.md) | Operator: Stripe Dashboard webhooks + secrets |
| Phase 4 UAT | [`reports/uat-holistika-contact-funnel-20260417.md`](reports/uat-holistika-contact-funnel-20260417.md) | Qualitative rows per traceability rule; mock customer E2E where automated |
| Public site (Next.js) handoff | [`docs/web/holistika-research-nextjs/README.md`](../../../web/holistika-research-nextjs/README.md) | Governance repo `docs/web/` (not Initiative `reports/`) |
| C3 after D1 | [`decision-log.md`](decision-log.md) D-GTM-C3-ORDER; [`reports/wave-c-weekly-metrics-forum-log.md`](reports/wave-c-weekly-metrics-forum-log.md) | PMO starts forums after D1 credible |
| Wave C — CRM fields (C2) | [`reports/crm-minimum-fields-supabase.md`](reports/crm-minimum-fields-supabase.md), [`decision-log.md`](decision-log.md) D-GTM-C2 | Initiative `reports/` |
| Contact ingest (`lead_intake`) | [`reports/contact-lead-ingest-spec.md`](reports/contact-lead-ingest-spec.md), [`decision-log.md`](decision-log.md) D-GTM-CONTACT-INGEST / D-GTM-CONTACT-CAPTCHA, DDL [`20260418_holistika_ops_lead_intake_up.sql`](../../../../scripts/sql/i14_phase3_staging/20260418_holistika_ops_lead_intake_up.sql) + CAPTCHA columns [`20260419_holistika_ops_lead_intake_captcha_columns_up.sql`](../../../../scripts/sql/i14_phase3_staging/20260419_holistika_ops_lead_intake_captcha_columns_up.sql), [`docs/web/holistika-research-nextjs/contact-api-implementation.md`](../../web/holistika-research-nextjs/contact-api-implementation.md) | Operator MCP / SQL verify |
| Wave C — SLA (C1) | [`decision-log.md`](decision-log.md) D-GTM-C1; v3.0 [SOP-GTM_INBOUND_SLA_001.md](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Growth/SOP-GTM_INBOUND_SLA_001.md) | `validate_hlk_vault_links.py` when link edits |
| Wave C — weekly forum (C3) | [`reports/wave-c-weekly-metrics-forum-log.md`](reports/wave-c-weekly-metrics-forum-log.md) | PMO fills 4 weeks |
| Wave D — vault index (D2) | [`reports/gtm-sop-vault-index.md`](reports/gtm-sop-vault-index.md), [`reports/phase-5-km-checklist.md`](reports/phase-5-km-checklist.md) | `validate_hlk_km_manifests.py` if `_assets/**/*.manifest.md` change |
| KiRBe / Supabase gap | [`reports/kirbe-supabase-gap-summary.md`](reports/kirbe-supabase-gap-summary.md) | N/A (doc) |
| MasterData inventory | [`reports/masterdata-supabase-inventory.md`](reports/masterdata-supabase-inventory.md) | N/A (doc) |
| Strategic GTM narrative (reference) | [`reports/strategic-gtm-narrative-reference.md`](reports/strategic-gtm-narrative-reference.md) | Reference-only; not canonical CSV |
| Event + attribution blueprint (reference) | [`reports/event-attribution-blueprint-reference.md`](reports/event-attribution-blueprint-reference.md) | Reference-only; DDL via sql-proposal |
| Charter north-star + segment (D-GTM-0) | [`decision-log.md`](decision-log.md), [`reports/phase-0-charter.md`](reports/phase-0-charter.md) | Initiative `reports/` |
