---
title: I83 AI Archivist + KiRBe ingestor — risk register
language: en
intellectual_kind: initiative_risk_register
sharing_label: internal_only
audience: J-OP;J-AIC
parent_initiative: INIT-OPENCLAW_AKOS-83
authored: 2026-05-29
last_review: 2026-05-29
status: active
---

# I83 — risk register

> Formalizes the master-roadmap §"Risks (top 6)". Authored at I86 Wave R+5 close to thicken the I83
> governance kit. L = likelihood, I = impact. I83 is pre-substantive-execution, so most risks are
> OPEN-monitored pending P0.

| ID | Risk | L | I | Mitigation | Status |
|:---|:---|:---:|:---:|:---|:---|
| **R-IH-83-1** | I82 not far enough along when I83 executes — KiRBe has nothing to ingest | High | High | Hard prerequisite: I82 P4 (use-case archive minted) before I83 P0 enters substantive work | OPEN (gated on I82 P4) |
| **R-IH-83-2** | Composio adoption cost vs native build | Low | Low | **RESOLVED** by `D-IH-83-D` (NATIVE BUILD; refactor the existing KiRBe POC + versioning) | MITIGATED |
| **R-IH-83-3** | RLS posture on `kirbe.*` schema unclear | Medium | High | Defaults: deny anon + authenticated; service_role only; classification-aware row filters per `KNOWLEDGE_PAIRING_REGISTRY.access_level` | OPEN (decide at P2 DDL gate) |
| **R-IH-83-4** | Audience translation hallucinates beyond canonical sources | Medium | High | Hard rule: KiRBe surfaces only registered rows; no LLM inference outside the registry-bounded answer space | OPEN (by-design guard at P3) |
| **R-IH-83-5** | hlk-erp Knowledge panel not yet built — P4 has no UI consumer | Medium | Medium | Forward-charter; scope down to API-only MVP + defer UI; ties to I89 (ERP panels) | OPEN (forward-charter) |
| **R-IH-83-6** | Full-sweep scope creep blows past the 13–17d ceiling | Medium | High | P0 sweep produces a per-area inventory matrix (not exhaustive remediation); P0 ≤ 5d hard cap; any sub-sweep that overruns forks to a dedicated initiative (I83-A / I83-B / …) per Option-5 default posture | OPEN (by-design cap) |

## Cross-references

- Master-roadmap: [`master-roadmap.md`](master-roadmap.md) §"Risks (top 6)". Decision log: [`decision-log.md`](decision-log.md).
- Rollout backlog (C2 feed-delivery → I83; C5 KiRBe ingestor → I83): [`research-rollout-backlog-2026-05-29.md`](../86-initiative-cluster-execution-coordinator/research-rollout-backlog-2026-05-29.md).
