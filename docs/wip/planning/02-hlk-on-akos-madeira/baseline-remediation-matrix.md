# Baseline Remediation Matrix

**Source plan**: `C:\Users\Shadow\.cursor\plans\hlk_madeira_proposal_3a66dc35.plan.md`
**Initiative**: `hlk-on-akos-madeira`
**Status**: Historical Phase 1 inventory; retained as a next-tranche queue and gap ledger
**Purpose**: This matrix started as the pre-implementation Phase 1 remediation inventory. Phase 1 is now reported as **GO** in `reports/phase-1-report.md`. This document is retained to: (1) preserve the original file-by-file gap framing, (2) show what was already resolved historically, and (3) provide a practical queue for the next baseline/compliance tranche where deferred items and deeper KiRBe sync work will continue.

---

## Current Interpretation

- **Phase 1 completion source**: `reports/phase-1-report.md` is the authoritative execution record for what was completed.
- **This matrix is not the current release backlog**: its original `OPEN/DONE` counts are superseded by the completion report and later follow-on programs.
- **Use this document now as**:
  - a historical inventory of the Phase 1 gap model
  - a queue for deferred structural work such as stable keys, process ownership/component wiring, and KiRBe sync automation

## Historical Resolution Snapshot

- **Resolved in Phase 1 / follow-on baseline work**: precedence contract, compliance taxonomy freeze, canonical baseline organisation, canonical process list, access review, granularity normalization, TBD row resolution, role description enrichment, vault v3.0 formalization, and multiple role-gap closures.
- **Still relevant for the next tranche**: `P1M-003`, `P1M-008`, `P1M-009`, `P1M-012`, `P1M-014`, `P1M-015`, plus any remaining population of `responsible_processes` / `components_used` and formal sync automation design.

## Scope

This matrix covers the main Phase 1 baseline artifacts:

- baseline organisation mirrors
- process list mirrors
- compliance taxonomy references
- SOP metadata contract
- KiRBe and SQL reference artifacts
- vault-to-KiRBe sync readiness

## Matrix

