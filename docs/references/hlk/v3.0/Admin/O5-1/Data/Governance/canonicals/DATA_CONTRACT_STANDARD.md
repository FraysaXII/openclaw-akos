---
title: Data Contract Standard
language: en
intellectual_kind: data-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Data Governance Lead
co_authors:
  - Data Steward
  - CDO
last_review: 2026-06-04
last_review_by: Data Governance Lead
last_review_at: 2026-06-04
last_review_decision_id: D-IH-93-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-93-D
  - D-IH-93-C
status: active
register: internal
linked_canonicals:
  - DATA_GOVERNANCE_POLICY.md
  - DATAOPS_DISCIPLINE.md
  - dimensions/DATA_CONTRACT_REGISTRY.csv
  - ../../../People/Compliance/canonicals/PRECEDENCE.md
companion_to:
  - DATA_GOVERNANCE_POLICY.md
---

# Data Contract Standard

> ODCS v3.1-aligned vocabulary for Holistika **data contracts** — the
> declared interface between a data producer and its consumers on a specific
> **data surface** (canonical CSV, mirror table, FDW projection, or graph).
> The lean on-ramp is `DATA_CONTRACT_REGISTRY.csv`; full ODCS YAML export is
> forward-chartered. Posture: **contracts-as-code, warn-first-fail-later**.

## 1. Purpose

Holistika already operates a contract-shaped machine: git-canonical CSV as
schema SSOT + Supabase mirror as operational projection. This standard **names
that contract** so producer→consumer obligations are explicit and checkable
instead of implicit.

Each registry row is one contract for one `(producer × data_surface)` pair.
When a canonical CSV also has a mirror and an FDW, register **separate rows**
— matching ODCS server/surface granularity. Seed example: CAPABILITY_REGISTRY
has `DC-HOL-COMPLIANCE-MIRROR-CSV-001` (People producer, `canonical_csv`) and
`DC-HOL-COMPLIANCE-MIRROR-001` (DataOps enforcer, `mirror_table`, forward DDL).

## 2. ODCS vocabulary mapping

We adopt Open Data Contract Standard (ODCS) v3.1.0 field names as the
**semantic anchor** for registry columns (strict JSON Schema in ODCS; CSV
registry here is the Holistika on-ramp).

| Registry column | ODCS construct | Notes |
|:---|:---|:---|
| `contract_id` | `id` | Pattern `DC-HOL-*` |
| `producer_process_id` / `producer_area` | `team` (producer) | FK → `process_list.csv` |
| `consumer_area_ids` | consumers | Semicolon-list of O5-1 areas |
| `data_surface` | `server` / deployment target | `canonical_csv` \| `mirror_table` \| `fdw_projection` \| `graph` |
| `schema_ref` | `schema` | Repo path or DDL ref |
| `semantics_ref` | `description` / `authoritativeDefinitions` | Business meaning; engagement IDs, etc. |
| `quality_rules` | `quality` | Semicolon-list; **must use DATA-01..07 codes** |
| `sla_freshness` | `slaProperties` (`latency` / `frequency`) | e.g. `24h`, `1h` |
| `sla_availability` | `slaProperties` (`availability`) | e.g. `99.5%` |
| `classification` | schema element classification | P5 privacy policy extends enum |
| `retention_policy_ref` | `slaProperties` (`retention`) | Forward to P5 policy |
| `version` / `status` | `version` / `status` | Semver + `active` \| `draft` \| `deprecated` |
| `owner_role` | `team` role | Business-accountable Data Owner (DAMA) |

### 2.1 Quality rules (DATA-01..07 only)

Contract quality rules **reference** the DataOps discipline — no parallel
quality taxonomy:

| Code | Dimension |
|:---|:---|
| DATA-01 | FK integrity |
| DATA-02 | Mirror parity |
| DATA-03 | FDW / external read-plane health |
| DATA-04 | Freshness / staleness |
| DATA-05 | Schema drift |
| DATA-06 | Manifest / KM alignment |
| DATA-07 | DAMA quality metrics (completeness, accuracy, consistency, timeliness, uniqueness, validity) |

