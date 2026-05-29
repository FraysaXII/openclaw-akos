---
title: Model selection research action (2026-05-28)
language: en
intellectual_kind: wip_intelligence_index
sharing_label: internal_only
audience: J-OP
authored: 2026-05-28
last_review: 2026-05-28
status: draft
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
---

# Model selection — research action folder (Option B)

> Governed research action: **which models** should drive Holistika work
> across Cursor IDE, open-source/self-hosted LLMs, and image/video/3D —
> built with the **research-to-decision discipline** (source ledger with
> trust scores → prong syntheses → master rollup → routing map).

## What's here

| File | What it is |
|:---|:---|
| `source-ledger.csv` | **25** scored sources (MS + MS-OSS + MS-MM prongs) |
| `recommendation-note.md` | Executive summary — start here |
| `model-routing-map.md` | Task → model class lookup table |
| `prong-ms-open-source-llms-and-local-routing.md` | OSS / RunPod / Ollama prong |
| `prong-ms-multimodal-image-video-3d.md` | Image / video / 3D prong |
| `master-synthesis.md` | Cross-prong rollup + decision questions |
| `research-action-pack.md` | Pack contract + operating-loop status |
| `operator-ratification-2026-05-28.md` | DQ-MS-01..06 operator verdicts |
| `field-test-note.md` | Composer 2.5 safety net + iteration log |

## Scope

- **In scope:** routing recommendations, WIP syntheses, internal CORPINT
  cross-refs (`model-catalog.json`, substrate audit).
- **Out of scope (forward-charter):** `MEDIA_GENERATION_REGISTRY.csv`, Supabase
  mirrors — require canonical CSV gate.
- **In scope (ratified 2026-05-28):** `SUBSTRATE_REGISTRY.csv` **candidate**
  rows for DeepSeek V4 + Kimi K2.6 (DQ-MS-03).

## Field test (Composer 2.5)

Option B expansion **is** the interpretive field test. See
`field-test-note.md` §"Iteration 1" for agent self-assessment; operator
fills §"Your verdict".

## Validator

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/model-selection-2026-05-28/source-ledger.csv
```

## Status

Tier-1 WIP intelligence (`draft`). Governance decisions DQ-MS-01..06
**ratified** 2026-05-28 — see `operator-ratification-2026-05-28.md`. Composer
field-test operator verdict still optional in `field-test-note.md`.

## Sibling research action

The model-routing directive (which model-seat drives which session) is an
instantiation of a broader agentic-entity taxonomy. That taxonomy + the
"is AKOS an agentic operating system?" question is researched separately at
[`../agentic-os-and-aic-taxonomy-2026-05-29/`](../agentic-os-and-aic-taxonomy-2026-05-29/)
(spawned 2026-05-29 from this folder's routing conversation). Read its
`master-synthesis.md` before homing or minting any model-routing rule.
