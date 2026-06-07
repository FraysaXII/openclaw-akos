---
intellectual_kind: capability_collapse_map
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L2 — Capability de-densify (R2-01) — small-area tranche (Data + Finance + Legal)
authored: 2026-06-08
status: draft
related_decisions:
  - D-IH-95-H   # ratified: keep-separate + de-densify CAPABILITY_REGISTRY into a stable map
  - D-IH-95-G   # Round-2 batch; R2-01
  - D-IH-82-P   # CAPABILITY_REGISTRY seed mint (the 1:1 process-shadow source)
language: en
audience: J-OP;J-AIC
register: internal
control_confidence_level: Euclid
internal_citations: 6
external_citations: 1
note: >
  Proposed de-densified capability maps for three SMALL areas — Data (17),
  Finance (16), Legal (11) = 44 process-shadow rows. The de-densify DIRECTION
  is Keter-settled (D-IH-95-H); THIS map is the Euclid-grade PARAMETER proposal
  for the three small areas, pending the per-area canonical-CSV-write ratification
  gate (the actual CAPABILITY_REGISTRY rewrite is a gated canonical change —
  akos-baseline-governance.mdc). Readonly research + one doc write; no canonical
  CSV is modified here.
---

# L2 collapse map — Data + Finance + Legal (44 shadows → 11 stable capabilities)

> **One-line answer:** These three areas are small and already near-strategic, so
> the collapse is **light** (4.0:1, not the ~10:1+ the GTM/MADEIRA areas need).
> The shrink comes from two mechanisms only — **near-duplicate / cross-entity dedup**
> and **task-grain folding** (keeping the granular rows in `process_list` as
> *realizations*, not deleting them). **Zero rows evict to
> `COMPONENT_PRIMITIVE_REGISTRY`** because none of the 44 are deliverable/UI
> primitives or MADEIRA code symbols. Proposed headline counts: **Data 17 → 4,
> Finance 16 → 4, Legal 11 → 3.**

This is a Tier-1 Research-area WIP proposal (`docs/wip/intelligence/`, internal
register permitted). It applies the ratified 6-step `capability_densify` method
from the [L2 method doc](../l2-capability-densify-findings-2026-06-07.md) to the
three small areas. It does **not** re-argue keep-vs-fuse (settled at D-IH-95-H).

---

## 0. Method recap + what I inspected (so this is falsifiable)

**Inputs read:** the [L2 method doc](../l2-capability-densify-findings-2026-06-07.md)
(6-step collapse; naming rules; ~9 L1 domains; worked clusters #8 Legal, #9/#10
Data); the 44 filtered `CAPABILITY_REGISTRY.csv` rows for `area ∈ {Data, Finance,
Legal}`; and `COMPONENT_PRIMITIVE_REGISTRY.csv` (the declared eviction target).

**The 6-step method (from §3.2 of the method doc), applied here:**

1. **Strip non-capabilities (eviction).** Code symbols → `COMPONENT_PRIMITIVE_REGISTRY`;
   task-grain micro-steps → stay in `process_list` as realizations. *Result for
   these areas: 0 component-registry evictions* (see §3).
2. **Normalize to (area, theme).** Group by `area` + `role_owner` + the obvious
   process theme.
3. **Merge across entity/convention.** Collapse `THI-*` / `HOL-*` duplicates of the
   same ability into one bearer-agnostic capability (e.g. Legal trademark-naming).
4. **Name as nouns/gerunds, outcome-oriented, technology-neutral.** "RPA" and
   "Create Relational Functions in SQL" are *techniques*, not capability names.
5. **Assign L1 domain + tier.** L1 ∈ {Legal·Compliance·Privacy / Finance·Revenue
   Operations / Data Governance·Enterprise Knowledge}. Tier ∈ {differentiating /
   utility} (proposed; the Q6 `capability_tier` column).
6. **Wire, don't copy.** Each new L2 carries its `originating_process_ids` (now
   **N:N** — many processes per capability) via the `realization` verb (TRP-006);
   **`bearer_class` lives on the realization edge, not the capability row** (Q4) —
   so every proposed capability is bearer-agnostic.

