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
* To provide a clear workflow for updating the central process graph database (`process_list_1` or its successors) with new or modified process information.

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
* **Action:** Each item is modeled as a new row for the master process list (`process_list_1.csv`). Key attributes such as `item_id`, `item_name`, `item_granularity`, `item_parent_1`, `role_owner`, `entity`, and `area` must be defined.  
* **Output:** A set of new, validated rows ready for addition to the master process list CSV.

4.3. SOP Documentation

* **Trigger:** The process has been modeled.  
* **Action:** The Process Owner or a designated technical writer (e.g., from the PMO) creates a formal SOP document (like this one) that describes the process in detail. The `item_name` and `item_id` from the process model should be referenced in the SOP's metadata.  
* **Output:** A finalized SOP document, stored in the official knowledge repository (e.g., Confluence, SharePoint, Git).

4.4. Process Data Ingestion & Update

* **Trigger:** The new process rows have been added to the master CSV and the SOP is complete.  
* **Action:** A Data Engineer or DevOps Engineer executes the necessary procedures to update the Neo4j database. This involves:  
  1. Adding the new rows to the master `process_list_1.csv` file.  
  2. Executing an idempotent Cypher script (using `UNWIND` and `MERGE`) to create the new nodes and relationships in the graph database without affecting existing data.  
* **Output:** The Neo4j graph is updated to reflect the new process structure.

4.5. Review & Maintenance

* **Trigger:** A scheduled review (e.g., annually) or a change in the underlying process.  
* **Action:** The Process Owner reviews the SOP and its corresponding graph representation for accuracy. If changes are needed, the process returns to step 4.2.  
* **Output:** An up-to-date and validated process model and documentation.

5.0 Roles and Responsibilities

* **Process Owner / Area Owner:** Responsible for identifying the need for a process, defining its scope, and ensuring its accuracy over time.  
* **Data Architect:** Responsible for guiding the modeling of the process into the graph structure and ensuring it adheres to established patterns.  
* **PMO / Technical Writer:** Responsible for drafting and maintaining the formal SOP documentation.  
* **Data Engineer / DevOps Engineer:** Responsible for the technical execution of updating the master data file and the Neo4j database.

6.0 Addendum

A.1: Process Definition Template (for `process_list_1.csv`)

| item\_id | item\_name | item\_granularity | item\_parent\_1 | role\_owner | entity | area | ... |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| (unique\_id) | (Descriptive Name) | (project/workstream/process/task) | (Name of parent item) | (Role responsible) | (Holistika/Think Big/etc.) | (Ops/Tech/MKT/etc.) | ... |

