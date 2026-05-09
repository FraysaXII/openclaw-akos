---
sop_id: SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001
title: Counterparty Baseline Reality Assessment
version: 1.0
status: active
classification: canonical
access_level: 5
register: internal
language: en
process_id: hol_res_prc_counterparty_baseline_assess_001
role_owner: Holistik Researcher
role_parent_1: O5-1
area: Research
entity: Holistika
governance:
  - D-IH-66-F (IntelligenceOps SOPs)
  - D-IH-66-M (dual-register contract)
  - D-IH-66-Q (agent checkpoint discipline)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
audit_methodology_source:
  - US Army FM 2-22.3 Human Intelligence Collector Operations (public release; chapters 5-8 — adapted, not literal)
  - ICD-203 Analytic Standards (public release; analytic standards adapted to commercial CORPINT context)
adaptation_note: |
  This SOP adapts public-release HUMINT methodology to a commercial CORPINT-research context.
  No restricted or classified material is referenced. The adaptation is methodological;
  no operational tradecraft is implied or transferred. The discipline is **research**, not
  intelligence collection in any state-actor sense.
---

# SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001 — Counterparty Baseline Reality Assessment

> **Internal-register SOP.** Governs how Holistika prepares for any counterparty engagement (investor pitch, advisor onboarding, ENISA review, customer discovery, partner kickoff, recruiter interaction). The deliverable is an **internal-register baseline reality assessment** that informs the engagement's elicitation plan, intelligence report, and external-register translation. **Never rendered to the counterparty.**

## 1. Purpose and scope

### 1.1 Purpose

To produce a structured, source-graded internal model of a counterparty **before** the engagement, so that:

- The engagement is approached with calibrated expectations rather than optimism.
- The elicitation plan (per `SOP-IO_ELICITATION_DISCIPLINE_001`) is tailored to the counterparty's actual posture, not a generic template.
- The post-engagement intelligence report (per `SOP-IO_INTELLIGENCE_REPORT_001`) has a baseline against which to measure new information.
- The external-register translation (the deck companion, the follow-up email, the proposal) is grounded in evidence, not generic positioning.

### 1.2 Scope

This SOP applies to **all** counterparty engagements where Holistika is the inviting or accepting party and the engagement has measurable stakes (financial, strategic, regulatory, reputational, hiring, partnership). It does **not** apply to:

- Casual conversations or networking interactions.
- Open-source / public research that does not target a specific counterparty.
- Internal-only meetings (founder-team, advisor-team, employee-team).

### 1.3 Out of scope

This SOP is **not** an intelligence-collection SOP in the state-actor sense. It does not authorise:

- Surveillance of any kind.
- Pretext-based contact (impersonating a non-Holistika role to extract information).
- Acquisition of information through privileged-access exploitation.
- Information-handling outside the bounds of GDPR + counterparty-jurisdictional commercial-research norms.

If during preparation an artefact suggests one of the above might be useful, **stop**. The CORPINT-research methodology is **public + observable + permissioned**: anything beyond that is out of scope and out of doctrine.

## 2. Inputs

| Input | Source | Mandatory |
|:---|:---|:---:|
| Engagement trigger (calendar invite, inbound email, outbound outreach result, advisor referral) | calendar / mailbox / CRM | YES |
| Counterparty type (investor, customer-SME, advisor, ENISA, partner, recruiter, customer-LATAM) | classify per `BRAND_BASELINE_REALITY_MATRIX.md` 7 audience rows | YES |
| Counterparty name + organisation | engagement trigger | YES |
| Public-information landing page (LinkedIn, company site, regulatory filings, public deals) | OSINT | YES |
| Prior-relationship context (previous emails, previous meetings, mutual-contact intelligence) | mailbox / CRM / advisor network | OPTIONAL |
| Industry / sector chatter (recent press, recent regulatory action, recent leadership change) | OSINT | OPTIONAL |

## 3. Process steps

Total time-budget: 30-90 minutes per counterparty depending on counterparty significance. **Investor and ENISA engagements always get the full 90 minutes.** Customer-SME and recruiter engagements may use the 30-minute fast-path.

### Step 1 — Classify the counterparty (5 min)

Per `BRAND_BASELINE_REALITY_MATRIX.md` audience rows, assign the counterparty to one of:

- Investor
- Customer-SME
- Advisor
- ENISA evidence-body
- Partner / collaborator
- Recruiter / hiring-manager
- LATAM customer
- (Other → escalate to operator before continuing)

Rationale: the audience class drives the elicitation plan template (per SOP-IO_ELICITATION_DISCIPLINE_001) and the external-register translation rules.

### Step 2 — Gather public-information sources (10-30 min)

Consult, in this order:

