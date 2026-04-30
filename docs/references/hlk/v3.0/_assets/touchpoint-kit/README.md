---
language: en
status: active
role_owner: PMO + Brand Manager
area: Operations / PMO
entity: Holistika Research
authority: Founder + Brand Manager
last_review: 2026-04-30
---

# Touchpoint kit — per-persona × per-channel × per-language templates

**Initiative origin:** Initiative 31 P4.

## What this folder is

The **touchpoint kit** is the per-cell template library of the 5-axis Holistik Ops operating system (`HOLISTIK_OPS_DISCOVERY.md`). Each cell is keyed by:

```
<persona_id>/<channel_id>/<artifact_class>_<language>.md
```

Where:

- `persona_id` — from [`PERSONA_REGISTRY.csv`](../../../../compliance/dimensions/PERSONA_REGISTRY.csv).
- `channel_id` — from [`CHANNEL_TOUCHPOINT_REGISTRY.csv`](../../../../compliance/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv).
- `artifact_class` — `intro_message`, `intro_pack`, `followup`.
- `language` — `en`, `es`, `fr`.

Distance variants (N1, N2, N3, N4) live as **inline sections** within a single template file, per Initiative 31 D-IH-31-H. This avoids the 1.920-cell explosion (16 personas × 10 channels × 4 distances × 3 languages) and keeps the file count proportional to the routing complexity.

## File structure inside each template

Each `intro_message_<lang>.md` carries a frontmatter block + Markdown body with sections:

```markdown
---
language: <code>
persona_id: <PERSONA-...>
channel_id: <CHAN-...>
artifact_class: intro_message
brand_voice: <BRAND_VOICE_FOUNDATION | BRAND_SPANISH_PATTERNS | BRAND_FRENCH_PATTERNS>
last_review: 2026-04-30
---

## Variant — N1 (direct contact)
[message text — assumes deep mutual context; no qualifying gate]

## Variant — N2 (warm referral, bridge known)
[message text — opens by referencing the bridge person]

## Variant — N3 / N4 (cold or chain-traceable)
[message text — runs qualifying gate first; promises follow-up only when answers land]
```

Variants that don't apply to the cell (e.g., a cold investor LinkedIn DM cell rarely sees N1) can be omitted; the file declares which N-bands it covers in frontmatter.

## Initiative 31 P4 seed coverage

The Initiative 31 P4 seed pass ships 8 highest-leverage cells. The remaining persona × channel combinations carry placeholder TODO[OPERATOR-touchpoint-...] markers so the registry FKs resolve but the operator knows which cells are unfilled.

| Persona × Channel | Languages | Distance variants |
|:------------------|:----------|:------------------|
| `PERSONA-INVESTOR-COLD` × `CHAN-LINKEDIN-DM` | en + es | N3, N4 |
| `PERSONA-INVESTOR-WARM` × `CHAN-EMAIL-INBOUND` | en + es | N1, N2 |
| `PERSONA-ADVISOR-REFERRAL` × `CHAN-EMAIL-INBOUND` | es | N1, N2 |
| `PERSONA-PARTNER-JOINT-EQUITY` × `CHAN-EMAIL-INBOUND` | es + en | N2, N3 |
| `PERSONA-TALENT-INBOUND` × `CHAN-WEB-FORM` | en + es | N4 |
| `PERSONA-VENDOR-OUTBOUND` × `CHAN-DIRECT-DM` | en + es | N1, N3, N4 |
| `PERSONA-CUSTOMER-KIRBE-PROSPECT` × `CHAN-WEB-FORM` | es + en | N4 |
| `PERSONA-IDEA-PROPOSER` × `CHAN-DIRECT-DM` | es + en | N1, N2 |

## Cross-references

- [`SOP-HLK_LOCALISATION_001.md`](../../../Admin/O5-1/Tech/System%20Owner/SOP-HLK_LOCALISATION_001.md) — locale policy (per-cell language is audience-driven).
- [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../../../Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) §4.9 — distance assessment.
- [`HOLISTIK_OPS_DISCOVERY.md`](../../../Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md) — 5-axis operating system meta-doc.
- [`BRAND_VOICE_FOUNDATION.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md) — EN voice rules.
- [`BRAND_SPANISH_PATTERNS.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_SPANISH_PATTERNS.md) — ES voice rules.
- [`BRAND_FRENCH_PATTERNS.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_FRENCH_PATTERNS.md) — FR voice rules (stub).
