---
report_type: experiential-uat-walk
intellectual_kind: uat_evidence
parent_initiative: INIT-OPENCLAW_AKOS-96
phase: P-G5-preview-uat
sharing_label: internal_only
authored: 2026-06-13
last_review: 2026-06-14
audience: J-OP;J-AIC
verdict: PASS-WITH-FOLLOWUP
ladder_tier: L3.5-Preview
capture_session: artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/
linked_charter: reports/uat-i96-research-center-preview-charter-2026-06-13.md
deploy_verification:
  platform: vercel
  workflow: feature-branch-pr
  pr_url: https://github.com/FraysaXII/hlk-erp/pull/36
  deploy_id: 5VYPNb5wyNfWHisS26X6hfnh9qcq
  source_sha: eedcd1d
  hostname: https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app
  badge_observed: Preview
  badge_expected: Preview
  vendor_state: READY
verdict_history:
  - verdict: FAIL
    date: 2026-06-13
    reason: Vercel SSO wall; bypass secret absent; 0 journey captures
  - verdict: FAIL
    date: 2026-06-14
    reason: Re-run @ d0e4b32 — AIC attempted dev-password path; 401 on /api/dev/sign-in; 0 journey captures (operator auth was magic link, not dev-password)
  - verdict: PASS-WITH-FOLLOWUP
    date: 2026-06-14
    reason: Magic-link session @ eedcd1d — v2 recapture after v1 visual-review failure; validate_uat_screenshot_evidence PASS; Preview env gaps remain
verdict_followup_rationale:
  followup_class: deferred-work-with-tracker
  closure_target: I96 P2 entry
  owner: System Owner
  tracker_path: docs/wip/planning/96-research-data-plane-and-research-center/reports/research-center-domain-and-cicd-ssot-2026-06-13.md
  notes: >-
    Preview env wiring deferred — SUPABASE_SERVICE_ROLE_KEY, GH_PAT_PLANNING_READER,
    research-data connection; target system verdict GREEN on re-capture. Operator auth
    is magic link (confirmed). Dev-password + auth-probe are CI-only (I99).
    BLK-PREV-02 reframed — not operator wrong-password.
---

# I96 Research Center — Preview L3.5 experiential walk (2026-06-13 / magic-link 2026-06-14)

> **Purpose:** AIC execution-seat experiential UAT on the **Vercel Preview** host per the Preview UAT charter — proves deploy + **Preview** badge + branch SHA parity beyond localhost B1.5 PWF.

## §1 Closure summary

| Target | Actual | Status |
|:---|:---|:---:|
| Vercel Preview deploy READY on PR #36 head SHA **`eedcd1d`** | GitHub Vercel check **SUCCESS**; inspector `5VYPNb5wyNfWHisS26X6hfnh9qcq` | **PASS** |
| ≥8 journey PNGs @1280 (Operator + Director) | **8/8** magic-link captures | **PASS** |
| Deploy badge reads **Preview** on captures | Visible on Research Center header (`01`, `05`) | **PASS** |
| Operator auth = **magic link** (not dev-password) | Existing Supabase session; sign-in UI is OTP + OAuth only | **PASS** |
| Planning BigInt fix @ `eedcd1d` — no 500 on `/planning` | Index + I96 detail render gracefully | **PASS** |
| Mirror footer **green** (Tier 0 sync) | Not verified on footer strip this walk | **SKIP** |
| Preview data plane fully wired (ledger rows, planning mirror, radar) | Env gaps; system verdict **RED** | **PWF** |
| CI `preview-uat-capture` (dev-password Playwright) | GitHub check **FAILURE** on `eedcd1d` push — CI-only path | **PWF** |

**Verdict: PASS-WITH-FOLLOWUP** — Preview deploy is **READY** on **`eedcd1d`**. Operator magic-link session reached Research Center and completed the full **8/8** journey matrix with **Preview** badge. Remaining followup is **Preview env data-plane wiring** (not operator authentication).

---

## §2 Deploy verification (vendor)

