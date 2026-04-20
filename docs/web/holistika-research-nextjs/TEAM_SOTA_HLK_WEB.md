# TEAM SOTA — Holistika Research web (Next.js marketing site)

**Audience:** Engineers who own the **public Holistika Research** site (Vercel or equivalent).  
**Location:** This file lives in the **governance repo** under `docs/web/holistika-research-nextjs/` so it stays separate from Initiative 14 marketing-ops planning. Copy snippets into your **application** repo.

**Standalone:** GTM, pixels, dataLayer, and env vars are fully specified here. **Contact API source files** are in [`contact-api-implementation.md`](contact-api-implementation.md).

**What this doc is not:** It does not replace the **company process registry** or vault SOPs. For inbound SLA / weekly metrics / GTM vault procedure text, use Initiative 14 planning in `docs/wip/planning/14-holistika-internal-gtm-mops/` — not duplicated here.

---

## 1. What this site is (and is not)

| Layer | Role |
|-------|------|
| **This Next.js app** | Public marketing: pages, forms, GTM, Meta Pixel, optional GA4 via gtag/GTM. |
| **Holistika ERP** (separate app repo) | Internal operator UI. It reads **Supabase** views for org/process data. It does **not** load Meta/GA pixels for public visitors. |
| **Supabase (MasterData-style project)** | Mirrors of governance CSVs, Holistika **company** commercial tables (`holistika_ops` pattern), and KiRBe product data—**only if** your forms or jobs write there. |
| **Stripe** | Payments; server webhooks are handled by **Supabase Edge Functions** in the company backend repo, not by this Next.js app. |

**Boundary:** The marketing site is **not** “wired to ERP” via pixels. Pixels and tags talk to **Google/Meta/etc.** Form submissions talk to **your API, email, or CRM**; the ERP may later **read the same database** through views. Do not expect Facebook Pixel events to appear inside ERP screens.

---

## 2. Reference layout (copy into your production git)

The snippets below match a common App Router layout. A **throwaway reference tree** may have shown the same files; **your shipped app** should contain the code copied from this document.

Work is described in **two layers**:

1. **Foundation** — GTM + Meta route tracking:
   - **`app/layout.tsx`:** Renders **Google Tag Manager** when `GOOGLE_GTM_KEY` is set (`@next/third-parties/google`), and mounts a client **Meta Pixel** wrapper so route changes fire **PageView**.
   - **`utils/meta-fbm/pixel-events.tsx`:** Lazy-loads `react-facebook-pixel`, calls `init` + `pageView` when the pathname or query string changes.
   - **Environment:** `GOOGLE_GTM_KEY`, `FACEBOOK_PIXEL_ID`, `NEXT_PUBLIC_SITE_URL` documented in §3.

2. **Measurement contract (lead forms)** — treat these as the **contract** for structured measurement:
   - **`lib/gtm-data-layer.ts`** — typed `dataLayer.push` helpers and `pushLeadIntent` for GTM.
   - **`components/forms/ProjectIntakeForm.tsx`** — after a **successful** `POST /api/project-intake`, fires `pushLeadIntent` + `gtag('event','lead_intent',…)` with a shared **`event_id`** for deduplication.

**Contact page** may be a different component: apply the **same post-success pattern** (dataLayer + gtag, no PII in the layer) wherever a lead is submitted. **Contact API + DB insert:** [`contact-api-implementation.md`](contact-api-implementation.md).

---

## 3. Environment variables (production)

Set in **Vercel → Project → Settings → Environment Variables** (or your host’s equivalent). Redeploy after changes.

| Variable | Purpose |
|----------|---------|
| `GOOGLE_GTM_KEY` | GTM container ID (`GTM-XXXX`). If unset, the GTM snippet is not rendered. |
| `NEXT_PUBLIC_SITE_URL` | Canonical site URL for metadata and Open Graph. |
| `FACEBOOK_PIXEL_ID` | Meta Pixel ID for the client pixel wrapper. |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL (also used by contact route). |
| `SUPABASE_SERVICE_ROLE_KEY` | **Server only** — required for `POST /api/contact` → `holistika_ops.lead_intake`. See [`contact-api-implementation.md`](contact-api-implementation.md). |
| `NEXT_PUBLIC_TURNSTILE_SITE_KEY` | Browser — Cloudflare Turnstile widget (optional; see contact doc). |
| `TURNSTILE_SECRET_KEY` | **Server only** — Turnstile `siteverify`. |
| `CONTACT_TURNSTILE` | Optional — set `off` to disable Turnstile even when keys are set. |

**Secrets:** Never commit API keys. Only use `NEXT_PUBLIC_*` for values that must be exposed to the browser.

---

## 4. Event taxonomy (why names matter)

