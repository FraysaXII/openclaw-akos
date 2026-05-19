---
language: en
---

# Holistika-tracked GitHub repositories (canonical index)

**Item type:** Canonical registry (see [PRECEDENCE.md](../../../compliance/PRECEDENCE.md))  
**SSOT for code trees:** GitHub — not this file  
**Revision:** Operators update rows when repos are added, archived, or ownership changes.

---

## How to use

1. Add or edit a row when Holistika **starts tracking** a repository.
2. Set `github_url` to the canonical HTTPS URL (`https://github.com/org/repo`).
3. Set `vault_doc_root` to the folder under `v3.0/Envoy Tech Lab/` that holds **vault-authored** docs for that product, if any (may be empty until docs exist).
4. Link the row from relevant **topic knowledge indexes** (`topic_ids`).
5. Optional: add a one-line stub under `platform/`, `internal/`, or `client-delivery/` pointing back here.
6. **`api_spec_pointer`:** repo-relative path or stable pattern to the primary OpenAPI/AsyncAPI (or edge-function doc root); use `—` if N/A. Never store secrets.
7. **`api_topic_id`:** optional KM topic (e.g. `topic_hlk_api_portfolio`) for portfolio indexes; use `—` if none.
8. **Join** detailed per-component API metadata in [`COMPONENT_SERVICE_MATRIX.csv`](../../../compliance/COMPONENT_SERVICE_MATRIX.csv) via matching **`repo_slug`** (one repo may map to multiple `component_id` rows).

**Security:** Do not paste secrets, tokens, or private URLs that bypass normal access control. Use public GitHub URLs or internal URLs only where policy allows.

---

## Registry table

