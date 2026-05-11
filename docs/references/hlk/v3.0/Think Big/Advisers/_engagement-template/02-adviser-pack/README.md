---
language: en
role_owner: PMO
purpose: material we receive from the adviser
audience: operator + agent (internal review and cross-link)
---

# `02-adviser-pack/` — material we receive from the adviser

This sub-folder holds material that **Holistika receives** from the adviser counterparty: legal opinions, ENISA evidence statements, banking confirmations, fiscal-readiness opinions, filed-instrument receipts.

This is the inbound counterpart to the outbound `02-customer-pack/` — material the counterparty produces, in the inbound direction "their pack" means "what they send to us".

## Audience

Operator + agent (internal review). Cross-link to role-owner canonicals (Legal Counsel, Business Controller, Compliance) for the substantive interpretation.

## Typical contents

- `legal-opinion-<topic>.<lang>.<YYYY-MM-DD>.md` — written legal opinion received from counsel; cross-link to `FOUNDER_FILED_INSTRUMENTS.csv` for filing references
- `enisa-evidence-statement.<lang>.<YYYY-MM-DD>.md` — adviser-issued ENISA-track evidence statements; cross-link to [`ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`](../../../Admin/O5-1/People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md)
- `banking-confirmation-<topic>.<lang>.<YYYY-MM-DD>.md` — desk-side confirmations, IBAN issuance, KYC clearance
- `fiscal-readiness-statement.<lang>.<YYYY-MM-DD>.md` — fiscal-track adviser statements; cross-link to `FOUNDER_FILED_INSTRUMENTS.csv` and the relevant `thi_finan_dtp_*` process rows
- `meeting-summary-<YYYY-MM-DD>-<topic>.md` — adviser-side meeting summary or call notes (with redaction per `SOP-HLK_TRANSCRIPT_REDACTION_001.md` if recordings exist)

## Conventions

- Date-suffix is recommended (`.<YYYY-MM-DD>.md`) — adviser deliverables are dated artifacts; chronological ordering matters for audit trail.
- Language suffix is mandatory (`.es.md`, `.en.md`, `.fr.md`).
- Cross-link to the relevant `POI-LEG-*` / `POI-BNK-*` / `POI-ADV-*` row in [`GOI_POI_REGISTER.csv`](../../../../compliance/dimensions/GOI_POI_REGISTER.csv) — name the adviser only via their ref_id.
- Substantive interpretation lives in role-owner canonicals under `Admin/O5-1/People/Legal/`, `Admin/O5-1/People/Compliance/`, etc.; this folder holds the source artifact + cross-links, not the operator's analysis.

## Cross-references

- Engagement template root: [`../README.md`](../README.md)
- Our pack (outbound material we send): [`../01-our-pack/README.md`](../01-our-pack/README.md)
- ENISA evidence pack canonical: [`../../../Admin/O5-1/People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`](../../../Admin/O5-1/People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md)
- Founder incorporation knowledge index: [`../../../Admin/O5-1/People/Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md`](../../../Admin/O5-1/People/Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md)
- Transcript redaction SOP: [`../../../Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../../Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md)
