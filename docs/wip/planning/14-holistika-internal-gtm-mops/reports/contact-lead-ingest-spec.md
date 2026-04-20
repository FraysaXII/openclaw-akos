# Contact lead ingest — process specification (Initiative 14)

**Date:** 2026-04-18 (CAPTCHA audit 2026-04-19)  
**Persistence:** `holistika_ops.lead_intake` (MasterData / company CRM plane; distinct from KiRBe SaaS).  
**Ingress (engineering):** **B1** — Next.js `POST /api/contact` uses **`SUPABASE_SERVICE_ROLE_KEY`** server-side only (Vercel env). **B2** (SECURITY DEFINER RPC + anon client) remains available if policy requires service role off Vercel.

**Related:** [crm-minimum-fields-supabase.md](crm-minimum-fields-supabase.md) (dictionary). **Application code for the public site (copy into the app repo):** [`docs/web/holistika-research-nextjs/contact-api-implementation.md`](../../../../web/holistika-research-nextjs/contact-api-implementation.md).

**DDL:** Base table [`20260418_holistika_ops_lead_intake_up.sql`](../../../../../scripts/sql/i14_phase3_staging/20260418_holistika_ops_lead_intake_up.sql); CAPTCHA columns [`20260419_holistika_ops_lead_intake_captcha_columns_up.sql`](../../../../../scripts/sql/i14_phase3_staging/20260419_holistika_ops_lead_intake_captcha_columns_up.sql).

---

## 1. Field map — marketing contact form → CRM logical fields

Source UI: Holistika Research **Contact** form (`name`, `email`, `company`, `service`, `message`) plus **session attribution** from the browser (UTM, referrer, page URL).

| UI / payload | Logical CRM field | Required | DB column (see migration) |
|--------------|-------------------|----------|-------------------------|
| `name` | Contact name | Yes | `contact_name` |
| `email` | Contact email | Yes | `contact_email` |
| `company` | Company | No | `company_name` |
| `service` | Service interest / intent | No | `service_interest` |
| `message` | Inquiry body | Yes | `message_body` |
| — | Form kind | Fixed `contact` for this funnel | `form_type` = `contact` |
| UTM / referrer / page URL / UA / tz (session) | Attribution | No (recommended) | `session_metadata` JSONB |
| Derived | Campaign / source summary | No | `source` (short text; e.g. utm_campaign or `direct`) |
| System | Qualification | Default | `qualification_status` = `new` |
| Server (Turnstile) | CAPTCHA provider | When CAPTCHA on | `captcha_provider` (e.g. `turnstile`); **Phase B** first-class column |
| Server (Turnstile) | CAPTCHA verified time | When CAPTCHA on | `captcha_verified_at` timestamptz; **Phase B** column |

**CAPTCHA audit — two layers (both populated on success when Turnstile is enabled):**

- **Phase A — `session_metadata`:** Envelope for DAMA/lineage next to attribution: `captcha_provider`, `captcha_verified_at` (ISO string), `captcha_success: true`. **Never** store raw Turnstile response tokens.
- **Phase B — columns:** Same facts as nullable `captcha_provider` / `captcha_verified_at` for **MAROPS** SQL (`WHERE captcha_verified_at IS NOT NULL`) and indexed reporting. Values are **server-set only** after Cloudflare `siteverify` success (design invariant — not client-supplied).

**Inbound SLA (SOP):** First human response is measured in CRM/ops tools using `created_at` and triage fields (`first_human_touch_at` can be added in a later tranche when ERP writes back).

---

## 2. RLS posture (plain language)

- **Anonymous and authenticated** Supabase clients **must not** read or write `holistika_ops.lead_intake` directly (RLS deny-all policies).
- **Inserts** for public leads happen only from the **Next.js API route** using the **service role** key (server environment only), which bypasses RLS for controlled server-side writes.
- **Future:** ERP or dashboard users may receive **SELECT/UPDATE** via dedicated policies and roles; not in the initial migration.
- **Logging:** Do not log full `message_body` or email in application info-level logs. Do **not** log Turnstile response tokens (SOC).

---

## 3. Spam / abuse

- **Honeypot** hidden field on the contact form; if filled, return **200** with generic success (same as project intake — do not train bots). **No** CAPTCHA verify on honeypot path (cheap exit).
- **Rate limit:** Same pattern as project intake — **5 submissions per 15 minutes per IP** (in-memory map; upgrade to Redis/Upstash for multi-instance if needed).
- **CAPTCHA (Cloudflare Turnstile):** When **`NEXT_PUBLIC_TURNSTILE_SITE_KEY`** and **`TURNSTILE_SECRET_KEY`** are set in the app environment, the Route Handler **requires** a valid `turnstileToken` from the client, verifies via **`siteverify`**, then inserts. **Fail closed** if verification fails (no row). Optional **`CONTACT_TURNSTILE=off`** forces off even if keys exist (documented in web handoff for staged rollouts).
- **Legal / consent:** When Turnstile is enabled, treat as part of bot-mitigation posture; coordinate with Legal if jurisdiction-specific consent copy is required on the public site.

---

## 4. Notifications (product decision)

- **v1:** **Database insert only** — ops pick up leads from Supabase SQL / ERP when wired.
- **Future:** Email to inbox (Resend/SMTP) and/or CRM webhook — separate decision; do not block ingest.

---

## 5. Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| Growth (fields) | *pending* | | |
| Ops (SLA / routing) | *pending* | | |
| Engineering (feasibility) | *repo implementation 2026-04-18* | 2026-04-18 | Spec + DDL + API landed in repo |
| Legal (consent / CAPTCHA) | *coordinate when Turnstile enabled in prod* | | |

**Decision log:** [decision-log.md](../decision-log.md) — **D-GTM-CONTACT-INGEST**, **D-GTM-CONTACT-CAPTCHA**.
