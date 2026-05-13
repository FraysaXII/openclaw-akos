---
language: en
status: active
canonical: true
role_owner: Ethics
classification: way_of_working + selling_point
intellectual_kind: ethical_posture
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
companion_to:
  - ../../canonicals/PEOPLE_AREA_RESTRUCTURE.md
  - ../../canonicals/FOUNDER_METHODOLOGY_VERSIONING.md
  - ../../../Marketing/Brand/Copywriter/canonicals/BRAND_COPYWRITING_DISCIPLINE.md
---

# ETHICAL_AUTOMATION_POSTURE — IBM CSOLT lesson + second-order accountability

> Authored I70 P9 (§9.5b) per plan section 9 + **D-IH-70-Q** (Conundrum 8 People restructure: Ethics as standalone sub-role under People). Codifies founder principle 2.2 (CSOLT lesson) as the operational ethical posture for any Holistika automation initiative. Cross-references founder principle 2.1 (AI-coexistence as design constraint per `FOUNDER_METHODOLOGY_VERSIONING.md` §3.2.1) + the brand-positioning thesis "we become unethical when we unlearn" (per `PEOPLE_AREA_RESTRUCTURE.md` §3).

## 1. The CSOLT lesson (founder principle 2.2 codification)

Operator-stated origin (per `FOUNDER_METHODOLOGY_VERSIONING.md` §3.2.2):

> *"On 2014, as I worked on IBM Watson AI … sales process design … automate 80% of the European CSOLT … big lay-off. 2015! Imagine my face when I saw the same thing happen post 2023."*

The 2014 IBM Watson European CSOLT (Customer Service / Operations / Logistics Team) automation project shipped in 2014, led to a major layoff in 2015. The founder was the engineer who designed the sales process automation. The lesson:

> **The engineer is responsible for who-loses-what when the process they design ships.**

This is not a one-off; it generalizes. Post-2023 LLM era replays the same dynamic at industry scale. The founder's experience makes the second-order accountability concrete and load-bearing for Holistika's commercial posture.

## 2. The 5 commitments (operational posture)

Holistika commits to the following on every automation initiative (internal R&D + customer engagements + future MADEIRA productization):

### 2.1 Pre-design impact assessment

Before designing any process automation, document:
- **Which roles are touched** (per `baseline_organisation.csv` if internal; per counterparty-supplied org chart if external).
- **What share of each role's work the automation absorbs** (estimate, with confidence band).
- **What residual work remains for the human** — and whether that residual is enriched or de-skilled.

This assessment lives in the engagement's `00-internal/checkpoints/` folder for customer engagements, or in the initiative's `docs/wip/planning/<NN>/reports/ethics-impact-assessment.md` for internal initiatives.

### 2.2 Co-existence design constraint

Per founder principle 2.1: automation is built so the human keeps **judgment**. The application calculates; the human validates. Worked example: SUEZ Slide 08 four-step flow (Lecture → Composition → Revue → Soumission) where **Revue** is the human-validation gate.

When the proposed automation does NOT permit a human-validation gate (because the process is fully deterministic and validation would slow it), document the rationale + the compensating discipline (e.g., post-hoc audit cadence; spot-check sampling).

### 2.3 Workforce-impact transparency

When the customer engagement directly leads to a workforce reduction:
- The customer is informed of the projected reduction at proposal stage (not at delivery stage).
- The proposal includes a section on the customer's transition responsibilities (re-skilling / redeployment / severance).
- The customer-pack proposal carries an **explicit workforce-impact line** when applicable; the customer cannot read the proposal without seeing it.

### 2.4 Refusal-to-engage criteria

Holistika reserves the right to refuse engagements where:
- The customer's stated automation goal is workforce reduction with no transition plan.
- The customer's automation request would automate decisions that should remain human (per per-engagement ethical review at proposal stage).
- The customer has demonstrated willingness to bypass the co-existence design constraint (§2.2).

The refusal-to-engage criteria are a **competitive surface boundary** (per `KM_CHANNEL_VALUE_NARRATIVE.md` §6 anti-claims): Holistika does NOT sell AI-replacement-for-humans.

