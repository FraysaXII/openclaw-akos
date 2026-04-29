STANDARD OPERATING PROCEDURE

* Item Name: Adviser transcript redaction
* Item Number: SOP-HLK_TRANSCRIPT_REDACTION_001
* Process Registry ID: hol_peopl_dtp_304 (primary); workstream hol_peopl_ws_1 (Compliance Methodology)
* Object Class: Guideline & Procedure
* Confidence Level: High
* Security Level: 2 (Internal Use)
* Entity Owner: Holistika
* Area Owner: People — Compliance
* Associated Workstream: Compliance Methodology (hol_peopl_ws_1); cross-cuts External Adviser Engagement (hol_opera_ws_5)
* Version: 1.0
* Revision Date: 2026-04-28

---

Table of Contents

* 1.0 Description
* 2.0 Purpose
* 3.0 Scope
* 4.0 Procedure
* 5.0 Roles and Responsibilities
* 6.0 Substitution rules
* 7.0 Forward-only history posture
* 8.0 Off-repo originals
* 9.0 Addendum

---

## 1.0 Description

This SOP governs **redaction of adviser call transcripts** before any markdown file lands in the public git repository. It builds on the **GOI/POI register** ([SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001](SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md)): every private organisation or person referenced in a transcript must be substituted by its `GOI-*` / `POI-*` `ref_id`, and originals are kept off-repo per Compliance.

## 2.0 Purpose

* Prevent **public exposure** of real names, contact details, and personal paths in committed markdown.
* Make redaction **deterministic** and **auditable** via the GOI/POI register and the [`scripts/redact_transcripts_p2.py`](../../../../../../../scripts/redact_transcripts_p2.py) helper.
* Document the **forward-only** policy (decision **D-CH-2** in [`21-hlk-adviser-engagement-and-goipoi/decision-log.md`](../../../../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/decision-log.md)) and its re-evaluation triggers.

## 3.0 Scope

**In scope:** Markdown transcripts (e.g. `.mp3.md`, `.m4a.md`) in [`docs/references/hlk/business-intent/delete-legal-transcripts/`](../../../../../business-intent/delete-legal-transcripts/) and any future call notes destined for in-repo storage; YAML frontmatter `source` paths; speaker labels and inlined names.

**Out of scope:** Raw audio (`.mp3` / `.m4a`); commit history rewriting (`git filter-repo` is **deferred** per D-CH-2); off-repo originals.

## 4.0 Procedure

### 4.1 Ingestion gate

* **Trigger:** New transcript or call note arrives.
* **Action:** Confirm every private organisation or person mentioned has a `ref_id` in [`GOI_POI_REGISTER.csv`](../../../../../compliance/GOI_POI_REGISTER.csv). If not, add the row first (per [SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001](SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md)).
* **Action:** Apply substitutions (§6.0) before the file is staged with `git add`.
* **Action:** Replace any `source:` YAML path that points at an operator's local filesystem with `source: <off-repo per SOP-HLK_TRANSCRIPT_REDACTION_001>`.

### 4.2 Helper script

* **Script:** `py scripts/redact_transcripts_p2.py --apply --report <path>` for the historical pushed transcripts (idempotent; safe to rerun).
* **Output:** Updated markdown with a redaction header comment; report under `docs/wip/planning/21-hlk-adviser-engagement-and-goipoi/reports/p2-redaction-diff.md`.

### 4.3 Validation gate

* **Trigger:** Before merge.
* **Action:** Run `py scripts/validate_hlk.py` (passes); inspect that no real names re-appeared (visual review of the diff is required).
* **Action:** Run `rg -n "(Carmi|Jorge|Ayúdate Pymes)" docs/` (or the canonical name list per the operator's redaction notes) and confirm zero matches outside the GOI/POI register itself.

### 4.4 Binary masquerading files

* **Trigger:** A transcript-folder file with a `.md` extension that is actually a zip / `.docx` archive (detected by encoding probe in the helper script).
* **Action:** Either rename the file to `.docx` and verify it contains no surplus identifying metadata, or delete it (operator preference; original kept off-repo). Document the action in the next P-2 redaction report.

## 5.0 Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| Compliance | Owns substitution rules, sensitivity bands, off-repo identity register |
| Legal Counsel | Reviews `confidential` / `restricted` transcripts; signs off on retention |
| PMO | Routes transcripts into ADVOPS workstreams; updates evidence matrix |
| System Owner / DevOps | Maintains helper script and `validate_hlk.py` integration |

## 6.0 Substitution rules

Apply the following minimum rules; operator may extend per call:

| Surface | Action |
|:--------|:-------|
| Real first or last name of a person | Replace with the `POI-*` `ref_id` from the register |
| Real organisation / firm name (private) | Replace with the `GOI-*` `ref_id` |
| Email addresses | Strip; never persist |
| Phone numbers | Strip or generalise (`<phone redacted>`) |
| Local filesystem paths in YAML frontmatter | Replace with the off-repo placeholder |
| Public organisations (e.g. ENISA, public authorities, named regulators) | **Keep** (when modeled with `is_public_entity = true`) |
| Industry references (e.g. SaaS vendor names that are public knowledge and contextual only) | **Keep** unless they imply a private commercial relationship |

Once substitution is applied, the file's body must contain **no** un-modeled real name. The redaction header (`<!-- Initiative 21 / P2 redacted forward-only ... -->`) is a marker only and is added automatically by the helper.

## 7.0 Forward-only history posture

Per **D-CH-2** in [`decision-log.md`](../../../../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/decision-log.md):

* **Current tip is redacted; commit history is not rewritten.**
* **Re-evaluation trigger:** A `restricted` POI is later identified in commit history without an explicit register row flagged for public reference, **or** counsel issues a privilege-protection demand. In that case, plan a separate `git filter-repo` initiative with operator approval and force-push window.

## 8.0 Off-repo originals

Operator-managed Drive (or equivalent) holds:

* Raw audio (`.mp3`, `.m4a`) recordings.
* Unredacted markdown transcripts (pre-redaction).
* Real-name ↔ `ref_id` identity mapping table.

This SOP intentionally does **not** specify a single off-repo tool; only the constraint that nothing in this list ever appears in the public git repository.

## 9.0 Addendum

* **Initiative reference:** [`docs/wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md`](../../../../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md).
* **Related SOP:** [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md).
* **Helper script:** `scripts/redact_transcripts_p2.py` (one-shot; safe to delete after retention review).
