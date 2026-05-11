---
language: en
status: active
role_owner: PMO
intellectual_kind: template
purpose: literal copy-target for new outbound engagement folders
---

# `_engagement-template/` — outbound engagement template (Holistika provides)

> **What this folder is.** A literal copy-target for new engagement folders under [`../`](../) (`Think Big/Clients/`). Created in P13.3 (2026-05-11) per blueprint §3 / §4. Companion to the inbound template at [`../../Advisers/_engagement-template/`](../../Advisers/_engagement-template/).
>
> **Authoritative shape.** This folder IS the canonical outbound shape. The skeleton encodes the per-root invariants from [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §4. Operators copy-and-rename when starting a new engagement; never re-invent.

## When to use this template

Use for any **outbound** engagement where Holistika is the provider — engagement-types 1 / 2 / 3 / 5 in [blueprint §3](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md):

| Engagement type | Slug shape | Audience for `02-customer-pack/` |
|:---|:---|:---|
| Customer engagement (type 1) | `<YYYY>-<slug>/` | External customer (e.g., `2026-suez-webuy/` for SUEZ) |
| Partner collaboration (type 2) | `<YYYY>-<slug>/` | Partner counterparty + jointly served customer |
| Product engagement (type 3) | `<YYYY>-<slug>/` | SaaS customer |
| Internal capacity (type 5) | `<YYYY>-internal-<slug>/` | **Stakeholder / board / internal-review pack** (no external customer); `_external_marks/` usually empty |

For **inbound** engagements (type 4 — advisers; Holistika is the customer), use the inbound template at [`../../Advisers/_engagement-template/`](../../Advisers/_engagement-template/) instead. The two roots are NOT interchangeable.

## How to use this template

1. **Copy** this folder to a sibling slug under `Think Big/Clients/`. Replace `_engagement-template/` with `<YYYY>-<slug>/` for external types or `<YYYY>-internal-<slug>/` for internal type 5.
2. **Rename** the folder; do NOT keep the underscore prefix (the underscore reserves `_engagement-template/` as the template; new engagement folders use the date-prefixed slug).
3. **Edit the root `README.md`** of the copied folder: replace placeholder tokens (`{{ENGAGEMENT_SLUG}}`, `{{ENGAGEMENT_NAME}}`, `{{COUNTERPARTY_GOI_ID}}`, `{{PARTNER_GOI_ID}}`, `{{PROGRAM_ID}}`, `{{LANGUAGE_CODE}}`) with engagement-specific values.
4. **Delete `.gitkeep` files** in any sub-folder where you add real content — they exist only to keep empty folders tracked at template creation time.
5. **Update each sub-folder `README.md`** to describe the actual material once it lands.
6. **Cross-link** to canonical assets: GOI/POI rows in [`GOI_POI_REGISTER.csv`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv); related `process_list.csv` rows; primary case docs under `Admin/O5-1/<area>/<role>/`.

## Skeleton

```
<YYYY>-<slug>/                     (or <YYYY>-internal-<slug>/ for type 5)
├── README.md                      Engagement scope + status + cross-links
├── 00-internal/                   Operator-only briefs + objection bank + counterparty intel
├── 01-operator-pack/              Operator + collaborator pack (proposal / deck / CDC / discovery)
├── 02-customer-pack/              Customer-facing pack (or internal-stakeholder pack for type 5)
├── _external_marks/               Guest / partner brand assets (usually empty for type 5)
├── _archive/                      Dated rollback snapshots (one sub-folder per archive event)
└── _exports/                      Rendered branded PDFs (tracked) + render-manifest.json
```

## Placeholder tokens

The following tokens appear in template READMEs and engagement-root `README.md` skeletons. Replace at copy time:

| Token | Meaning | Example |
|:---|:---|:---|
| `{{ENGAGEMENT_SLUG}}` | The folder slug | `2026-suez-webuy` |
| `{{ENGAGEMENT_NAME}}` | Human-readable engagement title | "SUEZ WeBuy procure-to-pay automation" |
| `{{COUNTERPARTY_GOI_ID}}` | Primary customer / counterparty GOI ref_id | `GOI-CUS-SUEZ-2026` |
| `{{PARTNER_GOI_ID}}` | Co-branding partner GOI ref_id (optional) | `GOI-PRT-EFA-2026` |
| `{{HOST_BRAND}}` | Co-branding host (usually Holistika) | `Holistika` |
| `{{GUEST_BRAND}}` | Co-branding guest (optional) | `EFA Académie` |
| `{{PROGRAM_ID}}` | `PRJ-*` program identifier (optional) | `PRJ-ENG-SUEZ-WEBUY-2026` |
| `{{LANGUAGE_CODE}}` | Primary engagement language | `fr` / `en` / `es` |
| `{{RELATED_PARTY}}` | `true` if engagement is related-party per blueprint; else empty | `true` for `2026-asesoria-hosteleria/` |

## Cross-references

- Blueprint: [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) — engagement-types matrix, per-root folder shape, file-tracking policy
- Clients root: [`../README.md`](../README.md) — naming convention, active engagements
- Inbound counterpart: [`../../Advisers/_engagement-template/`](../../Advisers/_engagement-template/) — when Holistika is the customer
- PMO hub: [`../../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](../../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) — engagement portfolio
- Co-branding pattern: [`../../../Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md) — host/guest semantics drive `_external_marks/`
- Reference engagement: [`../2026-suez-webuy/`](../2026-suez-webuy/) — the SUEZ engagement is the canonical example of this template applied
