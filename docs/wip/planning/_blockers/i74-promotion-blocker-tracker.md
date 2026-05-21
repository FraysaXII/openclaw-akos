---
intellectual_kind: blocker_tracker
sharing_label: internal_only
parent_candidate: I74
candidate_file: docs/wip/planning/_candidates/i74-brand-tooling-productization.md
authored: 2026-05-18
last_review: 2026-05-21
next_review_trigger: superseded
linked_decisions:
  - D-IH-76-A
  - D-IH-86-O
  - D-IH-84-D
  - D-IH-86-CC
  - D-IH-74-A
status: superseded
superseded_by: D-IH-86-CC + D-IH-74-A (I86 Wave O OVERRIDE 2026-05-21)
role_owner: PMO
co_owner_role: System Owner
language: en
---

# I74 — Promotion Blocker Tracker (SUPERSEDED)

> **SUPERSEDED 2026-05-21**: I74 promoted to `active` status during I86 Wave O OVERRIDE per `D-IH-86-CC`. Operator accepted speculative-promotion debt (TRIGGER-2 zero-count override-accepted; P4 external pilot still gated on actual TRIGGER-2 firing). Active master-roadmap at [`74-brand-tooling-productization/master-roadmap.md`](../74-brand-tooling-productization/master-roadmap.md). Tracker preserved for audit lineage of the original blocker-tracker → OVERRIDE-promotion governance pattern.
>
> Governance-shape artifact minted at I76 P0 charter (2026-05-18) per A0 Option 5 default posture (D-IH-86-O). Documents why I74 cannot be promoted in this Wave A push despite being named in the Bundle D scope, and tracks the conditions that resolve the blocker. This file is **NOT a charter**; it is a governance artifact preserving operator intent visibility (Lane 5 promotion was considered) without speculative-promotion debt (the candidate's own activation criteria are not yet met).

## 1. Why I74 is not promoted today

The I74 candidate file ([`docs/wip/planning/_candidates/i74-brand-tooling-productization.md`](../_candidates/i74-brand-tooling-productization.md)) §6 Spin-out trigger conditions explicitly requires (all-of):

| Condition | Status today (2026-05-18) | Source |
|:---|:---|:---|
| **TRIGGER-2 fires**: ≥2 external orgs request AKOS doctrine consumption without source-fork | **NOT MET (count: 0)** | i74 candidate §6 + §1 Operating story explicitly framed as "reactive trigger; this candidate sits dormant by design" |
| I70 closed | **MET** 2026-05-13 | INITIATIVE_REGISTRY row I70 |
| I71 closed | **PENDING** (active) | INITIATIVE_REGISTRY row I71; ~80% per I86 handoff §2 |
| I72 closed | **PENDING** (candidate per I86 handoff §2) | I72 candidate file |
| I73 closed | **PENDING** (candidate) | I73 candidate file |
| Founder + Brand Manager approval (license posture + brand boundaries) | **PENDING** | Operator decision deferred until trigger fires |
| HLK Tech Lab capacity available (per WORKSPACE_BLUEPRINT_HOLISTIKA.md §16.3 transition trigger) | **PENDING** | Capacity assessment deferred |

The I74 candidate's own risk register lists **speculative productization without TRIGGER-2 firing** as the **#1 critical risk** with mitigation = "this candidate sits dormant until ≥2 external requests land. Document the trigger threshold prominently in §6 above."

Promoting I74 today would directly violate this candidate's own gate and trigger its own #1 critical risk.

## 2. Already-cleared sub-decisions

Even though promotion is blocked, two architectural decisions for I74 have been pre-ratified at I84 P4 (2026-05-17):

- **D-IH-74-D = D3 (Hybrid library + agent platform)** per `D-IH-84-D` — Strand C (`@holistika/madeira-agent`) shape gate closed; ships as **library for technically-mature customers + hosted agent for less-technical customers**. C-74-3 (MADEIRA gate criteria) closes via I84 P4 ratification.
- **License separation enforceability (C-74-4)** is informed by I84 P1 Tier-1 WIP regulatory-tos-forecast.md §6 + §7 (Cursor SDK ToS analysis + IP-indemnity carve-out findings; ADVOPS engagement recommended before binding library-license posture).

So when TRIGGER-2 eventually fires, I74 P0 can charter quickly (D-IH-74-D inheritance + I76 elevation as prerequisite + ADVOPS engagement triggers per regulatory-tos-forecast.md).

## 3. Resolution conditions (when does this tracker close)

This tracker closes when I74 is promoted to active status in INITIATIVE_REGISTRY. Promotion is governed by:

1. **TRIGGER-2 fires** (≥2 external orgs request AKOS doctrine consumption); AND
2. I71 closes; AND
3. I72 closes (or completes P0..P4 such that engagement-template promotion machine is operational per Strand B; C-74 candidate file footnotes I72 P2 as soft dependency); AND
4. I73 closes (or completes P3..P4 such that People Operations + Learning curriculum is operational); AND
5. **I76 reaches at least P3 closure** (operator UX + persistence + personality SOPs minted; Strand C `@holistika/madeira-agent` library has the polished MADEIRA pattern to package); AND
6. Founder + Brand Manager approval recorded; AND
7. HLK Tech Lab capacity confirmed.

## 4. Next-review trigger

When ANY of (a) first external request lands (operator records in this file), (b) I71 closure ratified, (c) I72 closure ratified, (d) I73 closure ratified, (e) I76 P3 closure ratified — the operator should review this tracker. If **all** conditions §3 1-7 met, promote I74 via a fresh A1-equivalent ratify gate; close this tracker with archive disposition.

## 5. Reverted-promotion lineage

`D-IH-86-F` (2026-05-17) initially attempted to mint INIT row for I74 + D-IH-74-A inception decision; operator-corrected at `D-IH-86-G` (2026-05-17) with explicit revert. This tracker preserves the lesson: the prior aborted promotion was the correct discipline; today's tracker mint is the formalisation of that discipline as a durable governance shape per D-IH-86-O default posture.

## 6. Cross-references

- [I74 candidate file](../_candidates/i74-brand-tooling-productization.md) — primary source for activation gates + risk register + spin-out trigger conditions.
- [I84 master-roadmap §P4](../84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) — D-IH-84-D pre-ratification (D3 hybrid library + agent platform).
- [I84 P1 Tier-1 WIP regulatory-tos-forecast.md](../../intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md) — C-74-4 license-separation evidence base.
- [I76 master-roadmap](../76-madeira-elevation/master-roadmap.md) — prerequisite for I74 Strand C (per C-76-6).
- [`akos-inline-ratification.mdc`](../../../.cursor/rules/akos-inline-ratification.mdc) — pattern this tracker instantiates.
- D-IH-76-A — I76 charter inception decision authorising this tracker.
- D-IH-86-O — default posture decision authorising the blocker-tracker pattern as durable governance shape.
