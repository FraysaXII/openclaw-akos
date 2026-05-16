---
language: en
status: active
canonical: false
classification: way_of_working
intellectual_kind: risk_register
phase: P0
initiative: INIT-OPENCLAW_AKOS-80
authored: 2026-05-16
last_review: 2026-05-16
role_owner: PMO
ssot: false
companion_to:
  - master-roadmap.md
  - decision-log.md
---

# I80 — Risk Register

> Workspace mirror of I80 risks identified at charter time and during execution. Aligns with [`master-roadmap.md`](master-roadmap.md) §"Risks (preview)".

## R-IH-80-1 — Retrofit body/addendum split judgement varies per agent

**Description.** Different agents could extract different sections to the addendum during retrofit (P4-P5), creating inconsistency across the vault. Without a clear rubric, the body/addendum boundary becomes a matter of taste.

**Likelihood.** Medium. **Impact.** Low (rubric divergence costs review cycles, not data integrity).

**Mitigation.** Codify in `SOP-META_PROCESS_MGMT_001.md` extension at P1 with a 5-row rubric:

1. *Does the executor need this to perform the action?* → body.
2. *Does this name a system, validator, mirror, or cross-area artifact the executor doesn't operate?* → addendum.
3. *Does this carry jargon from another area?* → addendum (unless executor's role natively spans both areas).
4. *Does this require auditor/system-owner context for compliance evidence?* → addendum.
5. *Could a new hire in the executor's role complete the SOP without this?* → addendum if yes.

Single agent lands all P4+P5 retrofits in one session to maintain rubric consistency.

**Status.** Active.

---

## R-IH-80-2 — Stakeholder lenses become stale

**Description.** Lenses written at I80 (Q2 2026) reflect company state at that moment. Without periodic review, they go stale by 2027 (post-funding, post-role-activation, post-regulatory-submission).

**Likelihood.** Medium. **Impact.** Medium (stale lenses create onboarding friction; investor briefings reference outdated material).

**Mitigation.** Annual scheduled review cadence + event_triggered review at major company state changes (Series A close; first regulated client; CEO/CRO role activation; ENISA submission). Process_list row at P2 binds the cadence: `tbi_peopl_dtp_stakeholder_lenses_review_001` (People Operations Lead; cadence_type scheduled annual + event_triggered).

**Status.** Active. Forward-charter to first review at 2027-05-16.

---

## R-IH-80-3 — Inline-ratify craft skill not discovered by other agents

**Description.** Cursor skills require trigger-recognition to be read. Agents authoring AskQuestion may not recognize the trigger and proceed without consulting the skill, missing the quality bar.

**Likelihood.** Medium. **Impact.** Medium (low-quality AskQuestion calls accumulate; operator brainstorm benefit lost).

**Mitigation.** (a) Cursor rule extension at `.cursor/rules/akos-inline-ratification.mdc` cross-references the skill — agents authoring AskQuestion encounter the rule first because rules apply structurally. (b) Skill description carries strong trigger words (*author*, *AskQuestion*, *inline-ratify*, *operator decision*). (c) Future operator audit at I-NN cycle close-outs can spot-check AskQuestion quality and remind agents to consult the skill.

**Status.** Active. P3 deliverable.

---

## R-IH-80-4 — Paired-file convention adds file-count overhead

**Description.** Paired-file addendum default doubles the SOP file count when addenda are present. Some agents/operators may dislike the file ceremony, especially for SOPs that have only a small addendum.

**Likelihood.** Low. **Impact.** Low (file count is cheap; modern editors handle it well).

**Mitigation.** SOP-META extension at P1 explicitly permits the **single-file degenerate case** when an SOP has no addendum-worthy content (body is fully self-sufficient). Paired-file is the **default**, not the **mandate**. Authors may demote a paired SOP to single-file when an addendum review concludes its content belongs in the body or is no longer needed.

**Status.** Active. P1 deliverable.

---

## R-IH-80-5 — Full-vault retrofit (I81) never executes

**Description.** Forward-chartered I81 candidate stub for full v3.0 vault retrofit (~30+ SOPs) might languish without dedicated initiative cycles. Backlog grows; some SOPs stay non-paired indefinitely.

**Likelihood.** Medium. **Impact.** Medium (vault inconsistency erodes the "SOPs read like manifesto" goal at scale).

**Mitigation.** I81 candidate stub at P6 framed as **continuous initiative** posture (precedent: I01 AKOS Full Roadmap). Each SOP review cadence (annual or event_triggered) absorbs retrofit naturally — no urgency pressure; each cadence cycle migrates 2-5 SOPs. Estimated full-vault completion: 6-12 months from I80 close.

**Status.** Active. P6 forward-charter.

---

## R-IH-80-6 — Addendum register frontmatter divergence creates audit confusion

**Description.** Paired-file addendum and body could drift in `last_review` / `last_review_decision_id` / `methodology_version_at_review` if reviewed independently. Auditors might see inconsistent metadata and question integrity.

**Likelihood.** Low. **Impact.** Low (audit clarification, not data integrity).

**Mitigation.** Validator extension at P1 emits an info-level warning when paired files have divergent frontmatter beyond access_level / classification / role_owner (legitimately divergent fields). Operator review, not a failure. SOP-META extension defines the frontmatter contract: body and addendum may diverge on access_level / classification / role_owner; must converge on `methodology_version_at_review` (semantic version of the SOP itself); may diverge on `last_review` / `last_review_decision_id` (independent review cadences).

**Status.** Active. P1 deliverable.

---

## R-IH-80-7 — Cursor skills evolve faster than docs

**Description.** Cursor SDK and skill format evolve at platform velocity. The skill authored at P3 may need format adjustments as Cursor releases new skill capabilities (frontmatter fields, tool-use patterns, cross-skill references).

**Likelihood.** Low. **Impact.** Low (skills are agent-side; format adjustments are mechanical).

**Mitigation.** Skill format follows current Cursor SDK SKILL.md spec at I80 P3 authoring time. Reviewable per Cursor SDK release notes; non-blocking for I80 closure. Future agent or initiative can re-format without semantic change.

**Status.** Active. Monitoring at platform-version horizon.