| Field | Value |
|:---|:---|
| Platform | Vercel |
| PR | [hlk-erp #36](https://github.com/FraysaXII/hlk-erp/pull/36) |
| Head SHA | `eedcd1dec50391d7a4c4c1de164640faa43f4e6b` (`eedcd1d`) |
| Preview hostname | `https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app` |
| Deploy ID (inspector) | `5VYPNb5wyNfWHisS26X6hfnh9qcq` |
| GitHub Vercel check | **SUCCESS** (2026-06-14) |
| Prior SHA (superseded) | `d0e4b32` — deploy `A8KsVat128qV5vqzxwGt7gQ6Mgxh` |

Corroborated via `gh pr view 36 --json headRefOid,statusCheckRollup`.

---

## §3 Auth model (code + operator correction)

**Sign-in surface** (`hlk-erp/components/auth/sign-in-form.tsx`):

| Method | Mechanism | Default |
|:---|:---|:---|
| Magic link | `signInWithOtp` + work email | **Primary operator path** |
| Google OAuth | `signInWithOAuth({ provider: "google" })` | Enabled unless `NEXT_PUBLIC_AUTH_GOOGLE_ENABLED=false` |
| Microsoft OAuth | `signInWithOAuth({ provider: "azure" })` | Enabled unless `NEXT_PUBLIC_AUTH_MICROSOFT_ENABLED=false` |
| Password field | — | **Not present on sign-in UI** |

**Dev-password path** (`/api/dev/sign-in`, `DEV_PREVIEW_*`, `ALLOW_PREVIEW_DEV_SIGNIN`): scoped to **Vercel Preview** for **CI / Playwright** automation only (I99 parked). Operator UAT in this session used an **existing magic-link Supabase session** — not dev-password.

Prior diagnostic `00-diagnostic-dev-signin-401-1280.png` documents CI probe failure only; it is **not** evidence of operator auth failure.

---

## §4 Browser evidence (L3.5 + L3.0)

**Capture tools:** Cursor Browser MCP (magic-link session, 2026-06-14 recapture)  
**Auth:** magic-link Supabase session (operator); session cookie inherited in browser tab  
**Viewport:** CDP `1280×800`; **sidebar collapsed** before each shot (v1 failure mode: expanded sidebar crops)  
**Visual review:** Parent agent read every PNG; [`agent_visual_review.json`](../../../../artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/agent_visual_review.json)  
**Mechanical gate:** `py scripts/validate_uat_screenshot_evidence.py --session-dir …` → **PASS** (2026-06-14)

**Manifest:** [`artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/MANIFEST.json`](../../../../artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/MANIFEST.json)

### Recapture incident (v1 → v2)

| Issue | v1 | v2 recovery |
|:---|:---|:---|
| Subagent claimed VALID without reading PNGs | MANIFEST + report fiction | Foreground visual review + SOP mint |
| Director `06` = `08` (duplicate sha256) | Same triage frame twice | Audit shot scrolled to WIP research packs |
| Director captures sidebar-only (~22KB) | Expanded sidebar ate viewport | Collapse sidebar @ 1280 |
| Operator drawer blurry | Partial crop | `03-…-v2.png` with drawer legible |

### L3.0 self-verify + PNG observations (canonical files)

| File | Lens | Stage | Key observations | Verdict |
|:---|:---|:---|:---|:---:|
| `01-operator-discover-1280-magiclink.png` | Operator | Discover | Research Center h1; Operator POV; Discover journey; RED verdict; 3 signals | **VALID** |
| `02-operator-triage-1280-magiclink.png` | Operator | Triage | Triage active; Ledger not loaded; Open planning index | **VALID** |
| `03-operator-drawer-open-1280-magiclink-v2.png` | Operator | Drawer | Drawer “Research ledger has no loaded rows”; Act/Runbook/Govern | **VALID** (supersedes v1) |
| `04-operator-audit-1280-magiclink.png` | Operator | Audit | WIP packs; GH_PAT warning; no intelligence packs | **VALID** |
| `05-director-discover-1280-magiclink-v2.png` | Director | Discover | **PREVIEW** badge; Director POV; program-phase subtitle | **VALID** (supersedes v1) |
| `06-director-triage-1280-magiclink-v2.png` | Director | Triage | **P10-T2 PAUSED** phase blocker; Open I96 master roadmap | **VALID** (supersedes v1) |
| `07-director-drawer-open-1280-magiclink-v2.png` | Director | Drawer | Drawer P10-T2 PAUSED narrative | **VALID** (supersedes v1) |
| `08-director-audit-1280-magiclink-v2.png` | Director | Audit | WIP research packs panel; GitHub reader warning | **VALID** (supersedes v1) |
| `09-planning-index-1280-magiclink.png` | — | Planning | 0 initiatives; no BigInt crash | **SUPPLEMENTAL** |
| `10-planning-i96-detail-1280-magiclink.png` | — | Planning | Graceful could-not-load (no 500) | **SUPPLEMENTAL** |

**Screenshot count:** 8 charter-qualified journey (5× v2 supersession) · 2 supplemental · v1 director/operator-drawer retained as SUPERSEDED audit trail.

### Top charter-row findings

| # | Charter row | Result | Evidence |
|:---:|:---|:---:|:---|
| 1 | Vercel Preview deploy READY + SHA **`eedcd1d`** | **PASS** | `gh pr view 36` Vercel SUCCESS |
| 2 | **Preview** deploy badge on Research Center | **PASS** | `05-director-discover-1280-magiclink-v2.png` — PREVIEW chip |
| 3 | Operator + Director discover/triage/drawer/audit @1280 | **PASS** | v2 canonical set + `validate_uat_screenshot_evidence.py` PASS |
| 4 | Operator auth = magic link (not dev-password) | **PASS** | Operator correction + sign-in-form.tsx |
| 5 | Planning routes survive @ `eedcd1d` | **PASS** | `09`, `10` — render without 500 |
| 6 | Preview data plane live (ledger, mirror, radar, GREEN verdict) | **PWF** | RED verdict; env messages on all audit captures |
| 7 | CI dev-password capture workflow | **PWF** | `preview-uat-capture` FAILURE — I99 / automation track |

---

## §5 Per-lens journey checklist

| Lens | Discover | Triage | Act (drawer) | Audit | Overall |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Operator** | PASS | PASS | PASS | PASS | **PASS** |
| **Director** | PASS | PASS | PASS | PASS | **PASS** |

**UI shell / journey UX:** PASS on magic-link session. **Live data:** degraded on Preview (expected until env wiring) — tracked as PWF followup, not FAIL.

---

## §6 Blockers + recovery (revised)

| ID | Issue | Layer | Owner | Recovery |
|:---|:---|:---|:---|:---|
| **BLK-PREV-03** | Preview missing `SUPABASE_SERVICE_ROLE_KEY` / planning mirror empty | Data plane | System Owner | Add Preview-scoped service role + redeploy; re-walk `09`/`10` |
| **BLK-PREV-04** | `GH_PAT_PLANNING_READER` unset — WIP packs / markdown drill-ins unavailable | Data plane | System Owner | Add GitHub PAT on Preview tier per domain SSOT |
| **BLK-PREV-05** | Research data connection not configured — prong counts zero | Data plane | System Owner | Wire Preview BFF env per I96 Tier 1 checklist |
| **BLK-PREV-02** *(reframed)* | CI `/api/dev/sign-in` 401 on automation runs | **CI only** | AIC / I99 | Not operator UAT; use auth-probe + aligned Supabase test user when running Playwright |
| **BLK-PREV-01** | `VERCEL_AUTOMATION_BYPASS_SECRET` absent in AKOS `.env.local` | CI only | AIC | Optional for local Playwright; operator browser reached Preview without local secret |

**Carryover posture:** BLK-PREV-03..05 are **scheduled** (not dropped) — closure target when Preview captures show populated ledger + planning mirror row + system verdict not RED. Tracked in [research-center-domain-and-cicd-ssot-2026-06-13.md](research-center-domain-and-cicd-ssot-2026-06-13.md).

---

## §7 Cross-cutting charter rows

| Row | Result |
|:---|:---|
| Preview badge on captures | **PASS** |
| Navigate CTA destination check | **PASS** (drawer Govern links; planning CTAs present — destinations env-dependent) |
| Mirror footer green | **SKIP** — not read on this walk |
| No `fixture` chips on T0 | **SKIP** — prong cards show env warnings, not fixture chips |
| v1 accordion regression | **PASS** — accordion opens on operator + director |
| axe | **SKIP** — not run this session |

---

## §8 Optional CI diagnostic

`/api/dev/auth-probe` — **not called** (no `VERCEL_AUTOMATION_BYPASS_SECRET` in AKOS `.env.local`). CI-only diagnostic per `eedcd1d` commit; does not gate operator magic-link UAT.

---

## §9 Verdict line

```yaml
verdict: PASS-WITH-FOLLOWUP
deploy_verification:
  platform: vercel
  workflow: feature-branch-pr
  pr_url: https://github.com/FraysaXII/hlk-erp/pull/36
  deploy_id: 5VYPNb5wyNfWHisS26X6hfnh9qcq
  source_sha: eedcd1d
  hostname: https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app
  badge_observed: Preview
  badge_expected: Preview
ladder_tier: L3.5-Preview
screenshot_count_journey: 8
screenshot_count_supplemental: 2
screenshot_count_diagnostic: 3
auth_path_operator: magic-link-supabase-session
auth_path_ci_optional: dev-password-via-/api/dev/sign-in
followup_class: preview-env-data-plane-wiring
system_verdict_on_capture: RED
```

---

## Cross-references

- Charter: [`uat-i96-research-center-preview-charter-2026-06-13.md`](uat-i96-research-center-preview-charter-2026-06-13.md)
- Ladder L3.5: [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md)
- Visual review SOP: [`SOP-EXPERIENTIAL_UAT_AGENT_VISUAL_REVIEW_001.md`](SOP-EXPERIENTIAL_UAT_AGENT_VISUAL_REVIEW_001.md)
- Visual review JSON: [`agent_visual_review.json`](../../../../artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/agent_visual_review.json)
- Localhost baseline: [`uat-i96-research-center-b15-experiential-2026-06-13.md`](uat-i96-research-center-b15-experiential-2026-06-13.md)
- Domain + auth SSOT: [`research-center-domain-and-cicd-ssot-2026-06-13.md`](research-center-domain-and-cicd-ssot-2026-06-13.md)
- Workflow notes: [`artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/00-workflow-notes.md`](../../../../artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/00-workflow-notes.md)
