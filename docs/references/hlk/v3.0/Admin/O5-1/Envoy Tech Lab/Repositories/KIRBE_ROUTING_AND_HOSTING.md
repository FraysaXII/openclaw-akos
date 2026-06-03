---
language: en
status: active
last_review: 2026-06-01
linked_initiative: docs/wip/planning/90-routing-and-wiring/
ratifying_decisions:
  - D-IH-90-W
  - D-IH-90-X
  - D-IH-90-Y
linked_decisions:
  - D-IH-90-X
  - D-IH-90-Y
---

# KiRBe routing and hosting (canonical)

**Item type:** Canonical routing map (see [PRECEDENCE.md](../../People/Compliance/canonicals/PRECEDENCE.md))  
**SSOT for:** which repo hosts which surface, which hostname each client calls, and what Vercel vs Render vs Cloudflare each do.  
**Do not duplicate:** Repo-local SOPs under `kirbe/docs/kirbe_sops/` and `hlk-erp/other_documentation/kirbe/` remain *how-to* runbooks; they must **cite this file** for hostnames and plane split instead of re-stating routing tables.

**Verified 2026-06-01:** `GET https://kirbe.holistikaresearch.com/health` → **200** (full FastAPI on Render, proxied). Production Vercel kirbe project → **health-only** (`b5958c2` on `main`).

---

## Three surfaces (mental model)

