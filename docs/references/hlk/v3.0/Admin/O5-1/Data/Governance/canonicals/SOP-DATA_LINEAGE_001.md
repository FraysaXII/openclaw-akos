---
title: SOP — Formal Data Lineage
language: en
intellectual_kind: data-canonical-sop
sop_id: SOP-DATA_LINEAGE_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - Data Architect
co_authors:
  - Data Engineer
  - Data Governance Lead
last_review: 2026-06-04
last_review_by: Data Architect
last_review_decision_id: D-IH-93-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-D
status: active
register: internal
linked_canonicals:
  - ../../Architecture/canonicals/DATA_ARCHITECTURE.md
  - DATA_CONTRACT_STANDARD.md
  - dimensions/DATA_CONTRACT_REGISTRY.csv
  - DATA_GOVERNANCE_POLICY.md
linked_runbooks:
  - scripts/data_lineage_check.py
  - scripts/sync_hlk_neo4j.py
linked_processes:
  - thi_data_dtp_275
cadence: scheduled
cadence_trigger: quarterly lineage review OR post major vault/mirror tranche OR graph sync failure
---

# SOP — Formal Data Lineage (T1 → T2 → T3)

## Purpose

Operationalise **lineage stewardship** for Holistika's three-tier architecture:
git-canonical SSOT (T1) → Supabase mirrors/FDW (T2) → Neo4j graph read index (T3).
Pairs `thi_data_dtp_275` (Formal Data Lineage process).

## Scope

| In scope | Out of scope |
|:---|:---|
| Contract-bound surfaces in `DATA_CONTRACT_REGISTRY.csv` | Full OpenLineage emitter (forward P6+) |
| Graph parity checks (`assert_graph_registry_parity`) | Authoring data in Neo4j |
| Vault markdown LINKS_TO document graph (`--with-documents`) | KiRBe ingest pipeline changes |
| Lineage evidence report for operator review | Enterprise Purview scan |

## Lineage paths (reference)

Per `DATA_ARCHITECTURE.md`:

1. **T1 → T2** — mirror emit / migrations; contract row `data_surface=mirror_table`.
2. **T1 → T3** — `sync_hlk_neo4j.py` CSV graph projection.
3. **T1 → T3 (documents)** — optional `--with-documents` vault LINKS_TO edges.
4. **T1 → catalog** — `export_data_contract_odcs.py` (ODCS projection).

## Steps (AC-HUMAN)

1. **Inventory** — run `py scripts/data_lineage_check.py --report`; review chains.
2. **Verify contracts** — each production surface has registry row or forward-declared OPS tracker.
3. **Graph parity** — when `NEO4J_*` configured, run `sync_hlk_neo4j.py --dry-run`.
4. **Document gaps** — open OPS row for missing mirror or graph edge.
5. **Quarterly sign-off** — Data Engineer + Data Architect record review date.

## Steps (AC-AUTOMATION)

```powershell
py scripts/data_lineage_check.py --self-test
py scripts/data_lineage_check.py --report
py scripts/sync_hlk_neo4j.py --dry-run
py scripts/validate_data_contract_registry.py
```

PASS criteria: lineage report lists all active contracts; graph parity dry-run OK;
no orphan `data_surface=graph` contracts without sync path documented.

## Escalation

Graph parity FAIL → Data Engineer → Database Owner → System Owner.
Contract missing for live mirror → Data Steward → Data Governance Lead.

## Cross-references

- Architecture: `Data/Architecture/canonicals/DATA_ARCHITECTURE.md`
- KiRBe program: `Data/Governance/programs/PRJ-HOL-KIR-2026/README.md`
- I91 store inventory: `docs/wip/planning/91-enterprise-graph-store-coverage/reports/store-inventory-2026-06-01.md`
