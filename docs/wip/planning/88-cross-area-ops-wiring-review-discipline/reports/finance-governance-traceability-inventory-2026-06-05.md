---
report_kind: traceability_inventory
program: FINANCE-AREA-FULL
authored: 2026-06-05
control_confidence_level: Safe
purpose: Answer operator questions on full functionality, scalability, mint status, pricing/taxes, and People-meta-process parity
---

# Finance governance — traceability inventory (2026-06-05)

## Direct answers (operator questions)

### 1. Will this give a **fully functional** Finance area that scales to unknown needs?

| Claim | Honest status |
|:---|:---|
| **Fully functional for Holistika today** | **Not yet.** Counterparty + Stripe substrate is real; pricing/tax/O2C/PTP offices are **org-planned**, not operationally staffed. |
| **Fully functional after F0–F4** | **Yes, at Holistika scale** — if closure hits **88% area matrix + M1–M5 gates** (see research pack). |
| **Scalable to unidentified needs** | **Yes, by design** — via People **`pattern_area_buildout`**, **data contracts**, **five FINOPS planes**, **semantic metric catalog**, and **OPS_REGISTER** forward rows — **not** by minting every future process upfront. |

**Scalability mechanism (philosophy fit):**

- **People meta-process** — new Finance capabilities attach to the same 14-component bar (like Data).
- **Data contracts** — new RevOps/MKT/Legal surfaces extend DC-* rows, not new ad-hoc bridges.
- **Extension registries** — `PRICING_TIER_REGISTRY`, `FINOPS_TAX_CALENDAR`, `METRICS_REGISTRY` absorb new tiers/obligations/filings without re-architecting.
- **Under-engineering guard** — entity gate `thi_finan_dtp_306` until books are real; **over-engineering guard** — no ERP clone.

### 2. People meta-process parity — is Finance wired like Data?

| People / Data artifact (governed) | Finance equivalent | Status |
|:---|:---|:---|
| `AREA_GOVERNANCE_DISCIPLINE.md` | `FINOPS_DISCIPLINE.md` or `FINANCE_AREA_CHARTER.md` | **Not minted** (F0–F1) |
| `pattern_area_buildout` | Same pattern on `thi_finan_*` processes | **Not wired** in `process_list.csv` |
| `SOP-PEOPLE_AREA_GOVERNANCE_001` | `SOP-FINANCE_AREA_BUILDOUT_001` (proposed) | **Not minted** |
| `hol_peopl_dtp_area_governance_001` | `hol_finan_dtp_area_buildout_001` (proposed) | **Not minted** |
| `validate_area_completeness.py` | Same validator — Finance row **50%** | **Runnable**; Finance fails 5 gaps |
| `DATA_AREA_CHARTER.md` | `FINANCE_AREA_CHARTER.md` | **Not minted** |
| Quality Fabric §6 specialty | FINOPS discipline citation | **Partial** (I88 only) |

**Verdict:** Research and roadmap **inherit** the People model; **vault parity with Data is F1 deliverable**, not done.

### 3. Are recommended **tools** listed, governed, and **plan minted**?

**“Tools” = validators, scripts, SOPs, registries, Edge Functions, cursor rule/skill pairs.**

| Category | Listed in research? | Governed (SOP/process/registry)? | Plan minted? |
|:---|:---:|:---:|:---:|
| Counterparty register + validator | ✓ | ✓ (`thi_finan_dtp_303`, SOP maintenance) | **Live** |
| Stripe → finops writer pipeline | ✓ | ✓ (USER_GUIDE, migrations) | **Live** |
| FINOPS bridge SOP | ✓ | ✓ (RevOps) | **Live** |
| Mirror DML apply | ✓ | ✓ (`env_tech_dtp_compliance_mirror_dml_001`) | **Live** |
| `dataops_quality_check` / DATA-FAM | ✓ | ✓ (I93) | **Live**; FINOPS-specific probes **F3** |
| `FINOPS_REVENUE_RECOGNITION_POLICY` | ✓ | **OPS-81-5** open | **OPS row only** |
| `PRICING_TIER_REGISTRY` | ✓ | **OPS-81-6** open | **OPS row only** |
| `FINOPS_TAX_CALENDAR` | ✓ | **OPS-81-13** open | **OPS row only** |
| `validate_pricing_tier_registry.py` | ✓ | Forward-charter in OPS-81-6 | **Not in repo** |
| `validate_finops_tax_calendar.py` | ✓ | Forward-charter in OPS-81-13 | **Not in repo** |
| Finance cursor rule + skill | ✓ | F3 roadmap | **Not minted** |
| Five cross-area DC-* contracts | ✓ | F2 roadmap | **Not in DATA_CONTRACT_REGISTRY** |
| `METRICS_REGISTRY` finance rows | ✓ | F2 roadmap | **Partial** (Data registry exists) |

