---
title: FINOPS Discipline
language: en
intellectual_kind: finance-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - CFO
co_authors:
  - Business Controller
  - RevOps Lead
last_review: 2026-06-05
last_review_by: Business Controller
last_review_at: 2026-06-05
last_review_decision_id: D-IH-88-E
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-81-P
  - D-IH-88-E
status: charter
register: internal
linked_canonicals:
  - ../../canonicals/FINANCE_AREA_CHARTER.md
  - ../../../People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - ../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md
  - ../../../People/Compliance/canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv
  - ../../../Data/Governance/canonicals/DATAOPS_DISCIPLINE.md
  - ../../../Data/Governance/canonicals/DATA_CONTRACT_STANDARD.md
linked_runbooks:
  - scripts/validate_finops_ledger.py
  - scripts/sync_compliance_mirrors_from_csv.py
linked_sops:
  - ../../../Business Controller/SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md
companion_to:
  - ../../canonicals/FINANCE_AREA_CHARTER.md
---

# FINOPS Discipline

> The **Finance-area** meta-doctrine (Governance sub-domain) that names how every
> Holistika monetary artefact's quality bar is derived — across FINOPS canonical
> CSVs, Supabase mirrors, `holistika_ops` Stripe links, and `finops.registered_fact`.
> Minted at FINANCE-AREA-FULL **F1** per **D-IH-88-E**. CSV SSOT remains under
> Compliance `finops/`; this discipline owns the **bar** and **compose_FINOPS** rule.

## 1. Purpose

Holistika operates on a **dual-plane FINOPS model**: git-canonical CSVs under
`People/Compliance/canonicals/finops/` (SSOT for registers) + Supabase mirrors /
`holistika_ops` operational tables + Stripe FDW read plane (runtime). When
counterparty IDs drift or monetary facts lack lineage, governance loses its grip —
RevOps books against orphan customers, agents act on stale vendor rows, and audit
trails decouple from authority.

FINOPS Discipline names the quality bar that prevents drift across **all FINOPS
surfaces** — registers, mirrors, Stripe links, writer queue, and recon evidence.
It instantiates the Quality Fabric's `compose()` rule for the **finance axis**, in
the same way [`DATAOPS_DISCIPLINE.md`](../../../Data/Governance/canonicals/DATAOPS_DISCIPLINE.md)
instantiates it for the data axis.

**Ownership:** Business Controller (primary) with CFO (entity gate) and RevOps Lead
(engagement revenue chain consumer). **Execution** of mirrors and Edge workers stays
in Tech (System Owner) per DataOps / mirror DML SOPs.

## 2. The 5 FINOPS quality dimensions

| Dim | Quality property | Measurement | Drift signal |
|:---|:---|:---|:---|
| **FIN-01** | Register integrity | `validate_finops_ledger.py` + `validate_hlk.py` on finops CSVs | Pydantic / FK FAIL on register edit |
| **FIN-02** | Mirror parity | DATA-02 probe on finops mirrors (F3) | CSV row count ≠ mirror count |
| **FIN-03** | Join spine | `holistika_ops.stripe_customer_link.finops_counterparty_id` coverage | Stripe customer without counterparty link |
| **FIN-04** | Entity gate | `thi_finan_dtp_306` before production amounts in git | `registered_fact` without entity readiness |
| **FIN-05** | Cross-area contract | `DATA_CONTRACT_REGISTRY` DC-FINOPS-* rows (F2) | Ad-hoc finance bridge without contract row |

FIN-02 maps to **DATA-02** in [`DATAOPS_DISCIPLINE.md`](../../../Data/Governance/canonicals/DATAOPS_DISCIPLINE.md)
§2; Finance does not duplicate DATA dimension prose — it **consumes** DATA-02 at F3.

## 3. Five FINOPS planes (stewardship)

| Plane | Steward | SSOT (current) | Automated check |
|:---|:---|:---|:---|
| 1 Counterparty MDM | Business Controller | `FINOPS_COUNTERPARTY_REGISTER.csv` | `validate_finops_ledger.py` |
| 2 Rev-rec + pricing | Business Controller + PMO | F2 policy + `PRICING_TIER_REGISTRY` | F2 validators |
| 3 Tax calendar | Business Controller + counsel | `FINOPS_TAX_CALENDAR` (F2) | F2 validators |
| 4 O2C / AR | Business Controller | process_list O2C rows | F4 probes |
| 5 PTP / capex | Business Controller + Marketing | capex DC + MKT spend joins | F4 probes |

## 4. The compose_FINOPS rule

```
compose_FINOPS(audience, channel, scenario, brand, governance, *, finops_surface)
  → finops_quality_bar
```

Where `finops_surface` is one of: `canonical_csv` / `mirror_table` /
`stripe_link` / `registered_fact` / `recon_report`.

The bar derives multiplicatively from the 5 Quality Fabric axes + FIN-01..05.
Promotion from `charter` → `active` is gated at **F4** programme closure (paired
cursor rule + skill at F3).

## 5. Cadence

1. **At every finops CSV mint** — FIN-01 via `validate_hlk.py` + finops validators.
2. **At mirror upsert** — FIN-02 via DataOps mirror apply SOP (F3).
3. **At Stripe customer onboarding** — FIN-03 link spine check.
4. **Before first production `registered_fact`** — FIN-04 entity gate (`thi_finan_dtp_306`).
5. **At cross-area integration tranche** — FIN-05 contract registry row required (F2).
6. **Monthly** — recon report template + rationalization (`thi_finan_dtp_307`).

## 6. Integration with sister disciplines

| Sister | Relationship |
|:---|:---|
| **DATAOPS** | DATA-02 mirror parity; Data Steward co-review on DC mints |
| **AREA_GOVERNANCE** | `hol_finan_dtp_area_buildout_001` runs `validate_area_completeness.py` |
| **MKTOPS** | Capex spend grain via DC-MKT-FINOPS-CAPEX-001 (F2) |
| **Research action** | External rev-rec / tax grounding before F2 policy mint |

## 7. Cross-references

- Charter: [`FINANCE_AREA_CHARTER.md`](../../canonicals/FINANCE_AREA_CHARTER.md)
- Counterparty SOP: [`SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md`](../../../Business%20Controller/SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md)
- Programme: [`finance-area-buildout-roadmap-2026-06-05.md`](../../../../../../../wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-buildout-roadmap-2026-06-05.md)

## Evidence base

**Internal precedent:**

- [`DATAOPS_DISCIPLINE.md`](../../../Data/Governance/canonicals/DATAOPS_DISCIPLINE.md) — discipline shape + compose rule pattern.
- I81 [`p2-tranche-t1-finops-synthesis-2026-05-22.md`](../../../../../../../wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/i81/p2-tranche-t1-finops-synthesis-2026-05-22.md) — five-plane model.
- Live `thi_finan_dtp_303` + counterparty register — plane-1 operational substrate.

**External grounding:**

- DAMA Reference & Master Data ([EXT-01]).
- Counterparty golden-record MDM ([EXT-05]).
- ASC 606 / rev-rec handbook ([EXT-04] KPMG) — plane-2 F2 policy input.
