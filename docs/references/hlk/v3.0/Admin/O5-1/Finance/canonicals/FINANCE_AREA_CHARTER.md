---
language: en
status: charter
canonical: true
role_owner: CFO + Business Controller
classification: way_of_working
intellectual_kind: charter
ssot: true
authored: 2026-06-05
last_review: 2026-06-05
last_review_at: 2026-06-05
last_review_by: Business Controller
last_review_decision_id: D-IH-88-E
methodology_version_at_review: v3.1
inherited_pattern_id: pattern_area_buildout
ratifying_decisions:
  - D-IH-88-A
  - D-IH-88-E
  - D-IH-93-B
linked_canonicals:
  - ../Governance/canonicals/FINOPS_DISCIPLINE.md
  - ../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md
  - ../../../People/Compliance/canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv
  - ../../../Data/Governance/canonicals/DATA_CONTRACT_STANDARD.md
companion_to:
  - ../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md
---

# FINANCE_AREA_CHARTER — Finance area (FINANCE-AREA-FULL F1)

> Second worked example of the People area-governance meta-process
> (`pattern_area_buildout` / `compose_AREA`) after Data (I93 P1). Ratified under
> **FINANCE-AREA-FULL programme inception** (`D-IH-88-E`). Finance owns
> **operational finance truth**; Data owns global contract standards; Marketing
> and RevOps consume Finance IDs and metrics via explicit data contracts (F2+).

## 1. Mission

Finance exists so **every Holistika function trusts the monetary and counterparty
facts it consumes** — at the **Volvo operational bar**: semantic counterparty
MDM, governed facts, and automated cross-area joins. Finance:

1. **Authors** area doctrine (this charter; FINOPS discipline; F2+ rev-rec / tax policy).
2. **Stewards** the counterparty golden record (`FINOPS_COUNTERPARTY_REGISTER.csv`
   in Compliance `finops/` — CSV SSOT unchanged per `D-IH-88-E`).
3. **Publishes** cross-area obligations via `DATA_CONTRACT_REGISTRY` DC-FINOPS-* rows (F2).
4. **Governs** five FINOPS planes (I81 model) without replacing Legal instruments,
   Marketing creative, or a full ERP.

The verb is **govern + enable**: Finance does not own every area's campaign copy;
it owns the **bar**, the **IDs**, and the **evidence** that monetary facts meet the bar.

## 2. Roles + sub-domains

| Sub-domain | Folder | Role anchor | Status |
|:---|:---|:---|:---|
| **Governance** | `Finance/Governance/` | CFO → Business Controller | F1 charter |
| **Business Controller** | `Finance/Business Controller/` | Business Controller | active SOPs |

| Role | Entity | Notes |
|:---|:---|:---|
| **CFO** | Think Big | Area head; entity gate partner (`thi_finan_dtp_306`) |
| **Business Controller** | Think Big | Register stewardship; data-contract co-owner |
| **PMO** | Holistika | Process-cost mapping (`thi_finan_dtp_273`) |
| **RevOps Lead** | HLK Tech Lab | Engagement revenue chain consumer |

**Internal-first (`D-IH-81-P`):** roles may be AIC-absorbed until humans are hired;
gates remain in SOPs and validators.

## 3. Boundary

| Finance owns | Finance does not own |
|:---|:---|
| FINOPS discipline, counterparty golden record, rev-rec **policy** (F2), pricing/tax **registries** (F2) | Marketing campaign creative, Legal contract text |
| Five FINOPS planes (named here; populated F2–F4) | Data global contract **standard** (Data area) |
| Cross-area DC-* **producer** obligations where Finance is source | Supabase DDL execution (Tech / System Owner) |

**Federated rule:** Finance produces domain finance **data products** (registers,
policies, metrics); Data sets contract shape and quality dimensions.

## 4. Five FINOPS planes (I81 model)

| Plane | Name | F1 status | F-phase |
|:---:|:---|:---|:---|
| 1 | Counterparty / party MDM | **Live** (register + mirror + Stripe links) | F1 declares |
| 2 | Revenue recognition + pricing SSOT | partial / counsel + OPS backlog | F2 |
| 3 | Tax + statutory calendar | counsel-held | F2 |
| 4 | O2C / cash / AR | org-planned | F2–F4 |
| 5 | PTP / capex / spend | org-planned | F2–F4 |

