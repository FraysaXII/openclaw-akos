---
language: en
status: active
canonical: true
role_owner: UX Designer + PMO (joint)
classification: way_of_working
intellectual_kind: discipline_canonical
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
companion_to:
  - BRAND_UX_DESIGNER_CHARTER.md
  - ../../canonicals/BRAND_DISCIPLINE_ONTOLOGY.md
  - ../../../../../Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md
  - ../../../../../Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md
---

# BRAND_GANTT_DISCIPLINE — Brand/UX-Designer + PMO joint discipline

> Authored I70 P6 per plan section 6. Joint UX-Designer + PMO ownership: UX-Designer owns the visual + interaction primitives; PMO owns the engagement-orchestration semantics. Codifies the 4-quadrant audience matrix, the Mermaid Gantt SSOT, the confidence ladder for thinner-data engagements, and the Variant B proof-of-discipline pattern (SUEZ engagement worked example at `gantt.customer.fr.md`).

## 1. Why a Gantt discipline

Pre-I70, engagement timelines lived informally in proposal slides as ad-hoc tables. Two problems surfaced:

1. **Per-deliverable rigor varied** — the SUEZ deck slide 10 timeline (5-temps) and the Asesoría engagement (no formal Gantt yet) had inconsistent depth.
2. **Confidence wasn't communicated** — early-stage engagements with thin data shipped with deceptively-precise dates that the operator couldn't actually defend.

The discipline addresses both: a single Mermaid Gantt SSOT format, a 4-quadrant audience matrix that scales detail to engagement maturity, and an explicit confidence ladder.

## 2. The 4-quadrant audience matrix

Every Gantt deliverable picks a quadrant based on (audience-formality × data-maturity):

| | Low data maturity | High data maturity |
|:---|:---|:---|
| **Customer-facing** | Variant A — Posture sketch (no dates; phase ribbons; ratify-via-discovery) | Variant B — Proof of discipline (concrete dates; per-phase deliverables; per-phase ownership) |
| **Operator-internal** | Variant C — Hypothesis sketch (cross-linked sources; assumption flags; revisit cadence) | Variant D — Execution plan (granular weekly task breakdown; dependency arrows; resource allocation) |

**Variant A — Posture sketch.** When the engagement hasn't completed discovery yet. Shows phase ribbons (Cadrage / Prototype / Industrialisation per SUEZ's three variants) without committing to dates. Communicates approach, not schedule. Ratify-via-discovery is the explicit mechanism: dates fill in after week 1's discovery cadence.

**Variant B — Proof of discipline (worked example: SUEZ).** Customer-facing AND data-mature. Concrete dates; per-phase deliverables; per-phase ownership; per-phase risk ladder. The customer reads this as "Holistika has done this before; the discipline is real." Used when proposal targets a specific quote / specific engagement window. **`gantt.customer.fr.md` at `2026-suez-webuy/02-customer-pack/`** is the worked example in this commit.

**Variant C — Hypothesis sketch.** Operator-internal AND low data maturity. Used during discovery + scoping phases. Cross-links to source intelligence (per Research/Intelligence outputs); flags assumptions; declares revisit cadence (typically weekly).

**Variant D — Execution plan.** Operator-internal AND data-mature. Used post-engagement-acceptance for delivery management. Granular weekly task breakdown; dependency arrows between phases; resource allocation per role + per-week. Fed by PMO's engagement orchestration.

## 3. Mermaid Gantt SSOT format

Every Gantt deliverable uses Mermaid syntax with these primitives:

```mermaid
gantt
    title <Engagement> — <Variant Letter>
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section <Phase 1>
    <Deliverable 1.1>: <id1>, <start>, <duration>
    <Deliverable 1.2>: <id2>, after id1, <duration>

    section <Phase 2>
    <Deliverable 2.1>: <id3>, after id2, <duration>
```

**Mermaid is render-target-aware:**

- For customer-pack (Variants A + B), the Mermaid renders to SVG via the existing render pipeline (akos/hlk_pdf_render.py); SVG embeds in the PDF.
- For operator-internal (Variants C + D), Mermaid stays as raw text (Markdown native; renders in Cursor / GitHub / Drive).
- For ERP panel (HLK_ERP_ARCHITECTURE §4 reserved): Mermaid renders client-side via mermaid.js.

