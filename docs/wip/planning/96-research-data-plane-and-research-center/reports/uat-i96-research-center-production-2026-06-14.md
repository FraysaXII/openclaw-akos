---
report_type: experiential-uat-walk
intellectual_kind: uat_evidence
parent_initiative: INIT-OPENCLAW_AKOS-96
phase: P-G6-production-uat
sharing_label: internal_only
authored: 2026-06-14
last_review: 2026-06-14
audience: J-OP;J-AIC
verdict: FAIL
ladder_tier: L4-Production
capture_session: artifacts/uat-screenshots/i96-research-center-production-2026-06-14/
linked_charter: reports/uat-i96-research-center-production-charter-2026-06-13.md
closure_decision_source: n/a
deploy_verification:
  platform: vercel
  deploy_id: dpl_5ZdeDLcYqaUFYFJ6AR9JYo9vmw4Y
  source_sha: 3787f06
  hostname: erp.holistikaresearch.com
  vercel_production_url: https://hlk-erp-git-main-holistika.vercel.app
  badge_observed: none-on-charter-host
  badge_expected: Production
  vendor_state: READY
  custom_domain_on_vercel_project: false
verdict_history:
  - verdict: FAIL
    date: 2026-06-14
    reason: >-
      Vercel production deploy READY @ 3787f06 but charter hostname serves legacy v1 build;
      /sign-in 404 on erp.holistikaresearch.com; domain not in hlk-erp Vercel project;
      0/8 journey captures; BLOCKED-AUTH for magic-link after domain fix.
---

# I96 Research Center — Production L4 experiential walk (2026-06-14)

> **Purpose:** Production UAT on the mandated host `erp.holistikaresearch.com` per the production UAT charter — proves **Production** badge + B1.5 v2 insight machine + magic-link auth on live ERP after main merge.

## §1 Closure summary

| Target | Actual | Status |
|:---|:---|:---:|
| Vercel production deploy **READY** @ `3787f06` | `dpl_5ZdeDLcYqaUFYFJ6AR9JYo9vmw4Y` state **READY** | **PASS** |
| Charter host serves B1.5 v2 Research Center | Legacy v1 accordion (Documentation / POI / Facts); copyright **2025** | **FAIL** |
| **Production** badge on `erp.holistikaresearch.com` | Not observed | **FAIL** |
| Magic-link entry `/sign-in?next=%2Fresearch-center` on charter host | **404** page | **FAIL** |
| Custom domain on Vercel `hlk-erp` project | `get_project` `domains[]` = only `*.vercel.app` | **FAIL** |
| ≥8 journey PNGs @1280 (Operator + Director) | **0/8** — diagnostic captures only | **FAIL** |
| L3.0 visual review + screenshot validator | Diagnostics reviewed; validator **FAIL** (expected) | **FAIL** |

**Verdict: FAIL** — The Vercel **production build succeeded** on `main` @ `3787f06`, but the **charter hostname is not serving that deployment**. Until `erp.holistikaresearch.com` is attached to the `hlk-erp` Vercel project and propagates, P-G6 cannot pass. Magic-link operator auth is a **second blocker** after domain wiring (operator must click inbox link — not faked here).

---

## §2 Deploy verification (vendor)

| Field | Value |
|:---|:---|
| Platform | Vercel |
| Deploy ID | `dpl_5ZdeDLcYqaUFYFJ6AR9JYo9vmw4Y` |
| Source SHA | `3787f06737a6f6e5932bfb99709cfff975ccbbcf` (`3787f06`) |
| Target | `production` |
| Vendor state | **READY** (polled BUILDING → READY 2026-06-14) |
| Vercel production URL | `https://hlk-erp-git-main-holistika.vercel.app` |
| Charter hostname | `https://erp.holistikaresearch.com` |
| Prior production on main | `6fc9dee` (B1.5 merge) — `dpl_FvQ7u9L5d8DUhTXo4mvogGN6JjW8` |

**Domain drift evidence:** Vercel MCP `get_project` for `hlk-erp` returns `domains: ["hlk-erp-holistika.vercel.app", "hlk-erp-git-main-holistika.vercel.app"]` only — **`erp.holistikaresearch.com` is absent**. Browser walk confirms charter host behaviour diverges from Vercel production URL (v1 vs sign-in redirect).

---

## §3 Auth + domain blockers

### BLOCKED-DOMAIN-DRIFT (primary)

| URL | Observed |
|:---|:---|
| `https://erp.holistikaresearch.com/research-center` | Legacy v1 Research Center; no auth gate; no POV switcher |
| `https://erp.holistikaresearch.com/sign-in?next=%2Fresearch-center` | **404** |
| `https://hlk-erp-git-main-holistika.vercel.app/research-center` | Redirects to magic-link **sign-in** (B1.5+ behaviour) |

