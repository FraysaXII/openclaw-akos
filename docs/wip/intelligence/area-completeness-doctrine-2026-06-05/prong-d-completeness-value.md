---
intellectual_kind: research_prong
prong: D
topic_cluster: external_completeness_value
authored: 2026-06-05
status: active
language: en
---

# Prong D — How industry defines "complete" and ranks by value

> External research-sweep (`SRC-AREA-EXT-47..62`). Answers `def-complete` + `def-threshold`:
> what does "done/complete" mean rigorously, and how is value/priority encoded?

## D.1 "Complete" is a deliberately chosen bar, not "100% of fields"

The DAMA data-quality definition of **completeness** is the sharpest external correction to
our intuition: completeness is *"all data **required for a particular use** is present"* —
"**not** about 100% of fields; it's about determining what is **critical** vs **optional**"
(`SRC-AREA-EXT-47`, GOV.UK/DAMA-UK; echoed `SRC-AREA-EXT-48`, `SRC-AREA-EXT-50`).

**Applied to us:** our flat 14/14 implicitly treats every component as required. The DAMA
view says completeness should distinguish **critical** components (an area is not governed
without them) from **optional/enhancing** ones. This is the empirical basis for **weighting**
or **tiering** components rather than counting them equally — and it comes from the very same
DAMA lineage our `confidence_levels`/`source_taxonomy` already cite.

## D.2 Two complementary "done" contracts: universal bar + per-item criteria (DoD / AC)

Scrum's distinction (`SRC-AREA-EXT-51..54`) is structurally identical to what an area bar
needs:

- **Definition of Done** = a **universal quality checklist applied to every item** (our
  14-component bar is exactly a DoD for areas).
- **Acceptance Criteria** = **per-item, specific, measurable** conditions (what an *individual*
  area uniquely must satisfy — e.g. Finance needs a tax calendar; Research needs a source
  ledger).
- **Definition of Ready** = entry gate before work starts.

**Applied to us:** we have a strong DoD (the 14 components) but **no per-area Acceptance
Criteria** layer. The mainstream agile answer to "is a flat checklist enough?" is *no — pair
a universal DoD with per-item AC*. This is a clean, low-risk addition: keep the 14-component
DoD, add a thin per-area AC list (the area's own load-bearing artifacts).

## D.3 Value/priority is encoded as Cost-of-Delay ÷ effort, severity-first (WSJF / our ICS)

WSJF (`SRC-AREA-EXT-55..57`): priority = **Cost of Delay ÷ Job Size**, where CoD =
Business-Value + Time-Criticality + Risk-Reduction. This is *the same fusion* our
`INTENT_RANKED_REGRESSION` ICS already uses (`SRC-AREA-INT-27`). So when we rank *which area
to build next* or *which gap to close first*, WSJF/ICS is the validated tool — and the
baseline regression already ran it (Step 2). **We do not need to invent ranking; we need to
apply the ranking we already have to the area-completeness components.**

## D.4 Measure with purpose; outcomes not activities (GQM / OKR)

- **GQM** (`SRC-AREA-EXT-58..60`, Basili): every **metric** must trace up to a **question**
  and a **goal** — "don't start with metrics, start with purpose," avoid "data graveyards."
  *Test for our bar:* does each of the 14 components trace to a goal/question, or are some
  components measured because they're easy to detect? AREA-11 (rule+skill present) and
  AREA-13 (README present) are the most "activity-ish" — easy to detect, weak goal-linkage.
- **OKR** (`SRC-AREA-EXT-61`, `SRC-AREA-EXT-62`, Doerr): a Key Result is a **measurable
  outcome, not an activity** ("increase NPS 32→45", not "launch survey"). *Applied to us:*
  most of our 14 components are **activity/artifact-presence** ("README exists"), not
  **outcome** ("the area reliably ships its contracted capability"). The outcome axis (does
  the area actually *work* for its consumers) is absent — the same gap Prong C named via
  "area as a product."

## D.5 What Prong D establishes for the decision

- `def-complete`: "complete" = **critical-vs-optional**, not all-fields (DAMA). Pair a
  **universal DoD (the 14)** with **per-area Acceptance Criteria** (Scrum). Add an
  **outcome/value** check (OKR/GQM/Data-Mesh-product), since today's bar is
  artifact-presence only.
- `def-threshold`: keep flat % as a *descriptive* signal, but rank *closure order* by
  **WSJF/ICS** (already in-repo); consider **critical-component-must-pass** gating instead of
  a single % (a 93% area missing its charter is not "done").
- `def-components`: GQM/OKR test flags AREA-11/AREA-13 as weak-goal-linkage (candidates to
  down-weight, not delete); names a missing **outcome/SLO** component.
