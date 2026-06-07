---
intellectual_kind: capability_collapse_map
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L2 — Capability de-densify (R2-01) — area slice
area: Operations
authored: 2026-06-08
status: proposal
ratified_decision: D-IH-95-H
language: en
audience: J-OP;J-AIC
register: internal
control_confidence_level: Euclid
method_source: docs/wip/intelligence/canonical-articulation-model-2026-06-05/l2-capability-densify-findings-2026-06-07.md
eviction_target: docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv
note: >
  De-densified capability map for ONE area (Operations) of the 1,119-row
  CAPABILITY_REGISTRY process-shadow. Applies the 6-step collapse method
  (l2 findings §3.2): strip non-capabilities → normalize to (area,theme) →
  merge across entity/convention → name as nouns/gerunds (tech-neutral) →
  assign L1 domain → wire (don't copy). Keep-separate from process_list;
  link by the `realization` verb (TRP-006). Readonly research + one doc write.
  Every one of the 404 Operations rows is accounted for: rolled-up, evicted,
  or cross-area-flagged. This is a PROPOSAL feeding the L2 canonical-CSV gate —
  no canonical CSV is modified here.
---

# L2 collapse map — Operations area (404 → 18 + 9 evicted)

> **Headline:** The Operations slice of `CAPABILITY_REGISTRY` is **404 process-shadow
> rows** that collapse to **18 stable capabilities** (+ **9 evicted** non-capabilities).
> ~83% of the slice (337 rows) is a **bilingual company-build-out backlog** (`gtm_cl_* /
> gtm_launch_* / gtm_services_* / gtm_ops_*` — Trello-card task-grain micro-steps), not
> 337 distinct abilities. Those stay in `process_list` as **realizations**; the stable
> *ability* count for Operations is ~18. Several of those abilities are **not really
> Operations** — they belong to Finance, Legal, Research, Applied-AI, Product/Tech, or
> Go-to-Market and are flagged for cross-area merge (§4).

## Method applied (l2 findings §3.2)

1. **Strip non-capabilities (eviction).** Code/script/API symbols → `COMPONENT_PRIMITIVE_REGISTRY`;
   Kanban status enums + TBD placeholders + a Trello-link artifact → delete/park (§3).
2. **Normalize to (area, theme).** The `gtm_*` rows carry their theme verbatim in the
   `capability_name` (e.g. `"Operating model and internal controls — Infrastructure
   documentation: ..."`), giving a ready-made pre-clustering signal; the structured PMO
   rows cluster by `item_id` family + `role_owner`.
3. **Merge across entity/convention.** `CAP-HOL-* / CAP-THI-* / CAP-TBI-* / CAP-GTM-* /
   CAP-TBD-*` variants of the same ability collapse to **one** bearer-agnostic capability.
4. **Name as nouns/gerunds, technology-neutral.** "ERP & Data Platform Build-out", not
   "Pasar a Supabase"; "Component & Tooling Portfolio Management", not "Wrike/Trello/Monday".
5. **Assign L1 domain** from the ~9 (l2 findings §3.3). L1s are *abilities*, not org units —
   so an Operations-filed row can legitimately land in the Finance/Legal/Research L1.
6. **Wire, don't copy.** Each proposed capability lists the old `capability_ids` +
   `originating_process_ids` that realize it (§2); the *how* stays in `process_list`.

---

## 1. Proposed stable capabilities for Operations

> 18 capabilities. `capability_tier` follows the Umbrex/Accelare differentiating-vs-utility
> split [l2 findings E-22]. L1 domains drawn from the ~9 in l2 findings §3.3.

| proposed_capability_id | capability_name | L1_domain | capability_tier | definition (1 sentence) |
|:---|:---|:---|:---|:---|
| CAP-OPS-PROGRAM-PORTFOLIO-MGMT | Program & Portfolio Management | Delivery & Client Engagement Operations | utility | The ability to maintain the live portfolio of programs, projects, scenarios and register-anchors as a single source of truth. |
| CAP-OPS-PROJECT-ENGAGEMENT-PLANNING | Project & Engagement Planning & Estimation | Delivery & Client Engagement Operations | differentiating | The ability to scope, plan and estimate (time/effort/budget, min-par-max) a project or client engagement against defined objectives, deliverables and success metrics. |
| CAP-OPS-DELIVERY-EXECUTION-CADENCE | Delivery Execution & Agile Cadence | Delivery & Client Engagement Operations | utility | The ability to run delivery through agile cadence, gates and meeting/communication rhythm (sprint, ROD/scrum, GO/NO-GO, beta exit). |
| CAP-OPS-OPERATING-MODEL-DESIGN | Operating Model & Internal Controls Design | Delivery & Client Engagement Operations | differentiating | The ability to design the end-to-end operating model, standards and internal controls that bind processes, components and roles into a coherent enterprise. |
| CAP-OPS-PROCESS-CATALOG-MGMT | Process Architecture & Catalog Management | People, Org Design & Quality Fabric | differentiating | The ability to identify, decompose, model, document (SOP) and maintain the process catalog and its SOP↔component traceability. |
| CAP-OPS-WORKFORCE-CAPACITY-PLANNING | Workforce Capacity & Resource Planning | People, Org Design & Quality Fabric | utility | The ability to plan FTE capacity, availability and agile work allocation across quarterly/annual horizons and min-par-max scenarios. |
| CAP-OPS-OPERATIONAL-GOVERNANCE | Operational Governance & Cohesion | People, Org Design & Quality Fabric | differentiating | The ability to gate, regression-check and quarterly-review operational cohesion (vault promotion, regression execution, cohesion review). |
| CAP-OPS-KNOWLEDGE-MGMT-SYSTEM | Knowledge Management & Documentation System | Data Governance & Enterprise Knowledge | utility | The ability to organize, standardize and route the multi-surface knowledge base (Obsidian/Drive/Excalidraw/GitHub) by role and output standard. |
| CAP-OPS-ERP-DATA-PLATFORM-BUILD | ERP & Data Platform Build-out | Product & Platform Engineering | utility | The ability to build the ERP and operational data platform (tables, relations, transactional models, SQL flows, payment/external integrations). |
| CAP-OPS-COMPONENT-PORTFOLIO-MGMT | Component & Tooling Portfolio Management | Product & Platform Engineering | differentiating | The ability to maintain the component/service matrix — operating procedures, criticality, tiering, sourcing and cross-area reuse of every tool/component. |
| CAP-OPS-SERVICE-CATALOG-PRODUCTIZATION | Service Catalog & Productization | Go-to-Market & Brand | differentiating | The ability to define, price (FTE-based) and productize the service catalog, including methodology licensing and service-delivery SOPs. |
| CAP-OPS-INBOUND-LEAD-ROUTING | Inbound Lead Routing & Response SLA | Go-to-Market & Brand | utility | The ability to centralize inbound web leads, route them to BD and honour a response SLA. |
| CAP-OPS-REVENUE-OPERATIONS | Revenue Operations & Engagement Orchestration | Finance & Revenue Operations | differentiating | The ability to orchestrate the revenue engine — QBRs, engagement scaffolding, revenue rollups, CRM sync and counterparty checkpoints. |
| CAP-OPS-FINANCIAL-PLANNING-CONTROL | Financial Planning & Control | Finance & Revenue Operations | utility | The ability to model and control finances — forecast, cost/revenue categorization, P&L, pricing and payment infrastructure. |
| CAP-OPS-MARKET-INTEL-RESEARCH | Market & Competitive Intelligence | Corporate Intelligence & Research | differentiating | The ability to research market demand, buyers, competitors and PESTLE signals and feed them into strategy and the service catalog. |
| CAP-OPS-AGENTIC-USECASE-CATALOG | Agentic & AI Use-case Cataloging | Applied AI & MADEIRA | differentiating | The ability to catalog AI/agent use-cases per channel and area and integrate research/scrapping agents into the intelligence flow. |
| CAP-OPS-ENTITY-FORMATION-SETUP | Entity Formation & Corporate Setup | Legal, Compliance & Privacy | utility | The ability to stand up the legal entity — incorporation, equity split, contracts/NDAs, banking, gestoría/notaría and premises. |
| CAP-OPS-PROCESS-PRIORITIZATION | Process & Capability Prioritization & Sourcing | Delivery & Client Engagement Operations | differentiating | The ability to rank processes/capabilities by criticality, ROI, dependency, FTE difficulty and market demand, and to make make-vs-buy (insource/outsource) decisions. |

---

## 2. Rollup — each proposed capability ← old capability_ids / originating_process_ids

> Seed convention: `capability_id` = `CAP-` + uppercased `process item_id`; `originating_process_ids`
> = that one process (l2 findings §0). So the member lists below are equivalently the
> `originating_process_ids` (lowercase) for TRP-006. `dtp` numbers are abbreviated to ranges
> where contiguous. **Every count is reconciled in §5.**

### Delivery & Client Engagement Operations

**CAP-OPS-PROGRAM-PORTFOLIO-MGMT** ← 11 rows
`hol_opera_dtp_148` (Program Management), `_149` (Scenario Management), `_151` (Stakeholder management), `_310` (PMO project portfolio SSOT), `_311` (Adviser engagement disciplines maint.), `_312` (Adviser open questions register maint.); `hol_ops_dtp_72` (INITIATIVE_REGISTRY program-anchors maint.); `gtm_services_dtp_56,57` (consolidate/classify active projects); `gtm_ops_dtp_51,89` (projects folder + pipeline forecast).

**CAP-OPS-PROJECT-ENGAGEMENT-PLANNING** ← 25 rows
`thi_opera_dtp_79` (Project charter), `_97` (List of Requirements), `_107` (Document), `_113` (List Dependencies), `_120` (Plan), `_121-124` (Objectives/Deliverables/Define-Success/Metrics), `_127-129` (Stakeholders/Budget/Scope), `_132-137` (Time/Effort/Budget estimations + Min/Par/Max), `_201` (Product Requirements Definition), `_202` (MVP Definition of Done), `_220` (Phased Delivery Plan & Critical Path); `hol_opera_dtp_103` (List Existing Use Cases); `tbd_tbd_dtp_138` (Identify Resistances); `hol_eng_prc_estimation_001` (Engagement estimation discipline); `gtm_launch_dtp_52` (dependency-link tasks).

**CAP-OPS-DELIVERY-EXECUTION-CADENCE** ← 14 rows
`hol_ops_dtp_71` (Delivery Management); `thi_opera_dtp_96` (Meeting Preparation), `_221` (Feasibility GO/NO-GO Gate), `_222` (Beta Exit Criteria), `_223` (Communication Cadence), `_250` (Benchmark UX Review & Gap Register), `_251` (IEU Prioritization Ritual); `hol_opera_dtp_152` (ROD/Scrum meeting), `_300` (Benchmark UX Review Cycle); `gtm_launch_dtp_63,64,66,69` (meetings/minutes/offline-comms/Slack-WhatsApp); `gtm_ops_dtp_96` (internal/external comm flow).

**CAP-OPS-OPERATING-MODEL-DESIGN** ← 11 rows
`gtm_cl_*` theme "Operating model and internal controls": `0d5a82fbb9f3f5` + `19506389fd2113` (intelligence-absorption processes/infra), `1bef4c65e967c5` (Corporate control), `5ab0e9ee478374`+`6f3c1ff99ebc76`+`954e95b2e53b97`+`a5b7d822950329`+`b65f69db8a3ed0`+`dd6aa7ee8e3070` (End-to-end operating model: MOs, checklist, relations, standards, increments, internal/external split); `gtm_ops_dtp_130` (end-to-end functioning), `_131` (absorb & place intelligence).

**CAP-OPS-PROCESS-PRIORITIZATION** ← 17 rows
`gtm_launch_dtp_25` (prioritize by phases); `gtm_services_dtp_58` (validate priority by ROI/demand), `_66-79` (filter internal/external by maturity, ketter/euclid/safe state, compatibility, criticality, FTE difficulty, external availability/price, ROI/cost, market demand/availability, insource-100%, critical parts, dependency-rank, time-vs-difficulty); `gtm_ops_dtp_88` (internal/external definition by uclid/ketter).

### People, Org Design & Quality Fabric

**CAP-OPS-PROCESS-CATALOG-MGMT** ← 31 rows
`tbd_tbd_dtp_73` (Flow Design), `_74` (Flow Parameter Input); `thi_opera_dtp_108` (Design Process Flow); `hol_opera_dtp_276` (SOP/Component Matrix Traceability); `hol_ops_sd_5` (SOP Documentation); `SOP-META_PROCESS_MGMT_001`; `hol_ops_pis_3` (Process Identification & Scoping), `pdm_4` (Decomposition & Modeling), `pdiu_6` (Data Ingestion & Update); `gtm_cl_6666fcd6962238` (roles+process map); `gtm_launch_dtp_42` (MO to fill tables); `gtm_services_dtp_1,4,6,7,9,10,13,14,16,23,29,65` (review updates, org-chart/process-map, SOP standard, role/owner assignment, process descriptions, updated process list); `gtm_ops_dtp_5,6,7,8` (flows/architecture review+ownership+sprint), `_49` (processes folder), `_71,72` (update process list + RACI), `_104` (capture processes into list).

**CAP-OPS-WORKFORCE-CAPACITY-PLANNING** ← 19 rows
`gtm_cl_*` theme "FTE optimization": `0613df8d0ca2a3`,`0fd8cede0f6712`,`16f46540b1f140`,`a5825f358b0d65`; `gtm_launch_dtp_56-62` (FTE scenarios, agile work model, task prioritization, quarterly/annual plan, monthly hours, transport/equipment, work-days), `_65` (split time tasks/meetings), `_67,68` (Trello task design + Monday handoff), `_70,71,72` (dev/strategy split, weekly time by category, verticality categorization), `_75` (Optimizar FTEs); `gtm_services_dtp_22` (FTE matrix/formulas).

**CAP-OPS-OPERATIONAL-GOVERNANCE** ← 3 rows
`hol_opera_dtp_153` (Regression Process Execution); `gtm_pm_st_promo` (PMO vault promotion gate); `ops_pmo_dtp_cohesion_quarterly_001` (Operational cohesion quarterly review).

### Data Governance & Enterprise Knowledge

**CAP-OPS-KNOWLEDGE-MGMT-SYSTEM** ← 48 rows
`gtm_launch_dtp_53` (strategy folders/annexes); `gtm_services_dtp_2,3,5,8,17,18,28` (frameworks library, RFI, role-standard docs in KMS, list-in-KMS, tech docs, unify product docs, grant access); `gtm_ops_dtp_23-30` (KMS by org-chart, role-standard files, Admin folders, handoff to managers, role split, admin-resource links, Drive replication, unify under admin), `_52,53,54` (excalidraw/youtube/obsidian folders), `_57,58` (MO format standard, MO repository), `_78-86` (KMS organization, output design admin+role-personalized, folder/title discipline, standard vs personal docs, top-down, info filter, output-1 Excali design), `_90-95` (KMS org-chart, gather/clean/split/update admin docs, integrate updates), `_101,102,103` (research folder, unify research docs, list resources), `_106-114` (use-case guide MO, review periodicity, doc list, Drive integration, grant access, KMS repo/folders, output standards by platform+design).

### Product & Platform Engineering

**CAP-OPS-ERP-DATA-PLATFORM-BUILD** ← 54 rows
`gtm_cl_2083e7d57f31fe` (data-input interface), `b2d4d6d135d20a` (database), `b857ba02148488` (define tables); `gtm_launch_dtp_17-23` (close tables/columns/relations, Supabase, transactionals, SQL-to-flows, ERP connect), `_27` (categorized transactionals), `_34,35` (BBDD integration, payment methods config), `_37-40` (DB structure, columns/types, relations, Stripe/external tables), `_43-45` (daily-ops Excel, ERP forms, SQL load), `_47-51` (table relations, snowflake graph, SQL-relation MO, table/area/column listing, ERP form compatibility); `gtm_ops_dtp_11-22` (missing columns, financial-data flow, ERP interface/forms, Supabase tables, excel→supabase, foreign keys, transactional relations, SQL formulas, ERP integrate, testing, Stripe, table checklist), `_34-40` (external connections, financial/operational/product/legal tables, ERP data flow, extra functionality), `_42,43,44` (columns/types, table relations, transactionals P&L), `_50` (tables folder), `_122,123,125,126,128` (web apps/tables, devops MO, global vs process apps, ERP dev components, SQL load functions), `_129` (document infrastructure).

**CAP-OPS-COMPONENT-PORTFOLIO-MGMT** ← 44 rows
`gtm_cl_*` "Capability and resource inventory" + component infra: `06826551486d0a`,`3f6681940aeaab`,`434e6039e8ec68`,`45fd062aaaff6c`,`d0783fd7db9d8b`,`a813182e3a5c08` (component table),`c54318a2387815` (component workflow); `gtm_launch_dtp_29` (choose provider); `gtm_services_dtp_11,12` (review components, assign by area), `_61` (contact components), `_80` (categorize capability/resource inventory); `gtm_ops_dtp_1,2,3,4` (read matrix, github readmes, process/financial tables→components), `_9,10` (component+process tables, sheets), `_32` (choose provider 2), `_45-48` (reporting component, readmes, central resource list, components folder), `_55,56` (updated component table, readmes as guide), `_59-68` (tool tasks/permissions, criticality valuation, process list per component, responsible/support roles, visual flow, research actions, official docs, price/feature tiers, strategy-relevant functions, min-par-max thresholds), `_70` (future component uses), `_73-77` (cross-area inclusion, substitutions, market research, role perspectives, research annex), `_87` (the Admin matrix), `_105` (list components used), `_127` (component/form-design research).

### Go-to-Market & Brand

**CAP-OPS-SERVICE-CATALOG-PRODUCTIZATION** ← 28 rows
`gtm_cl_8d605e43ef1def` (GTM readiness), `5fb394c413062c`+`7506f05fe1f005`+`7c2f86a8c5a925`+`a57ff65e6109ec` (service-process documentation), `903c27de18165e` (Service definition); `gtm_launch_dtp_33` (integrate service comms), `_46` (logistics/prices/products flow); `gtm_services_dtp_15` (active products by area), `_19,20,21` (marketing/comm plan, integrate Marketing+Service Managers, PO product-design frameworks), `_24,25,26` (labor hourly price, profit ratio, FTE value by role), `_39,41,45` (volume offer models, apply to products, product timelines), `_59,60,62,63,64` (marketing funnel start, service comm plan, pitch, phased proposal SOP, project-service development), `_82` (define/document service processes); `gtm_ops_dtp_97-100` (client-collaboration MO, web copies, methodology-licensing plan + forecast).

**CAP-OPS-INBOUND-LEAD-ROUTING** ← 2 rows
`thi_opera_dtp_288` (LEADS WEB Centralization & BD Routing); `holistika_reach_dtp_003` (Inbound Response SLA — Holistika Services).

### Finance & Revenue Operations

**CAP-OPS-REVENUE-OPERATIONS** ← 7 rows
`tbi_ops_dtp_revops_qbr_001` (Quarterly Business Review), `_engagement_scaffold_001` (engagement RPA scaffolder), `_revenue_rollup_001` (weekly revenue rollup), `_persona_audit_001` (persona registry audit), `_crm_sync_001` (daily CRM adapter sync), `_regulator_checkpoint_001` (quarterly regulator-relationship checkpoint), `_media_review_001` (event-triggered media counterparty review).

**CAP-OPS-FINANCIAL-PLANNING-CONTROL** ← 16 rows
`gtm_cl_*` "Financial control": `24393c17d06385`,`29a5f6a52b15f9`,`7a454ec5fb7e4e`,`afb64082295a96`,`ff27eaf1eed5ee`,`d40d6f2d47d60b` (P2P/O2C docs, financial tables, forecast integration, cost/revenue categorization, relational/transactional, payment portal); `gtm_launch_dtp_16` (cost split), `_24` (cost/scenario table w/ components), `_26` (include in financial tables), `_28` (cost categories), `_41` (close P&L transactionals), `_54,55` (cost increases in outputs, cost dimensions), `_74` (Control financiero); `gtm_ops_dtp_33` (system costs in forecast), `_69` (include in forecast).

### Corporate Intelligence & Research

**CAP-OPS-MARKET-INTEL-RESEARCH** ← 28 rows
`gtm_cl_*` "Market demand" + research methodology: `3a38f6c7014d3e`,`3e8b5ab573de92`,`90684555501bb8`,`f8d245a7b6d763`,`ac5a89216d4ce8` (intel methodology),`b0db4bd3e78efd` (research frameworks); `gtm_services_dtp_27` (research frameworks), `_30,31,32` (alert channels/setup/periodicity), `_36,37,40` (intel→strategy, PM-as-service research, sector specializations), `_42-44` (buyers/PESTLE/competitors, filter by product/industry/size, regions), `_46` (market authority markers), `_48-55` (optimize existing products, buyer filter, competitor marketing, service times, prices/reviews, web funnels, comm channels, FAQs/web portals), `_81` (know market demand); `gtm_ops_dtp_115` (research process MO), `_116` (intelligence matrix included).

### Applied AI & MADEIRA

**CAP-OPS-AGENTIC-USECASE-CATALOG** ← 12 rows
`gtm_cl_cd667d728c75e0` (AI use cases); `gtm_services_dtp_33,34,35` (research/intel/update agents), `_38` (researcher scrapping), `_47` (include AI); `gtm_ops_dtp_31` (assistant + researcher/scrapper), `_117-121` (AI channel-guide MOs, AI help use-cases per channel, AI research use-cases per area, intel flow from AI delivery, agent matrix).

### Legal, Compliance & Privacy

**CAP-OPS-ENTITY-FORMATION-SETUP** ← 25 rows
`gtm_cl_*` "Entity formation": `3bd799aec13210`,`45a278c3a4778b`,`553039c22e9a68`,`7a8ab255ca7c48`,`d549cdb10a2410`,`da182afd130aeb` (social direction, autónomos budget, social split+contracts, bank account, devices as social capital, gestoría/notaría); `gtm_launch_dtp_1-15` (device capital, social capital, individual options, priority-area categorization, premises x2, bank offers, gestoría inclusion, equity %, contributed capital, NDAs, employment/supplier/client contracts, partner monthly fee), `_30,31,32` (create company account, integrate gestoría/bank, supplier contracts via gestoría), `_73` (Establecer sociedad).

---

## 3. Evict — code-symbols / non-capabilities (9 rows)

Per the eviction rule (l2 findings §3.2 step 1 + [E-19] "naming capabilities after systems
defeats the purpose"). Two sub-classes:

### 3a. → `COMPONENT_PRIMITIVE_REGISTRY.csv` (code / script / API symbols, 4 rows)

These name a *technical artifact or action*, not an ability. They land as primitives with a
new `kind` outside the current visual/prose/interactive set (proposed `kind: technical` /
`script` / `api`), `status: charter`, `parent_artifact_class_codes` pointing at the ERP/MADEIRA
platform.

| capability_id | name | why evict | proposed primitive kind |
|:---|:---|:---|:---|
| CAP-HOL-OPS-ECS-8 | Execute Cypher Update Script | a runnable script, not an ability | `script` |
| CAP-HOL-OPS-UPL-7 | Update process_list_1.csv | a file-mutation action naming a specific artifact | `script` |
| CAP-GTM-OPS-DTP-41 | MADEIRA API surface item | an API surface symbol (mirrors the l2 API-symbol eviction) | `api` |
| CAP-GTM-OPS-DTP-124 | Auth | a technical/component primitive, not a business ability | `technical` |

### 3b. → delete / park as non-capability (NOT components, 5 rows)

Neither capabilities nor components — workflow-state enum values, an explicit TBD placeholder,
and a board-link artifact. Recommend **delete** from the capability layer (optionally a tiny
`status-enum` primitive for the Kanban trio if a board model is ever formalized). They are NOT
process realizations either (a Kanban column is not a process).

| capability_id | name | why not a capability |
|:---|:---|:---|
| CAP-HOL-OPERA-DTP-163 | To do | Kanban workflow-state enum value |
| CAP-HOL-OPERA-DTP-164 | In process | Kanban workflow-state enum value |
| CAP-HOL-OPERA-DTP-165 | Done | Kanban workflow-state enum value |
| CAP-TBD-TBD-DTP-130 | Exploit (TBD) | explicit `tbd_tbd_*` placeholder; no definable ability |
| CAP-GTM-LAUNCH-DTP-36 | (Link a tarjeta Documentar infraestructura…) | a Trello card cross-link, not an ability |

---

## 4. Cross-area flags

L1 domains are *abilities*, not org units — so many Operations-filed rows realize abilities
that **belong to another area's capability**. The APQC PCF confirms this shape: PMO / program /
project management is mapped *across* categories rather than confined to one, and PCF splits
operating (1–6) from management/support (7–13) services [APQC PCF v7.4, §Overview]. The default
recommendation is **keep the capability bearer-agnostic and let the other area own the canonical
row; Operations is a *realizer* (a process owner), not the capability owner.**

| proposed_capability_id | belongs to / merges with (L1 + area) | recommendation |
|:---|:---|:---|
| CAP-OPS-ENTITY-FORMATION-SETUP | Legal, Compliance & Privacy | **Merge** into a Legal "Legal Instrument & Entity Management" capability (l2 cluster #8); Operations/PMO is the realizing process owner during stand-up only. |
| CAP-OPS-FINANCIAL-PLANNING-CONTROL | Finance & Revenue Operations | **Merge** into a Finance "Financial Planning & Control / FINOPS" capability; aligns with the FINOPS register lineage. |
| CAP-OPS-MARKET-INTEL-RESEARCH | Corporate Intelligence & Research | **Merge** into the Research "Counterparty Intelligence & Source-Grading / Market Intelligence" capability (l2 cluster #11). Dual-register: internal CORPINT name ↔ external "market research". |
| CAP-OPS-AGENTIC-USECASE-CATALOG | Applied AI & MADEIRA | **Merge** into a MADEIRA "AI Use-case & Agent Portfolio" capability; Operations catalogs use-cases, MADEIRA area owns the ability. |
| CAP-OPS-ERP-DATA-PLATFORM-BUILD | Product & Platform Engineering | **Co-own / shift to Tech.** The platform-build ability is Tech Lab's; Operations is the requirements + data-model realizer. |
| CAP-OPS-COMPONENT-PORTFOLIO-MGMT | Product & Platform Engineering (+ Tech component/service matrix) | **Co-own.** The component/service matrix is a shared Holistika signature; Operations maintains the portfolio view, Tech owns the technical registry. |
| CAP-OPS-KNOWLEDGE-MGMT-SYSTEM | Data Governance & Enterprise Knowledge | **Split per People-DoD rule:** KMS *infrastructure* (Obsidian/Drive/GitHub) → Tech; *persona-routing/accessibility* → People; Operations realizes the doc-org processes. |
| CAP-OPS-SERVICE-CATALOG-PRODUCTIZATION | Go-to-Market & Brand (+ Product) | **Co-own with GTM/Product.** Rows `gtm_services_dtp_19,20` + `gtm_ops_dtp_98` (marketing/comm plan, web copies) are Marketing — flag those realizations to GTM/Brand. |
| CAP-OPS-INBOUND-LEAD-ROUTING | Go-to-Market & Brand / RevOps | **Shift to GTM/RevOps** (demand-gen + BD routing); Operations holds the SLA execution only. |
| CAP-OPS-PROCESS-CATALOG-MGMT | People, Org Design & Quality Fabric | **Pattern owned by People** (process-design patterns per People-DoD rule); Operations/PMO authors and runs the catalog. Keep in Operations as executor, cite People as pattern owner. |
| CAP-OPS-OPERATIONAL-GOVERNANCE | People, Org Design & Quality Fabric | Regression execution + cohesion review are Quality-Fabric abilities; **cite People** as doctrine owner, Operations executes. |
| CAP-OPS-REVENUE-OPERATIONS (partial) | Go-to-Market & Brand (persona/media) + Legal/Compliance (regulator) | Three RevOps realizations are cross-area: `_persona_audit_001` (CMO) + `_media_review_001` (Brand & Narrative Mgr) → **Brand**; `_regulator_checkpoint_001` (Compliance) → **Legal/Compliance**. The RevOps *orchestration* ability stays in Finance & Revenue Ops. |

**Net:** 8 of the 18 proposed capabilities (entity, financial, market-intel, agentic, ERP,
KMS, inbound, service-catalog) are candidates to **merge into another area's canonical row** at
the cross-area de-dup pass (l2 findings §2 rec 3) — confirming the operator's intuition that
"Operations = 404" is inflated partly by *other areas' work filed under the PMO build-out
backlog*. The truly Operations-native abilities are ~7–10 (program/portfolio, project &
engagement planning, delivery cadence, operating-model design, process catalog, workforce
capacity, operational governance, process prioritization).

---

## 5. Count summary

| Disposition | Count |
|:---|---:|
| Old Operations rows (input) | **404** |
| → rolled up into proposed stable capabilities | 395 |
| → evicted (§3a components + §3b non-capabilities) | 9 |
| **Proposed stable capabilities (output)** | **18** |
| of which truly Operations-native | ~7–10 |
| of which cross-area merge candidates (§4) | 8 |
| differentiating tier | 9 |
| utility tier | 9 |

**Reconciliation (rolled-up, by capability):** 11 + 25 + 14 + 11 + 31 + 19 + 3 + 48 + 54 + 44 +
28 + 2 + 7 + 16 + 28 + 12 + 25 + 17 = **395**. Plus **9** evicted = **404**. ✓ Every old row is
accounted for.

**Organic count rationale.** 18 is above the per-area share of the ~60–110 global target, but
honest for this slice: Operations is the PMO build-out backlog, so it carries cross-area work
(8 of 18) that will *net out* at the cross-area de-dup pass — after merging those into Finance /
Legal / Research / AI / Tech / GTM canonical rows, Operations contributes only ~7–10 *net-new*
capabilities to the global map. The 337-row `gtm_*` backlog is the single largest source of
inflation (task-grain Trello cards), exactly the seed-clone pattern APQC/ServiceNow describe
("PCF gets you ~80% of the way, then you tweak" [ServiceNow Community]). The collapse ratio for
Operations is **404 → 18 (~22×)**.

## Research grounding (per akos-applied-research-discipline)

- **Internal:** method authority = l2 findings §3.2/§3.3 (the ratified D-IH-95-H collapse method,
  6 steps + ~9 L1 domains + eviction rule); seed structure = l2 findings §0; eviction target
  columns = `COMPONENT_PRIMITIVE_REGISTRY.csv` header (read).
- **External (1 source, refinement not novel framing):** APQC Process Classification Framework
  (Cross-Industry v7.4) — 13 L1 categories split operating (1–6) vs management/support (7–13);
  PMO/program/project management is cross-cutting; category 13.0 = "Develop and Manage Business
  Capabilities". Confirms (a) scatter-Operations-across-L1-domains, (b) cross-area flagging, and
  (c) the seed-clone inflation pattern. https://www.apqc.org/process-frameworks

## Cross-references

- Parent method (authoritative): [`l2-capability-densify-findings-2026-06-07.md`](../l2-capability-densify-findings-2026-06-07.md).
- Source registry: `dimensions/CAPABILITY_REGISTRY.csv` (area=='Operations', 404 rows).
- Eviction target: `dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv`.
- Sibling area collapse maps: `l2-collapse-maps/<area>-collapse-map.md` (one per area).
- Gate: the one-time collapse rewriting `CAPABILITY_REGISTRY` is a **canonical-CSV gate**
  (operator approval, per-domain slices) per `akos-baseline-governance.mdc` + l2 findings §4.4/§5.
- Decision: D-IH-95-H (keep-separate + de-densify, area-by-area, organic count).

