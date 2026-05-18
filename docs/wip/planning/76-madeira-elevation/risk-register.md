---
language: en
status: active
canonical: false
classification: way_of_working
intellectual_kind: risk_register
phase: P0
initiative: INIT-OPENCLAW_AKOS-76
authored: 2026-05-18
last_review: 2026-05-18
role_owner: System Owner
companion_to:
  - master-roadmap.md
  - decision-log.md
ssot: false
---

# I76 — Risk Register

> Workspace mirror of I76 risks. Lifecycle status updated as phases close. Per `akos-planning-traceability.mdc` Plan-quality bar.

| ID | Risk | L | I | Status | Mitigation | Owner |
|:---|:---|:---:|:---:|:---|:---|:---|
| **R-IH-76-1** | Premature AICs commitment locks pattern before live evidence supports it | Medium | High | open | F5 hybrid framing means per-task operator picks; the dispatcher pattern carries the framing flexibility. P5 UAT collects pivot frequency to inform whether F5 holds or any framing should be promoted as primary at I76 closure or follow-on initiative. | System Owner |
| **R-IH-76-2** | Brand-voice / personality conflict with `D-IH-70-I` strict mode | Medium | High | open | P3 SOP + paired runbook with BBR drift gate enforcement; Strand F brand-jargon hygiene gates at every MADEIRA-authored artifact per `akos-brand-baseline-reality.mdc`. | Brand & Narrative Manager (consult) |
| **R-IH-76-3** | Tool RBAC creep (MADEIRA gets too many tools too fast) | Medium | Medium | open | P2 explicit deny-list + per-mode RBAC frozen by enum; Langfuse trace audit per session per I71 Strand B; MADEIRA_TOOL_RBAC.csv as canonical SSOT. | System Owner |
| **R-IH-76-4** | Persistence violates `D-IH-70-I` brand-jargon hygiene OR `D-IH-71-E` review-stamp dimension | Medium | Medium | open | Default = methodology-scoped read-only (P3 SOP); brand-jargon validator + review-stamp validator both gate persistent state. | System Owner |
| **R-IH-76-5** | I11 / I13 / I17 consolidation ratify creates downtime in active engagements | Medium | High | open | Scope-overlap-tracker §3 ratifies one sibling per I76 phase (P4), not all at once; default = remain-parallel for any sibling without consolidation evidence; tracker forward-charters to I76b if consolidation needs second cycle. | Founder + System Owner |
| **R-IH-76-6** | P5 UAT cohort can't be assembled (no 5 active engagements when P4 closes) | Medium | Medium | open | P5 calendar-spread (~2 weeks); operator can use 3 engagements + 2 simulated runs as fallback; UAT report acknowledges sample size as caveat in evidence section. | PMO + Founder |
| **R-IH-76-7** | I76 closure fires before TRIGGER-2 of I74 (productization) — Strand C handoff has nothing to receive | Low | Low | open | D-IH-76-I gate at P6 — closure includes "handoff trigger pending TRIGGER-2 firing"; I74 picks up when its own gate clears (per i74-promotion-blocker-tracker.md). | Founder |
| **R-IH-76-8** | Methodology mode is overengineered (5th mode adds cognitive load without unique tool affordances) | Medium | Low | open | C-76-2 ratifies at P1 inline-ratify; default = real mode IF unique tool affordances; preset otherwise. | System Owner |
| **R-IH-76-9** | Inline-ratify gate density during P4 AICs implementation overwhelms operator (3 consolidation ratifies + dispatcher pattern + per-task config) | Low | Medium | open | Per `akos-inline-ratification.mdc` Principle 5 — batch tightly-coupled decisions; per-task config can be operator-default for first 2 weeks then reviewed; consolidation gates one per active sibling not all-at-once. | System Owner |

## Closed risks

(none yet — initiative just promoted)

## Risk-deltas at close-out

When I76 closure fires, this section will record which risks materialised, which were mitigated cleanly, and which are forward-charters to I76b / I74 Strand C.
