# Founder Filed Instrument Register (derived view)

> **Program**: [`PRJ-HOL-FOUNDING-2026`](programs/PRJ-HOL-FOUNDING-2026/README.md). New program-scoped Legal casework lands under that subfolder; this derived view remains at the role-folder root for backwards compatibility (Initiative 22 P3, D-IH-1).


**Document owner**: Legal Counsel  
**Version**: 2.0  
**Date**: 2026-04-28  
**Status**: Final (derived view)

---

## Purpose

**Per-discipline human view** of legal / fiscal / IP / banking / certification / notary instruments filed or to be filed for the founder incorporation program (`PRJ-HOL-FOUNDING-2026`).

> **SSOT note** — This document is a **derived view**. The single source of truth for filed instruments is the canonical CSV `docs/references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv`, validated by `py scripts/validate_founder_filed_instruments.py` (also via `validate_hlk.py`). Operators **edit the CSV first**, then update this view (or regenerate it via `scripts/export_adviser_handoff.py` once available). Do **not** treat this MD as authoritative.

**Handoff entrypoint**: [EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md](EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md). Plane SOP: [SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md](../../Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md). Discipline lookup: `docs/references/hlk/compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv`. GOI/POI references: `docs/references/hlk/compliance/GOI_POI_REGISTER.csv`.

---

## Status legend

- `draft` — content drafted but not signed/filed
- `signed` — executed by the relevant parties (e.g. founder, notary, counterparty)
- `filed` — registered with the appropriate registry (mercantile, fiscal, IP, etc.)
- `superseded` — replaced by a later instrument; see `supersedes_instrument_id`

---

## Per-discipline sections

### Legal (`discipline_id = legal`)

Constitution-level instruments: escritura de constitución, statutes/bylaws, shareholder agreements, capital changes, board resolutions.

| `instrument_id` | `instrument_type` | `jurisdiction` | `status` | `effective_or_filing_date` | `storage_location` | `vault_link` | `primary_owner_role` | `counterparty_goi_ref_id` |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `INST-LEG-ESCRITURA-DRAFT-2026` | escritura de constitución | ES | `draft` | tbd | off-repo (operator Drive) | — | Legal Counsel | `GOI-ADV-ENTITY-2026` |

Notes: seed row. Replace `storage_location` and `effective_or_filing_date` once the draft is exchanged with the notary; promote `status` to `signed`/`filed` after execution.

### Fiscal (`discipline_id = fiscal`)

Tax filings, AEAT/Hacienda registrations, fiscal certifications.

_(no instruments yet — add rows to `FOUNDER_FILED_INSTRUMENTS.csv` with `discipline_id = fiscal` and prefix `INST-FIS-…`.)_

### IP (`discipline_id = ip`)

Trademark filings (EUIPO/OEPM), patents, copyright registrations, IP assignment agreements.

_(no instruments yet — add rows with `discipline_id = ip` and prefix `INST-IP-…`.)_

### Banking (`discipline_id = banking`)

Bank account opening packages, capital deposit certificates, signing power certificates, KYC packages.

_(no instruments yet — add rows with `discipline_id = banking` and prefix `INST-BNK-…`.)_

### Certification (`discipline_id = certification`)

ENISA pre-application packages, MEIC submissions, startup certification artefacts.

_(no instruments yet — add rows with `discipline_id = certification` and prefix `INST-CERT-…`.)_

### Notary (`discipline_id = notary`)

Notarial instruments not otherwise classified (powers of attorney, apostilles, certified copies).

_(no instruments yet — add rows with `discipline_id = notary` and prefix `INST-NOT-…`.)_

---

## Maintenance

- **Edit** `docs/references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv` (canonical SSOT).
- **Validate**: `py scripts/validate_founder_filed_instruments.py` (and `py scripts/validate_hlk.py`).
- **Mirror sync** (live since Initiative 22 P7, 2026-04-29): `py scripts/sync_compliance_mirrors_from_csv.py --founder-filed-instruments-only --output <out.sql>` against `compliance.founder_filed_instruments_mirror` (DDL: `supabase/migrations/20260429081800_i21_compliance_founder_filed_instruments_mirror.sql`; staging: `scripts/sql/i21_phase1_staging/20260428_i21_compliance_founder_filed_instruments_mirror_up.sql`). Apply DML via user-supabase MCP `execute_sql` with `service_role`.
- **Refresh this view** after CSV changes: edit the per-discipline tables here, or regenerate via `scripts/export_adviser_handoff.py` (Initiative 21 / P7).
- **Lifecycle hooks**: after any new `signed`/`filed` row, run post-filing review per [FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md](../Compliance/FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md) and refresh [FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md](FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md) if mercantil or entity facts changed.

## Related

- [FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md](FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md)
- [EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md](EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md)
- [FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md](FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md) (per-discipline open questions, derived view)
- [TOPIC_PMO_CLIENT_DELIVERY_HUB.md](../../Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) (WS-A legal constitution)
- [SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md](../../Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md)
- [EXTERNAL_ADVISER_ROUTER.md](../../Operations/PMO/EXTERNAL_ADVISER_ROUTER.md)
- [SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md](../Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md)
