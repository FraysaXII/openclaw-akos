---
title: HxPESTAL Intent Tracking Discipline
language: en
status: active
canonical: true
role_owner: Research Director + KM Officer
classification: way_of_working
intellectual_kind: discipline_charter
access_level: 4
authored: 2026-06-10
last_review: 2026-06-10
last_review_decision_id: D-IH-94-A
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-94-A
linked_canonicals:
  - ../Pillars/HXPESTAL_ANALYSIS.md
  - RESEARCH_PRONG_LATTICE_DISCIPLINE.md
  - RESEARCH_ACTION_DISCIPLINE.md
  - ../../Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_METHODOLOGY_MODE.md
linked_runbooks:
  - scripts/validate_research_action.py
evidence_base:
  - Automation OS 950-row charter; holistic-agentic 1,000-row charter
  - Operator ratification 2026-06-10 (AIC intent representation via large ledgers)
---

# HxPESTAL Intent Tracking Discipline

## 1. Purpose

Large research packs (300–1,000+ sources) only pay off when **master-synthesis** proves a flagship
AIC can **represent Holistika's intent** — not merely summarise URLs. This discipline mints the
**tracking artifact** for that proof: the intent fidelity record paired with every
`master-synthesis-hxpestel.md`.

**What it prevents:** ledger cargo-cult (volume without harmonised humanity viewpoint); activism
collapse (single-camp narrative); AIC drift (synthesis that contradicts governed Holistika posture).

## 2. When to mint the tracker

| Trigger | Artifact |
|:---|:---|
| Per-prong synthesis complete (all `BL-*` prongs) | Draft tracker — scores provisional |
| Master HxPESTAL pass (R11 / pack closure) | **Ratified tracker** — scores binding for govern stage |
| MADEIRA Methodology session on same pack | Append `madeira_methodology_notes` column |

## 3. Tracker fields (Markdown table — not ledger CSV)

| Field | Meaning |
|:---|:---|
| `pack_slug` | Research pack folder name |
| `ledger_row_count` | Cumulative `source-ledger.csv` rows at master-synthesis |
| `prongs_synthesized` | Count of `BL-*` prongs with completed `prong-*.md` |
| `h_harmonisation_score` | 1–5 — does master narrative hold Holistika holistic intent? |
| `activism_spectrum_coverage` | 1–5 — are ≥2 steering vectors named with tension explicit? |
| `pestel_letter_coverage` | 6 checkboxes P/E/S/T/A/L — each cited in master-synthesis |
| `porter_master_hook` | Y/N — competition synthesis present at master level (optional rollup) |
| `aic_flagship` | e.g. `MADEIRA` / other AIC id |
| `intent_fidelity_score` | 1–5 — operator judgment: does AIC output represent Holistika intent? |
| `intent_fidelity_rationale` | 2–4 sentences; falsifiable |
| `src_anchor_ids` | Representative `SRC-*` IDs supporting H + A scores |
| `esg_material` | Y when footprint/regulatory ESG is in scope — cite under A + S in master-synthesis |
| `govern_ready` | Y only if `intent_fidelity_score` ≥ 4 AND activism_spectrum ≥ 4 |

## 4. Value proposition (why large ledgers matter)

```mermaid
flowchart LR
  Ledger[1000-row ledger]
  Prong[Per-prong PESTEL/Porter]
  Master[HxPESTAL master]
  Track[Intent tracker]
  Govern[Govern stage]
  Ledger --> Prong --> Master --> Track --> Govern
```

Breadth across CORPINT + OSINT lets the **Activism** letter surface steering vectors that
single-prong skims miss. The tracker makes that value **auditable** — operator can see whether
the research spend converted into intent representation, not just row count.

## 5. MADEIRA integration

When **MADEIRA Methodology mode** drives synthesis:

- Methodology checkpoints may propose `D-IH-*` rows when intent fidelity fails.
- Brand dual-register check runs on master-synthesis external-facing paragraphs.
- Tracker `madeira_methodology_notes` captures surfaced candidates not yet ratified.

Reference: [`../../Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_METHODOLOGY_MODE.md`](../../Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_METHODOLOGY_MODE.md).

## 6. Verification

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/<pack>/source-ledger.csv
```

Tracker is human-audited at govern gate; automation confirms ledger shape only.

## 7. Cross-references

- Macro lens craft: [`../Pillars/HXPESTAL_ANALYSIS.md`](../Pillars/HXPESTAL_ANALYSIS.md)
- WIP template: `docs/wip/intelligence/<pack>/hxpestel-intent-tracking-template.md`
