---
language: en
intellectual_kind: initiative_candidate
sharing_label: internal_only
audience: J-OP
authored: 2026-05-27
last_review: 2026-05-27
status: candidate
parent_canonical: docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
forward_charter_source: operator framing 2026-05-26 post-handshake transcript ("bound to get lost")
ratifying_decisions:
  - D-IH-86-ET
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md
external_references: []
---

# Candidate — I-NN: Program continuity discipline ("bound to get lost" mitigation)

## Purpose

Mint a candidate 15th (or later) Quality Fabric specialty addressing
the operator's lived failure mode at the boundary between two distinct
multi-week programs (e.g. the operator switches from SUEZ engagement
to Websitz engagement to investor-pack work to Madeira elevation work
within the same week, and substrate from the prior program risks
getting "bound to get lost" — operator's verbatim 2026-05-26 framing).

The discipline names a mechanical bar future agents and operators
inherit by default when shifting work attention from program A to
program B AND back to program A at a later date.

Concretely, the program-continuity discipline would govern:

- The minimum substrate-state-of-the-program snapshot that program A
  carries forward before the operator's attention shifts to program B
  (a durable artefact rather than chat-memory).
- The minimum re-read protocol future agents follow when the operator
  returns attention to program A (pre-action substrate re-read; sister
  to candidate `i-nn-pre-action-substrate-reread-discipline.md`).
- The decision-lineage continuity contract: when program A is paused
  for ≥ 1 calendar week, which `D-IH-NN-X` decision rows ratify the
  pause + the resumption framing.
- The cross-program coherence audit: when two programs ship competing
  artefacts to overlapping audience classes (e.g. SUEZ POC FULL KIT +
  investor stability dossier both reference the 13th+14th Quality
  Fabric specialties as IP-moat narrative), the coherence audit names
  the SSOT and prevents semantic drift between the two surfaces.

## Origin (forward-charter)

Operator framing 2026-05-26 verbatim during the SUEZ recommercialisation
post-handshake debrief: *"bound to get lost"* in the context of program-
boundary attention shifts. The framing surfaced repeatedly across the
Wave R+2 doctrine rewrite (7 commits over 2 days) + Wave R+3 SUEZ POC
SEND PACK tranche (4 commits + 1 chore hygiene over 1 day) where the
operator's attention shifted between collaborator-share doctrine work +
SUEZ customer-pack authoring + chore hygiene + standards-directive
self-audit — each shift carried risk that load-bearing substrate from
the prior context would be lost when the next context opened.

The discipline candidate is the durable carryover artefact for that
forward-charter, per [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc)
Option-5 default posture: surface the program-continuity gap as a
candidate file rather than promote prematurely OR conflate with an
in-flight engagement-class tranche.

## Activation criteria (when this candidate promotes to an active initiative)

1. At least 2 program-boundary failure modes (one of "bound to get
   lost" class) have been documented post-hoc by the operator OR an
   agent — proof that the discipline addresses a recurring rather
   than one-off failure shape.
2. The operator names a role_owner for the discipline (likely PMO
   interim until COO activation per I76 lineage).
3. A draft 5-7 dimension probe set has been sketched (analogous to
   SYNTHESIS_BEFORE_TRANCHE's 10-dim + INDEX_INTEGRITY's 8-dim).
4. A successor decision ID `D-IH-NN-A` is minted to formally promote
   from candidate → charter status.

## Scope (when promoted)

- Canonical doctrine at
  `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/PROGRAM_CONTINUITY_DISCIPLINE.md`
  per `akos-people-discipline-of-disciplines.mdc` Rule 1 (People owns
  the cross-area pattern).
- Pydantic chassis at `akos/hlk_program_continuity.py`.
- Validator at `scripts/validate_program_continuity.py` (status
  enum + program-state-snapshot frontmatter + re-read-protocol
  artefact existence + cross-program coherence audit).
- Paired runbook (e.g. `scripts/program_continuity_snapshot.py`)
  invokable at program-pause + program-resume cadence per
  `akos-executable-process-catalog.mdc` Rule 1.
- Cursor rule at `.cursor/rules/akos-program-continuity.mdc`.
- Paired skill at `.cursor/skills/program-continuity-craft/SKILL.md`.
- Paired SOP `SOP-PEOPLE_PROGRAM_CONTINUITY_001.md`.
- 15-surface specialty mint contract per
  `akos-index-integrity.mdc` RULE 5 (canonical + chassis + validator
  + runbook + cursor rule + skill + SOP+runbook pair + pattern-registry
  row + PRECEDENCE row + Quality Fabric §6 row + CHANGELOG + process_list
  row + validate_hlk umbrella + verification-profiles + release-gate
  wiring).
- Composes multiplicatively with SYNTHESIS_BEFORE_TRANCHE (pre-tranche
  design-layer review) + INTER_WAVE_REGRESSION (post-wave execution-
  layer regression) + INDEX_INTEGRITY (post-canonical-mint index
  freshness) per `HOLISTIKA_QUALITY_FABRIC.md` §3 multiplicative-AND
  composition — covers the program-lifecycle cadence that the existing
  3 specialties don't.

## Cross-references

- Sister candidate: [`i-nn-pre-action-substrate-reread-discipline.md`](i-nn-pre-action-substrate-reread-discipline.md) — funnel-vision substrate re-read mitigation; pair with this discipline at program-resume cadence.
- `HOLISTIKA_QUALITY_FABRIC.md` (parent meta-doctrine; 5-axis composition; would extend to 15+ specialties when this candidate promotes).
- `SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md` (sister 14th specialty; design-layer pre-tranche review; this candidate adds the program-boundary layer).
- `INDEX_INTEGRITY_DISCIPLINE.md` + `INTER_WAVE_REGRESSION_DISCIPLINE.md` (sister 11th + 10th specialties; post-commit cadence specialties).
- `COLLABORATOR_SHARE_DOCTRINE.md` (13th specialty — the worked example for the operator's lived "bound to get lost" failure mode at the SUEZ/Websitz program boundary).
- `.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc` (this candidate-file shape).
- D-IH-86-ET (ratifying decision row for the I86 Wave R+3 SUEZ POC SEND PACK tranche close, at which this candidate file was first authored).
