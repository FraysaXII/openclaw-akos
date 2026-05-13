---
sop_id: SOP-ENG_DISCOVERY_QUESTIONNAIRE_001
title: Discovery Questionnaire Operations
version: 1.0
status: active
classification: canonical
access_level: 4
language: en
register: external (operator-facing; the questionnaire content itself is external register)
process_id: hol_eng_prc_discovery_questionnaire_001
role_owner: Holistik Researcher
role_parent_1: O5-1
area: Research
entity: Holistika
governance:
  - D-IH-66-G (Engagement ops SOPs)
  - D-IH-66-R (sub-mark accountability — no Engagement Manager role; Holistik Researcher owns research-led discovery)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
sister_sops:
  - SOP-ENG_PROPOSAL_001
  - SOP-ENG_ENGAGEMENT_DESIGN_001
  - SOP-IO_ELICITATION_DISCIPLINE_001
---

# SOP-ENG_DISCOVERY_QUESTIONNAIRE_001 — Discovery Questionnaire Operations

> Holistik-Researcher-owned **per-engagement process** that delivers the **external-register** discovery questionnaire to a counterparty. Companion to the **internal-register** elicitation plan (`SOP-IO_ELICITATION_DISCIPLINE_001`).

## 1. Purpose

When Holistika engages a counterparty in discovery (customer-SME engagement, partner-fit conversation, advisor onboarding, ENISA evidence), a **structured discovery questionnaire** is the typical first deliverable. This SOP governs how that questionnaire is produced and delivered.

The questionnaire is **external-register**: per `BRAND_BASELINE_REALITY_MATRIX.md` §3, it is the public-facing translation of the internal elicitation plan. The counterparty sees a professional-looking questionnaire; the elicitation plan is what the agent or operator runs internally during the conversation.

## 2. Cadence

**Per-engagement** (no fixed cadence).

Trigger: any engagement where the counterparty is being asked structured discovery questions before a deliverable is sent.

Skip when: the engagement is a casual networking interaction or a one-shot pitch with no discovery component.

## 3. Inputs

- Counterparty baseline reality assessment (per `SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001`).
- Per-audience template under `docs/wip/intelligence/_templates/elicitation-template-<audience>.md` (one template per of 7 audience classes; investor template shipped in I66 P3, others to be created on first engagement).
- Engagement scope brief.

## 4. Process steps

### Step 1 — Select per-audience template (5 min)

From `docs/wip/intelligence/_templates/`, pick the audience template matching the counterparty class. If a template does not exist for that audience, create it from the investor template pattern (Section A frame-setting + B direct + C indirect + D reverse + E closing).

### Step 2 — Tailor the questionnaire (15-30 min)

Per the baseline reality assessment:

- Replace template placeholders with engagement-specific values.
- Adjust voice register per `BRAND_REGISTER_MATRIX.md` audience row (Tier-1 academic-formal for investors / advisors / ENISA; Tier-2 practical-operational for customer-SME / partners; Tier-2 technical-rigorous for engineering-side recruiter conversations).
- Translate any internal-register vocabulary to external register per `BRAND_BASELINE_REALITY_MATRIX.md` §3.
- Adjust language to per-locale rules per `BRAND_FRENCH_PATTERNS.md` / `BRAND_SPANISH_PATTERNS.md` if engagement is FR / ES.

### Step 3 — Produce the deliverable (15 min)

Render to:

- **PDF** (preferred for formal engagements; investor / advisor / ENISA / partner): use the dossier renderer pipeline if available, or operator-side Pages-to-PDF.
- **Email body** (preferred for customer-SME / recruiter conversations): plain HTML, no attachment.
- **Shared document** (preferred for ongoing-engagement collaboration; iterative revision): Google Docs / Notion link.

### Step 4 — Deliver and lock follow-up cadence (5 min)

In the delivery message: include the questionnaire, set expectations for response timeline (typically 5-10 working days), and lock the follow-up engagement (call to walk through responses, not async-only).

### Step 5 — Companion intelligence-side hand-off (5 min)

Inform the engagement's operator (or self if operator is also Holistik Researcher) that the questionnaire is sent. Hand off to `SOP-IO_ELICITATION_DISCIPLINE_001` — the internal elicitation plan governs the response-walk-through call.

## 5. Outputs

- Sent questionnaire (PDF / email / shared document).
- Locked follow-up call.
- Hand-off to elicitation discipline.

## 6. Anti-patterns

- **Generic-template send.** Sending the un-tailored audience template to a specific counterparty. Always pass through Step 2 tailoring.
- **Async-only fall-through.** Sending the questionnaire and expecting only async written responses. Always lock a follow-up call to walk through.
- **Internal-register leakage.** Forgetting to translate internal-register vocabulary; the questionnaire is **external-register**. Run `validate_brand_baseline_reality_drift.py --consumer-root <engagement-folder>` if uncertain.

## 7. Cross-references

- [`SOP-IO_ELICITATION_DISCIPLINE_001.md`](../IntelligenceOps/SOP-IO_ELICITATION_DISCIPLINE_001.md) — internal-register companion.
- [`SOP-ENG_PROPOSAL_001.md`](SOP-ENG_PROPOSAL_001.md) — successor SOP (after questionnaire + elicitation cycle).
- [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) §3 — translation table.
- [`BRAND_REGISTER_MATRIX.md`](../../Marketing/Brand/BRAND_REGISTER_MATRIX.md) — voice register selection.
- D-IH-66-G (Engagement ops SOPs), D-IH-66-R (no Engagement Manager role).
