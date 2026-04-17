# Phase 5 — KM and mirrors checklist

**Prerequisites:** Phase **1** stable; Phase **3** if graph ingest reads DB mirrors.

| Step | Command / artifact |
|------|---------------------|
| Topic–Fact–Source | [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md) |
| Topic index template | [`TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md) |
| Validate manifests | `py scripts/validate_hlk_km_manifests.py` if `_assets/**/*.manifest.md` change |
| Neo4j / KiRBe | `scripts/sync_hlk_neo4j.py` per operator procedure |

**Note:** `business-intent` transcripts remain **sources** until promoted through KM workflow.
