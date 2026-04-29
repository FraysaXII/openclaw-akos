---
status: scaffold-awaiting-discovery
role_owner: Brand Manager
area: Marketing
entity: Holistika
program_id: shared
topic_ids:
  - topic_brand_voice
artifact_role: canonical
intellectual_kind: brand_asset
authority: Operator (lived protocols)
last_review: pending
ssot: true
---

# BRAND_VOICE_FOUNDATION

> **Status — Scaffold awaiting discovery (Initiative 24 P0a; D-IH-24-A)**: This document is a **scaffold** until the brand manager fills Section 2 of [`docs/wip/planning/22a-i22-post-closure-followups/operator-answers-wave2.yaml`](../../../../../../wip/planning/22a-i22-post-closure-followups/operator-answers-wave2.yaml) and runs `py scripts/wave2_backfill.py --section brand_voice`. The scaffolder writes the operator's answers verbatim into this file and flips `status:` to `active`. Do **not** invent brand voice in this scaffold — that is the operator's expertise (D-IH-17). Composer (`scripts/compose_adviser_message.py`) refuses to resolve brand-foundation tokens while `status: scaffold-awaiting-discovery` unless `--allow-scaffold-tokens` is set explicitly for dry-run.

## Voice charter

> One sentence describing how Holistika speaks across all channels.
>
> **Operator-pending** (YAML Section 2 `brand_voice.voice_charter`).

## Archetype

> Single token; common choices: `expert_peer`, `trusted_advisor`, `rigorous_specialist`, `curious_explorer`, `calm_orchestrator`.
>
> **Operator-pending** (YAML Section 2 `brand_voice.archetype`).

## Narrative pillars

> 3 pillars; the recurring themes that anchor every message.
>
> **Operator-pending** (YAML Section 2 `brand_voice.narrative_pillars[]`).

1. _Pillar 1 — pending_
2. _Pillar 2 — pending_
3. _Pillar 3 — pending_

## Voice IS / IS NOT

See companion [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) (also scaffold-staged).

## Register matrix

See companion [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) (also scaffold-staged).

## How this is used

The methodology SOP [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md) cites this foundation as **Layer 1 (Brand foundation)**. The composer reads:

- `voice_charter` and `archetype` to validate every outgoing message stays inside the brand envelope.
- `narrative_pillars` to align the message's "why" with one or more pillars.
- The companion register matrix to pick the right tonal register for `(relationship, channel)`.

The **eloquence layer** (Layer 4) operates **inside** the brand voice — it adjusts register, language, and pronoun within the bounds set here. It does not override the brand voice.

## Maintenance

- Annual Brand Manager review (D-IH-17 re-evaluation trigger).
- Per-message dry-run via `py scripts/compose_adviser_message.py --recipient <ref_id> --discipline <id> --dry-run` to surface mismatches.
- Drift detection: if the methodology SOP's brand-foundation citations stop resolving, the next composer run fails loudly.

## Related

- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md)
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md)
- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md)
- Cross-program glossary §"Voice register": [`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md)
