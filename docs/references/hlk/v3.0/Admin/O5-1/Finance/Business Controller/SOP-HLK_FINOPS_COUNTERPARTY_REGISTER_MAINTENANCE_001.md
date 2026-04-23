STANDARD OPERATING PROCEDURE

* Item Name: FINOPS counterparty register maintenance  
* Item Number: SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001  
* Process Registry ID: thi_finan_dtp_303 (primary); workstream thi_finan_ws_4  
* Object Class: Guideline & Procedure  
* Confidence Level: High  
* Security Level: 2 (Internal Use)  
* Entity Owner: Think Big  
* Area Owner: Finance — Business Controller  
* Associated Workstream: FINOPS and counterparty economics (thi_finan_ws_4)  
* Version: 1.0  
* Revision Date: 2026-04-23  

---

Table of Contents

* 1.0 Description  
* 2.0 Purpose  
* 3.0 Scope  
* 4.0 Procedure  
* 5.0 Roles and Responsibilities  
* 6.0 Supabase mirror and access control  
* 7.0 Stripe bridge and FDW read plane  
* 8.0 Phase C boundary (monetary facts)  
* 9.0 Addendum  

---

## 1.0 Description

This SOP governs the **canonical FINOPS counterparty register**: [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../../../../compliance/FINOPS_COUNTERPARTY_REGISTER.csv). The register holds **commercial counterparty metadata** for **vendors, customers, and partners** (classification, ownership, process linkage, document pointers)—**not** monetary amounts, invoices, or ledger lines. It joins to [`process_list.csv`](../../../../../compliance/process_list.csv) (`thi_finan_*` processes), [`baseline_organisation.csv`](../../../../../compliance/baseline_organisation.csv) (`role_name`), optionally [`COMPONENT_SERVICE_MATRIX.csv`](../../../../../compliance/COMPONENT_SERVICE_MATRIX.csv) (`component_id`), and [`REPOSITORIES_REGISTRY.md`](../../../Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) (`repo_slug`).

## 2.0 Purpose

* Maintain a **single SSOT** for counterparty master data under the **CFO / Business Controller** chain.  
* Enable **governed sync** to Postgres via `compliance.finops_counterparty_register_mirror` for server-side applications (e.g. Holistika ERP).  
* Enforce **SOC posture**: no secrets or production amounts in git; **server-only** database access.

## 3.0 Scope

**In scope:** Counterparty rows (`counterparty_type` = vendor | customer | partner), billing and revenue classification fields per type, data sensitivity (`pci_phi_pii_scope`), contract **pointers**, renewal review dates, linkage to Finance processes.

**Out of scope:** Production **financial amounts** in CSV or public repo; card data; raw invoice payloads. Operational monetary facts belong in **Phase C** tables under schema **`finops`** (Postgres only), after **Legal and entity readiness** and CFO alignment—see process **`thi_finan_dtp_306`**.

## 4.0 Procedure

### 4.1 Column contract and schema authority

* **SSOT file:** `FINOPS_COUNTERPARTY_REGISTER.csv` per [PRECEDENCE.md](../../../../../compliance/PRECEDENCE.md).  
* **Schema authority:** `FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES` in `akos/hlk_finops_counterparty_csv.py`. Do not add or reorder columns without updating that module, the validator, mirror DDL, and this SOP.  
* **Encoding:** UTF-8; Unix line endings preferred in git.

### 4.2 Adding or updating rows

* **Trigger:** New counterparty, contract renewal, classification change, or periodic review (`thi_finan_dtp_307`).  
* **Action:** Assign a stable **`counterparty_id`** (lowercase slug; never recycle after retirement).  
* **Action:** Set `counterparty_type` and populate **type-specific** columns (`service_category` / `billing_model` for vendor and partner spend; `commercial_segment` / `revenue_model` for customers—use `na` where the validator requires).  
* **Action:** Set `process_item_id` to a **`thi_finan_*`** process that owns the relationship (typically `thi_finan_dtp_303`–`307` or `thi_finan_dtp_309`).  
* **Action:** Set `role_owner` to a valid `role_name` in `baseline_organisation.csv`.  
* **Action:** Set `pci_phi_pii_scope` and `confidence_level` (1–3 per [confidence_levels.md](../../../../../compliance/confidence_levels.md)).  
* **Output:** Row ready for validation.

