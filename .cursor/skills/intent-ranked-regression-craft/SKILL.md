---
name: intent-ranked-regression-craft
description: >-
  Use when running a regression that should be ordered by operator-intent value
  rather than by mechanical dimension number — i.e. "check what matters most to my
  goals first". Codifies the HOW of the Intent-Ranked Regression: distil the intent
  corpus, score surfaces by Intent Criticality (ICS = WSJF/FMEA fusion), run the
  sweep in ICS order, and disposition findings by attribution (new vs pre-existing
  vs known-deferred). Triggers on intent-ranked regression, value-weighted
  regression, ICS, intent criticality, FMEA RPN regression, WSJF regression,
  risk-based test prioritization, "regression but not mechanical". Pairs with
  .cursor/rules/akos-intent-ranked-regression.mdc (the WHEN); runnable by either
  seat via scripts/intent_ranked_regression.py.
version: 1.0.0
ratifying_decisions: D-IH-88-F (candidate — gate pending)
authored: 2026-06-05
---

# Intent-Ranked Regression Craft

> Minted 2026-06-05 from the operator's framing: *"not mechanical — take all my
> intents, use cases, logic, scenarios, interactions (past/present/future), make a
> ranking system, research inside and outside, review it, then regress."* This is
> the **value layer** above the mechanical inter-wave regression (which checks *is
> everything wired?*); this layer asks *is what I care about most still served?*

## Why this exists (vs the mechanical sweep)

`akos-inter-wave-regression.mdc` runs 13 structural dimensions at ~equal weight.
That answers integrity, not **priority**. When attention is scarce (operator review
minutes; agent context budget), you want the highest-stakes surfaces checked first
and deepest. External practice converges here:

- **FMEA / RPN** (Jama, SixSigma, testRigor 2026): rank failure modes by
  Severity × Occurrence × Detection; **severity-first override** — a catastrophic
  surface is actioned regardless of composite score.
- **WSJF** (SAFe / Reinertsen): Cost of Delay = Business-Value + Time-Criticality +
  Risk-Reduction; the right altitude for an **initiative-portfolio** regression.
- **TIA + Predictive Test Selection** (Microsoft, Meta, Fowler): bound the candidate
  set by what changed, rank by fault-likelihood, keep the **full sweep as a periodic
  safety net** (never delete it).

## The model (SSOT in code)

`akos/hlk_intent_ranked_regression.py` — 7 intent tiers + N surfaces + ICS.
`scripts/intent_ranked_regression.py --rank` prints the ranked sweep order.

```
ICS = 3*intent_value + 2*time_criticality + 2*risk_reduction + 1*detection_gap
```

- `intent_value` (1-5) = max value of the intent tiers the surface serves.
- `time_criticality` (1-5) = does delay cost? (before first sale / incorporation).
- `risk_reduction` (1-5) = blast radius if it breaks.
- `detection_gap` (1-5) = FMEA Detection **inverted** — 5 means no always-on gate
  would catch a regression here (so it deserves manual eyes); 1 means a strong gate
  already does.
- `severity_first` = FMEA Action-Priority override: existence-critical surfaces
  (legal/fiscal IT-2, governance-integrity IT-3) with a known live gap lead the
  queue regardless of ICS.

## The loop (both seats)

1. **Distil the intent corpus** (thinking seat): sweep operator-scratchpad,
   RICE-ranked `OPERATOR_INBOX.md`, `USE_CASE_ARCHIVE.csv`, open `OPS_REGISTER`
   severities, `INITIATIVE_REGISTRY`. Update tier weights only with evidence — never
   invent priority. Re-derive when the portfolio shifts materially.
2. **Score / re-score surfaces** (either seat): edit the surfaces in the SSOT module;
   `--self-test` must stay green.
3. **Run in ICS order** (execution seat): `--rank` gives the ordered probe list. Run
   top-down; stop-early is allowed only when remaining surfaces are all low-ICS AND
   green so far.
4. **Attribute every finding** (thinking seat) — the load-bearing craft move:
   - **new** = this session's diff caused it → rework-now.
   - **pre-existing** = drift that predates this session → fix-now only if high-ICS +
     low-effort + reversible (FMEA severity-first); else defer-OPS with owner.
   - **known-deferred** = already has an OPS row + ETA → cite it, do not re-litigate.
5. **Disposition** via the inter-wave 5-option enum (rework-now / forward-charter /
   defer-OPS / accept-as-canon / escalate-to-blocker). Never ad-hoc.
6. **Mint findings + (if high value) harden the method** so the next regression is
   cheaper — that is this discipline eating its own tail.

## Anti-patterns

- **AP1 — Flat failure lists.** A release-gate "9 failed" is not a regression result;
  rank + attribute the 9, or you have only noise.
- **AP2 — Blaming your own diff for inherited drift** (or the reverse). Attribution
  is mandatory; it is the difference between "I regressed X" and "X was already red".
- **AP3 — Deleting the safety net.** The ranked sweep *supplements* the full
  mechanical sweep / release-gate; it never replaces it (TIA safety-fallback).
- **AP4 — Inventing intent weights.** Every tier value cites scratchpad / inbox /
  OPS / registry evidence. No evidence, no weight change.
- **AP5 — RPN-only blindness.** Honour severity-first: an existence-critical surface
  leads even if its composite ICS is not the maximum.

## Worked example

`docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/intent-ranked-regression-2026-06-05.md`
— the 2026-06-05 run: 3552 pass / 9 fail, attributed to **0 new regressions**,
1 high-intent pre-existing drift fixed-now (the `area_governance` pattern-class
enum lag from I93), 8 known/deferred dispositioned.

## Cross-references

- SSOT model: `akos/hlk_intent_ranked_regression.py`
- Runbook: `scripts/intent_ranked_regression.py`
- Draft rule: `.cursor/rules/akos-intent-ranked-regression.mdc`
- Sister discipline (the safety net): `.cursor/rules/akos-inter-wave-regression.mdc`
  + `.cursor/skills/inter-wave-regression-craft/SKILL.md`
- Disposition enum: `.cursor/rules/akos-inline-ratification.mdc`