### 2.5 Ongoing-review cadence

Every automation initiative (internal + customer-engagement) ships with an ongoing-review cadence:
- **Quarterly**: revisit the §2.1 pre-design assessment vs. observed reality (did the residual work emerge as designed? are humans still in the loop where designed?).
- **Annual**: revisit §2.4 refusal-to-engage criteria + their applicability.

Findings cross-link to `LOGIC_CHANGE_LOG.md` when they trigger version-increment-worthy methodology updates.

## 3. The "we become unethical when we unlearn" thesis (brand-positioning)

Operator-stated thesis (per `PEOPLE_AREA_RESTRUCTURE.md` §3 + Conundrum 8 ratification):

> When an organization stops learning — when it stops investigating, stops questioning its assumptions, stops updating its operating models — it gradually loses the ground for ethical decisions. Ethical decisions require live information; live information requires ongoing learning. Unlearning produces unethical posture by structural starvation.

This thesis operationalizes as:
- **Ethics owns this canonical** (the posture).
- **Learning owns the curriculum** that keeps the posture live (per `PEOPLE_AREA_RESTRUCTURE.md` §2; Learning sub-role; deferred to I73 for full charter).
- **The two charters cross-reference.** This canonical's §5 below declares: "this posture remains live only if Learning curriculum is current; if Learning lapses, Ethics must escalate to founder."

## 4. Decision gates (when to invoke this canonical)

This canonical is invoked at:

| Gate | Who invokes | When |
|:---|:---|:---|
| **Engagement scope-acceptance** | PMO + Account Management (Marketing/Resonance) | Before sending proposal; checks §2.4 refusal criteria + drafts §2.1 impact assessment |
| **Internal automation initiative charter** | System Owner + Founder | Before initiating any I-NN automation initiative; cross-link to charter doc |
| **Quarterly ongoing-review** | Ethics sub-role (post-charter) + Founder | Per §2.5 cadence; updates this canonical's last_review timestamp |
| **MADEIRA productization activation** | Founder + System Owner + Ethics | Per HLK_ERP_ARCHITECTURE §8 trigger; full §2.1 impact assessment for the productized form before invitations issue |

## 5. Ethics + Learning inseparability contract

This canonical declares: **Ethics is alive only when Learning is current.**

Concretely:
- If the Learning curriculum (deferred to I73) lapses — operators stop reading current Research outputs; methodology pillars stop being updated; engagement diagnostic findings stop feeding back to canonicals — Ethics must **escalate to founder for posture review**.
- If a quarterly review (per §2.5) reveals Learning lapses, this canonical's `last_review` timestamp surfaces drift in the dashboard; founder triages.
- The two sub-roles cross-reference each other in their charters; neither operates in isolation.

## 6. Cross-references

- Parent: [`PEOPLE_AREA_RESTRUCTURE.md`](../../canonicals/PEOPLE_AREA_RESTRUCTURE.md) §3 — brand-positioning thesis "we become unethical when we unlearn".
- Sister: `FOUNDER_METHODOLOGY_VERSIONING.md` (People/canonicals/) §3.2.1 + §3.2.2 — founder principles 2.1 + 2.2.
- Sister: `BRAND_COPYWRITING_DISCIPLINE.md` (Marketing/Brand/Copywriter/canonicals/) — anti-AI-tone discipline operates the AI-coexistence design constraint at the prose register level.
- Sister: KM_CHANNEL_VALUE_NARRATIVE.md (Operations/PMO/) §5 Claim 4 (AI coexists with human judgment) + §6 anti-claim 2 (not AI-replacement-for-humans).
- HLK_ERP_ARCHITECTURE.md §8 (AKOS-complete-enough trigger) — pre-trigger gate invokes §2.1 impact assessment.
- D-IH-70-Q (P3 ratification) — Ethics as standalone sub-role.
- D-IH-70-V (P2.5 audit sub-decision) — AIC framing; MADEIRA productization gates.
- I70 plan §9 — full P9 deliverable spec (this canonical is part of P9 §9.5b).
- I73 (People Operations + Learning curriculum candidate) — full Learning charter author here on activation.
