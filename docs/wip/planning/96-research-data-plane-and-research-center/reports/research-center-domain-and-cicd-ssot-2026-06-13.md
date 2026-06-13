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
