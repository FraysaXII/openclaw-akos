---
language: en
initiative_id: INIT-OPENCLAW_AKOS-78
title: Brand-voice LLM-as-judge advisory layer (Tier 2 evolution from I71 P1 strategic review)
status: closed
inception_date: 2026-05-14
last_review: 2026-05-19
closed_at: 2026-05-19
owner_role: Brand & Narrative Manager
co_owner_role: System Owner
inception_decision_id: D-IH-78-A
closure_decision_id: D-IH-78-CLOSURE
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

## Closure note (D-IH-78-CLOSURE, 2026-05-19)

I78 closed at **engineering-done** (P1 + P2 shipped) per the I86 cluster burndown plan §6 axis-2 pragmatic-closure executive call. P3 + P4 + P5 (Strand C bias audit, Strand D promotion-to-strict ratify, closure UAT) **forward-chartered** to a successor strict-mode-promotion follow-up initiative that activates when (a) operator configures a live LLM provider under `config/openclaw.json` and (b) Strand D `D-IH-78-PROMOTE` ratifies the quantitative bias-audit thresholds per C-78-4. Full closure trace in [`reports/2026-05-19-closure.md`](reports/2026-05-19-closure.md). Reversibility = single-diff flip of `status: closed → active` here + `INITIATIVE_REGISTRY.csv` row + new `D-IH-78-REOPEN` decision.

## Cross-references

- [`decision-log.md`](decision-log.md)
- [`reports/2026-05-19-closure.md`](reports/2026-05-19-closure.md) (closure report + 3 executive calls)
- [`71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md`](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md) § Tier 2 forward-charter
- [`scripts/validate_brand_voice_register.py`](../../../scripts/validate_brand_voice_register.py)
- [`akos/brand_voice_judge.py`](../../../akos/brand_voice_judge.py) (P1 chassis)
- [`scripts/judge_brand_voice.py`](../../../scripts/judge_brand_voice.py) (P1 CLI runbook)
- [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/judge-pack.yml`](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/_validators/judge-pack.yml) (operator-editable pack)
