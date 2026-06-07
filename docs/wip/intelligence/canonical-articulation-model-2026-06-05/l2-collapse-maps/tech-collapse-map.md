---
intellectual_kind: capability_collapse_map
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L2 — Capability de-densify (R2-01) — area slice
area: Tech
authored: 2026-06-08
status: proposed
ratified_decision: D-IH-95-H   # parent: keep-separate + de-densify, area-by-area
control_confidence_level: Euclid   # proposal pending operator/AIC ratification + canonical-CSV gate
language: en
audience: J-OP;J-AIC
register: internal
related_decisions:
  - D-IH-95-H   # de-densify CAPABILITY_REGISTRY into a stable map (the method this applies)
  - D-IH-95-G   # R2-01 ratified keep-separate
  - D-IH-82-P   # the 1:1 process-shadow seed this collapses
method_source: docs/wip/intelligence/canonical-articulation-model-2026-06-05/l2-capability-densify-findings-2026-06-07.md
note: >
  Tech-area slice of the de-densify collapse. Applies the ratified 6-step method
  (§3.2 of the method doc) to the 379 Tech rows of CAPABILITY_REGISTRY.csv. Readonly
  research + one doc write; no canonical CSV is modified here. The actual rewrite of
  CAPABILITY_REGISTRY is a gated canonical-CSV change (operator approval, per-domain
  slices) — this doc is the reviewable proposal for that gate.
---

# L2 collapse map — **Tech** area (379 → 27 stable capabilities, +27 evicted)

> **Headline:** The 379 Tech rows are a 1:1 process-shadow seeded off `process_list`
> (D-IH-82-P). The overwhelming majority are **MADEIRA / KiRBe product-backlog rows** —
> feature-claims, framework component names, deployment targets, and research-radar
> *topics* — not stable abilities. They collapse to **27 stable, bearer-agnostic
> capabilities** across 5 L1 domains, with **27 MADEIRA code-symbol rows evicted** to
> `COMPONENT_PRIMITIVE_REGISTRY` (the exact `gtm_madeira_dtp_191..217` block the method
> doc named as cluster #3). **Five** of the 27 capabilities are **cross-area** (their stable
> home is Research / Data / GTM / Legal / Delivery) — flagged in §4 but fully accounted
> here so no Tech row is orphaned.

