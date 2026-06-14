---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: domain-cicd-ssot
authored: 2026-06-13
audience: J-OP;J-AIC
status: active
operator_note: holistika.com is NOT Holistika's domain — DELETE from KB (operator ratified 2026-06-13)
---

# Research Center — domain + Vercel CI/CD SSOT (2026-06-13)

> **Why this exists:** B1.5 check-links and deploy-target logic incorrectly pointed ratify at `erp.holistika.com`. Operator confirmed **2026-06-13: holistika.com is not Holistika's domain** (unknown external party). Intent: **DELETE** all `holistika.com` rows from SUBDOMAINS registry and **strip from KB** — not archive. Deployed ERP uses **`erp.holistikaresearch.com`** only.

## Deployed surfaces (operator ratify)

| Tier | Host | Vercel | Data | Badge |
|:---|:---|:---|:---|:---|
| **Production** | `https://erp.holistikaresearch.com` | **main** branch | `DATA_MODE=live` | Production |
| **Preview** | `https://preview.erp.holistikaresearch.com` | All non-main branches / PRs (Vercel Preview env) | Preview env vars | Preview |
| **Preview (fallback)** | `*.vercel.app` | Auto-generated PR URL (Deployment Protection on) | Preview env | Preview |

**Not UAT hosts:** `hlk-erp-git-main-*.vercel.app` is Vercel’s auto-alias for **main/production** builds — ignore for Preview ratify.

**Critical — `preview.erp` vs PR branch (operator finding 2026-06-13):** Vercel assigns `preview.erp.holistikaresearch.com` to the **latest Preview deployment**, not necessarily open PR #36. Browser verification showed `preview.erp` serving the **legacy Facts table UI** (Import/Export/Add Fact), while `hlk-erp-git-feat-i96-research-center-b15-*.vercel.app` serves **B1.5** (auth-gated sign-in → Research Center v2). Until `preview.erp` shows POV strip + Preview badge + drawer UX, **ratify Preview UAT on the PR branch URL** or re-deploy PR #36 as the newest Preview build.

**Verify which build a host serves:** B1.5 has POV selector, deploy badge, prong strip — not “Import / Export / Add Fact”. `curl -I` `Content-Length` alone is insufficient (legacy preview pages can be large).

## Vercel environment variables (per tier — do not share across tiers)

| Variable | Production | Preview | Local |
|:---|:---|:---|:---|
| `NEXT_PUBLIC_APP_URL` | `https://erp.holistikaresearch.com` | `https://preview.erp.holistikaresearch.com` | `http://localhost:3010` |
| `ALLOW_PREVIEW_DEV_SIGNIN` | **unset** | `1` | optional |
| `NEXT_PUBLIC_DEV_PASSWORD_AUTH` | **unset** | `1` | `1` in `.env.local` |
| `DEV_PREVIEW_EMAIL` / `DEV_PREVIEW_PASSWORD` | **unset** | preview user | `.env.local` |
| `VERCEL_AUTOMATION_BYPASS_SECRET` | auto (Vercel) | auto + GitHub secret for CI | local export for scripts |

`NEXT_PUBLIC_VERCEL_ENV` is injected at build via `next.config.mjs` from `VERCEL_ENV` for deploy badge accuracy.

## Supabase Auth (magic link / OAuth)

Add **Redirect URLs** in Supabase Dashboard → Authentication → URL Configuration:

- `https://preview.erp.holistikaresearch.com/auth/callback`
- `https://erp.holistikaresearch.com/auth/callback`

If preview magic links redirect to production, the preview callback is missing from this list.

For **PR branch URLs** (e.g. `hlk-erp-git-feat-i96-*.vercel.app`), add that host’s `/auth/callback` too when running magic-link UAT. **Dev password sign-in** (`/api/dev/sign-in`) does not use redirect URLs — see troubleshooting below.

## Dev sign-in troubleshooting (Preview UAT)

Symptom: plain-text **`Dev sign-in failed: Invalid login credentials`** at  
`/api/dev/sign-in?next=/research-center?pov=operator`.

