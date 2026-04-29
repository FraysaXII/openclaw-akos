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

# BRAND_DO_DONT

> **Status — Active (Initiative 24 P0a; Operator-authored 2026-04-29).** Auto-emitted by `scripts/wave2_backfill.py --section brand_voice` from `operator-answers-wave2.yaml` Section 2 `brand_voice.voice_is` / `voice_is_not`. Edit the YAML and re-run.

## Voice IS

| Trait | Example phrasing |
|:------|:-----------------|
| Rigorous | We base this decision on the 2026-04-01 fact pattern. |
| Structured | Three options ranked by reversibility. Option A is recommended. |
| Plain | We need to file the constitution before activating Stripe billing. |

## Voice IS NOT

| Trait | Example of what we'd refuse to say |
|:------|:-----------------------------------|
| Performative | We are delighted to announce our expert analysis. |
| Vague | We feel this is the right approach overall. |
| Jargon-heavy | Our holistic synergistic methodology paradigmatically de-risks the engagement. |

## How the composer uses this

Per-message reviewer checks (every Layer-4 eloquence pass):

- The proposed phrasing matches at least one **Voice IS** trait.
- The proposed phrasing does **not** match any **Voice IS NOT** pattern.

When ambiguous, the composer flags the message for operator review rather than auto-generate.

## Related

- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md)
- [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md)
- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md)
