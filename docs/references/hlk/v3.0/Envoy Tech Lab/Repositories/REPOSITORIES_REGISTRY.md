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

**Security:** Do not paste secrets, tokens, or private URLs that bypass normal access control. Use public GitHub URLs or internal URLs only where policy allows.

---

## Registry table

| repo_slug | github_url | class | primary_owner_role | topic_ids | vault_doc_root | notes |
|-----------|------------|-------|--------------------|-----------|----------------|-------|
| kirbe-platform | `https://github.com/<org>/<kirbe-repo>` (operator sets) | platform | System Owner | — | [../KiRBe/](../KiRBe/) | Replace `<org>/<kirbe-repo>` with the live KiRBe application repository. KiRBe Supabase mirrors canonical CSVs per PRECEDENCE. |
| madeira-hlk-runtime | `https://github.com/<org>/<akos-or-madeira-repo>` (operator sets) | platform | AI Engineer | `topic_madeira_research_radar`, `topic_madeira_product_timeline` | [../MADEIRA/](../MADEIRA/) | MADEIRA agent and HLK tooling often ship in the same monorepo as the vault; set URL to the canonical remote for that codebase. |
| client-delivery-pilot | `https://github.com/<org>/<client-project-repo>` (operator sets) | client-delivery | PMO | `topic_pmo_client_delivery_hub` | — | Template row for external delivery repos (e.g. websitz-class). Replace placeholders when the engagement is active. |

### Class values

- **platform** — Holistika product / core technical surface.
- **internal** — Internal tooling (add rows as needed).
- **client-delivery** — Client or engagement-specific repositories.

---

## Cross-references

- [Repositories README](README.md) — policy and folder taxonomy
- [PMO client delivery topic index](../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md)
- [RESEARCH_BACKLOG_TRELLO_REGISTRY.md](../../Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md) — external backlog index (Trello non-SSOT)
