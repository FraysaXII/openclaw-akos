---
language: en
---

STANDARD OPERATING PROCEDURE

* Item Name: Standard Operating Procedure for Process Definition and Management  
* Item Number: SOP-META\_PROCESS\_MGMT\_001  
* Object Class: Guideline & Procedure  
* Confidence Level: High  
* Security Level: 2 (Internal Use)  
* Entity Owner: Holistika R\&D, Operations  
* Area Owner: Data Architecture & PMO  
* Associated Workstream: Process Governance, Knowledge Management, SOP Lifecycle Management  
* Version: 1.0  
* Revision Date: 2025-05-24

---
Table of Contents

* 1.0 Description  
* 2.0 Purpose  
* 3.0 Scope  
* 4.0 Procedure  
  * 4.1. Process Identification & Scoping  
  * 4.2. Process Decomposition & Modeling  
  * 4.3. SOP Documentation  
  * 4.4. Process Data Ingestion & Update  
  * 4.5. Review & Maintenance  
  * 4.6. Body and Addendum split (I80 P1; D-IH-80-B + D-IH-80-G)  
* 5.0 Roles and Responsibilities  
* 6.0 Addendum  
  * A.1: Process Definition Template

---

1.0 Description

This document outlines the standard procedure for identifying, defining, documenting, and maintaining all operational and technical processes within Holistika. It establishes a repeatable framework for capturing process knowledge in a structured format suitable for ingestion into the central process graph database (Neo4j), ensuring that our organizational knowledge is consistent, interconnected, and up-to-date. This SOP is the governing document for the creation of all other SOPs, including SOP-GRAPHDB\_NEO4J\_001.

2.0 Purpose

* To create a single source of truth for how Holistika defines and manages its internal processes.  
* To ensure all new processes are modeled and documented in a consistent manner.  
* To define the lifecycle of a process, from initial identification to ongoing maintenance or archival.  
* To provide a clear workflow for updating the central process graph database (`process_list.csv` and derived graph projections) with new or modified process information.

3.0 Scope

This SOP applies to all Holistika personnel designated as Process Owners, Area Owners, Data Architects, and members of the PMO who are involved in defining or documenting any new or existing business, technical, or operational process.

4.0 Procedure

The lifecycle of a process follows these key stages:

4.1. Process Identification & Scoping

* **Trigger:** A new process is required due to a new project, a change in business needs, or the formalization of an existing ad-hoc workflow.  
* **Action:** The designated Process Owner or Area Owner defines the high-level goal, scope, inputs, and outputs of the new process.  
* **Output:** A brief proposal or charter for the new process.

4.2. Process Decomposition & Modeling

* **Trigger:** The process proposal is approved.  
* **Action:** The Process Owner, in collaboration with a Data Architect, breaks the process down into its constituent parts according to the established hierarchy:  
  * **Project:** The highest-level container for a major initiative.  
  * **Workstream:** A major stream of work within a project.  
  * **Process:** A sequence of related tasks to achieve a specific outcome.  
  * **Task:** The most granular unit of work.  
* **Action:** Each item is modeled as a new row for the master process list (`process_list.csv`). Key attributes such as `item_id`, `item_name`, `item_granularity`, `item_parent_1`, `role_owner`, `entity`, and `area` must be defined.  
* **Output:** A set of new, validated rows ready for addition to the master process list CSV.

4.3. SOP Documentation

* **Trigger:** The process has been modeled.  
* **Action:** The Process Owner or a designated technical writer (e.g., from the PMO) creates a formal SOP document (like this one) that describes the process in detail. The `item_name` and `item_id` from the process model should be referenced in the SOP's metadata.  
* **Output:** A finalized SOP document, stored in the official knowledge repository (e.g., Confluence, SharePoint, Git).

4.4. Process Data Ingestion & Update

* **Trigger:** The new process rows have been added to the master CSV and the SOP is complete.  
* **Action:** A Data Engineer or DevOps Engineer executes the necessary procedures to update the Neo4j database. This involves:  
  1. Adding the new rows to the master `process_list.csv` file.  
  2. Executing an idempotent Cypher script (using `UNWIND` and `MERGE`) to create the new nodes and relationships in the graph database without affecting existing data.  
* **Output:** The Neo4j graph is updated to reflect the new process structure.

4.5. Review & Maintenance

