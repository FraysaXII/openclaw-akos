# External Counsel Handoff Package

**Document owner**: Legal Counsel
**Version**: 2.0
**Date**: 2026-04-28
**Status**: Final

---

## Purpose

Single entrypoint for **external advisers** working on founder incorporation across all engagement disciplines (Legal & Corporate, Fiscal & Tax, IP & Trademark, Banking, Startup Certification, Notary). This file is **guidance and packaging only**; it does not replace filed instruments or professional legal advice.

**Program context**: PMO portfolio row `PRJ-HOL-FOUNDING-2026` — [TOPIC_PMO_CLIENT_DELIVERY_HUB.md](../../Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md).

**Plane**: External Adviser Engagement (`hol_opera_ws_5`); see [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001`](../../Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) and the [`EXTERNAL_ADVISER_ROUTER`](../../Operations/PMO/EXTERNAL_ADVISER_ROUTER.md) for plane and routing context.

**Stakeholder convention**: Real organisations and persons appear as `GOI-*` / `POI-*` `ref_id`s from [`GOI_POI_REGISTER.csv`](../../../../../compliance/GOI_POI_REGISTER.csv); identity mapping is off-repo per [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001`](../Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md).

---

## Read order

1. This document (binding ladder, sharing legend, exhibit index).
2. [FOUNDER_FILED_INSTRUMENT_REGISTER.md](FOUNDER_FILED_INSTRUMENT_REGISTER.md) — what is draft, signed, or filed, and where originals live.
3. [FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md](FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md) — short fact pattern and related-entity map (with pointers to case memos).
4. [FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md](FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md) — current question queue for counsel.
5. [FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md](FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md) — entity formation case position.
6. [RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md](../../Research/RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md) — research vs Tech Lab layering.
7. [FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md](../../Finance/Business%20Controller/Taxes/FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md) — founder-to-company funding posture.
8. [BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md](BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) — naming and trademark scope.
9. [ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md](../Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md) — certification / evidence context, as needed.
10. Working synthesis (non-canonical): [founder-incorporation-report.md](../../../../../../../wip/planning/04-holistika-company-formation/reports/founder-incorporation-report.md) — read **last** for narrative and validation history only.

Full bundle index: [FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md](FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md).

---

## Binding vs narrative (precedence ladder)

Higher layers override lower layers if there is a conflict. Updates that resolve a conflict must be **dated** and applied at the **highest affected layer** first (filed facts before internal narrative).

| Priority | Layer | Typical examples |
|:--------:|:------|:-----------------|
| 1 | **Filed / executed instruments** | Escritura, registered corporate purpose, bylaws, signed shareholder agreements, IP assignments as executed |
| 2 | **Registral or official extracts** | Mercantile registry excerpts, tax or fiscal registrations where they record legal fact |
| 3 | **Canonical vault case memos** | Role-owned markdown under `docs/references/hlk/v3.0/` (e.g. entity formation memo, capitalization note) |
| 4 | **Working synthesis** | `docs/wip/` planning and reports — interpretive only until promoted |

**Rule**: Do not treat SOPs or internal procedures as statements of law or as substitutes for filed text. They describe **how Holistika operates**, not what a registry entry says.

---

## Supersedence

- One **authoritative** narrative per topic in the case layer; other documents **link** to it rather than restating it.
- If counsel agrees a change to filed instruments, Legal updates [FOUNDER_FILED_INSTRUMENT_REGISTER.md](FOUNDER_FILED_INSTRUMENT_REGISTER.md) and reconciles affected case memos and [FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md](FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md) in the same change cycle where possible.

---

## Sharing legend (exports and attachments)

Use these labels on bundles sent outside the organisation. Align with GOI/POI sensitivity discipline in the PMO hub.

| Label | Meaning |
|:------|:--------|
| `counsel_ok` | Safe to share with external legal counsel under engagement terms |
| `internal_only` | Not for external distribution without redaction and Legal sign-off |
| `counsel_and_named_counterparty` | Share only with counsel and an explicitly named third party (bank, notary, authority) per instruction |

---

## Exhibit index (pointers only)

