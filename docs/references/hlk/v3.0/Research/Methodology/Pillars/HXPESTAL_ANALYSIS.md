---
title: HxPESTAL Analysis — Holistika Macro Lens
language: en
status: active
canonical: true
intellectual_kind: methodology_pillar
role_owner: Lead Researcher
capability_id: CAP-HOL-RESEA-DTP-99
process_list_ref: hol_resea_dtp_99
authored: 2026-06-10
last_review: 2026-06-10
last_review_decision_id: D-IH-94-A
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-94-A
linked_canonicals:
  - ../canonicals/RESEARCH_PRONG_LATTICE_DISCIPLINE.md
  - ../canonicals/HXPESTAL_INTENT_TRACKING_DISCIPLINE.md
  - PESTEL_ANALYSIS.md
  - ../../Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_METHODOLOGY_MODE.md
evidence_base:
  - Operator ratification 2026-06-10 (activism + humanity framing)
  - Automation OS + holistic-agentic cumulative ledgers (300–1000 sources)
---

# HxPESTAL Analysis — Holistika macro lens

> **Master-synthesis pillar** (`hol_resea_dtp_99`). Sits **above** per-prong PESTEL/Porter skims.
> Answers: *given everything we collected, where is humanity trying to steer — and does our
> synthesis represent Holistika's intent?*

## 1. Structure (binding)

```
HxPESTAL = H  ×  PESTAL
           │      └── Political · Economic · Social · Technological · Activism · Legal
           └── Humanity / Holistik / Harmonisation (operational English for harmonisation)
```

| Layer | Symbol | Functional meaning |
|:---|:---|:---|
| **H** | Humanity prefix | Holistika's **holistic** viewpoint — harmonisation across dimensions humans care about. *Harmonisation* is operational English only; not a universal Holistika brand string. |
| **×** | Cross-product | Every PESTAL letter is read **through** the H lens — not as detached macro trivia. |
| **P** | Political | Power, policy, institutions shaping the topic. |
| **E** | Economic | Value, cost, incentives, distribution. |
| **S** | Social | Culture, adoption, equity, collective behaviour. |
| **T** | Technological | Capability shifts, substrate, automation posture. |
| **A** | **Activism** | **Where humans are trying to steer** — movements, advocacy, intent vectors, full-spectrum positions on the topic. Research **all relevant spectrums**; do not collapse to a single camp. |
| **L** | Legal | Hard constraints, liability, compliance bars. |

> **Activism replaces Environmental** in classic PESTEL for this pillar (operator ratification
> 2026-06-10 — closer to real people and Holistika brand posture than a detached ESG checkbox).

### ESG without a separate Environmental letter

ESG pressure is **not dropped** — it is **governed semantically** through:

| ESG signal | HxPESTAL route |
|:---|:---|
| Climate / footprint materiality | **A** (activist steering) + **S** (collective stake) |
| Regulatory disclosure (CSRD, etc.) | **L** + **P** |
| Stakeholder capitalism narratives | **S** + **H** harmonisation |

When ESG is material to the pack, set `esg_material: true` on the intent tracker and cite footprint
sources in the **A** and **S** rows. Per-prong PESTEL skims may still use Environmental viewpoint
for source-level tagging; master HxPESTAL holds the Holistika macro posture.

## 2. Placement in the research loop

| Stage | Craft | Granularity |
|:---|:---|:---|
| Ingest / Rate | Source ledger | `BL-*` consumer prongs only |
| Synthesize (per prong) | PESTEL + Porter | One prong subject at a time |
| **Synthesize (master)** | **HxPESTAL** | Whole pack / whole initiative |
| Govern | Option sets | After HxPESTAL intent check passes |

See [`../canonicals/RESEARCH_PRONG_LATTICE_DISCIPLINE.md`](../canonicals/RESEARCH_PRONG_LATTICE_DISCIPLINE.md) §5.

## 3. AIC flagship representation (MADEIRA)

**MADEIRA Methodology mode** is the primary vehicle for demonstrating whether a flagship AIC can
**represent Holistika intent** through the full research procedure:

1. Large cumulative ledger (hundreds–thousands of `SRC-*` rows) supplies evidence breadth.
2. Per-prong PESTEL/Porter skims compress prong-level signal.
3. **HxPESTAL master pass** asks: does the cross-prong narrative honour the **H** lens and capture
   **activism spectrums** without flattening dissent?
4. Operator scores **intent fidelity** per [`../canonicals/HXPESTAL_INTENT_TRACKING_DISCIPLINE.md`](../canonicals/HXPESTAL_INTENT_TRACKING_DISCIPLINE.md).

Other flagship AICs use the same tracker shape; MADEIRA is the worked example because Methodology
mode is always-on underlay per [`../../Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_METHODOLOGY_MODE.md`](../../Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_METHODOLOGY_MODE.md).

## 4. Output shape (master-synthesis)

File pattern: `master-synthesis-hxpestel.md` in the research pack.

1. **H harmonisation paragraph** — what Holistika is trying to hold together across prongs.
2. **PESTAL table** — one row per letter; cite cross-prong `SRC-*` IDs (not every row — representative + outliers).
3. **Activism spectrum** — minimum two steering vectors named; tensions explicit.
4. **Intent fidelity block** — operator + AIC scores per intent tracker.

WIP template: `docs/wip/intelligence/<pack>/hxpestel-intent-tracking-template.md`.

## 5. Cross-references

- Per-prong execution: [`PESTEL_ANALYSIS.md`](PESTEL_ANALYSIS.md)
- Intent tracking: [`../canonicals/HXPESTAL_INTENT_TRACKING_DISCIPLINE.md`](../canonicals/HXPESTAL_INTENT_TRACKING_DISCIPLINE.md)
- Synthesis SOP: [`../canonicals/SOP-RESEARCH_PRONG_SYNTHESIS_001.md`](../canonicals/SOP-RESEARCH_PRONG_SYNTHESIS_001.md)
