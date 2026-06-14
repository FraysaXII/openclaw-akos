---
report_type: research-integrity-audit
parent_initiative: INIT-OPENCLAW_AKOS-100
authored: 2026-06-14
audience: J-OP
status: active
---

# Source ledger integrity audit (2026-06-14)

## Executive honesty

The 780-row ledger **passes the Research Action validator** but **does not yet meet operator intent**
for per-component research. Part of it was **volume padding** — that was wrong, and you were right
to challenge it.

## What is real vs padded

| Bucket | Rows | Quality |
|:---|:---:|:---|
| Internal (`SRC-I100-INT-*`) | 260 | **Real paths** — keyword census of repo files touching lab/governance. Useful for cross-initiative sweep; not deep vendor research. |
| External base URLs | 60 unique | **Mostly real** vendor doc paths (Vercel, Cloudflare, GitHub, Sentry, Langfuse, etc.) |
| External hash duplicates (`#1`, `#2`, …) | 463 | **Not distinct sources** — same page counted many times to hit a row-count target. **Must be replaced** with verified section-level citations or removed. |

Sample HTTP checks (2026-06-14):

| URL | Result |
|:---|:---|
| `https://vercel.com/docs/security/shared-responsibility` | 200 OK |
| `https://vercel.com/docs/deployments/deployment-checks` | **404** — path wrong or moved; needs fix |
| `https://developers.cloudflare.com/dns/manage-dns-records/` | 200 OK |
| `https://docs.github.com/en/actions/deployment/about-deployments/deploying-with-github-actions` | 200 OK |
| `https://docs.sentry.io/product/performance/` | 200 OK |
| `https://langfuse.com/docs` | 200 OK |

## Correct research model (per component)

For each of **110 matrix components**, the lab should mint:

1. **Verified doc trace** — 3–10 URLs that resolve (200) and map to governable surfaces.
2. **Superuser probe pack** — what you can see in dashboard/API with your account (not guessed).
3. **Gap row** — what governance artifact is missing (SOP, dimension row, mirror, capability confidence).
4. **Promotion path** — D0→D1→D2→D3 when an active consumer appears (I96, I83, RevOps, etc.).

Row-count targets are **secondary** to this matrix. The seed script is **deprecated for closure**
and will be replaced by `scripts/verify_source_ledger_urls.py` + per-family research packs.

## Remediation (P9)

1. Strip hash-padded external rows; keep ≤60 verified bases until per-component packs land.
2. Add URL verify step to research-action gate (fail on 404 for new external rows).
3. One research pack per `module_family` with active superuser (vercel, cloudflare, github, supabase, sentry, langfuse, stripe, make, n8n, render).
4. D0 `other` family: batch by consumer demand from OPS_REGISTER + CAPABILITY_REGISTRY — not all 83 need D2 today.
