---
parent_initiative: INIT-OPENCLAW_AKOS-96
purpose: operator-validation index — click these, not subagent chats
updated: 2026-06-13
current_tranche: Gap-closure P-G5 — Preview UAT re-run ready
---

# I96 — Operator check links

> **Rule:** Agents update **§ Check now** only (≤7 rows). Subagent chats are not your ratify surface.

---

## Check now — Preview UAT re-run (2026-06-13)

**Pipeline:** Local L3 **PWF** ✓ · Preview **READY** (env vars set) · UAT **re-run pending** · Production **blocked**

**Preview URL (PR #36 — B1.5 authoritative until preview.erp catches up):** https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app/research-center

**Custom Preview domain (verify UI before ratify):** https://preview.erp.holistikaresearch.com/research-center — must show B1.5 UX, not legacy Facts table

| # | Open this | Why |
|:---:|:---|:---|
| 1 | [PR branch Research Center](https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app/research-center) | **B1.5 build** — Preview UAT ratify here until preview.erp matches |
| 2 | [preview.erp (custom Preview domain)](https://preview.erp.holistikaresearch.com/research-center) | Only if POV strip + Preview badge — currently legacy Facts UI ⚠ |
| 3 | [hlk-erp PR #36](https://github.com/FraysaXII/hlk-erp/pull/36) | Latest deploy · Vercel SUCCESS |
| 4 | [Preview UAT charter](uat-i96-research-center-preview-charter-2026-06-13.md) | ≥8 shots @1280 · use PR branch URL |
| 5 | [Domain + CI/CD SSOT](research-center-domain-and-cicd-ssot-2026-06-13.md) | preview.erp vs PR branch · Supabase redirects |
| 6 | [CICD baseline SOP §5 bypass](../../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-CICD_BASELINE_001.md) | `VERCEL_AUTOMATION_BYPASS_SECRET` |
| 7 | [Prior FAIL report](uat-i96-research-center-preview-2026-06-13.md) | SSO wall — superseded on re-run if PASS |

**Re-run script** (use PR branch host until preview.erp shows B1.5):

```powershell
cd c:\Users\Shadow\cd_shadow\openclaw-akos
$env:VERCEL_AUTOMATION_BYPASS_SECRET = "<your-rotated-secret>"
$env:I96_PREVIEW_BASE = "https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app"
node scripts/_one_off/i96_preview_l3_experiential_screenshots.mjs
```

Or say **run browser preview UAT** to watch the walk live.

**Local dev:** [dev sign-in → Research Center](http://localhost:3010/api/dev/sign-in?next=/research-center)

**Production (after deploy):** `https://erp.holistikaresearch.com/research-center`

**Do not ratify I96 production** until Preview UAT PASS (currently **FAIL** on SSO blocker).

---

## Archive — production URLs (holistikaresearch.com)

| Lens | URL |
|:---|:---|
| Default | https://erp.holistikaresearch.com/research-center |
| Operator | https://erp.holistikaresearch.com/research-center?pov=operator |
| Director | https://erp.holistikaresearch.com/research-center?pov=director |
| Sign-in | https://erp.holistikaresearch.com/sign-in?next=%2Fresearch-center |

## Archive — localhost dev

| What | URL |
|:---|:---|
| Dev sign-in | http://localhost:3010/api/dev/sign-in?next=/research-center |
| Operator | http://localhost:3010/research-center?pov=operator |

## Archive — screenshot folders

| Tranche | Folder |
|:---|:---|
| B1.5 L3 (localhost PWF) | `artifacts/uat-screenshots/i96-research-center-v2-b15-2026-06-13/` |
| B1/B2 journey | `artifacts/uat-screenshots/i96-research-center-v2-bc-2026-06-12/` |

## Archive — tranche history

| Wave | Status | Report |
|:---|:---|:---|
| B1 | REJECTED | B1.5 superseded |
| **B1.5** | L3 localhost **PWF** · L4 production pending | [`uat-i96-research-center-b15-experiential-2026-06-13.md`](uat-i96-research-center-b15-experiential-2026-06-13.md) |
| Gap-closure | **Active** — P-G1+P-G1b committed 2026-06-13 | [`research-center-gap-closure-deploy-uat-tranche-2026-06-13.md`](research-center-gap-closure-deploy-uat-tranche-2026-06-13.md) |
| Domain fix | **2026-06-13** | [`research-center-domain-and-cicd-ssot-2026-06-13.md`](research-center-domain-and-cicd-ssot-2026-06-13.md) |

## Archive — planning SSOT

| Topic | Path |
|:---|:---|
| Experiential UAT ladder (+ L3.5/L4 tiers) | [`research-center-experiential-uat-ladder-2026-06-12.md`](research-center-experiential-uat-ladder-2026-06-12.md) |
| Governance corpus | [`research-center-governance-corpus-2026-06-12.md`](research-center-governance-corpus-2026-06-12.md) |
| topic_cluster harmonization | [`topic-cluster-intelligenceops-harmonization-2026-06-13.md`](topic-cluster-intelligenceops-harmonization-2026-06-13.md) |
| Process catalog e2e | [`research-center-process-catalog-e2e-2026-06-13.md`](research-center-process-catalog-e2e-2026-06-13.md) |
| SUBDOMAINS registry (canonical) | `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/SUBDOMAINS_REGISTRY.md` |
