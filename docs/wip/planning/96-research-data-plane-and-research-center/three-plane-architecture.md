---
initiative_id: INIT-OPENCLAW_AKOS-96
authored: 2026-06-11
audience: J-OP
---

# Three-plane architecture — research stack

Holistika research work flows through three planes. Each plane has a single system of record; mirrors and BFFs are read paths, not competing authorities.

## Planes

### Govern — AKOS (git)

**What it holds:** Methodology vault, source ledgers, Research Radar targets, SSOT registries, Cursor rules/skills, HCAM relationship registry, process_list pairings.

**Operator-facing signal:** Session recap, planning initiative I96, validation scripts (`validate_research_action.py`, `validate_hlk.py`).

**Anti-pattern:** Treating KiRBe or ERP as places to edit canon.

### Execute — KiRBe

**What it holds:** Ingested documents, hybrid search indexes (BM25 + vectors + RRF), embedding jobs, audit logs, tenant billing (`kirbe.*` schema).

**Authority boundary:** Reads Holistika compliance mirrors read-only per [`config/sync/kirbe-sync-contract.md`](../../../../config/sync/kirbe-sync-contract.md). Local Neo4j for vault search only — **separate from AKOS Neo4j** (`D-IH-32-M`).

### Experience — HLK-ERP

**What it holds:** Operator UI — Mission Control, persona rollups (I89), **Research Center** (I96 Track D).

**Read pattern:** BFF proxies to KiRBe (`KIRBE_API_URL` → `/api/kirbe/*`); GitHub Contents for WIP packs (I65 pattern).

## Staleness loop (summary)

Research Radar marks targets STALE/DUE → govern stage updates ledger/canonicals → KiRBe re-ingests tagged `SRC-*` rows → ERP panels show fresh `next_verify_by` and search results.

Detail: [`staleness-loop-spec.md`](staleness-loop-spec.md).

## STORE → RECALL → SHARE (D-IH-75-G)

| Lifecycle stage | Plane |
|:---|:---|
| STORE | Govern git + Supabase mirrors + KiRBe vault |
| RECALL | KiRBe search + ERP panels + radar queue |
| SHARE | ERP Research Center + future multi-channel feed (P10) |

Promoted from candidate [`i-nn-research-data-management-and-feed-delivery.md`](../_candidates/i-nn-research-data-management-and-feed-delivery.md).