**Verdict:** **Operational core is governed.** **Pricing, tax, rev-rec, and cross-area contracts are planned in OPS_REGISTER + F2 — not vault-minted yet.**

### 4. Will the plan **guarantee** end-to-end process followability?

| Requirement for E2E | In F0–F4 plan? | Today |
|:---|:---:|:---:|
| Paired SOP + runbook on every money-touching process | F2 | **0/16** runbook_path filled in CSV |
| Human AC-HUMAN steps in SOPs | F1–F2 | Partial (8 processes cite SOP paths) |
| AIC AC-AUTOMATION validators in release-gate | F3 | Partial (`validate_finops_*`) |
| Data contract breach = visible FAIL | F3 | GTM-CRM seed only |
| Monthly recon evidence | F3–F4 | None yet |
| Closure UAT with operator sign-off | F4 | None for Finance area |

**Verdict:** The plan **can** guarantee E2E **when executed and closed at F4** — it does **not** guarantee it from research reports alone. Traceability without execution would repeat the P1 desk-audit gap.

### 5. Were **all findings minted** for traceability?

#### Minted (I88 `reports/` — git-tracked when committed)

| Artifact | Path |
|:---|:---|
| Finance full-governance research pack | `research-finance-full-governed-area-2026-06-05/` |
| Source ledger (v1) | `.../source-ledger.csv` |
| Intent regression | `intent-regression-finance-bar-2026-06-05.md` |
| Programme roadmap F0–F4 | `finance-area-buildout-roadmap-2026-06-05.md` |
| P1 sweep (superseded for area bar) | `p1-finops-pillar-sweep-2026-06-05.md` |
| P1 entry research | `research-p1-entry-gate-2026-06-05/` |
| **This inventory** | `finance-governance-traceability-inventory-2026-06-05.md` |
| Expanded source ledger (v2) | `research-finance-full-governed-area-2026-06-05/source-ledger-v2.csv` |

#### Not minted (still forward — required for vault traceability)

| Finding | Target surface | Phase |
|:---|:---|:---|
| Finance buildout inception decision | `DECISION_REGISTER.csv` + I88 decision-log | F0 |
| `FINANCE_AREA_CHARTER.md` | Vault | F1 |
| `FINOPS_DISCIPLINE.md` | Vault | F1 |
| DC-FINOPS-* rows | `DATA_CONTRACT_REGISTRY.csv` | F2 |
| `PRICING_TIER_REGISTRY.csv` | Vault + validator | F2 (OPS-81-6) |
| `FINOPS_REVENUE_RECOGNITION_POLICY.md` | Vault | F2 (OPS-81-5) |
| `FINOPS_TAX_CALENDAR.csv` | Vault | F2 (OPS-81-13) |
| `files-modified.csv` commit SHAs | I88 initiative | Per commit |
| Closure UAT | `uat-finance-area-buildout-*.md` | F4 |

#### Pre-existing traceability (use, do not duplicate)

| Artifact | Role |
|:---|:---|
| I81 FINOPS synthesis | Five-plane model + OPS-81-* backlog |
| `OPERATOR_INBOX.md` | OPS-81-5/6/13 priority |
| `baseline_organisation.csv` | Pricing, Taxes, O2C, PTP roles |
| `process_list.csv` | `thi_finan_dtp_126`, `203`, etc. |
| PMO `PRICING_MODEL.md` | **Commercial** pricing narrative (join to Finance registries at F2) |

---

## Pricing and Taxes — dedicated section

### Org design (already ratified in baseline)

| Role | Reports to | Function | Status |
|:---|:---|:---|:---|
| **Pricing** | Business Controller | Pricing database + logic; approves usage | **planned** |
| **Taxes** | Business Controller | Tax DB as date/ratio multiplier on financial data | **planned** |

**Philosophy (fits Holistika):** Operations can run **pre-tax**; Taxes applies governed ratios for **statement-facing** outputs — not blocking pipeline design.

### Processes (process_list — exist, not fully paired)