| HTTP response | Meaning | Fix |
|:---|:---|:---|
| Vercel HTML “Authentication Required” | Deployment Protection (SSO wall) | Log into Vercel in browser, or send `x-vercel-protection-bypass: $VERCEL_AUTOMATION_BYPASS_SECRET` (SOP §5.1) |
| `Not available in production` (404) | Route blocked on Production | Use Preview URL; never set `ALLOW_PREVIEW_DEV_SIGNIN` on Production |
| `Dev password sign-in disabled` (403) | `NEXT_PUBLIC_DEV_PASSWORD_AUTH` ≠ `1` at build | Set `NEXT_PUBLIC_DEV_PASSWORD_AUTH=1` on **Preview**, redeploy |
| `DEV_PREVIEW_EMAIL and DEV_PREVIEW_PASSWORD must be set` (500) | Preview secrets missing | Set both on **Preview** env in Vercel (not Production) |
| **`Invalid login credentials` (401)** | Supabase rejected email/password | **Operator action** — see checklist below |

**401 checklist (most common Preview failure):**

1. **Same Supabase project** — Preview `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY` must be the project where the user exists (usually same as local `.env.local`).
2. **Create or reset the Auth user** — Supabase Dashboard → Authentication → Users → Add user (or reset password). Email + password must **exactly** match Vercel Preview `DEV_PREVIEW_EMAIL` / `DEV_PREVIEW_PASSWORD` (no extra spaces; email is case-insensitive).
3. **Role mapping** — After sign-in succeeds, user needs `holistika_ops.user_role_mapping` with `access_level >= 4` or Research Center redirects to `/auth/role-resolve`. Local UAT user typically has level 6; replicate that row for the preview email if missing.
4. **Redeploy after env change** — `NEXT_PUBLIC_DEV_PASSWORD_AUTH` is baked at build time; changing Preview env vars requires a new Preview deployment.

**UAT identity (no paid `@holistikaresearch.com` mail required):**

- **No Supabase password reset required** for Preview UAT if `fay.njoya@gmail.com` already exists — set Vercel Preview `DEV_PREVIEW_EMAIL` / `DEV_PREVIEW_PASSWORD` to match the **existing** Auth password (same password all your systems use).
- **`DEV_PREVIEW_EMAIL` must be exactly** `fay.njoya@gmail.com` (not `uat@example.com`, not a plus-alias unless that alias is the Auth user email).
- **Special characters in Vercel:** paste password in the dashboard UI only (no surrounding quotes). Avoid trailing newline when copy-pasting. If CLI was used to set env vars, `$` and `\` may have been mangled — re-save in the Vercel UI. After any change, **redeploy Preview**.
- **Alternative without storing password in Vercel:** use **magic-link UAT** on Preview (`/sign-in?next=/research-center`) — your real inbox receives the link; no `DEV_PREVIEW_PASSWORD` needed.
- **`uat@example.com` often fails at Supabase user creation** — Auth abuse protection or domain blocklists; plus **live auth triggers** block new users (see live DB discovery report). Use existing Gmail user for M0.
- **Magic-link UAT** needs redirect URLs configured; **dev-password UAT** does not send email.

**Exact Vercel Preview env vars (names must match code):**

| Variable | Preview value | Production |
|:---|:---|:---|
| `ALLOW_PREVIEW_DEV_SIGNIN` | `1` | **unset** |
| `NEXT_PUBLIC_DEV_PASSWORD_AUTH` | `1` | **unset** |
| `DEV_PREVIEW_EMAIL` | same email as Supabase Auth user | **unset** |
| `DEV_PREVIEW_PASSWORD` | same password as Supabase Auth user | **unset** |
| `NEXT_PUBLIC_SUPABASE_URL` | Holistika project URL | same project |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | anon key for that project | same project |

**Browser UAT next step:** After 401 is cleared (303 redirect + `sb-*-auth-token` cookie), open  
`https://<preview-host>/api/dev/sign-in?next=/research-center?pov=operator`  
→ expect Research Center v2 with POV strip + Preview badge. Capture 1280 screenshots per B1.5 charter.

## CI/CD + observability gaps (I96 P-G5, 2026-06-13)