List one or more codes in `quality_rules`, semicolon-separated.

### 2.2 SLA drivers (informative)

When documenting SLA intent, classify the driver per ODCS:

- **regulatory** — compliance, retention, audit
- **analytics** — reporting, KPI, engagement facts
- **operational** — runtime mirrors, CRM sync, FDW read plane

Seed contracts in the registry encode the driver in `notes` until a dedicated
column is forward-chartered.

## 3. Registry mechanics

Follow `pattern_register_csv_pydantic_validator_mirror`:

| Artifact | Path |
|:---|:---|
| CSV SSOT | `dimensions/DATA_CONTRACT_REGISTRY.csv` |
| Pydantic SSOT | `akos/hlk_data_contract_csv.py` |
| Validator | `scripts/validate_data_contract_registry.py` |
| Tests | `tests/test_validate_data_contract_registry.py` |
| Supabase mirror | forward-charter (DDL not in P2 scope) |

FK gates: `producer_process_id` → `process_list.csv`; `owner_role` →
`baseline_organisation.csv`; `last_review_decision_id` → `DECISION_REGISTER.csv`;
`quality_rules` codes → DATA-01..07 only; `consumer_area_ids` → known O5-1 areas;
`schema_ref` paths under `docs/` must resolve on disk (SQL mirror/FDW refs exempt).

## 4. Change management

1. **Draft** — new row with `status=draft`; validator PASS required.
2. **Active** — Data Governance Lead approval; `status=active`; semver bump
   on material schema/SLA change.
3. **Deprecated** — successor contract row must exist; old row `status=deprecated`.

Canonical-CSV tranche gate applies to registry mints (operator approval per
baseline governance).

## 5. Warn-first-fail-later

P2 enables **declaration + validation** without blocking unrelated work:

- Missing contracts on known surfaces → INFO/WARN in DataOps sweeps (future
  DATA-FAM probes at I93 P6).
- Invalid registry rows → FAIL at `validate_data_contract_registry.py`.
- ODCS YAML export → forward-charter; CSV remains SSOT until export tooling
  lands.

## 6. Cross-references

- Policy: `DATA_GOVERNANCE_POLICY.md`
- Registry: `dimensions/DATA_CONTRACT_REGISTRY.csv`
- Research packet: `docs/wip/planning/93-data-area-foundation-and-governance/reports/research-p2-2026-06-04.md`
- Cross-area seeds: `docs/wip/planning/93-data-area-foundation-and-governance/reports/cross-area-data-map-2026-06-04.md`

## Evidence base (internal precedent + external grounding)

**Internal precedent**

- Two-plane model (git-canonical CSV ↔ Supabase mirror):
  `.cursor/rules/akos-holistika-operations.mdc`.
- DataOps 7-dimension quality bar (DATA-01..07) this standard's `quality_rules`
  reference: `Data/Governance/canonicals/DATAOPS_DISCIPLINE.md`.
- Register 4-file shape reused by `DATA_CONTRACT_REGISTRY`:
  `pattern_register_csv_pydantic_validator_mirror`
  (`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`).

**External grounding**

- Open Data Contract Standard (ODCS) v3.1.0 — Bitol/Linux Foundation, Dec
  2025 (Apache-2.0): `schema` + executable `quality` (library/sql/custom) +
  `slaProperties` (driver ∈ regulatory/analytics/operational) + `team`.
  https://bitol.io/ — the contract vocabulary adopted here.
- DAMA-DMBOK2 Ch.3 Data Governance (DAMA International, 2017): governance =
  authority + control + shared decision-making; governance decides, management
  executes; federated operating model.
- Dehghani, Z. (2019), "Data Mesh Principles and Logical Architecture",
  martinfowler.com: federated computational governance — standards baked
  computationally into the platform (validators + mirror emit), data-as-a-product.
- EDM Council DCAM — capability-maturity lens complementing DAMA's
  knowledge-area lens.