**Eviction-target finding (important):** `COMPONENT_PRIMITIVE_REGISTRY.csv` holds
**deliverable / UI component primitives** (cover page, executive summary, CTA,
slide-hero, data-table, form-field, confidentiality-block — 26 `CP-*` rows). **None
of the 44 Data/Finance/Legal rows are deliverable-UI primitives or code symbols**,
so the registry is not the destination for any shrink here. The shrink is dedup +
task-grain folding, both of which keep rows alive in `process_list`.

---

## 1. Proposed capabilities (the de-densified map)

Columns: proposed bearer-agnostic `capability_id` · stable name (noun-phrase) · L1
domain · proposed tier · primary `role_owner` (+ co-owners) · rolled-up
lifecycle · `realizes` (the `originating_process_ids`, N:N via TRP-006).

### 1.1 Legal — 11 → 3

| # | Proposed `capability_id` | Stable capability name | L1 domain | Tier | Owner (+co) | Lifecycle | Realizes (`originating_process_ids`) |
|:--|:--|:--|:--|:--|:--|:--|:--|
| L1 | `CAP-LEGAL-INSTRUMENT-LIFECYCLE` | Legal Instrument Lifecycle Management | Legal, Compliance & Privacy | utility | Legal Consumer Specialist (+Legal Collaborator Specialist) | planned | `thi_legal_dtp_21`; `thi_legal_dtp_22`; `thi_legal_dtp_23`; `thi_legal_dtp_26`; `thi_legal_dtp_27` |
| L2 | `CAP-LEGAL-IP-TRADEMARK` | Intellectual Property & Trademark Management | Legal, Compliance & Privacy | **differentiating** | Legal Counsel | active | `hol_lgl_prc_trademark_naming_governance_001`; `hol_lgl_prc_trademark_monitoring_001`; `hol_lgl_prc_ip_register_mtnce_001`; `thi_legal_dtp_303` *(deprecated shadow, merged)* |
| L3 | `CAP-LEGAL-CORP-ENTITY-READINESS` | Corporate & Entity Legal Readiness | Legal, Compliance & Privacy | utility | Legal Counsel | active (partial) | `thi_legal_dtp_302`; `thi_legal_dtp_304` |

### 1.2 Finance — 16 → 4

| # | Proposed `capability_id` | Stable capability name | L1 domain | Tier | Owner (+co) | Lifecycle | Realizes (`originating_process_ids`) |
|:--|:--|:--|:--|:--|:--|:--|:--|
| F1 | `CAP-FIN-PRICING-MONETIZATION` | Pricing & Monetization Strategy | Finance & Revenue Operations | **differentiating** | Business Controller | planned | `thi_finan_dtp_126`; `thi_finan_dtp_203` |
| F2 | `CAP-FIN-REVENUE-OPS-BILLING` | Revenue Operations & Billing (quote-to-cash) | Finance & Revenue Operations | utility | Business Controller | active (partial) | `thi_finan_dtp_261`; `thi_finan_dtp_271`; `thi_finan_dtp_301`; `thi_finan_dtp_308` |
| F3 | `CAP-FIN-BUDGET-COST-CAPITAL` | Budget, Cost & Capital Planning | Finance & Revenue Operations | utility | Business Controller (+PMO) | active (partial) | `thi_finan_dtp_125`; `thi_finan_dtp_272`; `thi_finan_dtp_273`; `thi_finan_dtp_302` |
| F4 | `CAP-FIN-COUNTERPARTY-MDM` | Counterparty & Financial Master-Data Stewardship | Finance & Revenue Operations | utility | Business Controller | active | `thi_finan_dtp_303`; `thi_finan_dtp_304`; `thi_finan_dtp_305`; `thi_finan_dtp_306`; `thi_finan_dtp_307`; `thi_finan_dtp_309` |

### 1.3 Data — 17 → 4

