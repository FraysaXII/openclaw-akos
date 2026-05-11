---
language: en
status: active
role_owner: PMO
intellectual_kind: template
purpose: literal copy-target for new inbound engagement folders
---

# `_engagement-template/` — inbound engagement template (Holistika contracts)

> **What this folder is.** A literal copy-target for new engagement folders under [`../`](../) (`Think Big/Advisers/`). Created in P13.3 (2026-05-11) per blueprint §3 / §4. Companion to the outbound template at [`../../Clients/_engagement-template/`](../../Clients/_engagement-template/).
>
> **Authoritative shape.** This folder IS the canonical inbound shape. The skeleton encodes the per-root invariants from [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §4. Operators copy-and-rename when starting a new inbound engagement; never re-invent.

## When to use this template

Use for any **inbound** engagement where Holistika is the customer of external advisers — engagement-type 4 in [blueprint §3](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md):

| Adviser discipline | Counterparty class (GOI/POI) | Example |
|:---|:---|:---|
| Legal counsel | `external_adviser` / `public_authority` (notaries, registry) | `POI-LEG-ENISA-LEAD-2026`, `POI-LEG-FISCAL-LEAD-2026` |
| Banking channel | `banking_channel` | `GOI-BNK-INC-2026`, `POI-BNK-DESK-LEAD-2026` |
| Fiscal / accounting | `external_adviser` | fiscal-track adviser at incorporation adviser firm |
| Startup certification | `external_adviser` / `public_authority` | ENISA-track adviser; ENISA itself when surfaced |

For **outbound** engagements (types 1 / 2 / 3 / 5; Holistika provides), use the outbound template at [`../../Clients/_engagement-template/`](../../Clients/_engagement-template/) instead. The two roots are NOT interchangeable.

## How to use this template

1. **Copy** this folder to a sibling slug under `Think Big/Advisers/`. Replace `_engagement-template/` with `<YYYY>-<slug>/` (e.g. `2026-holistika-incorporation/`).
2. **Rename** the folder; do NOT keep the underscore prefix.
3. **Edit the root `README.md`** of the copied folder: replace placeholder tokens (`{{ENGAGEMENT_SLUG}}`, `{{ENGAGEMENT_NAME}}`, `{{ADVISER_GOI_ID}}`, `{{DISCIPLINE}}`, `{{MANDATE_PHASE}}`, `{{LINKED_PROGRAM_ID}}`).
4. **Delete `.gitkeep` files** in any sub-folder where you add real content.
5. **Update each sub-folder `README.md`** to describe the actual material once it lands.
6. **Cross-link** to canonical assets — the inbound folder is a **unified entry point** that POINTS INTO existing canonicals:
   - [`EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`](../../../Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md) — handoff doc for external counsel
   - [`FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md`](../../../Admin/O5-1/People/Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md) — incorporation knowledge index
   - [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../../Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) — ADVOPS plane SOP
   - `ADVISER_*` CSVs under [`compliance/`](../../../../compliance/) — adviser engagement / open questions / filed instruments
   - Relevant `GOI-ADV-*` / `POI-LEG-*` / `POI-BNK-*` rows in [`GOI_POI_REGISTER.csv`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv)

## Skeleton

```
<YYYY>-<slug>/
├── README.md                      Engagement scope + mandate + cross-links
├── 00-internal/                   Operator-only notes; GOI/POI cross-links
├── 01-our-pack/                   Material WE send to advisers (brief / KYC / scope)
├── 02-adviser-pack/               Material WE receive (opinions / evidence / confirmations)
├── _archive/                      Dated rollback snapshots
└── _exports/                      Rendered branded PDFs (tracked) + render-manifest.json
```

**No `_external_marks/` under the inbound template.** We are the customer; there is no host/guest co-branding posture. Advisers brand themselves; Holistika receives their outputs.

## Placeholder tokens

| Token | Meaning | Example |
|:---|:---|:---|
| `{{ENGAGEMENT_SLUG}}` | The folder slug | `2026-holistika-incorporation` |
| `{{ENGAGEMENT_NAME}}` | Human-readable engagement title | "Founder incorporation + ENISA evidence + fiscal readiness" |
| `{{ADVISER_GOI_ID}}` | Primary adviser firm GOI ref_id | `GOI-ADV-ENTITY-2026` |
| `{{DISCIPLINE}}` | Adviser discipline | `legal_constitution` / `banking_kyc` / `fiscal_readiness` / `enisa_certification` |
| `{{MANDATE_PHASE}}` | Current mandate phase | `intake` / `discovery` / `drafting` / `filing` / `closure` |
| `{{LINKED_PROGRAM_ID}}` | `PRJ-*` program identifier | `PRJ-HOL-FOUNDING-2026` |
| `{{LANGUAGE_CODE}}` | Primary engagement language | `es` / `en` / `fr` |

## Cross-references

- Blueprint: [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) — engagement-types matrix, per-root folder shape
- Advisers root: [`../README.md`](../README.md) — inbound naming conventions, active engagements (created in P13.5)
- Outbound counterpart: [`../../Clients/_engagement-template/`](../../Clients/_engagement-template/) — when Holistika provides
- ADVOPS canonical: [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../../Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) — operator runbook for engaging external advisers
- External counsel handoff: [`EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`](../../../Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md) — material we hand off
- Founder incorporation: [`FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md`](../../../Admin/O5-1/People/Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md) — incorporation-program knowledge index
- PMO hub: [`TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](../../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md)
