---
language: en
status: draft
intellectual_kind: research_action_pack
sharing_label: internal_only
audience: J-OP;J-AIC
role_owner: Research Director + KM Officer
authored: 2026-05-28
last_review: 2026-05-28
linked_sources:
  - source-ledger.csv
  - master-synthesis.md
  - model-routing-map.md
  - prong-ms-open-source-llms-and-local-routing.md
  - prong-ms-multimodal-image-video-3d.md
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SOP-RESEARCH_ACTION_001.md
  - docs/wip/intelligence/README.md
---

# Model-selection research action pack (Option B — full knowledge base)

## 1. Why this pack exists

The operator ratified **Option B**: expand the minimal Cursor-only recommendation
into a **full model-selection knowledge base** — open-source LLMs plus image /
video / 3D — built under the **research-to-decision discipline** (the rulebook
that requires a source log with trust scores before synthesis drives decisions).

Option A (minimal Cursor note only) shipped first for budget; this pack is the
**Option B viability test on Composer 2.5** (cheap model doing interpretive
research, not just execution).

## 2. Artifact inventory (Option B contract)

| Artifact | Purpose | Status |
|:---|:---|:---|
| `source-ledger.csv` | 25 scored sources (MS + MS-OSS + MS-MM) | **draft** |
| `prong-ms-open-source-llms-and-local-routing.md` | OSS/self-host prong synthesis | **draft** |
| `prong-ms-multimodal-image-video-3d.md` | Image/video/3D prong synthesis | **draft** |
| `master-synthesis.md` | Cross-prong rollup + decision questions | **draft** |
| `model-routing-map.md` | Operator lookup: task → model class | **draft** |
| `recommendation-note.md` | Executive summary (updated) | **draft** |
| `field-test-note.md` | Composer safety net + iteration log | **draft** |
| `README.md` | Folder index | **draft** |

Not in scope for this WIP tranche (forward-charter):

- `MEDIA_GENERATION_REGISTRY.csv` (new dimension CSV)
- Supabase mirror DDL

Ratified in scope (DQ-MS-03, 2026-05-28):

- `SUBSTRATE_REGISTRY.csv` candidate rows: `SUBS-DEEPSEEK-DEEPSEEK-V4`,
  `SUBS-MOONSHOT-KIMI-K26`

## 3. Operating loop status

| Stage | Evidence |
|:---|:---|
| **Ingest** | 15 new ledger rows + 10 prior Cursor rows |
| **Rate** | holistika_reliability_score + control_confidence_level on every row |
| **Rank** | Ranked options in each prong (not flat conclusions) |
| **Synthesize** | 2 prongs + master + routing map |
| **Govern** | DQ-MS-01..06 ratified 2026-05-28 | [`operator-ratification-2026-05-28.md`](operator-ratification-2026-05-28.md) |
| **Implement** | SUBSTRATE candidate rows minted; model-tiers forward | Partial |
| **Test** | `validate_research_action.py --source-ledger` at commit time |
| **Iterate** | Field-test iteration 1 logged in field-test-note |

## 4. Placement

Folder: `docs/wip/intelligence/model-selection-2026-05-28/` under Tier 1 WIP
(Research-owned per `docs/wip/intelligence/README.md`).

Cross-link from:

- `docs/wip/intelligence/model-selection-2026-05-28/recommendation-note.md`
  (operator daily driver)
- Future I84 substrate initiative when SUBSTRATE rows promote

## 5. Validator command

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/model-selection-2026-05-28/source-ledger.csv
```

Self-test (always on pre_commit):

```powershell
py scripts/validate_research_action.py --self-test
```

## 6. Anti-patterns avoided

- **Research-as-ornament:** every prong ends with operator ratification questions.
- **False precision:** benchmark scores cited with skeptic sources paired.
- **Premature governance:** no canonical CSV edits without operator gate.
- **Folder ambiguity:** README + pack index name all artifacts.

## 7. Next commit message shape (when operator asks)

```
docs(intelligence): model-selection Option B KB — OSS + multimodal prongs

Research-to-decision expansion of model-selection-2026-05-28: 25-row
source ledger, MS-OSS + MS-MM prongs, master synthesis, routing map.
Composer 2.5 field-test iteration 1. No canonical CSV changes.
```