| Process ID | Name | Capability | SOP in CSV? |
|:---|:---|:---|:---:|
| `thi_finan_dtp_126` | Pricing Definition | CAP-THI-FINAN-DTP-126 | No |
| `thi_finan_dtp_203` | Subscription Pricing Strategy | CAP-THI-FINAN-DTP-203 | No |
| `thi_finan_dtp_125` | Budget Scope | CAP-THI-FINAN-DTP-125 | No |

### Vault folders

- `Finance/Business Controller/Pricing/` — **`.gitkeep` only**
- `Finance/Business Controller/Taxes/` — **`.gitkeep` only**

### OPS plans (governed backlog — **plan minted**, artifact not)

| OPS ID | Deliverable | Severity |
|:---|:---|:---|
| **OPS-81-5** | `FINOPS_REVENUE_RECOGNITION_POLICY.md` (ASC 606 / IFRS 15 perf obligations) | CRITICAL before first sale |
| **OPS-81-6** | `PRICING_TIER_REGISTRY.csv` + FK to perf obligations + validators | HIGH |
| **OPS-81-13** | `FINOPS_TAX_CALENDAR.csv` (Modelo 200/720/036, IVA, etc.) | CRITICAL |
| **OPS-81-14** | Hacienda Foral vs AEAT territoriality doctrine | HIGH |
| **OPS-81-16** | ENISA reporting cadence (feeds tax calendar) | HIGH |

### Marketing / PMO join (important)

| Surface | Owner | Finance join at F2 |
|:---|:---|:---|
| `Operations/PMO/.../PRICING_MODEL.md` | PMO / strategy | Map tiers to `PRICING_TIER_REGISTRY`; external deck numbers cite metric catalog |
| `SERVICE_OFFERING_CATALOG.md` | Marketing | Capacity narrative → `thi_finan_dtp_203` tiers |
| MKT `thi_finan_dtp_272` | Capex alignment | DC-MKT-FINOPS-CAPEX-001 |

**Pricing lesson:** Do **not** let three pricing stories diverge (PMO model, product tiers, FINOPS recognition). F2 mint makes **Finance registry SSOT**; PMO/MKT **consume**.

**Tax lesson:** Tax is **counsel-encoded + calendar-driven** (OPS-81-13/14), not invented by AIC. Gestoría executes Layer A per D-IH-81-P; Holistika encodes **obligations and dates** agent-readably.

### External evidence (pricing/tax) — see `source-ledger-v2.csv`

ASC 606 five-step model, SSP allocation, tier changes (Numeric, Stripe, DualEntry, HubiFi, Certinia); Spain filings remain OPS-81-13 scoped with AEAT references from I81 synthesis.

---

## Methodology / philosophy layer (not only processes)

| Holistika doctrine | How Finance programme expresses it |
|:---|:---|
| D-IH-81-P internal-first + activation triggers | OPS-81-20 judgment SOPs; no CFOaaS default |
| D-IH-93-B area buildout | Same 14-component bar as Data |
| Quality Fabric dual register | FINOPS outbound = brand + render trail (pillar 9) |
| People discipline-of-disciplines | CPO owns pattern; CFO owns Finance body |
| Data mesh / contracts (I93) | Finance as producer/consumer via DC-* |
| Collaborator share | People payout contract (two-fact invariant) |

**Mint gap:** `FINANCE_AREA_CHARTER.md` should open with **philosophy + boundaries** (like `DATA_AREA_CHARTER.md`), not only process list — **F0/F1**.

---

## Recommended next traceability commits

1. **Commit** all `reports/*` inventory + expanded ledger (research traceability).
2. **F0:** `DECISION_REGISTER` row `D-IH-88-FINANCE-FULL` (or extend I88 log) + ratify programme.
3. **F1:** Vault mint charter + discipline + `files-modified` + `validate_hlk`.

---

## Cross-references

- Research: [`research-finance-full-governed-area-2026-06-05/master-synthesis.md`](research-finance-full-governed-area-2026-06-05/master-synthesis.md)
- Roadmap: [`finance-area-buildout-roadmap-2026-06-05.md`](finance-area-buildout-roadmap-2026-06-05.md)
- I81 synthesis: [`docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/i81/p2-tranche-t1-finops-synthesis-2026-05-22.md`](../../81-vault-integrity-layout-milestones-retrofit/reports/i81/p2-tranche-t1-finops-synthesis-2026-05-22.md)
