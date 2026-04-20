# Contact form → `holistika_ops.lead_intake` (Next.js Route Handler)

**Audience:** Frontend engineers shipping the public Holistika Research site.  
**Copy these files into your production repo** (paths are suggestions; align with your tree).

**Do not** expose `SUPABASE_SERVICE_ROLE_KEY` or `TURNSTILE_SECRET_KEY` to the browser.

**Business field mapping and SLA intent:** [`../../wip/planning/14-holistika-internal-gtm-mops/reports/contact-lead-ingest-spec.md`](../../wip/planning/14-holistika-internal-gtm-mops/reports/contact-lead-ingest-spec.md)

**Measurement after success:** [`TEAM_SOTA_HLK_WEB.md`](TEAM_SOTA_HLK_WEB.md) (GTM `pushLeadIntent` + `gtag` only after HTTP success).

---

## Standards (DX / UX / DI / SOC / SSOT / DAMA / OPS / MAROPS)

| Standard | How this design satisfies it |
|----------|------------------------------|
| **SSOT** | Env names, request/response codes, and audit field names match [`contact-lead-ingest-spec.md`](../../wip/planning/14-holistika-internal-gtm-mops/reports/contact-lead-ingest-spec.md) and this file. |
| **DI** | Only the Route Handler verifies Turnstile and inserts; **no** client-supplied `captcha_provider` / `captcha_verified_at` — server sets both after `siteverify`. |
| **SOC** | Secrets server-only; never log Turnstile response tokens or `message_body` in info logs. |
| **DAMA / MAROPS** | **Phase A:** `session_metadata.captcha_*` keys. **Phase B:** nullable columns `captcha_provider`, `captcha_verified_at` (same facts; index-friendly SQL). |
| **UX** | Turnstile managed or invisible mode; clear error on failure; retry with fresh token. GTM only after **201**. |
| **OPS** | Alert on `CAPTCHA_FAILED` vs `INSERT_FAILED` rate; Cloudflare verify latency. |
| **Scalability** | Stateless verify; optional partial index on `captcha_verified_at` (see governance DDL). |

---

## 1. Environment variables

Add to **Vercel → Settings → Environment Variables** (Production):

| Variable | Where used |
|----------|------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Client + server (existing). |
| `SUPABASE_SERVICE_ROLE_KEY` | **Server only** — Route Handler for `lead_intake` insert. |
| `NEXT_PUBLIC_TURNSTILE_SITE_KEY` | Browser — Turnstile widget (optional). |
| `TURNSTILE_SECRET_KEY` | **Server only** — `siteverify`. |
| `CONTACT_TURNSTILE` | Optional; set to `off` to force-disable Turnstile even if keys exist (staging / rollback). |

**Turnstile is required** when both `NEXT_PUBLIC_TURNSTILE_SITE_KEY` and `TURNSTILE_SECRET_KEY` are set **and** `CONTACT_TURNSTILE` is not `off`.

Never prefix the service role or Turnstile secret with `NEXT_PUBLIC_`.

---

## 2. Dependencies

- `@supabase/supabase-js`, `zod` (existing).
- `@marsidev/react-turnstile` (recommended) **or** Cloudflare’s widget script — pick one and keep consistent.

---

## 3. `lib/turnstile.ts` (server-only)

```typescript
const SITEVERIFY = "https://challenges.cloudflare.com/turnstile/v0/siteverify";

export type TurnstileVerifyResult =
  | { success: true }
  | { success: false; errorCodes: string[] };

export async function verifyTurnstileToken(
  token: string | undefined,
  remoteip: string
): Promise<TurnstileVerifyResult> {
  const secret = process.env.TURNSTILE_SECRET_KEY;
  if (!secret) {
    return { success: false, errorCodes: ["missing-secret"] };
  }
  if (!token?.trim()) {
    return { success: false, errorCodes: ["missing-input-response"] };
  }

  const body = new URLSearchParams();
  body.set("secret", secret);
  body.set("response", token.trim());
  if (remoteip && remoteip !== "unknown") body.set("remoteip", remoteip);

  const res = await fetch(SITEVERIFY, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  const json = (await res.json()) as {
    success?: boolean;
    "error-codes"?: string[];
  };

  if (json.success === true) return { success: true };
  return {
    success: false,
    errorCodes: json["error-codes"] ?? ["verify-failed"],
  };
}
```

---

## 4. `lib/schemas/contact.ts`

