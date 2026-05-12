---
language: en
status: active
canonical: true
role_owner: KM Officer + Research Director
classification: way_of_working
intellectual_kind: discipline_charter
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
---

# VALIDATION_DISCIPLINE_CHARTER — Research/Validation

> Authored I70 P4.7 per `RESEARCH_AREA_CHARTER.md` §2 + D-IH-70-S. **NEW formalization** (cross-links existing `confidence_levels.md` + `source_taxonomy.md` from compliance/). Validation is the truth-gate that runs AFTER Intelligence collection + Diagnosis verdicts.

## 1. Mission

The discipline of *what's true*. Defines source-reliability grading (HUMINT-derived A-F scale + OSINT confidence levels), cross-source corroboration practices, evidence-confidence scoring on diagnostic verdicts, and the validation-gate decisions that license downstream canonical promotion.

## 2. Three validation moves

| Move | What it grades | Inputs | Output |
|:---|:---|:---|:---|
| **Source-reliability grading** | Single-source trustworthiness (HUMINT + OSINT) | Source identity + track-record + corroboration history | A-F reliability grade per `confidence_levels.md` |
| **Cross-source corroboration** | Multiple-source convergence on a claim | 2+ sources + their reliability grades | Confidence score (1-5) per claim |
| **Evidence-confidence scoring** | Claim-level confidence after weighing sources | Source mix + reliability grades + counter-evidence | Per-claim verdict: Confirmed / Probable / Possible / Doubtful / Improbable |

## 3. Validation gates

Validation runs AT specific moments in the workflow:

- **Pre-canonical promotion** (per blueprint §13 step 3): Tier 1 WIP candidate must reach Confidence ≥ Probable on its load-bearing claims before promoting to canonical (Stage 3 inline-ratify).
- **Pre-customer-deliverable** (per render pipeline): customer-facing claims (numbers, KPIs, methodology assertions) must be at Confirmed or Probable; mark Possible+ claims as "operator estimate" or remove.
- **Pre-investor-deliverable** (per `KM_CHANNEL_VALUE_NARRATIVE`): selling-point claims that defend the moat must be at Confirmed; never make moat claims at Possible or below.
- **Pre-engagement-acceptance**: counterparty-baseline-reality assessments must reach Confirmed or Probable on the gap-of-the-week before recommending engagement scope.

## 4. Roles

- **KM Officer** (primary) — owns source-reliability registry + grading discipline.
- **Research Director** (primary) — owns validation-gate decisions for canonical promotions + investor-pack claims.

## 5. Cross-references

- Parent: [`RESEARCH_AREA_CHARTER.md`](../../canonicals/RESEARCH_AREA_CHARTER.md)
- Sister disciplines: Intelligence (input data), Methodology (how-to), Diagnosis (consumer of validated outputs).
- `confidence_levels.md` (compliance/; will move to People/Compliance/canonicals/ at P4.5 wave 3) — defines the 5-level confidence scale.
- `source_taxonomy.md` (compliance/; will move at P4.5 wave 3) — source-type catalog.
- HLK_KM_TOPIC_FACT_SOURCE.md — fact-vs-claim contract (every fact has at least one cited source).
- BRAND_BASELINE_REALITY_MATRIX (`Admin/O5-1/Marketing/Brand/canonicals/`) — reliability grading translates to external-register confidence language for customer-facing surfaces.
