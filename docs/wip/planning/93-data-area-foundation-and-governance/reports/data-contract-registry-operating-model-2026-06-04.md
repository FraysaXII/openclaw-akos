---
intellectual_kind: operating_model
parent_initiative: INIT-OPENCLAW_AKOS-93
feeds_phase: P2b
status: active
audience: J-OP
role_owner: Data Governance Office
language: en
authored: 2026-06-04
last_review: 2026-06-04
research_packet: research-p2b-registry-operating-model-2026-06-04.md
---

# Data Contract Registry — operating model (2026-06-04)

> Plain-language answer to: *what are the 4 rows, what are they not, how do
> they relate to process_list and capabilities, and what still belongs to
> P3–P8?*

## 1. What a contract row is

One row in `DATA_CONTRACT_REGISTRY.csv` declares **obligations for one data
surface** — one producer process, one deployment target (`canonical_csv`,
`mirror_table`, `fdw_projection`, or `graph`), with:

- who owns it (`owner_role`)
- who consumes it (`consumer_area_ids`)
- where the schema lives (`schema_ref`)
- quality bar (`quality_rules` = DATA-01..07 only)
- SLA intent (`sla_freshness`, `sla_availability`)

**Example:** CAPABILITY_REGISTRY has **two** rows today — git CSV (People
producer) and forward mirror (DataOps enforcer) — because CSV and mirror are
**different surfaces** with different producers.

## 2. What a contract row is NOT

| Not this | Why |
|:---|:---|
| A duplicate `process_list` row | process_list = org/work catalog; contract = data obligation on a surface |
| A duplicate `CAPABILITY_REGISTRY` row | Capability = what the org can do; contract = producer→consumer data promise |
| Proof that Holistika has only 4 contracts | Most surfaces are still **implicit** (validators + two-plane discipline) |
| Proof that mirrors exist | Row `DC-HOL-COMPLIANCE-MIRROR-001` is a **forward declaration** (OPS-86-15) |

## 3. Three-register model (anti-drift)

```
process_list          →  "What work exists? Who owns the process?"
CAPABILITY_REGISTRY   →  "What executable capability does work surface?"
DATA_CONTRACT_REGISTRY →  "What data does this process publish/consume, on which surface, with what quality/SLA?"
```

**Drift prevention:** contracts **FK** to `producer_process_id`; P6 **DATA-FAM**
umbrella capabilities group processes; P6 **DataOps `--data-fam` probes** check
live surfaces against `quality_rules`. Maintenance SOP governs **when humans
add/amend/deprecate** rows.

## 4. Why only 4 rows (P2 acceptance)

| Row | DATA-FAM family | Role |
|:---|:---|:---|
| `DC-HOL-COMPLIANCE-MIRROR-CSV-001` | COMPLIANCE-MIRROR | Canonical CSV surface pattern |
| `DC-HOL-COMPLIANCE-MIRROR-001` | COMPLIANCE-MIRROR | Forward mirror + OPS-86-15 gap tracker |
| `DC-HOL-SUEZ-ENG-FACT-001` | ENGAGEMENT-FACT | Live engagement mirror example |
| `DC-HOL-GTM-CRM-001` | GTM-CRM | FDW read-plane example |

**Growth path**

| Phase | Contract coverage |
|:---|:---|
| **P2 (done)** | 4 seeds, machinery |
| **P6** | 7 DATA-FAM umbrellas + map ~115 processes; bulk contract tranches by family |
| **P7** | Component matrix + engagement reconciliation rows |
| **P8+** | ODCS YAML export optional; OpenMetadata import if hybrid posture ratified |

Cross-area map: `reports/cross-area-data-map-2026-06-04.md` (115 mapped / 35 unmapped).

## 5. Area score 81% — the missing ~19% (Data area only)

Formula: pass=1, partial=0.5 → (8 + 2.5) / 13 ≈ **81%**.

| Component | Now | To reach pass | Phase |
|:---|:---|:---|:---|
| AREA-06 Capability↔confidence | partial (10 CAP, 0 CONF) | Data CONF seeds | **P6** |
| AREA-08 Dimension registries | partial (1 CSV) | 2nd registry e.g. METRICS | **P4** |
| AREA-09 Paired SOP+runbook | partial (0/6 paired) | Lineage/MDM SOPs + contract SOP (P2b) | **P4–P5 + P2b** |
| AREA-11 Cursor rule+skill | partial | Data-specific skill or extend area-governance globs | **P8** |
| AREA-14 inherited_pattern_id | partial | `pattern_dataops_discipline` on Data processes | **P8** |

Run: `py scripts/validate_area_completeness.py --matrix`

## 6. Fully functional governance? (honest status)

| Layer | Status |
|:---|:---|
| Policy + decision rights | **Active** (P2) |
| Contract standard + registry shape | **Active** (P2) |
| Maintenance SOP + registry check runbook | **Active** (P2b) |
| Catalog tool posture doc | **Active** (P2b) |
| Populated contract catalog | **Early** (4/~many) |
| Live DATA-FAM probes | **Forward** (P6) |
| Semantic layer / lineage / MDM / privacy | **Forward** (P4–P5) |
| Purview/OpenMetadata deployment | **Not required**; hybrid export optional |

**vs OpenMetadata / Purview:** we implement **contracts-as-code in git** (like
ODCS-on-rails); those tools are **discovery + scan + UI** layers — not SSOT.
See `DATA_CATALOG_INTEGRATION_POSTURE.md` **§7–§9** (three-layer DAMA stack,
11-area matrix, governed-claim bar).

## 7. DAMA-tool-friendly (founder logic, plain language)

Holistika is **not** anti-tool. DAMA-DMBOK is the blueprint; git vault + validators
are how we **prove** control; OpenMetadata / Purview / datacontract-cli are how we
**operationalize** discovery and DQ when needed — same split as ITIL doctrine vs
ServiceNow BPA. Repo-native SSOT (Option A) **plus** ODCS interoperability is the
industry-standard pattern (OpenMetadata stores contracts in git first, then imports).

## 8. Operator commands

```powershell
py scripts/validate_data_contract_registry.py
py scripts/data_contract_registry_check.py --self-test
py scripts/data_contract_registry_check.py --coverage-report
py scripts/validate_area_completeness.py --matrix
```
