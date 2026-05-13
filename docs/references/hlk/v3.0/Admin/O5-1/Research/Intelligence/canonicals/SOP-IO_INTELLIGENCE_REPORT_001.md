---
sop_id: SOP-IO_INTELLIGENCE_REPORT_001
title: Intelligence Report
version: 1.0
status: active
classification: canonical
access_level: 5
register: internal
language: en
process_id: hol_res_prc_intelligence_report_001
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
  - US Army FM 2-22.3 chapter 8 (Reporting; public release; adapted)
  - ICD-203 (BLUF + analytic confidence; adapted)
sister_sops:
  - SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001
  - SOP-IO_ELICITATION_DISCIPLINE_001
  - SOP-IO_RELIABILITY_GRADING_001
---

# SOP-IO_INTELLIGENCE_REPORT_001 — Intelligence Report

> **Internal-register SOP.** Governs how Holistika produces the post-engagement structured report. The intelligence report is the **internal** counterpart of the external-register research brief / engagement report / context memo that the counterparty receives. Both forms exist for every meaningful engagement; the internal form is the source-of-truth.

## 1. Purpose and scope

The intelligence report:

- Captures the structured output of a counterparty engagement before it fades from memory.
- Updates the baseline reality assessment with new information observed in-engagement.
- Source-grades every new claim made by or about the counterparty.
- Recommends a specific next action (proceed to follow-up / pause / disengage).
- Provides the **basis** for the external-register translation (deck companion / proposal / follow-up email / public dossier).

This SOP applies to every meaningful counterparty engagement (per SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT scope §1.2).

Out of scope: post-engagement notes that are casual rather than structured (e.g., a 5-minute hallway conversation at a conference). For those, a single-paragraph note is sufficient and lives in the engagement's notes folder, not as a structured intelligence report.

## 2. Inputs

| Input | Source |
|:---|:---|
| Pre-engagement baseline reality assessment | `counterparty-brief.md` from SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT |
| Elicitation plan | `elicitation-plan.md` from SOP-IO_ELICITATION_DISCIPLINE |
| Source grades (pre-engagement + new in-engagement) | `source-grade.csv` from SOP-IO_RELIABILITY_GRADING |
| In-engagement notes | listening-protocol output (raw notes, redacted before commit) |

## 3. Report structure

The intelligence report follows a **6-section structure** based on FM 2-22.3 chapter 8 (adapted):

### Section 1 — BLUF (Bottom Line Up Front)

**One sentence.** What's the most important takeaway from this engagement?

Examples (anonymised):

- *"`[Investor-NN]` is unlikely to lead a Series A round but is a high-probability follow-on if a tier-1 lead emerges."*
- *"`[Customer-MM]` confirms strong-pull demand for the engagement's first deliverable but introduces an unanticipated regulatory blocker on the second."*
- *"`[Advisor-PP]` accepted the formal advisor role with explicit time-budget caveats; appoint within 14 days."*

**Critical discipline**: BLUF is what the operator reads and acts on. If BLUF is generic ("the meeting went well"), the report has failed.

### Section 2 — Updated baseline reality assessment

**One short paragraph** per row that materially changed in the baseline assessment. Specifically address:

- **Declared posture**: did the counterparty state anything new? Specifically?
- **Inferred posture**: did the counterparty's behaviour reveal something the pre-engagement assessment missed?
- **Decision-maker shape**: any new information about who actually decides?
- **Risk appetite**: did the engagement reveal the counterparty's actual (vs declared) risk tolerance?
- **Anti-patterns**: any new disqualification signals?

If a row didn't materially change, omit it. **Don't pad.**

### Section 3 — Source-graded reliability assessment

A bulleted or tabular list of every **new claim** the counterparty made or that emerged in-engagement, with its grade per `SOP-IO_RELIABILITY_GRADING_001`.

Format per row:

```
- "Counterparty claim or new fact" — Grade: <reliability>-<credibility>
  Rationale: <one sentence justifying the grade>
  Cross-reference: <other sources confirming or contradicting>
```

### Section 4 — Recommended next action

**One short paragraph.** Concretely:

- **Proceed to follow-up**: with what cadence (24h email / 5-10d deliverable / longer-term engagement)?
- **Pause**: for how long, contingent on what?
- **Disengage**: explicitly why, and what's the polite-disengagement script?

The recommended action must be **specific** and **time-bound**. "We should follow up at some point" is not a valid Section 4.

### Section 5 — Translation rules for external register

A short list of which internal-register concepts will need translation when this engagement's external-register deliverables (deck companion, proposal, follow-up email) are written.

Per `BRAND_BASELINE_REALITY_MATRIX.md` §3, translation pairs commonly used:

- internal: counterparty → external: client / advisor / regulator (depending on engagement type)
- internal: this elicitation cycle → external: this discovery / this conversation / this call
- internal: source-graded confidence → external: high-confidence / working-hypothesis / open-question