L1-domain split mirrors the **DAMA-DMBOK 2.0** knowledge-area taxonomy (11 areas,
Data Governance at the hub — DAMA International, 2024 revision [E-1]): Reference/Master
Data + Warehousing/BI → F-D1; Architecture + Modeling/Design + Storage → D2;
Integration/Interoperability + Quality + Metadata(lineage) → D3; Storage/Operations
as productized data-as-a-product → D4.

| # | Proposed `capability_id` | Stable capability name | L1 domain | Tier | Owner (+co) | Lifecycle | Realizes (`originating_process_ids`) |
|:--|:--|:--|:--|:--|:--|:--|:--|
| D1 | `CAP-DATA-ENTERPRISE-MGMT-MDM` | Enterprise Data Management & Master Data | Data Governance & Enterprise Knowledge | utility | Data Steward (+Data Engineer) | planned | `thi_data_dtp_31`; `thi_data_dtp_32`; `thi_data_dtp_33`; `thi_data_dtp_34` |
| D2 | `CAP-DATA-MODELING-ENGINEERING` | Data Modeling & Database Engineering | Data Governance & Enterprise Knowledge | utility | Data Governance Office (+Data Engineer) | planned | `thi_data_dtp_77`; `thi_data_dtp_76`; `thi_data_dtp_78` |
| D3 | `CAP-DATA-PIPELINE-QUALITY-LINEAGE` | Data Pipeline, Quality & Lineage | Data Governance & Enterprise Knowledge | utility | Data Engineer (+Data Steward) | planned | `SOP-ETL_MACROECON_INGESTION_001`; `thi_data_dtp_274`; `thi_data_dtp_275` |
| D4 | `CAP-DATA-PLATFORM-PRODUCTS` | Enterprise Data Platform & Data-Product Stewardship | Data Governance & Enterprise Knowledge | **differentiating** | Data Governance Office (+RevOps Manager, +System Owner) | active | `hol_data_dtp_datafam_compliance_mirror_001`; `hol_data_dtp_datafam_canonical_csv_001`; `hol_data_dtp_datafam_engagement_fact_001`; `hol_data_dtp_datafam_telemetry_obs_001`; `hol_data_dtp_datafam_gtm_crm_001`; `hol_data_dtp_datafam_km_topic_001`; `hol_data_dtp_datafam_aic_runtime_001` |

---

## 2. Rollup — every old shadow → its new home (the accounting ledger)

All 44 old `CAPABILITY_REGISTRY` rows are listed below with the proposed target
capability and the collapse rationale. This is the "every old row accounted for"
proof; §5 sums it.

### 2.1 Legal (11 rows)

| Old `capability_id` | Old name | → New capability | Collapse rationale |
|:--|:--|:--|:--|
| `CAP-THI-LEGAL-DTP-21` | Terms and Conditions | L1 Instrument Lifecycle | consumer legal instrument |
| `CAP-THI-LEGAL-DTP-22` | Privacy | L1 Instrument Lifecycle | privacy policy = an instrument (see §4.1 split alternative) |
| `CAP-THI-LEGAL-DTP-23` | Retention (Think Big Legal) | L1 Instrument Lifecycle | retention policy = an instrument |
| `CAP-THI-LEGAL-DTP-26` | NDA (Think Big Legal template A) | L1 Instrument Lifecycle | task-grain template → realization |
| `CAP-THI-LEGAL-DTP-27` | NDA (Think Big Legal template B) | L1 Instrument Lifecycle | **near-duplicate of template A** → same capability, 2 realizations |
| `CAP-HOL-LGL-PRC-TRADEMARK-NAMING-GOVERNANCE-001` | Trademark naming governance | L2 IP & Trademark | the canonical (active) bearer |
| `CAP-THI-LEGAL-DTP-303` | Trademark and Naming Governance | L2 IP & Trademark | **cross-entity dedup** — deprecated THI shadow of the active HOL row above |
| `CAP-HOL-LGL-PRC-TRADEMARK-MONITORING-001` | Trademark monitoring | L2 IP & Trademark | trademark lifecycle |
| `CAP-HOL-LGL-PRC-IP-REGISTER-MTNCE-001` | IP register maintenance | L2 IP & Trademark | IP portfolio operations |
| `CAP-THI-LEGAL-DTP-302` | Founder Entity Formation Readiness | L3 Corp & Entity Readiness | corporate formation |
| `CAP-THI-LEGAL-DTP-304` | Filed instruments register maintenance | L3 Corp & Entity Readiness | the register of filed formation/legal instruments |

