---
intellectual_kind: research_findings
parent_initiative: INIT-OPENCLAW_AKOS-95
related_initiatives: [94, 93, 91]
authored: 2026-06-05
status: active
language: en
named_decision: D-IH-95-A (ownership sub-decision pending operator ratify)
control_confidence_level: Keter
source_ledger: ./source-ledger.csv (Prong E; +53 rows, 27 external / 26 internal)
note: HONEST ownership recommendation per operator request - Data-Governance / semantic-layer findings
---

# Who owns HCAM? — Data Governance / semantic-layer findings (honest answer)

> **Operator asked (2026-06-05):** *"involve data governance before, I feel they are completely
> left out and they shouldn't… research +25 internal & +25 external about semantic layer / data
> governance… resurface."* And: *"[KM home] I say option B [Learning Curator → KM] but maybe it
> should be in Research? what do you think and what do you recommend… be honest."*
>
> You asked for honesty. Here it is, with 53 new sources behind it.

## 1. The honest headline

**You were right and I had drifted.** My earlier "Knowledge Manager under People" framing
over-indexed on the word *knowledge*. The evidence — internal and external — is overwhelming:
**the enterprise ontology / semantic layer is a Data discipline, owned federated, not a People-KM
or Research function.** Data Governance was being left out, and they shouldn't be.

**My recommendation: home HCAM in Data, as the entity-and-relationship tier of the Semantic Layer
Data already owns — governed federated, with each area contributing its own concepts.** Not
Learning Curator → KM. Not Research-as-owner. Below is why, and what each role does.

## 2. The decisive internal fact: Data already owns this

Two canonicals already exist in the Data area, both authored by the **Data Architect**, ratified
`D-IH-93-D`:

- **`SEMANTIC_LAYER.md`** (Data/Architecture) — *"define-once-use-everywhere"* governance. Today
  it governs **metrics** (`METRICS_REGISTRY.csv`). HCAM is simply its **entity + relationship
  tier** — the same canonical, extended from "what a metric means" to "what every artifact is and
  how it links."
- **`DATA_ARCHITECTURE.md`** — the **three-tier model**: T1 git-CSV SSOT → T2 Supabase → **T3
  Neo4j graph** ("Role Process Program Topic + 6-axis nodes"). It already governs the very graph
  HCAM would type, already references `akos/hlk_graph_model.py` and the parity assertions, and
  already maps to DAMA conceptual/logical/physical. **HCAM is not a new home — it's the missing
  semantic tier of an architecture Data already runs.**

And the **graph rework you mentioned is real and named**: initiative **I91 — Enterprise Graph
Store Coverage** (`docs/wip/planning/91-enterprise-graph-store-coverage/`). HCAM (I95) and the
graph rework (I91) are **one workstream** — exactly the bidirectional coupling you asked for.

## 3. The roster already has the seats (no new role needed)

| Role | Charter (verbatim) | HCAM responsibility |
|:---|:---|:---|
| **CDO** | oversees Data Architecture/Science/Engineering/Governance | **Accountable**; chairs the Semantic Council |
| **Data Architect** | "structure of available data… current and future architecture"; authors SEMANTIC_LAYER + DATA_ARCHITECTURE | **HCAM metamodel author** (entity catalog + verb taxonomy) |
| **Data Governance Office** | "enterprise masterdata, **masterdata relationship management**, data quality standards" | **Relationship-registry owner** (valid-triple standards) |
| **Data Steward** | "day-to-day… **masterdata relationship management**" | **Operational triple stewardship** |
| **AI Engineer** (Tech) | "owns the **Neo4j knowledge graph**… GraphRAG… intersection of Data Architecture and Tech" | **Graph platform / engineering** |
| **System Owner** (Tech) | "infrastructure and data governance" | **Platform custodian** for the store |

The phrase **"masterdata relationship management"** is literally in the Data Governance Office's and
Data Steward's charters. HCAM's triples *are* masterdata relationship management. The fit is exact.

