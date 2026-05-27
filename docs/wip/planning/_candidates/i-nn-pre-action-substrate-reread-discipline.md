---
language: en
intellectual_kind: initiative_candidate
sharing_label: internal_only
audience: J-OP
authored: 2026-05-27
last_review: 2026-05-27
status: candidate
parent_canonical: docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
forward_charter_source: operator framing 2026-05-26 post-handshake transcript (funnel-vision mitigation)
ratifying_decisions:
  - D-IH-86-ET
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md
external_references: []
---

# Candidate — I-NN: Pre-action substrate re-read discipline (funnel-vision mitigation)

## Purpose

Mint a candidate Quality Fabric specialty addressing the lived failure
mode where an agent (or operator) about to execute a substantive
action skips the substrate re-read step, narrows attention to the
immediate action surface, and produces an output that turns out to be
mis-calibrated against substrate that was readily available at the
moment of action but un-consulted.

The Wave R+2 COLLABORATOR_SHARE doctrine rewrite is the worked example:
the original Wave R+1 P2c-a doctrine mint encoded `share_pattern` as
3 shapes including `orchestration_broker_thin_margin` based on the
operator's intermediate framing; the 13/05 SUEZ customer-meeting
transcript (which existed on disk at the time of the original mint
but was not re-read at the SUEZ classification moment) would have
surfaced the actual 4-base + 1-overlay shape — saving the entire
Wave R+2 rewrite tranche (7 commits + Stage-1 demotion + decision
supersede chain) that became necessary because the substrate hadn't
been re-read at the load-bearing decision point.

The discipline would name a mechanical bar that fires before any
agent commits to:

- A canonical CSV mint (e.g. SHARE_REGISTRY row authoring).
- A doctrine `status:` flip (charter → active OR active → charter).
- A decision-row mint at status `active` that ratifies a load-bearing
  semantic choice (e.g. share_pattern resolution; collaborator-class
  resolution; engagement-model resolution).

The bar would require:

1. Sha256 verification that the agent has Read (or Grep'd) the named
   substrate files within the current chat session.
2. A short ratification answer naming what the substrate says vs what
   the action assumes — making any mismatch visible BEFORE the action
   lands rather than after a downstream tranche needs to remediate it.

## Origin (forward-charter)

Operator framing 2026-05-26 during the Wave R+2 doctrine rewrite
context: the post-handshake debrief named the funnel-vision failure
mode in the SUEZ classification context (substrate available; not
re-read; 7-commit rewrite tranche needed to remediate). The candidate
was named in the Wave R+2 Commit 1.5 interstitial substrate-drain
(scratchpad L1805+ context) AND further forward-pointed in the Wave
R+3 SUEZ POC SEND PACK tranche close drain (Commit 4 ratifying
decision D-IH-86-ET §"Forward-pointers").

Surfaced as a forward-charter rather than promoted directly because:

- The discipline shape needs at least one more lived-experience
  worked example before its probe set crystallises (the SUEZ-doctrine
  worked example alone risks over-fitting to one failure mode).
- The mechanical implementation (sha256-pre-action + ratification
  answer) is non-trivial — would need a Pydantic chassis + a
  pre-action gate runbook + integration with inline-ratify gates.
- Per `akos-conflict-surfacing-and-blocker-trackers.mdc` Option-5
  default posture: surface as candidate file rather than promote
  prematurely.

## Activation criteria (when this candidate promotes to an active initiative)

1. At least 2 funnel-vision failure modes have been documented
   post-hoc (the Wave R+2 SUEZ-classification worked example is the
   first; the second emerges naturally in the operator's lived practice
   within ~3-6 months of routine execution).
2. The mechanical implementation pattern is sketched (sha256-pre-action
   probe + ratification answer integration with inline-ratify gates).
3. The operator names a role_owner for the discipline (likely PMO
   interim).
4. A successor decision ID `D-IH-NN-A` is minted to formally promote
   from candidate → charter status.

## Scope (when promoted)

- Canonical doctrine at
  `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/PRE_ACTION_SUBSTRATE_REREAD_DISCIPLINE.md`.
- Pydantic chassis at `akos/hlk_pre_action_substrate_reread.py`.
- Validator at `scripts/validate_pre_action_substrate_reread.py` (sha256
  pre-action ledger + ratification-answer schema validation).
- Paired runbook (e.g. `scripts/pre_action_substrate_reread_gate.py`)
  invokable at the relevant pre-action moments.
- Integration with `inline-ratify-craft` skill (Principle 1 evidence
  sweep already names a sister practice; this specialty would name
  the mechanical enforcement layer).
- Cursor rule at `.cursor/rules/akos-pre-action-substrate-reread.mdc`.
- Paired skill at `.cursor/skills/pre-action-substrate-reread-craft/SKILL.md`.
- Paired SOP `SOP-PEOPLE_PRE_ACTION_SUBSTRATE_REREAD_001.md`.
- 15-surface specialty mint contract per
  `akos-index-integrity.mdc` RULE 5.
- Composes multiplicatively with SYNTHESIS_BEFORE_TRANCHE +
  PROGRAM_CONTINUITY (sister candidate) per `HOLISTIKA_QUALITY_FABRIC.md`
  §3 multiplicative-AND composition.

## Cross-references

- Sister candidate: [`i-nn-program-continuity-discipline.md`](i-nn-program-continuity-discipline.md) — program-boundary discipline; pair with this candidate at program-resume cadence.
- `SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md` (sister 14th specialty; pre-tranche design-layer review; this candidate adds the pre-action substrate-reread layer at a finer-grained cadence).
- `COLLABORATOR_SHARE_DOCTRINE.md` (13th specialty — the worked example for the funnel-vision failure mode that motivated this candidate; the Wave R+2 7-commit rewrite tranche is the proof that the discipline addresses a real and costly failure shape).
- `.cursor/skills/inline-ratify-craft/SKILL.md` Principle 1 evidence sweep (sister practice that names the *what* of substrate re-reading without yet naming the mechanical enforcement layer this candidate would provide).
- `.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc` (this candidate-file shape).
- Wave R+2 Commit 1.5 interstitial substrate-drain (sha `14d992f`; pre-send regression gate spec at `docs/wip/planning/86-initiative-cluster-execution-coordinator/pre-send-regression-gate-spec-2026-05-26.md` is a sibling candidate to this one).
- D-IH-86-ET (ratifying decision row for the I86 Wave R+3 SUEZ POC SEND PACK tranche close, at which this candidate file was first authored as a durable artefact).