| Gap | Status | Remediation |
|:---|:---|:---|
| Preview Playwright in CI with bypass header | Partial — SOP §5.1 + template exist; hlk-erp PR #36 not yet wired to `preview.erp` smoke post-merge | Add `playwright/auth.setup.ts` + CI job on `deployment_status` |
| Vercel env-specific `NEXT_PUBLIC_APP_URL` | Operator must set per environment | This SSOT table |
| Supabase multi-host redirect allow-list | Operator action | URLs above |
| Sentry release tag `hlk-erp@<sha>` on Preview | `.env.example` has DSN; verify Preview `tracesSampleRate: 0` per SOP §5.2 posture | Vercel Preview env |
| Vercel Runtime / Observability logs | Available in Vercel dashboard; not yet in AKOS UAT evidence | Optional: log drain row in OPS_REGISTER |
| `vercel curl` / CLI smoke in release checklist | Documented in Vercel docs; not in hlk-erp README | Add to Preview UAT charter prerequisites |

Cross-ref: [CI/CD baseline SOP §5.1](../../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-CICD_BASELINE_001.md) (Deployment Protection bypass).
| **Showcase (demo)** | `showcase.holistikaresearch.com` | Separate showcase project | `DATA_MODE=demo` | Preview / demo banner |
| **Local dev** | `http://localhost:3010` | Not Vercel | Dev `.env.local` | Local dev |

**B1.5 code on your machine is not on Vercel until committed, pushed, and deployed** — localhost L3 evidence does not prove production.

## Drift (canonical vs deployed)

| Source | ERP production hostname | Status |
|:---|:---|:---|
| **hlk-erp `.env.example`** | `erp.holistikaresearch.com` | **Deployed SSOT** (operator + UAT) |
| **v1 browser UAT auth allow-list** | `erp.holistikaresearch.com/auth/callback` | **Binding** |
| **SUBDOMAINS_REGISTRY** (`erp` @ `holistika.com`) | `erp.holistika.com` | **DELETE** — operator ratified strip from KB; see [`subdomains-registry-reconciliation-proposal-2026-06-13.md`](subdomains-registry-reconciliation-proposal-2026-06-13.md) |
| **I96 B1.5 docs (wrong, fixed 2026-06-13)** | `erp.holistika.com` | **Retired** from check-links |

**P-G1:** DELETE holistika.com registry rows; holistikaresearch.com-only topology. **P-G1b:** KB purge (~36 files, ~105 grep hits). Until purge completes, **check-links and deploy-target use holistikaresearch.com only**.

## Preview workflow (operator ratified 2026-06-13)

Feature branch → **PR to main** → Vercel Preview URL on PR → AIC Preview UAT → merge → Production on `erp.holistikaresearch.com`.

## Vercel CI/CD bar (Research Center)

