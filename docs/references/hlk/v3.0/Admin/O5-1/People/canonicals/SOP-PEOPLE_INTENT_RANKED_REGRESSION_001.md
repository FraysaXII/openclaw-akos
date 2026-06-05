---
title: SOP — People Intent-Ranked Regression
language: en
intellectual_kind: people-canonical-sop
sop_id: SOP-PEOPLE_INTENT_RANKED_REGRESSION_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - PMO
co_authors:
  - System Owner
  - Founder/CEO
last_review: 2026-06-05
last_review_by: PMO
last_review_decision_id: D-IH-88-F
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-88-F
status: active
register: internal
linked_canonicals:
  - INTENT_RANKED_REGRESSION_DISCIPLINE.md
  - INTER_WAVE_REGRESSION_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
linked_runbooks:
  - scripts/intent_ranked_regression.py
linked_processes:
  - hol_peopl_dtp_intent_ranked_regression_001
cadence: on_demand
cadence_trigger: operator asks for value/intent/risk-weighted regression OR post-area-buildout checkpoint
---

# SOP — People Intent-Ranked Regression

## Purpose

Operationalise [`INTENT_RANKED_REGRESSION_DISCIPLINE.md`](INTENT_RANKED_REGRESSION_DISCIPLINE.md):
run a regression ordered by **operator-intent value** (ICS), with every finding
attributed before it is reported. Owner **PMO**; co-owners **System Owner**
(runbook) + **Founder/CEO** (intent-corpus weights).

Paired runbook: [`scripts/intent_ranked_regression.py`](../../../../../scripts/intent_ranked_regression.py).

## Scope

In scope: portfolio-wide or area-buildout regression checkpoints where attention is
scarce. Out of scope: a single-file change (use the mechanical self-test) and a true
wave-close (run the 13-dimension inter-wave sweep — this SOP sits above it).

## AC-HUMAN (role_owner steps, ~20-40 min)

1. **Refresh the intent corpus** — skim `operator-scratchpad.md`, `OPERATOR_INBOX.md`
   (RICE), `USE_CASE_ARCHIVE.csv`, open `OPS_REGISTER` severities. Adjust tier values
   in `akos/hlk_intent_ranked_regression.py` **only** with cited evidence.
2. **Rank** — `py scripts/intent_ranked_regression.py --rank`; read the ordered surfaces.
3. **Run probes top-down** — execute each surface's probe in ICS order; stop-early
   only if all remaining surfaces are low-ICS and green so far.
4. **Attribute every finding** — new / pre-existing / known-deferred (the load-bearing
   step). Fix-now a pre-existing finding only when high-ICS + low-effort + reversible
   (severity-first); else defer-OPS with a named owner.
5. **Disposition** via the 5-option inline-ratify enum; never ad-hoc.
6. **Mint the dated report** under the active initiative's `reports/`; if the run
   achieved a lot, harden the method (skill / runbook / model) in the same cycle.

## AC-AUTOMATION

- `py scripts/intent_ranked_regression.py --self-test` exits 0 at every `pre_commit`
  via `config/verification-profiles.json` `validate_intent_ranked_regression_self_test`
  + `scripts/release-gate.py` `run_intent_ranked_regression_self_test`.
- `py scripts/intent_ranked_regression.py --rank` emits the ICS-ordered table for the
  execution seat; `tests/test_intent_ranked_regression.py` locks determinism +
  severity-first ordering.

## Cross-references

- Discipline: [`INTENT_RANKED_REGRESSION_DISCIPLINE.md`](INTENT_RANKED_REGRESSION_DISCIPLINE.md)
- Cursor rule: [`.cursor/rules/akos-intent-ranked-regression.mdc`](../../../../../.cursor/rules/akos-intent-ranked-regression.mdc)
- Skill: [`.cursor/skills/intent-ranked-regression-craft/SKILL.md`](../../../../../.cursor/skills/intent-ranked-regression-craft/SKILL.md)
