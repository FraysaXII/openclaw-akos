---
language: en
role_owner: PMO
purpose: customer-facing pack (or internal-stakeholder pack for type 5)
audience: customer (with optional named host / guest header); or internal stakeholders for type-5 internal-capacity engagements
---

# `02-customer-pack/` — customer-facing pack

This sub-folder holds the **customer-facing** view of the engagement: the customer-segmented proposal (pricing redacted or surfaced separately), the customer deck, and any tarification annex shared with the customer.

For **type-5 internal-capacity engagements** (`<YYYY>-internal-<slug>/`), this folder is repurposed as the **stakeholder / board / internal-review pack** (no external customer). Tooling parity preserves the renderer and manifest conventions.

## Audience

- External engagements (types 1 / 2 / 3): customer (the external counterparty), often with an optional named host / guest header per [`BRAND_COBRANDING_PATTERN.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md).
- Internal-capacity engagements (type 5): internal stakeholders / board / capacity reviewers; the "customer" is the operator's own organization.

## Typical contents

- `proposal.customer.<lang>.md` — customer-segmented proposal (pricing redacted or referenced via annex)
- `deck.customer.<lang>.md` — customer-facing deck (co-branded header where applicable)
- `tarification.customer.<lang>.md` — separate tarification annex (when proposal is pricing-free)

## Conventions

- Language suffix is mandatory (`.fr.md`, `.en.md`, `.es.md`).
- The `.customer.` infix is a strong convention: it distinguishes customer-facing assets from operator-pack equivalents in flat search results.
- Co-branded surfaces (host=Holistika / guest=`{{PARTNER_GOI_ID}}` or polarity-flipped) consume guest assets from [`../_external_marks/`](../_external_marks/) per [`BRAND_COBRANDING_PATTERN.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md).
- For type-5 internal engagements: drop the `.customer.` infix in favor of `.stakeholder.` or similar if internal-review framing is clearer.

## Cross-references

- Engagement template root: [`../README.md`](../README.md)
- Operator pack: [`../01-operator-pack/README.md`](../01-operator-pack/README.md)
- Co-branding: [`../../../Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md`](../../../Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md)
- Reference engagement: [`../../2026-suez-webuy/02-customer-pack/`](../../2026-suez-webuy/02-customer-pack/) — canonical example with separate tarification annex
