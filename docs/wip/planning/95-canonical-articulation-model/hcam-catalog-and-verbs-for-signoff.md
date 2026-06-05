---
intellectual_kind: design_signoff
initiative: INIT-OPENCLAW_AKOS-95
phase: P1 pre-build (catalog sign-off gate)
authored: 2026-06-05
status: awaiting_operator_signoff
language: en
named_decision: D-IH-95-B (entity catalog + verb set + valid-triple matrix)
gate: catalog_signoff_first (operator 2026-06-05)
---

# HCAM — entity catalog + verbs + sample triples (SIGN-OFF GATE)

> **Operator gate (catalog_signoff_first):** sign off the **entity catalog**, the **~10 verbs**,
> and **sample triples** before I build `CANONICAL_RELATIONSHIP_REGISTRY.csv` + Pydantic +
> validator. Nothing is wired until you approve. Ownership ratified **Data-federated**; council
> **full** + **wired into existing Governance**.

## A. Entity catalog (the node labels) — ~31 canonical types

Each type → one **ArchiMate aspect** (Active structure = performer / Behavior = action /
Passive = object / Motivation = why / Strategy = capability / Implementation = roadmap) and one
**Zachman cell** (Who/How/What/Why/When/Where). "Graph today" = projected in `hlk_graph_model.py`.

| # | Entity type | SSOT | ArchiMate aspect | Zachman | Graph today | Owning area |
|:--|:---|:---|:---|:---|:---|:---|
| 1 | **Role** | baseline_organisation.csv | Active structure | Who | :Role | People |
| 2 | **AIC** | AIC_REGISTRY.csv | Active structure | Who | — | Tech |
| 3 | **Persona** | PERSONA_REGISTRY.csv | Active structure (archetype) | Who | :Persona | Marketing |
| 4 | **Entity** (Holistika/ThinkBig/HLKTechLab) | baseline_organisation.entity | Active structure (org unit) | Who | — | People |
| 5 | **Process** | process_list.csv | Behavior | How | :Process | per-area |
| 6 | **Pattern** | PEOPLE_DESIGN_PATTERN_REGISTRY.csv | Behavior (template) | How | — | People |
| 7 | **Engagement** | ENGAGEMENT_REGISTRY.csv | Behavior / service | How | — | Finance/Reach |
| 8 | **OPS action** | OPS_REGISTER.csv | Implementation | When | — | People/Compliance |
| 9 | **Capability** | CAPABILITY_REGISTRY.csv | Strategy | How/What | — | per-area |
| 10 | **Area** | AREA_KIND_ENTITY (area model) | Strategy (bounded context) | Where | — | People |
| 11 | **Topic** | TOPIC_REGISTRY.csv | Passive structure | What | :Topic | Research/KM |
| 12 | **Component** | COMPONENT_PRIMITIVE_REGISTRY.csv | Passive / app component | What | — | Tech |
| 13 | **Skill** | SKILL_REGISTRY.csv | Behavior (competence) | How | :Skill | People |
| 14 | **Canonical** | CANONICAL_REGISTRY.csv | Passive (artifact) | What | — | per-area |
| 15 | **Metric** | METRICS_REGISTRY.csv | Passive (measure) | What | — | Data |
| 16 | **Decision** | DECISION_REGISTER.csv | Motivation | Why | — | People/Compliance |
| 17 | **Policy** | POLICY_REGISTER.csv | Motivation | Why | :Policy | per-area |
| 18 | **Goal/POI** | GOI_POI_REGISTER.csv | Motivation | Why | — | per-area |
| 19 | **Audience** | AUDIENCE_REGISTRY.csv | Motivation (stakeholder) | Who/Why | — | Marketing |
| 20 | **Initiative** | INITIATIVE_REGISTRY.csv | Implementation | When | — | per-area |
| 21 | **Program** | PROGRAM_REGISTRY.csv | Implementation | When | :Program | per-area |
| 22 | **Channel** | CHANNEL_TOUCHPOINT_REGISTRY.csv | Active structure (interface) | Where | :Channel | Marketing |
| 23 | **Touchpoint-kit-cell** | TOUCHPOINT_KIT_CELL_REGISTRY.csv | Passive | Where | :TouchpointKitCell | Marketing |
| 24 | **Sourcing** | SOURCING_REGISTER.csv | Active structure | Where | :Sourcing | Reach |
| 25 | **Artifact-class** | ARTIFACT_CLASS_REGISTRY.csv | Passive (meta) | What | — | People/Compliance |
| 26 | **Output-type** | OUTPUT_TYPE_REGISTRY.csv | Passive (meta) | What | — | People/Compliance |
| 27 | **Substrate** | SUBSTRATE_REGISTRY.csv | Technology object | What/Where | — | Tech |
| 28 | **Use-case** | USE_CASE_ARCHIVE.csv | Behavior (scenario) | How | — | Marketing |
| 29 | **Persona-scenario** | PERSONA_SCENARIO_REGISTRY.csv | Behavior (scenario) | How | — | Marketing |
| 30 | **Source/Fact** | source_taxonomy + intelligence | Passive (evidence) | What | — | Research/KM |
| 31 | **Calendar/Cadence** | COUNTRY_WORK_CALENDAR + cadence_type | Time | When | — | Operations |

