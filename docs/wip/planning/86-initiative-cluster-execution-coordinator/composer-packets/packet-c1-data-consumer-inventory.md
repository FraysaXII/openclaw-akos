---
intellectual_kind: composer_bounded_packet
packet_id: C1-data-consumer-inventory
target_seat: Composer (execution)
owning_initiative: INIT-OPENCLAW_AKOS-88
ops_forward: OPS-86-29
authored: 2026-05-29
status: ready
---

# Composer packet — C1 Data-consumer / ETL inventory

## Objective

Author a governed inventory of every system that **consumes or moves** research-shaped data in
Holistika (KiRBe sources, ERP, KB, Supabase mirrors, orchestration, RPA). Output feeds the DAMA
candidate and backlog item C1.

## Deliverable

`docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/data-consumer-inventory-2026-05-29.csv`

## Schema (columns — exact header order)

```
consumer_id,consumer_name,repo_or_surface,role_in_flow,data_shape,freshness_expectation,access_level,dama_knowledge_area,linked_canonicals,notes
```

## Sources to crawl (read-only)

| Source | What to extract |
|:---|:---|
| `kirbe-platform/` (sibling) | Ingest endpoints, webhook handlers, research feed hooks |
| `hlk-erp/` (sibling) | Panels reading `compliance.*_mirror` |
| `docs/references/hlk/v3.0/_assets/**` | KM manifests |
| `supabase/migrations/` | Mirror table list |
| `scripts/sync_hlk_neo4j.py` | Graph projection inputs |
| `config/mcporter.json.example` | MCP research surfaces |
| Backlog §3.2 + cross-area-tech-propagation report | Known consumers named in prose |

## Validators

None blocking for inventory-only; run `py scripts/validate_hlk.py` if any canonical CSV touched.

## Acceptance

- Every consumer named in backlog §3.2 has ≥1 row.
- Each row has a DAMA knowledge-area tag.
- Row count ≥ 15 (minimum credible coverage).

## Escalate to Opus if

- A consumer implies a new canonical CSV mint.
- Freshness expectation conflicts with prod-mirror drift findings.
