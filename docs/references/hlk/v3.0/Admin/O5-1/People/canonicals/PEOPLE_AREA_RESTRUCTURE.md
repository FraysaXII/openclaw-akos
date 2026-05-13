---
language: en
status: active
canonical: true
role_owner: CPO + Founder
classification: way_of_working
intellectual_kind: area_restructure
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
companion_to:
  - Compliance/canonicals/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md
  - Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md
---

# PEOPLE_AREA_RESTRUCTURE — Talent monolith → 4 sub-roles

> Authored I70 P8 (§8.5) per **D-IH-70-Q** (Conundrum 8 ratification). Splits the legacy `People/Talent/` monolith into 4 sub-roles: **Compliance + Ethics + Learning + People Operations**. Codifies the operator-stated brand-positioning rationale: *"we become unethical when we unlearn"* — Ethics + Learning are inseparable disciplines under the Holistika brand.

This canonical is the **structural restructure parent doc**. Per-sub-role charters live at each sub-role's `canonicals/` folder. CSV updates to `baseline_organisation.csv` (Talent row split into 4 sub-roles + access-level adjustments) are **deferred to the dedicated operator-driven canonical-CSV migration session** (alongside P4.5 wave 2/3 + Marketing M3 CSV migration) per canonical-CSV-gate discipline.

## 1. Why the restructure

Pre-I70, People consisted of `Compliance + Legal + Organisation + Talent` with `Talent` containing `Corporate Marketing` and `Ethics & Learning` as sub-folders. Three signals motivated the split (per Conundrum 8 + the SUEZ engagement diagnostic):

1. **Talent doesn't capture the four distinct disciplines.** The legacy `Talent/Ethics & Learning/` mashed two disciplines that warrant separate ownership. `Talent/Corporate Marketing/` was mis-placed (it's a Marketing/Storytelling responsibility per D-IH-70-X).
2. **Founder principle 2.1 (AI-coexistence) and 2.2 (CSOLT lesson)** require an Ethics canonical with explicit ownership — `ETHICAL_AUTOMATION_POSTURE.md` codifies the second-order accountability for any future automation initiative. Ethics needs a sub-role home, not a sub-folder.
3. **People Operations** doesn't exist today as a role. Hiring + onboarding + payroll + offboarding are operational concerns that need explicit ownership; conflating them with Compliance or Legal is mis-fitting.

## 2. The 4 sub-roles

| Sub-role | Owns | Replaces (legacy) |
|:---|:---|:---|
| **Compliance** | identity / behavior / authorization compliance; CPO L6 master; CANONICAL_REGISTRY ownership; access-level taxonomy; confidence-level taxonomy | (existing People/Compliance; preserved + promoted to L6 master per D-IH-70-A) |
| **Ethics** | ETHICAL_AUTOMATION_POSTURE codification; CSOLT-lesson governance; second-order-accountability decision gates for automation initiatives; ethical posture on customer engagements | replaces legacy People/Talent/Ethics & Learning/ (Ethics half) |
| **Learning** | curriculum + onboarding (Holistik Researcher cohort per D-IH-70-M; deferred to I73); knowledge-transfer discipline; methodology-pillar-application coaching | replaces legacy People/Talent/Ethics & Learning/ (Learning half) |
| **People Operations** | hiring + onboarding flow + payroll + offboarding; per-role employment lifecycle; benefits + working-time policies | NEW (no legacy role; absorbs operational concerns scattered across legacy Talent) |

Plus existing People sub-areas preserved:
- **Legal** — preserved; per `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` + legal templates suite.
- **Organisation** — preserved (sparse; reserved for organizational design canon).
- **Founder** — top-level role-pseudo (FOUNDER_BIO + FOUNDER_TRAJECTORY_INTERNAL + future FOUNDER_METHODOLOGY_VERSIONING + FOUNDER_CORPUS_INVENTORY at P9).

## 3. Brand-positioning rationale: "we become unethical when we unlearn"

Operator-stated thesis (per Conundrum 8 + plan A6): Ethics and Learning are inseparable disciplines under the Holistika brand. The operator's reasoning:

> When an organization stops learning — when it stops investigating, stops questioning its assumptions, stops updating its operating models — it gradually loses the ground for ethical decisions. Ethical decisions require live information; live information requires ongoing learning. Unlearning produces unethical posture by structural starvation.