*Sign-off question 1: is this the right ~31, or add/remove any? (e.g. should Workstream be its own
type, or is it = Program-child? Should Sub-mark/Brand be explicit Marketing types?)*

## B. The closed verb set (10 + 1) — ArchiMate-grounded

| Verb | Definition | Holistika use | Replaces (forked edge) |
|:---|:---|:---|:---|
| **composition** | strong whole-part (part dies with whole) | area→sub-area; process project→…→task; topic/program tree | `PARENT_OF`+`PROGRAM_PARENT_OF`+`TOPIC_PARENT_OF` |
| **aggregation** | weak whole-part (part lives independently) | program aggregates initiatives; topic aggregates facts | `*_SUBSUMES` |
| **assignment** | performs / owns / accountable | role→process; role→role (reports_to); area→role | `OWNED_BY`, `REPORTS_TO` |
| **realization** | concrete realizes abstract | process→capability; pattern→process; canonical→pattern | `inherited_pattern_id` |
| **serving** | provides function to a consumer | process→engagement; component→role; platform area→area; channel→audience | `PRODUCES_FOR`/`CONSUMES` |
| **access** | reads/writes a passive object | process→registry/metric; metric→data-contract | (implicit today) |
| **influence** | affects a motivation element | decision→area/process; policy→process; OPS→initiative | (implicit) |
| **triggering** | temporal/causal sequence | process→process handoff; lifecycle stage→stage | (new) |
| **flow** | transfer between elements | engagement→counterparty; producer→consumer | `CONSUMES` |
| **specialization** | "is a kind of" | sub-mark→brand; persona-scenario→persona | (new) |
| *association* | *catch-all (minimize)* | *only when none above fits; flagged for review* | *RELATED_TO* |

*Sign-off question 2: accept the ArchiMate 10 (+association as last-resort), or adjust?*

## C. Sample valid triples (representative — full matrix built after sign-off)