1. Counterparty's **public-facing professional profile** (LinkedIn / company site / personal site).
2. Counterparty's **organisation profile** (Crunchbase / Companies House / equivalent national register / press history).
3. Counterparty's **public statements** (interviews, podcasts, talks, written op-eds, blog posts) from the **last 18 months**.
4. Counterparty's **portfolio / customer-base / employer history**, where applicable.
5. **Mutual-contact intelligence** (advisor network, prior-engagement notes, our own CRM history).

For each source consulted, **immediately grade it** per `SOP-IO_RELIABILITY_GRADING_001`. Do not skip the grading step; ungraded sources have a habit of being treated as A-1 by default, which is wrong.

### Step 3 — Construct the baseline reality assessment (10-30 min)

Use the template from `docs/wip/intelligence/_templates/elicitation-template-<audience>.md`. Fill out **all** the following fields:

| Field | Source it should derive from |
|:---|:---|
| Counterparty name (anonymised for any working-doc that survives the engagement) | Step 1 classification + counterparty's own self-description |
| Counterparty type | Step 1 classification |
| Declared posture (their stated thesis / declared need / declared anti-pattern) | Counterparty's own public statements |
| Inferred posture (what their behaviour reveals beyond their declarations) | Cross-reference of Steps 2.1-2.5 |
| Known anti-patterns | Industry chatter + portfolio analysis |
| Decision-maker shape | Organisation profile + role-pattern analysis |
| Time horizon | Inferred from past-engagement cadence patterns |
| Risk appetite (declared) | Counterparty's own statements |
| Risk appetite (inferred) | Behavioural pattern (cheque-size, governance asks, sector concentration) |
| Confidence level | Per-field A-F × 1-6 grade — composite confidence is the **lowest** field's grade, not the average |

**Critical discipline**: the **declared** vs **inferred** split is the heart of the assessment. Counterparties almost always have a gap between the two; the gap is the most useful intelligence the assessment produces. Do not collapse declared and inferred into a single "what they want" cell.

### Step 4 — Identify the gap and the unknowns (5-15 min)

Explicitly enumerate:

- **The gap** between declared and inferred posture (one short paragraph).
- **The unknowns** — what we cannot tell from public information alone (numbered list).

The unknowns become the **elicitation targets** for the engagement (per SOP-IO_ELICITATION_DISCIPLINE_001 §"Discovery questions").

### Step 5 — Produce the engagement design implication (5-15 min)

In one short paragraph, answer: given the assessment, what should the **engagement design** be?

- **Voice tier**: Tier-1 (operator-led, evidence-grounded, specific) vs Tier-2 (warmer, action-oriented). Per `BRAND_REGISTER_MATRIX.md`.
- **Approach techniques**: which of (direct interrogation / direct elicitation / indirect elicitation / provocation) are appropriate. Per SOP-IO_ELICITATION_DISCIPLINE_001 §3.
- **Time-discipline**: how long the engagement is sized for, and what's in / out of scope for this single engagement vs a follow-up.
- **Translation rules**: which internal-register concepts will need translation to which external-register tokens. Per `BRAND_BASELINE_REALITY_MATRIX.md` §3.

## 4. Outputs

### 4.1 Primary output

A `counterparty-brief.md` file under `docs/wip/intelligence/<YYYY-MM-DD>-<counterparty-slug>/counterparty-brief.md`, containing all five steps' output, with explicit per-field source-grading.

The file is **internal-register** — it uses the canonical internal vocabulary (counterparty, elicitation, baseline reality, etc.) per `BRAND_BASELINE_REALITY_MATRIX.md`. It is governed by `validate_brand_baseline_reality_drift.py` exemption (file-name suffix `.counterparty-brief.md` and parent dir `docs/wip/intelligence/`).

### 4.2 Secondary outputs

- An `elicitation-plan.md` (governed by SOP-IO_ELICITATION_DISCIPLINE_001) — derived from this assessment.
- A `source-grade.csv` (governed by SOP-IO_RELIABILITY_GRADING_001) — one row per source consulted in Step 2.

## 5. Redaction protocol

When an artefact in `docs/wip/intelligence/` survives the engagement window (i.e., is not deleted within 48h post-engagement), it **must** be redacted per the following rules:

| Field | Redaction rule |
|:---|:---|
| Counterparty individual name | Replace with anonymised slug (`Investor-NN`, `Advisor-NN`, etc.) |
| Counterparty organisation name | Replace with industry descriptor + size band (`mid-stage VC`, `Series-A SaaS firm in DACH`, etc.) |
| Specific dollar / euro figures | Round to nearest order of magnitude (`~€1M`, `~$10M`) |
| Specific dates | Generalise to month + year (`2026-04`) or quarter (`Q2 2026`) |
| Identifiable third parties | Replace with role descriptor |
| Specific quotes | Paraphrase or omit |
| Email addresses, phone numbers, addresses | Remove entirely |

