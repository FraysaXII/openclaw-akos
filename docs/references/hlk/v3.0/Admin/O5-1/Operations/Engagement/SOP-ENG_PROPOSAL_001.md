---
sop_id: SOP-ENG_PROPOSAL_001
title: Proposal Generation
version: 1.0
status: active
classification: canonical
access_level: 4
language: en
register: external
process_id: hol_eng_prc_proposal_001
role_owner: Brand Manager
role_parent_1: CMO
area: MKT
entity: Holistika
governance:
  - D-IH-66-G (Engagement ops SOPs)
  - D-IH-66-E (service catalog operationalisation)
  - D-IH-66-R (Brand Manager owns proposals as brand-derived deliverables)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
sister_sops:
  - SOP-ENG_DISCOVERY_QUESTIONNAIRE_001
  - SOP-ENG_ENGAGEMENT_DESIGN_001
---

# SOP-ENG_PROPOSAL_001 — Proposal Generation

> Brand-Manager-owned **per-engagement process** that produces the templated proposal after a discovery + elicitation cycle. The proposal is the **external-register** scope + price + timeline document the counterparty signs.

## 1. Purpose

Once Holistika has run discovery (per `SOP-ENG_DISCOVERY_QUESTIONNAIRE_001`) and elicitation (per `SOP-IO_ELICITATION_DISCIPLINE_001`), the next deliverable for a paid engagement is a **proposal**: scope, price posture, timeline, deliverables, success criteria.

This SOP governs how the proposal is produced. It is owned by Brand Manager (per D-IH-66-R) because the proposal is a brand-derived deliverable: voice-tier-aligned per `BRAND_REGISTER_MATRIX.md`, structurally consistent with the deck and dossier templates (P6), and a fundamental brand surface the counterparty reads.

## 2. Cadence

**Per-engagement** (no fixed cadence).

Trigger: counterparty has completed discovery + elicitation cycle and is ready to receive a scoped proposal.

Skip when: engagement is unpaid (advisor / partnership-mutual; uses different doctrine), or engagement is a sub-1-hour consultation with no scope.

## 3. Inputs

- Counterparty baseline reality assessment + intelligence report (per IntelligenceOps SOPs).
- Discovery questionnaire responses (Step 4 of `SOP-ENG_DISCOVERY_QUESTIONNAIRE_001`).
- `SERVICE_OFFERING_CATALOG.md` — the 6×3 matrix; identifies which cells the engagement spans.
- Proposal template (P6 deliverable; until P6 lands, the operator's last-known proposal template under `docs/_assets/advops/` or operator-private storage serves).

## 4. Process steps

### Step 1 — Map engagement to SERVICE_OFFERING_CATALOG cells (15 min)

Identify which cells the proposed engagement spans (single-cell or multi-cell). Common patterns per `SERVICE_OFFERING_CATALOG.md` §"How counterparties enter the matrix":

- Investor-thesis path: 2A → 3A → 6A.
- SME-operator path: 1A → 1B → 5C.
- Foresight-led path: 4A → 3A → 4C.
- Tech-led path: 5C → 1C → 6C.
- Hybrid: documented per-engagement.

### Step 2 — Select voice tier and language (5 min)

Per `BRAND_REGISTER_MATRIX.md`:

- Tier-1 (academic-formal) for investor / advisor / ENISA proposals.
- Tier-2 (practical-operational) for customer-SME / partner / hybrid-operational proposals.
- Tier-2 (technical-rigorous) for engineering-led HLK Tech Lab proposals.

Per language: EN / ES / FR per counterparty preference, applying respective `BRAND_*_PATTERNS.md` rules.

### Step 3 — Tailor proposal sections (60-120 min)

Standard 7-section proposal structure:

1. **Counterparty understanding** — translates the internal baseline reality to "what we observe about your situation".
2. **Proposed scope** — per-cell mapping into `SERVICE_OFFERING_CATALOG`; explicit scope-in / scope-out.
3. **Methodology** — how the engagement will run; references the four methodology pillars (Process Engineering, Business Engineering, Factor Combination, Foresight) where relevant.
4. **Timeline + milestones** — phase-gated, with explicit operator-pause-point analogs (deliverable handoffs the counterparty signs off on).
5. **Pricing posture** — scoped (fixed) / embedded (continuous) / transformational (large multi-cell). Specifics live in operator-private storage; the proposal references the posture, not the line items.
6. **Success criteria** — concrete, measurable, time-bound.
7. **About Holistika + founder bio** — references the canonical founder bio per `SOP-PEOPLE_FOUNDER_BIO_001`, audience-tailored FAQ entries.

### Step 4 — Drift-gate + brand canon review (10 min)

Run `validate_brand_jargon.py` on the proposal draft (or manual review against `BRAND_JARGON_AUDIT.md` §4 if operator-private). Run `validate_brand_baseline_reality_drift.py` to confirm no internal-register tokens leak. Voice-tier check against `BRAND_REGISTER_MATRIX.md`.

### Step 5 — Deliver (10 min)

Render to PDF (preferred for paid engagements). Deliver via the channel the counterparty has indicated (email attachment / shared document / DocuSign for signature-ready proposals). Lock the follow-up call (proposal walkthrough; never async-only delivery for paid engagements).

### Step 6 — Track-record update (5 min)

Once the proposal is signed (or rejected), update the operator-private engagement-tracking doc. Signed proposals contribute to founder bio anonymised track-record (per `SOP-PEOPLE_FOUNDER_BIO_001`) on next quarterly cycle.

## 5. Outputs

- Sent proposal (PDF / shared doc / DocuSign).
- Locked walkthrough call.
- Engagement-tracking entry.

## 6. Anti-patterns

- **Template-overload.** Sending a 30-page proposal for a 2-week engagement. Proposal length scales with engagement size; pad-by-template is unprofessional.
- **Pricing line-item leakage.** Including detailed pricing line items in the proposal text (vs. posture + reference). Detailed pricing belongs in operator-private storage.
- **Missing scope-out.** Proposals that don't explicitly say "we will not do X" are guaranteed to grow scope mid-engagement.
- **Internal-register leakage.** Same anti-pattern as discovery questionnaire; the proposal is external-register.

## 7. Cross-references

- [`SERVICE_OFFERING_CATALOG.md`](../../Marketing/Brand/SERVICE_OFFERING_CATALOG.md) — 6×3 service matrix.
- [`SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md`](SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md) — predecessor SOP.
- [`SOP-ENG_ENGAGEMENT_DESIGN_001.md`](SOP-ENG_ENGAGEMENT_DESIGN_001.md) — multi-cell-engagement governance.
- [`SOP-PEOPLE_FOUNDER_BIO_001.md`](../../People/SOP-PEOPLE_FOUNDER_BIO_001.md) — bio canonical referenced in §7 of every proposal.
- D-IH-66-E (service catalog), D-IH-66-G (Engagement ops SOPs), D-IH-66-R (Brand Manager owns proposals).
