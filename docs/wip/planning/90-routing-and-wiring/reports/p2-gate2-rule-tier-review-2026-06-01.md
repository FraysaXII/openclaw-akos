---
report_kind: gate2_pause
initiative_id: INIT-OPENCLAW_AKOS-90
authored: 2026-06-01
linked_decisions:
  - D-IH-90-R
  - D-IH-90-A
status: PENDING-OPERATOR-WALK
---

# I90 P2 — GATE #2 rule tier review

## Mechanical evidence

| Check | Command | Result |
|:---|:---|:---|
| Rule tier scan | `py scripts/validate_cursor_rule_tiers.py` | **PASS** — 34 rules, **3** always-on |
| Tier self-test | `py scripts/validate_cursor_rule_tiers.py --self-test` | **PASS** |
| HLK umbrella | `py scripts/validate_hlk.py` | *(run at commit)* |

**Always-on core:**

- `akos-operator-communication.mdc`
- `akos-baseline-governance.mdc` (supersedes `akos-governance-remediation.mdc`)
- `akos-rule-router.mdc`

**New surfaces:** root `AGENTS.md` (repo-wide index), `config/cursor-rule-tiers.json` (tier policy SSOT), `.cursor/hooks.json` + four hook scripts, `docs/guides/cursor-two-seat-routing.md`, `akos/hlk_cursor_rule_tiers.py`, `scripts/validate_cursor_rule_tiers.py`.

**Repo-wide posture (2026-06-01 follow-up):** tier cap + core slugs are **config-driven**, not hardcoded to I90/I91/I92; active initiatives are discovered via `docs/wip/planning/README.md`, not a fixed table in `AGENTS.md`.

## Operator approval checklist (≤7)

| # | Item | PASS / N/A / DEFER |
|:--|:---|:---|
| 1 | Three always-on rules + router table match how you want Composer sessions to load doctrine | |
| 2 | `akos-baseline-governance` rename acceptable (same body as old governance-remediation) | |
| 3 | UAT / inter-wave / research-area glob scopes are sufficient for your wave-close workflow | |
| 4 | Hooks: canonical CSV commit `ask` + secret scan on prompt — acceptable friction | |
| 5 | P3 backlog drain may proceed after this gate | |
| 6 | I91 / I92 remain stub until P3 handoff (no premature graph/ERP execution) | |
| 7 | Brand-domain tranche (`D-IH-86-FK`) remains cite-only | |

## Verdict

**PENDING-OPERATOR-WALK** — reply with checklist rows or `continue P3` to clear reversible items per time-box recovery.
