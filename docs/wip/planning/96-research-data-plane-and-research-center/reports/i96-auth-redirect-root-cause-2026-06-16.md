---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: auth-rca
authored: 2026-06-16
audience: J-OP;J-AIC
status: active
---

# I96 magic-link redirect — root cause (2026-06-16)

> **Plain language:** When the magic-link email shows `redirect_to=https://holistikaresearch.com` (marketing) instead of the ERP callback, that is **not** because the operator used the wrong inbox or pasted badly. Supabase Auth **silently swaps** the redirect when it does not accept the URL the app sent — and PKCE links **cannot** be pasted into a different browser anyway.

## What we verified on production (mechanical)

| Check | Result |
|:---|:---|
| Charter host sign-in shell | **PASS** — `erp.holistikaresearch.com/sign-in?next=/research-center` loads B1.5+ form (© 2026) |
| Production bundle auth fix | **PASS** — sign-in chunk uses `window.location.origin + /auth/callback` (no `?next=` on redirect) and `hlk_auth_next` cookie for post-login path |
| Dev-password on Production | **Not available** — `/api/dev/auth-probe` returns "Not available." (by design per lab platform binding SSOT) |

Evidence: production chunk `app/sign-in/page-*.js` contains:

```text
d(g); let e = c(window.location.origin); ... signInWithOtp({ email, options: { emailRedirectTo: e }})
```

So **if** the operator requests a link **from the ERP sign-in page**, the app sends `https://erp.holistikaresearch.com/auth/callback`.

## Why the email still showed marketing (three causes)

1. **Supabase allow-list fallback (most likely)** — GoTrue requires an **exact** match on Redirect URLs. If `https://erp.holistikaresearch.com/auth/callback` is missing or typo'd in Supabase Dashboard → Authentication → URL Configuration, GoTrue **replaces** `redirect_to` with **Site URL** (`https://holistikaresearch.com`) at email issuance. The operator never sees an error.

2. **Link not issued from ERP sign-in** — Magic links sent from Supabase Dashboard "Send magic link" or from the marketing site always use Site URL. Only the ERP `/sign-in` form sends the ERP callback.

3. **PKCE session binding (paste failure class)** — Even with a correct redirect, **pasting** the verify URL into chat/Cursor Browser fails when the link was requested in a different browser session. Symptom: `otp_expired` or marketing landing with no ERP session. Fix: request + click **in the same browser** (see methodology regression report § Auth blocker).

## Registry expectation vs live Dashboard

Canonical row **SUPA-AUTH-04** (`SUPABASE_AUTH_REGISTRY.csv`) records production callback as **active**:

`https://erp.holistikaresearch.com/auth/callback`

AKOS cannot read live Supabase Dashboard from this workspace (no management API env). **Reconcile live allow list to registry** — if live differs, that is the fix.

## Operator clarification (2026-06-16)

Operator confirms **production magic link works** when signing in normally on `erp.holistikaresearch.com` (not paste-to-chat). Remaining L4 gap is **AIC browser capture** — Cursor Browser has no session until operator completes same-tab magic-link flow there.

## Preview / localhost (not compromised)

| Tier | Magic link | Dev-password shortcut | Notes |
|:---|:---|:---|:---|
| **Production** | **Works** (operator confirmed) | Disabled by design | ERP callback fix deployed in bundle |
| **Preview** | Same code as prod | Gates on; password test **fail** (wrong creds in Vercel env — OPS-96-8) | Not a security compromise — automation path only |
| **Localhost :3010** | Needs allow-list + same-tab flow | **B1.5 PASS** via `/api/dev/sign-in` | L3 tier evidence |

1. Supabase project `swrmqpelgoblaquequzb` → **Authentication → URL Configuration → Redirect URLs** — confirm exact row above exists (no trailing slash drift).
2. In **Cursor Browser** (same tab): open ERP sign-in → enter email → Send magic link → open email **on this machine** and click (do not paste URL into chat).
3. After click, land on `/research-center` signed-in → AIC captures operator/director journeys.

## AIC follow-up (scheduled, not dropped)

- Sibling **hlk-erp** deploy already carries callback fix on production bundle — no new ERP code change indicated from bundle inspection.
- Optional: auth redirect live probe script when Supabase management token available (I99 carryover).
- I96 L4 UAT remains **FAIL / BLOCKED-AUTH** until same-browser sign-in succeeds or operator ratifies PWF with B1.5 localhost tier.

Cross-ref: [`artifacts/uat-screenshots/i96-research-center-2026-06-11/00-workflow-notes.md`](../../../../../../artifacts/uat-screenshots/i96-research-center-2026-06-11/00-workflow-notes.md), [`research-center-methodology-regression-2026-06-14.md`](research-center-methodology-regression-2026-06-14.md).
