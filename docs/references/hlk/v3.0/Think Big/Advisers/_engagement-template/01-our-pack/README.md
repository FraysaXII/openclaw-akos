---
language: en
role_owner: PMO
purpose: material WE send to the adviser
audience: external adviser (named counterparty)
---

# `01-our-pack/` — material we send to the adviser

This sub-folder holds material that **Holistika sends** to the adviser counterparty: scope-of-mandate briefs, KYC packs, redaction-safe context summaries, and any other artifacts the adviser needs to deliver their opinion / evidence / filing.

This is the inbound counterpart to the outbound `01-operator-pack/` — material we author, in the inbound direction "operator pack" means "what we send".

## Audience

Named adviser counterparty (the firm or individual on the engagement). Pre-shared via Drive, email, or secure handoff per the adviser's intake process.

## Typical contents

- `scope-of-mandate.<lang>.md` — explicit scope of what we ask the adviser to do; deliverable list; deadline; pricing posture; cross-link to `ADVISER_ENGAGEMENT_DISCIPLINES.csv`
- `kyc-pack.<lang>.md` — Know-Your-Client material the adviser firm needs: legal-entity registration, beneficial-owner declaration, contact officers, EIDAS / DNI-NIE references
- `context-brief.<lang>.md` — redaction-safe summary of why we engage them, what they need to know about adjacent advisers and the founder-program context (cross-links to `FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md`)
- `open-questions.<lang>.md` — questions WE pose to the adviser; cross-link to `ADVISER_OPEN_QUESTIONS.csv` rows

## Conventions

- Language suffix is mandatory (`.es.md`, `.en.md`, `.fr.md`).
- The infix `our` makes it unambiguous in flat search that this is OUR material going OUT.
- KYC packs are confidential — even in redaction-safe form they contain entity-identifying material. Do NOT export to a public-readable rendering surface; the audience is the named adviser.
- Cross-link to [`EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`](../../../Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md) for the canonical handoff pattern.

## Cross-references

- Engagement template root: [`../README.md`](../README.md)
- Adviser pack (inbound material we receive): [`../02-adviser-pack/README.md`](../02-adviser-pack/README.md)
- External counsel handoff canonical: [`../../../Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`](../../../Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md)
- ADVOPS SOP: [`../../../Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../../Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md)