```typescript
import { z } from "zod";

/** Public marketing contact form (/contact) */
export const ContactFormSchema = z.object({
  name: z.string().min(1, "Name is required").max(200),
  email: z.string().email("Valid email is required").max(320),
  company: z.string().max(300).optional().or(z.literal("")),
  service: z.string().max(100).optional().or(z.literal("")),
  message: z.string().min(1, "Message is required").max(20000),
  /** Honeypot — must stay empty for humans */
  honeypot: z.string().optional(),
});

export type ContactFormData = z.infer<typeof ContactFormSchema>;

export const ContactSessionMetadataSchema = z
  .object({
    pageUrl: z.string().max(2000).optional(),
    referrer: z.string().max(2000).optional(),
    userAgent: z.string().max(2000).optional(),
    utm: z.record(z.string()).optional(),
    timestamp: z.string().optional(),
  })
  .passthrough();

/** Top-level POST body */
export const ContactPostBodySchema = z.object({
  formData: ContactFormSchema,
  sessionMetadata: ContactSessionMetadataSchema.optional(),
  /** Turnstile response token; required when Turnstile is enabled */
  turnstileToken: z.string().min(1).optional(),
});

export function isTurnstileEnabled(): boolean {
  if (process.env.CONTACT_TURNSTILE === "off") return false;
  return Boolean(
    process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY?.trim() &&
      process.env.TURNSTILE_SECRET_KEY?.trim()
  );
}
```

---

## 5. `utils/supabase/service.ts` (server-only)

```typescript
import { createClient } from "@supabase/supabase-js";

/**
 * Server-only Supabase client with service role (bypasses RLS).
 * Use only in Route Handlers / Server Actions — never import from client components.
 */
export function createServiceRoleClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    throw new Error(
      "Missing NEXT_PUBLIC_SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY for server-side inserts"
    );
  }
  return createClient(url, key, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
}
```

---

## 6. `app/api/contact/route.ts` (handler order)

1. Rate limit (IP).  
2. Parse JSON.  
3. Zod `ContactPostBodySchema` (fail fast on bad fields).  
4. Honeypot → `200` `{ success: true }`, **no** Turnstile, **no** insert.  
5. If `isTurnstileEnabled():` require `turnstileToken` → `verifyTurnstileToken` → on failure `422` `{ code: "CAPTCHA_FAILED" }` (never echo token).  
6. Merge `session_metadata` + **Phase A** captcha keys + **Phase B** columns on insert.

```typescript
import { NextRequest, NextResponse } from "next/server";
import {
  ContactPostBodySchema,
  ContactSessionMetadataSchema,
  isTurnstileEnabled,
} from "@/lib/schemas/contact";
import { verifyTurnstileToken } from "@/lib/turnstile";
import { createServiceRoleClient } from "@/utils/supabase/service";

const contactRateLimitMap = new Map<string, { count: number; resetTime: number }>();

export async function POST(request: NextRequest) {
  try {
    const clientIp = getClientIP(request);
    if (await isContactRateLimited(clientIp)) {
      return NextResponse.json(
        {
          success: false,
          error: "Rate limit exceeded. Please wait before submitting again.",
          code: "RATE_LIMITED",
        },
        { status: 429 }
      );
    }

    const body = await request.json().catch(() => null);
    if (!body) {
      return NextResponse.json(
        { success: false, error: "Invalid JSON.", code: "INVALID_JSON" },
        { status: 400 }
      );
    }

    const parsedBody = ContactPostBodySchema.safeParse(body);
    if (!parsedBody.success) {
      return NextResponse.json(
        {
          success: false,
          error: "Validation failed.",
          code: "VALIDATION_ERROR",
          fieldErrors: parsedBody.error.flatten().fieldErrors,
        },
        { status: 422 }
      );
    }

    const { formData, sessionMetadata: rawMeta, turnstileToken } = parsedBody.data;

    if (formData.honeypot?.trim()) {
      return NextResponse.json({ success: true }, { status: 200 });
    }

    const turnstileOn = isTurnstileEnabled();
    if (turnstileOn && !turnstileToken?.trim()) {
      return NextResponse.json(
        {
          success: false,
          error: "Verification required.",
          code: "CAPTCHA_REQUIRED",
        },
        { status: 422 }
      );
    }

    let captchaVerifiedAtIso: string | null = null;
    if (turnstileOn) {
      const captcha = await verifyTurnstileToken(turnstileToken, clientIp);
      if (!captcha.success) {
        console.error("turnstile verify failed:", captcha.errorCodes);
        return NextResponse.json(
          {
            success: false,
            error: "Verification failed. Please try again.",
            code: "CAPTCHA_FAILED",
          },
          { status: 422 }
        );
      }
      captchaVerifiedAtIso = new Date().toISOString();
    }

    const parsedMeta = ContactSessionMetadataSchema.safeParse(rawMeta ?? {});
    const sessionMeta = parsedMeta.success ? parsedMeta.data : {};

    const enriched = {
      ...sessionMeta,
      ipAddress: clientIp,
      userAgent: request.headers.get("user-agent") ?? undefined,
      referrer: sessionMeta.referrer ?? request.headers.get("referer") ?? undefined,
      ...(captchaVerifiedAtIso
        ? {
            captcha_provider: "turnstile",
            captcha_verified_at: captchaVerifiedAtIso,
            captcha_success: true,
          }
        : {}),
    };

    const sourceSummary = buildSourceSummary(enriched.utm);

    const insertRow = {
      form_type: "contact" as const,
      contact_name: formData.name.trim(),
      contact_email: formData.email.trim().toLowerCase(),
      company_name: formData.company?.trim() || null,
      service_interest: formData.service?.trim() || null,
      message_body: formData.message.trim(),
      source: sourceSummary,
      qualification_status: "new",
      session_metadata: enriched,
      ...(captchaVerifiedAtIso
        ? {
            captcha_provider: "turnstile",
            captcha_verified_at: captchaVerifiedAtIso,
          }
        : {
            captcha_provider: null,
            captcha_verified_at: null,
          }),
    };

    const supabase = createServiceRoleClient();
    const { data, error } = await supabase
      .schema("holistika_ops")
      .from("lead_intake")
      .insert(insertRow)
      .select("id")
      .single();

    if (error) {
      console.error("lead_intake insert error:", error.code, error.message);
      return NextResponse.json(
        {
          success: false,
          error: "Could not save your message. Please try again later.",
          code: "INSERT_FAILED",
        },
        { status: 500 }
      );
    }

    return NextResponse.json(
      {
        success: true,
        data: { leadId: data.id },
        message: "Thank you — we received your message.",
      },
      { status: 201, headers: { "Cache-Control": "no-store" } }
    );
  } catch (e) {
    console.error("Contact API error:", e);
    return NextResponse.json(
      {
        success: false,
        error: "Something went wrong. Please try again.",
        code: "INTERNAL_ERROR",
      },
      { status: 500 }
    );
  }
}

function getClientIP(request: NextRequest): string {
  const xForwardedFor = request.headers.get("x-forwarded-for");
  if (xForwardedFor) return xForwardedFor.split(",")[0].trim();
  return (
    request.headers.get("cf-connecting-ip") ||
    request.headers.get("x-real-ip") ||
    "unknown"
  );
}

async function isContactRateLimited(clientIp: string): Promise<boolean> {
  const now = Date.now();
  const windowMs = 15 * 60 * 1000;
  const maxRequests = 5;

  const current = contactRateLimitMap.get(clientIp);
  if (!current || now > current.resetTime) {
    contactRateLimitMap.set(clientIp, { count: 1, resetTime: now + windowMs });
    return false;
  }
  if (current.count >= maxRequests) return true;
  current.count++;
  return false;
}

function buildSourceSummary(utm?: Record<string, string>): string | null {
  if (!utm || Object.keys(utm).length === 0) return null;
  const c = utm.utm_campaign || utm.utm_source;
  return c ? String(c).slice(0, 500) : null;
}
```

