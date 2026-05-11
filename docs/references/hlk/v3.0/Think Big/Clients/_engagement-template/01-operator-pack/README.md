---
language: en
role_owner: PMO
purpose: operator + collaborator pack
audience: operator + collaborator (named partner / guest)
---

# `01-operator-pack/` — operator + collaborator pack

This sub-folder holds the **operator-and-collaborator** view of the engagement: the proposal with internal tarification, the deck, the CDC feasibility shape, and the discovery questionnaire. These materials may include pricing, internal cost reasoning, and partner-specific framing that does NOT belong in the customer-facing pack.

## Audience

Operator + named partner or guest counterparty (the collaborator who works the engagement alongside Holistika). The customer never sees these materials directly — they receive the redacted / pricing-free versions from [`../02-customer-pack/`](../02-customer-pack/).

## Typical contents

- `proposal.<lang>.md` — full proposal with internal tarification annex; per `SOP-ENG_PROPOSAL_001.md`
- `deck-<engagement-slug>.<lang>.md` — pitch / context deck for joint meetings
- `cdc-feasibility-shape.<lang>.md` — feasibility shape per `SOP-ENG_ENGAGEMENT_DESIGN_001.md`
- `discovery-questionnaire.<lang>.md` — discovery elicitation per `SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md`

## Conventions

- Language suffix is mandatory (`.fr.md`, `.en.md`, `.es.md`).
- Internal tarification reasoning lives here (in the proposal annex or a separate `tarification.<lang>.md`); the customer pack receives a redacted / pricing-shape-only version.
- Cross-link to the source process rows in [`process_list.csv`](../../../../compliance/process_list.csv) — `hol_eng_prc_proposal_001`, `hol_eng_prc_discovery_questionnaire_001`, `hol_eng_prc_engagement_design_001`, `hol_eng_prc_estimation_001`.
- For type-5 internal-capacity engagements, this folder holds the operator-level material; `02-customer-pack/` becomes the stakeholder / board pack instead.

## Cross-references

- Engagement template root: [`../README.md`](../README.md)
- Customer pack: [`../02-customer-pack/README.md`](../02-customer-pack/README.md)
- Reference engagement: [`../../2026-suez-webuy/01-operator-pack/`](../../2026-suez-webuy/01-operator-pack/) — canonical example