## 5. Process catalog (initial)

| Process | `item_id` |
|:---|:---|
| Think Big Finance Architecture (project) | `thi_finan_prj_1` |
| Financial Forecast (workstream) | `thi_finan_ws_1` |
| Revenue Operations (workstream) | `thi_finan_ws_2` |
| Founder Capital Governance (workstream) | `thi_finan_ws_3` |
| FINOPS and counterparty economics (workstream) | `thi_finan_ws_4` |
| Finance area buildout completeness sweep | `hol_finan_dtp_area_buildout_001` |
| FINOPS counterparty register maintenance | `thi_finan_dtp_303` |

Full `thi_finan_dtp_*` runbook pairing is **F2** hygiene — not F1 scope.

## 6. Activation cadence

| Phase | Deliverable | Matrix target |
|:---|:---|:---|
| **F1** | Shell + FINOPS discipline at `charter` | Finance ≥65%; AREA-02/03/13 cleared |
| **F2** | Registries + DC-* + CONF seeds + rev-rec policy | ≥77% |
| **F3** | Mirror evidence + finance cursor rule + recon / fact | AREA-10 evidence |
| **F4** | Closure UAT + I88 P1b re-grade | **≥88% / 0 gaps** + M1–M5 |

### M1–M5 falsifiable gates (programme closure)

| ID | Gate | Falsifiable test |
|:---|:---|:---|
| **M1** | All 5 I81 planes have SSOT + owner + automated check | Per-plane validator matrix |
| **M2** | Counterparty operational: Stripe customers linked; register ≥ **25** rows (`FINOPS_M2_COUNTERPARTY_ROW_FLOOR`) | `finops_monthly_recon.py` + SQL at incorporation |
| **M3** | ≥1 `registered_fact` + monthly recon &lt;0.1% variance | `reports/finops-recon-YYYY-MM.md` |
| **M4** | ≥8 finance metrics in `METRICS_REGISTRY` | `validate_metrics_registry.py` |
| **M5** | Area matrix ≥88% / 0 gaps + I88 Tier-1 spines PASS | `validate_area_completeness.py` + P1b sweep |

**M2 threshold N = 25** — documented at F3 (`akos/hlk_dataops_quality.py` `FINOPS_M2_COUNTERPARTY_ROW_FLOOR`); Stripe `finops_counterparty_id` link coverage verified at first live recon post-incorporation. No production monetary amounts in git at F1.

## 7. Cross-references

- Programme roadmap: [`docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-buildout-roadmap-2026-06-05.md`](../../../../../../wip/planning/88-cross-area-ops-wiring-review-discipline/reports/finance-area-buildout-roadmap-2026-06-05.md)
- Research synthesis: [`master-synthesis.md`](../../../../../../wip/planning/88-cross-area-ops-wiring-review-discipline/reports/research-finance-full-governed-area-2026-06-05/master-synthesis.md)
- People meta-process: [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md)
- I81 FINOPS synthesis: [`p2-tranche-t1-finops-synthesis-2026-05-22.md`](../../../../../../wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/i81/p2-tranche-t1-finops-synthesis-2026-05-22.md)

## Evidence base

**Internal precedent (≥3):**

- [`DATA_AREA_CHARTER.md`](../../../Data/canonicals/DATA_AREA_CHARTER.md) — seven-section area charter pattern (I93 P1).
- [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md) — 14-component `compose_AREA` bar (`D-IH-93-B`).
- [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../../People/Compliance/canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv) + `thi_finan_dtp_303` — live plane-1 substrate.
- Research pack [`master-synthesis.md`](../../../../../../wip/planning/88-cross-area-ops-wiring-review-discipline/reports/research-finance-full-governed-area-2026-06-05/master-synthesis.md) — gap analysis + M1–M5 gates.

**External grounding (≥2):**

- DAMA-DMBOK Reference & Master Data ([EXT-01] in finance research source ledger).
- Counterparty golden-record MDM practice ([EXT-05] Finantrix / golden-record article).
- Record-to-report maturity framing ([EXT-02] EY R2R journey) — plane 4–5 activation bar.
