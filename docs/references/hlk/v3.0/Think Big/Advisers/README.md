---
language: en
status: active
role_owner: PMO
area: PMO
entity: Holistika Research SL
last_review: 2026-05-11
---

# Think Big — Advisers (inbound engagements; Holistika is the customer)

This is the canonical home for **inbound** engagement documentation where Holistika contracts external advisers and acts as their customer. Engagement-type 4 in [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §3. Outbound engagements where Holistika provides (types 1 / 2 / 3 / 5) live under [`../Clients/`](../Clients/) instead.

Each adviser engagement gets its own folder under this directory, named with an ISO-prefixed slug that encodes the start year and a short identifier.

## Naming convention

```
<YYYY>-<short-slug>/
```

Examples:

- `2026-holistika-incorporation/` — founder incorporation engagement (legal counsel, banking-desk, fiscal-track, ENISA-track advisers); unified entry point pointing into existing canonicals at `Admin/O5-1/People/Legal/`
- (future) `2026-trademark-counsel/` — trademark-track legal counsel engagement (post-incorporation)
- (future) `2027-tax-advisory/` — annual tax-advisory engagement

The slug is **lowercased**, **hyphen-separated**, and **redaction-safe** (no surnames, no adviser firm real names, no internal codenames).

## Per-engagement shape (inbound minimum-viable)

Each engagement folder follows the inbound template under [`_engagement-template/`](_engagement-template/):

| Folder | Purpose | Audience |
|:---|:---|:---|
| `00-internal/` | Operator-only notes; GOI/POI cross-link tables; mandate-phase tracker | operator + agent only |
| `01-our-pack/` | Material WE send to advisers: scope of mandate, KYC pack, context brief, our open questions | named adviser counterparty |
| `02-adviser-pack/` | Material WE receive: legal opinions, ENISA evidence, banking confirmations, fiscal-readiness statements | operator + agent (internal review) |
| `_archive/` | Dated rollback snapshots | rollback only |
| `_exports/` | Rendered branded PDFs (tracked) + render-manifest.json | distribution to advisers + Drive readers |

**No `_external_marks/`** under the inbound root — we are the customer; advisers brand themselves; there is no host/guest co-branding posture to manage.

## What an inbound engagement folder IS and IS NOT

- **IS** a unified entry point that cross-links to the canonical material under `Admin/O5-1/People/Legal/`, `Admin/O5-1/People/Compliance/`, `Admin/O5-1/Operations/PMO/`, and the `ADVISER_*` CSV registers.
- **IS NOT** a content store. Substantive interpretation lives in role-owner canonicals. Adviser deliverables (`02-adviser-pack/`) hold the source artifact + cross-link; the analysis lives in `EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`, `FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md`, and similar role-owner SOPs.

## Cross-references

- [`../README.md`](../README.md) — Think Big vault purpose and two-root model
- [`../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) — engagement-types matrix; per-root folder shape; inbound vs outbound doctrine
- [`../../Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) — ADVOPS operator runbook for engaging external advisers
- [`../../Admin/O5-1/Operations/PMO/EXTERNAL_ADVISER_ROUTER.md`](../../Admin/O5-1/Operations/PMO/EXTERNAL_ADVISER_ROUTER.md) — disciplines / triage map
- [`../../Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`](../../Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md) — handoff doc for external counsel
- [`../../Admin/O5-1/People/Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md`](../../Admin/O5-1/People/Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md) — incorporation-program knowledge index
- [`_engagement-template/`](_engagement-template/) — literal copy-target for new inbound engagements (created in P13.3)
- ADVISER CSVs: [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv), [`ADVISER_OPEN_QUESTIONS.csv`](../../../compliance/ADVISER_OPEN_QUESTIONS.csv), [`FOUNDER_FILED_INSTRUMENTS.csv`](../../../compliance/FOUNDER_FILED_INSTRUMENTS.csv), [`GOI_POI_REGISTER.csv`](../../../compliance/dimensions/GOI_POI_REGISTER.csv) (filter `class IN (external_adviser, banking_channel, public_authority)`)

## Active inbound engagements

| Slug | Start | Status | Primary GOI | Discipline cluster | Linked program |
|:---|:---|:---|:---|:---|:---|
| [`2026-holistika-incorporation/`](2026-holistika-incorporation/) | 2026-04 | active | `GOI-ADV-ENTITY-2026`, `GOI-BNK-INC-2026` | legal_constitution + banking_kyc + fiscal_readiness + enisa_certification | `PRJ-HOL-FOUNDING-2026` |

End.
