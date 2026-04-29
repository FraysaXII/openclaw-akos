# Founder Fact Pattern and Related Entities

> **Program**: [`PRJ-HOL-FOUNDING-2026`](programs/PRJ-HOL-FOUNDING-2026/README.md). New program-scoped Legal casework lands under that subfolder; this document remains at the role-folder root for backwards compatibility (Initiative 22 P3, D-IH-1).

**Document owner**: Legal Counsel  
**Version**: 2.0  
**Date**: 2026-04-28  
**Status**: Final

---

## Purpose

**Short scaffold** of the commercial and entity fact pattern for external advisers across all disciplines (Legal / Fiscal / IP / Banking / Certification / Notary). Detailed positions live in linked case memos; update this page when those memos change or when **filed** facts change (see [FOUNDER_FILED_INSTRUMENT_REGISTER.md](FOUNDER_FILED_INSTRUMENT_REGISTER.md), derived from `docs/references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv`).

> **Naming posture (Initiative 21 / D-CH-2)** — Canonical text in this document references **only** GOI/POI ref_ids from `docs/references/hlk/compliance/GOI_POI_REGISTER.csv`. Real names of private entities and individuals are kept off-repo per [SOP-HLK_TRANSCRIPT_REDACTION_001.md](../Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md) and [SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md](../Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md). Public authorities (e.g. ENISA, AEAT, OEPM, mercantile registries) may be named directly because they are public entities.

**Handoff entrypoint**: [EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md](EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md) (per-discipline). Plane SOP: [SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md](../../Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md). Router: [EXTERNAL_ADVISER_ROUTER.md](../../Operations/PMO/EXTERNAL_ADVISER_ROUTER.md).

---

## Fact pattern (fill / refresh from case layer)

- **Program**: `PRJ-HOL-FOUNDING-2026` — founder incorporation of Holistika.
- **Commercial purpose (high level)**: Corporate intelligence, research-led business engineering, technology-enabled delivery, with a credible innovation and scale path (detail: [FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md](FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md)).
- **Operating story**: Founder-led, service- and research-heavy today; productization and lab-style scale as a future option rather than day-one legal split (same memo).
- **Intended activity clusters**: Research, architecture analysis, AI-enabled interpretation and delivery, future productization — aligned to registry wording once filed (memo + filed register).
- **External adviser context**: Engagement managed via the **External Adviser Engagement (ADVOPS)** plane against `GOI-ADV-ENTITY-2026` (third-party startup-certification adviser firm). Discipline leads:
  - **Legal / ENISA-track**: `POI-LEG-ENISA-LEAD-2026` (lens: `entity_readiness`).
  - **Fiscal**: `POI-LEG-FISCAL-LEAD-2026` (lens: `fiscal_readiness`).
  - **Initial intake**: `POI-ADV-INTAKE-LEAD-2026` (lens: `entity_readiness`).
- **Banking / KYC narrative**: Bank channel anchored on `GOI-BNK-INC-2026` (constitution-desk bank), with `POI-BNK-DESK-LEAD-2026` as the named desk lead. Narrative *TBD in consultation with Legal and the banking channel* — must stay consistent with mercantil registry and CNAE / IAE posture (PMO WS-B). See `Q-BNK-001` in `docs/references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv`.

---

## Related entities

Holistika treats **Research** and **Tech Lab** as conceptual layers that may share a **single legal entity** initially; separation is deferred until commercial, legal, cap-table, or operational signals justify it. Full rationale: [RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md](../../Research/RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md).

External counterparties referenced by ref_id (resolve via `GOI_POI_REGISTER.csv`):

- `GOI-ADV-ENTITY-2026` — third-party startup-certification adviser firm (private, sensitivity `internal`).
- `GOI-BNK-INC-2026` — constitution-desk bank (private, sensitivity `confidential`).
- `POI-LEG-ENISA-LEAD-2026`, `POI-LEG-FISCAL-LEAD-2026`, `POI-ADV-INTAKE-LEAD-2026` — adviser-firm contacts.
- `POI-BNK-DESK-LEAD-2026` — banking desk lead.

---

## Cross-workstream consistency (WS-A through WS-D)

Program workstreams for `PRJ-HOL-FOUNDING-2026` are defined in [TOPIC_PMO_CLIENT_DELIVERY_HUB.md](../../Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md):

| Stream | Scope | Primary discipline / GOI / POI | Consistency note |
|:-------|:------|:--------------------------------|:-----------------|
| WS-A | Legal constitution (*objeto social*, deed path) | Legal · `GOI-ADV-ENTITY-2026` · `POI-LEG-ENISA-LEAD-2026` | Drives mercantil **facts**; other streams must not contradict filed text. |
| WS-B | Banking channel; CNAE / IAE alignment | Banking · `GOI-BNK-INC-2026` · `POI-BNK-DESK-LEAD-2026` | One coherent story across registry, banking, and later startup narrative. |
| WS-C | External startup plan and certification path | Certification · `GOI-ADV-ENTITY-2026` · `POI-LEG-ENISA-LEAD-2026` | Certification body has final say; Legal checks alignment with WS-A. |
| WS-D | Founder-to-company funding evidence | Fiscal · `POI-LEG-FISCAL-LEAD-2026` | Must not contradict WS-A/C in filings or packs ([SOP-FOUNDER_COMPANY_FUNDING_001.md](../../Finance/Business%20Controller/Taxes/SOP-FOUNDER_COMPANY_FUNDING_001.md)). |

---

## Related

- [FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md](FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md)
- [FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md](FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md) (derived per-discipline view; SSOT: `ADVISER_OPEN_QUESTIONS.csv`)
- [FOUNDER_FILED_INSTRUMENT_REGISTER.md](FOUNDER_FILED_INSTRUMENT_REGISTER.md) (derived per-discipline view; SSOT: `FOUNDER_FILED_INSTRUMENTS.csv`)
- [EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md](EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md)
- [EXTERNAL_ADVISER_ROUTER.md](../../Operations/PMO/EXTERNAL_ADVISER_ROUTER.md)
- [SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md](../../Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md)
- [SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md](../Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md)
- [SOP-HLK_TRANSCRIPT_REDACTION_001.md](../Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md)
- KM Topic manifest: [`docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/adviser_handoff/topic_external_adviser_handoff.manifest.md`](../../../_assets/advops/PRJ-HOL-FOUNDING-2026/adviser_handoff/topic_external_adviser_handoff.manifest.md)