**Per-deliverable metadata (frontmatter):**

- `gantt_variant: A | B | C | D` — which quadrant.
- `confidence_band: 1-5` — per the confidence ladder (§4 below).
- `ratify_cadence: discovery_week_1 | weekly | bi-weekly | monthly | post-acceptance` — when dates get re-validated.

## 4. Confidence ladder (5-level)

Every Gantt date carries an implicit confidence band. The discipline makes it explicit:

| Band | Label | Definition | When to use |
|:---:|:---|:---|:---|
| **5** | Confirmed | Dates committed in signed engagement contract; calendar-locked | Variant B; post-contract |
| **4** | Probable | Dates derived from confirmed dependencies + operator capacity check | Variant B; mid-acceptance |
| **3** | Posture | Dates derived from discipline-typical durations; flagged as posture | Variant A + Variant C |
| **2** | Hypothesis | Dates derived from analogous prior engagements; flagged as hypothesis | Variant C only |
| **1** | Reserved | Phase ribbon only; no dates | Variant A only |

**Display rules (UX-Designer authority):**

- Band 5: solid bar + dates in title.
- Band 4: solid bar + dates with `~` prefix.
- Band 3: dotted bar + dates with `~` prefix + footnote-mark.
- Band 2: dotted bar + dates with `?` prefix + explicit "hypothesis" footnote.
- Band 1: phase ribbon only; no bars.

Customer-pack should not ship Variant B with bands 1-2. Customer-pack Variant A is preferred when data maturity is low.

## 5. Slide-legibility QA gate (per BRAND_UX_DESIGNER_CHARTER §3)

Customer-pack Gantt deliverables pass:
- **Headline gate** — Gantt title ≤ 60 chars; engagement-id-prefixed.
- **Confidence band visible** — band annotation in subtitle or footnote.
- **Variant declared** — frontmatter `gantt_variant:` matches displayed shape.
- **Multilingual register** (per P7) — title + section names + footnotes match per-engagement language.

## 6. Worked example — SUEZ engagement (Variant B)

The SUEZ engagement ships its first Variant B Gantt at `2026-suez-webuy/02-customer-pack/gantt.customer.fr.md` (sibling commit). The Gantt shows:

- 3 variants (A — Cadrage / B — Prototype / C — Industrialisation) per the proposal section 4.
- Per-variant phase breakdown (Lecture / Composition / Revue / Soumission for variant B) per the deck slide 08 4-step flow.
- Per-phase deliverable + owner + confidence band.
- Footer cross-link to the proposal.customer.fr.md for narrative context.

This worked example demonstrates the discipline at customer-pack-Variant-B-grade: concrete dates; per-phase deliverables; band 4 (Probable) for the recommended Variant B; band 3 (Posture) for the speculative Variants A + C.

## 7. Validator (forward-link to I71)

`scripts/validate_brand_gantt_discipline.py` (NEW; deferred to I71 implementation) checks every `gantt.*.md` file in customer-pack folders for:
1. Frontmatter `gantt_variant:` declared + valid.
2. Frontmatter `confidence_band:` declared + valid integer 1-5.
3. Frontmatter `ratify_cadence:` declared + valid enum.
4. Mermaid `gantt` block present; passes basic syntax check.
5. Per-phase deliverables ≥ 1 (no empty sections).
6. Variant-quadrant consistency: customer-pack only ships A or B; operator-internal only ships C or D.

## 8. Cross-references

- Parent: `BRAND_UX_DESIGNER_CHARTER.md` (sibling at this canonicals/) §1 (Gantt discipline).
- Sister: `BRAND_DISCIPLINE_ONTOLOGY.md` (parent ontology).
- Sister: `BRAND_COPYWRITING_DISCIPLINE.md` (Gantt titles + footnotes pass copywriting discipline gates).
- PMO co-owner: `WORKSPACE_BLUEPRINT_HOLISTIKA.md` (engagement orchestration semantics).
- HLK_ERP_ARCHITECTURE §4 — `/operator/marketing/brand/ux-designer/` panel reserves a Gantt-rendering surface (P10.5).
- Validator: `scripts/validate_brand_gantt_discipline.py` (forward-link to I71).
- Worked example: `2026-suez-webuy/02-customer-pack/gantt.customer.fr.md` (sibling commit).
- I70 plan section 6 — full P6 deliverable spec.
