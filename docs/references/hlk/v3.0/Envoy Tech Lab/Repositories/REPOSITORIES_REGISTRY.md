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
| client-delivery-pilot | `https://github.com/<org>/<client-project-repo>` (operator sets) | client-delivery | PMO | `topic_pmo_client_delivery_hub` | — | — | — | No public delivery repo identified in org audit; keep placeholder until an engagement remote is known. |

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
