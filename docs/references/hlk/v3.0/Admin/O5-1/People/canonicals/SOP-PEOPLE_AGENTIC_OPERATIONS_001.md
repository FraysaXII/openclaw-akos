---
title: SOP — People Agentic Operations
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_AGENTIC_OPERATIONS_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - People Operations Lead
last_review: 2026-05-16
last_review_by: People Operations Lead
last_review_decision_id: D-IH-80-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-79-A
  - D-IH-79-F
  - D-IH-79-L
  - D-IH-80-D
status: active
register: internal
linked_canonicals:
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - ETHICAL_AGENTIC_BOUNDARIES.md
  - PEOPLE_DESIGN_PATTERN_LIBRARY.md
linked_runbooks:
  - scripts/peopl_agentic_knowledge_test.py
linked_processes:
  - tbi_peopl_dtp_agentic_ops_mtnce_001
companion_to:
  - SOP-PEOPLE_AGENTIC_OPERATIONS_001.addendum.md
cadence: scheduled
cadence_schedule: monthly
cadence_secondary: event_triggered
cadence_secondary_trigger: substantive canonical revision in agent scope
---

# SOP — People Agentic Operations

## Purpose

Operationalise the People-side oversight of agents in our employ. This SOP carries the cadence — knowledge-test rhythm, collaborator training, escalation when an agent's confidence drops — that keeps the agentic doctrine governed in practice rather than only on paper.

