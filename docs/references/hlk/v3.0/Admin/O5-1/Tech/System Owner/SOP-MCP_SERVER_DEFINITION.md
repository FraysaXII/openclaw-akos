STANDARD OPERATING PROCEDURE

* Item Name: MCP server definition and governance  
* Item Number: SOP-MCP_SERVER_DEFINITION  
* Process Registry ID: SOP-MCP_SERVER_DEFINITION  
* Object Class: Guideline & Procedure  
* Confidence Level: Safe  
* Security Level: 2 (Internal Use)  
* Entity Owner: HLK Tech Lab  
* Area Owner: Tech  
* Associated Workstream: HLK Infrastructure and DevOPS (env_tech_prj_4)  
* Version: 0.1  
* Revision Date: 2026-04-20  

---

## Purpose

Establish vault anchor for **Model Context Protocol** server definitions, tool registration, and configuration governance referenced from `process_list.csv`.

## Scope

Covers MCP servers used by Holistika engineering and agent surfaces; excludes vendor MCPs outside Holistika configuration control.

## Procedure (v0.1)

* **Trigger:** New MCP server or tool surface.  
* **Action:** Document tool names, auth model, and data residency; align with HTTP API inventory in [SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md](SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md) where overlap exists.  
* **Output:** v1.0 expansion tracked in `docs/wip/planning/15-hlk-api-lifecycle-governance/reports/`.

## Roles

**CTO / System Owner:** Approves new MCP exposure; **DevOPS:** operational deployment.

## Promotion to v1.0

Complete detailed procedures, examples, and review checklist; update **Version** and **Revision Date**.