Holistika ties **web event names** to a **measurement discipline** owned by **Growth**, aligned with the registry item **`env_tech_dtp_243`** (event/attribution discipline). In practice:

- Use **one consistent name** for the same user action (e.g. `lead_intent`) in **dataLayer**, **gtag**, and GTM triggers.
- Put **business fields** in parameters (`form_type`, `cta_location`, `event_id`, scores)—**not** email or phone in `dataLayer` unless Legal/Data Protection explicitly approves.
- **`event_id`:** Generate once per successful submit (e.g. `crypto.randomUUID()`); reuse the same value in **dataLayer** and **gtag** so Meta/GA deduplication can work if you add server-side sends later.

---

## 5. Exact code — copy into your production git

Paths match a typical Holistika Research layout; adjust if your tree differs.

### 5.1 `lib/gtm-data-layer.ts` (full file)

```typescript
/**
 * Initiative 14 Wave E1 — structured dataLayer pushes for GTM (Holistika Research).
 * Use alongside existing gtag events; keep event names aligned with env_tech_dtp_243 / Growth owner.
 */

declare global {
  interface Window {
    dataLayer?: Record<string, unknown>[];
  }
}

export type GtmBusinessEvent = {
  event: string;
  /** Use for Meta browser/server deduplication when dual-firing */
  event_id?: string;
  /** Non-PII business context */
  form_type?: string;
  content_topic?: string;
  lead_score_bucket?: string;
};

function pushPayload(payload: Record<string, unknown>) {
  if (typeof window === "undefined") return;
  window.dataLayer = window.dataLayer ?? [];
  window.dataLayer.push(payload);
}

/** Push a named event after GTM has initialized the dataLayer */
export function pushGtmEvent(e: GtmBusinessEvent) {
  pushPayload({
    event: e.event,
    ...(e.event_id ? { event_id: e.event_id } : {}),
    ...(e.form_type ? { form_type: e.form_type } : {}),
    ...(e.content_topic ? { content_topic: e.content_topic } : {}),
    ...(e.lead_score_bucket ? { lead_score_bucket: e.lead_score_bucket } : {}),
  });
}

/** Example: lead intent (aligns with existing lead_intent gtag usage) */
export function pushLeadIntent(opts: {
  formType?: string;
  eventId?: string;
}) {
  pushGtmEvent({
    event: "lead_intent",
    form_type: opts.formType,
    event_id: opts.eventId,
  });
}
```

### 5.2 `app/layout.tsx` — GTM + Meta (excerpt)

```tsx
import { GoogleTagManager } from "@next/third-parties/google";
import { FacebookPixelEvents } from '../utils/meta-fbm/pixel-events'

const gtmId = process.env.GOOGLE_GTM_KEY;

// In RootLayout:
{gtmId ? <GoogleTagManager gtmId={gtmId} /> : null}
// ...
<Suspense fallback={null}>
  <FacebookPixelEvents />
</Suspense>
```

### 5.3 `utils/meta-fbm/pixel-events.tsx` (full file)

```tsx
"use client";
import React, { useEffect } from "react";
import { usePathname, useSearchParams } from "next/navigation";


export const FacebookPixelEvents: React.FC = () => {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const facebookPixelID = process.env.FACEBOOK_PIXEL_ID as string;

  useEffect(() => {
    import("react-facebook-pixel")
      .then((x) => x.default)
      .then((ReactPixel) => {
        ReactPixel.init(facebookPixelID);
        ReactPixel.pageView();
      });
  }, [pathname, searchParams]);

  return null;
};
```

### 5.4 `components/forms/ProjectIntakeForm.tsx` — after successful API response

**Summary**

| Area | What to do |
|------|------------|
| Import | `import { pushLeadIntent } from "@/lib/gtm-data-layer";` |
| Submit | Keep existing `POST /api/project-intake` with `formData` + `sessionMetadata` (URL, referrer, UTM, GA client id helper, device context, timestamp). |
| After `response.ok` | Clear draft, show success toast, **then** measure: `dedupeId` → `pushLeadIntent({ formType: "project_intake", eventId: dedupeId })` → `window.gtag('event', 'lead_intent', { …, event_id: dedupeId })`. |
| Order | Measurement **only after** server success so failed requests do not pollute analytics. |

**Measurement block (after success toast, before redirect/callback):**

```tsx
      const dedupeId =
        typeof crypto !== "undefined" && crypto.randomUUID
          ? crypto.randomUUID()
          : `lead_${Date.now()}`;
      pushLeadIntent({ formType: "project_intake", eventId: dedupeId });
      if (window.gtag) {
        window.gtag("event", "lead_intent", {
          cta_text: "Send project brief",
          cta_location: "make_a_project_form",
          destination: "/make-a-project",
          lead_score: result.data.leadScore,
          service_track: formData.serviceTrack,
          budget_range: formData.budgetRange,
          company_size: formData.companySize,
          value: result.data.leadScore,
          event_id: dedupeId,
        });
      }
```

