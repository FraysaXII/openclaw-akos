---
language: en
intellectual_kind: initiative_candidate
sharing_label: internal_only
audience: J-OP
authored: 2026-05-23
last_review: 2026-05-23
status: candidate
parent_canonical: docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
forward_charter_source: HOLISTIKA_QUALITY_FABRIC.md forward_charters
ratifying_decisions:
  - D-IH-86-CR
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv
external_references: []
---

# Candidate — I-NN: Channel doctrines (per-channel goods/bads research)

## Purpose

Mint a per-channel doctrine library covering the high-traffic communication
channels operated by Holistika (Email-outbound, Email-inbound, LinkedIn-DM,
LinkedIn-post-response, Web-form, Cal-schedule, Event-meeting, Ad-campaign).
Each channel doctrine documents:

- Goods (what works for this channel, with industry research grounding)
- Bads (anti-patterns specific to this channel)
- Audience pairings (which AUDIENCE_REGISTRY classes this channel reaches)
- Format pairings (which 6-surface render formats are acceptable)
- Cadence + frequency norms
- Brand-register translations specific to the channel (per dual-register
  contract in `BRAND_BASELINE_REALITY_MATRIX.md`)
- Measurement primitives (which signals indicate channel-effective vs
  channel-noise)

## Origin (forward-charter)

`HOLISTIKA_QUALITY_FABRIC.md` declares a forward-charter row reading:

> I-NN-CHANNEL-DOCTRINES (per-channel goods/bads research; activation
> gates HOLISTIKA_QUALITY_FABRIC P1 + 1 channel research pass)

This candidate is minted as the durable carryover artefact for that
forward-charter, per [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc)
Option-5 default posture: surface the forward-charter as a candidate
file rather than promote prematurely.

Surfaced as a gap finding at the Wave-Q regression sweep
(2026-05-22) under DIM-02 FORWARD-CHARTER-CARRYOVER; dispositioned
**forward-charter-next-wave** at the Wave R Lane B drain (D-IH-86-CR).

## Activation criteria (when this candidate promotes to an active initiative)

1. `HOLISTIKA_QUALITY_FABRIC.md` reaches P1 (per its own roadmap).
2. At least 1 channel has accumulated ≥ 1 quarter of operational signal
   to ground the doctrine in lived experience (not just industry research).
3. Operator names a Marketing/Resonance/RevOps owner for the discipline
   (`role_owner` per `baseline_organisation.csv`).
4. A successor decision ID `D-IH-NN-A` is minted to formally promote.

## Scope (when promoted)

- Per-channel doctrine canonicals at
  `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Reach/canonicals/<channel>_DOCTRINE.md`
  OR equivalent area-owned path per `akos-people-discipline-of-disciplines.mdc`
  Rule 1 (other areas author their own processes; People mints the pattern).
- Cross-references to `CHANNEL_TOUCHPOINT_REGISTRY.csv` rows (FK).
- Cross-references to `akos-external-render-discipline.mdc` RULE 7
  channel-format compatibility table.
- Validator + pre-commit gate when the doctrine reaches `status:active`.

## Cross-references

- `HOLISTIKA_QUALITY_FABRIC.md` §6 (forward-charter origin).
- `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv` (channel ID source).
- `.cursor/rules/akos-external-render-discipline.mdc` RULE 7 (3-axis channel x audience x format framing).
- `.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc` (this candidate-file shape).
- D-IH-86-CR (Wave R Lane B drain ratifying decision).
- `docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/regression-sweep-2026-05-22.md` (originating gap finding).
