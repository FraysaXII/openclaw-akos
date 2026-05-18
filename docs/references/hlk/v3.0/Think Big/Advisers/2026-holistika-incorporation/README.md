---
language: en
status: active
role_owner: PMO
area: PMO
entity: Holistika Research SL
last_review: 2026-05-18
engagement_slug: 2026-holistika-incorporation
engagement_name: "Founder incorporation + ENISA evidence + fiscal readiness (inbound legal/fiscal/banking advisers)"
linked_program_id: PRJ-HOL-FOUNDING-2026
linked_program_asset_bucket: docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/
discipline_cluster:
  - legal_constitution
  - banking_kyc
  - fiscal_readiness
  - enisa_certification
language_code: es
---

# 2026-holistika-incorporation — inbound engagement folder

> **Unified entry point only.** This folder is a unified inbound entry point per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §4. Canonical content for the founder-incorporation program lives in role-owner SOPs and CSV registers under `Admin/O5-1/People/Legal/`, `Admin/O5-1/People/Compliance/`, `Admin/O5-1/Operations/PMO/`, and the `ADVISER_*` CSV registers. This folder cross-links into those canonicals; it does NOT duplicate content.

## Scope

Inbound engagement covering the founder-incorporation program: four adviser disciplines — legal constitution (`thi_legal_dtp_302`), banking channel + KYC (`thi_legal_dtp_302` / `thi_legal_dtp_303`), fiscal readiness (`thi_finan_dtp_302`), and ENISA / startup-certification readiness (`hol_opera_dtp_310` / `hol_peopl_dtp_302`). Linked to `PRJ-HOL-FOUNDING-2026` in `TOPIC_PMO_CLIENT_DELIVERY_HUB.md`.

## Cross-references — where the canonical content lives

### Role-owner canonicals (authoritative narrative)

- [`EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`](../../../Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md) — handoff doc for external counsel; this is the canonical material we hand off
- [`FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md`](../../../Admin/O5-1/People/Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md) — incorporation-program knowledge index (legal-side narrative SSOT)
- [`ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`](../../../Admin/O5-1/People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md) — ENISA evidence pack (compliance-side narrative SSOT)
- [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../../Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) — ADVOPS operator runbook (PMO-owned)
- [`EXTERNAL_ADVISER_ROUTER.md`](../../../Admin/O5-1/Operations/PMO/EXTERNAL_ADVISER_ROUTER.md) — disciplines / triage map

### Tightened mirror canonicals (machine-readable companions)

- [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../../compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv) — disciplines registry (FK for opinions, open questions, filed instruments)
- [`ADVISER_OPEN_QUESTIONS.csv`](../../../../compliance/ADVISER_OPEN_QUESTIONS.csv) — adviser-facing open questions
- [`FOUNDER_FILED_INSTRUMENTS.csv`](../../../../compliance/FOUNDER_FILED_INSTRUMENTS.csv) — legal / fiscal / IP / banking / certification / notary instruments
- [`GOI_POI_REGISTER.csv`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv) — counterparty rows for this engagement (filter `program_id = PRJ-HOL-FOUNDING-2026`)

### Counterparty rows for this engagement

| ref_id | class | discipline-cluster role | Notes |
|:---|:---|:---|:---|
| [`GOI-ADV-ENTITY-2026`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv) | `external_adviser` | adviser firm (ENISA + fiscal tracks) | `lens=entity_readiness` |
| [`GOI-BNK-INC-2026`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv) | `banking_channel` | constitution-desk bank | `lens=incorporation` |
| [`POI-LEG-ENISA-LEAD-2026`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv) | `external_adviser` | ENISA-track adviser lead at GOI-ADV-ENTITY-2026 | |
| [`POI-LEG-FISCAL-LEAD-2026`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv) | `external_adviser` | Fiscal-track adviser at GOI-ADV-ENTITY-2026 | |
| [`POI-ADV-INTAKE-LEAD-2026`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv) | `external_adviser` | Intake contact at GOI-ADV-ENTITY-2026 | |
| [`POI-BNK-DESK-LEAD-2026`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv) | `banking_channel` | Constitution-desk lead at GOI-BNK-INC-2026 | |

## Folder shape (skeleton)

| Folder | State | Purpose |
|:---|:---|:---|
| `00-internal/` | placeholder | Operator notes; mandate-phase tracker; GOI/POI cross-link table (drafted in this README for now) |
| `01-our-pack/` | **populated (2026-05-18)** | Outbound material to advisers: scope-of-mandate, KYC pack, legal-constitutor handoff. Currently holds: [`legal-constitutor-handoff-2026-05-18.md`](01-our-pack/legal-constitutor-handoff-2026-05-18.md). |
| `02-adviser-pack/` | placeholder | Will hold received legal opinions, ENISA evidence statements, banking confirmations, fiscal-readiness statements |
| `_archive/` | placeholder | Dated rollback snapshots |
| `_exports/` | placeholder | Branded PDFs once any our-pack material renders |

This folder will populate progressively as the inbound engagement produces and receives material. The canonical content stays at the role-owner SOPs cross-linked above.

## Cross-references — Think Big context

- [`../README.md`](../README.md) — Advisers root: inbound naming conventions and active engagements
- [`../../README.md`](../../README.md) — Think Big two-root model (Clients + Advisers)
- [`../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) — engagement-types matrix
- [`../_engagement-template/`](../_engagement-template/) — canonical inbound template this folder was populated from
- [`../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](../../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) — `PRJ-HOL-FOUNDING-2026` portfolio row cross-links here

## Cross-references — program asset bucket (rendered external collateral)

- [`../../../_assets/advops/2026-holistika-incorporation/README.md`](../../../_assets/advops/2026-holistika-incorporation/README.md) — **program asset bucket** (rendered external collateral: ENISA evidence dossier, company-dossier deck, adviser-handoff topic visual). The asset bucket sits under `_assets/advops/` keyed by `program_id`; this engagement folder sits under `Think Big/Advisers/` keyed by `engagement_slug`. The two coexist intentionally — see the asset-bucket README for the two-slug rationale.
- [`../../../_assets/advops/2026-holistika-incorporation/enisa_evidence/dossier_es.md`](../../../_assets/advops/2026-holistika-incorporation/enisa_evidence/dossier_es.md) — ENISA-reviewer-facing evidence appendix (Spanish).
- [`../../../_assets/advops/2026-holistika-incorporation/enisa_company_dossier/deck_slides.yaml`](../../../_assets/advops/2026-holistika-incorporation/enisa_company_dossier/deck_slides.yaml) — Visual deck companion for the ENISA evidence appendix.

End of unified entry point.
