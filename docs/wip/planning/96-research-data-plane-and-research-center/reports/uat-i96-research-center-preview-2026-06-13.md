---
report_type: experiential-uat-walk
intellectual_kind: uat_evidence
parent_initiative: INIT-OPENCLAW_AKOS-96
phase: P-G5-preview-uat
sharing_label: internal_only
authored: 2026-06-13
audience: J-OP;J-AIC
verdict: FAIL
ladder_tier: L3.5-Preview
capture_session: artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/
linked_charter: reports/uat-i96-research-center-preview-charter-2026-06-13.md
deploy_verification:
  platform: vercel
  workflow: feature-branch-pr
  pr_url: https://github.com/FraysaXII/hlk-erp/pull/36
  deploy_id: dpl_8PobeHi92NB1gARScp4SHBXKSy5P
  source_sha: e47d8b9
  hostname: https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app
  badge_observed: null
  badge_expected: Preview
  vendor_state: READY
---

# I96 Research Center — Preview L3.5 experiential walk (2026-06-13)

> **Purpose:** AIC execution-seat experiential UAT on the **Vercel Preview** host per the Preview UAT charter — proves deploy + **Preview** badge + branch SHA parity beyond localhost B1.5 PWF.

## §1 Closure summary

| Target | Actual | Status |
|:---|:---|:---:|
| Vercel Preview deploy READY on PR #36 head SHA | GitHub Vercel check **SUCCESS**; inspector `8PobeHi92NB1gARScp4SHBXKSy5P` | **PASS** |
| ≥8 journey PNGs @1280 (Operator + Director) | **0** journey captures | **FAIL** |
| Deploy badge reads **Preview** on captures | Not reached — SSO wall before ERP | **FAIL** |
| Navigate CTA lands ERP/GitHub/KiRBe (not holistika.com) | Not executed — blocked at Vercel auth | **SKIP** |
| L3.0 agent self-verify on all PNGs | 1 diagnostic PNG read — **INVALID** (Vercel login) | **FAIL** |
| Auth path: dev-password on preview | Attempted `/api/dev/sign-in` — never reached ERP | **BLOCKED** |

**Verdict: FAIL** — Preview deploy is **READY** but **Vercel Deployment Protection** (SSO / HTTP 401) prevents the experiential walk. Localhost B1.5 PWF remains the only live UI evidence until bypass or operator-authenticated re-capture.

---

## §2 Deploy verification (vendor)

| Field | Value |
|:---|:---|
| Platform | Vercel |
| PR | [hlk-erp #36](https://github.com/FraysaXII/hlk-erp/pull/36) |
| Head SHA | `e47d8b919f51bf090b405014945fab103fc8d4af` (`e47d8b9`) |
| Preview hostname | `https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app` |
| Deploy ID (inspector) | `dpl_8PobeHi92NB1gARScp4SHBXKSy5P` |
| GitHub Vercel check | **SUCCESS** (2026-06-13) |
| HTTP probe (unauthenticated) | **401** on `/research-center` |

Vercel MCP was unavailable (server error). Deploy state corroborated via `gh pr view 36` status rollup + PR Vercel comment payload.

---

## §3 Browser evidence (L3.5 + L3.0)

**Capture tools:** Cursor Browser MCP + Playwright (`scripts/_one_off/i96_preview_l3_experiential_screenshots.mjs`)  
**Auth attempted:** dev-password — `https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app/api/dev/sign-in?next=/research-center?pov=operator`  
**Blocker:** All routes redirect to `https://vercel.com/login` (Vercel SSO). `VERCEL_AUTOMATION_BYPASS_SECRET` **not set** in execution environment.

**Manifest:** [`artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/MANIFEST.json`](../../../../artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/MANIFEST.json)

### L3.0 self-verify

| File | Heading | Full UI | Agent verdict |
|:---|:---:|:---:|:---|
| `00-diagnostic-vercel-sso-wall-1280.png` | ✗ | ✗ (Vercel login) | **INVALID** |
| `01`–`08` journey shots | — | — | **NOT CAPTURED** |

**Screenshot count:** 1 diagnostic (invalid for charter) · **0** charter-qualified journey shots.

---

## §4 Per-lens journey checklist

| Lens | Discover | Triage | Act (drawer) | Audit | Overall |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Operator** | BLOCKED | BLOCKED | BLOCKED | BLOCKED | **FAIL** |
| **Director** | BLOCKED | BLOCKED | BLOCKED | BLOCKED | **FAIL** |

---

## §5 Blockers + recovery

| ID | Blocker | Owner | Recovery |
|:---|:---|:---|:---|
| **BLK-PREV-01** | Vercel Deployment Protection SSO on `*.vercel.app` preview | System Owner / operator | Provide `VERCEL_AUTOMATION_BYPASS_SECRET` to AIC session **or** operator Vercel login + re-run capture script **or** temporary protection waiver for PR #36 UAT |

**Re-run command (after bypass available):**

```powershell
$env:VERCEL_AUTOMATION_BYPASS_SECRET = "<from Vercel project settings>"
node scripts/_one_off/i96_preview_l3_experiential_screenshots.mjs
```

Per [CICD baseline SOP §5](../../../../references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-CICD_BASELINE_001.md) — `x-vercel-protection-bypass` header pattern.

---

## §6 Cross-cutting charter rows

| Row | Result |
|:---|:---|
| Preview badge on captures | **FAIL** — ERP never rendered |
| Navigate CTA destination check | **SKIP** — blocked |
| No `fixture` chips on T0 | **SKIP** |
| v1 accordion regression | **SKIP** |
| axe | **SKIP** (no post-login route) |

---

## §7 Verdict line

```yaml
verdict: FAIL
deploy_verification:
  platform: vercel
  workflow: feature-branch-pr
  pr_url: https://github.com/FraysaXII/hlk-erp/pull/36
  deploy_id: dpl_8PobeHi92NB1gARScp4SHBXKSy5P
  source_sha: e47d8b9
  hostname: https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app
  badge_observed: null
  badge_expected: Preview
ladder_tier: L3.5-Preview
screenshot_count_journey: 0
screenshot_count_diagnostic: 1
auth_path_attempted: dev-password via /api/dev/sign-in
auth_blocker: vercel-deployment-protection-sso
```

---

## Cross-references

- Charter: [`uat-i96-research-center-preview-charter-2026-06-13.md`](uat-i96-research-center-preview-charter-2026-06-13.md)
- Ladder L3.5: [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md)
- Localhost baseline (does **not** satisfy Preview): [`uat-i96-research-center-b15-experiential-2026-06-13.md`](uat-i96-research-center-b15-experiential-2026-06-13.md)
- Workflow notes: [`artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/00-workflow-notes.md`](../../../../artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/00-workflow-notes.md)
