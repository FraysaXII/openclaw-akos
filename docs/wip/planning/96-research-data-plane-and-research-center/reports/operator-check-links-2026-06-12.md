---
parent_initiative: INIT-OPENCLAW_AKOS-96
purpose: operator-validation index — click these, not subagent chats
updated: 2026-06-13
current_tranche: Gap-closure P-G1–G6 — Local L3 PWF → Preview blocked → Production blocked
---

# I96 — Operator check links

> **Rule:** Agents update **§ Check now** only (≤7 rows). Subagent chats are not your ratify surface.

---

## Check now — Gap-closure tranche (2026-06-13)

**Pipeline:** Local L3 **PWF** ✓ · Preview **PR open** (Vercel deploy pending) · Production **blocked**

**P-G1 ✓ · P-G1b ✓ (`770e1358`)** · **hlk-erp PR #36** → AIC Preview UAT when Vercel green

| # | Open this | Why |
|:---:|:---|:---|
| 1 | [hlk-erp PR #36](https://github.com/FraysaXII/hlk-erp/pull/36) | B1.5 branch pushed — wait Vercel Preview READY → AIC charter |
| 2 | [SUBDOMAINS registry (canonical)](../../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/Repositories/SUBDOMAINS_REGISTRY.md) | holistikaresearch.com-only — committed P-G1 |
| 3 | [B1.5 L3 PWF report](uat-i96-research-center-b15-experiential-2026-06-13.md) | Localhost done — **does not** satisfy Preview charter |
| 4 | [Preview UAT charter (AIC)](uat-i96-research-center-preview-charter-2026-06-13.md) | Fires after hlk-erp push + Vercel Preview green |
| 5 | [Production UAT charter](uat-i96-research-center-production-charter-2026-06-13.md) | Fires after Preview PASS + main deploy on `erp.holistikaresearch.com` |
| 6 | [IntelligenceOps population pack](intelligenceops-register-i96-population-2026-06-13.md) | Draft CSV rows — radar DUE 2026-06-15 disposition |
| 7 | [Localhost screenshots (B1.5)](artifacts/uat-screenshots/i96-research-center-v2-b15-2026-06-13/01-operator-discover-1280-auth-dev-password.png) | Local dev badge — dev evidence only |

**Local dev:** [dev sign-in → Research Center](http://localhost:3010/api/dev/sign-in?next=/research-center)

**Production (after deploy):** `https://erp.holistikaresearch.com/research-center`

**Never cite removed apex** — see [domain SSOT](research-center-domain-and-cicd-ssot-2026-06-13.md). Product hosts: `holistikaresearch.com` only.

**Do not ratify I96 production** until hlk-erp Preview PR UAT complete.

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
