---
title: I75 Research area governance — risk register
language: en
intellectual_kind: initiative_risk_register
sharing_label: internal_only
audience: J-OP;J-AIC
parent_initiative: INIT-OPENCLAW_AKOS-75
authored: 2026-05-29
last_review: 2026-05-29
status: active
---

# I75 — risk register

> Formalizes the master-roadmap §"Risks (top 5)" preview + adds the Wave R+5 logic-change risk.
> Authored at I86 Wave R+5 close to thicken the I75 governance kit. L = likelihood, I = impact.

| ID | Risk | L | I | Mitigation | Status |
|:---|:---|:---:|:---:|:---|:---|
| **R-IH-75-1** | Research Director hire delayed; KM Officer + Founder interim continues indefinitely | High | Medium | Per `D-IH-84-H` interim posture is acceptable; `D-IH-75-B` P0 ratify decides hire-or-defer cleanly | OPEN (monitored) |
| **R-IH-75-2** | SOP buildout dilutes Research Lead bandwidth (Tier-1 WIP curation already heavy) | Medium | High | Cadence cap: 2 SOPs/week max; defer remaining SOPs to next operator cycle if bandwidth shrinks | OPEN (monitored) |
| **R-IH-75-3** | `process_list.csv` tranches require operator approval at every phase | High | Medium | Batched operator-approval gates per phase entry (P1/P2/P3/P4); pause records per `akos-agent-checkpoint-discipline.mdc` | OPEN (by-design) |
| **R-IH-75-4** | Per-engagement intelligence cadence collides with Marketing/Research engagement handoffs | Medium | Medium | P5 cadence SOP explicit about the handoff seam with Marketing/Research per F-51 | OPEN (deferred to P5) |
| **R-IH-75-5** | I71/I72/I73 not yet closed at I75 P1+ entry | Medium | Medium | Per `D-IH-86-CC` OVERRIDE accepted; I72 now closed; I71/I73 closure tracked separately | PARTIALLY-MITIGATED (I72 closed) |
| **R-IH-75-6** *(NEW — Wave R+5)* | The CORPINT-lifecycle logic change (`D-IH-75-G`) destabilizes the area or loses technique knowledge | Low | High | **NOT-TRIGGERED at Wave R+5 close**: all gates PASS (validate_hlk OVERALL PASS; vault links PASS); husk deletion lossless (knowledge preserved in CAPABILITY_REGISTRY + SOPs + source taxonomy per lifecycle doctrine §7); regression sweep confirms the wave's own deliverables clean | NOT-TRIGGERED |
| **R-IH-75-7** *(NEW — Wave R+5)* | The legacy SSOT migration (SOPs + IntelligenceOps register) breaks links / cursor-rule globs when executed | Medium | Medium | Migration deliberately NOT executed this wave; gated to `OPS-86-26` with the full ripple spec pre-written in the migration proposal; operator approves mapping first | DEFERRED (gated) |

## Cross-references

- Master-roadmap: [`master-roadmap.md`](master-roadmap.md) §"Risks (top 5)".
- Decision log: [`decision-log.md`](decision-log.md).
- Wave R+5 closure UAT (R-IH-75-6 NOT-TRIGGERED evidence): [`uat-wave-r-plus-5-close-2026-05-29.md`](../86-initiative-cluster-execution-coordinator/reports/uat-wave-r-plus-5-close-2026-05-29.md) §7.
- Rollout backlog (R-IH-75-7 gated item): [`research-rollout-backlog-2026-05-29.md`](../86-initiative-cluster-execution-coordinator/research-rollout-backlog-2026-05-29.md) (A2 / `OPS-86-26`).