### 2.2 Finance (16 rows)

| Old `capability_id` | Old name | → New capability | Collapse rationale |
|:--|:--|:--|:--|
| `CAP-THI-FINAN-DTP-126` | Pricing Definition | F1 Pricing & Monetization | pricing |
| `CAP-THI-FINAN-DTP-203` | Subscription Pricing Strategy | F1 Pricing & Monetization | pricing (subscription variant) |
| `CAP-THI-FINAN-DTP-261` | KiRBe Stripe Billing Activation and Reconciliation | F2 Revenue Ops & Billing | billing + reconciliation |
| `CAP-THI-FINAN-DTP-271` | BID Lead-to-Contract Revenue Chain | F2 Revenue Ops & Billing | quote-to-cash pipeline |
| `CAP-THI-FINAN-DTP-301` | Revenue Share Automation (Partnerships) | F2 Revenue Ops & Billing | partner revenue settlement |
| `CAP-THI-FINAN-DTP-308` | Holistika Stripe Wrappers FDW stewardship | F2 Revenue Ops & Billing | billing-data plumbing (cross-area → Data, §4.2) |
| `CAP-THI-FINAN-DTP-125` | Budget Scope | F3 Budget, Cost & Capital | budgeting |
| `CAP-THI-FINAN-DTP-272` | Capex Alignment for Paid Media and Channel Spend | F3 Budget, Cost & Capital | capex allocation |
| `CAP-THI-FINAN-DTP-273` | Process-Cost and FTE Mapping from Organigrama | F3 Budget, Cost & Capital | process-cost/FTE (cross-area → PMO/People, §4.2) |
| `CAP-THI-FINAN-DTP-302` | Founder-to-Company Funding Path | F3 Budget, Cost & Capital | capital planning / funding (cross-area → Legal, §4.2) |
| `CAP-THI-FINAN-DTP-303` | FINOPS counterparty register maintenance | F4 Counterparty MDM | the counterparty register itself |
| `CAP-THI-FINAN-DTP-304` | Counterparty onboarding and offboarding checklist | F4 Counterparty MDM | task-grain checklist → realization |
| `CAP-THI-FINAN-DTP-305` | Counterparty data classification and sensitivity review | F4 Counterparty MDM | counterparty data governance |
| `CAP-THI-FINAN-DTP-306` | Legal and entity readiness gate for financial facts | F4 Counterparty MDM | registered-fact entity gate (cross-area → Legal, §4.2) |
| `CAP-THI-FINAN-DTP-307` | Annual counterparty rationalization and renewal review | F4 Counterparty MDM | counterparty renewal cadence |
| `CAP-THI-FINAN-DTP-309` | Counterparty segment and revenue metadata review | F4 Counterparty MDM | counterparty segment/metadata |

### 2.3 Data (17 rows)

