# PMO client delivery hub — topic knowledge index (pilot)

**Document owner**: PMO  
**Version**: 0.2  
**Date**: 2026-04-15  
**Status**: Draft  
**topic_id**: `topic_pmo_client_delivery_hub`

---

## Purpose

Canonical entrypoint for **cross-entity client delivery** and the **PMO project portfolio (SSOT)**: links **Think Big** (non-repo artifacts), **Envoy Tech Lab** (GitHub repos), PMO registries, and **active programs** (metadata and pointers only—no duplicate long-form case narratives here).

One primary owner (**PMO**); **O5-1 (Chief Business Officer)** is the executive accountable line for cross-entity founder-scale programs; other roles link here instead of duplicating engagement maps.

---

## PMO project portfolio (SSOT)

**Rules**

- One **table row per program** (initiative with external parties, deadlines, and cross-role dependencies).
- Columns hold **metadata and links** only. Legal, Compliance, and Finance keep **authoritative narrative** in their role-owned case docs.
- **O5-1** is the accountable executive for Holistika-wide founder-class programs; **PMO** remains responsible for cadence, RAID-style visibility, and registry hygiene.
- Do **not** record personal names of external counterparties here. Use **GOI/POI-style references** (below) or role titles (e.g. “bank incorporation desk”, “external certification adviser firm”).

| project_id | name | accountable | pmo_responsible | status | primary_case_doc | process_list anchors | external_sources (operators) |
|:-----------|:-----|:------------|:----------------|:-------|:-----------------|:----------------------|:-----------------------------|
| PRJ-HOL-FOUNDING-2026 | Founder incorporation and startup certification readiness | O5-1 | PMO | Active | [FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md](../../People/Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md) | `thi_legal_dtp_302`, `thi_legal_dtp_303`, `thi_finan_dtp_302`, `hol_peopl_dtp_302`, `hol_opera_dtp_310` | [External transcripts](../../../../../../../wip/planning/04-holistika-company-formation/external/) (UTF-8 `.md` exports; non-canonical) |

**Program workstreams (single portfolio row; split only for mental model)**

| ws_id | scope | accountable domain | Notes |
|:------|:------|:-------------------|:------|
| WS-A | Legal constitution (`object social`, deed path) | Legal Counsel | Drives mercantil facts. External counsel read order: [EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md](../../People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md). |
| WS-B | Banking channel and CNAE / IAE alignment | Legal Counsel (+ Finance for KYC posture as needed) | Keep **one** coherent activity story across mercantil registry, banking channel, and later startup narrative. |
| WS-C | External adviser — startup business plan and certification path | Compliance (+ Legal for consistency with WS-A) | Certification body has final say; plan is collaborative and long-cycle. |
| WS-D | Founder-to-company funding evidence | Business Controller / Taxes | Must not contradict WS-A/C in filings or packs. |

---

## Stakeholder index (GOI / POI pattern)

Inspired by the **Groups of Interest / Persons of Interest** pattern (filters: type, entity, access band, lens)—implemented here as a **portable markdown register** until a runtime tool is wired.

**Conventions**

- **ref_id**: stable handle (`GOI-*` for organisations/groups, `POI-*` for individual roles **as positions**, not given names).
- **class**: `external_adviser` | `banking_channel` | `supplier` | `research_benchmark` | `lead` | `client_org` | `collaborator` | `other`.
- **lens**: why the row exists (`entity_readiness`, `marketing_benchmark`, `delivery`, etc.).
- **sensitivity**: `internal` | `confidential` | `restricted` (drives where detailed notes may live).
- **primary_link**: vault case doc, wip synthesis, or empty if only external file paths are kept off-repo.

| ref_id | class | lens | sensitivity | primary_link | notes |
|:-------|:------|:-----|:--------------|:-------------|:------|
| GOI-ADV-ENTITY-2026 | external_adviser | entity_readiness | internal | [ENISA evidence pack — external party model](../../People/Compliance/ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md#external-party-operating-model-startup-certification-path) | Third-party firm assisting with startup business plan and certification filing preparation. |
| GOI-BNK-INC-2026 | banking_channel | incorporation | confidential | — | Institution handling incorporation desk / CNAE selection support; operational detail off-vault. |

Add rows sparingly; prefer **one row per external organisation**, not per email thread.

---

## Canonical registry hygiene (applied)

- **`baseline_organisation.csv`**: `role_name` for Chief Business Officer is **`O5-1`** (letter O).
- **`process_list.csv`**: process **`hol_opera_dtp_310`** — *PMO project portfolio SSOT* — child of **Program Management** (`hol_opera_dtp_148`), owner **PMO**.
- **`scripts/merge_gtm_into_process_list.py`**: org parent resolution uses **`O5-1`** (removed legacy `05-1` token).

---

## Bundle structure

### Source synthesis

- Working synthesis: `docs/wip/planning/04-holistika-company-formation/reports/founder-incorporation-report.md`
- External call exports (UTF-8 `.md` only): [external/README.md](../../../../../../../wip/planning/04-holistika-company-formation/external/README.md)

### Procedural layer

- PMO processes: lookup `role_owner` = PMO in [process_list.csv](../../../../../compliance/process_list.csv) for repeatable delivery patterns.
- [SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md](SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md)
- [SOP-PMO_VAULT_PROMOTION_GATE_001.md](SOP-PMO_VAULT_PROMOTION_GATE_001.md)

### Case layer

- Placeholder: add Think Big `Clients/` or `Projects/` paths when engagements are active.

### Linked Git repositories

- Canonical registry: [REPOSITORIES_REGISTRY.md](../../../../Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) — see row `client-delivery-pilot` (replace GitHub URL placeholders when live).
- Optional stubs: [client-delivery/README.md](../../../../Envoy%20Tech%20Lab/Repositories/client-delivery/README.md)

### Think Big (non-repo artifacts)

- [Think Big/README.md](../../../../Think%20Big/README.md)
- `Think Big/Clients/` — client-scoped vault files  
- `Think Big/Projects/` — project documentation not stored as a repo root

### External backlog index (non-SSOT)

- [RESEARCH_BACKLOG_TRELLO_REGISTRY.md](RESEARCH_BACKLOG_TRELLO_REGISTRY.md)

### Registered process anchors

- Add `item_id` anchors when delivery behavior is registered as repeatable processes.

### Facts (optional)

- Short bullet facts with `source_id` citations pointing at meeting notes, registry rows, or GitHub URLs per [HLK_KM_TOPIC_FACT_SOURCE.md](../../../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md).

---

## How to use

1. Register every tracked client-delivery repo in `REPOSITORIES_REGISTRY.md` (`class` = `client-delivery`).  
2. Keep commercials and non-repo deliverables under `Think Big/`.  
3. Maintain **one row per active program** in the portfolio table above; link to a single primary case doc per program.  
4. Promote stable, repeatable delivery steps toward SOPs and `process_list.csv` only when SOP-META criteria are met.  
5. Use Obsidian tags per KM contract, e.g. `topic/topic_pmo_client_delivery_hub`, `dim/entity/think_big`, `dim/entity/envoy_tech_lab`.

---

## Maintenance

Update this index when registry rows, Think Big paths, portfolio status, or major engagement scope changes.
