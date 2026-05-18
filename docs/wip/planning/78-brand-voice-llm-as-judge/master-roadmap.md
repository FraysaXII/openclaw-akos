---
language: en
initiative_id: INIT-OPENCLAW_AKOS-78
title: Brand-voice LLM-as-judge advisory layer (Tier 2 evolution from I71 P1 strategic review)
status: active
inception_date: 2026-05-14
last_review: 2026-05-17
owner_role: Brand & Narrative Manager
co_owner_role: System Owner
inception_decision_id: D-IH-78-A
authority: Founder + Brand Manager + System Owner
---

# I78 — Brand-voice LLM-as-judge advisory layer

## SSOT split

| Surface | Role |
|:---|:---|
| [`docs/wip/planning/_candidates/i78-brand-voice-llm-judge.md`](../_candidates/i78-brand-voice-llm-judge.md) | Deep scaffold — strands, phase grid, conundrums, TRIGGER-derived **bias-audit / strict-mode promotion** posture (still binding for Strand D). |
| **`INITIATIVE_REGISTRY.csv`** row `INIT-OPENCLAW_AKOS-78` | Governed lifecycle metadata (`status: active` per **`D-IH-78-A`** — operator-directed mint 2026-05-17). |

## Reality check (engineering state)

**Delivered today**

- Strategic charter + architecture narrative + governance hooks across CHANGELOG, planning templates, and `DECISION_REGISTER` **`D-IH-78-A`**.

**Not yet shipped** (P1 execution backlog)

- `akos/brand_voice_judge.py`, `scripts/judge_brand_voice.py`, release-gate `[INFO]` row — candidate Strand B; codebase grep confirms **no** judge module as of registry mint.

**Neighbor initiatives**

- **I71** (closed): deterministic Pack A1 + Vale floor — I78 stacks **above** this layer per candidate §Operating story.
- **I52**: persona/eval LLM-judge harness — **different scope** from marketing brand-voice judge unless explicitly bridged later.

## Phase posture (from candidate §4 — execution)

| Phase | Focus |
|:---:|:---|
| **P0** | ~~Charter + registry~~ — **complete** (`D-IH-78-A` + `INIT-OPENCLAW_AKOS-78`). |
| **P1** | Pydantic judge chassis + CLI + provider abstraction + caching |
| **P2** | Release-gate advisory (`INFO`) + WORKSPACE cross-links + tests |
| **P3** | Bias-audit cadence launch |
| **P4** | Promotion-to-strict ratification (`D-IH-78-PROMOTE` — mint at gate time) |
| **P5** | Closure UAT |

## Verification

- Registry sync: `py scripts/validate_initiative_registry_frontmatter_sync.py`
- Umbrella: `py scripts/validate_hlk.py`
- Mirror emit when `.csv` mint touches mirrors operator workflow: `py scripts/verify.py compliance_mirror_emit` (if initiative mirror parity CI expects emit artefacts refreshed).

## Cross-references

- [`decision-log.md`](decision-log.md)
- [`71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md`](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md) § Tier 2 forward-charter
- [`scripts/validate_brand_voice_register.py`](../../../scripts/validate_brand_voice_register.py)