| Surface | Repo | Host | Runtime | Maturity | Who calls it |
|---------|------|------|---------|----------|--------------|
| **KiRBe API (full)** | [`kirbe`](https://github.com/FraysaXII/kirbe) (`kirbe-platform`) | **`https://kirbe.holistikaresearch.com`** | **Render** web service (Gunicorn/Uvicorn); DNS/edge via **Cloudflare** on `holistikaresearch.com` zone | **Production** — live ingestion, tasks, vaults, docs API | GDrive SOP scripts, automation, **hlk-erp server** (`KIRBE_API_URL`), future SaaS backend |
| **Operator ERP + embedded KiRBe lab** | [`hlk-erp`](https://github.com/FraysaXII/hlk-erp) | **`https://erp.holistika.com`** (Vercel) | Next.js on Vercel | **Production** (Mission Control); Tech Lab Kirbe **beta / underdeveloped** | Holistika operators (browser) |
| **KiRBe SaaS POC UI** | [`kirbe-frontend`](https://github.com/FraysaXII/kirbe-frontend) | _(Vercel project TBD — not in local `root_cd`)_ | Next.js 16 (experiment) | **POC / stale** (last GitHub push 2026-04-14) | External SaaS experiment only |

**Not the full API:** Vercel project `kirbe` (`kirbe-holistika.vercel.app`) — **health-only gateway** after 2026-06-01; bundle limit (~245 MB) prevents hosting LlamaIndex/Neo4j/long tasks on serverless.

---

## Canonical API base URL

| Use | Value |
|-----|--------|
| **Scripts, GDrive SOP, server proxies** | `https://kirbe.holistikaresearch.com` (no trailing slash) |
| **Health check** | `GET /health` → 200 |
| **OpenAPI** | `https://kirbe.holistikaresearch.com/api/openapi.json` |
| **Swagger UI** | `https://kirbe.holistikaresearch.com/api/docs` |

**Deprecated / do not use for new wiring**

- `https://api.hlk.kirbe.holistikaresearch.com` — appears in older kirbe SOP copies only; not verified live.
- `https://kirbe-holistika.vercel.app` — Vercel health-only; deployment protection may return 401 without SSO.
- `https://your-app.onrender.com` — placeholder in runbooks until replaced with the custom domain above.

---

## hlk-erp → KiRBe (BFF pattern)

Browsers **must not** call the Kirbe API directly with secrets. hlk-erp implements a **same-origin BFF**:

1. Browser → `https://erp.holistika.com/api/kirbe/*` (Next.js route handlers).
2. Server → `fetch(`${process.env.KIRBE_API_URL}/api/v1/...`)` (server env only).

| Item | Location |
|------|----------|
| Client wrappers | `hlk-erp/lib/services/kirbe.ts` |
| BFF routes | `hlk-erp/app/api/kirbe/**` |
| UI (Tech Lab) | `hlk-erp/app/tech-lab/project-kirbe/`, `components/tech-lab/kirbe/` |
| **Required Vercel env** | `KIRBE_API_URL=https://kirbe.holistikaresearch.com` |

**Health path:** BFF uses `/health` on the upstream (not `/api/v1/health` — upstream returns 404 there).

### BFF health verification (OPS-90-7 / D-IH-90-Y)

| Probe | URL | Expected when healthy |
|-------|-----|------------------------|
| **Upstream (Render)** | `GET https://kirbe.holistikaresearch.com/health` | **200** JSON `status: ok` |
| **BFF (hlk-erp)** | `GET https://erp.holistika.com/api/kirbe/health` | **200** JSON includes upstream echo + `bff: ok` |
| **Tech Lab UI** | Mission Control → Tech Lab → KiRBe status card | Calls same-origin `/api/kirbe/health` while session active |

**Governance:** **OPS-90-7** closed 2026-06-01 ([hlk-erp PR #26](https://github.com/FraysaXII/hlk-erp/pull/26) → `f96001b`: public `/api/kirbe/health` + structured 503/502). Re-spot-check after each erp production deploy.

**Known failure modes (2026-06-01 audit)**

| Symptom | Likely cause | Remediation owner |
|---------|--------------|-------------------|
| `ERR_SSL_PROTOCOL_ERROR` on `erp.holistika.com` | Vercel/custom-domain TLS or DNS misconfig | System Owner — Vercel project `erp` / domain dashboard |
| **302** → `/sign-in` on `/api/kirbe/health` | Route not in `PUBLIC_PREFIXES` (fixed in hlk-erp PR after `i90-p35-erp-kirbe-bff-health`) | Engineering — merge BFF health PR |
| **503** `KIRBE_API_URL is not configured` | Missing server env on Vercel preview/prod | System Owner — set `KIRBE_API_URL` per env contract above |
| **502** `upstream_unreachable` | Render down, wrong URL, or network block from Vercel region | Engineering + System Owner |

**SOP drift:** `hlk-erp/other_documentation/kirbe/kirbe_sops/sop-hlk-erp-kirbe.md` still documents `NEXT_PUBLIC_API_BASE_URL` + direct browser calls — **superseded by BFF + `KIRBE_API_URL`** for Mission Control. Update that SOP in-repo when next touching hlk-erp kirbe docs (pointer-only here to avoid duplicating steps).

---

## Security posture (operator wiring)

| Concern | Posture |
|---------|---------|
| **Secrets in browser** | Avoid `NEXT_PUBLIC_*` pointing at Kirbe for authenticated ingestion; use BFF. |
| **CORS** | Kirbe `ALLOWED_ORIGINS` must include `https://erp.holistika.com` if any browser ever hits Kirbe directly; BFF avoids CORS for normal ERP flows. |
| **Multi-tenant** | Kirbe API exposes vaults, documents, memberships with **RLS** (see OpenAPI tag descriptions in live `/` HATEOAS payload). |
| **Service auth** | Kirbe may expect `Authorization` for some routes — configure server-side headers on BFF routes when enabling prod Tech Lab (do not commit keys). |
| **Vercel kirbe project** | Optional `KIRBE_RENDER_API_URL` on Vercel kirbe project surfaces Render hint in health JSON only. |

Explore Kirbe security controls in `kirbe` repo (`app/api/main.py`, Supabase RLS workflow `kirbe-ci-rls-and-auth`) before widening ERP exposure.

---

## Environment contract (hlk-erp)

| Variable | Where set | Value / rule |
|----------|-----------|--------------|
| `KIRBE_API_URL` | Vercel + `.env.local` (**server-only**) | `https://kirbe.holistikaresearch.com` (no trailing slash). Used by `app/api/kirbe/**` BFF route handlers. |
| `NEXT_PUBLIC_*` Kirbe API | **Do not use** for prod | Browser must call `/api/kirbe/*` on the ERP origin, not the Kirbe host directly. |

**Historical note:** production `hlk-erp` on Vercel has carried `KIRBE_API_URL` pointing at this host since **~October 2025** (operator-confirmed 2026-06-01). Ratified under **D-IH-90-X**.

---

## Cloudflare + Render

Operational detail stays in **repo runbooks** (single copy):

- [`kirbe/docs/kirbe_sops/deployment_cloudflare_render.md`](https://github.com/FraysaXII/kirbe/blob/main/docs/kirbe_sops/deployment_cloudflare_render.md)
- [`kirbe/docs/kirbe_sops/render_deployment_gdrive.md`](https://github.com/FraysaXII/kirbe/blob/main/docs/kirbe_sops/render_deployment_gdrive.md)

This canonical only records: **custom domain `kirbe.holistikaresearch.com` → Render service**, Cloudflare proxied on the `holistikaresearch.com` zone.

---

## Subdomain registry alignment

| Registry row | Intent |
|--------------|--------|
| `kirbe` @ `holistikaresearch.com` | **active** — API host (this document) |
| `kirbe` @ `holistika.com` | **reserved** — future operator-facing Kirbe UI on corporate apex if needed ([`SUBDOMAINS_REGISTRY.md`](SUBDOMAINS_REGISTRY.md)) |
| `erp` @ `holistika.com` | **active** — hlk-erp Mission Control |

---

## Vault pairing (OPS-90-6 → I81 P6)

| `process_list` row | Pairing registry | Full SOP retrofit |
|--------------------|------------------|-------------------|
| `env_tech_dtp_255` (KiRBe Multi-Source Connector Setup workstream) | [`pair_env_tech_dtp_255_kirbe_connector_001`](../../People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) | I81 P6 — v3.0 connector / GDrive SOP |
| `env_tech_dtp_256` (KiRBe Canonical Ingestion Envelope) | [`pair_env_tech_dtp_256_kirbe_ingestion_001`](../../People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) | I81 P6 — body + addendum per `pattern_sop_addendum_split` |

Forward charter: [`docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/ops-90-6-kirbe-gdrive-pairing-forward-2026-06-01.md`](../../../../../../../wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/ops-90-6-kirbe-gdrive-pairing-forward-2026-06-01.md).

---

## Related registries

- [`REPOSITORY_REGISTRY.csv`](../../People/Compliance/canonicals/REPOSITORY_REGISTRY.csv) — `kirbe-platform`, `kirbe-frontend`, `hlk-erp`
- [`REPOSITORIES_REGISTRY.md`](REPOSITORIES_REGISTRY.md) — narrative repo list
- [`SUBDOMAINS_REGISTRY.md`](SUBDOMAINS_REGISTRY.md) — DNS / Vercel slugs
- Initiative: [`docs/wip/planning/90-routing-and-wiring/`](../../../../wip/planning/90-routing-and-wiring/)
