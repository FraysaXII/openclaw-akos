---
title: Research Action Discipline
language: en
status: active
canonical: true
role_owner: Research Director + KM Officer
classification: way_of_working
intellectual_kind: discipline_charter
access_level: 4
authored: 2026-05-27
last_review: 2026-06-10
last_review_by: Lead Researcher
last_review_decision_id: D-IH-94-A
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-86-FF
  - D-IH-94-A
linked_runbooks:
  - scripts/validate_research_action.py
  - scripts/research_ledger.py
linked_canonicals:
  - RESEARCH_PRONG_LATTICE_DISCIPLINE.md
  - SOP-RESEARCH_PRONG_SYNTHESIS_001.md
  - docs/references/hlk/v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md
  - docs/references/hlk/v3.0/Research/Intelligence/canonicals/INTELLIGENCE_DISCIPLINE_CHARTER.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md
---

# Research Action Discipline

## 1. Purpose

Research Action is the discipline that turns research into governed decisions. It exists because raw synthesis is not enough: a role-owner must know what topic was researched, where each source came from, what format the information had, how reliable Holistika considers it, how credible an external reader would consider it, what workflow consumes it, and which decision it can support.

This discipline is Research-owned and cross-area consumed. Research authors the source ledger and findings; Marketing, People, Operations, Tech, Legal, and other areas consume the processed findings to author their own canonicals and outputs.

## 2. Source Ledger Contract

Every research action that can drive strategic / tactical / operational work carries a source ledger with these fields:

| Field | Meaning |
|:---|:---|
| `source_id` | Stable local source ID, prefixed `SRC-`. |
| `prong` | **Baseline consumer prong** (`BL-*` per `RESEARCH_PRONG_LATTICE_DISCIPLINE.md`). Charter aliases (`P1-TECH`, `P1-DATA`, …) normalize at ingest. PESTEL/Porter are synthesis lenses — not ledger tags. |
| `topic_cluster` | Topic family. |
| `source_title_or_owner` | Human-readable source name. |
| `url` | Public URL or repo-relative `docs/` path. |
| `format` | Article, report, book, dataset, podcast, webpage, video transcript, internal canonical, or internal transcript. |
| `source_category` | OSINT / HUMINT / SIGINT / CORPINT / MOTINT / TBD per `source_taxonomy.md`. |
| `source_level` | Numeric source-level value per `source_taxonomy.md`. |
| `holistika_reliability_score` | 1-5 internal reliability assessment. |
| `external_perceived_credibility_score` | 1-5 estimate of how credible the source appears to an external reader. |
| `control_confidence_level` | Safe / Euclid / Keter control intensity per `confidence_levels.md`. |
| `decision_use` | Which downstream decision or output can use the source. |
| `notes` | Limits, caveats, or why the source matters. |

The Pydantic SSOT is `akos/hlk_research_action.py`; the validator/runbook is `scripts/validate_research_action.py`.

### 2.1 Prong lattice (minted 2026-06-10)

Three layers — **do not conflate**:

1. **Baseline consumer prongs (`BL-*`)** — ledger column; 14 stable IDs across Holistika areas.
2. **Analytical lenses** — PESTEL (six letter viewpoints) + Porter (four forces + competition synthesis) at per-prong synthesis only.
3. **Charter aliases** — pack-local `P1-…` shorthand; map to `BL-*` before commit.

Full lattice + crosswalk tables: [`RESEARCH_PRONG_LATTICE_DISCIPLINE.md`](RESEARCH_PRONG_LATTICE_DISCIPLINE.md).
Synthesis craft: [`SOP-RESEARCH_PRONG_SYNTHESIS_001.md`](SOP-RESEARCH_PRONG_SYNTHESIS_001.md).

## 3. Operating Loop

1. **Ingest** sources and transcripts into a durable folder.
2. **Rate** every source in the source ledger.
3. **Rank** sources by relevance to the decision, not only by prestige.
4. **Synthesize** claim-level findings with internal-canonical mapping.
5. **Govern** by surfacing option sets only after the source ledger and synthesis are processed.
6. **Implement** in the owning area after the operator or role-owner ratifies.
7. **Test** with the relevant validator / UAT / render trail.
8. **Iterate** by promoting, rejecting, deferring, or keeping the topic on radar.

## 4. C1.6 Worked Example

Wave R+4 C1/C1.5 is the founding worked example. The initial C1 commit captured 7 prongs of research. The operator rejected immediate C2 canonical edits because the research lacked a governed action layer. C1.5 added `source-ledger.csv` and `research-action-pack.md`. C1.6 promotes that pattern to this discipline and adds the validator/runbook.

## 5. What This Discipline Prevents

- Research-as-ornament: sources cited but not mapped to decisions.
- Confidence drift: shorthand scores that do not match canonical confidence taxonomy.
- Premature governance: canonical edits proposed before source metadata and workflow are processed.
- Folder ambiguity: research artifacts placed somewhere without citing Research-area ownership.
- ERP/KB invisibility: research findings that cannot become a radar, source, finding, recommendation, or implementation link.

## 6. Verification

Minimum verification before research findings drive canonical edits:

```powershell
py scripts/validate_research_action.py --self-test
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/research-grounded-wave-r-plus-4-2026-05-27/source-ledger.csv
py scripts/test.py hlk tests/test_hlk_research_action.py tests/test_validate_research_action.py
py scripts/validate_hlk.py
```

## 7. Cross-References

- `RESEARCH_PRONG_LATTICE_DISCIPLINE.md` — baseline `BL-*` registry + charter alias crosswalk + PESTEL/Porter placement.
- `SOP-RESEARCH_PRONG_SYNTHESIS_001.md` — per-prong PESTEL + Porter synthesis SOP.
- `RESEARCH_AREA_CHARTER.md` — Research owns Tier 1 WIP and authors investigative artifacts.
- `INTELLIGENCE_DISCIPLINE_CHARTER.md` — Intelligence owns what we collect.
- `source_taxonomy.md` — source category, source level, and internal/public credibility scoring.
- `confidence_levels.md` — Safe / Euclid / Keter control-intensity taxonomy.
- `docs/wip/intelligence/research-grounded-wave-r-plus-4-2026-05-27/research-action-pack.md` — founding C1.5 action pack.