| ID | File | Field Category | Current Issue | Target State | Priority | Depends On | Notes |
|----|------|----------------|---------------|--------------|----------|------------|-------|
| P1M-001 | `docs/references/hlk/compliance/SOP-META_PROCESS_MGMT_001.md` | Source-of-truth precedence | No explicit rule for canonical vs mirrored vs reference-only assets | Add explicit precedence contract for markdown, CSV, KiRBe, SQL dumps, and Drive | P0 | None | Blocks safe data entry |
| P1M-002 | `docs/references/hlk/Research & Logic/.../supabase (9).ts` | Compliance taxonomy | Compliance taxonomy exists in schema but is not yet frozen as the operational canon | Freeze access, confidence, source category, and source level semantics | P0 | P1M-001 | Treat typed schema as reference contract, not authoring surface |
| P1M-003 | `C:\Users\Shadow\full_dump.sql` | Rules policy | `public.rules` exists but is empty | Define where policy rules are authored and how they are mirrored into DB | P1 | P1M-001, P1M-002 | High governance risk |
| P1M-004 | `docs/references/hlk/Research & Logic/.../baseline_organisation_rows (4).csv` | Role descriptions | CSV mirror does not represent `role_full_description` and many descriptions remain shallow | Define authoring path and fill missing role descriptions with source-backed content | P0 | P1M-001, P1M-002 | Data-entry ASAP candidate |
| P1M-005 | `C:\Users\Shadow\full_dump.sql` | Placeholder descriptions | SQL snapshot shows 41 placeholder `role_full_description` values | Replace placeholders through curated enrichment batches | P0 | P1M-004 | Use `Research & Logic` to source semantics |
| P1M-006 | `docs/references/hlk/Research & Logic/.../baseline_organisation_rows (4).csv` | Access level semantics | Multiple governance-sensitive roles currently sit at access level `0` | Review and justify or change access semantics for sensitive roles | P0 | P1M-002 | Includes `Compliance`, `AIC`, `Susana Madeira`, `O5`, `CDO`, `CTO`, others |
| P1M-007 | `docs/references/hlk/compliance/baseline_organisation_rows.txt` | Export consistency | TXT mirror is structurally different from CSV and richer DB shape | Decide whether TXT remains reference-only or becomes a normalized export target | P2 | P1M-001 | Avoid dual authoring |
| P1M-008 | `docs/references/hlk/Research & Logic/.../baseline_organisation_rows (4).csv` | Role-to-process ownership | CSV mirror does not represent `responsible_processes` | Define whether process ownership is authored in CSV, markdown, or derived from process docs | P1 | P1M-004 | Needed for MADEIRA lookup quality |
| P1M-009 | `docs/references/hlk/Research & Logic/.../baseline_organisation_rows (4).csv` | Role-to-component mapping | CSV mirror does not represent `components_used` | Define component mapping authoring strategy and target field model | P2 | P1M-004 | Useful later for ERP and system topology queries |
| P1M-010 | `docs/references/hlk/Research & Logic/.../process_list_1 - process_list_1.csv` | Granularity canon | 72 rows use inconsistent `Process` / `Task` casing | Normalize to lowercase `project/workstream/process/task` canon | P0 | P1M-001 | Must match SOP contract |
| P1M-011 | `docs/references/hlk/Research & Logic/.../process_list_1 - process_list_1.csv` | Unknown scope rows | 4 rows still use `TBD` entity and area values | Assign owner and resolution path for each TBD row | P0 | P1M-001 | Good early cleanup target |
| P1M-012 | `docs/references/hlk/Research & Logic/.../process_list_1 - process_list_1.csv` | Sparse metadata | Later rows have missing confidence, frequency, and quality values | Define minimum required process metadata for ingest-ready rows | P1 | P1M-002 | Helps deterministic validation |
| P1M-013 | `docs/references/hlk/compliance/process_list_1.csv` and `docs/references/hlk/Research & Logic/.../process_list_1 - process_list_1.csv` | Mirror divergence | Two process mirrors exist and may drift | Declare canonical process file and define mirror sync direction | P0 | P1M-001 | Same issue for baseline organisation mirrors |
| P1M-014 | `docs/references/hlk/Research & Logic/.../supabase (9).ts` and SQL dumps | Stable key policy | Several typed relationships rely on `role_name` rather than stable IDs | Define machine-key policy for long-term sync and rename safety | P1 | P1M-004, P1M-010 | Important before automation expands |
| P1M-015 | `docs/references/hlk/compliance/SOP-META_PROCESS_MGMT_001.md` and `docs/references/hlk/Research & Logic/.../supabase (9).ts` | SOP ingestion pipeline | Structured SOP tables exist but markdown-to-DB contract is not documented | Define markdown-first to `compliance_001.sop_documents` / `sop_sections` pipeline | P1 | P1M-001, P1M-002 | Enables later retrieval and embeddings |

## Target Vault File Structure

The canonical vault should mirror the organisational hierarchy. Every compliance or baseline item has an owner; the file tree cascades from entity to area to role chain to owned processes and SOPs.

```
docs/references/hlk/
  compliance/                          # Cross-entity governance baselines
    baseline_organisation_rows.csv     # Canonical org baseline (single file)
    process_list_1.csv                 # Canonical process baseline (single file)
    SOP-META_PROCESS_MGMT_001.md       # Governing meta-SOP
    access_levels.md                   # Frozen taxonomy
    confidence_levels.md               # Frozen taxonomy
    source_taxonomy.md                 # Frozen source categories and levels

  Research & Logic/
    Holistika Research v2.7/
      Admin/                           # Entity: Holistika -- Admin area
        CBO/                           # Chief Business Office
          O5-1/                        # Role: O5-1 (currently you)
            CPO/                       # Area: People
              Compliance/
                Organisation/
              Talent/
                Ethics & Learning/
                Corporate Marketing/
            CFO/                       # Area: Finance
              Business Controller/
                Pricing/
                Taxes/
              Financial Controller/
                Front Office/
                  O2C/
                  PTP/
            COO/                       # Area: Operations
              PMO/
                Project Manager/
                Product Owner/
              SMO/
                Service Delivery Manager/
                Account Manager/
                Asset Manager/
            CMO/                       # Area: Marketing
              Brand Manager/
                AV/
                Copywriter/
                Design/
              Social Media Manager/
                Community Manager/
                Paid Media Manager/
            CDO/                       # Area: Data
              Data Architect/
              Lead Data Scientist/
                Business Analyst/
                Data Engineer/
            CTO/                       # Area: Tech
              DevOPS/
              System Owner/
          Envoy Tech Lab/              # Entity: Envoy Tech / HLK Tech Lab
          Research Dept/               # Entity: Holistika Research
        AI/                            # Susana Madeira and AIC chain
```

