---
status: active
role_owner: Brand Manager
area: Marketing
entity: Holistika
program_id: shared
topic_ids:
  - topic_brand_voice
artifact_role: canonical
intellectual_kind: brand_asset
authority: Operator (lived protocols)
last_review: 2026-04-29
ssot: true
---

# BRAND_VOICE_FOUNDATION

> **Status — Active (Initiative 24 P0a; Operator-authored 2026-04-29).** Operator-lived brand voice per D-IH-17. Maintained by the Brand Manager (CMO chain); annual review trigger lives in `process_list.csv` `thi_mkt_dtp_293` (Initiative 24 P1).

## Voice charter

> Holistika speaks as the rigorous peer who removes uncertainty without performing expertise.

## Archetype

`expert_peer` — see [`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md) for archetype definitions used across the organisation.

## Narrative pillars

1. Evidence over assertion
2. Structure that scales
3. Plain words, deliberate jargon

These three pillars anchor every Holistika message. The composer (`scripts/compose_adviser_message.py`, Initiative 24 P4) validates that drafts align with at least one pillar; messages that align with none flag for operator review.

## Voice IS / IS NOT

See companion [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md) for the per-trait do/don't pairs.

## Register matrix

See companion [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) for the `(relationship, channel) -> register` lookup the composer uses at Layer 4 eloquence resolution.

## Language patterns

Spanish-language patterns (salutations, register matching, jargon-to-refuse) are captured in [`BRAND_SPANISH_PATTERNS.md`](BRAND_SPANISH_PATTERNS.md) — hand-authored companion sourced from real Holistika ↔ external-counsel exchanges. The composer cites it at Layer 4 when `language_preference: es` resolves. English / bilingual patterns get added as separate companions (`BRAND_ENGLISH_PATTERNS.md`, etc.) when the operator surfaces enough lived examples.

## How this is used

The methodology SOP [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md) cites this foundation as **Layer 1 (Brand foundation)**. The composer reads:

- `voice_charter` and `archetype` to validate every outgoing message stays inside the brand envelope.
- `narrative_pillars` to align the message's "why" with one or more pillars.
- The companion register matrix to pick the right tonal register for `(relationship, channel)`.

The **eloquence layer** (Layer 4) operates **inside** the brand voice — it adjusts register, language, and pronoun within the bounds set here. It does not override the brand voice.

## Maintenance

- **Source of truth**: `docs/wip/planning/22a-i22-post-closure-followups/operator-answers-wave2.yaml` Section 2. Edits to this MD by hand will be **overwritten** on next `py scripts/wave2_backfill.py --section brand_voice` — edit the YAML and re-run.
- Annual Brand Manager review (D-IH-17 re-evaluation trigger).
- Per-message dry-run via `py scripts/compose_adviser_message.py --recipient <ref_id> --discipline <id> --dry-run` to surface mismatches.
- Drift detection: if the methodology SOP's brand-foundation citations stop resolving, the next composer run fails loudly.

## Related

- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md)
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md)
- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md)
- Cross-program glossary §"Voice register": [`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md)
