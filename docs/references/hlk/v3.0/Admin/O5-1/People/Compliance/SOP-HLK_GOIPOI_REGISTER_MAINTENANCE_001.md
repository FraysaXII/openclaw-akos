STANDARD OPERATING PROCEDURE

* Item Name: GOI/POI register maintenance
* Item Number: SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001
* Process Registry ID: hol_peopl_dtp_303 (primary); workstream hol_peopl_ws_1 (Compliance Methodology)
* Object Class: Guideline & Procedure
* Confidence Level: High
* Security Level: 2 (Internal Use)
* Entity Owner: Holistika
* Area Owner: People — Compliance
* Associated Workstream: Compliance Methodology (hol_peopl_ws_1); cross-cuts External Adviser Engagement (hol_opera_ws_5) and all founder-incorporation streams
* Version: 1.0
* Revision Date: 2026-04-28

---

Table of Contents

* 1.0 Description
* 2.0 Purpose
* 3.0 Scope
* 4.0 Procedure
* 5.0 Roles and Responsibilities
* 6.0 Supabase mirror and access control
* 7.0 Off-repo identity mapping
* 8.0 Privacy bands and sharing labels
* 9.0 Addendum

---

## 1.0 Description

This SOP governs the **canonical GOI/POI register**: [`GOI_POI_REGISTER.csv`](../../../../../compliance/GOI_POI_REGISTER.csv). The register is a **knowledge-architecture dimension** that lets every other vault asset reference **organisations (GOI)** and **persons (POI)** by stable, public-safe `ref_id`s instead of real names.

**GOI** (Group of Interest): organisation, firm, public authority, or other corporate entity referenced by HLK content.

**POI** (Person of Interest): a position-as-a-row reference to a real human counterparty (adviser lead, banker, regulator contact, …). The register holds the **obfuscated display label** and lookup metadata; the **identity mapping** (real name + contact) is kept off-repo per §7.

## 2.0 Purpose

* Maintain a **single SSOT** for organisation and person references used across the founder-incorporation program and all future engagements.
* Make obfuscation **deterministic** and **rebuildable**: any markdown can be regenerated from CSV without ambiguity.
* Enforce **SOC posture**: no real names of private entities or persons in git; no email addresses; no contact strings in `notes`.

## 3.0 Scope

**In scope:** GOI / POI rows used by the canonical vault, ADVOPS plane, founder-program registers, and KM Topic-Fact-Source manifests.

**Out of scope:** Identity mapping (real name ↔ `ref_id`), contact details, calendar invites, raw recordings, or any unobfuscated communications. These live off-repo.

## 4.0 Procedure

### 4.1 Column contract and schema authority

* **SSOT file:** `GOI_POI_REGISTER.csv` per [PRECEDENCE.md](../../../../../compliance/PRECEDENCE.md).
* **Schema authority:** `GOIPOI_REGISTER_FIELDNAMES` in `akos/hlk_goipoi_csv.py`. Do not add or reorder columns without updating that module, the validator, mirror DDL, and this SOP.
* **Encoding:** UTF-8; Unix line endings preferred.

### 4.2 Adding rows

* **Trigger:** A new organisation or position is referenced by counsel handoff, transcripts, vault notes, or PMO hub stakeholder index.
* **Action:** Allocate a stable `ref_id` per the scheme:
  * **POI:** `POI-<DISC3>-<SLUG>-<YYYY>` (e.g. `POI-LEG-ENISA-LEAD-2026`).
  * **GOI:** `GOI-<DISC3>-<SLUG>-<YYYY>` (e.g. `GOI-ADV-ENTITY-2026`).
  * **Slug discipline:** ASCII uppercase + digits + hyphen; never recycle after retirement; year is the year of first capture.
