# Founder Filed Instrument Register

**Document owner**: Legal Counsel  
**Version**: 1.0  
**Date**: 2026-04-23  
**Status**: Final

---

## Purpose

**Single table** tracking legal instruments and registral artifacts for the founder incorporation program (`PRJ-HOL-FOUNDING-2026`). Keeps vault narrative aligned with **what is actually filed or signed**.

**Handoff entrypoint**: [EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md](EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md).

---

## Register

| instrument_type | jurisdiction | status | effective_or_filing_date | storage_location | vault_link | primary_owner_role |
|:----------------|:-------------|:-------|:-------------------------|:-----------------|:-----------|:-------------------|
| *example: escritura de constitución* | *e.g. Spain* | `draft` / `signed` / `filed` | YYYY-MM-DD or TBD | *Drive path, deal room, or off-repo* | — or MD path | Legal Counsel |

**Instructions**

- **Legal** maintains this table when corporate purpose, bylaws, capital, shareholder arrangements, or other constitution-level facts change at the **filed or signed** layer.
- Replace template rows with real entries; remove the example row when the first real instrument is recorded.
- `storage_location` may be `off-repo` when the canonical file is not in git; still record where operators retrieve the original.
- After any update here, run **post-filing review** per [FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md](../Compliance/FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md) and refresh [FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md](FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md) if mercantil or entity facts changed.

---

## Related

- [FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md](FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md)
- [TOPIC_PMO_CLIENT_DELIVERY_HUB.md](../../Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) (WS-A legal constitution)
