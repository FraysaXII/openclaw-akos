---
sop_id: SOP-IO_ELICITATION_DISCIPLINE_001
title: Elicitation Discipline
version: 1.0
status: active
classification: canonical
access_level: 5
register: internal
language: en
process_id: hol_res_prc_elicitation_discipline_001
role_owner: Holistik Researcher
role_parent_1: O5-1
area: Research
entity: Holistika
governance:
  - D-IH-66-F (IntelligenceOps SOPs)
  - D-IH-66-M (dual-register contract)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
audit_methodology_source:
  - US Army FM 2-22.3 chapter 6 (Approach Techniques, public release; adapted, not literal)
sister_sops:
  - SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001
  - SOP-IO_RELIABILITY_GRADING_001
  - SOP-IO_INTELLIGENCE_REPORT_001
---

# SOP-IO_ELICITATION_DISCIPLINE_001 — Elicitation Discipline

> **Internal-register SOP.** Governs how Holistika designs the per-engagement elicitation plan: choice of approach techniques, discovery questions, listening-protocol checklist, post-engagement follow-up cadence. Sister to SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001 (the input) and SOP-IO_INTELLIGENCE_REPORT_001 (the output).

## 1. Purpose and scope

Elicitation is the **act of gathering insight from a counterparty during a real-time interaction**. It is distinct from intelligence collection (broader concept including pre-engagement OSINT) and from intelligence reporting (post-engagement structured output).

The elicitation plan governs:

- **Which approach technique** is chosen for the engagement.
- **Which discovery questions** are asked, in what order, with what listening-protocol.
- **What follow-up cadence** is committed to in-engagement.

Out of scope: any elicitation that occurs without the counterparty's understanding that we are in a professional research / business engagement. Pretext, surveillance, recording without consent — all explicitly out of scope (see SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT §1.3).

## 2. Inputs

| Input | Source |
|:---|:---|
| Counterparty baseline reality assessment | SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT output |
| Engagement type (pitch, discovery, advisory, partner-fit, recruiter, ENISA evidence) | Engagement trigger |
| Engagement time-budget | Engagement trigger (calendar invite duration) |
| Voice tier and translation-rule set | Baseline assessment §"engagement-design implication" |

## 3. Approach technique selection

Per FM 2-22.3 chapter 6 (adapted), four approach techniques apply to commercial research engagements:

### 3.1 Direct interrogation

**What it is**: structured questioning where the counterparty's answers are taken at face value, without inference or pattern-matching against other sources.

**When to use**: regulatory or legal contexts where the counterparty's *literal* statement is the deliverable (e.g., ENISA evidence body; legal-counsel discovery). Almost never appropriate for commercial-research engagements.

**Risk**: counterparty reads as adversarial; they shut down or perform.

### 3.2 Direct elicitation (default)

**What it is**: structured questioning where the counterparty's answers are interpreted in context — both the literal statement and the surrounding behaviour (tone, hesitation, follow-up). Default for almost all engagements.

**When to use**: investor pitches, customer discovery, advisor onboarding, partner-fit, recruiter conversations.

**Risk**: requires real-time inference; mistakes get encoded.

### 3.3 Indirect elicitation (anchored on a peer)

**What it is**: structured questioning where the question references a peer or comparator rather than asking directly about the counterparty's own situation. Surfaces information that direct elicitation cannot.

