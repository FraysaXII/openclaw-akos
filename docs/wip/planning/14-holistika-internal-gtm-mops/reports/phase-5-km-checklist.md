# Phase 5 — KM and mirrors checklist

**Prerequisites:** Phase **1** stable; Phase **3** if graph ingest reads DB mirrors.

| Step | Command / artifact |
|------|---------------------|
| Topic–Fact–Source | [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../../references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md) |
| Topic index template | [`TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md) |
| Validate manifests | `py scripts/validate_hlk_km_manifests.py` if `_assets/**/*.manifest.md` change |
| Neo4j / KiRBe | `scripts/sync_hlk_neo4j.py` per operator procedure |

**Note:** `business-intent` transcripts remain **sources** until promoted through KM workflow.

## Initiative 14 — GTM procedures (Wave D2)

| Need | Location |
|------|----------|
| Vault index of v3.0 GTM SOP paths | [`gtm-sop-vault-index.md`](gtm-sop-vault-index.md) |
| New raster/diagram under `v3.0/_assets/` | Follow frontmatter contract in [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../../references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md); then `py scripts/validate_hlk_km_manifests.py` |

Text-only SOPs already live under `docs/references/hlk/v3.0/Admin/O5-1/`; **manifests are optional** until a visual asset is promoted.
