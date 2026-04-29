# Program — `PRJ-HOL-KIR-2026` (Data / Architecture chain)

**Owner role**: Data Architect (CDO chain)  
**Program registry**: [`PROGRAM_REGISTRY.csv`](../../../../../../../compliance/dimensions/PROGRAM_REGISTRY.csv) → `PRJ-HOL-KIR-2026`.  
**Scope**: All Data Architecture casework specifically scoped to KiRBe's graph navigation and masterdata model.

This folder is the **program-scoped landing point** for Data Architecture casework on KiRBe — the graph projection that lets MADEIRA and KiRBe navigate the HLK knowledge model end-to-end. Initiative 23 P-graph extends the existing Neo4j projection (Initiative 07) with `:Program` nodes; KiRBe is the first product-tier program that benefits from typed `:CONSUMES` / `:PRODUCES_FOR` edges.

> **Process-list anchors** — `env_tech_dtp_269 Neo4j knowledge graph navigation` (covers both MADEIRA and KiRBe). Initiative 07's `:Role` + `:Process` + `:Document` schema + the new Initiative 23 `:Program` extension is the canonical graph DDL surface (D-IH-18).

## Casework scope (incoming)

- KiRBe → Neo4j projection contract: which entities become nodes, which relations become typed edges.
- Allowlisted Cypher templates for KiRBe operator queries.
- Rebuild cadence and graph staleness alarms.

## Cross-references

- Tech KiRBe folder: [`Admin/O5-1/Tech/System Owner/programs/PRJ-HOL-KIR-2026/`](../../../../Tech/System%20Owner/programs/PRJ-HOL-KIR-2026/README.md)
- Data Governance KiRBe folder (DQ + lineage): [`Admin/O5-1/Data/Governance/programs/PRJ-HOL-KIR-2026/`](../../Governance/programs/PRJ-HOL-KIR-2026/README.md)
- Initiative 23 master roadmap: [`docs/wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md`](../../../../../../../../wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md)
- Initiative 07 graph stack baseline: existing `:Role` + `:Process` schema in [`akos/hlk_graph_model.py`](../../../../../../../../../akos/hlk_graph_model.py)
