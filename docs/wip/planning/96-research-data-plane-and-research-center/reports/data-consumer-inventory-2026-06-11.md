---
initiative_id: INIT-OPENCLAW_AKOS-96
authored: 2026-06-11
linked_ops: OPS-86-29
---

# Data-consumer inventory (OPS-86-29)

DAMA-DMBOK lens on research data consumers. First honest inventory per candidate [`i-nn-research-data-management-and-feed-delivery.md`](../_candidates/i-nn-research-data-management-and-feed-delivery.md) §3.

| Consumer / ETL | Produces / consumes | Freshness probe | DAMA concern |
|:---|:---|:---|:---|
| **KiRBe** (+ sources) | Ingest vault docs, vectors, search API | Ingest job logs; `/health` | Integration; Storage |
| **HLK-ERP** | Operator UI; BFF to KiRBe | `/api/kirbe/health`; panel render | Content; BI |
| **KM vault** (Topic-Fact-Source) | Canonical knowledge | `validate_hlk_km_manifests.py` | Document; Metadata |
| **Supabase mirrors** | Registry copies | `sync_compliance_mirrors_from_csv.py`; drift scripts | Storage; Architecture |
| **AKOS orchestration** | Ledger append, validators | `verify.py pre_commit_fast` | Integration |
| **RPAs** | Adapter registries | `validate_adapter_registries.py` | Integration; Quality |
| **Neo4j (AKOS)** | HCAM projection | `sync_hlk_neo4j.py` | Metadata; Architecture |
| **Neo4j (KiRBe local)** | Vault graph search | KiRBe ops (separate instance) | Storage (scoped) |

## Readiness gaps (honest)

| Gap | Evidence | I96 action |
|:---|:---|:---|
| Prod mirror lag | OPS-86-32 class (2026-05-29 sweep) | Staleness loop P3; freshness badges on ERP |
| No unified research feed product | Operator ask (D-IH-75-G) | P10 optional |
| Research Center stub | E2 exploration | P7 four-panel v1 |

## Freshness SLAs (proposed v1)

| Surface | Target | Owner |
|:---|:---|:---|
| Ledger stats | Git commit age | I96 Track A |
| Radar queue | `next_verify_by` from register | I75 / I96 |
| KiRBe search | Last ingest timestamp | I83 |
| Mirror row counts | Match canonical CSV | DataOps emit cadence |