| Old `capability_id` | Old name | → New capability | Collapse rationale |
|:--|:--|:--|:--|
| `CAP-THI-DATA-DTP-31` | Query, KPI & Reporting Catalog | D1 Enterprise Data Mgmt & MDM | BI/reporting catalog |
| `CAP-THI-DATA-DTP-32` | Enterprise MasterData (Relationship Management) | D1 Enterprise Data Mgmt & MDM | master data (DAMA Reference/Master Data) |
| `CAP-THI-DATA-DTP-33` | Datamarts & Enterprise Applications | D1 Enterprise Data Mgmt & MDM | warehousing/marts |
| `CAP-THI-DATA-DTP-34` | RPA | D1 Enterprise Data Mgmt & MDM | **tech-named** (anti-pattern E-19) → folded as automation realization, name retired |
| `CAP-THI-DATA-DTP-77` | Data Modeling | D2 Modeling & Database Eng | the modeling capability (DAMA Modeling/Design) |
| `CAP-THI-DATA-DTP-76` | Create Relational Functions in SQL | D2 Modeling & Database Eng | **task-grain technique** → realization |
| `CAP-THI-DATA-DTP-78` | Column Types | D2 Modeling & Database Eng | **task-grain concept** → realization |
| `CAP-SOP-ETL-MACROECON-INGESTION-001` | Macroeconomic ETL Ingestion | D3 Pipeline, Quality & Lineage | ingestion/ETL (DAMA Integration) |
| `CAP-THI-DATA-DTP-274` | KiRBe Ingestion Data Quality Monitoring | D3 Pipeline, Quality & Lineage | data quality (cross-area → KiRBe product, §4.3) |
| `CAP-THI-DATA-DTP-275` | Formal Data Lineage (Ingestion → Supabase → Graph) | D3 Pipeline, Quality & Lineage | lineage/metadata |
| `CAP-HOL-DATA-FAM-COMPLIANCE-MIRROR-001` | DATA-FAM compliance mirror product | D4 Data Platform & Products | data-product plane (TRP-053 specialization) |
| `CAP-HOL-DATA-FAM-CANONICAL-CSV-001` | DATA-FAM canonical CSV SSOT product | D4 Data Platform & Products | data-product plane |
| `CAP-HOL-DATA-FAM-ENGAGEMENT-FACT-001` | DATA-FAM engagement operational facts product | D4 Data Platform & Products | data-product plane |
| `CAP-HOL-DATA-FAM-TELEMETRY-OBS-001` | DATA-FAM telemetry and observability facts product | D4 Data Platform & Products | data-product plane |
| `CAP-HOL-DATA-FAM-GTM-CRM-001` | DATA-FAM GTM CRM plane product | D4 Data Platform & Products | data-product plane (cross-area → RevOps, §4.3) |
| `CAP-HOL-DATA-FAM-KM-TOPIC-001` | DATA-FAM KM topic-fact-source graph product | D4 Data Platform & Products | data-product plane |
| `CAP-HOL-DATA-FAM-AIC-RUNTIME-001` | DATA-FAM AIC runtime persistence product | D4 Data Platform & Products | data-product plane (cross-area → Tech/System Owner, §4.3) |

---

## 3. Evictions

**Headline: 0 evictions to `COMPONENT_PRIMITIVE_REGISTRY.csv` across all three areas.**
That registry holds deliverable/UI primitives (cover page, CTA, slide-hero,
data-table, form-field, confidentiality-block); none of the 44 rows are UI
primitives or MADEIRA code symbols (those live only in the GTM/MADEIRA areas — method
doc §0). So the shrink here is **not** eviction-to-components — it is dedup +
task-grain folding, and **no row is deleted** (folded rows stay in `process_list`
as `realization` edges).

### 3.1 Legal evictions

- **Component-registry evictions: 0.**
- **Cross-entity / near-duplicate dedup (−2 capability rows):**
  - `thi_legal_dtp_303` (deprecated *Trademark and Naming Governance*, THI) ≡
    `hol_lgl_prc_trademark_naming_governance_001` (active, HOL) → **one** capability.
  - `thi_legal_dtp_26` (NDA template A) ≡ `thi_legal_dtp_27` (NDA template B) →
    **one** NDA ability, two template realizations.
- **Task-grain demotions (stay as `process_list` realizations):** the two NDA
  templates (26, 27) are templates, not capabilities.

### 3.2 Finance evictions

- **Component-registry evictions: 0.**
- **Cross-entity dedup: 0** (no THI/HOL duplicate pair; all 16 are `thi_finan_*`).
- **Task-grain demotions (stay as `process_list` realizations):**
  - `thi_finan_dtp_304` (Counterparty onboarding/offboarding **checklist**) — a
    checklist artifact → realization of F4 Counterparty MDM, not its own capability.
- The Finance shrink (16 → 4) is **pure theme-clustering** of six counterparty
  process-shadows (303/304/305/306/307/309) into one register-stewardship capability
  plus three small thematic groups — the largest single collapse in this tranche.

### 3.3 Data evictions

