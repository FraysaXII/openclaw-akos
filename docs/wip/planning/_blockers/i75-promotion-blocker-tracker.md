---
intellectual_kind: blocker_tracker
sharing_label: internal_only
parent_candidate: I75
candidate_file: docs/wip/planning/_candidates/i75-research-area-governance.md
authored: 2026-05-18
last_review: 2026-05-21
next_review_trigger: superseded
linked_decisions:
  - D-IH-76-A
  - D-IH-86-O
  - D-IH-86-CC
  - D-IH-75-A
  - D-IH-84-G
  - D-IH-84-H
status: superseded
superseded_by: D-IH-86-CC + D-IH-75-A (I86 Wave O OVERRIDE 2026-05-21)
role_owner: PMO
co_owner_role: Research Director (interim Founder)
language: en
---

# I75 — Promotion Blocker Tracker (SUPERSEDED)

> **SUPERSEDED 2026-05-21**: I75 promoted to `active` status during I86 Wave O OVERRIDE per `D-IH-86-CC`. Operator accepted speculative-promotion debt (Research Director hire decision deferred so SOP buildout proceeds in parallel). Active master-roadmap at [`75-research-area-governance/master-roadmap.md`](../75-research-area-governance/master-roadmap.md). Tracker preserved for audit lineage of the original blocker-tracker → OVERRIDE-promotion governance pattern.
>
> Governance-shape artifact minted at I76 P0 charter (2026-05-18) per A0 Option 5 default posture (D-IH-86-O). Documents why I75 cannot be promoted in this Wave A push despite being conditionally named in handoff §2.2 ("if Lane 1 promoted"), and tracks the conditions that resolve the blocker. Not a charter; governance artifact.

## 1. Why I75 is not promoted today

The I75 candidate file ([`docs/wip/planning/_candidates/i75-research-area-governance.md`](../_candidates/i75-research-area-governance.md)) §6 Spin-out trigger conditions explicitly requires:

| Condition | Status today (2026-05-18) | Source |
|:---|:---|:---|
| I70 closing UAT | **MET** 2026-05-13 | INITIATIVE_REGISTRY row I70 |
| I71 P0 charter | **MET** 2026-05-13 | I71 master-roadmap |
| **I72 P0 charter** | **PENDING** (candidate per I86 handoff §2; I72 candidate file lists 8+ phases not yet started) | I72 candidate file |
| **I73 P0 charter** | **PENDING** (candidate) | I73 candidate file |
| I70 P4.5 wave 3 federated-canonicals migration (IntelligenceOps SOPs migrated under Research/Intelligence) | **MET** (commit `f0c8e9f`) | I70 P4.5 |
| **First Research Director hire OR founder formally takes the role** | **PENDING** | No `baseline_organisation.csv` row activation for Research Director; founder has not formally claimed the role |

I75 is the most constraint-blocked of the four Lane 5 candidates: 3 of 6 conditions PENDING, including a hiring decision that may take quarters to resolve.

The handoff itself flagged I75 as **conditional** in §2.2 ("(and I75 if Lane 1 promoted)") — i.e., I75 was never in the unconditional Lane 5 scope. The operator's Bundle D framing ("promote I76 + I74 + I83") did not include I75; I75 was added to the agent's plan in error and surfaced via this tracker rather than promoted speculatively.

## 2. Resolution conditions (when does this tracker close)

This tracker closes when I75 is promoted to active status in INITIATIVE_REGISTRY. Promotion is governed by:

1. **I72 P0 charter** ratified (or I72 promoted to active such that Marketing Area Governance + engagement-template promotion machine is operational); AND
2. **I73 P0 charter** ratified (or I73 promoted to active such that People Operations + Learning curriculum baseline is operational); AND
3. **Research Director role activated** — either first hire ratified (`baseline_organisation.csv` row activation) OR founder formally takes the role (recorded as `D-IH-75-PRE` charter-time decision); AND
4. **Lane 1 promoted** per the handoff §2.2 conditional framing (or operator overrides the conditional with explicit ratify).

## 3. Already-named sub-decisions (to inform when promotion fires)

When promotion fires, I75 candidate file §5 names the likely D-IH-75-* rows:

- **D-IH-75-A** — Methodology pillar SOP architecture (per-pillar SOP shape + cadence).
- **D-IH-75-B** — Intelligence per-source-type SOPs + Intelligence Matrix codification.
- **D-IH-75-C** — Diagnosis templates + Validation rubrics + SOURCE_RELIABILITY_REGISTRY architecture.
- **D-IH-75-D** — KM Officer curriculum (cross-coordinated with `D-IH-73-A`).
- **D-IH-75-E** — Research Director activation.
- **D-IH-75-F** — Per-engagement intelligence cadence SOP.

Cross-coordinations to be honored: with I73 (KM Officer / Holistik Researcher boundary per C-75-4); with I72 (engagement-template promotion machine cross-coordinates with Per-engagement intelligence cadence Strand D).

## 4. Next-review trigger

When ANY of (a) I72 P0 closure ratified, (b) I73 P0 closure ratified, (c) Research Director hire ratified OR founder-takes-role recorded — the operator should review this tracker. If **all** §2 conditions met, promote I75 via a fresh A1-equivalent ratify gate; close this tracker with archive disposition.

## 5. Reverted-promotion lineage

`D-IH-86-F` (2026-05-17) initially attempted to mint INIT row for I75 + D-IH-75-A inception decision; operator-corrected at `D-IH-86-G` (2026-05-17) with explicit revert. This tracker preserves the discipline.

## 6. Cross-references

- [I75 candidate file](../_candidates/i75-research-area-governance.md) — primary source.
- [I72 candidate file](../_candidates/i72-marketing-area-governance.md) (or active master-roadmap if promoted) — prerequisite.
- [I73 candidate file](../_candidates/i73-people-operations-and-learning-curriculum.md) — prerequisite + cross-coordination.
- [`baseline_organisation.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv) — Research Director role activation row pending.
- D-IH-76-A — I76 charter inception authorising this tracker.
- D-IH-86-O — default posture authorising the blocker-tracker pattern.
