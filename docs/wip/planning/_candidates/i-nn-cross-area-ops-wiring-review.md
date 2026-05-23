---
candidate_id: I-NN-CROSS-AREA-OPS-WIRING-REVIEW
title: Cross-area Ops-wiring review discipline — FINOPS/PeopleOps/RevOps/LegalOps as backbone wiring spines
status: candidate
authored: 2026-05-22
last_review: 2026-05-22
parent_initiatives: [81]
related_initiatives: [21, 72, 79, 86]
priority: 4
language: en
audience: J-OP;J-AIC
access_level: 5
parent_lane: I81 Wave R lane D T1-gate (FINOPS synthesis ratification)
charter_decisions:
  - D-IH-81-O
forward_charter_authority: D-IH-81-O (operator novel framing at FINOPS synthesis Decision C gate 2026-05-22)
linked_canonicals:
  - docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/i81/p2-tranche-t1-finops-synthesis-2026-05-22.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv
  - .cursor/rules/akos-people-discipline-of-disciplines.mdc
  - .cursor/rules/akos-executable-process-catalog.mdc
  - .cursor/rules/akos-quality-fabric.mdc
linked_ops_action_ids:
  - OPS-81-2
  - OPS-81-3
  - OPS-81-4
  - OPS-81-5
  - OPS-81-6
  - OPS-81-17
---

# I-NN-CROSS-AREA-OPS-WIRING-REVIEW — backbone Ops wiring review discipline

> **Spawned by D-IH-81-O** (operator novel framing at the FINOPS end-to-end synthesis ratification gate, 2026-05-22). Operator verbatim: *"add regressions or continuous revisions or enhancements or backfill for all of this. Because FINOPS is a backbone, main representative of finance + legal + PeopleOps + other area's Ops, needs to be wired properly and cleverly to ensure we can grow our all ops as we go. Think you could review each area's OPS to ensure proper wiring maintenance etc. Mint this in the operator scratchbook too to ensure audit trail."*

## 1. Doctrine in one sentence

Backbone-class Ops areas (FINOPS / PeopleOps / RevOps / LegalOps) are not just per-area operational disciplines — they are **wiring spines** that compose how every other area touches money / talent / customers / contracts. They require **explicit cross-area wiring review** as ongoing discipline beyond per-area maintenance, so that backbone integrity is checked the same way Inter-Wave Regression checks cluster-coordinator integrity.

## 2. Activation gates

- **A1.** Operator sets activation criteria explicitly (this candidate names *that* the discipline should exist; *when* it activates is operator-discretion at next ratify cycle).
- **A2.** At least one backbone area (FINOPS most likely first per OPS-81-2 + OPS-81-3 sequencing) has reached "wired-enough to be reviewable" maturity — i.e., counterparty register populated + at least one paired SOP+runbook exercised end-to-end + at least one cross-area event-trigger fired (e.g., engagement signed → counterparty registered → Stripe customer linked per SOP-FINOPS_BRIDGE_001).
- **A3.** Either CFOaaS firm contracted (per OPS-81-17 + D-IH-81-N D1) OR operator declares interim ownership explicit, so the cross-area review has a *role* to invoke.

When all three gates clear, this candidate promotes to a numbered initiative folder under `docs/wip/planning/<NN>-cross-area-ops-wiring-review/`.

## 3. Scope sketch (subject to operator refinement at promotion)

### 3.1 Backbone areas in scope (initial)

| Area | Backbone-ness | Wired-to | Wiring review focus |
|:---|:---|:---|:---|
| **FINOPS** | Money spine | Every counterparty + every revenue/expense/capital/tax fact + every adviser engagement carrying money | Counterparty register populated; recognition policy authored; tax calendar deterministic; founder ledger reconciled |
| **PeopleOps** | Talent spine (per People-as-DoD per D-IH-79-H) | Every role + every process + every paired SOP+runbook + every cross-area breakthrough | Pattern registry populated; design patterns adopted across areas; breakthroughs announced |
| **RevOps** | Customer-flow spine (per D-IH-72-N) | Every engagement template + every CRM adapter + every billing adapter + every contract adapter | Engagement-template registry populated; adapters status enum honest; integration spine event-triggered |
| **LegalOps** (within ADVOPS per D-IH-21-* lineage) | Contract spine | Every filed instrument + every adviser open question + every counterparty contract pointer + every program filing | Filed instruments registered; open questions routed; cap-table instruments captured |

