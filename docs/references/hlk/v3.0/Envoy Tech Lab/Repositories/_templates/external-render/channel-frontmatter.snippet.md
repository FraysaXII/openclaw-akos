---
template_id: external-render/channel-frontmatter
status: active
authority: System Owner
language: en
last_review: 2026-05-19
linked_decisions:
  - D-IH-86-P (external-render discipline canonization)
  - D-IH-86-Q (Wave F INFO->FAIL gate flip)
  - D-IH-86-S (Wave G B-G2 channel-frontmatter onboarding template mint)
---

# `channel:` frontmatter snippet — when authoring or editing an external-delivery surface

Use this snippet when authoring or editing any markdown surface under
`docs/references/hlk/v3.0/_assets/advops/**/*.md` or
`docs/references/hlk/v3.0/Think Big/Advisers/**/*.md` that carries an external
`audience:` tag (J-IN / J-CU / J-PT / J-AD / J-ENISA / J-RC / J-CO).

Per [`akos-external-render-discipline.mdc`](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc)
RULE 7 (Wave F, 2026-05-19), every external surface answers three questions —
audience (who?) + channel (through what inbound/outbound path?) + format (PDF /
Web / ERP / Mail / Slide / Broadcast). The `audience:` and rendered artifact
already cover the *who* and the *format*. The `channel:` frontmatter field is
the *path* dimension — it is **optional** advisory metadata; when present, the
drift-gate validator FK-resolves it against
[`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../../../../Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv)
at INFO advisory.

## Snippet — paste inside frontmatter

```yaml
# Inside an external-delivery surface frontmatter (e.g. dossier_*.md, cover_email_*.md, deck_*.md):
audience: [J-ENISA]          # required: who is the recipient (FK to AUDIENCE_REGISTRY.csv)
channel: [CHAN-DIRECT-DM]    # advisory: the inbound/outbound path (FK to CHANNEL_TOUCHPOINT_REGISTRY.csv)
language: es                 # required if external prose carries a locale
```

## How to look up the right channel IDs

1. Open [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../../../../Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv).
2. Match the `direction` column against your surface's delivery posture
   (inbound = they reach you; outbound = you reach them; bidirectional = both).
3. Match the `typical_personas` column against your `audience:` tag's typical
   persona class via [`AUDIENCE_REGISTRY.csv`](../../../../Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv).
4. Pick one or more `channel_id` values for the `channel:` list. Multi-channel
   composition is normal (see examples below).
5. If no existing code fits cleanly, **do not invent a new code locally** —
   open a successor canonical-CSV gate to mint the new code per
   [`akos-mirror-template.mdc`](../../../../../../../../.cursor/rules/akos-mirror-template.mdc) §"Never invent HLK IDs locally".
   In the interim, omit `channel:` (absence is not a finding); the validator
   no-ops on missing channel metadata.

## Example blocks — realistic cases

### Case 1 — Founder-initiated outbound email with PDF attachment (J-ENISA dossier)

```yaml
audience: [J-ENISA]
channel: [CHAN-DIRECT-DM]
language: es
artifact_role: adviser_evidence_appendix
```

*Rationale:* The dossier is sent as a PDF attachment via the founder's personal
email. `CHAN-DIRECT-DM` (bidirectional; covers founder's outbound personal
email per the registry `notes` column) is the closest fit until
`CHAN-EMAIL-OUTBOUND` is minted in a successor canonical-CSV tranche.

### Case 2 — Public web page + paid-ad amplification (J-CU / J-RC founder bio)

```yaml
audience: [J-CU, J-RC]
channel: [CHAN-SEARCH-ORGANIC, CHAN-AD-CAMPAIGN]
language: en
artifact_role: public_canonical
```

*Rationale:* The founder bio lives at `holistikaresearch.com/founder` (web
surface) and is reached via both organic search (SEO) and paid ad campaigns
when those activate. Two channels in the list captures both paths.

### Case 3 — Deck used in a live meeting + sent as sealed attachment (J-IN investor deck)

```yaml
audience: [J-IN]
channel: [CHAN-EVENT-MEETING, CHAN-DIRECT-DM]
language: en
artifact_kind: deck_template
```

*Rationale:* The investor deck is presented at scheduled meetings
(`CHAN-EVENT-MEETING`) AND sent as a sealed PDF afterwards
(`CHAN-DIRECT-DM`). Two-channel composition reflects the actual delivery
practice. Note: `artifact_kind: deck_template` exempts the surface from the
render-trail enforcement check, but the `channel:` advisory remains useful as
pre-populated metadata for per-engagement instances copied from this template.

## Validator behaviour

When `channel:` is present:

- [`scripts/validate_external_render_trail.py`](../../../../../../../../scripts/validate_external_render_trail.py)
  parses the YAML list (or scalar) and FK-resolves each `CHAN-*` code against
  the registry.
- Unknown codes surface as INFO-advisory findings; they never fail CI
  (Wave F doctrine: channel is the *enabling* axis, not a blocking gate).
- The validator emits a summary line including `with channel-tag <N>` and
  `unknown channel codes <M>` counters.

When `channel:` is absent:

- The validator no-ops (absence is not a finding; channel is optional).
- The surface is still required to satisfy the render-trail discipline per
  RULE 4 + RULE 6.

## Cross-references

- [`.cursor/rules/akos-external-render-discipline.mdc`](../../../../../../../../.cursor/rules/akos-external-render-discipline.mdc) §RULE 7 — the *when* rule for channel tagging.
- [`.cursor/skills/external-render-craft/SKILL.md`](../../../../../../../../.cursor/skills/external-render-craft/SKILL.md) §"Surface 0" + §"Authoring `channel:` frontmatter" — the *how* skill.
- [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../../../../Admin/O5-1/People/Compliance/canonicals/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv) — the FK source.
- [`AUDIENCE_REGISTRY.csv`](../../../../Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) — the audience FK source.
- D-IH-86-S (template mint at Wave G B-G2) + D-IH-86-Q (Wave F closure of RULE 6 ramp) + D-IH-86-P (RULE 6 ramp inception) in [`DECISION_REGISTER.csv`](../../../../Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv).