| Source type | verb | Target type | Evidence (current FK / fact) |
|:---|:---|:---|:---|
| Area | composition | Area (sub-area) | area model sub_area |
| Area | assignment | Role | baseline_organisation.area |
| Role | assignment | Process | process_list.role_owner |
| Role | composition | Role (reports_to) | baseline_organisation.reports_to |
| Role | serving← Component (component serves role) | Component | baseline_organisation.components_used |
| Process | composition | Process (activity/task) | process_list.item_parent_*_id |
| Process | realization | Capability | (new triple; capability map) |
| Process | realization← Pattern | Pattern | process_list.inherited_pattern_id |
| Process | serving | Engagement | process_list.engagement_template_id |
| Process | serving | Persona | process_list.persona_id |
| Process | access | Metric/Registry | SEMANTIC_LAYER source refs |
| Process | triggering | Process | (new; lifecycle handoff) |
| Engagement | flow | Entity/Counterparty | FINOPS counterparty |
| Engagement | serving | Audience | engagement model |
| Capability | composition | Capability | capability map levels |
| Program | aggregation | Initiative | INITIATIVE_REGISTRY.program_anchors |
| Initiative | influence← Decision | Decision | DECISION_REGISTER.initiating_initiative_id |
| Decision | influence | Area/Process | DECISION_REGISTER.linked_* |
| Policy | influence | Process | POLICY_REGISTER |
| OPS action | influence | Initiative | OPS_REGISTER.linked |
| Topic | composition | Topic | TOPIC_REGISTRY parent |
| Topic | aggregation | Source/Fact | intelligence matrix |
| Channel | serving | Audience | CHANNEL_TOUCHPOINT |
| Canonical | realization | Pattern | inherited_pattern_id |
| Persona-scenario | specialization | Persona | PERSONA_SCENARIO |
| Metric | access | Source/Contract | METRICS_REGISTRY.source_contract_id |

*Sign-off question 3: do these articulations match how you think about the business? Any missing
key link (e.g. Skill→Role, Use-case→Capability, AIC→Process)?*

## D. Semantic Council — full, wired into existing Governance

**Membership (full from day one):**
- **Chair:** CDO (accountable).
- **Data core:** Data Architect (HCAM metamodel author) · Data Governance Lead (relationship-
  registry owner) · Data Steward (operational triples) · AI Engineer + System Owner (graph platform).
- **8 area reps:** one per scored area — Data, Finance, Marketing, Tech, People, Research,
  Operations, Legal — each = that area's owner from the **area-governance model** (federated authorship).

**Wired into the Governance we already built (no parallel governance):**

| Existing governance asset | How the council reuses it (does NOT duplicate) |
|:---|:---|
| **O5 Executive Governance Board** | Council reports into O5; O5 holds final authority on enterprise-level changes |
| **DECISION_REGISTER** (`D-IH-*`) | Cross-area verb/triple/catalog changes ratified as decisions — same register, same cadence |
| **process_list + SOP-META** | The council's operation = a **governed process** with a SOP + runbook (owned by Data Governance Lead), like `SOP-DATA_CONTRACT_REGISTRY_MAINTENANCE_001` — so the **process-governance work is reused, not lost** |
| **Area-governance methodology** (People/Compliance) | Each area rep federates their area's concepts through the existing area-governance cadence; area-completeness **v3** (articulation completeness) is the acceptance check |
| **OPS_REGISTER** | Council actions tracked as OPS rows |
| **CANONICAL_REGISTRY** | HCAM + the relationship registry registered as governed canonicals (T1/T2/T3 declaration) |
| **DATA three-tier architecture** | Registry = T1 SSOT; Neo4j = T3 projection (parity-checked) — reuses `DATA_ARCHITECTURE.md` |

*Sign-off question 4: this wiring keeps HCAM governance inside the existing fabric (O5 board +
DECISION_REGISTER + SOP-META + area-governance + OPS + CANONICAL_REGISTRY). Good, or want it tied
in differently?*

## E. What I build AFTER sign-off (P1 = B)
1. `CANONICAL_RELATIONSHIP_REGISTRY.csv` (the full valid-triple matrix from §C, expanded) +
   `ENTITY_CATALOG` (§A) — as **Data-Architecture canonicals** (sibling to `SEMANTIC_LAYER.md`).
2. `akos/hlk_canonical_articulation.py` (Pydantic: entity catalog enum + verb enum + triple schema).
3. `scripts/validate_canonical_articulation.py` (validates triples against the catalog; self-test).
4. Tests; wire into `validate_hlk.py`.
5. The council SOP + runbook (governed-process wiring, §D).
6. Ratify as **D-IH-95-B**.

Then **C** (Neo4j unify, coupled with I91) and **E** (area-completeness v3 + Q2/Q3 placement).
