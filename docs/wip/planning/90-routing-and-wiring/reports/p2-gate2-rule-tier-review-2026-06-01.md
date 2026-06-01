---
report_kind: gate2_pause
initiative_id: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
last_review: 2026-06-01
linked_decisions:
  - D-IH-90-R
  - D-IH-90-A
  - D-IH-90-W
closure_decision_source: operator_explicit
verdict: PASS
verdict_history:
  - verdict: PENDING-OPERATOR-WALK
    date: 2026-06-01
    reason: Awaiting operator walk on tier model
  - verdict: PASS
    date: 2026-06-01
    reason: Operator ratified all checklist rows; proceed per recommended sequence
---

# I90 P2 — GATE #2 rule tier review

## Closure summary

Operator ratified GATE #2 on 2026-06-01 (blanket approval per recommended sequence). **Three always-on** rules + router + config-driven tier policy (`config/cursor-rule-tiers.json`) are the durable routing model for this repo.

## Mechanical evidence

| Check | Command | Result |
|:---|:---|:---|
| Rule tier scan | `py scripts/validate_cursor_rule_tiers.py` | **PASS** — 34 rules, **3** always-on |
| Tier self-test | `py scripts/validate_cursor_rule_tiers.py --self-test` | **PASS** |
| Rule×skill pairing | `py scripts/validate_rule_skill_pairing.py` | **PASS** — 21/21 |
| HLK umbrella | `py scripts/validate_hlk.py` | **PASS** (2026-06-01) |

**Always-on core:**

- `akos-operator-communication.mdc`
- `akos-baseline-governance.mdc` (supersedes `akos-governance-remediation.mdc`)
- `akos-rule-router.mdc`

**New surfaces:** root `AGENTS.md` (repo-wide index), `config/cursor-rule-tiers.json` (tier policy SSOT), `.cursor/hooks.json` + four hook scripts, `docs/guides/cursor-two-seat-routing.md`, `akos/hlk_cursor_rule_tiers.py`, `scripts/validate_cursor_rule_tiers.py`.

**Repo-wide posture:** tier cap + core slugs are **config-driven**, not hardcoded to I90/I91/I92; active initiatives are discovered via `docs/wip/planning/README.md`.

## Operator approval checklist (≤7)

| # | Item | PASS / N/A / DEFER |
|:--|:---|:---|
| 1 | Three always-on rules + router table match how you want Composer sessions to load doctrine | **PASS** |
| 2 | `akos-baseline-governance` rename acceptable (same body as old governance-remediation) | **PASS** |
| 3 | UAT / inter-wave / research-area glob scopes are sufficient for your wave-close workflow | **PASS** |
| 4 | Hooks: canonical CSV commit `ask` + secret scan on prompt — acceptable friction | **PASS** |
| 5 | P3 backlog drain may proceed after this gate | **PASS** |
| 6 | I91 / I92 remain stub until P3 handoff (no premature graph/ERP execution) | **PASS** (I91 P0 inventory only; no graph execution) |
| 7 | Brand-domain tranche (`D-IH-86-FK`) remains cite-only | **PASS** |

## Verdict

**PASS** — operator-explicit ratification 2026-06-01 (`D-IH-90-W`). P3 routing policy sign-off cleared; sibling mirror realign via `bless_external_repo.py` executed post-gate.
