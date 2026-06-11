---
title: SOP - Research Prong Synthesis
language: en
intellectual_kind: research-area-canonical-sop
sop_id: SOP-RESEARCH_PRONG_SYNTHESIS_001
access_level: 4
confidence_level: Euclid
source_taxonomy: holistika-internal-sop
authors:
  - Lead Researcher
  - KM Officer
last_review: 2026-06-10
last_review_by: Lead Researcher
last_review_decision_id: D-IH-94-A
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-86-FF
  - D-IH-94-A
status: active
register: internal
linked_canonicals:
  - RESEARCH_PRONG_LATTICE_DISCIPLINE.md
  - RESEARCH_ACTION_DISCIPLINE.md
  - ../Pillars/PESTEL_ANALYSIS.md
  - ../Pillars/PORTER_COMPETITIVE_ANALYSIS.md
cadence: on_demand
---

# SOP — Research Prong Synthesis

## Purpose

Execute **per-prong synthesis** at Research Action stage 4 (Synthesize) using baseline consumer prongs
(`BL-*`) plus PESTEL and Porter analytical lenses. Prevents charter-alias drift and conflating ledger
tags with macro-environment viewpoints.

## Acceptance Criteria

- **AC-HUMAN**: author can produce one `prong-*.md` per baseline prong with PESTEL six-viewpoint +
  Porter four-force + competition synthesis sections citing `SRC-*` IDs.
- **AC-AUTOMATION**: ledger `prong` values normalize to `BL-*` via `akos.research_ledger_ops.normalize_prong`;
  `validate_research_action.py --source-ledger` PASS.

## Steps

1. **Resolve baseline prong** — map charter alias (`P1-TECH`, `P1-DATA`, …) to `BL-*` per
   [`RESEARCH_PRONG_LATTICE_DISCIPLINE.md`](RESEARCH_PRONG_LATTICE_DISCIPLINE.md) §4.
2. **Filter ledger** — select cumulative `source-ledger.csv` rows where `prong` matches baseline ID
   (after normalization).
3. **Draft synthesis header** — prong ID, functional name, ICS tier, downstream consumer, cited source IDs.
4. **PESTEL pass** — six separate viewpoints (P/E/S/T/E/L) per
   [`../Pillars/PESTEL_ANALYSIS.md`](../Pillars/PESTEL_ANALYSIS.md).
5. **Porter pass** — four force viewpoints + **competition as synthesis of 1–4** per
   [`../Pillars/PORTER_COMPETITIVE_ANALYSIS.md`](../Pillars/PORTER_COMPETITIVE_ANALYSIS.md).
6. **Pack hook** — registry columns, engine behaviour, verify step (pack-specific).
7. **Feed master-synthesis** — after all prongs: `master-synthesis-hxpestel.md` per
   [`../Pillars/HXPESTAL_ANALYSIS.md`](../Pillars/HXPESTAL_ANALYSIS.md) + intent tracker per
   [`HXPESTAL_INTENT_TRACKING_DISCIPLINE.md`](HXPESTAL_INTENT_TRACKING_DISCIPLINE.md).

## WIP template

Pack-local copy: `docs/wip/intelligence/<pack>/prong-synthesis-template.md` — must stay aligned with
this SOP when edited.

## Cross-references

- Research Action loop: [`SOP-RESEARCH_ACTION_001.md`](SOP-RESEARCH_ACTION_001.md)
- Engine: [`scripts/research_ledger.py`](../../../../../../scripts/research_ledger.py)
