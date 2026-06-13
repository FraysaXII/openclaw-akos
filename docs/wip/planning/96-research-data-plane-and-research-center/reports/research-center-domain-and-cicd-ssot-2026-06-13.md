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
| **Production** | `https://erp.holistikaresearch.com` | Production project on **main** merge | `DATA_MODE=live` | Production |
| **Preview** | `*.vercel.app` or PR branch URL | Non-main deploy / `vercel` without `--prod` | Usually live or preview env | Preview |
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
