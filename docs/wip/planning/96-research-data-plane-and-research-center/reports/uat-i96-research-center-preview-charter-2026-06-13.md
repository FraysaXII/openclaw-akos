---
report_type: uat-charter
intellectual_kind: uat_evidence
parent_initiative: INIT-OPENCLAW_AKOS-96
phase: P-G5-preview-uat
sharing_label: internal_only
authored: 2026-06-13
audience: J-AIC
deploy_tier: preview
hostname_pattern: "*.vercel.app"
badge_expected: Preview
language: en
status: draft
verdict: PENDING-AIC-WALK
supersedes_localhost: uat-i96-research-center-b15-experiential-2026-06-13.md
linked_ladder: research-center-experiential-uat-ladder-2026-06-12.md
---

# UAT charter — Research Center Preview deploy (AIC-owned)

> **Audience:** J-AIC (execution seat). Operator spot-checks via check-links — not a substitute for this thorough walk.
>
> **Explicit:** Localhost L3 B1.5 PWF ([`uat-i96-research-center-b15-experiential-2026-06-13.md`](uat-i96-research-center-b15-experiential-2026-06-13.md)) **does NOT satisfy** this charter. Preview proves Vercel build + Preview badge + branch SHA parity.

## Deploy target

| Field | Value |
|:---|:---|
| **Tier** | Vercel Preview |
| **Workflow** | **Feature branch → PR to `main`** (operator ratified 2026-06-13) |
| **Hostname** | Vercel **PR preview URL** — from GitHub PR "View deployment" or Vercel dashboard (typically `https://<project>-<git-branch-hash>.vercel.app`) |
| **Badge** | **Preview** (not Local dev, not Production) |
| **Data** | Preview env vars (`DATA_MODE` per Vercel project) |
| **Auth** | Dev-password path if enabled on preview; magic-link only if preview auth configured |

## Prerequisites (gate before walk)

- [ ] B1.5 Research Center changes on **hlk-erp feature branch** (not only local uncommitted)
- [ ] **PR opened** to `main` — Vercel Preview deployment attached to PR
- [ ] Preview URL copied from GitHub PR checks or Vercel (record full URL in UAT frontmatter)
- [ ] Vercel Preview deploy **READY** (vendor MCP: deploy ID + sha + state)
- [ ] L1 mechanical green on PR head SHA (`tsc`, `research-center*.spec.ts`, BFF pytest)
- [ ] L2 contract unchanged or re-ratified (page spec v2, P9b Figma)
- [ ] No navigate CTA or auth callback cites `holistika.com` (KB purge / holistikaresearch.com only)

## Thorough experiential checklist (derived from ladder + B1.5)

### L3.0 self-verify (binding)

- [ ] Agent reads **every** PNG before check-links READY
- [ ] Full-page UI + Research Center heading — not favicon/loader
- [ ] Record VALID/INVALID in session `00-workflow-notes.md`

### Auth matrix (minimum)

| Path | Captures |
|:---|:---|
| Dev-password (if preview allows) | Operator + Director @ 1280 |
| Magic-link (if configured) | Operator @ 1280 + sign-in ready |

### Per-lens journey (Operator + Director T2 — binding)

| Stage | Operator PASS | Director PASS | Filename token |
|:---|:---|:---|:---|
| Discover | Hero, POV, freshness strip, prong strip | Same | `{lens}-discover-1280` |
| Triage | ≥1 headline + navigate CTA | ICS/ledger narrative | `{lens}-triage-1280` |
| Act | Drawer open OR CTA executed | Drawer open | `{lens}-drawer-open-1280` |
| Audit | T3 accordion collapsed default | Optional | `{lens}-audit-1280` |

### Cross-cutting rows

- [ ] Deploy badge reads **Preview** on all captures
- [ ] Navigate CTAs land ERP route / GitHub blob / KiRBe — **not** `holistika.com` apex
- [ ] No `fixture` chips on T0 card face (Gate B)
- [ ] v1 four-panel accordion expands (regression)
- [ ] Impeccable disposition — no open VIS-B blockers without PWF tracker
- [ ] axe PASS or documented SKIP (Python 3.12)

### Stretch (P11 charter — note PASS/SKIP)

- [ ] Auditor / Finance / Compliance lenses @ 1280
- [ ] Operator @ 375 + 768 responsive
- [ ] Drawer Recharts (B1.5-02 stretch)
- [ ] Manifest ≥25 rows (full P11 closure bar)

## Manifest requirements

| Requirement | Minimum |
|:---|:---|
| Folder | `artifacts/uat-screenshots/i96-research-center-preview-<YYYY-MM-DD>/` |
| Shots @ 1280 | **≥ 8** (Operator+Director × discover/triage/drawer/audit) |
| MANIFEST.json | `captures[]` with sha256 + `deploy_tier: preview` + Vercel deploy ID |
| Naming | [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md) §manifest |

## Verdict line template

```yaml
verdict: PASS | PASS-WITH-FOLLOWUP | FAIL | PENDING-AIC-WALK
deploy_verification:
  platform: vercel
  workflow: feature-branch-pr
  pr_url: <github-pr-url>
  deploy_id: dpl_<id>
  source_sha: <7-char>
  hostname: <pr-preview-url>
  badge_observed: Preview
ladder_tier: L3.5-Preview
```

**PASS-WITH-FOLLOWUP** allowed for: magic-link preview parity, KiRBe env on preview, axe SKIP — each with `verdict_followup_rationale` per PWF governance.

## Deliverable report path (on completion)

`reports/uat-i96-research-center-preview-<YYYY-MM-DD>.md`

## Cross-references

- Master tranche P-G5: [`research-center-gap-closure-deploy-uat-tranche-2026-06-13.md`](research-center-gap-closure-deploy-uat-tranche-2026-06-13.md)
- Domain SSOT: [`research-center-domain-and-cicd-ssot-2026-06-13.md`](research-center-domain-and-cicd-ssot-2026-06-13.md)
- v2 charter dimensions: [`uat-i96-research-center-v2-charter-2026-06-12.md`](uat-i96-research-center-v2-charter-2026-06-12.md)