Rules:
- each role folder can contain its own SOPs, process docs, and linked assets
- process items from `process_list_1.csv` are owned by the `role_owner` in that row and cascade under that role's folder
- compliance baseline items (access levels, confidence, source taxonomy) live under `compliance/` because they are cross-entity
- the `Research & Logic` tree already approximates this structure; Phase 1 should formalize and fill gaps rather than restructure from scratch

## Data-Entry Queue

This queue is organized by entity, area, and organigram hierarchy. It replaces the earlier flat batch lists with a structure that matches the target vault layout. Each entry shows what needs to be filled and what access-level review is needed.

Depends on: completion of `P1.DEP.1` (precedence), `P1.DEP.2` (taxonomy freeze), and `P1.DEP.3` (org contract) before bulk entry begins.

### Holistika -- Admin

| Role | Entity | Area | reports_to | Current access | Access review needed | Description status | Fields to fill |
|------|--------|------|------------|----------------|----------------------|--------------------|----------------|
| Admin | Holistika | Admin | Admin | 6 | Confirm | Has description | `role_full_description`, `responsible_processes`, `components_used` |
| O5 | Holistika | Admin | Admin | 0 | Review: likely 5-6 | Missing description | `role_description`, `role_full_description`, `sop_url`, `org_id` |
| O5-1 | Holistika | Admin | Admin | 0 | Review: likely 6 | Shallow | `role_full_description`, `responsible_processes` |

### Holistika -- AI

| Role | Entity | Area | reports_to | Current access | Access review needed | Description status | Fields to fill |
|------|--------|------|------------|----------------|----------------------|--------------------|----------------|
| Susana Madeira | Holistika | AI | Admin | 0 | Review: likely 5-6 | Has description | `role_full_description`, `sop_url`, `org_id`, `responsible_processes` |
| AIC | Holistika | AI | Susana Madeira | 0 | Review: likely 5 | Has description | `role_full_description`, `sop_url`, `org_id`, `responsible_processes`, `components_used` |

### Holistika -- People (special roles)

| Role | Entity | Area | reports_to | Current access | Access review needed | Description status | Fields to fill |
|------|--------|------|------------|----------------|----------------------|--------------------|----------------|
| Public | Holistika | People | Admin | 0 | Confirm (intentional 0) | Has description | `role_full_description`, `org_id` |
| D-Class | Holistika | People | CPO | 0 | Confirm (intentional 0) | Has description | `role_full_description`, `org_id` |
| Holistik Researcher | Holistika | People | O5-1 | 0 | Review: likely 4 | Missing description | `role_description`, `role_full_description`, `sop_url`, `org_id` |
| Lead Researcher | Holistika | People | Holistik Researcher | 0 | Review: likely 3 | Missing description | All fields |
| Senior Researcher | Holistika | People | Lead Researcher | 0 | Review: likely 2 | Missing description | All fields |
| Private Researcher | Holistika | People | Lead Researcher | 0 | Review: likely 1 | Missing description | All fields |

### Think Big -- People (CPO chain)

| Role | Entity | Area | reports_to | Current access | Access review needed | Description status | Fields to fill |
|------|--------|------|------------|----------------|----------------------|--------------------|----------------|
| CPO | Think Big | People | O5-1 | 5 | Confirm | Shallow | `role_full_description`, `responsible_processes` |
| Compliance | Think Big | People | CPO | 0 | Review: likely 4-5 | Has description | `role_full_description`, `responsible_processes` |
| Organisation | Think Big | People | CPO | 4 | Confirm | Has description | `role_full_description`, `responsible_processes` |
| Talent | Think Big | People | CPO | 4 | Confirm | Has description | `role_full_description`, `responsible_processes` |
| Ethics & Learning | Think Big | People | Talent | 3 | Confirm | Has description | `role_full_description` |
| Corporate Marketing | Think Big | People | Talent | 0 | Review: likely 3 | Has description | `role_full_description` |

