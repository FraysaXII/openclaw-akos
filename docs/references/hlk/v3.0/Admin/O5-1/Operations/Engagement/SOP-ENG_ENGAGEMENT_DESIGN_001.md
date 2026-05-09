---
sop_id: SOP-ENG_ENGAGEMENT_DESIGN_001
title: Engagement Design (Multi-Cell)
version: 1.0
status: active
classification: canonical
access_level: 4
language: en
register: external (deliverable-facing) + internal (design-side)
process_id: hol_eng_prc_engagement_design_001
role_owner: Holistik Researcher
role_parent_1: O5-1
area: Research
entity: Holistika
governance:
  - D-IH-66-G (Engagement ops SOPs)
  - D-IH-66-E (service catalog operationalisation)
  - D-IH-66-R (Holistik Researcher owns multi-cell methodology orchestration)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
sister_sops:
  - SOP-ENG_DISCOVERY_QUESTIONNAIRE_001
  - SOP-ENG_PROPOSAL_001
---

# SOP-ENG_ENGAGEMENT_DESIGN_001 — Engagement Design (Multi-Cell)

> Holistik-Researcher-owned **per-engagement process** that governs the design of engagements spanning multiple cells of the `SERVICE_OFFERING_CATALOG.md` 6×3 matrix. Single-cell engagements skip this SOP; multi-cell engagements run through it before the proposal lands.

## 1. Purpose

When a counterparty engagement spans multiple service-domain × delivery-mode cells (e.g., Process Engineering × R&S → Process Engineering × Think Big → Tech Lab Integrations × HLK Tech Lab — the SME-operator path), the engagement is by definition phased. This SOP governs:

- **Cell-to-cell transitions** — where one cell ends and the next begins; what artefact bridges them.
- **Per-phase deliverable lock** — each phase has an explicit signed-off deliverable before the next begins.
- **Per-phase voice-tier consistency** — voice register may shift between cells (e.g., R&S Tier-1 → Think Big Tier-2); this SOP keeps the shift intentional rather than accidental.
- **Multi-cell economics** — each phase has its own scope + pricing posture; consolidation savings (vs running phases as independent engagements) are quantified explicitly.

## 2. Cadence

**Per-engagement** (no fixed cadence).

Trigger: discovery + elicitation cycle reveals the engagement spans ≥ 2 cells.

Skip: single-cell engagements where the proposal directly captures the engagement design without need for phased structure.

## 3. Inputs

- Counterparty intelligence report (per `SOP-IO_INTELLIGENCE_REPORT_001`).
- Discovery questionnaire responses.
- `SERVICE_OFFERING_CATALOG.md` — the 6×3 matrix; the 5 representative paths in §"How counterparties enter the matrix" are pattern references.

## 4. Process steps

### Step 1 — Confirm multi-cell scope (10 min)

Verify the engagement spans ≥ 2 cells of the 6×3 matrix. If single-cell, skip this SOP and proceed directly to `SOP-ENG_PROPOSAL_001`.

### Step 2 — Map the path (20 min)

Identify the path through the matrix. Pick the closest representative pattern from `SERVICE_OFFERING_CATALOG.md` §"How counterparties enter the matrix" (or document a hybrid path explicitly).

For each cell in the path:

- Phase number (1 / 2 / 3 / …).
- Cell coordinate (row × column; e.g., 2A = Business Engineering × Holistika R&S).
- Phase deliverable (the artefact that closes this phase).
- Voice tier for this phase (Tier-1 R&S vs Tier-2 Think Big vs Tier-2 HLK Tech Lab).
- Phase duration estimate.
- Phase-to-phase transition trigger.

### Step 3 — Design transition artefacts (20 min)

Each phase-to-phase transition needs an artefact that **bridges** the previous phase's deliverable to the next phase's input. Common transition artefacts:

- **R&S → Think Big**: research brief → operational playbook → executable program.
- **R&S → HLK Tech Lab**: research brief → technical spec → architecture document.
- **Think Big → HLK Tech Lab**: GTM-system design → technical-marketing infrastructure spec.
- **Methodology cell → Capability building cell**: deliverable + workshop content + handoff guide.

Document the transition artefact's structure + voice-tier + acceptance criteria.

### Step 4 — Pricing posture per phase (15 min)

Per phase, decide pricing posture: scoped / embedded / transformational. Per `SERVICE_OFFERING_CATALOG.md` §"Pricing posture", the posture lives in the proposal abstractly; line-item pricing is operator-private. Calculate the multi-cell consolidation discount (engagement run as single multi-phase program vs as 3 independent engagements).

### Step 5 — Document the engagement design (30 min)

Produce a **design document** (internal-register; lives under `docs/wip/intelligence/<engagement-slug>/engagement-design.md` or operator-private storage). Sections:

1. Counterparty + multi-cell path.
2. Per-phase scope + deliverable + duration.
3. Transition artefacts.
4. Per-phase voice tier.
5. Pricing posture per phase + consolidation savings.
6. Acceptance criteria per phase.
7. Risk register specific to this engagement design.

The design document feeds the proposal generation (`SOP-ENG_PROPOSAL_001` Step 3) — the proposal is the external-register expression of this internal-register design.

### Step 6 — Operator review (variable)

Multi-cell engagements warrant operator (CBO/O5-1) review before the proposal lands. The operator either approves the design as-is, requests revisions to phase structure / pricing posture, or escalates concerns about engagement viability.

## 5. Outputs

- Engagement design document (Step 5).
- Operator-approved phase structure.
- Hand-off to `SOP-ENG_PROPOSAL_001` for proposal generation.

## 6. Anti-patterns

- **Phase collapse** — designing a multi-cell engagement as if it were single-cell. Always preserve phase-deliverable lock; without it, scope grows uncontrollably.
- **Voice-tier drift** — changing voice tier mid-phase rather than at a phase transition. Voice tier should shift only at phase boundaries, never mid-deliverable.
- **Pricing-posture mismatch** — using one posture (e.g., scoped) for a phase that's structurally embedded (continuous-presence). Pricing posture follows phase structure, not preference.
- **Transition-artefact omission** — running phase 1 → phase 2 without an explicit transition artefact. Without it, the next phase's inputs are unclear and rework follows.

## 7. Cross-references

- [`SERVICE_OFFERING_CATALOG.md`](../../Marketing/Brand/SERVICE_OFFERING_CATALOG.md) — 6×3 matrix + 5 representative paths.
- [`SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md`](SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md) — predecessor SOP.
- [`SOP-ENG_PROPOSAL_001.md`](SOP-ENG_PROPOSAL_001.md) — successor SOP.
- [`BRAND_REGISTER_MATRIX.md`](../../Marketing/Brand/BRAND_REGISTER_MATRIX.md) — voice tier rules.
- D-IH-66-E (service catalog), D-IH-66-G (Engagement ops SOPs), D-IH-66-R (Holistik Researcher owns multi-cell orchestration).
