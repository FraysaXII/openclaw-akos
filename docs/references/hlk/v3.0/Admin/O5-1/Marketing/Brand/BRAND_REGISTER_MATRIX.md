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
---

# BRAND_REGISTER_MATRIX

> **Status — Active (Initiative 24 P0a; Operator-authored 2026-04-29).** Auto-emitted by `scripts/wave2_backfill.py --section brand_voice` from `operator-answers-wave2.yaml` Section 2 `brand_voice.register_matrix`. Edit the YAML and re-run; do **not** edit this file by hand — it will be overwritten.

## How (relationship, channel) maps to a register

The composer (`scripts/compose_adviser_message.py`, Initiative 24 P4) looks up the (relationship, channel) pair against this matrix to pick the right tonal register. When a pair is missing, the composer falls back to the discipline default (`ADVISER_ENGAGEMENT_DISCIPLINES.csv`), then to the brand foundation default (archetype-implied register).

| Relationship | Channel | Register |
|:-------------|:--------|:---------|
| external_counsel | email | `formal_legal` |
| peer_founder | dm | `peer_consulting` |
| regulator | memo | `regulator_neutral` |
| investor | deck | `investor_aspirational` |
| client_prospect | proposal | `peer_consulting` |
| internal_team | slack | `casual_internal` |

Common register tokens: `formal_legal`, `peer_consulting`, `casual_internal`, `regulator_neutral`, `investor_aspirational`. Add new tokens by extending YAML Section 2 + (optionally) the `voice_register` enum on `GOI_POI_REGISTER.csv` (Initiative 24 P2).

## Related

- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md)
- [`BRAND_DO_DONT.md`](BRAND_DO_DONT.md)
- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md) §3 Use-case layer
- Cross-program glossary §"Voice register": [`docs/reference/glossary-cross-program.md`](../../../../../../reference/glossary-cross-program.md)