If the engagement's external deliverables will need any non-standard translation, document it here so the deliverable author has reference.

### Section 6 — Cross-references and follow-up artefact pointers

- Pointer to the `counterparty-brief.md` (input baseline).
- Pointer to the `elicitation-plan.md` (input plan).
- Pointer to the `source-grade.csv` (updated source grades).
- Pointer to the (forthcoming) external-register deliverable.
- Pointer to any follow-on engagement scheduled.

## 4. Filing discipline

The intelligence report is filed within **24 hours** of engagement closure, regardless of:

- Whether the external-register deliverable is ready (it almost never is — the report is its prerequisite, not its companion).
- Whether the counterparty has followed up (their follow-up is irrelevant to our internal record).
- Whether the operator has read the prior iteration of the brief (the report exists for the institutional memory, not the operator's immediate consumption).

File location: `docs/wip/intelligence/<YYYY-MM-DD>-<counterparty-slug>/intelligence-report.md`.

## 5. Promotion / archival

Once the engagement closes (the external-register deliverable is sent, the partner is signed, the investor passes or commits, the customer engages or doesn't):

1. **Archive raw**: the in-engagement notes are deleted within 14 days of engagement closure (operator-private; never enter git).
2. **Promote redacted**: the intelligence report is redacted per SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT §5 and:
   - **Stays** under `docs/wip/intelligence/` for 30 days for cross-engagement reference.
   - **Either** archives to `docs/_assets/transcripts/` (post-redaction, pattern-source) **or** deletes after 30 days, depending on whether there's lasting institutional-memory value.
3. **Companion**: if the engagement produced an external-register deck or dossier, the intelligence report is promoted (post-redaction) to a `.counterparty-brief.md` companion file alongside the deck under `docs/references/hlk/v3.0/_assets/advops/<engagement-slug>/`.

## 6. Quality discipline

### 6.1 Anti-patterns

- **Diary mode** — writing the report as a chronological account of the meeting. The report is **structured by analytic dimension**, not by conversation order.
- **Padding** — writing all 6 sections at length even when most rows didn't change. If Section 2 has nothing material, write "no material changes to baseline assessment" and move on.
- **Action-vague Section 4** — "we'll see" or "let's follow up" is not a valid recommended next action.
- **External-register leakage** — using "client" instead of "counterparty" or "research" instead of "intelligence collection" in the report itself. The report is internal-register; do not pre-emptively translate.
- **Source-grade collapse** — listing claims without grading them. Every claim needs a `<reliability>-<credibility>` grade or it's a vibe, not intelligence.

### 6.2 Quality gates

Before the report is filed:

1. Does Section 1 (BLUF) communicate the most important takeaway in one sentence?
2. Does Section 2 only list rows that materially changed?
3. Does Section 3 grade every new claim, with no defaults to A-1?
4. Does Section 4 specify a concrete time-bound next action?
5. Are there no external-register tokens leaking into the report's prose (validator: `validate_brand_baseline_reality_drift.py` — the report file would fail this gate if external-register tokens leaked, but the report is in `docs/wip/intelligence/` which is exempt; the discipline is self-imposed)?

## 7. Translation to external register

The intelligence report is **never** sent to the counterparty. Its external-register form is the **research brief** (R&S engagements), the **engagement report** (advisor engagements), or the **context memo** (customer / partner engagements).

Translation rules per `BRAND_BASELINE_REALITY_MATRIX.md` §3:

| Internal-register section | External-register form |
|:---|:---|
| §1 BLUF | High-level summary in the deliverable's executive summary |
| §2 Updated baseline | Section "What we observe about your situation" — specific to the engagement |
| §3 Source-graded reliability | "We are confident that …" / "evidence suggests …" / "this is a working hypothesis" — translation per `SOP-IO_RELIABILITY_GRADING_001` §4 |
| §4 Recommended next action | "We propose to …" with explicit time-bound deliverable commitments |
| §5 Translation rules | Not rendered (it's a translation key, not a deliverable section) |
| §6 Cross-references | Internal pointers; not rendered to external deliverable |

The external deliverable is shorter, less structured-looking, and reads as professional research — exactly because the underlying intelligence report did the structured-analysis work.

## 8. Cross-references

- [`SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md`](SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md) — input
- [`SOP-IO_ELICITATION_DISCIPLINE_001.md`](SOP-IO_ELICITATION_DISCIPLINE_001.md) — input
- [`SOP-IO_RELIABILITY_GRADING_001.md`](SOP-IO_RELIABILITY_GRADING_001.md) — input
- [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) §3 — translation rules
- [`.cursor/rules/akos-brand-baseline-reality.mdc`](../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc) — register-selection rule
- D-IH-66-F (IntelligenceOps SOPs)
