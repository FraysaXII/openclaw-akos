STANDARD OPERATING PROCEDURE

* Item Name: External Adviser Engagement (ADVOPS plane)
* Item Number: SOP-EXTERNAL_ADVISER_ENGAGEMENT_001
* Process Registry ID: hol_opera_ws_5 (workstream); hol_opera_dtp_311 (disciplines maintenance)
* Object Class: Guideline & Procedure
* Confidence Level: High
* Security Level: 2 (Internal Use)
* Entity Owner: Holistika
* Area Owner: Operations — PMO
* Associated Workstream: External Adviser Engagement (`hol_opera_ws_5`); cross-cuts Legal, Fiscal, IP, Banking, Certification, Notary
* Version: 1.0
* Revision Date: 2026-04-28

---

Table of Contents

* 1.0 Description
* 2.0 Purpose
* 3.0 Scope
* 4.0 Procedure
* 5.0 Roles and Responsibilities
* 6.0 Discipline catalogue
* 7.0 Mirror and access control
* 8.0 Adding a new discipline or program
* 9.0 Addendum

---

## 1.0 Description

This SOP defines the **External Adviser Engagement plane** (ADVOPS) — a cross-program scaffold for managing **external advisers** (Legal, Fiscal, IP, Banking, Certification, Notary, …) parallel to MKTOPS / FINOPS / OPS / TECHOPS. It is the operating contract for the **disciplines lookup**, the **router**, the **counsel handoff package** structure, and the linkage from ADVOPS rows to **GOI/POI** ([`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001`](../../People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md)).

## 2.0 Purpose

* Establish a **single, scalable** plane for external-adviser engagements that does not contaminate Legal, Finance, or Compliance trees with per-engagement schemas.
* Make discipline routing **data-driven** (CSV row-level changes, not new tables) so adding accounting, employment, regulatory affairs, etc. is trivial.
* Enforce **DAMA-grade SSOT** for adviser questions, filed instruments, and stakeholder references via FK relationships into the disciplines lookup, GOI/POI register, and `process_list.csv`.

## 3.0 Scope

**In scope:** Disciplines lookup, ADVOPS open questions register (P4), ADVOPS filed instruments register (P5), counsel handoff package per-discipline sections, router, plane integration with PMO portfolio.

**Out of scope:** Lead intake (MKTOPS), counterparty metadata for non-adviser commercial relationships (FINOPS), payments and financial ledger (Stripe / `finops.*`), engineering team management.

## 4.0 Procedure

### 4.1 Disciplines lookup maintenance

* **SSOT file:** [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../../../compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv) per [`PRECEDENCE.md`](../../../../../compliance/PRECEDENCE.md).
* **Schema authority:** `ADVISER_ENGAGEMENT_DISCIPLINES_FIELDNAMES` in `akos/hlk_adviser_disciplines_csv.py`.
* **Rules:**
  * `discipline_id` is `lowercase_snake` (e.g. `legal`, `fiscal`, `accounting`); never recycle after retirement.
  * `discipline_code` is **3 uppercase letters** (e.g. `LEG`, `FIS`, `ACC`); used as the middle slug of question / instrument ids (see §6.0).
  * `canonical_role` must resolve in [`baseline_organisation.csv`](../../../../../compliance/baseline_organisation.csv).
  * `default_process_item_id` must resolve in [`process_list.csv`](../../../../../compliance/process_list.csv).
* **Validation gate:** `py scripts/validate_hlk.py` (PASS).

### 4.2 Open questions register (Initiative 21 / P4)

* **SSOT file:** `ADVISER_OPEN_QUESTIONS.csv` (graduates from [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](../../People/Legal/FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md)).
* **`question_id` scheme:** `Q-<DISC3>-<NNN>` (e.g. `Q-LEG-001`).
* **Each row** carries discipline FK, `program_id`, optional `poi_ref_id` / `goi_ref_id`, `status`, `target_date`, evidence pointer.
* **Vault MD** is a **derived view**: human read-out grouped by discipline. Updated manually from CSV unless a render script is introduced.

