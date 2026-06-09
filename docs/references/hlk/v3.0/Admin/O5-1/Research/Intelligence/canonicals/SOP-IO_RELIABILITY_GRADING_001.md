---
sop_id: SOP-IO_RELIABILITY_GRADING_001
title: Source Reliability Grading
version: 1.0
status: active
classification: canonical
access_level: 5
register: internal
language: en
process_id: hol_res_prc_reliability_grading_001
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
  - US Army FM 2-22.3 §B-12 / §B-13 (Admiralty grading; public release; adapted)
  - ICD-203 §3 (analytic confidence taxonomy; adapted)
sister_sops:
  - SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001
  - SOP-IO_ELICITATION_DISCIPLINE_001
  - SOP-IO_INTELLIGENCE_REPORT_001
---

# SOP-IO_RELIABILITY_GRADING_001 — Source Reliability Grading

> **Internal-register SOP.** Governs how Holistika grades the trustworthiness of every source consulted in research. The grading is **two-dimensional** — source reliability (A-F) and information credibility (1-6), per the Admiralty system (FM 2-22.3 §B-12 / §B-13, adapted from the public-release).

## 1. Purpose and scope

Every research deliverable Holistika produces — whether internal-register intelligence report or external-register research brief — references sources. **Every referenced source is graded.** Ungraded sources are treated by readers as A-1 by default, which is almost never accurate.

This SOP applies to:

- Pre-engagement OSINT (per SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT step 2).
- In-engagement elicitation outputs (per SOP-IO_ELICITATION_DISCIPLINE).
- Any source consulted for an intelligence report (per SOP-IO_INTELLIGENCE_REPORT_001).
- Any source consulted for an external-register research brief.

