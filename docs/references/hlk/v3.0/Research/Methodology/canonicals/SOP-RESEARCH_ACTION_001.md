---
title: SOP - Research Action
language: en
intellectual_kind: research-area-canonical-sop
sop_id: SOP-RESEARCH_ACTION_001
access_level: 4
confidence_level: Euclid
source_taxonomy: holistika-internal-sop
authors:
  - Research Director
  - KM Officer
  - System Owner
last_review: 2026-05-27
last_review_by: Founder
last_review_decision_id: D-IH-86-FF
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-86-FF
status: active
register: internal
linked_canonicals:
  - RESEARCH_ACTION_DISCIPLINE.md
  - source_taxonomy.md
  - confidence_levels.md
linked_runbooks:
  - scripts/validate_research_action.py
cadence: on_demand
---

# SOP - Research Action

## Purpose

Execute a governed research action before research findings drive canonical edits, external outputs, ERP workflows, or strategic decisions.

## Acceptance Criteria

- **AC-HUMAN**: a Research Director, KM Officer, Founder, or AIC can fill a source ledger, review findings, and surface decision questions without invoking the validator.
- **AC-AUTOMATION**: `py scripts/validate_research_action.py --source-ledger <path>` validates the source ledger header, row shape, scoring bounds, source taxonomy values, uniqueness, and control confidence values.

## Inputs

- A research question or operator request.
- Source material: public URLs, transcripts, internal canonicals, datasets, or engagement intelligence.
- `source_taxonomy.md` and `confidence_levels.md`.
- A target downstream decision or output.

## Steps

1. **Open a research action folder.** Use `docs/wip/intelligence/<slug>/` unless a future Research topology decision renames or aliases Tier 1 WIP.
2. **Ingest sources.** Save transcripts or durable links. Do not rely on chat memory.
3. **Create `source-ledger.csv`.** Use the exact field order in `akos/hlk_research_action.py`.
4. **Rate every source.** Assign source category, source level, Holistika reliability, external perceived credibility, and control confidence.
5. **Write prong synthesis.** Each claim cites sources and maps to existing Holistika canonicals or gaps.
6. **Write master synthesis.** Summarize load-bearing claims and downstream decisions.
7. **Run the validator.**

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/<slug>/source-ledger.csv
```

8. **Surface decisions only after validation.** Canonical CSV gates, doctrine amendments, and external artifacts can only proceed once the source ledger validates and the master synthesis names the decision-use.
9. **Close the loop.** The implementation commit cites the research bundle paths in decision rationales, CHANGELOG, and initiative tracking rows.

## Failure Modes

| Failure | Recovery |
|:---|:---|
| Source cited in prose but missing from ledger. | Add ledger row before using it for a decision. |
| Source has high external credibility but low Holistika reliability. | Use it as framing, not as a load-bearing internal decision source. |
| Source has high Holistika reliability but low external credibility. | Use it internally; translate or corroborate before external prose. |
| Control confidence is Keter. | Require stronger validation before canonical edits. |
| Decision questions are implementation-shaped too early. | Return to source ledger + master synthesis and recompose options. |

## Outputs

- `source-ledger.csv`.
- Prong synthesis files.
- Master synthesis.
- Decision questions or decision-row drafts.
- Validator output.

## Cross-References

- `RESEARCH_ACTION_DISCIPLINE.md`.
- `scripts/validate_research_action.py`.
- `akos/hlk_research_action.py`.
- `docs/wip/intelligence/README.md`.
