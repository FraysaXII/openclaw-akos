---
intellectual_kind: research_action_pack
parent_initiative: INIT-OPENCLAW_AKOS-93
related_initiatives: [88, 86]
authored: 2026-06-05
last_review: 2026-06-05
status: active
role_owner: Research Lead
co_owner_roles: [PMO, CPO, System Owner]
language: en
discipline: RESEARCH_ACTION_DISCIPLINE.md (15th Quality Fabric specialty; D-IH-86-FF)
source_ledger: source-ledger.csv
control_confidence_level: Euclid
---

# Research-action pack — "What is an area, and what does completeness mean for us?"

> **Control layer** for the area-completeness doctrine research action, per
> [`RESEARCH_ACTION_DISCIPLINE.md`](../../../references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md)
> §3 (8-stage loop) and [`akos-research-action.mdc`](../../../../.cursor/rules/akos-research-action.mdc) RULE 1
> (mandatory source ledger). Authored at operator instruction 2026-06-05 (verbatim below).

## 0. Operator instruction (verbatim)

> *"before going for option A then D, but before starting, update area completeness
> parameters, do a regression over the full picture, then each area topography, then do
> full fledged research inside and outside to see how those are handled and ranked and
> their value, then come back here, mint the research (be sure to have +50 internal
> sources and +50 external sources, the more the better, all categorized), then with
> that, do a regression over what an area is and what completeness means for us. When
> that is done, explain the result to me and AskQuestion before going to option A and D."*

## 1. The named downstream decision (Principle 1 — decision first, research second)

Every source in [`source-ledger.csv`](source-ledger.csv) is rated against **one** decision:

> **D-AREA-DEF — Before driving the remaining five O5-1 areas (People, Marketing,
> Operations, Research, Tech) to closure, should Holistika amend the definition of
> "an area" and/or the 14-component completeness bar — and if so, how?**

The decision has four sub-questions, each a `decision_use` tag in the ledger:

| Tag | Sub-question |
|:---|:---|
| `def-area` | **What is an area?** Is the current "O5-1 folder tree + roles + processes" boundary the right unit, or do we need sharper criteria (bounded context, value-stream, capability domain)? |
| `def-complete` | **What does "complete" mean for us?** Is flat pass-count the right scalar, or do we need weighting / a definition-of-done / a maturity ladder? |
| `def-components` | **Are the 14 components the right set?** Missing dimensions (data-quality, outcome/value, security, observability, lifecycle)? Redundant ones? |
| `def-threshold` | **What PASS threshold = "done"?** Today 88% is the I93 reference bar; is a single global threshold correct, or per-area / per-tier? |

## 2. Why this is a research action (not scratchwork)

Per `akos-research-action.mdc` "When this rule applies": this research **will drive a
canonical edit** — specifically a possible amendment to
[`AREA_GOVERNANCE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md)
§2 (the 14 components) and/or `akos/hlk_area_completeness.py` (the scored enum) and/or the
PASS-threshold posture. That is the trigger for the mandatory source ledger + 8-stage loop.

## 3. The 8-stage loop application

| Stage | Artifact in this pack | Status |
|:---|:---|:---|
| 1 Ingest | [`source-ledger.csv`](source-ledger.csv) — 55 internal + 62 external = **117 rows** | ✅ done |
| 2 Rate | per-row reliability + external-credibility + Safe/Euclid/Keter (validator PASS) | ✅ done |
| 3 Rank | sources ranked by relevance to D-AREA-DEF inside [`baseline`](baseline-state-2026-06-05.md) + prong files | ✅ done |
| 4 Synthesize | [`baseline`](baseline-state-2026-06-05.md) + [`prong A–D`](master-synthesis.md) + [`master-synthesis`](master-synthesis.md) | ✅ done |
| 5 Govern | option set surfaced to operator via AskQuestion (Step 7) | ⏳ **operator gate** |
| 6 Implement | amend `AREA_GOVERNANCE_DISCIPLINE.md` / `hlk_area_completeness.py` **only after** operator ratifies | gated |
| 7 Test | `validate_research_action.py --source-ledger` PASS ✅ + (if Stage 6 fires) `validate_area_completeness.py` | partial |
| 8 Iterate | disposition per prong recorded in [`master-synthesis`](master-synthesis.md) §6 | ✅ done |

## 4. Prong structure

| Prong | Topic cluster | Question it answers |
|:---|:---|:---|
| **A** | `internal_area_doctrine` | How do WE currently define an area + completeness? (evidence-sweep) |
| **B** | `external_maturity_models` | How does industry rank governance/data maturity? (DAMA-DMBOK, DCAM, CMMI, EDM) |
| **C** | `external_domain_boundaries` | How does industry define a "domain/area" boundary? (DDD, Team Topologies, Data Mesh) |
| **D** | `completeness_and_value` | How is "complete" + "value-ranked" defined? (DoD/DoR, data-quality dims, weighting, WSJF) |

## 5. Folder shape (per research-action-craft Principle 4 worked example)

```
docs/wip/intelligence/area-completeness-doctrine-2026-06-05/
├── README.md                       (folder index)
├── research-action-pack.md         (this file — control layer)
├── source-ledger.csv               (ALL sources, canonical 13-field schema)
├── baseline-state-2026-06-05.md    (Steps 1-3: matrix refresh + regression + topography)
├── prong-a-internal-doctrine.md    (Stage 4 — internal)
├── prong-b-external-maturity.md    (Stage 4 — maturity models)
├── prong-c-domain-boundaries.md    (Stage 4 — what is an area)
├── prong-d-completeness-value.md   (Stage 4 — what is completeness)
└── master-synthesis.md             (cross-prong rollup + the definitional regression + option set)
```

## 6. Cross-references

- Discipline: [`RESEARCH_ACTION_DISCIPLINE.md`](../../../references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md)
- Subject under study: [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md) + `akos/hlk_area_completeness.py`
- Schema: [`akos/hlk_research_action.py`](../../../../akos/hlk_research_action.py) (13-field `ResearchSourceRow`)
- Validator: `py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/area-completeness-doctrine-2026-06-05/source-ledger.csv`