### 4.3 Filed instruments register (Initiative 21 / P5)

* **SSOT file:** `FOUNDER_FILED_INSTRUMENTS.csv` (graduates from [`FOUNDER_FILED_INSTRUMENT_REGISTER.md`](../../People/Legal/FOUNDER_FILED_INSTRUMENT_REGISTER.md)).
* **`instrument_id` scheme:** `INST-<DISC3>-<SLUG>-<YYYY>`.

### 4.4 Counsel handoff package

* The single entrypoint remains [`EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`](../../People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md). Per-discipline sections are added in P4 alongside the questions CSV.
* Export deliverable: `py scripts/export_adviser_handoff.py --discipline all --format md` (P7).

### 4.5 Stakeholder integration

* Stakeholder rows in [`TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](TOPIC_PMO_CLIENT_DELIVERY_HUB.md) reference `POI-*`/`GOI-*` `ref_id`s from the GOI/POI register.

## 5.0 Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| PMO | Plane owner; disciplines lookup, router, integration with project portfolio |
| Legal Counsel | Review legal / IP / banking / notary discipline rows and instruments |
| Compliance | GOI/POI register, transcript redaction, sensitivity bands |
| Business Controller | Fiscal discipline rows, fiscal questions and filings |
| System Owner / DevOps | Mirror DDL, sync execution, helper scripts |

## 6.0 Discipline catalogue

Initial seed (see CSV for the source of truth):

| discipline_id | code | display_name | canonical_role | entrypoint process |
|:--------------|:----:|:-------------|:---------------|:-------------------|
| `legal` | LEG | Legal & Corporate | Legal Counsel | `thi_legal_dtp_302` |
| `fiscal` | FIS | Fiscal & Tax | Business Controller | `thi_finan_dtp_302` |
| `ip` | IPT | IP & Trademark | Legal Counsel | `thi_legal_dtp_303` |
| `banking` | BNK | Banking | Legal Counsel | `thi_legal_dtp_302` |
| `certification` | CRT | Startup Certification | Compliance | `hol_peopl_dtp_302` |
| `notary` | NOT | Notary | Legal Counsel | `thi_legal_dtp_302` |

## 7.0 Mirror and access control

* **Tables:** `compliance.adviser_engagement_disciplines_mirror` (P3), and (P4–P5) `compliance.adviser_open_questions_mirror`, `compliance.founder_filed_instruments_mirror`.
* **RLS:** Same posture as other compliance mirrors — deny `anon` and `authenticated`; `service_role` only.
* **Sync:** `py scripts/sync_compliance_mirrors_from_csv.py --adviser-disciplines-only` (and the per-CSV flags introduced in P4 / P5).

## 8.0 Adding a new discipline or program

* **Trigger:** New adviser type emerges (e.g. `accounting`, `employment`, `data_protection`) **or** a new founder/program engagement (e.g. `PRJ-HOL-MOTHER-2027`).
* **Action:**
  1. Add a row to `ADVISER_ENGAGEMENT_DISCIPLINES.csv` (no schema change). Validate.
  2. (Optional) Add corresponding GOI/POI rows for new firm or persons.
  3. (For a new program) Pick a `program_id` (`PRJ-<E>-<TOPIC>-<YYYY>`) and reuse the same registers for that program.
  4. Update [`EXTERNAL_ADVISER_ROUTER.md`](EXTERNAL_ADVISER_ROUTER.md) routing section.
* **Output:** Plane absorbs the new discipline / program with **zero** schema migrations.

## 9.0 Addendum

* **Initiative reference:** [`docs/wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md`](../../../../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md).
* **Cursor rule:** [`.cursor/rules/akos-adviser-engagement.mdc`](../../../../../../../.cursor/rules/akos-adviser-engagement.mdc).
* **Counsel handoff package:** [`EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`](../../People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md).
