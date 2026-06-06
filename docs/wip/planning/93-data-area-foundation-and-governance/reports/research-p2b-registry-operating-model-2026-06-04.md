---
intellectual_kind: research_synthesis
parent_initiative: INIT-OPENCLAW_AKOS-93
feeds_phase: P2b
status: research-synthesis
audience: J-OP
role_owner: Data Governance Office + PMO
language: en
authored: 2026-06-04
last_review: 2026-06-04
ratifying_research:
  - OpenMetadata ODCS 3.1 import/export API (docs.open-metadata.org)
  - Microsoft Purview Unified Catalog + data products (learn.microsoft.com)
  - Holistika internal — DATA_CONTRACT_REGISTRY, cross-area-data-map, area-completeness matrix
internal_evidence_sweeps: 6
---

# I93 P2b — research: data-contract registry operating model + catalog-tool posture

> Operator question (2026-06-04): why only 4 registry rows; relation to
> process_list / CAPABILITY_REGISTRY; drift risk; vs Purview/OpenMetadata;
> what the missing 19% area score means. This packet grounds the **P2b mint**
> (operating-model report, maintenance SOP, registry check runbook, catalog
> integration posture canonical).

## 0. Load-bearing finding

**Four rows are a pattern proof, not catalog coverage.** Holistika already
governs data through git-canonical SSOT + validators + mirrors; P2 **named**
producer→consumer obligations. Full coverage (~115 classified processes, 7
DATA-FAM families) is **P6–P7 work**, not P2 scope. The three registers
(process_list, CAPABILITY_REGISTRY, DATA_CONTRACT_REGISTRY) answer **different
questions** and must stay linked by FK, not merged.

**Catalog tools (OpenMetadata, Purview)** are **optional projection layers** —
not replacements for repo SSOT. ODCS 3.1 export from our CSV registry is
mechanically aligned (OpenMetadata ships import/export for ODCS 3.1.0). Default
posture: **repo-native SSOT + validators + phased ODCS export**; evaluate hosted
catalog only when operator need for discovery UI / multi-cloud scan exceeds
maintenance cost.

## 1. Internal evidence sweep

| # | Evidence | Implication |
|:--|:---|:---|
| I1 | `DATA_CONTRACT_REGISTRY.csv` — 4 seed rows | Machinery + 3 DATA-FAM examples; not exhaustive |
| I2 | `cross-area-data-map-2026-06-04.md` — 115 mapped / 35 unmapped | P6 populates families; contracts grow with families |
| I3 | OPS-86-15 — 5 CSVs without mirror DDL | Forward mirror contracts track gap explicitly |
| I4 | Area matrix Data 81% — 5 partials listed | Missing 19% = partial→pass on AREA-06/08/09/11/14 (P4–P8) |
| I5 | `process_list` vs `CAPABILITY_REGISTRY` vs contracts | Three-axis model; contracts FK `producer_process_id` |
| I6 | P6 roadmap — DATA_FAM_PROBE_PROFILES + `--data-fam` | Probes enforce contracts; not same as maintenance SOP |

## 2. External research sweep

| Source | Holistika reliability | Credibility (external) | Control | Finding |
|:---|:---:|:---:|:---|:---|
| [OpenMetadata ODCS API](https://docs.open-metadata.org/v1.11.x/api-reference/data-contracts/odcs) | 4 | 5 | Safe | GET/POST ODCS 3.1 JSON/YAML — **export path for our CSV registry** |
| [OpenMetadata 1.12 blog](https://blog.open-metadata.org/announcing-openmetadata-1-12-9e15b66e7748) | 4 | 4 | Safe | Data-product-level contract inheritance; superset over ODCS |
| [Microsoft Purview governance overview](https://learn.microsoft.com/en-us/purview/data-governance-overview) | 4 | 5 | Safe | Unified Catalog + Data Map scan; **discovery/classification plane** |
| [Purview data products](https://learn.microsoft.com/en-us/purview/unified-catalog-data-products) | 4 | 5 | Safe | Data products bundle assets + access policy — maps to our DATA-FAM umbrellas (P6) |

## 3. Synthesis → mint spec

| Artifact | Purpose |
|:---|:---|
| `reports/data-contract-registry-operating-model-2026-06-04.md` | Intent, three-register model, growth path, area-score closure map |
| `SOP-DATA_CONTRACT_REGISTRY_MAINTENANCE_001.md` | Steward cadence for add/amend/deprecate rows |
| `scripts/data_contract_registry_check.py` | Paired runbook: coverage + forward-mirror gap report |
| `DATA_CATALOG_INTEGRATION_POSTURE.md` | Repo SSOT vs OpenMetadata/Purview; hybrid export forward-charter |
| `DATA_CONTRACT_STANDARD.md` §2.3 | Three-register relationship (canonical amendment) |
| `process_list` + `KNOWLEDGE_PAIRING` + registry rows | Executable + documentation pairing |

## 4. Catalog-tool posture options (for inline-ratify)

| Option | Posture | When |
|:---|:---|:---|
| **A — Repo-native (default)** | CSV SSOT + validators + ODCS export forward-charter | Current scale; git-audit trail primary |
| **B — Hybrid read replica** | Periodic ODCS YAML export → OpenMetadata import for discovery UI | When stewards need non-git search/discovery |
| **C — Purview for Azure estate** | Purview scan + Unified Catalog for Microsoft/Fabric assets only | If Think Big Azure/Fabric becomes primary lakehouse |
| **D — Full catalog first** | Deploy OpenMetadata/Purview before growing registry | **Not recommended** — duplicates SSOT, drift risk |

**Recommend A now**, document B as P8+ forward-charter in posture canonical.

## 5. Cross-references

- P2 mint: `DATA_GOVERNANCE_POLICY.md`, `DATA_CONTRACT_STANDARD.md`, registry CSV
- P6: DATA-FAM families + `--data-fam` probes
- Area bar: `AREA_GOVERNANCE_DISCIPLINE.md`, `validate_area_completeness.py`
