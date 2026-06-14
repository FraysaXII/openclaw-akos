Production blocker: `erp.holistika.com` returns SSL error -107; UAT runs localhost-first at `http://localhost:3010/sign-in?next=%2Fresearch-center`.



## Magic-link redirect root cause (2026-06-12 fix)



**Symptom:** Supabase verify URLs in magic-link emails showed `redirect_to=https://holistikaresearch.com` even when the operator requested the link from `http://localhost:3010/sign-in?next=%2Fresearch-center`. Session landed on the marketing site, not the ERP.



**Root cause (not operator error):**



1. **Supabase Auth project config (primary):** GoTrue **Site URL** is set to `https://holistikaresearch.com` (marketing). When the client-supplied `emailRedirectTo` is **not** on the Auth **Redirect URLs** allow list, Supabase **silently replaces** `redirect_to` with Site URL at email issuance time — before the link is clicked.

2. **Allow-list gap:** `http://localhost:3010/auth/callback` (and port 3010 wildcard) were not on the redirect allow list. The ERP dev server for I96 UAT runs on **3010**, not the default 3000.

3. **App code:** `hlk-erp/components/auth/sign-in-form.tsx` already sent `window.location.origin + /auth/callback?next=…` — no hardcoded marketing URL in the ERP repo. The mismatch was server-side fallback, not wrong sign-in page origin.



**Fix applied (hlk-erp):**



- Added `lib/auth/callback-url.ts` — central builder; prefers `NEXT_PUBLIC_APP_URL` over `window.location.origin`.

- Updated sign-in form to pass both `emailRedirectTo` and `redirectTo` via the helper.

- Documented env + allow list in `.env.example`.

- Local `.env.local`: `NEXT_PUBLIC_APP_URL=http://localhost:3010` (not committed).



**Operator action required (Supabase Dashboard — env-only, not in git):**



Project `swrmqpelgoblaquequzb` → **Authentication → URL Configuration → Redirect URLs**. Add:



- `http://localhost:3010/auth/callback` (or `http://localhost:3010/**`)

- `http://localhost:3000/auth/callback` (default Next dev)

- `https://erp.holistikaresearch.com/auth/callback` (production ERP)



**Status: RESOLVED (2026-06-12 operator)** — all three redirect URLs above are on the Supabase Auth allow list.

## Magic-link retest FAILED — session 7 (2026-06-12)

**Symptom:** After allow-list update + dev restart, operator pasted a **fresh** magic-link verify URL — still `redirect_to=https://holistikaresearch.com` (marketing Site URL), not `http://localhost:3010/auth/callback`.

**Root cause (code, not operator):** GoTrue validates `emailRedirectTo` with an **exact string match**. The ERP sign-in form was sending `http://localhost:3010/auth/callback?next=%2Fresearch-center`. That full string does **not** match allow-list entry `http://localhost:3010/auth/callback` (no query). GoTrue silently substitutes Site URL at **issuance** — before the link is clicked. Allow-list entries were correct; the **client payload** was wrong.

**Fix applied (hlk-erp, session 7):**

- `emailRedirectTo` / OAuth `redirectTo` now use **base path only**: `{origin}/auth/callback` (no `?next=`).
- Post-login `next` path stored in short-lived cookie `hlk_auth_next` before OTP/OAuth; `/auth/callback` reads cookie after code exchange.
- Browser `window.location.origin` wins over `NEXT_PUBLIC_APP_URL` when building redirect URL.
- Dev-only `console.info` logs exact `emailRedirectTo` sent (no secrets).

**Retest after fix:** Restart dev server (`PORT=3010 npm run dev`), open `http://localhost:3010/sign-in?next=%2Fresearch-center`, request **new** magic link. Email verify URL must show `redirect_to=http%3A%2F%2Flocalhost%3A3010%2Fauth%2Fcallback` (no `?next=` in redirect_to). Browser devtools console should log `[auth] signInWithOtp` with matching `emailRedirectTo`.



Site URL can stay `https://holistikaresearch.com` for marketing; redirect URLs control magic-link targets.



**Verify:** Restart dev server (`PORT=3010 npm run dev`), open localhost sign-in, request a **new** magic link, inspect email verify URL — `redirect_to` must encode `http://localhost:3010/auth/callback` only (no `?next=` on redirect_to; `next` travels via cookie).

## Magic-link retest blocked — session 8 (2026-06-12)

**Symptom:** Supabase returns **email rate limit exceeded** on Send magic link from localhost sign-in.

**Workaround (UAT continues):** Dev password auth — open in browser:

`http://localhost:3010/api/dev/sign-in?next=/research-center`

(Role-mapping fix from session 4 applied; panel walk already captured at PWF.)

**Magic-link closure:** Retry after Supabase auth email cooldown (typically ~1 hour). Code fix (exact-match callback + cookie `next`) is deployed; verify URL must show marketing-free `redirect_to` before we close the magic-link follow-up item.

**UAT shortcut (already in `.env.local`):** `NEXT_PUBLIC_DEV_PASSWORD_AUTH=1` → `GET /api/dev/sign-in?next=/research-center` bypasses email while rate-limited.

## Dev password sign-in attempt (2026-06-12 session 3)

**Route contract (`app/api/dev/sign-in/route.ts`):**

- `GET /api/dev/sign-in` — no `?next=` support; always `303` → `/mission-control`.
- Requires `NEXT_PUBLIC_DEV_PASSWORD_AUTH=1`, `DEV_PREVIEW_EMAIL`, `DEV_PREVIEW_PASSWORD` in `.env.local`.
- Uses `signInWithPassword`; sets Supabase SSR cookie on redirect response.

**Mechanical result (curl with cookie jar):**

- `GET /api/dev/sign-in` → **303** + `sb-*-auth-token` cookie (password auth **PASS**).
- `GET /research-center` with cookie → page shell renders but `requireLevel(4)` redirects to `/auth/role-resolve` (mapping read **FAIL** in app).
- `GET /mission-control` → **307** → `/auth/role-resolve`; role-resolve RPC level 6 → **307** → `/mission-control` → **redirect loop**.
- `GET /api/research-center/ledger-stats` with cookie → **403** `{"detail":"Forbidden"}`.
- Supabase SQL: `holistika_ops.user_role_mapping` row exists for dev user (`access_level=6`); `/api/me/export` returns `"role_mapping": null` (PostgREST self-read **FAIL**).

**Browser MCP:**

- Following dev sign-in redirect → **`ERR_TOO_MANY_REDIRECTS`** (mission-control ↔ role-resolve).
- Screenshots: `08-dev-signin-redirect-error-{375,768,1280}.png`, `08-research-center-redirect-error-1280.png`.

**Reopen gate:** Fix `getCurrentUser()` / PostgREST read of `public.user_role_mapping` so it matches `current_access_level()` RPC (or add `?next=/research-center` on dev route and skip mission-control hop). Then re-run panel walk + axe.

