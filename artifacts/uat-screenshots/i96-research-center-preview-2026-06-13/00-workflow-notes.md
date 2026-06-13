# I96 Preview L3.5 — experiential capture attempt (2026-06-13)

**Scope:** Operator + Director @1280 · discover → triage → drawer-open → audit · Vercel Preview host  
**Tool:** Playwright (`scripts/_one_off/i96_preview_l3_experiential_screenshots.mjs`) + Cursor Browser MCP  
**Preview URL:** https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app/research-center  
**PR:** https://github.com/FraysaXII/hlk-erp/pull/36 · SHA `e47d8b9`  
**Auth attempted:** dev-password (`/api/dev/sign-in?next=…`) — **blocked before ERP auth**

## Blocker (binding)

**Vercel Deployment Protection** returns **HTTP 401** on all preview routes. Browser and Playwright redirect to `vercel.com/login` (Vercel SSO). `VERCEL_AUTOMATION_BYPASS_SECRET` **not set** in this execution environment.

Per CICD baseline SOP §5, automation requires `x-vercel-protection-bypass` header or operator Vercel session cookie.

## Agent self-verify (L3.0)

| File | Research Center heading | Full-page UI | Verdict |
|:---|:---:|:---:|:---|
| `00-diagnostic.png` | ✗ | ✗ (Vercel login wall) | **INVALID** — not ERP |
| `01`–`08` journey shots | — | — | **NOT CAPTURED** (SSO timeout) |

## Recovery path (operator / AIC)

1. Set `VERCEL_AUTOMATION_BYPASS_SECRET` in session env (Vercel project → Deployment Protection → Automation bypass), **or**
2. Operator completes Vercel SSO once and re-runs capture from authenticated browser, **or**
3. Temporarily disable preview protection for PR #36 walk (re-enable after UAT).

Re-run: `node scripts/_one_off/i96_preview_l3_experiential_screenshots.mjs`