Per [Vercel environment docs](https://vercel.com/docs/deployments/environments):

1. **Preview** — every PR / non-production branch → test on generated URL; badge **Preview**.
2. **Production** — merge to production branch → `erp.holistikaresearch.com`; badge **Production**.
3. **Never label localhost or unmerged local edits as Production** in operator check-links.

## Agent binding (L3.0 extension)

Before READY FOR REVIEW:

- [ ] Check-links production rows use **`erp.holistikaresearch.com`** only
- [ ] Agent opened at least one **navigate** CTA and confirms destination is ERP route, GitHub AKOS blob, or KiRBe — **not** marketing apex `holistika.com`
- [ ] Screenshot deploy badge matches hostname (Local dev on localhost)

## Cross-references

- SUBDOMAINS_REGISTRY: `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/SUBDOMAINS_REGISTRY.md`
- Deploy target code: `hlk-erp/lib/research-center/deploy-target.ts`
- Operator index: [`operator-check-links-2026-06-12.md`](operator-check-links-2026-06-12.md)

## I99 Supabase EG-5 coordination (2026-06-13)

**Sibling initiative:** [I99 Supabase Platform EG-5 Tranche](../../99-supabase-platform-eg5-tranche/master-roadmap.md) (`INIT-OPENCLAW_AKOS-99`).

| Layer | I96 (this thread) owns | I99 owns |
|:---|:---|:---|
| **Hosts / Vercel** | `erp.holistikaresearch.com`, `preview.erp.*`, PR branch URLs, env vars, Deployment Protection bypass | — |
| **Supabase Auth dashboard** | Redirect URL checklist (§ Supabase Auth above) | **Auth registry** (SUPA-MOD-22) — redirect allow-list as governed rows, hooks, providers |
| **DDL applied** | Consumes `20260612093000` RPC + `user_role_mapping` row | Migration ledger repair (D-IH-99-C); P2 Auth spec |
| **Preview UAT script failures** | Use **PR branch URL** not stale `preview.erp` until redeploy; dev-password 401 = Supabase user/env mismatch | Role mapping via `holistika_ops.user_role_mapping` + `current_user_role_mapping()` |

**Do not duplicate:** Redirect URLs stay operational in this SSOT; I99 **canonical** Auth registry rows **reference** these URLs as the I96 consumer binding.

**I99 P5 complete (D-IH-99-J, 2026-06-13):** Vault registries minted — bind ERP work to canonical paths, not wip drafts:

| Registry | Canonical path | I96 consumer rows |
|:---|:---|:---|
| Auth | [`SUPABASE_AUTH_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_AUTH_REGISTRY.csv) | SUPA-AUTH-04..07 redirects; SUPA-AUTH-01 magic link **active** |
| Realtime | [`SUPABASE_REALTIME_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_REALTIME_REGISTRY.csv) | SUPA-RT-02 radar badge; publication DDL **applied** MasterData 2026-06-13 (D-IH-99-K) |
| Storage | [`SUPABASE_STORAGE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_STORAGE_REGISTRY.csv) | ST-17 git-first UAT; ST-11 ERP attachments **scheduled** B2 |

**Specs (still authoritative for behavior):** [P2 Auth](../../99-supabase-platform-eg5-tranche/reports/auth-registry-and-i96-consumer-spec-2026-06-13.md) · [P3 Realtime](../../99-supabase-platform-eg5-tranche/reports/realtime-publication-and-i96-freshness-spec-2026-06-13.md) · [P4 Storage](../../99-supabase-platform-eg5-tranche/reports/storage-bucket-and-gtm-asset-spec-2026-06-13.md)

**Hosted DDL (applied 2026-06-13):** `supabase/migrations/20260613150000_i99_realtime_publication_i96_i62.sql` — MasterData via `supabase db push` (**D-IH-99-K**). **Next:** I96 B2.4 wires hlk-erp Realtime subscription on `public.intelligenceops_register_mirror`.

**After ledger clean:** Re-run preview screenshots against PR branch host with bypass header per § Dev sign-in troubleshooting; expect Research Center heading once auth + role mapping succeed.

## Preview auth outcomes (operator 2026-06-13)

| Path | Result | Notes |
|:---|:---|:---|
| **Magic link** | **PASS** | Operator signed in on PR branch Preview; Research Center v2 shell reachable (`pov=director` observed) |
| **Dev-password** | **PARKED** | Invalid-credentials response despite operator belief password is correct — **not blocking** while magic link works; track as OPS-96-8 |
| **Vercel Deployment Protection** | Bypassed by operator session | AIC automated captures still need `VERCEL_AUTOMATION_BYPASS_SECRET` or operator-authenticated re-walk ([`uat-i96-research-center-preview-2026-06-13.md`](uat-i96-research-center-preview-2026-06-13.md) FAIL on SSO wall) |

**I99 binding (D-IH-99-E):** Magic link is the **active** Preview auth path for I96 consumer UAT. Google Workspace OAuth + custom Supabase Auth templates are **scheduled** under I99 P2/P5 — not implemented in this session.

**Product gap (honest):** Auth PASS ≠ product PASS. Preview still shows env-remediation skeleton when `GH_PAT_PLANNING_READER` / mirror BFF absent; journey steps and CTAs diverge from v2 spec — **I96 B2 tranche** ([`research-center-phase-bc-tranche-plan-2026-06-12.md`](research-center-phase-bc-tranche-plan-2026-06-12.md)), not I99.