- **Component-registry evictions: 0.**
- **Cross-entity dedup: 0** (the `thi_data_*` classic rows and the `hol_data_*`
  DATA-FAM product rows are distinct families, not duplicates).
- **Task-grain demotions (stay as `process_list` realizations):**
  - `thi_data_dtp_76` (Create Relational Functions in SQL) — a SQL technique.
  - `thi_data_dtp_78` (Column Types) — a typing concept.
  - `thi_data_dtp_34` (RPA) — **technology-named** (anti-pattern E-19, method doc
    §3.2 step 4): folded into D1 as an automation realization; the capability is
    *named for the outcome*, not the tool.
- **TRP-053 note:** the 7 DATA-FAM `hol_data_*` rows are *data products*, which the
  HCAM relationship registry already models as **specializations** of a capability
  (TRP-053 `data_product —specialization→ capability`). Collapsing them into one
  `CAP-DATA-PLATFORM-PRODUCTS` capability (with 7 plane-realizations) is the
  doctrine-faithful move — not 7 separate capability rows.

---

## 4. Cross-area flags

Capabilities/realizations whose `role_owner` or subject crosses an area boundary —
these are the rows the operator should sanity-check against the owning area's map so
the same ability is not double-counted in two areas.

### 4.1 Legal cross-area flags

- **`CAP-LEGAL-IP-TRADEMARK` ↔ Marketing/Brand.** *Trademark naming governance*
  is the Legal half of the brand-naming decision flow that also touches brand
  architecture + domain topology (the `brand-naming-craft` skill composes all three).
  Keep the *clearance/registration* ability in Legal; the *naming candidate / brand
  architecture* ability stays in Marketing. Flag for de-dup against the Marketing map.
- **Design decision (Privacy split).** Privacy (22) + Retention (23) are folded into
  L1 Instrument Lifecycle as *instruments*. **Alternative for ratification:** split a
  4th Legal capability `CAP-LEGAL-PRIVACY-DATAPROTECTION` (privacy + retention) to
  mirror the L1 domain name "…& Privacy". Recommended default: **keep folded** (these
  are Think-Big consumer document templates, not a standing privacy program) — but
  surface as an inline-ratify option (would make Legal 11 → 4).

### 4.2 Finance cross-area flags

- **`thi_finan_dtp_273` (Process-Cost & FTE Mapping from Organigrama) → owned by PMO**,
  sources from `baseline_organisation.csv` (People/Operations). Flag Finance ↔ PMO/People.
- **`thi_finan_dtp_308` (Stripe Wrappers FDW stewardship) ↔ Data.** FDW is a data-plane
  concern (DATAOPS); owned by Business Controller but mechanically a Data capability.
  Flag Finance ↔ Data (do not also land it in the Data map).
- **`thi_finan_dtp_306` (Legal & entity readiness gate) + `thi_finan_dtp_302`
  (Founder-to-Company Funding Path) ↔ Legal.** Both depend on
  `CAP-LEGAL-CORP-ENTITY-READINESS` (entity formation). Flag Finance ↔ Legal —
  the *funding/financial-fact* ability is Finance; the *entity-formation* ability is Legal.
- **`CAP-FIN-COUNTERPARTY-MDM` ↔ Data (MDM boundary).** Counterparty master-data lives
  in Finance, but "Enterprise MasterData" (`thi_data_dtp_32`) lives in Data. Intentional
  split: Finance owns the *counterparty* register; Data owns *generic* enterprise MDM.
  Flag so the two MDM capabilities stay distinct rather than merging.

### 4.3 Data cross-area flags

- **`hol_data_dtp_datafam_gtm_crm_001` (GTM CRM plane) → owned by RevOps Manager.**
  Flag Data ↔ RevOps/Marketing — the data-product *plane* is Data; the GTM *use* is RevOps.
- **`hol_data_dtp_datafam_aic_runtime_001` (AIC runtime persistence) → owned by System
  Owner.** Flag Data ↔ Tech (System Owner) — runtime persistence straddles Data + Tech.
- **`thi_data_dtp_274` (KiRBe Ingestion Data Quality) ↔ KiRBe product plane.** Flag
  Data ↔ KiRBe/product (the quality ability is Data; the KiRBe pipeline is product).
