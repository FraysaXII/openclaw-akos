---
name: research-action-craft
description: Use when authoring or extending a research action in this AKOS workspace — any external research sweep, source-ledger build, or research synthesis intended to feed a downstream canonical edit / runbook activation / brief authoring / external deliverable. Codifies the craft for walking the 8-stage operating loop (ingest → rate → rank → synthesize → govern → implement → test → iterate) without falling into the 5 anti-patterns the discipline exists to prevent. Triggers on phrases like research action, source ledger, source-ledger.csv, research synthesis, prong synthesis, master-synthesis, research-action-pack, ingest-rate-rank-govern, RESEARCH_ACTION_DISCIPLINE, validate_research_action, Holistika reliability score, control confidence level (Safe / Euclid / Keter). Pairs with .cursor/rules/akos-research-action.mdc (the WHEN); this skill is the HOW.
---

# Research Action Craft

The 15th Quality Fabric specialty (minted Wave R+4 C1.6 per
`D-IH-86-FF`) names a research action as **the act of converting raw
research into governed decisions through a structured 8-stage loop
backed by a per-source ledger**. This skill is the craft layer: how
to walk the loop well enough that the operator (or another agent)
can act on the output without re-doing the work.

## Operator framing that motivated the mint (verbatim)

> *"I wwn't rapprrove C2 uuntil i geet a proper research actiion. mabe
> yo did research utt i don't know and i don'tt know ohw we that
> researrchh was dnoe or if i's a reseerach actin that really goes
> well withh or alreadyy minted loogicc and already rreated arttifats."*
> — operator, 2026-05-27

The instruction surfaced when the agent attempted to move from C1
research substrate directly to C2 canonical edits. The C1.5 + C1.6
work formalized the missing layer.

## The 8-stage operating loop (RULE 2 binding)

| # | Stage | Output | Failure mode if skipped |
|:--|:---|:---|:---|
| 1 | **Ingest** | Sources captured into a dated WIP folder; transcripts saved durably | Sources cited from memory; no audit trail |
| 2 | **Rate** | Each source carries `holistika_reliability_score`, `external_perceived_credibility_score`, `control_confidence_level` | Reliability shorthand drifts from canonical taxonomy |
| 3 | **Rank** | Sources ordered by relevance to the named decision (not by prestige) | Big names crowd out load-bearing operational sources |
| 4 | **Synthesize** | Per-prong markdown synthesis citing source IDs + internal canonicals | Findings unmapped to repo state |
| 5 | **Govern** | Option set surfaced via inline-ratify gate per `akos-inline-ratification.mdc` | Canonical edits proposed before operator picks |
| 6 | **Implement** | Owning area edits the canonical / mints the runbook / authors the artifact | Stage-4 synthesis dies as a "we should" prose blob |
| 7 | **Test** | Validator self-test PASS + per-canonical validator clean + render trail if external | Edits land then break sibling validators |
| 8 | **Iterate** | Promotion / rejection / deferral logged; topic stays on radar OR retires | Research debt accumulates silently across waves |

## Six load-bearing principles for the craft

### Principle 1 — Pick the decision first, the research second

A research action without a named downstream decision becomes
ornament. Before opening the WIP folder, the agent answers:
**which canonical / runbook / artifact will this research feed?**
The answer goes into the `decision_use` column of every ledger row.

Worked example (good): "C2 governance surfaces need to know whether
J-IN should split into sub-personas, and if so how many." Decision
is named; every source rates against this question.

Worked example (bad): "Research investor segmentation broadly."
Without a decision target, every prestigious-looking source ends up
in the ledger with no rank discipline.

### Principle 2 — Author the ledger as you ingest, not after

Open `source-ledger.csv` BEFORE reading the first source. Each
source goes in as you ingest it, fields populated in real time.
Retrospective ledger authoring after a synthesis is the most common
source of confidence drift (Stage 2 failure) — the agent rebuilds
scores from memory rather than from the lived ingestion.

