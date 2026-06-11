---
title: Prong synthesis template — Automation OS (PESTEL + Porter skim)
intellectual_kind: research_synthesis_template
status: active
used_at_tranche: R11
---

# Prong synthesis template (`prong-pN-*.md`)

> **Not for ledger ingest** — use at R11 per-prong synthesis only. Each letter / force gets
> its own viewpoint on the **same prong subject** (Holistika methodology posture).

## Header

- Prong ID + functional name (charter §3)
- ICS tier + downstream consumer
- Source IDs cited (from cumulative ledger)

## PESTEL — six viewpoints (one bullet each)

| Letter | Viewpoint question | Your one-line finding |
|:---|:---|:---|
| **P** Political | Policy/regulatory pressure on this prong? | |
| **E** Economic | Cost/ROI pressure (CI minutes, registry maintenance)? | |
| **S** Social | Workforce/adoption friction for this automation? | |
| **T** Technological | Binding tech shift (substrate, runner, protocol)? | |
| **E** Environmental | Sustainability/ops footprint (if material; else N/A) | |
| **L** Legal | Audit/durability bar for registry edits? | |

Vault anchor: [`PESTEL_ANALYSIS.md`](../../../references/hlk/v3.0/Research/Methodology/Pillars/PESTEL_ANALYSIS.md)
(`hol_resea_dtp_315`). SOP: [`SOP-RESEARCH_PRONG_SYNTHESIS_001.md`](../../../references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_PRONG_SYNTHESIS_001.md).

## Porter — four forces + synthesis (competition is emergent)

| Force | Viewpoint question | Your one-line finding |
|:---|:---|:---|
| **1** Supplier power | Who supplies the capability this prong depends on? | |
| **2** Buyer power | Who can refuse / bypass this automation layer? | |
| **3** Substitutes | What replaces governed runbooks (one-offs, SaaS)? | |
| **4** New entrants | What lowers the bar to new scripts/adapters? | |
| **∴ Competition** | **Synthesis of 1–4** — competitive pressure on this prong | |

> Operator discipline: **competition is not a separate input** — it is the integrated result of
> the other four forces. Vault pillar:
> [`PORTER_COMPETITIVE_ANALYSIS.md`](../../../references/hlk/v3.0/Research/Methodology/Pillars/PORTER_COMPETITIVE_ANALYSIS.md).

## Automation OS hook

- Registry columns affected
- `research_ledger.py` behaviour
- Verify-profile step (if any)