Keep **`getGA4ClientId()`** and **`sessionMetadata`** for **server-side** routing and CRM—do not push PII into `dataLayer`.

---

## 6. Step-by-step — tools and owners

### 6.1 Vercel (or host)

1. Open the **Holistika Research** project → **Settings → Environment Variables**.
2. Set `GOOGLE_GTM_KEY`, `FACEBOOK_PIXEL_ID`, `NEXT_PUBLIC_SITE_URL` for **Production** (and Preview if you test there). Add Supabase vars per §3 if you ship contact ingest.
3. **Redeploy** the latest commit (or trigger “Redeploy” on the production deployment).
4. Open the live site in a private window and confirm the page loads with **no console errors** from the pixel (missing `FACEBOOK_PIXEL_ID` will break the dynamic import path—fix env before release).

### 6.2 Google Tag Manager

1. In [tagmanager.google.com](https://tagmanager.google.com), open the **container** that matches `GOOGLE_GTM_KEY`.
2. **Tags:** Ensure you have tags that listen for **Custom Event** or **dataLayer** pushes (e.g. event name `lead_intent`) and forward to GA4 / Ads as designed by Growth.
3. **Triggers:** Create a trigger that fires on the event name you push from code (`lead_intent`) or on **Data Layer Variable** conditions (`form_type`, `cta_location`) if you use them.
4. **Preview:** Click **Preview**, enter your production or staging URL, submit a **test** lead. In Tag Assistant, confirm the **dataLayer** contains `event: "lead_intent"` and non-PII fields.
5. **Submit → Publish** when QA passes (follow your change-management rule: who approves GTM publishes).

### 6.3 GA4 (if wired through GTM)

1. In **Google Analytics** → **Admin** → your **Web** data stream, confirm the **Measurement ID** matches what GTM uses.
2. Use **Configure → DebugView** (or GA4’s real-time) while GTM Preview is running; submit a test lead and confirm the **conversion/event** appears with expected parameters.
3. If events are missing, fix **GTM tags/triggers** first—changing only React code will not help if the container does not subscribe to the event.

### 6.4 Meta (Facebook) Pixel

1. In **Meta Events Manager**, select your **Pixel** (same ID as `FACEBOOK_PIXEL_ID`).
2. Open **Test events** (or use the browser helper). Load your site; confirm **PageView** fires on navigation.
3. For **lead** events: either map `lead_intent` from GTM to Meta, or use Meta’s **Conversions API** later—keep the same **`event_id`** in browser and server when you dual-fire.
4. Record **Test event** screenshots or IDs for your release notes if Marketing requires evidence.

### 6.5 Contact form → API + Supabase

**Full drop-in code:** [`contact-api-implementation.md`](contact-api-implementation.md) (Zod, service client, Turnstile verify, `app/api/contact/route.ts`, honeypot, rate limit, Phase A + B captcha audit).

**Contract summary:** `POST /api/contact` on the same origin. **Persistence:** `holistika_ops.lead_intake`. **RLS:** `anon` / `authenticated` denied on the table; inserts use **`SUPABASE_SERVICE_ROLE_KEY`** only in the Route Handler. **CAPTCHA:** optional Cloudflare Turnstile — server `siteverify` before insert; **no** raw tokens stored; **`session_metadata`** + optional columns per process spec.

**Process spec (fields, notifications, SLA intent — no code):** [`../../wip/planning/14-holistika-internal-gtm-mops/reports/contact-lead-ingest-spec.md`](../../wip/planning/14-holistika-internal-gtm-mops/reports/contact-lead-ingest-spec.md)

**Phase B DDL (operator):** [`../../../scripts/sql/i14_phase3_staging/20260419_holistika_ops_lead_intake_captcha_columns_up.sql`](../../../scripts/sql/i14_phase3_staging/20260419_holistika_ops_lead_intake_captcha_columns_up.sql)

---

## 7. QA checklist (before you call it “done”)

1. **GTM Preview:** Test lead → `lead_intent` visible in Tag Assistant / dataLayer.
2. **GA4 DebugView or Realtime:** Event appears if GA4 is connected through GTM.
3. **Meta Test events:** PageView + any mapped conversion.
4. **Backend:** Lead visible in the agreed channel (inbox/CRM/DB).
5. **Privacy:** No unnecessary PII in `dataLayer` or public analytics params.

---

## 8. Security

- Do not log full PII in client consoles in production.
- Cookie / consent banners must **gate** non-essential tags per your **GDPR** posture and GTM **Consent Mode** setup (configure in GTM + legal review).