### 3.2 Cross-area wiring checks (illustrative — to be refined at promotion)

- **FINOPS ↔ RevOps**: every `process_list.csv` row tagged `area=Finance` that mentions an engagement event has a paired `area=Operations` RevOps row with matching event trigger.
- **FINOPS ↔ LegalOps**: every `FOUNDER_FILED_INSTRUMENTS.csv` row carrying a money amount (when the money-amount field exists per OPS-81-15) has a paired counterparty_id back-reference.
- **PeopleOps ↔ FINOPS**: every role activation in `baseline_organisation.csv` (post-incorporation; first hire) has paired employment-counterparty row in FINOPS counterparty register.
- **RevOps ↔ LegalOps**: every active engagement has paired contract instrument in `FOUNDER_FILED_INSTRUMENTS.csv` (or the SME-counterparty equivalent when minted).

The review is structurally analogous to [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md) — instead of dimensions over a cluster wave, dimensions over a backbone wiring surface.

## 4. Quartet expectations at promotion

Per [`akos-quality-fabric.mdc`](../../../../.cursor/rules/akos-quality-fabric.mdc) RULE 7 + the Wave M/N specialty-mint contract, promotion ships:

1. Canonical doctrine: `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/CROSS_AREA_OPS_WIRING_REVIEW_DISCIPLINE.md`.
2. Pydantic chassis: `akos/hlk_cross_area_ops_wiring.py` (per-area wiring row Pydantic model).
3. Validator: `scripts/validate_cross_area_ops_wiring.py` (release-gate-wired self-test; INFO ramp).
4. Runbook: `scripts/cross_area_ops_wiring_sweep.py` (paired with SOP per [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1).
5. Cursor rule: `.cursor/rules/akos-cross-area-ops-wiring.mdc` (the *when*).
6. Skill: `.cursor/skills/cross-area-ops-wiring-craft/SKILL.md` (the *how*).
7. SOP+runbook pair: `SOP-PEOPLE_CROSS_AREA_OPS_WIRING_001.md` with AC-HUMAN + AC-AUTOMATION acceptance.
8. PEOPLE_DESIGN_PATTERN_REGISTRY row (pattern_id `pattern_cross_area_ops_wiring_review`, class `cross_area_ops_wiring_cadence`).
9. PRECEDENCE canonical + mirror rows when the discipline ships a registry.
10. HOLISTIKA_QUALITY_FABRIC §6 row (12th specialty if minted after the 11th INDEX_INTEGRITY).
11. CHANGELOG entry.
12. `process_list.csv` row(s) per area.
13. `validate_hlk.py` umbrella registration when umbrella-scoped.
14. `config/verification-profiles.json` `pre_commit` step (INFO ramp).
15. `scripts/release-gate.py` advisory wiring.

## 5. Anti-patterns to avoid at promotion

- **Conflating with INTER_WAVE_REGRESSION.** That discipline checks wave-close integrity inside a cluster initiative. This discipline checks backbone wiring across areas, independent of wave cadence.
- **Forcing all areas into the discipline.** Non-backbone areas (e.g., Marketing/Reach) may not need cross-area wiring review at this granularity; the discipline names *which* areas are backbones.
- **Authoring the discipline before any backbone area is mature enough to be reviewed.** Pre-mature discipline becomes governance theatre. Hold candidate at this status until A2 gate clears.
- **Treating it as a sub-discipline of People DoD.** It generalises beyond what People-as-DoD covers (which is per-area pattern stewardship); backbone wiring review is a horizontal slice across area boundaries.

## 6. Cross-references

- Parent decision: D-IH-81-O (architecture, active 2026-05-22).
- Synthesis context: [`p2-tranche-t1-finops-synthesis-2026-05-22.md`](../81-vault-integrity-layout-milestones-retrofit/reports/i81/p2-tranche-t1-finops-synthesis-2026-05-22.md) §10.1.
- Sister disciplines:
  - [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md) — structural analogue (review-cadence discipline shape).
  - [`INDEX_INTEGRITY_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md) — sister 11th specialty.
- Parent rule: [`akos-people-discipline-of-disciplines.mdc`](../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) RULE 1 (People owns patterns; this candidate names a pattern People will own).
- Operator-scratchpad audit-trail entry: `docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md` (2026-05-22 wave-R-lane-D-T1-gate drain).