* **Action:** Set `entity_kind` = `person` for POI rows, `organisation` for GOI rows. Validator enforces alignment with prefix.
* **Action:** Set `class`. The validator accepts:
  * Initiative-21 seed set: `external_adviser`, `banking_channel`, `supplier`, `research_benchmark`, `lead`, `client_org`, `collaborator`, `public_authority`, `other`.
  * Initiative-22 P4 extension (multi-program reuse): `client`, `partner`, `investor`, `regulator`, `vendor`, `media`. See §4.7 for when each is preferred.
* **Action:** Set `is_public_entity = true` only when the entity is a public authority or otherwise publicly known and the operator accepts using the real name. Otherwise `false`.
* **Action:** Set `display_name`. For private entities, write a **role-shaped label** (e.g. `"Constitution-desk lead at GOI-BNK-INC-2026"`). Never include surnames, first names, or email addresses.
* **Action:** Set `lens` = `lowercase_snake` describing the analysis lens (e.g. `entity_readiness`, `fiscal_readiness`, `incorporation`, `marketing_benchmark`).
* **Action:** Set `sensitivity` (`public`, `internal`, `confidential`, `restricted`). Validator enforces consistency with `is_public_entity`.
* **Action:** Set `program_id` (e.g. `PRJ-HOL-FOUNDING-2026`) when applicable.
* **Action:** Set `role_owner` to a `role_name` in [`baseline_organisation.csv`](../../../../../compliance/baseline_organisation.csv) and `process_item_id` to a `thi_*` / `hol_*` / `env_*` row in [`process_list.csv`](../../../../../compliance/process_list.csv).
* **Output:** Row ready for validation.

### 4.3 Validation gate

* **Trigger:** Before every merge that touches the register.
* **Action:** `py scripts/validate_hlk.py` (calls `validate_goipoi_register.py`).
* **Output:** PASS/FAIL.

### 4.4 Mirror sync (operator)

* **Trigger:** After a merged commit that changes the CSV.
* **Action:** `py scripts/sync_compliance_mirrors_from_csv.py --goipoi-register-only --output /tmp/goipoi_upsert.sql` and review.
* **Action:** Apply via Supabase MCP `execute_sql` from `service_role`. Never expose this mirror to the browser.

### 4.5 Updates and retirements

* **Trigger:** Display label refinement, sensitivity change, role reassignment, retirement.
* **Action:** Edit existing row. **Do not** recycle `ref_id` after retirement. Mark retirement in `notes` and freeze the row.
* **Action:** Re-run validators and mirror sync.

### 4.6 Document references