This SOP is paired with the runbook at [`scripts/peopl_agentic_knowledge_test.py`](../../../../../../scripts/peopl_agentic_knowledge_test.py) per [`akos-executable-process-catalog.mdc`](../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 (paired SOP plus runbook). Either a human or an agent acting as a role owner can run it via the SOP; the runbook is the unattended path. Both surfaces are SSOT for the same process.

## Scope

In scope:

- Hybrid knowledge-test cadence (ratified at I79 P3a inline-ratify gate, 2026-05-15): a small set of knowledge-base lookup tasks that an agent must answer correctly to remain in good standing for its named role. Two complementary triggers — a scheduled monthly baseline that catches drift during idle periods, and an event-triggered run on substantive canonical revision in the agent's scope that catches drift at the source during high-work periods.
- Onboarding cadence for new collaborators (human or agent) joining a process where an agent shares the role.
- Escalation when an agent fails a knowledge-test, when its self-reported confidence drops below the threshold for a step, or when its work product is flagged by audit.
- Adjustment cadence for the canonicals when the knowledge-test reveals a doctrine drift (the canonical is unclear, not the agent).

Out of scope:

- Specific framework or tool selection — that is Tech Lab's surface, governed by [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md).
- Infrastructure deployment, monitoring, version pinning — that is Tech Lab's surface, governed by [`SOP-TECH_AGENTIC_INFRA_001.md`](../../Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md).
- Ethical red lines — those are Ethics' surface, governed by [`ETHICAL_AGENTIC_BOUNDARIES.md`](../Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md). This SOP cites the anchor; it does not author the rules.

## Inputs

- The list of agents currently in our employ, with the named role each holds.
- The set of canonicals each agent is expected to honour (typically: the manifesto + the agentic doctrine + the area-specific SOPs that govern its named role).
- The knowledge-test bank for each agent's named role (a small set of question-answer pairs grounded in the canonicals; see [`scripts/peopl_agentic_knowledge_test.py`](../../../../../../scripts/peopl_agentic_knowledge_test.py)).
- The previous knowledge-test result for each agent, if any.

## Steps

### 1. Schedule the cadence (hybrid: monthly baseline + event-triggered)

People Operations Lead schedules the monthly knowledge-test baseline in advance. The session is a fixed slot — same day-of-month, same window. Predictability matters: the agents are not surprised, and the operator can set aside the time.

A second trigger fires off-cadence: whenever a canonical in an agent's scope is revised substantively (the canonical owner flags the edit as substantive, not a typo or formatting fix), People Operations Lead schedules an event-triggered knowledge-test for that agent against the revised canonical. The event-triggered run replaces the next monthly run for that agent if it falls within the same fortnight; otherwise both run. The two triggers cover the operator's framing — the monthly baseline keeps idle agents tested, the event trigger keeps high-work agents tested at the moment doctrine changes underneath them.

### 2. Identify the test scope per agent

For each agent in scope, gather the canonicals the agent is expected to honour and the knowledge-test bank for the agent's named role. The knowledge-test bank is a small set (between five and ten) of question-answer pairs whose answers are in the canonicals. Questions are short, answers are unambiguous, and every answer has a citation to a specific canonical line range.

When a canonical has changed since the last cadence, the test bank is updated. New questions reflect the new canonical content. Old questions whose answers have changed are revised; old questions whose canonicals have not changed remain in the bank for continuity.

### 3. Run the knowledge-test session

Run the harness at [`scripts/peopl_agentic_knowledge_test.py`](../../../../../../scripts/peopl_agentic_knowledge_test.py). The harness presents each question to the agent, records the agent's answer, and emits a structured result file under `docs/wip/planning/79-people-manifesto-and-pattern-library/reports/knowledge-tests/<YYYY-MM>/<agent-name>.md`.

The harness reads canonicals as plain text and writes results as plain text. The why behind that choice (zero-framework on purpose; methodology-version agnostic; portable across infrastructure changes) lives in [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.addendum.md`](SOP-PEOPLE_AGENTIC_OPERATIONS_001.addendum.md) §A.

### 4. Score the results

For each question, the operator marks the agent's answer as one of three:

- **Pass** — the agent's answer matches the canonical answer.
- **Fail** — the agent's answer contradicts the canonical answer or is missing.
- **Drift** — the agent's answer is plausible but the canonical itself is ambiguous on the point. Drift is a People signal that the canonical needs revision; it is not a fail against the agent.

A passing session is one where every question is marked Pass or Drift, with no Fails, and at most one Drift per session.

### 5. Apply the verdict

If the session passes, the agent continues to hold its named role. The result file is committed and serves as the audit record for the month.

If the session fails (any Fail mark), the agent is suspended from the failing question's covered scope. People Operations Lead opens an escalation per the next step. The operator may decide to keep the agent active for unrelated steps; that decision is recorded in the result file.

If the session shows Drift, People Operations Lead opens a canonical-revision ticket. The drift is a signal that the doctrine has aged or was unclear; the cadence will not improve until the canonical is revised. The revision follows the standard People canonical-edit process and the cross-area breakthrough propagation pattern when the change is substantive.

### 6. Escalation

When an agent fails a knowledge-test, when its self-reported confidence drops below the documented threshold for a step in any of its named SOPs, or when its work product is flagged by an audit channel:

- People Operations Lead is the first responder. They review the failing artifact, classify the failure (knowledge gap / canonical drift / red-line violation / out-of-scope action), and route accordingly.
- Knowledge gaps route back to the knowledge-test cadence and to canonical revision when needed.
- Canonical drift routes to the canonical owner for revision.
- Red-line violations route immediately to Ethics Advisor per [`ETHICAL_AGENTIC_BOUNDARIES.md`](../Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md). The agent is suspended from the relevant scope until Ethics signs off.
- Out-of-scope actions route to the role-design surface: the SOP is updated to either include the action explicitly (if the action was correct) or forbid it explicitly (if the action was wrong).

Escalation outcomes are recorded in the agent's result file for the month. Patterns across months feed back into the People design pattern library when they reveal a cross-process breakthrough.

### 7. Onboarding cadence

When a new collaborator (human or agent) joins a process where an agent shares the role, People Operations Lead runs a short onboarding session with the joining party plus the existing role holders (human and agent). The session covers:

- The agent's named role and the canonicals it honours.
- The escalation routing for failures.
- The knowledge-test cadence and the joining party's first session date.
- The cross-discipline interfaces relevant to the new collaborator's area.

The onboarding session does not have its own paired runbook; it is People-facilitated and captured in a meeting note rather than a structured artifact.

## Outputs

- One result file per agent per month under `docs/wip/planning/79-people-manifesto-and-pattern-library/reports/knowledge-tests/<YYYY-MM>/<agent-name>.md`.
- Canonical-revision tickets when Drift is observed.
- Escalation records folded into the result file.
- Updates to the agent's named-role SOP when out-of-scope actions reveal scope ambiguity.

## Failure modes

- **Cadence skipped.** Mitigation: the cadence is a `scheduled` row in `process_list.csv`; when the date passes without execution, the process_list row's last-run column flags it as overdue. The event-triggered secondary cadence does not have a date stamp; the canonical-revision commit log doubles as its audit trail (every substantive revision should have a knowledge-test result file inside the same fortnight).
- **Test bank stale.** Mitigation: at every canonical edit that touches an agent's scope, People Operations Lead reviews the test bank and revises affected questions.
- **Drift accumulating.** Mitigation: more than one Drift in a single session is a signal that the canonical is significantly aged; People Operations Lead schedules a focused revision sprint.
- **Agent and role drift apart.** Mitigation: when the agent's underlying infrastructure changes (Tech Lab upgrade), People runs an off-cycle knowledge-test before the next scheduled session to confirm the upgrade has not changed the agent's behaviour against the doctrine.

## Cross-references

- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](HOLISTIKA_AGENTIC_DOCTRINE.md) — the doctrine this SOP operationalises.
- [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) — the People manifesto framing both.
- [`ETHICAL_AGENTIC_BOUNDARIES.md`](../Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md) — red-line escalation target.
- [`scripts/peopl_agentic_knowledge_test.py`](../../../../../../scripts/peopl_agentic_knowledge_test.py) — paired runbook.
- [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](PEOPLE_DESIGN_PATTERN_LIBRARY.md) — paired SOP and runbook pattern this SOP instantiates.
- [`SOP-TECH_AGENTIC_INFRA_001.md`](../../Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md) — sibling SOP at Tech Lab; covers infrastructure operations.