This thesis is operationalized as:
- **Ethics owns the posture canonical** (ETHICAL_AUTOMATION_POSTURE.md); applies the CSOLT lesson (founder principle 2.2: 2014 IBM Watson + European CSOLT 80% automation + 2015 layoff; operator was the engineer — second-order accountability).
- **Learning owns the curriculum** that keeps the posture live; ensures operators and Holistik Researcher cohorts have current methodology + current Research outputs.
- **The two charters cross-reference.** Ethics canonical declares: "this posture remains live only if Learning curriculum is current; if Learning lapses, Ethics must escalate." Learning canonical declares: "the curriculum's purpose is keeping Ethics decisions defensible."

This is a **Holistika differentiator** per `KM_CHANNEL_VALUE_NARRATIVE.md` §5 Claim 4 (AI coexists with human judgment) — operationalizing it requires the inseparable Ethics+Learning duo.

## 4. Per-sub-role charter forward-links

- `People/Compliance/canonicals/` — already federated home (P4.5 wave 2 deferred); existing SOPs at compliance/ migrate here.
- `People/Ethics/canonicals/` — RESERVED for `ETHICAL_AUTOMATION_POSTURE.md` (P9 deliverable; sibling commit at Phase 9).
- `People/Learning/canonicals/` — RESERVED for curriculum specs; full charter authoring deferred to I73 (People Operations + Learning curriculum candidate).
- `People/People Operations/canonicals/` — RESERVED for hiring + onboarding + offboarding SOPs; charter authoring at I73.

## 5. CSV updates (DEFERRED to operator-driven session)

Per the canonical-CSV-gate discipline:

- **`baseline_organisation.csv`** updates needed:
  - Deprecate `Talent` role row (replaced by 4 sub-roles).
  - Update `Talent/Ethics & Learning` references → split into Ethics + Learning rows.
  - Update `Talent/Corporate Marketing` → migrate to Marketing/Storytelling/Corporate Marketing per D-IH-70-X (cross-area).
  - Add `People Operations` role row (NEW; access_level TBD per operator review).
  - Add `Holistik Researcher Trainee` (already exists per P13.4; cross-link to Learning sub-role).

- **`process_list.csv`** updates needed:
  - Reorganize `hol_peopl_*` processes per new sub-roles (Compliance / Ethics / Learning / People Operations).
  - Add NEW `hol_peopl_ethics_dtp_*` processes for the ethical-posture decision gates.

- **`compliance/dimensions/SKILL_REGISTRY.csv`** + **`PERSONA_REGISTRY.csv`** + various dimensions touch People references.

These updates require operator approval per `akos-governance-remediation.mdc` HLK governance and coordinate with the canonical-CSV migration session.

## 6. Interim posture

- This canonical is **active** and authoritative on the People restructure target.
- The legacy `baseline_organisation.csv` `Talent` row remains operational until CSV migration.
- New canonicals authored at `People/<sub-role>/canonicals/` per the new structure (e.g., ETHICAL_AUTOMATION_POSTURE.md at P9 lands at `People/Ethics/canonicals/`).
- The 4 sub-roles exist as `populate` verdicts in the P2.5 v3.0 vault audit; they activate per this canonical.

## 7. Cross-references

- Sister structural redesign: [`MARKETING_AREA_M3_REDESIGN.md`](../../Marketing/canonicals/MARKETING_AREA_M3_REDESIGN.md) — sibling P8 deliverable.
- ETHICAL_AUTOMATION_POSTURE (P9 forward-link at `People/Ethics/canonicals/`).
- Founder Principle 2.2 (CSOLT lesson) — 2014 IBM Watson + European CSOLT 80% automation + 2015 layoff. Codified at FOUNDER_METHODOLOGY_VERSIONING.md (P9 forward-link).
- Founder Principle 2.1 (AI coexists with human judgment) — KM_CHANNEL_VALUE_NARRATIVE §5 Claim 4.
- D-IH-70-Q (P3 ratification) — People area restructure (4 sub-roles).
- D-IH-70-X (P2.5 audit sub-decision) — Corporate Marketing migrates to Marketing/Storytelling.
- D-IH-70-M (P3 ratification) — Holistik Researcher = role row + cohort tag (Learning sub-role consumes).
- Conundrum 8 — People area restructure resolution.
- I73 (People Operations + Learning curriculum) — deferred candidate for full Learning + People Operations charter authoring.
- I70 plan section 8.5 — full P8.5 deliverable spec.
