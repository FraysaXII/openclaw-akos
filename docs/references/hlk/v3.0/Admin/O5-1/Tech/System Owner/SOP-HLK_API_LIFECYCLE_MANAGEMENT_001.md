STANDARD OPERATING PROCEDURE

* Item Name: HLK API lifecycle and portfolio governance  
* Item Number: SOP-HLK_API_LIFECYCLE_MANAGEMENT_001  
* Process Registry ID: env_tech_dtp_306  
* Object Class: Guideline & Procedure  
* Confidence Level: High  
* Security Level: 2 (Internal Use)  
* Entity Owner: HLK Tech Lab  
* Area Owner: Tech  
* Associated Workstream: API lifecycle and portfolio (env_tech_ws_api_1)  
* Version: 1.0  
* Revision Date: 2026-04-20  

---

Table of Contents

* 1.0 Description  
* 2.0 Purpose  
* 3.0 Scope  
* 4.0 Procedure  
* 5.0 Roles and Responsibilities  
* 6.0 Addendum  

---

## 1.0 Description

Holistika operates **multiple GitHub repositories** and **managed services** that expose or consume **HTTP APIs**, **webhooks**, **edge functions**, and **partner-facing surfaces**. This SOP defines the **repeatable lifecycle** for designing, documenting, cataloguing, securing, changing, and retiring those APIs across repos.

**Portfolio SSOT** for “what exists” at the component level is **`COMPONENT_SERVICE_MATRIX.csv`** (`api_exposure`, `api_spec_pointer`, joins to `repo_slug`). **Repository membership** and canonical remotes are **`REPOSITORIES_REGISTRY.md`**. **GitHub** remains SSOT for source code and machine-readable specs checked into repos.

## 2.0 Purpose

* Provide **one operating model** for API work across MAROPS, DEVOPS, DATAOPS, PM/SM/OPS, and LEGOPS consumers.  
* Reduce **undocumented** or **unticketed** breaking changes.  
* Align **internal testing** (Postman / composite calls) with **published** contracts.  
* Ensure **vendor and third-party** claims are **attributed** using [source_taxonomy.md](../../../../compliance/source_taxonomy.md).

## 3.0 Scope

**In scope:** First-party REST/HTTP APIs, GraphQL gateways if used, Supabase edge functions, Stripe/Shopify webhooks owned by Holistika stacks, internal BFFs, and **MCP-adjacent** HTTP surfaces (MCP tool definitions remain under **SOP-MCP_SERVER_DEFINITION**).

**Out of scope:** KiRBe ingestion connector specifics (see KiRBe platform processes); pure UI-only pages with no API contract; client proprietary codebases not listed in `REPOSITORIES_REGISTRY.md`.

## 4.0 Procedure

### 4.1 Portfolio inventory

* **Trigger:** New service, new repo, or material architecture change.  
* **Action:** Ensure a **`COMPONENT_SERVICE_MATRIX.csv`** row exists with correct `component_kind`, `api_exposure` (`none` / `internal` / `partner` / `public`), and `api_spec_pointer` (repo-relative path or documented public spec URL pattern).  
* **Action:** If the component maps to GitHub, ensure **`REPOSITORIES_REGISTRY.md`** has a row; set optional **`api_spec_pointer`** / **`api_topic_id`** at repo level when one spec covers the whole repo.  
* **Action:** Execute **env_tech_dtp_307** (tracked repository API surface registration) for new tracked repos.  
* **Output:** Joinable inventory: matrix ↔ registry ↔ Git remote.

### 4.2 Machine-readable specification SSOT

* **Trigger:** API reaches `experimental` or `active` lifecycle in the matrix.  
* **Action:** Maintain **OpenAPI 3.x** or **AsyncAPI** (or platform-native equivalent documented in `api_spec_pointer`) in-repo; prefer **generated-from-code** or **verified** hand-authored specs committed beside services.  
* **Action:** CI SHOULD fail on invalid spec where tooling exists.  
* **Output:** Spec path recorded in matrix and/or registry; consumers can diff versions.

### 4.3 Authentication, authorization, and secrets