Applies the ratified method in
[`l2-capability-densify-findings-2026-06-07.md`](../l2-capability-densify-findings-2026-06-07.md)
§3.2 (strip non-capabilities → normalize to (area, theme) → merge across entity/convention →
name as nouns/gerunds technology-neutral → assign L1 domain → wire, don't copy). Worked
clusters #1 (API Lifecycle & Portfolio Governance) and #3 (Conversational AI Delivery Engine)
from the method doc are Tech and are reproduced faithfully below.

---

## 1. Proposed stable capabilities (the de-densified Tech map)

27 capabilities. `proposed_capability_id` matches `^CAP-[A-Z0-9-]+$`. Names are nouns/gerunds,
outcome-oriented, technology-neutral (no system names in the capability name itself, per E-19).
`tier`: **D** = differentiating · **U** = utility.

| # | proposed_capability_id | capability_name | L1_domain | tier | definition |
|:--|:--|:--|:--|:--|:--|
| 1 | `CAP-CONVERSATIONAL-AI-ENGINE` | Conversational AI Delivery Engine | Applied AI & MADEIRA | D | The ability to serve grounded, multilingual, multimodal (text/voice) conversational answers with reasoning, memory, streaming, and structured output. |
| 2 | `CAP-AI-PERSONA-PERSONALITY` | AI Persona & Personality Configuration | Applied AI & MADEIRA | D | The ability to give an AI collaborator a configurable, sentiment-aware persona — traits, emotional state, interaction style, backstory, avatar — and self-awareness of org + user. |
| 3 | `CAP-KNOWLEDGE-RETRIEVAL-RAG` | Knowledge Retrieval & RAG Platform | Applied AI & MADEIRA | D | The ability to ingest any source, index it (vector + graph), and retrieve/rerank relevant knowledge for grounding — the KiRBe archivist platform. |
| 4 | `CAP-KNOWLEDGE-VAULT-GOVERNANCE` | Knowledge Vault Governance, Security & Metering | Applied AI & MADEIRA | U | The ability to govern multi-tenant knowledge vaults — RBAC/membership, usage metering/quotas, audit logging, auth/RLS test gating. |
| 5 | `CAP-AI-EVALUATION-BENCHMARKING` | AI Evaluation, Benchmarking & Compliance Scoring | Applied AI & MADEIRA | D | The ability to evaluate AI outputs for quality, ethics, and code-of-conduct compliance via automated + agentic evaluators. |
| 6 | `CAP-AI-AGENT-ORCHESTRATION` | Multi-Agent Orchestration & Tooling | Applied AI & MADEIRA | D | The ability to compose and run a roster of cooperating AI agents (research, swarm-edit, code, ReAct) with tool/API access. |
| 7 | `CAP-MADEIRA-SCENARIO-LIFECYCLE` | AI Verdict, Scenario & Telemetry Lifecycle | Applied AI & MADEIRA | D | The ability to run the operational governance loop for a deployed AI — verdict review, dossier emit, incident response, scenario promote/quarantine/deprecate, telemetry feedback, UX review. (Method cluster #2.) |
| 8 | `CAP-AI-SCENARIO-RESEARCH-RADAR` | AI Scenario Research Radar | Applied AI & MADEIRA | U | The ability to curate the macro/geo/tech/AI scenario corpus that feeds MADEIRA's reasoning. **Cross-area: Research** (see §4). |
| 9 | `CAP-API-LIFECYCLE-GOVERNANCE` | API Lifecycle & Portfolio Governance | Product & Platform Engineering | D | The ability to register, specify (SSOT), catalog, version, and attribute the full internal + third-party API portfolio. (Method cluster #1.) |
| 10 | `CAP-WEB-APP-EXPERIENCE-ENG` | Web & Application Experience Engineering | Product & Platform Engineering | U | The ability to build accessible web/app UI — components, UI logic, forms, user management, in-codebase SEO, storefront surfaces. |
| 11 | `CAP-MULTIPLATFORM-DEPLOYMENT` | Multi-Platform Deployment & Packaging | Product & Platform Engineering | U | The ability to package and deploy the product across cloud, web, desktop, mobile-native, and edge/VR targets. |
| 12 | `CAP-CICD-RELEASE-ENG` | CI/CD & Release Engineering | Product & Platform Engineering | D | The ability to test, gate, merge, and ship code through automated pipelines across local + cloud CI/CD. |
| 13 | `CAP-CODEBASE-CATALOG-STANDARDS` | Codebase Catalog, Standards & Developer Onboarding | Product & Platform Engineering | U | The ability to maintain an IT/codebase catalog with access unification, SDK/package standards, continuous improvement, and developer onboarding. |
| 14 | `CAP-CROSS-REPO-GOVERNANCE` | Cross-Repo Governance & Schema Propagation | Product & Platform Engineering | D | The ability to bless external repos, remediate drift, and propagate schema/contract changes across the multi-repo fleet. |
| 15 | `CAP-AGENTIC-INFRA-OPS` | Agentic Infrastructure Operations & Runtime Health | Product & Platform Engineering | D | The ability to operate the agentic runtime — infra ops, runtime-health triage, agentic + substrate landscape maintenance. |
| 16 | `CAP-TECHOPS-RELIABILITY-OBSERVABILITY` | TechOps Reliability & Observability | Product & Platform Engineering | D | The ability to keep deployed systems reliable — observability/logs/KPIs, deploy cadence, defect remediation, render-gate + app-governance sweeps. |
| 17 | `CAP-APPLICATION-SECURITY` | Application Security & Secrets Management | Product & Platform Engineering | U | The ability to secure the codebase and manage secrets/tokens via a vault pattern. |
| 18 | `CAP-DATABASE-GRAPH-MGMT` | Database & Graph Store Management | Product & Platform Engineering | U | The ability to provision and operate relational + graph (Neo4j) data stores, including cost/clustering posture. |
| 19 | `CAP-DOMAIN-DNS-MGMT` | Domain & DNS Management | Product & Platform Engineering | U | The ability to manage domains, nameservers, sub-domains, and web-traffic analytics. (Method cluster #7.) |
| 20 | `CAP-ECOMMERCE-PLATFORM-INTEGRATION` | E-commerce & Storefront Platform Integration | Product & Platform Engineering | D | The ability to integrate and ship commerce surfaces — Shopify app/theme/billing, plugins, storefront performance budgets. |
| 21 | `CAP-THIRD-PARTY-INTEGRATION-MGMT` | Third-Party Integration Management | Product & Platform Engineering | U | The ability to manage outbound integrations to third-party platforms (FB/Google/Sentry/Pinecone, PMS + comms tools). |
| 22 | `CAP-ENVOY-TECHLAB-SHOWCASE` | Tech Lab Studio & Showcase Engineering | Product & Platform Engineering | U | The ability to build and maintain the Envoy Tech Lab demo/showcase surfaces (AI Studio, MADEIRA/KiRBe/ERP showcases, lab architecture). |
| 23 | `CAP-MARKETING-PRODUCT-DATA-PLATFORM` | Marketing, Ads & Product Analytics Data Platform | Data Governance & Enterprise Knowledge | U | The ability to govern audience/event/campaign data + ad-platform integrations + analytics pipelines. **Cross-area: Data/Marketing** (see §4). |
| 24 | `CAP-DATAOPS-QUALITY-ASSURANCE` | DataOps Quality Assurance | Data Governance & Enterprise Knowledge | D | The ability to enforce the canonical-CSV + mirror data-quality bar (7-dimension DataOps check). |
| 25 | `CAP-AI-PRODUCT-GTM-LAUNCH` | AI Product GTM & Launch Management | Go-to-Market & Brand | D | The ability to take an AI product from market-requirements → business case → positioning/pricing → alpha/beta/GA release. **Cross-area: GTM/Product** (see §4). |
| 26 | `CAP-DOC-REDACTION-PRIVACY-TOOLING` | Document Redaction & Privacy Tooling | Legal, Compliance & Privacy | U | The ability to enforce data-retention, NDA, and dynamic document-redaction controls in the product. **Cross-area: Legal** (see §4). |
| 27 | `CAP-CLIENT-AI-DATAOPS-DELIVERY` | Client AI & DataOps Engagement Delivery | Delivery & Client Engagement Operations | D | The ability to deliver bespoke client AI/DataOps modules (the SUEZ POC family: extraction, mapping, dispute register, dashboards). **Cross-area: Delivery** (see §4). |

**L1 domains used (5 of the method's ~9):** Applied AI & MADEIRA (8) · Product & Platform Engineering (14) · Data Governance & Enterprise Knowledge (2) · Go-to-Market & Brand (1) · Legal, Compliance & Privacy (1) · Delivery & Client Engagement Operations (1). Tier split: **13 differentiating / 14 utility.**

---

## 2. Rollup — every old Tech row → its new stable capability

The `originating_process_ids` column is what TRP-006 (`process —realization→ capability`) wires
on the de-densified row (N:N — many processes realize one capability). Ranges use the method
doc's compact `a..b` notation. **352 rows roll up here; the remaining 27 are evicted (§3); 352 + 27 = 379.**

| proposed_capability_id | rolls up old `capability_id`(s) | `originating_process_ids` (rolled, N:N) | n |
|:--|:--|:--|--:|
| `CAP-CONVERSATIONAL-AI-ENGINE` | `CAP-ENV-TECH-DTP-263`; `CAP-GTM-MADEIRA-DTP-{52,53,59,60,61..73,97,101,129}`; `CAP-GTM-CL-{1b74aa11c26612,2a86fe54beeb84,1ce9390550d234,68f2ea7ca41cdd,8835a727fafc8c,aeb937a98e9d97,f0cd4525cd4646}`; `CAP-SOP-GEMINI-FASTAPI-SERVICE-001`; (+folded code-adjacent `…DTP-180,183`) | `env_tech_dtp_263`; `gtm_madeira_dtp_{52,53,59,60,61..73,97,101,129,180,183}`; `gtm_cl_{1b74aa11c26612,2a86fe54beeb84,1ce9390550d234,68f2ea7ca41cdd,8835a727fafc8c,aeb937a98e9d97,f0cd4525cd4646}`; `SOP-GEMINI_FASTAPI_SERVICE_001` | 31 |
| `CAP-AI-PERSONA-PERSONALITY` | `CAP-ENV-TECH-DTP-265`; `CAP-GTM-MADEIRA-DTP-{89,90,92,93,94,95,96,98}`; `CAP-GTM-CL-{3b697c1febacb8,71a6fb2dbce712,a43b42abaf8e3c,ffc7e886b6a4f3,a2f9b65f49a925}` | `env_tech_dtp_265`; `gtm_madeira_dtp_{89,90,92,93,94,95,96,98}`; `gtm_cl_{3b697c1febacb8,71a6fb2dbce712,a43b42abaf8e3c,ffc7e886b6a4f3,a2f9b65f49a925}` | 14 |
| `CAP-KNOWLEDGE-RETRIEVAL-RAG` | `CAP-ENV-TECH-DTP-{256,258,268,269}`; `CAP-SOP-KIRBE-{TEXTSPLITTER-SENTENCE-001,NODEPARSER-SEMANTIC-001,NODE-MANAGEMENT-001,NODEPOSTPROCESSOR-CUSTOMFILTER-001,NODEPOSTPROCESSOR-ENTITY-001,NODEPOSTPROCESSOR-RERANK-001,NODEPOSTPROCESSOR-KEYWORD-001,LLM-MANAGEMENT-001,ANALYTICS-READINESS}`; `CAP-GTM-MADEIRA-DTP-{54,58,102,108..128,130..139,159..175,178,179,182,184..190}`; `CAP-GTM-CL-{89f1c8c3b32bba,4b160680e2afaf,bd109f630f4e77,95ccfca55c3ef6}` | `env_tech_dtp_{256,258,268,269}`; `SOP-KIRBE_{TEXTSPLITTER_SENTENCE_001,NODEPARSER_SEMANTIC_001,NODE_MANAGEMENT_001,NODEPOSTPROCESSOR_CUSTOMFILTER_001,NODEPOSTPROCESSOR_ENTITY_001,NODEPOSTPROCESSOR_RERANK_001,NODEPOSTPROCESSOR_KEYWORD_001,LLM_MANAGEMENT_001,ANALYTICS_READINESS}`; `gtm_madeira_dtp_{54,58,102,108..128,130..139,159..175,178,179,182,184..190}`; `gtm_cl_{89f1c8c3b32bba,4b160680e2afaf,bd109f630f4e77,95ccfca55c3ef6}` | 78 |
| `CAP-KNOWLEDGE-VAULT-GOVERNANCE` | `CAP-ENV-TECH-DTP-{80,257,259,260,278,279}` | `env_tech_dtp_{80,257,259,260,278,279}` | 6 |
| `CAP-AI-EVALUATION-BENCHMARKING` | `CAP-GTM-MADEIRA-DTP-{57,91,99,105,140,141,142,143,144,224}`; `CAP-GTM-CL-1b6d2fb3b4bcde` | `gtm_madeira_dtp_{57,91,99,105,140,141,142,143,144,224}`; `gtm_cl_1b6d2fb3b4bcde` | 11 |
| `CAP-AI-AGENT-ORCHESTRATION` | `CAP-ENV-TECH-DTP-264`; `CAP-GTM-MADEIRA-DTP-{51,55,56,100,103,104,106,107,176,177,181}`; `CAP-SOP-FLOWMAKER-MADEIRA-ARCHITECTURE-001`; `CAP-GTM-CL-09a94b87396e7b` | `env_tech_dtp_264`; `gtm_madeira_dtp_{51,55,56,100,103,104,106,107,176,177,181}`; `SOP-FLOWMAKER_MADEIRA_ARCHITECTURE_001`; `gtm_cl_09a94b87396e7b` | 14 |
| `CAP-MADEIRA-SCENARIO-LIFECYCLE` | `CAP-ENV-TECH-DTP-MADEIRA-{VERDICT,DOSSIER,INCIDENT,LIFECYCLE,TELEMETRY,UXREVIEW}` | `env_tech_dtp_madeira_{verdict,dossier,incident,lifecycle,telemetry,uxreview}` | 6 |
| `CAP-AI-SCENARIO-RESEARCH-RADAR` | `CAP-GTM-MADEIRA-DTP-{1..28,45,218}`; `CAP-GTM-CL-{4106a1d37422d3,699cc4cd6e207d,814367ea727b74,9d17a1ce9894c5,9eb55dbcbe2b59,cf58a1460f29ea}` | `gtm_madeira_dtp_{1..28,45,218}`; `gtm_cl_{4106a1d37422d3,699cc4cd6e207d,814367ea727b74,9d17a1ce9894c5,9eb55dbcbe2b59,cf58a1460f29ea}` | 36 |
| `CAP-API-LIFECYCLE-GOVERNANCE` | `CAP-ENV-TECH-DTP-{306,307,308,309,311,312,313,266,293}`; `CAP-SOP-MCP-SERVER-DEFINITION`; `CAP-GTM-MADEIRA-DTP-44` | `env_tech_dtp_{306,307,308,309,311,312,313,266,293}`; `SOP-MCP_SERVER_DEFINITION`; `gtm_madeira_dtp_44` | 11 |
| `CAP-WEB-APP-EXPERIENCE-ENG` | `CAP-ENV-TECH-DTP-{8,16,53,81..93}`; `CAP-THI-TECH-DTP-52` | `env_tech_dtp_{8,16,53,81..93}`; `thi_tech_dtp_52` | 17 |
| `CAP-MULTIPLATFORM-DEPLOYMENT` | `CAP-GTM-MADEIRA-DTP-{74..88}` | `gtm_madeira_dtp_{74..88}` | 15 |
| `CAP-CICD-RELEASE-ENG` | `CAP-ENV-TECH-DTP-{70,75,295,299}`; `CAP-GTM-MADEIRA-DTP-{50,145..149,151,152,153,157,225,226,227}`; `CAP-GTM-CL-{028e05b3126789,0370bec6e882ca}` | `env_tech_dtp_{70,75,295,299}`; `gtm_madeira_dtp_{50,145..149,151,152,153,157,225,226,227}`; `gtm_cl_{028e05b3126789,0370bec6e882ca}` | 19 |
| `CAP-CODEBASE-CATALOG-STANDARDS` | `CAP-ENV-TECH-DTP-{12,155,156,285,292}`; `CAP-GTM-MADEIRA-DTP-150` | `env_tech_dtp_{12,155,156,285,292}`; `gtm_madeira_dtp_150` | 6 |
| `CAP-CROSS-REPO-GOVERNANCE` | `CAP-SOP-EXTERNAL-REPO-BLESSING-001`; `CAP-SOP-EXTERNAL-REPO-DRIFT-REMEDIATION-001`; `CAP-SOP-CROSS-REPO-SCHEMA-PROPAGATION-001` | `SOP-EXTERNAL_REPO_BLESSING_001`; `SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001`; `SOP-CROSS_REPO_SCHEMA_PROPAGATION_001` | 3 |
| `CAP-AGENTIC-INFRA-OPS` | `CAP-ENV-TECH-DTP-AGENTIC-LANDSCAPE-MTNCE-001`; `CAP-ENV-TECH-DTP-AGENTIC-INFRA-OPS-001`; `CAP-ENV-TECH-DTP-OPENCLAW-RUNTIME-HEALTH-TRIAGE-001`; `CAP-ENV-TECH-DTP-SUBSTRATE-LANDSCAPE-MTNCE-001` | `env_tech_dtp_agentic_landscape_mtnce_001`; `env_tech_dtp_agentic_infra_ops_001`; `env_tech_dtp_openclaw_runtime_health_triage_001`; `env_tech_dtp_substrate_landscape_mtnce_001` | 4 |
| `CAP-TECHOPS-RELIABILITY-OBSERVABILITY` | `CAP-ENV-TECH-DTP-{253,techops-reliability-001,app-governance-quarterly-001,external-render-gate-promotion-001}`; `CAP-SOP-KIRBE-TRACEABILITY-OBSERVABILITY-001`; `CAP-GTM-MADEIRA-DTP-{154,155}` | `env_tech_dtp_253`; `env_tech_dtp_techops_reliability_001`; `env_tech_dtp_app_governance_quarterly_001`; `env_tech_dtp_external_render_gate_promotion_001`; `SOP-KIRBE_TRACEABILITY_OBSERVABILITY_001`; `gtm_madeira_dtp_{154,155}` | 7 |
| `CAP-APPLICATION-SECURITY` | `CAP-ENV-TECH-DTP-{13,277}` | `env_tech_dtp_{13,277}` | 2 |
| `CAP-DATABASE-GRAPH-MGMT` | `CAP-ENV-TECH-DTP-{15,270}`; `CAP-SOP-GRAPHDB-NEO4J-001`; `CAP-SOP-KIRBE-GRAPHDB-NEO4J-002` | `env_tech_dtp_{15,270}`; `SOP-GRAPHDB_NEO4J_001`; `SOP-KIRBE_GRAPHDB_NEO4J_002` | 4 |
| `CAP-DOMAIN-DNS-MGMT` | `CAP-ENV-TECH-DTP-{28,29,30,44}` | `env_tech_dtp_{28,29,30,44}` | 4 |
| `CAP-ECOMMERCE-PLATFORM-INTEGRATION` | `CAP-ENV-TECH-DTP-{56,242,294,296,297,298}` | `env_tech_dtp_{56,242,294,296,297,298}` | 6 |
| `CAP-THIRD-PARTY-INTEGRATION-MGMT` | `CAP-ENV-TECH-DTP-{18,63,64}`; `CAP-GTM-MADEIRA-DTP-{156,158}` | `env_tech_dtp_{18,63,64}`; `gtm_madeira_dtp_{156,158}` | 5 |
| `CAP-ENVOY-TECHLAB-SHOWCASE` | `CAP-SOP-ENVOYLAB-REFACTOR-ARCHITECTURE-001`; `CAP-SOP-AI-STUDIO-SHOWCASE-ENHANCEMENT`; `CAP-SOP-MADEIRA-ENVOYTECH-SHOWCASE-002`; `CAP-SOP-KIRBE-ENVOYTECH-SHOWCASE-003`; `CAP-SOP-MADEIRA-HLK-ERP-SHOWCASE-004` | `SOP-ENVOYLAB_REFACTOR_ARCHITECTURE_001`; `SOP-AI_STUDIO_SHOWCASE_ENHANCEMENT`; `SOP-MADEIRA_ENVOYTECH_SHOWCASE_002`; `SOP-KIRBE_ENVOYTECH_SHOWCASE_003`; `SOP-MADEIRA_HLK_ERP_SHOWCASE_004` | 5 |
| `CAP-MARKETING-PRODUCT-DATA-PLATFORM` | `CAP-ENV-TECH-DTP-{35,36,37,38,45,46,49,243}` | `env_tech_dtp_{35,36,37,38,45,46,49,243}` | 8 |
| `CAP-DATAOPS-QUALITY-ASSURANCE` | `CAP-HOL-DATAOPS-QUALITY-CHECK-001` | `env_tech_dtp_dataops_quality_001` | 1 |
| `CAP-AI-PRODUCT-GTM-LAUNCH` | `CAP-ENV-TECH-DTP-244`; `CAP-GTM-MADEIRA-DTP-{29..43,46,47,48,49,219,220,221,222,223}`; `CAP-GTM-CL-{6f205adfbb6119,aa7b490c0fca48,b35cb2c55bea2f,c4268c352c26e7,f23d23dfda8a02,b8104f5193dcac}` | `env_tech_dtp_244`; `gtm_madeira_dtp_{29..43,46,47,48,49,219,220,221,222,223}`; `gtm_cl_{6f205adfbb6119,aa7b490c0fca48,b35cb2c55bea2f,c4268c352c26e7,f23d23dfda8a02,b8104f5193dcac}` | 31 |
| `CAP-DOC-REDACTION-PRIVACY-TOOLING` | `CAP-ENV-TECH-DTP-{24,25}`; `CAP-SOP-DYNAMIC-DOCUMENT-REDACTION-001` | `env_tech_dtp_{24,25}`; `SOP-DYNAMIC_DOCUMENT_REDACTION_001` | 3 |
| `CAP-CLIENT-AI-DATAOPS-DELIVERY` | `CAP-HOL-DATAOPS-SUEZ-LIBELLE-GENERATOR-001`; `CAP-HOL-DATAOPS-SUEZ-CATEGORY-ACCOUNT-MAPPING-001`; `CAP-HOL-MADEIRA-SUEZ-EMAIL-EXTRACTION-001`; `CAP-HOL-DATAOPS-SUEZ-DISPUTE-REGISTER-001`; `CAP-HOL-DATAOPS-SUEZ-USAGE-DASHBOARD-001` | `hol_eng_prc_engagement_design_001` (×5; the SUEZ POC module family — N:1 originating process) | 5 |

> **Folding note (LlamaIndex construction block `gtm_madeira_dtp_159..190`).** These 32 rows
> (minus the three agent rows 176/177/181 → orchestration, and 191..217 → evicted) fold into
> `CAP-KNOWLEDGE-RETRIEVAL-RAG` as framework-component realizing processes. Several
> (`StorageContext`, `Init Vector Store`, `Callback Manager`, `Open AIEmbedding`,
> `asynccontextmanager`) are themselves **component-grade** and are flagged as **secondary
> eviction candidates** in §3 — kept in the rollup here so the row count is honest, but a future
> component-primitive pass may relocate them next to the §3 block.

---

## 3. Code-symbols to EVICT → `COMPONENT_PRIMITIVE_REGISTRY`

Per method step 1 ("strip non-capabilities"; E-19 *"naming capabilities after systems defeats the
purpose"*). These rows' `capability_name` is a verbatim software identifier — a class, function,
HTTP-verb endpoint handler, module dunder, or `*_SYSTEM_PROMPT` constant — with **no
business-outcome reading**. They are components *of* `CAP-CONVERSATIONAL-AI-ENGINE` /
`CAP-AI-PERSONA-PERSONALITY`, not capabilities.

**This is exactly the `gtm_madeira_dtp_191..217` block the method doc named as cluster #3 (27 → 1 +evict).** 217 − 191 + 1 = **27 rows**, matching the method's projection precisely.

| # | old `capability_id` | old name (code symbol) | symbol kind | proposed `component_primitive_code` |
|:--|:--|:--|:--|:--|
| 1 | `CAP-GTM-MADEIRA-DTP-191` | MADEIRA delivery — Close Db | function | `CP-MADEIRA-CLOSE-DB` |
| 2 | `CAP-GTM-MADEIRA-DTP-192` | MADEIRA delivery — Query | method | `CP-MADEIRA-QUERY` |
| 3 | `CAP-GTM-MADEIRA-DTP-193` | MADEIRA delivery — Structured Response | class | `CP-MADEIRA-STRUCTURED-RESPONSE` |
| 4 | `CAP-GTM-MADEIRA-DTP-194` | MADEIRA delivery — Pydantic Query Engine | class | `CP-MADEIRA-PYDANTIC-QUERY-ENGINE` |
| 5 | `CAP-GTM-MADEIRA-DTP-195` | MADEIRA delivery — Enhanced Madeira Agent | class | `CP-MADEIRA-ENHANCED-AGENT` |
| 6 | `CAP-GTM-MADEIRA-DTP-196` | MADEIRA delivery — Async Stream Wrapper | class | `CP-MADEIRA-ASYNC-STREAM-WRAPPER` |
| 7 | `CAP-GTM-MADEIRA-DTP-197` | MADEIRA_SYSTEM_PROMPT | constant | `CP-MADEIRA-SYSTEM-PROMPT` |
| 8 | `CAP-GTM-MADEIRA-DTP-198` | MADEIRA delivery — Assistant Memory | class | `CP-MADEIRA-ASSISTANT-MEMORY` |
| 9 | `CAP-GTM-MADEIRA-DTP-199` | MADEIRA delivery — Get Madeira Agent | function | `CP-MADEIRA-GET-AGENT` |
| 10 | `CAP-GTM-MADEIRA-DTP-200` | MADEIRA delivery — Custom Re Act Agent | class | `CP-MADEIRA-CUSTOM-REACT-AGENT` |
| 11 | `CAP-GTM-MADEIRA-DTP-201` | MADEIRA delivery API — POST madeira_query | endpoint | `CP-MADEIRA-EP-POST-QUERY` |
| 12 | `CAP-GTM-MADEIRA-DTP-202` | MADEIRA delivery — Stream Query Request | class | `CP-MADEIRA-STREAM-QUERY-REQUEST` |
| 13 | `CAP-GTM-MADEIRA-DTP-203` | MADEIRA delivery API — POST madeira_stream_query | endpoint | `CP-MADEIRA-EP-POST-STREAM-QUERY` |
| 14 | `CAP-GTM-MADEIRA-DTP-204` | MADEIRA delivery API — GET madeira_personality | endpoint | `CP-MADEIRA-EP-GET-PERSONALITY` |
| 15 | `CAP-GTM-MADEIRA-DTP-205` | MADEIRA delivery API — POST madeira_personality | endpoint | `CP-MADEIRA-EP-POST-PERSONALITY` |
| 16 | `CAP-GTM-MADEIRA-DTP-206` | MADEIRA delivery — Get Storage Context | function | `CP-MADEIRA-GET-STORAGE-CONTEXT` |
| 17 | `CAP-GTM-MADEIRA-DTP-207` | MADEIRA delivery API — GET health | endpoint | `CP-MADEIRA-EP-GET-HEALTH` |
| 18 | `CAP-GTM-MADEIRA-DTP-208` | MADEIRA delivery API — POST clear_madeira_memory | endpoint | `CP-MADEIRA-EP-POST-CLEAR-MEMORY` |
| 19 | `CAP-GTM-MADEIRA-DTP-209` | MADEIRA delivery — __main__ | dunder | `CP-MADEIRA-MAIN-ENTRYPOINT` |
| 20 | `CAP-GTM-MADEIRA-DTP-210` | MADEIRA delivery — Sentiment Analyzer | class | `CP-MADEIRA-SENTIMENT-ANALYZER` |
| 21 | `CAP-GTM-MADEIRA-DTP-211` | MADEIRA delivery — Emotional State | class/enum | `CP-MADEIRA-EMOTIONAL-STATE` |
| 22 | `CAP-GTM-MADEIRA-DTP-212` | MADEIRA delivery — Interaction Style | class/enum | `CP-MADEIRA-INTERACTION-STYLE` |
| 23 | `CAP-GTM-MADEIRA-DTP-213` | MADEIRA delivery — LLMConfig | class | `CP-MADEIRA-LLM-CONFIG` |
| 24 | `CAP-GTM-MADEIRA-DTP-214` | MADEIRA delivery — Personality Trait | class | `CP-MADEIRA-PERSONALITY-TRAIT` |
| 25 | `CAP-GTM-MADEIRA-DTP-215` | MADEIRA delivery — Personality Config | class | `CP-MADEIRA-PERSONALITY-CONFIG` |
| 26 | `CAP-GTM-MADEIRA-DTP-216` | MADEIRA delivery — Madeira Personality System | class | `CP-MADEIRA-PERSONALITY-SYSTEM` |
| 27 | `CAP-GTM-MADEIRA-DTP-217` | EnhancedMadeiraAgent (2) | class (dup of #5) | `CP-MADEIRA-ENHANCED-AGENT` (merge — duplicate) |

**Eviction = 27 rows** (`gtm_madeira_dtp_191..217`). All parent to artifact-class `madeira_delivery_runtime`; `kind: software` (a new value vs the registry's existing deliverable-primitive kinds — see schema note).

> **Schema note (for the gated write).** `COMPONENT_PRIMITIVE_REGISTRY.csv` today holds 25
> **deliverable-rendering** primitives (`CP-COVER-PAGE`, `CP-EXECUTIVE-SUMMARY`, kinds
> `visual`/`prose`). These MADEIRA code symbols are **software** components. `ENTITY_CATALOG`
> already routes `component → COMPONENT_PRIMITIVE_REGISTRY.csv`, so the home is correct, but the
> evicted rows introduce a `kind: software` class. The gated canonical-CSV write should either
> (a) add `kind: software` to the registry's allowed values, or (b) stand up a sibling
> `COMPONENT_PRIMITIVE_REGISTRY` partition for runtime/software primitives. **Decision deferred to
> the operator/AIC at the canonical-CSV gate** (inline-ratify) — this doc only proposes the eviction set.

> **Secondary eviction candidates (NOT in the 27; folded into `CAP-KNOWLEDGE-RETRIEVAL-RAG` for now).**
> The adjacent LlamaIndex construction block `gtm_madeira_dtp_159..190` (e.g. `StorageContext`,
> `VectorStoreIndex/PGVectorStore`, `GraphStoreIndex/Neo4jGraphStore`, `Init Vector/Graph/Storage`,
> `Callback Manager`, `Open AIEmbedding`, `QueryEngineTool`, `ChatMessage`, `asynccontextmanager`)
> is equally component-grade. The method doc's named set stops at 191, so to stay faithful and
> bounded the **primary eviction = the 27 named rows**; these ~20 are flagged for a follow-up
> component-primitive sweep rather than silently inflating the headline count.

---

## 4. Cross-area flags

Five Tech-seeded capabilities have their **stable home in another area's map** (capabilities are
org-agnostic — method step 3 + E-2/E-19). They are fully accounted in §1–§2 so no Tech row is
orphaned, but at the gated write the operator/AIC should decide whether each **moves to the
sibling area's slice** or stays Tech-owned with a cross-area `realization` edge. Recommendation:
move to the named area, keeping Tech as a *realizing* role via TRP-039 where Tech still builds it.

| proposed_capability_id | Tech rows | stable home (L1 domain / area) | why it is not Tech-native | recommendation |
|:--|--:|:--|:--|:--|
| `CAP-AI-SCENARIO-RESEARCH-RADAR` | 36 | Corporate Intelligence & **Research** | `gtm_madeira_dtp_1..28,45,218` + 6 `gtm_cl` "research radar … themes" are macro/geo/tech/legal/social/econ **scenario topics**, not engineering abilities. These are CORPINT research-radar content (see `akos-research-area.mdc` RULE 1). | Move to Research area map; MADEIRA *consumes* it via TRP-029 (use_case realization). |
| `CAP-AI-PRODUCT-GTM-LAUNCH` | 31 | **Go-to-Market & Brand** / Product Mgmt | `gtm_madeira_dtp_29..43,46..49,219..223` + `gtm_cl` product-delivery rows are market-requirements / business-case / positioning / pricing / alpha-beta-GA release — product GTM, not platform engineering. | Move to GTM map; Tech realizes the *delivery* slice (build) via TRP-006. |
| `CAP-MARKETING-PRODUCT-DATA-PLATFORM` | 8 | **Data Governance & Enterprise Knowledge** (+ **Marketing**) | `env_tech_dtp_35..38,45,46` are explicitly tagged "(HLK Data Governance)"; `env_tech_dtp_49` (SEM) is demand-gen; `243` is the analytics pipeline. Audience/event/campaign governance is a Data ability; SEM is a Marketing ability. | Split: data-governance rows → Data map; SEM/demand-gen → Marketing map; Tech realizes the integration plumbing. |
| `CAP-CLIENT-AI-DATAOPS-DELIVERY` | 5 | **Delivery & Client Engagement Operations** | The 5 SUEZ-POC rows all originate from `hol_eng_prc_engagement_design_001` — a client-engagement process, not a Tech-platform process. | Move to Delivery map; Tech + AI realize the modules per engagement. |
| `CAP-DOC-REDACTION-PRIVACY-TOOLING` | 3 | **Legal, Compliance & Privacy** | `env_tech_dtp_24` (Retention) + `env_tech_dtp_25` (NDA) + `SOP-DYNAMIC_DOCUMENT_REDACTION_001` are privacy/retention controls — a Legal ability the product enforces. | Keep tooling build in Tech; the *capability* (the control) is Legal-owned (TRP-039 Legal role assignment). |

**Not cross-area (Tech-native, noted to pre-empt confusion):** `CAP-DATAOPS-QUALITY-ASSURANCE`
sits under the Data-Governance L1 domain but is **Tech-owned** (System Owner; the canonical-CSV +
mirror data-quality gate is a Tech/Platform discipline) — it stays in the Tech slice.

---

## 5. Count summary

| | rows |
|:--|--:|
| **Tech rows in `CAPABILITY_REGISTRY.csv` (area = Tech)** | **379** |
| → roll up into stable capabilities | 352 |
| → evicted to `COMPONENT_PRIMITIVE_REGISTRY` (§3) | 27 |
| **Reconciliation** (352 + 27) | **379 ✓** |

**379 → 27 stable capabilities (+27 evicted).** Net de-densification on the surviving map: **352 → 27 ≈ 13:1**.

Per L1 domain (stable-capability count · rolled-row count):

| L1 domain | capabilities | rolled rows |
|:--|--:|--:|
| Applied AI & MADEIRA | 8 | 196 |
| Product & Platform Engineering | 14 | 108 |
| Data Governance & Enterprise Knowledge | 2 | 9 |
| Go-to-Market & Brand *(cross-area)* | 1 | 31 |
| Legal, Compliance & Privacy *(cross-area)* | 1 | 3 |
| Delivery & Client Engagement Operations *(cross-area)* | 1 | 5 |
| **Total** | **27** | **352** |

**Sizing check (E-17 / E-3):** Tech is the largest of the ~9 L1 domains (379 of 1,119 ≈ 34% of the
registry). 27 stable Tech capabilities is consistent with the 40–100 **whole-enterprise** L2
sweet-spot once the other 7 areas are collapsed — Tech alone should be ~⅓ of that band, and 27
lands there. After eviction the map is strategy-legible (no `LLMConfig` / `__main__` rows), which is
the entire point (E-19/E-20: a capability map must not decay into a component/process catalog).

## Cross-references
- Method (ratified): [`l2-capability-densify-findings-2026-06-07.md`](../l2-capability-densify-findings-2026-06-07.md) — 6-step collapse, eviction rule, ~9 L1 domains, worked clusters #1/#3.
- Parent decision: **D-IH-95-H** (de-densify, keep-separate, area-by-area, organic count).
- Source registry: `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv` (area = Tech rows).
- Eviction target: `…/dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv` (+ schema note §3 for the `kind: software` extension).
- Gate: the actual `CAPABILITY_REGISTRY` rewrite is a **canonical-CSV change** (`akos-baseline-governance.mdc`) — operator approval, per-domain slices; this doc is the reviewable proposal for the Tech slice.
- Cross-area handoffs (§4): Research (`akos-research-area.mdc`), GTM/Brand, Data Governance, Legal, Delivery — sibling area maps receive the flagged capabilities.