### Think Big -- Operations (COO chain)

| Role | Entity | Area | reports_to | Current access | Access review needed | Description status | Fields to fill |
|------|--------|------|------------|----------------|----------------------|--------------------|----------------|
| COO | Think Big | Operations | O5-1 | 5 | Confirm | Shallow | `role_full_description`, `responsible_processes` |
| PMO | Think Big | Operations | COO | 4 | Confirm | Has description | `role_full_description`, `responsible_processes` |
| SMO | Think Big | Operations | COO | 0 | Review: likely 4 | Shallow | `role_full_description`, `responsible_processes` |
| Project Manager | Think Big | Operations | PMO | 3 | Confirm | Shallow | `role_full_description` |
| Product Owner | Think Big | Operations | PMO | 3 | Confirm | Shallow | `role_full_description` |
| Service Delivery Manager | Think Big | Operations | SMO | 3 | Confirm | Shallow | `role_full_description` |
| Account Manager | Think Big | Operations | SMO | 3 | Confirm | Has description | `role_full_description` |
| Asset Manager | Think Big | Operations | SMO | 3 | Confirm | Shallow | `role_full_description` |

### Think Big -- Finance (CFO chain)

| Role | Entity | Area | reports_to | Current access | Access review needed | Description status | Fields to fill |
|------|--------|------|------------|----------------|----------------------|--------------------|----------------|
| CFO | Think Big | Finance | O5-1 | 5 | Confirm | Shallow | `role_full_description`, `responsible_processes` |
| Business Controller | Think Big | Finance | CFO | 4 | Confirm | Has description | `role_full_description`, `responsible_processes` |
| Financial Controller | Think Big | Finance | CFO | 4 | Confirm | Has description | `role_full_description` |
| Pricing | Think Big | Finance | Business Controller | 3 | Confirm | Has description | `role_full_description` |
| Taxes | Think Big | Finance | Business Controller | 0 | Review: likely 3 | Has description | `role_full_description` |
| Front Office | Think Big | Finance | Financial Controller | 3 | Confirm | Has description | `role_full_description` |
| O2C | Think Big | Finance | Front Office | 3 | Confirm | Has description | `role_full_description` |
| PTP | Think Big | Finance | Front Office | 3 | Confirm | Has description | `role_full_description` |

### Think Big -- Marketing (CMO chain)

| Role | Entity | Area | reports_to | Current access | Access review needed | Description status | Fields to fill |
|------|--------|------|------------|----------------|----------------------|--------------------|----------------|
| CMO | Think Big | Marketing | O5-1 | 5 | Confirm | Shallow | `role_full_description`, `responsible_processes` |
| Brand Manager | Think Big | Marketing | CMO | 0 | Review: likely 4 | Has description | `role_full_description` |
| Social Media Manager | Think Big | Marketing | CMO | 4 | Confirm | Shallow | `role_full_description` |
| AV | Think Big | Marketing | Brand Manager | 3 | Confirm | Shallow | `role_full_description` |
| Copywriter | Think Big | Marketing | Brand Manager | 0 | Review: likely 3 | Shallow | `role_full_description` |
| Design | Think Big | Marketing | Brand Manager | 3 | Confirm | Shallow | `role_full_description` |
| Community Manager | Think Big | Marketing | Social Media Manager | 0 | Review: likely 3 | Has description | `role_full_description` |
| Paid Media Manager | Think Big | Marketing | Social Media Manager | 3 | Confirm | Has description | `role_full_description` |

### Think Big -- Data (CDO chain)

| Role | Entity | Area | reports_to | Current access | Access review needed | Description status | Fields to fill |
|------|--------|------|------------|----------------|----------------------|--------------------|----------------|
| CDO | Think Big | Data | O5-1 | 0 | Review: likely 5 | Shallow | `role_full_description`, `responsible_processes` |
| Data Architect | Think Big | Data | CDO | 0 | Review: likely 4 | Has description | `role_full_description` |
| Lead Data Scientist | Think Big | Data | CDO | 4 | Confirm | Shallow | `role_full_description` |
| Business Analyst | Think Big | Data | Lead Data Scientist | 3 | Confirm | Shallow | `role_full_description` |
| Data Engineer | Think Big | Data | Lead Data Scientist | 3 | Confirm | Shallow | `role_full_description` |