* **Trigger:** A scheduled review (e.g., annually) or a change in the underlying process.  
* **Action:** The Process Owner reviews the SOP and its corresponding graph representation for accuracy. If changes are needed, the process returns to step 4.2.  
* **Output:** An up-to-date and validated process model and documentation.

4.6. Body and Addendum split (I80 P1; D-IH-80-B + D-IH-80-G)

* **Trigger:** Any SOP authored from 2026-05-16 forward, or any existing SOP undergoing scheduled review (§4.5) that carries cross-area technical jargon, validator names, mirror table references, or other supporting documentation that the executor does not need to perform the work end-to-end.
* **Action:** The Process Owner authors **two paired files** as the default contract:
  1. **Body** at `<area>/<role>/canonicals/SOP-<purpose>_<NNN>.md` — plain-language; speaks the executor's home dialect (Data canonicals speak data; Tech Lab canonicals speak tech; Finance canonicals speak finance; People canonicals speak plain language because People is for people); habilitates the executor to perform the work end-to-end with the relevant context — nothing more.
  2. **Addendum** at `<area>/<role>/canonicals/SOP-<purpose>_<NNN>.addendum.md` — carries everything else: cross-area jargon, validator names, mirror table details, system-owner audit material, scoring rubrics, integration postures, infrastructure dimensions.