- **`thi_data_dtp_34` (RPA) ↔ Operations/Tech.** Process automation is not purely a
  Data ability; flagged so a future Operations map can claim the automation realization.

---

## 5. Count summary per area

| Area | Old shadows | → Proposed capabilities | Collapse ratio | Of which differentiating | Component-registry evictions |
|:--|:--:|:--:|:--:|:--:|:--:|
| **Data** | 17 | **4** | 4.3 : 1 | 1 (D4 Platform & Products) | 0 |
| **Finance** | 16 | **4** | 4.0 : 1 | 1 (F1 Pricing) | 0 |
| **Legal** | 11 | **3** | 3.7 : 1 | 1 (L2 IP & Trademark) | 0 |
| **Combined** | **44** | **11** | **4.0 : 1** | 3 | **0** |

**Accounting check (every old row accounted for):**

- Legal: 5 (L1) + 4 (L2, incl. 1 deprecated-dedup) + 2 (L3) = **11** ✓
- Finance: 2 (F1) + 4 (F2) + 4 (F3) + 6 (F4) = **16** ✓
- Data: 4 (D1) + 3 (D2) + 3 (D3) + 7 (D4) = **17** ✓
- **Total: 44 shadows → 11 stable capabilities; 0 deleted, 0 evicted to components.**

This 4.0:1 light collapse confirms the brief's prior: these three areas were already
near-strategic. (Contrast the method doc's worked GTM/MADEIRA clusters #3/#4 at
~27→1 and ~35→1.) The proposed 11 sit comfortably inside the 40–100 L2 strategic band
the method doc targets [E-1 / method §2].

**Next step (gated):** the actual `CAPABILITY_REGISTRY.csv` rewrite (44 rows → 11,
re-keyed bearer-agnostic, `originating_process_ids` set N:N, `capability_tier` added)
is a **canonical-CSV change** — operator approval per `akos-baseline-governance.mdc`,
ideally as a per-area slice (Q7 in the method doc). The Privacy-split (§4.1) and the
tier assignments (§1) are the two inline-ratify options to resolve at that gate.

---

## Citations & cross-references

**Internal:**
- **[I-1]** [`l2-capability-densify-findings-2026-06-07.md`](../l2-capability-densify-findings-2026-06-07.md) — the ratified 6-step method, naming rules, ~9 L1 domains, worked clusters #8/#9/#10 (D-IH-95-H).
- **[I-2]** `…/dimensions/CAPABILITY_REGISTRY.csv` — the 44 filtered Data/Finance/Legal process-shadow rows (source).
- **[I-3]** `…/dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv` — the declared eviction target (26 `CP-*` deliverable/UI primitives; 0 fits here).
- **[I-4]** `…/dimensions/CANONICAL_RELATIONSHIP_REGISTRY.csv` — TRP-006 (`process —realization→ capability`, N:N), TRP-053 (`data_product —specialization→ capability`).
- **[I-5]** `.cursor/rules/akos-baseline-governance.mdc` — the canonical-CSV gate governing the §5 rewrite.
- **[I-6]** `.cursor/skills/brand-naming-craft/SKILL.md` — the Legal↔Marketing↔Tech brand-naming composition behind the §4.1 IP&Trademark flag.

**External:**
- **[E-1]** DAMA-DMBOK 2.0 (2024 maintenance revision) — 11 data-management knowledge areas with Data Governance at the hub; basis for the §1.3 Data 4-way split. DAMA International, https://dama.org/learning-resources/dama-data-management-body-of-knowledge-dmbok/ ; summarized at https://atlan.com/dama-dmbok-framework/ and https://www.dataversity.net/data-concepts/what-is-the-data-management-body-of-knowledge-dmbok/ .

**Cross-references:**
- Parent lane: I95 master-roadmap → L2 (capability de-densify).
- Sibling: the method doc [I-1] (this map applies it); the GTM/MADEIRA + remaining-area collapse maps land as sibling files in this `l2-collapse-maps/` folder.