### Think Big -- Tech (CTO chain)

| Role | Entity | Area | reports_to | Current access | Access review needed | Description status | Fields to fill |
|------|--------|------|------------|----------------|----------------------|--------------------|----------------|
| CTO | Think Big | Tech | O5-1 | 0 | Review: likely 5 | Has description | `role_full_description`, `responsible_processes` |
| DevOPS | Think Big | Tech | CTO | 0 | Review: likely 4 | Shallow | `role_full_description` |
| System Owner | Think Big | Tech | CTO | 0 | Review: likely 4 | Shallow | `role_full_description` |

### Access-Level Review Summary

Roles currently at access `0` that likely need review:

| Role | Entity | Area | Likely target | Rationale |
|------|--------|------|---------------|-----------|
| O5 | Holistika | Admin | 5-6 | Executive governance |
| O5-1 | Holistika | Admin | 6 | Currently you |
| Susana Madeira | Holistika | AI | 5-6 | AI agent chain root |
| AIC | Holistika | AI | 5 | Code execution permissions |
| Compliance | Think Big | People | 4-5 | Policy enforcement |
| Corporate Marketing | Think Big | People | 3 | Cross-functional |
| SMO | Think Big | Operations | 4 | Service management |
| CDO | Think Big | Data | 5 | C-level |
| CTO | Think Big | Tech | 5 | C-level |
| Data Architect | Think Big | Data | 4 | Architecture authority |
| DevOPS | Think Big | Tech | 4 | Infrastructure access |
| System Owner | Think Big | Tech | 4 | Infrastructure authority |
| Brand Manager | Think Big | Marketing | 4 | Area management |
| Copywriter | Think Big | Marketing | 3 | Content production |
| Community Manager | Think Big | Marketing | 3 | Customer-facing |
| Taxes | Think Big | Finance | 3 | Financial data |
| Holistik Researcher | Holistika | People | 4 | Research authority |
| Lead Researcher | Holistika | People | 3 | Research chain |
| Senior Researcher | Holistika | People | 2 | Research chain |
| Private Researcher | Holistika | People | 1 | Base research |

### Process-Level Items Relevant Across Batches

Process items from `process_list_1.csv` cascade under their `role_owner`. During data entry, these should be reviewed alongside the role they belong to:

- `hol_resea_dtp_*` processes belong under the Holistika Research chain
- `hol_ops_dtp_*` processes belong under Holistika Operations / PMO
- `hol_peopl_dtp_*` processes belong under Holistika People / Compliance / Talent
- `thi_opera_dtp_*` processes belong under Think Big Operations / PMO
- `thi_finan_dtp_*` processes belong under Think Big Finance / CFO chain
- `thi_mkt_dtp_*` processes belong under Think Big Marketing / CMO chain
- `thi_data_dtp_*` processes belong under Think Big Data / CDO chain
- `thi_tech_dtp_*` and `env_tech_dtp_*` processes belong under HLK Tech Lab / CTO chain
- `env_mkt_dtp_*` processes belong under Envoy Tech Marketing
- `tbd_tbd_dtp_*` processes need owner assignment before any further work
- `thi_legal_dtp_*` processes need a Legal area owner defined in the baseline
- `thi_peopl_dtp_*` processes belong under Think Big People chain

## Notes For Implementation

- Prefer filling meaning from `docs/references/hlk/Research & Logic/` before inventing new wording.
- Treat SQL dumps as audit/reference material unless the plan later promotes a structured table as canonical.
- Do not start bulk sync automation until precedence, taxonomy, and stable-key policy are frozen.
- The data-entry queue above is the single source for batch planning; do not create separate batch files.
- Process items should be reviewed alongside the role they cascade under, not in a separate pass.
- The target vault structure formalizes the existing `Research & Logic` tree; Phase 1 fills gaps rather than restructuring from scratch.
