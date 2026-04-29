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

# BRAND_REGISTER_MATRIX

> **Status — Scaffold awaiting discovery (Initiative 24 P0a; D-IH-24-A)**: Operator fills YAML Section 2 `brand_voice.register_matrix[]` and runs `py scripts/wave2_backfill.py --section brand_voice`. The scaffolder writes the table below from the operator's rows.

## How (relationship, channel) maps to a register

The composer looks up the (relationship, channel) pair against this matrix to pick the right tonal register. When a pair is missing, the composer falls back to the discipline default (`ADVISER_ENGAGEMENT_DISCIPLINES.csv`), then to the brand foundation default (archetype-implied register).

> **Operator-pending — YAML Section 2 carries the canonical rows.** Below is the YAML default seed (illustrative; will be re-emitted by the scaffolder when Section 2 is filled).

| Relationship | Channel | Register |
|:------------|:-------|:---------|
| external_counsel | email | formal_legal |
| peer_founder | dm | peer_consulting |
| regulator | memo | regulator_neutral |
| investor | deck | investor_aspirational |
| client_prospect | proposal | _operator-pending_ |
| internal_team | slack | casual_internal |

Common register tokens: `formal_legal`, `peer_consulting`, `casual_internal`, `regulator_neutral`, `investor_aspirational`. Add new tokens by extending YAML Section 2 + (optionally) the `voice_register` enum on `GOI_POI_REGISTER.csv` (Initiative 24 P2).

## Related

- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md)
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md)
- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md) §3 Use-case layer
- Cross-program glossary §"Voice register": [`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md)