Post-redaction, the artefact may be:

- **Archived** to `docs/_assets/transcripts/` for brand-voice pattern sourcing (per I66 P1 working space).
- **Promoted** as a `.counterparty-brief.md` companion to a deck under `docs/references/hlk/v3.0/_assets/advops/<engagement-slug>/`.
- **Retained** in `docs/wip/intelligence/` for ongoing-engagement reference (deleted on engagement closure).

Pre-redaction artefacts must **not** be committed to git. Operator-private storage (encrypted laptop folder, password-protected operator-only Google Drive folder) is the only acceptable home.

## 6. Quality discipline

### 6.1 Anti-patterns

- **Optimism bias** — assuming the counterparty thinks more highly of us than evidence suggests. Mitigation: explicit "inferred" column always references a specific behavioural source, not a hopeful inference.
- **Pattern-matching to single comparator** — assuming the counterparty is "like that other investor / advisor / customer". Mitigation: at least three independent comparators consulted before claiming a pattern.
- **Stale information** — using a counterparty's 18-month-old public statement as current-thinking evidence. Mitigation: every statement consulted is dated; statements > 18 months old are explicitly flagged as such.
- **Methodology theater** — going through the steps without genuine reasoning, producing a brief that's structurally complete but content-free. Mitigation: the "gap" and "unknowns" sections (§4 of the brief) are short — they should produce 1-3 specific items each, not generic prose.

### 6.2 Quality gates (self-review before engagement)

Before the engagement begins, the agent or operator authoring the brief reviews:

1. Does each cell in the baseline assessment have a specific, source-graded entry (not "TBD" or "unknown")?
2. Does the **declared / inferred** split show a meaningful difference, or have both columns collapsed into the same content (a sign of insufficient inference work)?
3. Are the unknowns specific enough to be answerable in the engagement, or are they so generic they cannot be addressed?
4. Does the engagement-design implication identify a specific voice tier, approach technique, time-discipline, and translation-rule set, or is it generic?
5. Is the source-grading column populated for every source consulted, with no defaults assumed to A-1?

If any of these answers is "no", the brief is incomplete; redo before engagement.

## 7. Cross-references

- [`SOP-IO_ELICITATION_DISCIPLINE_001.md`](SOP-IO_ELICITATION_DISCIPLINE_001.md) (sibling SOP — elicitation plan)
- [`SOP-IO_RELIABILITY_GRADING_001.md`](SOP-IO_RELIABILITY_GRADING_001.md) (sibling SOP — source grading)
- [`SOP-IO_INTELLIGENCE_REPORT_001.md`](SOP-IO_INTELLIGENCE_REPORT_001.md) (sibling SOP — post-engagement report)
- [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) — per-audience baseline + dual-register translation table
- [`.cursor/rules/akos-brand-baseline-reality.mdc`](../../../../../../../.cursor/rules/akos-brand-baseline-reality.mdc) — register-selection rule for agents
- [`scripts/validate_brand_baseline_reality_drift.py`](../../../../../../../scripts/validate_brand_baseline_reality_drift.py) — drift gate
- I66 master-roadmap §"P3 — Ops, process, organization, catalog, SOPs"
- D-IH-66-F (IntelligenceOps SOPs) and D-IH-66-M (dual-register contract) in `docs/wip/planning/66-brand-vision-ops-sweep/decision-log.md`

## 8. Methodology source citation

The discipline encoded in this SOP draws methodologically — not operationally or tactically — from:

- **US Army FM 2-22.3** (Human Intelligence Collector Operations, public release, September 2006). Specifically: chapter 5 (HUMINT Operational Planning), chapter 6 (Approach Techniques), chapter 8 (Reporting). These public-release chapters describe **structured-elicitation and source-grading discipline** as a public-domain skill. Holistika's adaptation translates this discipline into commercial CORPINT-research where:
  - "Source" = an interlocutor in a counterparty engagement.
  - "Approach" = a counterparty-engagement design (interview / pitch / discovery / advisory call).
  - "Report" = an internal-register engagement report that informs the external-register research brief.
- **ICD-203 Analytic Standards** (US Director of National Intelligence, public release). Specifically: the analytic-standards framework (BLUF, source-graded confidence, alternative-hypothesis discipline). Holistika's adaptation applies the same disciplines to commercial research outputs.

**Crucial adaptation note**: this SOP does **not** adopt the **operational** dimensions of FM 2-22.3 (interrogation techniques, captive-population work, military operational context). It adopts the **methodological** dimensions only (structured discovery, source-grading, BLUF-led reporting). The translation from military / state-actor context to commercial / CORPINT-research context is explicit, deliberate, and bounded by §1.3 "Out of scope".
