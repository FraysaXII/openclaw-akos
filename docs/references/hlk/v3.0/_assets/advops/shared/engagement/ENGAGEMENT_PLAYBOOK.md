---
status: active
classification: canonical
access_level: 4
language: en
register: mixed
artifact_kind: engagement_playbook
role_owner: Holistik Researcher
area: Research
entity: Holistika
process_id: hol_eng_prc_engagement_design_001
linked_initiative: I66
governance:
  - SOP-ENG_ENGAGEMENT_DESIGN_001
  - SOP-ENG_PROPOSAL_001
  - SERVICE_OFFERING_CATALOG.md
last_review: 2026-05-09
---

# Engagement Playbook

> Operator-facing playbook for turning a discovery conversation into a scoped engagement. The external sections can be adapted for clients; the design notes remain internal.

## 1. Entry Conditions

Run this playbook when:

- The client has completed a discovery conversation.
- The work spans more than one service-catalog cell, or the cell is uncertain.
- The client needs a clear proposal, not an open-ended advisory thread.

Skip when:

- The work is a short advisory call.
- The scope is a single obvious deliverable.
- Legal or budget authority is absent.

## 2. Engagement Path Selection

| Path | Typical trigger | Cell path | Primary owner |
|:---|:---|:---|:---|
| Investor thesis | Model, unit economics, path to scale | 2A → 3A → 6A | Holistik Researcher |
| SME operator | Process pain, repeated rework, poor handoff | 1A → 1B → 5C | Brand Manager + CTO |
| Foresight-led | Regulatory or market uncertainty | 4A → 3A → 4C | Holistik Researcher |
| Tech-led | Integration or AI system need | 5C → 1C → 6C | CTO |
| Hybrid | Multiple constraints | custom | CBO/O5-1 |

## 3. Internal Design Note

Use the following structure before writing the proposal:

```markdown
# Engagement Design — [Client / project]

## Path
[Chosen path + why]

## Phase Design
| Phase | Cell | Deliverable | Acceptance criteria | Duration |
|:---|:---|:---|:---|:---|

## Transition Artifacts
- Phase 1 → 2:
- Phase 2 → 3:

## Risks
- Scope risk:
- Data/access risk:
- Decision-maker risk:
- Handoff risk:

## Proposal Translation
[How the internal design becomes external language]
```

## 4. Phase Rules

- Every phase ends with a named deliverable.
- Every transition has an artifact that moves work from one delivery mode to the next.
- Voice register can shift at a phase boundary, never randomly inside a phase.
- Commercial posture follows the phase structure, not preference.
- Handoff is designed from phase 1, not added at the end.

## 5. Client-Facing Rhythm

The client-facing explanation is:

1. We understand the operating reality.
2. We map the work into phases.
3. Each phase has a clear output.
4. Each output unlocks the next phase.
5. The final handoff makes the system usable by the client team.

## 6. Required Attachments

- Proposal generated from `PROPOSAL_TEMPLATE.md`.
- Statement of Work generated from `LEGAL_TEMPLATE_SOW.md`.
- NDA or DPA when discovery or implementation involves sensitive information.
- Founder bio variant from `FOUNDER_BIO.md` when credibility context is needed.

## 7. Closure

At the end of the engagement, file:

- Outcome review.
- What changed.
- What remains open.
- What should happen next.
- Which template or SOP should be updated from what was learned.