Out of scope: sources used in internal-only operating decisions (e.g., the founder's own memory of a prior meeting) where formal grading would be theatre.

## 2. The two-dimensional grading system

Source grading is two-dimensional because **reliability** (the source's track record) and **credibility** (this particular piece of information's plausibility) are independent. A historically reliable source can produce a low-credibility item; an unproven source can produce a high-credibility item.

### 2.1 Reliability codes (A-F)

Per FM 2-22.3 §B-12, adapted:

| Code | Label | Definition |
|:---:|:---|:---|
| **A** | Completely reliable | Source has been verified from **multiple independent** prior interactions or has documented credentials from multiple independent vetting institutions. |
| **B** | Usually reliable | Source has been verified from **one independent** prior interaction or has documented credentials from one institution. |
| **C** | Fairly reliable | Source is plausible but unverified; e.g., a public-statement source whose track record we have not independently confirmed. |
| **D** | Not usually reliable | Source has produced contradictory information in the past, or contradictory evidence from independent sources is available. |
| **E** | Unreliable | Source has demonstrated reverse-narrative motive (e.g., a competitor's marketing material). |
| **F** | Cannot be judged | Insufficient evidence to grade reliability — used when the source is genuinely new and we have no track record. **Most common code in early-engagement preparation.** |

### 2.2 Information credibility codes (1-6)

Per FM 2-22.3 §B-13, adapted:

| Code | Label | Definition |
|:---:|:---|:---|
| **1** | Confirmed by other sources | This specific piece of information is independently confirmed by multiple sources. |
| **2** | Probably true | Logically consistent with multiple other accepted facts; not directly confirmed but plausible. |
| **3** | Possibly true | Logically possible but unconfirmed; consistent with what we know but extends it. |
| **4** | Doubtful | Logically possible but contradictory to other accepted facts. |
| **5** | Improbable | Contradictory to multiple other accepted facts. |
| **6** | Cannot be judged | Insufficient evidence to grade credibility — used when the information is novel and unverifiable. |

### 2.3 Composite grading

A source's grade for a specific information item is recorded as `<reliability>-<credibility>`, e.g.:

- `A-1` — completely reliable source, independently confirmed information. Highest confidence.
- `B-2` — usually reliable source, probably-true information. Good baseline.
- `C-3` — fairly reliable source, possibly-true information. Investigative lead.
- `F-6` — unrated source, unverifiable information. Treat as a question, not an answer.

### 2.4 What grades to expect

In practice, most pre-engagement research yields `B-2`, `C-3`, or `F-6` grades. **`A-1` is rare** and almost always a sign of either deep prior relationship or insufficient skepticism. **`F-6` is common and not bad** — it just means the information is a hypothesis rather than a fact.

## 3. Process steps

### Step 1 — At point of consultation, grade the source (1-2 min per source)

When consulting a source (LinkedIn profile, public statement, regulatory filing, prior-meeting note, mutual-contact intelligence), immediately:

1. Open the engagement's `source-grade.csv` (under `docs/wip/intelligence/<YYYY-MM-DD>-<counterparty-slug>/source-grade.csv`).
2. Add a row with: source name, source type, reliability (A-F), credibility (1-6), notes.
3. Note any caveats specific to this source (e.g., "source is 18-month-old public statement; may not reflect current posture").

### Step 2 — Cross-reference (5-10 min per assessment cycle)

Once 3-5 sources have been consulted on the same topic:

1. Compare their grades and content.
2. Where multiple sources confirm a point, the composite grade rises (e.g., two B-2 sources confirming each other → A-1 for the confirmed point).
3. Where sources contradict, **the contradiction itself is recorded** as an entry — do not silently pick one and discard the others.

### Step 3 — Reflect grade in downstream artefacts

When the source is referenced in:

- An internal intelligence report → grade is shown explicitly per claim.
- An external research brief → grade is **translated** to confidence language (per §4 below) — never shown literally, since "Admiralty B-2" is internal-register.

## 4. Translation to external register

Internal `<reliability>-<credibility>` grades are translated when rendered in external-register artefacts (research briefs, decks, dossiers, founder bios):

| Internal grade | External-register translation |
|:---|:---|
| A-1, A-2, B-1 | **High confidence**; cite source where appropriate. |
| B-2, B-3, C-1, C-2 | **Confident**; "we observe that …" with source cited. |
| C-3, D-1, D-2 | **Working hypothesis**; "evidence suggests …"; flag as not fully confirmed. |
| D-3, E-1, E-2, F-1, F-2 | **Open question**; "we do not yet have …"; defer claim or remove. |
| Anything-3+, F-3+, F-6 | **Cannot be claimed**; either remove from the deliverable or explicitly mark as forward-looking conjecture. |

## 5. Anti-patterns

- **Default-to-A-1** — assigning highest-confidence grade because the source "feels authoritative" (e.g., a partner at a big-name firm). The Admiralty system is about track record and verifiability, not authority.
- **Grade-after-the-fact** — adding grades to the source-grade.csv only at the end of the engagement. Always grade at consultation time; the immediate context informs the grade.
- **Single-source confirmation** — grading something A-1 because one source is reliable and confident. A-1 requires **multiple independent** sources.
- **Translation collapse** — exposing internal grades in external deliverables. The Admiralty grades are internal vocabulary per `BRAND_BASELINE_REALITY_MATRIX.md`; the external-register form is "high confidence / confident / working hypothesis / open question".

## 6. Quality discipline

### 6.1 Quality gates

Before any deliverable using these grades is released:

1. Does every source consulted have a row in `source-grade.csv`, or have some been skipped?
2. Is every claim in the deliverable cross-referenceable to a graded source?
3. Are external-register deliverables free of literal `A-1`-style notation, with translation to "high confidence / working hypothesis" instead?
4. Does the deliverable's stated confidence (in BLUF or summary) match the **lowest** grade among its supporting sources, not the average?

### 6.2 Periodic re-grading

Sources don't have permanent grades. Re-grade:

- After every engagement that involved the source (their reliability may rise or fall).
- Quarterly for sources used in repeat engagements (per `tbi_mkt_prc_brand_canon_mtnce_001` cadence).
- Immediately when a source produces contradicted information (re-grade downward; document the contradiction).

## 7. Cross-references

- [`SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md`](SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001.md) — uses this grading at step 2
- [`SOP-IO_ELICITATION_DISCIPLINE_001.md`](SOP-IO_ELICITATION_DISCIPLINE_001.md) — sibling
- [`SOP-IO_INTELLIGENCE_REPORT_001.md`](SOP-IO_INTELLIGENCE_REPORT_001.md) — uses this grading in §"source-graded reliability assessment"
- [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) §3 (translation rules — Admiralty grades are internal-register)
- D-IH-66-F (IntelligenceOps SOPs)
