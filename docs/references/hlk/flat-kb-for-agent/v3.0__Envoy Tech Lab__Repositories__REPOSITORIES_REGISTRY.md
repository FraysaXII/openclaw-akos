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
| kirbe-platform | `https://github.com/FraysaXII/kirbe` | platform | System Owner | — | [../KiRBe/](../KiRBe/) | — | — | KiRBe application repository (operator-confirmed 2026-04-15). |
| madeira-hlk-runtime | `https://github.com/FraysaXII/openclaw-akos` | platform | AI Engineer | `topic_madeira_research_radar`, `topic_madeira_product_timeline` | [../MADEIRA/](../MADEIRA/) | `docs/references/hlk/v3.0/` (vault index; add `openapi.yaml` when published) | `topic_hlk_api_portfolio` | Canonical remote from `git remote get-url origin` on the AKOS workspace (2026-04-15). |
| akos-telemetry-ci | `https://github.com/FraysaXII/openclaw-akos` | internal | System Owner | — | — | — | — | Same monorepo remote as `madeira-hlk-runtime`; **internal** class tags Langfuse/log-watcher/drift automation evidence (no second code tree). |
| client-delivery-pilot | `https://github.com/<org>/<client-project-repo>` (operator sets) | client-delivery | PMO | `topic_pmo_client_delivery_hub` | — | — | — | No public delivery repo identified in org audit; keep placeholder until an engagement remote is known. |

### Class values

- **platform** — Holistika product / core technical surface.
- **internal** — Internal tooling (add rows as needed).
- **client-delivery** — Client or engagement-specific repositories.

---

## Cross-references

- [Repositories README](README.md) — policy and folder taxonomy
- [COMPONENT_SERVICE_MATRIX.csv](../../../compliance/COMPONENT_SERVICE_MATRIX.csv) — CTO-chain component/service SSOT
- [SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md](../../Admin/O5-1/Tech/System%20Owner/SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md)
- [PMO client delivery topic index](../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md)
- [RESEARCH_BACKLOG_TRELLO_REGISTRY.md](../../Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md) — external backlog index (Trello non-SSOT)