* **What goes where (5-row rubric).** When in doubt about whether content belongs in the body or the addendum, apply this rubric in order:
  1. *Does the executor need this to perform the action?* → body.
  2. *Does this name a system, validator, mirror, or cross-area artifact the executor does not operate?* → addendum.
  3. *Does this carry jargon from another area?* → addendum (unless the executor's role natively spans both areas).
  4. *Does this require auditor or system-owner context for compliance evidence?* → addendum.
  5. *Could a new hire in the executor's role complete the SOP without this?* → addendum if yes.
* **Frontmatter contract.** Body and addendum each carry their **own complete frontmatter** (access_level, register, role_owner, classification, last_review, last_review_decision_id, methodology_version_at_review, ssot, intellectual_kind). Body and addendum **may diverge** on `access_level` / `classification` / `role_owner` (legitimate independent classification) and on `last_review` / `last_review_decision_id` (legitimate independent review cadences); they **must converge** on `methodology_version_at_review` (semantic version of the SOP itself). Both files cross-link in their frontmatter: body lists addendum under `companion_to`; addendum lists body under `parent_sop`.
* **Single-file degenerate case.** If an SOP body is fully self-sufficient and has no addendum-worthy content, do not split. Single-file is the **degenerate case** of the pattern, not a violation. Promote to paired-file when an addendum review concludes content has accumulated that does not belong in the body.
* **Anti-jargon drift gate scope.** Per **D-IH-80-F**, the People-canonical anti-jargon drift gate ([`scripts/validate_design_pattern_registry.py --jargon-scan`](../../../../../../scripts/validate_design_pattern_registry.py)) glob-excludes any file whose name ends with `.addendum.md` from scan scope at file-selection time. Addenda may legitimately carry cross-area jargon. The body must read plain.
* **Pattern provenance.** This contract instantiates [`pattern_sop_addendum_split`](../canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) (`pattern_class=documentation_layering`; the 11th class added at I80 P1 per **D-IH-80-G**). The narrative companion is at [`PEOPLE_DESIGN_PATTERN_LIBRARY.md` `#pattern-sop-addendum-split`](../../canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md#pattern-sop-addendum-split).
* **DAMA-DMBOK 2.0 alignment.** Paired-file is structurally aligned with three DAMA knowledge areas: **Metadata Management** (each file is a discrete metadata row consumable by KM systems without parsing markdown structure); **Reference & Master Data Management** (independent review cadences body vs addendum); **Data Integration & Interoperability** (Supabase RLS at file-level, not section-level; ERP panel filter routing becomes a join, not a regex).
* **Registry-side governance (I80 P6.5; D-IH-80-H).** Every paired-file pair authored under §4.6 — and every other documentation-relationship in the AKOS canonical vault (index→entries, doctrine→companion, charter→phases, registry→narrative) — is registered in [`KNOWLEDGE_PAIRING_REGISTRY.csv`](dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) at `Admin/O5-1/People/Compliance/canonicals/dimensions/`. The registry is the SSOT for documentation-relationships; PRECEDENCE.md remains the human-readable companion. Pydantic SSOT at [`akos/hlk_knowledge_pairing_csv.py`](../../../../../../akos/hlk_knowledge_pairing_csv.py); validator at [`scripts/validate_knowledge_pairing_registry.py`](../../../../../../scripts/validate_knowledge_pairing_registry.py) (wired into `validate_hlk.py` umbrella). When authoring a new paired-file pair, append a `pair_<purpose>_<NNN>` row alongside the file mints; validator runs in pre-commit.
* **Output:** A paired SOP body and addendum (or a single-file SOP body when the degenerate case applies), both registered in §7 of this document, in `process_list.csv` if the SOP operationalises a `process_list` row, AND in `KNOWLEDGE_PAIRING_REGISTRY.csv` if the SOP is paired (per §4.6 Registry-side governance).

5.0 Roles and Responsibilities

* **Process Owner / Area Owner:** Responsible for identifying the need for a process, defining its scope, and ensuring its accuracy over time.  
* **Data Architect:** Responsible for guiding the modeling of the process into the graph structure and ensuring it adheres to established patterns.  
* **PMO / Technical Writer:** Responsible for drafting and maintaining the formal SOP documentation.  
* **Data Engineer / DevOps Engineer:** Responsible for the technical execution of updating the master data file and the Neo4j database.

6.0 Addendum

A.1: Process Definition Template (for `process_list.csv`)

| item\_id | item\_name | item\_granularity | item\_parent\_1 | role\_owner | entity | area | ... |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| (unique\_id) | (Descriptive Name) | (project/workstream/process/task) | (Name of parent item) | (Role responsible) | (Holistika/Think Big/etc.) | (Ops/Tech/MKT/etc.) | ... |

7.0 Registered SOP Cross-References

This section lists every SOP that has gone through the §4 process and is currently active. New SOPs added under §4 must append a row here so the registry stays the canonical "what SOPs do we have?" lookup. Drift detection: every active SOP file must appear in this table; every row here must point to an existing file with `status: active`.

7.1 Brand Operations (Initiative I66 P3)

| SOP ID | File | process\_id | role\_owner | cadence |
| :---- | :---- | :---- | :---- | :---- |
| SOP-BRAND\_CANON\_MAINTENANCE\_001 | [`v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_CANON_MAINTENANCE_001.md`](../v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_CANON_MAINTENANCE_001.md) | tbi\_mkt\_prc\_brand\_canon\_mtnce\_001 | Brand Manager | Quarterly |
| SOP-BRAND\_VOICE\_DRIFT\_TRIAGE\_001 | [`v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md`](../v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md) | tbi\_mkt\_prc\_voice\_drift\_triage\_001 | Brand Manager | Monthly |
| SOP-BRAND\_REGISTER\_MATRIX\_REVIEW\_001 | [`v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_REGISTER_MATRIX_REVIEW_001.md`](../v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_REGISTER_MATRIX_REVIEW_001.md) | tbi\_mkt\_prc\_register\_matrix\_review\_001 | Brand Manager | Bi-annual |
| SOP-BRAND\_JARGON\_AUDIT\_REVIEW\_001 | [`v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_JARGON_AUDIT_REVIEW_001.md`](../v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_JARGON_AUDIT_REVIEW_001.md) | tbi\_mkt\_prc\_jargon\_audit\_review\_001 | Brand Manager | Quarterly |
| SOP-BRAND\_TEMPLATE\_REGISTRY\_MTNCE\_001 | [`v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001.md`](../v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001.md) | tbi\_mkt\_prc\_template\_registry\_mtnce\_001 | Brand Manager | Quarterly |
| SOP-BRAND\_DRIFT\_GATE\_OPS\_001 | [`v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_DRIFT_GATE_OPS_001.md`](../v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_DRIFT_GATE_OPS_001.md) | tbi\_mkt\_prc\_drift\_gate\_ops\_001 | Brand Manager | Quarterly |

7.2 Intelligence Operations (Initiative I66 P3 — HUMINT-derived)

| SOP ID | File | process\_id | role\_owner | cadence |
| :---- | :---- | :---- | :---- | :---- |
| SOP-IO\_COUNTERPARTY\_BASELINE\_ASSESSMENT\_001 | [`v3.0/Admin/O5-1/Operations/IntelligenceOps/SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md`](../v3.0/Admin/O5-1/Operations/IntelligenceOps/SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md) | hol\_res\_prc\_counterparty\_baseline\_assess\_001 | Holistik Researcher | Per-engagement |
| SOP-IO\_ELICITATION\_DISCIPLINE\_001 | [`v3.0/Admin/O5-1/Operations/IntelligenceOps/SOP-IO_ELICITATION_DISCIPLINE_001.md`](../v3.0/Admin/O5-1/Operations/IntelligenceOps/SOP-IO_ELICITATION_DISCIPLINE_001.md) | hol\_res\_prc\_elicitation\_discipline\_001 | Holistik Researcher | Per-engagement |
| SOP-IO\_RELIABILITY\_GRADING\_001 | [`v3.0/Admin/O5-1/Operations/IntelligenceOps/SOP-IO_RELIABILITY_GRADING_001.md`](../v3.0/Admin/O5-1/Operations/IntelligenceOps/SOP-IO_RELIABILITY_GRADING_001.md) | hol\_res\_prc\_reliability\_grading\_001 | Holistik Researcher | Per-engagement |
| SOP-IO\_INTELLIGENCE\_REPORT\_001 | [`v3.0/Admin/O5-1/Operations/IntelligenceOps/SOP-IO_INTELLIGENCE_REPORT_001.md`](../v3.0/Admin/O5-1/Operations/IntelligenceOps/SOP-IO_INTELLIGENCE_REPORT_001.md) | hol\_res\_prc\_intelligence\_report\_001 | Holistik Researcher | Per-engagement (24h post-engagement filing) |

7.3 Engagement Operations (Initiative I66 P3)

| SOP ID | File | process\_id | role\_owner | cadence |
| :---- | :---- | :---- | :---- | :---- |
| SOP-ENG\_DISCOVERY\_QUESTIONNAIRE\_001 | [`v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md`](../v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md) | hol\_eng\_prc\_discovery\_questionnaire\_001 | Holistik Researcher | Per-engagement |
| SOP-ENG\_PROPOSAL\_001 | [`v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_PROPOSAL_001.md`](../v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_PROPOSAL_001.md) | hol\_eng\_prc\_proposal\_001 | Brand Manager | Per-engagement |
| SOP-ENG\_ENGAGEMENT\_DESIGN\_001 | [`v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md`](../v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md) | hol\_eng\_prc\_engagement\_design\_001 | Holistik Researcher | Per-engagement (multi-cell only) |

7.4 Brand Legal Operations (Initiative I66 P3)

| SOP ID | File | process\_id | role\_owner | cadence |
| :---- | :---- | :---- | :---- | :---- |
| SOP-LEGAL\_TRADEMARK\_MONITORING\_001 | [`v3.0/Admin/O5-1/People/Legal/SOP-LEGAL_TRADEMARK_MONITORING_001.md`](../v3.0/Admin/O5-1/People/Legal/SOP-LEGAL_TRADEMARK_MONITORING_001.md) | hol\_lgl\_prc\_trademark\_monitoring\_001 | Legal Counsel | Quarterly |
| SOP-LEGAL\_IP\_REGISTER\_MAINTENANCE\_001 | [`v3.0/Admin/O5-1/People/Legal/SOP-LEGAL_IP_REGISTER_MAINTENANCE_001.md`](../v3.0/Admin/O5-1/People/Legal/SOP-LEGAL_IP_REGISTER_MAINTENANCE_001.md) | hol\_lgl\_prc\_ip\_register\_mtnce\_001 | Legal Counsel | Quarterly |
| SOP-TRADEMARK\_NAMING\_GOVERNANCE\_001 | [`v3.0/Admin/O5-1/People/Legal/SOP-TRADEMARK_NAMING_GOVERNANCE_001.md`](../v3.0/Admin/O5-1/People/Legal/SOP-TRADEMARK_NAMING_GOVERNANCE_001.md) | hol\_lgl\_prc\_trademark\_naming\_governance\_001 | Legal Counsel | Per-introduction |

7.5 People Operations (Initiative I66 P3)

| SOP ID | File | process\_id | role\_owner | cadence |
| :---- | :---- | :---- | :---- | :---- |
| SOP-PEOPLE\_FOUNDER\_BIO\_001 | [`v3.0/Admin/O5-1/People/SOP-PEOPLE_FOUNDER_BIO_001.md`](../v3.0/Admin/O5-1/People/SOP-PEOPLE_FOUNDER_BIO_001.md) | tbi\_ppl\_prc\_founder\_bio\_mtnce\_001 | Talent | Quarterly |

