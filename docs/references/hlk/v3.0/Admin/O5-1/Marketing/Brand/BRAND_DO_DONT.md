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
---

# BRAND_DO_DONT

> **Status — Scaffold awaiting discovery (Initiative 24 P0a; D-IH-24-A)**: Operator fills YAML Section 2 `brand_voice.voice_is[]` and `voice_is_not[]` and runs `py scripts/wave2_backfill.py --section brand_voice`. The scaffolder writes the tables below from the operator's rows.

## Voice IS — operator-pending

| Trait | Example phrasing |
|:------|:-----------------|
| _operator-pending_ | _operator-pending_ |
| _operator-pending_ | _operator-pending_ |
| _operator-pending_ | _operator-pending_ |

## Voice IS NOT — operator-pending

| Trait | Example of what we'd refuse to say |
|:------|:-----------------------------------|
| _operator-pending_ | _operator-pending_ |
| _operator-pending_ | _operator-pending_ |
| _operator-pending_ | _operator-pending_ |

## How the composer uses this

Per-message reviewer checks (every layer-4 eloquence pass):

- The proposed phrasing matches at least one **Voice IS** trait.
- The proposed phrasing does **not** match any **Voice IS NOT** pattern.

When ambiguous, the composer flags the message for operator review rather than auto-generate.

## Related

- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md)
- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md)
- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md)
