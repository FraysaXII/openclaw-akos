---
parent_initiative: INIT-OPENCLAW_AKOS-96
purpose: operator-validation index — click these, not subagent chats
updated: 2026-06-13
current_tranche: Gap-closure P-G5 — Preview UAT FAIL (SSO blocker)
---

# I96 — Operator check links

> **Rule:** Agents update **§ Check now** only (≤7 rows). Subagent chats are not your ratify surface.

---

## Check now — Preview UAT blocked (2026-06-13)

**Pipeline:** Local L3 **PWF** ✓ · Preview deploy **READY** · Preview UAT walk **FAIL** (SSO wall) · Production **blocked**

**Preview URL:** https://hlk-erp-git-feat-i96-research-center-b15-holistika.vercel.app/research-center

| # | Open this | Why |
|:---:|:---|:---|
| 1 | [Preview UAT report — FAIL](uat-i96-research-center-preview-2026-06-13.md) | AIC walk blocked — Vercel SSO 401; **0/8** journey shots |
| 2 | [SSO wall diagnostic PNG](../../../../artifacts/uat-screenshots/i96-research-center-preview-2026-06-13/00-diagnostic-vercel-sso-wall-1280.png) | Proof of blocker (not ERP UI) |
| 3 | [hlk-erp PR #36](https://github.com/FraysaXII/hlk-erp/pull/36) | SHA `e47d8b9` · Vercel check SUCCESS · deploy `dpl_8PobeHi92NB1gARScp4SHBXKSy5P` |
| 4 | [Preview UAT charter](uat-i96-research-center-preview-charter-2026-06-13.md) | Re-run after bypass secret or operator Vercel login |
| 5 | [B1.5 L3 PWF (localhost)](uat-i96-research-center-b15-experiential-2026-06-13.md) | Still valid dev evidence — **not** Preview substitute |
| 6 | [CICD baseline SOP §5 bypass](../../../../references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/canonicals/SOP-CICD_BASELINE_001.md) | `VERCEL_AUTOMATION_BYPASS_SECRET` pattern |
| 7 | [Master tranche P-G5](research-center-gap-closure-deploy-uat-tranche-2026-06-13.md) | Merge gate waits Preview PASS |

**Unblock options:** (a) export `VERCEL_AUTOMATION_BYPASS_SECRET` to AIC and re-run `node scripts/_one_off/i96_preview_l3_experiential_screenshots.mjs` · (b) operator completes Vercel SSO in browser then spot-check preview · (c) temporary preview-protection waiver for PR #36.

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