### BLOCKED-AUTH (secondary — after domain fix)

On the correct Vercel production stack, operator path is **magic link only** (no dev-password on Production). Automated capture cannot proceed without:

1. Operator opens `https://erp.holistikaresearch.com/sign-in?next=%2Fresearch-center` (once `/sign-in` exists on charter host).
2. Enters work email → **Send magic link**.
3. Clicks link in inbox → lands signed-in on Research Center v2.
4. AIC re-captures 8 journey PNGs @1280 with sidebar collapsed.

Dev-password (`/api/dev/sign-in`) is **CI-only** per Preview charter — **SKIP** on Production.

---

## §4 Browser evidence (diagnostic only)

**Capture tool:** Cursor Browser MCP  
**Session:** [`artifacts/uat-screenshots/i96-research-center-production-2026-06-14/`](../../../../artifacts/uat-screenshots/i96-research-center-production-2026-06-14/)  
**Visual review:** [`agent_visual_review.json`](../../../../artifacts/uat-screenshots/i96-research-center-production-2026-06-14/agent_visual_review.json) — `delegation_allowed: false`  
**Mechanical gate:** `py scripts/validate_uat_screenshot_evidence.py --session-dir …` → **FAIL** (0 journey PNGs; honest)

| File | Route | Finding |
|:---|:---|:---|
| `00-diagnostic-production-landing-1280.png` | `/research-center` on charter host | Legacy v1 — not B1.5 v2 |
| `00-diagnostic-sign-in-404-1280.png` | `/sign-in` on charter host | 404 — magic-link path broken |
| `00-diagnostic-vercel-prod-sign-in-1280.png` | Vercel production URL `/sign-in` | Magic-link form present (supplementary; not charter host) |

**Journey matrix:** 0/8 required captures — **not attempted** on wrong host; would be dishonest to mark PASS.

---

## §5 Production charter rows (P-01..P-06)

| # | Check | Status | Note |
|:---|:---|:---:|:---|
| P-01 | Production badge on charter host | **FAIL** | No badge; v1 UI |
| P-02 | Magic-link sign-in → Research Center | **FAIL** | `/sign-in` 404 on charter host |
| P-03 | Auth callback allow-list | **SKIP** | Cannot test until host serves B1.5 |
| P-04 | SSL / MCP walk | **PASS** | MCP reached charter host; documented drift |
| P-05 | `DATA_MODE=live` honesty | **SKIP** | v2 surface not on charter host |
| P-06 | Freshness strip live mirror | **SKIP** | B2.4 Realtime on Vercel URL only |

---

## §6 Operator L4 checklist (7 items)

| # | Item | Status |
|:---|:---|:---:|
| 1 | Lens differentiation | **FAIL** — v1 accordion only on charter host |
| 2 | Plain-language headlines | **FAIL** — not v2 insight rail |
| 3 | Primary CTA acts in ≤2 steps | **SKIP** |
| 4 | Drawer runbook copy-complete | **SKIP** |
| 5 | Freshness strip matches severity | **SKIP** |
| 6 | v1 accordion still expands | **N/A** — entire page is v1 |
| 7 | Would use before five other tools | **FAIL** — operator cannot reach v2 |

---

## §7 Recovery steps (scheduled — not dropped)

1. **Wire domain** — Add `erp.holistikaresearch.com` to Vercel `hlk-erp` project; confirm DNS points to Vercel production alias. Tracked in [`research-center-domain-and-cicd-ssot-2026-06-13.md`](research-center-domain-and-cicd-ssot-2026-06-13.md).
2. **Verify propagation** — Charter host shows v2 + **Production** badge + working `/sign-in`.
3. **Operator magic-link** — One inbox click to establish session.
4. **Re-run P-G6** — Full 8 journey PNGs + L3.0 review + validator exit 0 before PASS/PWF verdict.

Carryover posture: **scheduled** for domain-fix tranche (not dropped) — see gap-closure L4 row update.

---

## §8 Cross-references

| Artifact | Path |
|:---|:---|
| Production charter | [`uat-i96-research-center-production-charter-2026-06-13.md`](uat-i96-research-center-production-charter-2026-06-13.md) |
| Gap-closure tranche | [`research-center-gap-closure-deploy-uat-tranche-2026-06-13.md`](research-center-gap-closure-deploy-uat-tranche-2026-06-13.md) |
| Preview PWF baseline | [`uat-i96-research-center-preview-2026-06-13.md`](uat-i96-research-center-preview-2026-06-13.md) |
| Domain + CI/CD SSOT | [`research-center-domain-and-cicd-ssot-2026-06-13.md`](research-center-domain-and-cicd-ssot-2026-06-13.md) |
| Experiential ladder L4 | [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md) |