| Exhibit ref | Document |
|:------------|:---------|
| E1 | [FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md](FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md) |
| E2 | [RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md](../../Research/RESEARCH_VS_TECH_LAB_ENTITY_RATIONALE_2026-04.md) |
| E3 | [FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md](../../Finance/Business%20Controller/Taxes/FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md) |
| E4 | [BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md](BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) |
| E5 | [ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md](../Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md) |
| E6 | [FOUNDER_FILED_INSTRUMENT_REGISTER.md](FOUNDER_FILED_INSTRUMENT_REGISTER.md) |

Add rows only for **vault-resident** pointers; cap tables, signed PDFs, and deal-room files stay in their storage location with a row in the filed instrument register.

---

## Per-discipline sections

Each section is a **derived view** filtered from canonical CSVs. Source of truth lives in [`ADVISER_OPEN_QUESTIONS.csv`](../../../../../compliance/ADVISER_OPEN_QUESTIONS.csv) and [`FOUNDER_FILED_INSTRUMENTS.csv`](../../../../../compliance/FOUNDER_FILED_INSTRUMENTS.csv) (Initiative 21 / P4 / P5).

### Legal & Corporate (`legal`)

- **Canonical owner role**: Legal Counsel.
- **Entrypoint process**: [`thi_legal_dtp_302`](../../../../../compliance/process_list.csv) (Founder Entity Formation Readiness).
- **Open questions (live):** see Legal & Corporate section in [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md).
- **Filed instruments (Legal):** rows with `discipline_id = legal` in [`FOUNDER_FILED_INSTRUMENT_REGISTER.md`](FOUNDER_FILED_INSTRUMENT_REGISTER.md).
- **Sharing default:** `counsel_ok`.

### Fiscal & Tax (`fiscal`)

- **Canonical owner role**: Business Controller (Finance / Taxes chain).
- **Entrypoint process**: [`thi_finan_dtp_302`](../../../../../compliance/process_list.csv) (Founder company funding / fiscal readiness).
- **Open questions (live):** Fiscal & Tax section in [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md).
- **Cross-link memo:** [`FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md`](../../Finance/Business%20Controller/Taxes/FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04.md).
- **Sharing default:** `counsel_ok`.

### IP & Trademark (`ip`)

- **Canonical owner role**: Legal Counsel.
- **Entrypoint process**: [`thi_legal_dtp_303`](../../../../../compliance/process_list.csv) (Trademark and Naming Governance).
- **Open questions (live):** IP & Trademark section in [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md).
- **Cross-link memo:** [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md).
- **Sharing default:** `counsel_ok`.

### Banking (`banking`)

- **Canonical owner role**: Legal Counsel (constitution-desk relationship).
- **Entrypoint process**: [`thi_legal_dtp_302`](../../../../../compliance/process_list.csv).
- **Counterparty references**: `GOI-BNK-INC-2026`, `POI-BNK-DESK-LEAD-2026`.
- **Open questions (live):** Banking section in [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md).
- **Sharing default:** `counsel_and_named_counterparty`.

### Startup Certification (`certification`)

- **Canonical owner role**: Compliance.
- **Entrypoint process**: [`hol_peopl_dtp_302`](../../../../../compliance/process_list.csv) (ENISA Readiness and Evidence Pack).
- **Counterparty references**: `GOI-ADV-ENTITY-2026`, `POI-LEG-ENISA-LEAD-2026`.
- **Open questions (live):** Startup Certification section in [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md).
- **Cross-link evidence pack:** [`ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`](../Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md).
- **Sharing default:** `counsel_ok`.

### Notary (`notary`)

- **Canonical owner role**: Legal Counsel.
- **Entrypoint process**: [`thi_legal_dtp_302`](../../../../../compliance/process_list.csv).
- **Open questions (live):** Notary section in [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md). _(no rows today; new ones use `Q-NOT-NNN`)_
- **Sharing default:** `counsel_and_named_counterparty` for booking logistics; `counsel_ok` for the executed deed once filed.

---

## Adding a new discipline

Plane-level guarantee from the [ADVOPS plane SOP](../../Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md): adding a new discipline (e.g. accounting, employment, regulatory affairs) is **a row in [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../../../compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv)** plus a new section above; **no schema migrations**.