The Pydantic SSOT at `akos/hlk_research_action.py` enforces the field
shapes; `scripts/validate_research_action.py --source-ledger <path>`
catches drift the moment you save.

### Principle 3 — Anchor scoring against `source_taxonomy.md` and `confidence_levels.md`

`holistika_reliability_score` and `external_perceived_credibility_score`
are NOT the same axis. The first is **our** read of whether the source
holds; the second is **what an external auditor or counterparty would
think** if we cited it. A McKinsey report often scores 3-3 on the
first and 5-5 on the second; an internal-canonical doctrine often
scores 5-5 on the first and 2-3 on the second (because external
readers don't yet have access to it).

`control_confidence_level` maps to the canonical `confidence_levels.md`
Safe / Euclid / Keter taxonomy. Treat anything below Safe as a
finding to surface (RULE 1 of `akos-inline-ratification.mdc`
Principle 1 evidence-sweep applies to scoring decisions, not just to
canonical edits).

### Principle 4 — Synthesize per-prong, not per-source

Stage 4 produces one markdown file per research prong (or topic
cluster), not one per source. The synthesis cites source IDs by
their `source_id` and threads the per-prong narrative through the
canonical findings. This makes the synthesis itself queryable
("which prong claims X?") and decouples the synthesis cadence from
the ingest cadence.

Worked example folder shape from Wave R+4 C1:
```
docs/wip/intelligence/research-grounded-wave-r-plus-4-2026-05-27/
├── README.md                 (folder index)
├── research-pipeline.md      (the 8-stage doctrine application)
├── source-ledger.csv         (ALL sources cross-prong)
├── research-action-pack.md   (control layer; C1.5 mint)
├── prong-a-*.md              (one synthesis per prong)
├── prong-b-*.md
├── ...
└── master-synthesis.md       (cross-prong rollup; cites prong files)
```

### Principle 5 — Surface decisions as option sets, not as conclusions

Stage 5 governance happens via inline-ratify per
`akos-inline-ratification.mdc`. The synthesis must produce a
**ranked option set** for each downstream decision, NOT a single
"recommended action" presented as fait accompli. Each option carries
the rationale embedded inline (Principle 2 of
`inline-ratify-craft`); the operator picks; ratification triggers
Stage 6 implementation.

Worked example (good): "For J-IN sub-persona granularity, three
options surfaced: (a) 5 sub-personas with Decline-Class as
qualification metadata [recommended — research-grounded; matches NUVC
9 archetypes consolidated]; (b) 6 sub-personas with Decline-Class as
its own row [matches operator's verbatim 6-type framing but mixes
qualification axis with persona axis]; (c) keep J-IN single-row and
defer segmentation to C4 brief authoring [zero scope but loses
governance benefit]."

Worked example (bad): "Recommendation: split J-IN into 5 sub-personas."
Single conclusion; no option set; operator has no surface to push back
without rejecting the whole synthesis.

### Principle 6 — Iterate explicitly; retire OR keep on radar

Stage 8 is the often-missed close. Every research action commits an
explicit disposition per topic cluster: **promoted** (became canonical
edit / runbook), **rejected** (no evidence supports the framing),
**deferred** (kept in WIP for next wave), or **on-radar** (no
immediate action but topic stays in the source ledger for refresh).
Topics without explicit disposition become research debt — the agent
or operator returns months later wondering whether the prong is
still hot.

## Pre-flight checklist (walk before saving the synthesis)

1. ☐ Is the downstream decision named in plain language, not in
   internal jargon?
2. ☐ Is `source-ledger.csv` populated for every cited source (not
   just the load-bearing ones)?
3. ☐ Does every ledger row have a non-empty `decision_use` column?
4. ☐ Have reliability + credibility scores been graded against the
   canonical taxonomy (`source_taxonomy.md`)?
5. ☐ Has `control_confidence_level` been set per
   `confidence_levels.md` (Safe / Euclid / Keter)?
6. ☐ Does each prong synthesis cite source IDs (not bare URLs)?
7. ☐ Is the option set ranked + rationale embedded inline per
   `inline-ratify-craft` Principle 2?
8. ☐ Has `scripts/validate_research_action.py --source-ledger <path>`
   been run and PASSED?
9. ☐ Is the folder shape consistent with the Wave R+4 C1 worked
   example (README + research-pipeline + source-ledger +
   action-pack + per-prong + master-synthesis)?
10. ☐ Has the C5 disposition (promoted / rejected / deferred / on-radar)
    been named per topic?

If any item fails, fix BEFORE surfacing the inline-ratify gate to
the operator. Surfacing a half-formed ledger forces the operator to
do the synthesis work — that defeats the discipline.

## Anti-patterns

- **Research-as-ornament.** Source cited in synthesis prose but not
  in the ledger. Symptom: ledger row count < citation count.
- **Confidence drift.** Reliability score authored from memory after
  the fact, doesn't match what `source_taxonomy.md` says about that
  source class.
- **Premature governance.** Canonical edit proposed before the
  source ledger lands. Symptom: PR diff contains canonical changes
  but no `source-ledger.csv` change.
- **Folder ambiguity.** Research artifact lives somewhere other than
  `docs/wip/intelligence/<dated-folder>/` without citing Research-
  area ownership. Symptom: governance commit fails to link
  `linked_research_sources` to a stable folder path.
- **ERP/KB invisibility.** Research finding lands but cannot become
  a radar entry / source citation / finding row / recommendation /
  implementation link. Symptom: 6 months later the work is
  irrecoverable from the KB.

## Recovery patterns

- **If the operator rejects the synthesis as "not a real research
  action"** (Wave R+4 C1 → C1.5 precedent): mint the source ledger
  retroactively at C-NN.5, then a research-action-pack to document
  the metadata schema + workflow, then re-run the synthesis stage
  citing IDs from the ledger.
- **If the source ledger validator fails on a fixture row**: do NOT
  loosen the Pydantic constraints. Either fix the row data or
  surface the schema gap as a successor decision row that amends
  the SSOT explicitly.
- **If a research prong yields no actionable finding**: dispose it
  as **rejected** in Stage 8 with a one-line reason. Empty prongs
  are signal, not failure.

## Cross-references

- Paired rule: [`akos-research-action.mdc`](../../rules/akos-research-action.mdc)
  (the *when* + binding rules).
- Parent canonical: [`RESEARCH_ACTION_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md).
- Parent meta-discipline: [`akos-applied-research-discipline.mdc`](../../rules/akos-applied-research-discipline.mdc)
  + [`RESEARCH_HEAD_DISCIPLINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md).
- Sister inline-ratify craft: [`.cursor/skills/inline-ratify-craft/SKILL.md`](../inline-ratify-craft/SKILL.md)
  (governance stage 5 mechanics).
- Pydantic SSOT: [`akos/hlk_research_action.py`](../../../akos/hlk_research_action.py).
- Validator + runbook: [`scripts/validate_research_action.py`](../../../scripts/validate_research_action.py).
- SOP: [`SOP-RESEARCH_ACTION_001.md`](../../../docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_ACTION_001.md).
- Founding worked example: [`docs/wip/intelligence/research-grounded-wave-r-plus-4-2026-05-27/`](../../../docs/wip/intelligence/research-grounded-wave-r-plus-4-2026-05-27/)
  + the C1.5 `research-action-pack.md` that documents the metadata
  schema + workflow.
- Source taxonomy: [`source_taxonomy.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md).
- Control confidence taxonomy: [`confidence_levels.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md).
- Ratifying decision: D-IH-86-FF (active mint Wave R+4 C1.6, 2026-05-27).