### 4.3 Validation gate

* **Trigger:** Before every merge that touches the register.  
* **Action:** Run **`py scripts/validate_hlk.py`** (includes **`validate_finops_counterparty_register.py`**).  
* **Output:** PASS/FAIL; fix FKs, enums, or duplicate `counterparty_id` before merge.

### 4.4 Supabase mirror sync (operator)

* **Trigger:** After a merged git commit that changes the CSV.  
* **Precondition:** DDL applied: `compliance.finops_counterparty_register_mirror` (see [`supabase/migrations/`](../../../../../../../supabase/migrations/README.md)).  
* **Action:** Generate upserts:  
  `py scripts/sync_compliance_mirrors_from_csv.py --finops-counterparty-register-only --output /tmp/finops_counterparty_upsert.sql`  
  or full profile **`py scripts/verify.py compliance_mirror_emit`**.  
* **Action:** Review SQL; apply in staging first per [`operator-sql-gate.md`](../../../../../../wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md).  
* **Action:** Use **`service_role`** or database connection from a **trusted server** only—never expose mirror access to browser clients (see §6).

### 4.5 Escalation

* **Material classification or counterparty risk changes:** escalate to **CFO** per **`thi_finan_dtp_305`**.  
* **Entity / legal readiness for financial facts:** follow **`thi_finan_dtp_306`** and [FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md](../../../People/Legal/FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md).

## 5.0 Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| Business Controller | Owns CSV accuracy, classification, and cadence |
| CFO | Approves material changes and Phase C readiness |
| Legal Counsel | Input to entity readiness gate (`thi_finan_dtp_306`) |
| System Owner / DevOps | DDL apply, sync job execution, credential rotation, Stripe FDW posture (`thi_finan_dtp_308`) |

## 6.0 Supabase mirror and access control

* **Table:** `compliance.finops_counterparty_register_mirror`  
* **RLS:** Enabled; **deny** policies for `anon` and `authenticated`; **`service_role`** used for sync and trusted server reads.  
* **Client applications:** Must **not** query this table with the public anon key. Use **server-side** routes (Next.js Route Handlers, Edge Functions with secrets, or backend workers). See initiative handoff: `docs/wip/planning/16-hlk-finops-vendor-ssot/reports/HLK_ERP_FRONTEND_HANDOFF_FINOPS_MIRROR.md` (updated for counterparty naming).

## 7.0 Stripe bridge and FDW read plane

* **`holistika_ops.stripe_customer_link.finops_counterparty_id`** stores the CSV **`counterparty_id`** slug when populated (git authoritative; not a DB FK to the mirror).  
* **Stripe API** is authoritative for payment objects; **`stripe_gtm`** foreign tables (behind **`stripe_gtm_server`**) are a **read projection**. Stewardship: **`thi_finan_dtp_308`** and [`stripe-fdw-operator-runbook.md`](../../../../../../wip/planning/18-hlk-finops-counterparty-stripe/reports/stripe-fdw-operator-runbook.md).

## 8.0 Phase C boundary (monetary facts)

* **Do not** add amount columns to `FINOPS_COUNTERPARTY_REGISTER.csv`.  
* **Future:** Native tables under schema **`finops`** with strict RLS—**Postgres-only**, never git SSOT. Author DDL only after documented Legal/CFO gate.

## 9.0 Addendum

* **SQL proposal reference:** [`sql-proposal-stack-20260417.md`](../../../../../../wip/planning/14-holistika-internal-gtm-mops/reports/sql-proposal-stack-20260417.md) §7.  
* **Initiative 18:** [`master-roadmap.md`](../../../../../../wip/planning/18-hlk-finops-counterparty-stripe/master-roadmap.md).  
* **Related SOP:** [SOP-FOUNDER_COMPANY_FUNDING_001.md](Taxes/SOP-FOUNDER_COMPANY_FUNDING_001.md) (`thi_finan_dtp_302`).