## 4. The external consensus: federated, Data-led

- **DAMA-DMBOK:** Data Governance is "the **coordinating** knowledge area"; Data Architecture +
  Metadata Management own structure + semantics + the business glossary. Enterprise ontologies are
  *"assets which should have the same degree of governance and stewardship as other data assets"*
  (EWSolutions) — and Data Stewards *"must be involved when ontologies are developed/changed."*
- **Data mesh — federated computational governance:** global standards set centrally + enforced
  locally; **domains own their own concepts**; a **governance council** (domain + platform reps)
  resolves cross-domain conflicts (Fowler/Dehghani; Starburst; dbt; OvalEdge).
- **Ontology-governance operating model (tripartite):** *domain stewards* (propose concepts) +
  *semantic architecture board / Semantic Council* (cross-domain standards, naming, SHACL gates,
  final approval) + *platform team* (publish/rollout) (Galaxy; Architect Coach).
- **Real-world roles confirm placement:** "Knowledge Graph & Semantic Governance Manager"
  (AstraZeneca) and "Ontology Expert & Knowledge Graph Engineer" (Siemens) **both sit in the Data
  Office**, collaborating with AI/ML + enterprise architecture. Nobody puts the enterprise ontology
  under L&D or pure research.
- **Business glossary** is *business-owned for meaning, Data-steward-maintained for structure* — so
  each **area** owns its concept definitions (federated authorship), Data stewards the registry.

## 5. So, honestly, on your three candidates

- **Learning Curator → Knowledge Manager (your option B): NO.** Learning Curator is curriculum +
  knowledge-transfer (teaching people). That is the wrong skillset for ontology engineering +
  masterdata relationship governance. Mis-homing it there repeats the "fell to generic People"
  error in a new costume.
- **Research: NO as owner, YES as contributor.** Research authors new canonical *concepts* and
  methodology — it **feeds** the entity catalog (a domain steward of the "Research" area). But it
  does not govern the operational metamodel or the graph. Owner ≠ contributor.
- **Data (federated): YES — recommended.** Data Architect authors HCAM; Data Governance Office owns
  the relationship registry/standards; Data Steward maintains triples; AI Engineer/System Owner run
  the graph platform; CDO chairs a **Semantic Council** with one stakeholder per area (each area
  federates its own concepts); **People/Compliance keeps the area-governance *methodology*** (the
  meta-process for chartering areas — that part *is* People's, and it's distinct from HCAM).

This separates two things you (understandably) had fused: the **articulation metamodel / semantic
layer** (Data) vs the **area-governance methodology** (People/Compliance). Both are real; they have
different homes.

## 6. What this changes in the build

- **No new Knowledge Manager role required.** Elevate the existing Data seats + stand up a Semantic
  Council. (If you still want a "Knowledge Manager" title, it belongs in Data as the council
  secretary / semantic-governance lead — not a reworked Learning Curator.)
- **P3 (=E.1) of I95 changes** from "mint KM role" to "publish HCAM as a **Data-Architecture
  canonical** (sibling to SEMANTIC_LAYER.md) + stand up the Semantic Council + federated area-rep
  model." Lower roster churn, higher fidelity.
- **Couple with I91** (graph rework) as one workstream.
- **Keep the Data Governance Office full name** (your Q2) — doubly justified now: they own the
  relationship registry.

## 7. Cross-references
- Existing Data ownership: `SEMANTIC_LAYER.md`, `DATA_ARCHITECTURE.md`, `DATA_GOVERNANCE_POLICY.md`
- Graph rework: I91 (`docs/wip/planning/91-enterprise-graph-store-coverage/`)
- Synthesis (updated §4): [`master-synthesis.md`](./master-synthesis.md)
- Ledger Prong E: [`source-ledger.csv`](./source-ledger.csv) (53 new rows)