**When to use**: when direct elicitation is plausibly defensive (e.g., asking an investor about their portfolio failures directly is harder than asking what their colleagues' portfolio failure mode tends to be); when the counterparty has a strong public position they need to reconcile with their actual posture.

**Risk**: can be read as evasive if mishandled.

### 3.4 Provocation (deliberate counter-position)

**What it is**: stating a deliberate counter-position to the counterparty's expected view to surface their actual reasoning.

**When to use**: rarely; for advisor-tier or repeat-customer engagements where rapport is high enough to absorb the friction; for ENISA-style review where the regulatory body explicitly invites adversarial questioning.

**Risk**: high. Damages rapport with first-time counterparties. Always pre-decided, never improvised.

## 4. Discovery question design

### 4.1 Question structure

Discovery questions are organised in **5 sections** (per the elicitation templates):

- **Section A — Frame-setting** (no extraction; signals discipline).
- **Section B — Direct elicitation** (extracts the counterparty's current operating posture).
- **Section C — Indirect elicitation** (extracts the counterparty's view of us by reflection).
- **Section D — Reverse-elicitation** (signals competence; extracts disqualification signals).
- **Section E — Closing** (extracts residual concerns; locks the next step).

### 4.2 Per-question discipline

Each question must:

- Be **specific enough** that a generic answer is harder than a specific one.
- Reference an **observable** rather than an opinion ("what's a deal that surprised you in execution" is observable; "what's your investment philosophy" is opinion).
- Avoid **leading** ("what's the failure mode you see most often" is non-leading; "do you agree that founders fail most often because of X" is leading).
- Have an **expected answer space** that's pre-thought-out — if every answer to the question would be useful, the question is too generic.

### 4.3 Order discipline

- Section A first (always — opens the conversation with our framing, not theirs).
- Sections B / C / D ordering depends on baseline assessment posture: defensive counterparties get B → C → D; open counterparties can take D → B → C.
- Section E last (always — counterparty must leave with the next-step lock).

## 5. Listening-protocol checklist

During the engagement, the agent or operator running elicitation:

1. **Notes literal answers** (what they said).
2. **Notes inferential answers** (what their tone / hesitation / follow-up revealed beyond the literal).
3. **Flags contradiction** (where their answer here contradicts their declared posture or a previous answer).
4. **Flags surprise** (where their answer is meaningfully different from the baseline assessment's prediction).
5. **Holds the question budget** — does not skip Section E to fit the time-box; Section E is non-negotiable.

## 6. Post-engagement follow-up cadence

In-engagement, commit to a follow-up cadence:

- **Always**: a follow-up email within 24h thanking the counterparty + confirming key points.
- **Sometimes**: a deck companion / proposal / research brief within 5-10 working days.
- **Rarely**: an immediate-next-day deliverable (only when the engagement explicitly required it).

The post-engagement intelligence report (per SOP-IO_INTELLIGENCE_REPORT_001) is filed within 24h, regardless of follow-up commitments.

## 7. Quality discipline

### 7.1 Anti-patterns

- **Improvised provocation** — using §3.4 without pre-decision. Always pre-plan if a provocation is in scope.
- **Section-collapse** — skipping Section A (frame-setting) to "save time"; almost always damages the engagement.
- **Listen-to-respond, not listen-to-understand** — formulating the next question while the counterparty is still answering. Hold silence between question and response by 2-3 seconds.
- **Confirmation seeking** — asking a question whose only acceptable answer is "yes". Re-frame as observable.

### 7.2 Quality gates

The elicitation plan is reviewed before the engagement against these gates:

1. Does the chosen approach technique match the baseline-assessment voice tier and translation-rule set?
2. Do the discovery questions cover all 5 sections, or has a section been skipped?
3. Are there at least 1-2 reverse-elicitation questions in Section D, or has the section been collapsed into Section B?
4. Is the follow-up cadence specific (24h email + 5-10d deliverable) or generic ("we'll be in touch")?

## 8. Cross-references

- [`SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md`](SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md) — input
- [`SOP-IO_RELIABILITY_GRADING_001.md`](SOP-IO_RELIABILITY_GRADING_001.md) — sibling
- [`SOP-IO_INTELLIGENCE_REPORT_001.md`](SOP-IO_INTELLIGENCE_REPORT_001.md) — output
- Elicitation templates under `docs/wip/intelligence/_templates/`
- D-IH-66-F (IntelligenceOps SOPs) in `docs/wip/planning/66-brand-vision-ops-sweep/decision-log.md`