| repo_slug | github_url | class | primary_owner_role | topic_ids | vault_doc_root | api_spec_pointer | api_topic_id | notes |
|-----------|------------|-------|--------------------|-----------|----------------|------------------|--------------|-------|
| kirbe-platform | `https://github.com/FraysaXII/kirbe` | platform | System Owner | `topic_kirbe_billing_plane_routing`, `topic_holistik_ops_discovery` | [../KiRBe/](../KiRBe/) | `docs/api_reference.md` (v1.2; add `openapi.yaml` when published) | `topic_hlk_api_portfolio` | KiRBe application repository (operator-confirmed 2026-04-15). **v1.2 production**: 7 connectors (Discord/Gmail/Notion/Web/Google Drive/etc.), hybrid search (BM25 + vector + RRF), audit logging (SOC2/GDPR-ready, 2-year retention), Stripe billing with FDW + webhook, per-tenant usage metering with quotas, WebSocket progress streams, service-first DI, LlamaIndex readers, **its own local Neo4j** (independent of AKOS Neo4j per D-IH-32-M), Pydantic Logfire observability. Tracked by REPO_HEALTH_SNAPSHOT (I32 P7). |
| openclaw-akos | `https://github.com/FraysaXII/openclaw-akos` | platform | AI Engineer | `topic_madeira_platform`, `topic_holistik_ops_discovery` | [../MADEIRA/](../MADEIRA/) | `docs/references/hlk/v3.0/` (vault index; add `openapi.yaml` when published) | — | Canonical remote from `git remote get-url origin` on the AKOS workspace (2026-04-15). I59 P1.1 promoted this row to canonical CSV `REPOSITORY_REGISTRY.csv` (slug renamed from legacy `madeira-hlk-runtime` for repo-slug alignment). |
| akos-telemetry-ci | `https://github.com/FraysaXII/openclaw-akos` | internal | System Owner | — | — | — | — | Same monorepo remote as `madeira-hlk-runtime`; **internal** class tags Langfuse/log-watcher/drift automation evidence (no second code tree). |
| hlk-erp | `https://github.com/FraysaXII/hlk-erp` | platform | System Owner | `topic_holistik_ops_discovery` | — | — | — | **Initiative 32 P7 registration (D-IH-32-K).** Holistika ERP shell — internal operator UI for process registry, organization, components, sales overview. Stack: Next.js 14 + React + shadcn/ui + Tailwind + Supabase Auth + FastAPI. Has 13 local cursor rules with **no AKOS HLK SSOT cross-reference today** (E12); EXTERNAL_REPO_CONTRACT.md + akos-mirror.mdc PR patches staged in I32 P7 reports. Note local `data-ssot.mdc` rule contradicts AKOS PRECEDENCE.md (E13); Q10 supersession recommendation in P10 architecture audit. |
| boilerplate | `https://github.com/FraysaXII/boilerplate` (operator confirms) | reference | Brand Manager | `topic_brand_visual_identity` | — | — | — | **Initiative 32 P11 registration (D-IH-32-N).** Marketing/web boilerplate. Carries Holistika brand assets (Holistika logo SVG, hero gradient, EN/ES/FR i18n), an embedded Obsidian vault snapshot at `app/dashboard/applications/kms/obsidian-holistika-main/` (NOT canonical — live vault is AKOS `docs/references/hlk/v3.0/`), its own Supabase project (10 schemas under `supabase/schemas/`), Pinecone integration, n8n workflows, Sentry. **Reference-only** per D-IH-32-N: no SSOT obligation, no `.cursor/rules/` to seed with akos-mirror.mdc; only the EXTERNAL_REPO_CONTRACT.md is shipped (light-touch). |
| agentuity | `https://github.com/FraysaXII/agentuity` | reference | AI Engineer | — | — | — | — | Agentic-platform comparison/exploration artifact; stale ~7 months per Lane F sweep. |
| app-directory | `https://github.com/FraysaXII/app-directory` | internal | System Owner | — | — | — | — | App-directory experiment. |
| assemblyai | `https://github.com/FraysaXII/assemblyai` | internal | AI Engineer | — | — | — | — | AssemblyAI research notebook. |
| boilerplate-2 | `https://github.com/FraysaXII/boilerplate-2` | internal | System Owner | — | — | — | — | Boilerplate v2 experiment. |
| crew-ai-f | `https://github.com/FraysaXII/crew-ai-f` | internal | AI Engineer | — | — | — | — | CrewAI research exploration. |
| dalle3api | `https://github.com/FraysaXII/dalle3api` | internal | AI Engineer | — | — | — | — | DALL-E 3 API research experiment. |
| e-commerce | `https://github.com/FraysaXII/e-commerce` | internal | System Owner | — | — | — | — | E-commerce v1 experiment. |
| e-commerce2 | `https://github.com/FraysaXII/e-commerce2` | internal | System Owner | — | — | — | — | E-commerce v2 experiment. |
| fastapi-vercel | `https://github.com/FraysaXII/fastapi-vercel` | internal | System Owner | — | — | — | — | FastAPI on Vercel experiment. |
| feature-flag-apple-store | `https://github.com/FraysaXII/feature-flag-apple-store` | internal | System Owner | — | — | — | — | Feature-flag + Apple Store experiment. |
| floating-endpoints | `https://github.com/FraysaXII/floating-endpoints` | internal | AI Engineer | — | — | — | — | Floating endpoints experiment. |
| function-call | `https://github.com/FraysaXII/function-call` | internal | AI Engineer | — | — | — | — | Function-calling research notebook. |
| funk-coding | `https://github.com/FraysaXII/funk-coding` | internal | System Owner | — | — | — | — | Funk coding experiment. |
| gemini-fastapi-rag-pydantic | `https://github.com/FraysaXII/gemini_fastapi_RAG_Pydantic` | internal | AI Engineer | — | — | — | — | RAG + Pydantic + FastAPI research spike. |
| hkassistant | `https://github.com/FraysaXII/hkassistant` | internal | AI Engineer | — | — | — | — | HK assistant experiment. |
| hlk-erp-design | `https://github.com/FraysaXII/hlk-erp-design` | internal | System Owner | — | — | — | — | HLK ERP design exploration artifact. |
| hlk-vercel-payload | `https://github.com/FraysaXII/hlk-vercel-payload` | internal | System Owner | — | — | — | — | Vercel Payload integration experiment (HLK fork). |
| holistika-web | `https://github.com/FraysaXII/holistika-web` | internal | Brand & Narrative Manager | — | — | — | — | Earlier holistika-web iteration; superseded by boilerplate. |
| holistika-website | `https://github.com/FraysaXII/holistika-website` | internal | Brand & Narrative Manager | — | — | — | — | Predecessor of boilerplate marketing site. |
| holistika-websitz-shopify-app | `https://github.com/FraysaXII/holistika-websitz-shopify-app` | client-delivery | PMO | — | — | — | — | Live customer-facing Shopify partnership app; promoted to governed per D-IH-86-AE. |
| homeplace-deploy | `https://github.com/FraysaXII/homeplace-deploy` | internal | System Owner | — | — | — | — | HomePlace deploy experiment. |
| kirbe-frontend | `https://github.com/FraysaXII/kirbe-frontend` | internal | System Owner | — | — | — | — | KiRBe-adjacent frontend experiment. |
| nextjs | `https://github.com/FraysaXII/nextjs` | internal | System Owner | — | — | — | — | Next.js experiment. |
| nextjs-2 | `https://github.com/FraysaXII/nextjs-2` | internal | System Owner | — | — | — | — | Next.js v2 experiment. |
| nextjs-enterprise-boilerplate | `https://github.com/FraysaXII/nextjs-enterprise-boilerplate` | reference | System Owner | — | — | — | — | Enterprise Next.js boilerplate template. |
| nextjs-fastapi-starter | `https://github.com/FraysaXII/nextjs-fastapi-starter` | reference | System Owner | — | — | — | — | Next.js + FastAPI starter template. |
| nextjs-fastapi-supabase-vercel | `https://github.com/FraysaXII/nextjs-fastapi-supabase-vercel` | reference | System Owner | — | — | — | — | Boilerplate template (Next.js + FastAPI + Supabase + Vercel). |
| nextjs-openai-doc-search-starter | `https://github.com/FraysaXII/nextjs-openai-doc-search-starter` | reference | System Owner | — | — | — | — | Next.js + OpenAI doc-search starter template. |
| nextjs-supabase-kit | `https://github.com/FraysaXII/nextjs-supabase-kit` | reference | System Owner | — | — | — | — | Next.js + Supabase boilerplate template. |
| nextjs-with-supabase | `https://github.com/FraysaXII/nextjs-with-supabase` | reference | System Owner | — | — | — | — | Next.js + Supabase boilerplate template. |
| obsidian-holistika | `https://github.com/FraysaXII/obsidian-holistika` | internal | AI Engineer | — | — | — | — | Obsidian-vault Holistika experiment. |
| obsidian-reader | `https://github.com/FraysaXII/obsidian-reader` | internal | AI Engineer | — | — | — | — | Obsidian-vault reader experiment. |
| open-source-ai-artifacts | `https://github.com/FraysaXII/open-source-ai-artifacts` | internal | AI Engineer | — | — | — | — | OSS AI artifacts collection. |
| pinecone-vercel-ai | `https://github.com/FraysaXII/pinecone-vercel-ai` | internal | AI Engineer | — | — | — | — | Pinecone + Vercel AI experiment. |
| platforms-starter-kit | `https://github.com/FraysaXII/platforms-starter-kit` | reference | System Owner | — | — | — | — | Platforms starter-kit template. |
| python-hello-world | `https://github.com/FraysaXII/python-hello-world` | internal | System Owner | — | — | — | — | Python hello-world starter. |
| python-hello-world-2 | `https://github.com/FraysaXII/python-hello-world-2` | internal | System Owner | — | — | — | — | Python hello-world starter v2. |
| questions-2 | `https://github.com/FraysaXII/Questions-2` | internal | AI Engineer | — | — | — | — | Questions v2 experiment. |
| saas1 | `https://github.com/FraysaXII/saas1` | internal | System Owner | — | — | — | — | SaaS v1 experiment. |
| sop-shield-scribe | `https://github.com/FraysaXII/sop-shield-scribe` | internal | System Owner | — | — | — | — | SOP-tooling experiment. |
| subscription-starter | `https://github.com/FraysaXII/subscription-starter` | internal | System Owner | — | — | — | — | Subscription starter experiment. |
| supabase | `https://github.com/FraysaXII/supabase` | reference | System Owner | — | — | — | — | Tracked upstream fork of supabase/supabase. |
| susana-autogen-search | `https://github.com/FraysaXII/Susana-Autogen-Search` | internal | AI Engineer | — | — | — | — | Susana Autogen-Search research. |
| susana-rag | `https://github.com/FraysaXII/susana-rag` | internal | AI Engineer | — | — | — | — | Susana RAG research. |
| susanatest001 | `https://github.com/FraysaXII/susanatest001` | reference | AI Engineer | — | — | — | — | Tracked upstream fork (Susana test 001). |
| system-prompts-and-models-of-ai-tools | `https://github.com/FraysaXII/system-prompts-and-models-of-ai-tools` | reference | AI Engineer | — | — | — | — | Tracked upstream fork (no AKOS contract beyond inventory). |
| tradingagents | `https://github.com/FraysaXII/TradingAgents` | reference | AI Engineer | — | — | — | — | Tracked upstream fork (TradingAgents). |
| v0-efa-slim-crowdfunding-page | `https://github.com/FraysaXII/v0-efa-slim-crowdfunding-page` | internal | AI Engineer | — | — | — | — | v0-generated crowdfunding spike. |
| vercel-payload | `https://github.com/FraysaXII/vercel-payload` | internal | System Owner | — | — | — | — | Vercel Payload integration experiment. |
| visiongen | `https://github.com/FraysaXII/visiongen` | internal | AI Engineer | — | — | — | — | AKOS-internal research output. |
| with-google-analytics | `https://github.com/FraysaXII/with-google-analytics` | internal | System Owner | — | — | — | — | Google Analytics integration experiment. |

### Class values

- **platform** — Holistika product / core technical surface.
- **internal** — Internal tooling (add rows as needed).
- **client-delivery** — Client or engagement-specific repositories.
- **reference** *(NEW Initiative 32 P11, D-IH-32-N)* — Tracked for visual / brand / pattern reference; carries no SSOT obligation. Boilerplate is the seed entry. Reference repos receive only the EXTERNAL_REPO_CONTRACT.md (light-touch); they do not receive the akos-mirror.mdc cursor rule unless they have a `.cursor/rules/` directory already.

---

## Cross-references

- [Repositories README](README.md) — policy and folder taxonomy
- [COMPONENT_SERVICE_MATRIX.csv](../../../compliance/COMPONENT_SERVICE_MATRIX.csv) — CTO-chain component/service SSOT
- [SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md](../../Admin/O5-1/Tech/System%20Owner/SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md)
- [PMO client delivery topic index](../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md)
- [RESEARCH_BACKLOG_TRELLO_REGISTRY.md](../../Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md) — external backlog index (Trello non-SSOT)