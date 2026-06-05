---
title: Intent-Ranked Regression Discipline
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder/CEO
co_authors:
  - PMO
  - System Owner
last_review: 2026-06-05
last_review_by: Founder/CEO
last_review_at: 2026-06-05
last_review_decision_id: D-IH-88-F
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-88-F
status: active
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - UAT_DISCIPLINE.md
  - ../Compliance/canonicals/PRECEDENCE.md
linked_cursor_rules:
  - .cursor/rules/akos-intent-ranked-regression.mdc
  - .cursor/rules/akos-inter-wave-regression.mdc
  - .cursor/rules/akos-inline-ratification.mdc
linked_skills:
  - .cursor/skills/intent-ranked-regression-craft/SKILL.md
linked_runbooks:
  - scripts/intent_ranked_regression.py
companion_to:
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
---

# Intent-Ranked Regression Discipline

> The People-area canonical that names **how to decide what to regress first** when
> attention (operator review minutes or agent context budget) is scarce. It is the
> **value layer** above [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md):
> that discipline asks *is everything wired?* (13 structural dimensions at ~equal
> weight); this one asks *is what the operator cares about most still served?* and
> orders the sweep by it. Minted 2026-06-05 from the operator's framing — *"not
> mechanical: take all my intents, use cases, logic, scenarios, interactions
> (past/present/future), rank them, research inside and outside, review, then
> regress"* — ratified under **D-IH-88-F**.

## 1. Purpose

A flat full-sweep (`release-gate.py`) answers integrity, not **priority**: a "9
failed" line buries the one finding that endangers a load-bearing goal among eight
that do not. This discipline ranks **regression surfaces** by an **Intent
Criticality Score (ICS)** so the highest-stakes surfaces are checked first and
deepest, and every finding is **attributed** (new / pre-existing / known-deferred)
before it is reported. The full mechanical sweep remains the periodic safety net —
this layer sits on top of it, never replaces it.

## 2. External grounding (cited, not invented)

| Frame | Source (reliability) | Contribution |
|:---|:---|:---|
| FMEA / Risk Priority Number | Jama Software; SixSigma.us; testRigor 2026 (A2) | `Severity × Occurrence × Detection`; severity-first / Action-Priority override; Detection is the weak axis deserving manual eyes. |
| WSJF (Cost of Delay ÷ duration) | SAFe / Reinertsen; Centercode 2026 (A2) | Cost of Delay = Business-Value + Time-Criticality + Risk-Reduction; portfolio altitude (right for an initiative portfolio). |
| Test Impact Analysis + Predictive Test Selection | Microsoft Learn; Meta Engineering; Fowler 2026 (A1) | Bound the candidate set by what changed; rank by fault-likelihood; keep the full sweep as a periodic safety fallback. |

## 3. The Intent Criticality Score

```
ICS = 3·intent_value + 2·time_criticality + 2·risk_reduction + 1·detection_gap   (max 40)
```

- **intent_value** (1-5): max value of the intent tiers the surface serves (§4).
- **time_criticality** (1-5): does the value decay if we delay (before first sale / incorporation window)?
- **risk_reduction** (1-5): blast radius if the surface breaks.
- **detection_gap** (1-5): FMEA Detection **inverted** — 5 = no always-on gate would catch a regression here (deserves manual eyes); 1 = a strong gate already does.
- **severity_first** override: an existence-critical surface (legal/fiscal or governance-integrity intent with a known live gap) leads the queue regardless of composite ICS (FMEA Action-Priority).

Deliberate deviation from WSJF: the ÷ job-duration term is omitted because regression
"checking" duration is ~uniform across surfaces and the operator wants a
depth-ordering, not an effort-economy. SSOT: [`akos/hlk_intent_ranked_regression.py`](../../../../../akos/hlk_intent_ranked_regression.py).

## 4. The intent corpus (re-derived from evidence)

Seven tiers, weighted 1-5 from the operator's own surfaces (scratchpad "full-protocol"
sessions, RICE-ranked `OPERATOR_INBOX.md`, `USE_CASE_ARCHIVE.csv`, open `OPS_REGISTER`
severities, `INITIATIVE_REGISTRY`). Weights change **only with evidence**.

| Tier | Intent | Value |
|:---|:---|:---:|
| IT-1 | Commercial path to first revenue | 5 |
| IT-2 | Legal / fiscal existence | 5 |
| IT-3 | Governance integrity / SSOT trust (the AKOS thesis) | 5 |
| IT-4 | Operator leverage & interaction quality | 4 |
| IT-5 | Brand & external credibility | 4 |
| IT-6 | Evidence & quality discipline | 3 |
| IT-7 | Runtime & deploy health | 3 |

## 5. The loop (both seats)

1. **Distil / refresh the intent corpus** (thinking seat) — evidence-only weights.
2. **Score surfaces** in the SSOT module; `--self-test` stays green.
3. **Run in ICS order** (`scripts/intent_ranked_regression.py --rank`) top-down.
4. **Attribute every finding**: new (this diff) → rework-now; pre-existing → fix-now
   only if high-ICS + low-effort + reversible (severity-first), else defer-OPS with an
   owner; known-deferred → cite the existing OPS row, do not re-litigate.
5. **Disposition** via the 5-option inline-ratify enum (shared with the inter-wave
   discipline): rework-now / forward-charter-next / defer-OPS / accept-as-canon /
   escalate-to-blocker.
6. **Mint findings**; if the run achieved a lot, **harden the method** so the next
   run is cheaper.

## 6. Cadence (§4-style)

- **On-demand** when the operator asks for a value/intent/risk-weighted regression.
- **Recommended** after a multi-phase area buildout (confirm goals are served, not
  just wiring intact) and at portfolio checkpoints.
- **Always-on circuit-breaker**: `scripts/intent_ranked_regression.py --self-test`
  runs at every `pre_commit` (validates the model; ~1s) — it does **not** run the
  probes (those are on-demand), mirroring the inter-wave self-test split.

## 7. Either-seat contract

- **Execution seat** (Composer-class): `--rank` (ordered checklist) + `--self-test`.
- **Thinking seat** (Opus-class): corpus distillation + attribution + disposition per
  [`intent-ranked-regression-craft`](../../../../../.cursor/skills/intent-ranked-regression-craft/SKILL.md).

## 8. Worked example

[`intent-ranked-regression-2026-06-05.md`](../../../../wip/planning/88-cross-area-ops-wiring-review-discipline/reports/intent-ranked-regression-2026-06-05.md)
— 3552 pass / 9 fail attributed to **0 new regressions**, 1 high-intent pre-existing
drift fixed-now (the `area_governance` pattern-class enum lag), 8 known/deferred
dispositioned.

## Cross-references

- Mechanical companion (when): [`akos-intent-ranked-regression.mdc`](../../../../../.cursor/rules/akos-intent-ranked-regression.mdc)
- Craft (how): [`.cursor/skills/intent-ranked-regression-craft/SKILL.md`](../../../../../.cursor/skills/intent-ranked-regression-craft/SKILL.md)
- SSOT + runbook: [`akos/hlk_intent_ranked_regression.py`](../../../../../akos/hlk_intent_ranked_regression.py) · [`scripts/intent_ranked_regression.py`](../../../../../scripts/intent_ranked_regression.py)
- Safety net (sister): [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md)
- SOP: [`SOP-PEOPLE_INTENT_RANKED_REGRESSION_001.md`](SOP-PEOPLE_INTENT_RANKED_REGRESSION_001.md)
- Process: `hol_peopl_dtp_intent_ranked_regression_001` · Pattern: `pattern_intent_ranked_regression`
