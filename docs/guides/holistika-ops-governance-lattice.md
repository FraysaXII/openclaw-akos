# Holistika Ops vs Data governance lattice

**Audience:** Operator, PMO, CDO, System Owner  
**Status:** Active reference (2026-06-05) — post-I93 closure + D-GTM-DB-6 mirror-apply standard

Holistika platform work splits into **doctrine areas** (what the business owns) and
**execution lanes** (how AKOS + Supabase enforce it). Data governance and Ops governance
are complementary, not duplicate.

---

## The two planes (all initiatives)

| Plane | What | Who authors | How it lands |
|:---|:---|:---|:---|
| **Schema (DDL)** | Tables, RLS, extensions | Tech / migrations | `supabase db push` + operator SQL gate |
| **Mirror data (DML)** | `compliance.*_mirror` rows | Compliance CSVs in git | Emit → review → apply (this doc + mirror DML SOP) |

SSOT: [`akos-holistika-operations.mdc`](../../.cursor/rules/akos-holistika-operations.mdc) · [`operator-sql-gate.md`](../wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md)

---

## Data governance (I93 — closed 2026-06-05)

**Functional name:** the DATA area + DataOps quality bar.

| Layer | Artifact | Role |
|:---|:---|:---|
| Area charter | `DATA_AREA_CHARTER.md` | What DATA owns (DAMA, contracts, families) |
| Quality doctrine | `DATAOPS_DISCIPLINE.md` | DATA-01..07 dimensions |
| Paired SOP | `SOP-TECH_DATAOPS_QUALITY_001.md` | When probes fire (mint, emit, wave-close) |
| Contracts | `DATA_CONTRACT_REGISTRY.csv` | Producer × surface SLAs |
| Families | 7× DATA-FAM umbrella processes | Federated data products |
| People meta | `pattern_area_buildout` + area completeness validator | How areas get built/scored |

**Data does not** replace the operator SQL gate — it defines **what “good” looks like** after mirrors are loaded.

---

## Ops governance (in flight — I88 and PMO doctrine)

**Functional name:** cross-area operations wiring + “which surface do I open?”

| Layer | Artifact | Role |
|:---|:---|:---|
| Surface routing | `OPERATIONAL_COHESION_DOCTRINE.md` | AKOS vs ERP vs external render vs runtime |
| Wiring review | I88 `CROSS_AREA_OPS_WIRING_REVIEW_DISCIPLINE` (when minted) | Every-area OPS maintenance at correct density |
| RevOps catalog | `REVOPS_PROCESS_CATALOG.yaml` | Cross-area handoffs (Marketing → Finance → …) |
| ERP architecture | `HLK_ERP_ARCHITECTURE.md` | Mirror → view → panel triplets (read projections) |
| SQL gate | `operator-sql-gate.md` | DDL proposal → approval → migrate |

**Ops does not** author canonical CSV business data — it orchestrates **platform operations**
and **human entrypoints**.

---

## Mirror DML — shared seam (now fully governed)

The emit→apply loop is where Data and Ops meet:

```mermaid
flowchart LR
  CSV[Git CSV SSOT] -->|DataOps emit| SQL[Reviewed upsert SQL]
  SQL -->|Ops gated apply| MIRROR[compliance.*_mirror]
  MIRROR -->|DATA-02 verify| PASS[Parity PASS]
```

| Step | Primary owner | Governed by |
|:---|:---|:---|
| Edit CSV | Area steward / Compliance chain | `validate_hlk.py` + tranche gates |
| Emit SQL | DataOps / automation | `compliance_mirror_emit`, `sync_compliance_mirrors_from_csv.py` |
| **Apply SQL** | **System Owner + PMO** | **`SOP-HOLISTIKA_COMPLIANCE_MIRROR_DML_001`** + [`holistika-mirror-dml-apply.md`](holistika-mirror-dml-apply.md) |
| Verify parity | Data Governance Lead | `dataops_quality_check.py`, DATA-02 |

**Process register:** `env_tech_dtp_compliance_mirror_dml_001` (`process_list.csv`)  
**Decision:** **D-GTM-DB-6** (linked CLI preferred; psql valid)

Before 2026-06-05 this seam was documented in repo guides and cursor rules but **not**
registered as a paired SOP + `process_list` row — that gap is closed.

---

## Envoy Tech Lab (sibling repos)

**Functional name:** the governed index of GitHub repositories.

| Artifact | Role |
|:---|:---|
| [`REPOSITORIES_REGISTRY.md`](../references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) | Which repos exist + ownership |
| [`EXTERNAL_REPO_CONTRACT_TEMPLATE.md`](../references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md) | Consumer repos read mirrors; no local CSV SSOT |
| [`CONTRIBUTING.template.md`](../references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/_templates/CONTRIBUTING.template.md) | Operator SQL gate + mirror discipline for siblings |

Platform repos (hlk-erp, kirbe) **consume** `compliance.*_mirror`; AKOS **projects** them.

---

## Is the mirror-apply process governed?

| Criterion | Before I93 closure follow-up | After 2026-06-05 |
|:---|:---:|:---:|
| Operator runbook (repo) | ✓ | ✓ |
| Initiative 14 decision (D-GTM-DB-6) | ✓ | ✓ |
| DataOps doctrine cites apply | partial | ✓ |
| Paired SOP + `process_list` row | ✗ | ✓ |
| `CANONICAL_REGISTRY` + KNOWLEDGE_PAIRING | ✗ | ✓ |
| Envoy consumer contract cites apply method | partial | ✓ |
| I88 cross-area OPS wiring discipline minted | in flight | in flight |

**Verdict:** Mirror DML apply is **governed** at the Holistika platform layer. **I88** will extend Ops governance to **every-area wiring review** — a different scope, not a substitute for this seam.

---

## Related initiatives

| ID | Focus | Status |
|:---|:---|:---|
| I93 | DATA area + area-buildout meta-process | **closed** |
| I88 | Cross-area Ops wiring review discipline | **active** |
| I14 | Holistika internal GTM / mirror emit profiles | **active** (D-GTM-DB-2..6) |
| I86 | Cluster / OPS-86-15 mirror DDL sprint | OPS-86-15 may remain open for CHANNEL mirror |