**Note:** `captcha_verified_at` in Postgres is `timestamptz`; pass ISO string from JS — Supabase accepts ISO-8601 for timestamptz.

---

## 7. Client — Turnstile + `fetch` (excerpt)

```tsx
"use client";
import { Turnstile } from "@marsidev/react-turnstile";
import { useState } from "react";

// ...
const [turnstileToken, setTurnstileToken] = useState<string | null>(null);

// In JSX when Turnstile enabled (NEXT_PUBLIC_TURNSTILE_SITE_KEY in env):
<Turnstile
  siteKey={process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY!}
  onSuccess={setTurnstileToken}
  onExpire={() => setTurnstileToken(null)}
/>

// On submit:
const res = await fetch("/api/contact", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    formData: { ... },
    sessionMetadata: { ... },
    turnstileToken: turnstileToken ?? undefined,
  }),
});
```

**Only** after `res.ok` and `json.success`, call `pushLeadIntent` + `gtag` — see [`TEAM_SOTA_HLK_WEB.md`](TEAM_SOTA_HLK_WEB.md) §5.4 with `formType: "contact"`. If the site key is unset, omit the widget and omit `turnstileToken` (server must match).

---

## 8. Governance DDL (Phase B columns)

Apply after operator approval in Supabase:

- [`20260419_holistika_ops_lead_intake_captcha_columns_up.sql`](../../scripts/sql/i14_phase3_staging/20260419_holistika_ops_lead_intake_captcha_columns_up.sql)
- Rollback: [`20260419_holistika_ops_lead_intake_captcha_columns_rollback.sql`](../../scripts/sql/i14_phase3_staging/20260419_holistika_ops_lead_intake_captcha_columns_rollback.sql)

**Deploy order:** Apply Phase B SQL in Supabase **before** production enables Turnstile with the insert snippet that sets `captcha_provider` / `captcha_verified_at` (or the insert will error if columns are missing).

---

## 9. Verification

1. With Turnstile keys: test token from Cloudflare test keys; row has `session_metadata.captcha_*` and columns set.  
2. Bad token → `422` `CAPTCHA_FAILED`, no row.  
3. Honeypot → `200`, no verify call, no row.  
4. `anon` cannot `SELECT` on `lead_intake` (RLS).