* All canonical vault markdown that mentions a private entity or person **must** use the `ref_id` as the primary handle. Display labels may be inlined for readability but must come from the register.
* The transcript redaction SOP ([`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](SOP-HLK_TRANSCRIPT_REDACTION_001.md)) details the substitution rules for transcripts and call notes.

### 4.7 Class taxonomy (extended for multi-program reuse, Initiative 22 P4 / D-IH-5)

The register is **engagement-keyed** (D-CH-8, Initiative 21): a single dimension serves all programs. Choose `class` to match the **functional relationship**, not the program scope.

| `class` | When to use | Typical sensitivity | FK / cross-reference |
|:--------|:-----------|:--------------------|:---------------------|
| `external_adviser` | Engaged adviser firm or named adviser (Legal, Fiscal, IP, Banking, Certification, Notary) | `internal` | `ADVISER_ENGAGEMENT_DISCIPLINES.csv`, `ADVISER_OPEN_QUESTIONS.csv`, `FOUNDER_FILED_INSTRUMENTS.csv` |
| `banking_channel` | Constitution-desk bank, IBAN-providing institution, banking desk lead | `confidential` | `FOUNDER_FILED_INSTRUMENTS.csv` (via `counterparty_goi_ref_id`) |
| `client` | Active or contracted **client** of Holistika under a delivery program | program-keyed via `program_id` | future MKTOPS / delivery registers |
| `partner` | Strategic partner, channel partner, system-integrator partner | `internal` | future partnership registers |
| `investor` | Angel, VC, fund, public-funding agency operating in **investor capacity** (private flow) | `confidential` | future fundraising registers |
| `regulator` | Public regulator authority (CNMC, AEAT, mercantile registry, …) — usually `is_public_entity = true` | `public` | public-affairs / compliance trackers |
| `vendor` | Paid commercial supplier (FINOPS counterparty); FK target for FINOPS workflows | `internal` | `FINOPS_COUNTERPARTY_REGISTER.csv` (`counterparty_id`) |
| `supplier` | Legacy synonym for `vendor` (kept for Initiative-21 rows); prefer `vendor` for new entries | `internal` | same as `vendor` |
| `lead` | Inbound lead or prospect not yet under contract | `internal` | future MKTOPS lead-intake flows |
| `media` | Press, podcast host, public-relations contact (private flow) | `internal` | future MKTOPS / brand registers |
| `research_benchmark` | Reference organisation cited for benchmarking; not under contract | `public` or `internal` | research synthesis docs |
| `client_org` | Legacy synonym for `client` (kept for Initiative-21 rows); prefer `client` for new entries | program-keyed | same as `client` |
| `collaborator` | Non-paid collaborator, advisor with no formal contract, contributor to research | `internal` | research / community trackers |
| `public_authority` | Catch-all for public authority bodies that are also `is_public_entity = true` | `public` | regulators, ministries, certification bodies |
| `other` | Use only when no class above fits; flag for taxonomy review | `internal` | — |

**Disambiguation tips.** Prefer `vendor` over `supplier` and `client` over `client_org` for new rows; the legacy synonyms remain valid so Initiative-21 seed rows do not break. A row may be both `regulator` and `public_authority` semantically — pick the more specific (`regulator`) and set `is_public_entity = true`. A `media` contact who is also an `investor` is recorded with the **primary engagement** class; the secondary relationship goes in `notes` and gets its own row only when sensitivity differs.

### 4.8 Onboarding a new program (Initiative 22 P4 / D-IH-5)

When a new program (e.g. `PRJ-HOL-KIRBE-2027`) is registered in `process_list.csv`, follow this sub-flow before adding any GOI/POI rows scoped to it:

1. **Allocate `program_id`.** It MUST match the canonical `item_id` for the program-level row in `process_list.csv` (`item_granularity = project`). The Initiative 22 layout convention requires this id to be unambiguous across the vault.
2. **Confirm or create the role-folder program subfolder** under each role that owns casework for the program — e.g. `Admin/O5-1/People/Legal/programs/<program_id>/README.md`. The subfolder README links into `compliance/README.md` and lists the program-scoped docs (Initiative 22 P3).
3. **Confirm or create the `_assets/` program subfolder.** Topic bundles for the program go under `_assets/<plane>/<program_id>/<topic_id>/`. Use `shared` only when the asset is genuinely cross-program (Initiative 22 P2).
4. **Allocate ref_ids with the right slug discipline.** For private parties scoped to the program, follow `<PREFIX>-<DISC3>-<SLUG>-<YYYY>` where `<YYYY>` is the year of first capture (often the program year). Slugs never overlap across programs in the canonical vault.
5. **Pick a `class`** from the extended taxonomy in §4.7 — most program-onboarding rows for a delivery program will use `client`, `partner`, `vendor`, `external_adviser`, or `regulator`.
6. **Choose default sensitivity** per §8.0; `confidential` is the default for new private parties until the operator confirms downgrade is safe.
7. **Update the off-repo identity mapping** (§7.0) before staging any commit; never commit a row whose mapping cell is empty.
8. **Run** `py scripts/validate_hlk.py` and `py scripts/sync_compliance_mirrors_from_csv.py --goipoi-register-only --count-only` before merging.

The new program's first GOI/POI rows should be merged in a single tranche so reviewers can spot-check sensitivity bands and class choices in one diff.

## 5.0 Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| Compliance | Owns CSV accuracy, slug discipline, sensitivity bands, redaction substitution |
| PMO | Maintains stakeholder cross-references in TOPIC_PMO_CLIENT_DELIVERY_HUB.md (manual view) |
| Legal Counsel | Reviews `confidential` / `restricted` rows tied to legal counterparties |
| System Owner / DevOps | Mirror DDL apply, sync execution, credential rotation |

## 6.0 Supabase mirror and access control

* **Table:** `compliance.goipoi_register_mirror`
* **RLS:** Enabled; deny policies for `anon` and `authenticated`; `service_role` for sync and trusted server reads.
* **Client applications:** Must not query this table with a public anon key.

### 6.1 `service_role` quarterly rotation procedure (Initiative 26 P2 / D-IH-26-D)

**Cadence:** quarterly (last business day of each quarter) unless an incident triggers an earlier rotation.

**Operator runbook:**

1. **Open Supabase dashboard** → Project → Settings → API.
2. **Roll** the `service_role` key (Supabase generates a new value; the old key revokes within ~60 seconds).
3. **Update the operator credential store** that backs the `user-supabase` MCP server (typically `~/.openclaw/.env` `SUPABASE_SERVICE_ROLE_KEY=…`, or a 1Password / Vault entry the operator references). **Never commit the value to git.**
4. **Smoke the rotation**: run `py scripts/probe_compliance_mirror_drift.py --emit-sql`, paste the SELECT into MCP `execute_sql` (which now uses the new key), save the JSON to `artifacts/probes/mirror-drift-<YYYYMMDD>.json`, then `py scripts/probe_compliance_mirror_drift.py --verify`. PASS confirms the new key works end-to-end.
5. **Log the rotation** in [`docs/wip/planning/26-hlk-ops-hardening/decision-log.md`](../../../../../wip/planning/26-hlk-ops-hardening/decision-log.md) as a one-line row: `<YYYY-MM-DD>` / `<operator initials>` / `service_role rotated; smoke probe PASS`.

**Rollback** if the new key is rejected by MCP after step 4:

* In dashboard → Settings → API, re-roll the key (generates a fresh value; the **rejected** new key revokes).
* Re-run step 3 with the fresh key.
* Re-run step 4 to confirm.

**Calendar reminder pattern:** add a recurring quarterly reminder in the operator's calendar — last business day of Q1/Q2/Q3/Q4. Industry baseline cadence; longer windows accumulate exposure surface, shorter windows produce operator fatigue.

**SOC**: per [`akos-governance-remediation.mdc`](../../../../../../.cursor/rules/akos-governance-remediation.mdc) §"SOC / Security": never log secret values. The runbook refers to the dashboard path and the credential store path only — the key value itself is never written to git, terminal history (use the dashboard copy-to-clipboard, then paste into the credential store editor), or Slack/email.

## 7.0 Off-repo identity mapping

The **real-name ↔ ref_id** mapping is operator-managed and must remain off-repo. Recommended forms:

* A private spreadsheet in operator-controlled storage with columns `ref_id`, `legal_name`, `email`, `phone`, `notes`.
* OR a private vault entry encrypted at rest.

This SOP intentionally does **not** specify a single tool — only the constraint that the mapping never lands in the public git repository.

## 8.0 Privacy bands and sharing labels

| sensitivity | Default sharing label | Examples |
|:------------|:----------------------|:---------|
| `public` | `counsel_ok`, public authorities | ENISA (when modeled as `public_authority`), regulator bodies |
| `internal` | `internal_only` | Adviser firm operating relationship, internal benchmarks |
| `confidential` | `counsel_and_named_counterparty` | Banking-desk relationship, draft instruments |
| `restricted` | bespoke per release | Privileged correspondence, litigation-adjacent material |

When in doubt, escalate to Compliance and Legal before raising the band.

## 9.0 Addendum

* **Initiative reference:** [`docs/wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md`](../../../../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md).
* **Related SOP:** [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](SOP-HLK_TRANSCRIPT_REDACTION_001.md) (transcript redaction, P2).
* **Related SOP:** [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../../Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) (ADVOPS plane).