* **Trigger:** Any API handling non-public data or privileged actions.  
* **Action:** Follow **Secrets and Token Vault Pattern** (**env_tech_dtp_277**); no long-lived secrets in issue trackers or public READMEs.  
* **Action:** Document rotation and **escalation_owner_role** in the matrix row.  
* **Output:** Operational secrecy and least-privilege alignment.

### 4.4 Internal API catalog and synthetic tests

* **Trigger:** API used by more than one team or repo.  
* **Action:** Maintain collections per **Postman as Internal API Catalog** (**env_tech_dtp_293**), coordinated with **Internal API catalog and consumer registry** (**env_tech_dtp_309**).  
* **Output:** Callable **golden paths** for regression and onboarding.

### 4.5 Versioning, deprecation, and breaking changes

* **Trigger:** Contract change that can break consumers.  
* **Action:** Use semantic versioning or URL versioning as documented in the repo; publish **deprecation** headers or changelog entries.  
* **Action:** Notify consumers listed in **env_tech_dtp_309**; record major milestones in matrix `notes` if needed.  
* **Output:** Controlled sunset path without silent production breakage.

### 4.6 Third-party and vendor APIs

* **Trigger:** Dependency on external SaaS or partner API behavior.  
* **Action:** Record **facts** about limits, guarantees, and pricing-relevant assumptions with citations; classify sources per [source_taxonomy.md](../../../../compliance/source_taxonomy.md).  
* **Action:** Use **Third-party API evidence and attribution** (**env_tech_dtp_312**) and **Feasibility Gate Checklist** (**env_tech_dtp_244**) pointers when validating access early.  
* **Output:** Defensible evidence trail for audits and handovers.

### 4.7 MCP tool surfaces vs HTTP APIs

* **Trigger:** New agent tool or MCP server.  
* **Action:** Define tools under **SOP-MCP_SERVER_DEFINITION**; if the same capability exposes HTTP, cross-link matrix row and MCP SOP so **security review** covers both entry points.

### 4.8 Publishing and redaction

* **Trigger:** Public or partner-facing documentation derived from internal runbooks.  
* **Action:** Apply **SOP-DYNAMIC_DOCUMENT_REDACTION_001** when sensitive paths, tenant names, or internal URLs must not leak.

### 4.9 Incidents and degradation

* **Trigger:** Elevated errors, quota exhaustion, or webhook delivery failure.  
* **Action:** Follow `runbook_link` on the matrix row; escalate via `escalation_owner_role`; post-mortem updates `last_verified_date` and `notes` as needed.

## 5.0 Roles and Responsibilities

* **System Owner:** Owns portfolio coherence, matrix fields for critical platforms, and cross-repo API dependencies.  
* **DevOPS / Back-End Developer:** Owns CI spec checks, Postman catalog hygiene, deployment-time contract gates.  
* **Tech Lead:** Arbitration on versioning and technical debt trade-offs.  
* **PMO:** Client-delivery repo registration and engagement-specific URLs (with Compliance where client data appears).  
* **Compliance:** Classification disputes, public documentation policy.

## 6.0 Addendum

### A.1 Process index (registry ids)

| item_id | item_name |
|---------|-----------|
| env_tech_ws_api_1 | API lifecycle and portfolio |
| env_tech_dtp_306 | HLK API lifecycle and portfolio governance |
| env_tech_dtp_307 | Tracked repository API surface registration |
| env_tech_dtp_308 | Machine-readable API specification SSOT |
| env_tech_dtp_309 | Internal API catalog and consumer registry |
| env_tech_dtp_311 | API versioning deprecation and breaking-change control |
| env_tech_dtp_312 | Third-party API evidence and attribution |
| env_tech_dtp_313 | Component and service matrix maintenance |

### A.2 Pending KiRBe / MADEIRA vault anchors

Numerous **`SOP-*`** rows in `process_list.csv` under KiRBe and MADEIRA await full vault markdown. They remain **registry-true**; expand in dedicated tranches without blocking this SOP.

### A.3 References

* [COMPONENT_SERVICE_MATRIX.csv](../../../../compliance/COMPONENT_SERVICE_MATRIX.csv)  
* [REPOSITORIES_REGISTRY.md](../../../Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md)  
* [HLK_KM_TOPIC_FACT_SOURCE.md](../../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md)  
* [TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md](../../../People/Compliance/TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md)  
* [SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001.md](SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001.md)  
