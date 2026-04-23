STANDARD OPERATING PROCEDURE

* Item Name: HLK component and service matrix maintenance  
* Item Number: SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001  
* Process Registry ID: env_tech_dtp_313  
* Object Class: Guideline & Procedure  
* Confidence Level: High  
* Security Level: 2 (Internal Use)  
* Entity Owner: HLK Tech Lab  
* Area Owner: Tech  
* Associated Workstream: IT Catalog (env_tech_dtp_156); HLK Infrastructure and DevOPS (env_tech_prj_4)  
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

This SOP governs the **canonical component and service inventory** for Holistika-tracked technology: **`docs/references/hlk/compliance/COMPONENT_SERVICE_MATRIX.csv`**. The matrix is the **CTO-chain** analogue of the **COO-chain** `process_list.csv` and the **CPO-chain** `baseline_organisation.csv`: it records **what systems and services exist**, how they are **owned and classified**, how they **integrate**, and where **runbooks and specs** live—without duplicating GitHub file trees or Supabase schemas.

The matrix **joins** to:

* **`baseline_organisation.csv`** via `primary_owner_role`, `secondary_owner_role`, and `escalation_owner_role` (`role_name` values).  
* **`process_list.csv`** via `primary_process_item_id` and `related_process_item_ids` (`item_id` values).  
* **`REPOSITORIES_REGISTRY.md`** via `repo_slug` when a component maps to a tracked repository.

## 2.0 Purpose

* Establish a **single SSOT** for MAROPS, DEVOPS, DATAOPS, PMSMO, LEGOPS, and related stewardship planes (`steward_ops_domain`).  
* Enable **impact analysis** using `depends_on_component_ids` and `parent_component_id`.  
* Support **compliance and SOC** posture via `access_level_data`, `data_classification`, and retention / legal-hold pointers.  
* Keep **operational freshness** visible through `last_verified_date`.

## 3.0 Scope

**In scope:** All production-relevant components, SaaS tools, data platforms, integrations, observability stacks, and client runtimes that Holistika operates or depends on for delivery.

**Out of scope:** Raw application source code (GitHub remains SSOT); detailed row-level database schemas (reference links only); secrets, API keys, and credentials (never stored in this CSV).

## 4.0 Procedure

### 4.1 Column contract and schema authority

* **SSOT file:** `docs/references/hlk/compliance/COMPONENT_SERVICE_MATRIX.csv` per [PRECEDENCE.md](../../../../compliance/PRECEDENCE.md).  
* **Schema authority:** `COMPONENT_SERVICE_FIELDNAMES` in `akos/hlk_component_service_csv.py`. Do not add or reorder columns without updating that module and this SOP.  
* **Encoding:** UTF-8, single header row, Unix line endings preferred in git.

### 4.2 Adding or updating rows

* **Trigger:** New vendor, new environment, architecture change, ownership change, or periodic review.  
* **Action:** Assign a **new** `component_id` (`comp_*` or `svc_*` prefix); **never** recycle ids after retirement.  
* **Action:** Set `lifecycle_status` (`experimental` → `active` → `constrained` → `sunset` → `retired`).  
* **Action:** Fill `steward_ops_domain` for **runbook routing**; align `primary_owner_role` to a real `role_name` in `baseline_organisation.csv`.  
* **Action:** If the component maps to a repo, set `repo_slug` to an existing slug in `REPOSITORIES_REGISTRY.md`.  
* **Output:** Updated CSV row(s) ready for validation.

### 4.3 Validation gate

* **Trigger:** Before every merge that touches the matrix.  
* **Action:** Run **`py scripts/validate_hlk.py`** (includes **`validate_component_service_matrix.py`** when the file is present).  
* **Output:** PASS/FAIL; fix duplicate `component_id` / `component_name`, broken FKs, or invalid enums before merge.

### 4.4 Bulk import (e.g. spreadsheet migration)

* **Trigger:** One-off or periodic import from finance or architecture spreadsheets.  
* **Action:** Use or extend **`scripts/ingest_matriz_componentes_to_matrix.py`** as a **template**; map columns explicitly in the initiative **decision log**.  
* **Action:** **Redact** PII, credentials, and client-confidential URLs before committing.  
* **Output:** Tranche merged with operator approval (see workspace canonical CSV tranche template).

### 4.5 Optional mirrors

* **KiRBe / Supabase / Neo4j:** If a mirror table or graph projection is added, it is **derived** from this CSV; **author here first**, then sync per data architecture SOPs.

## 5.0 Roles and Responsibilities

* **CTO / Tech leadership:** Owns stewardship policy and escalation for the matrix.  
* **System Owner:** Primary operator for row quality, `slo_tier`, and `runbook_link` integrity.  
* **DevOPS / Back-End Developer:** Maintains execution truth for deployments, environments, and integration patterns.  
* **Data Architect / Data Governance:** Validates data platforms and classification fields.  
* **Compliance / Legal (as needed):** Confirms `legal_hold` and `retention_policy_ref` when classification is `restricted` or regulated data is involved.

## 6.0 Addendum

### A.1 Related processes

* **env_tech_dtp_313** — Component and service matrix maintenance (this SOP).  
* **env_tech_dtp_306** — HLK API lifecycle and portfolio governance ([SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md](SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md)).  
* **env_tech_dtp_292** — Codebase catalog and access unification.  
* **env_tech_dtp_293** — Postman internal API catalog.

### A.2 References

* [PRECEDENCE.md](../../../../compliance/PRECEDENCE.md)  
* [HLK_KM_TOPIC_FACT_SOURCE.md](../../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md)  
* [SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md](../../Operations/PMO/SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md) (maintenance pattern parity)  

### A.3 Technology baseline (libraries and language versions)

* **Default SSOT** for dependency versions is **repository artifacts** (lockfiles, `package.json`, `requirements*.txt`, Docker base images)—not a separate spreadsheet.  
* **This matrix** carries **exceptions only**: policy-mandated stacks, vendor-required versions, onboarding gaps, or components **without** a repo row in `REPOSITORIES_REGISTRY.md`.  
* **No bulk ingest** of a dedicated libraries/languages sheet unless a documented driver exists (audit, insurer, regulated customer, or multi-repo drift that lockfiles do not capture).  
* **Forfeit:** a row that cannot be tied to a `repo_slug` **and** has no approved exception reason is **out of scope** for the matrix. (Decision **D-15-6**, Initiative 15 decision-log.)
