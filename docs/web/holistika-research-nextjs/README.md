# Holistika Research — public Next.js site (frontend handoff)

This folder holds **implementation and measurement docs for the marketing website team**. It is intentionally **separate** from Initiative 14 marketing-ops / process-engineering planning under `docs/wip/planning/14-holistika-internal-gtm-mops/`.

| Document | Purpose |
|----------|---------|
| [`TEAM_SOTA_HLK_WEB.md`](TEAM_SOTA_HLK_WEB.md) | GTM, Meta Pixel, dataLayer, project-intake measurement patterns, env vars, QA. |
| [`contact-api-implementation.md`](contact-api-implementation.md) | `POST /api/contact` — Zod, Turnstile (`siteverify`), service-role client, route handler, React widget excerpt, honeypot/rate limit, Phase A/B captcha audit, Vercel secrets. |

**Business / SLA / field policy (no application code):** [`../../wip/planning/14-holistika-internal-gtm-mops/reports/contact-lead-ingest-spec.md`](../../wip/planning/14-holistika-internal-gtm-mops/reports/contact-lead-ingest-spec.md)

**Database DDL (governance repo):** [`../../../scripts/sql/i14_phase3_staging/20260418_holistika_ops_lead_intake_up.sql`](../../../scripts/sql/i14_phase3_staging/20260418_holistika_ops_lead_intake_up.sql)
