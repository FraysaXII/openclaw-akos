# Founder Governance Document Lifecycle

**Document owner**: Compliance  
**Version**: 1.0  
**Date**: 2026-04-08  
**Status**: Final

---

## Purpose

This document defines the promotion ladder for founder-governance knowledge in the HLK vault. It exists so lower-layer founder, entity, funding, certification, and IP work can scale without drifting into duplicated notes, inconsistent owners, or premature registry changes.

## Promotion Ladder

| Layer | Purpose | Canonical? | Typical location |
|:------|:--------|:-----------|:-----------------|
| Source evidence | Raw calls, interviews, adviser notes, external research | No | External files, working inputs |
| Working synthesis | Redacted interpretation and cross-checking | No | `docs/wip/` |
| Case layer | Current founder/entity decisions and evidence packs | Yes | `docs/references/hlk/v3.0/` |
| SOP layer | Repeatable operating procedure | Yes | `docs/references/hlk/v3.0/` |
| Registry layer | Runtime-discoverable project/workstream/process/task model | Yes | `docs/references/hlk/compliance/process_list.csv` |
| Org layer | Role ownership model | Yes | `docs/references/hlk/compliance/baseline_organisation.csv` |
| PMO portfolio layer | Program metadata SSOT (status, links, GOI/POI handles); not a second narrative vault | Yes (thin) | [TOPIC_PMO_CLIENT_DELIVERY_HUB.md](../../Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) |

## Operating Rule

Do not skip layers unless the target layer is already clearly justified.

In practice:

- raw conversations do not become canonical by themselves
- `docs/wip` is where interpretation and validation happen
- once the content is stable and role-owned, it becomes a case doc in `v3.0`
- once the activity is repeatable, it becomes an SOP
- once the activity must be discoverable as a formal process, it gets a `process_list.csv` row
- `baseline_organisation.csv` changes only when ownership itself changes

## One-Owner Rule

Every canonical case or SOP doc should have one clear primary owner.

Cross-functional work is expected, but duplication is not. If multiple roles need the same concept:

- pick one primary owner
- keep one canonical file
- reference it from the other roles or layers instead of rewriting it

## Promotion Triggers

### Promote From `docs/wip` To A Case Doc When

- sensitive material has been redacted
- the business meaning is stable enough to preserve
- a role owner can be assigned clearly
- the note is specific to the current founder/entity case

### Promote From Case Doc To SOP When

- the activity is clearly repeatable
- the same checklist or sequence will be used again
- inputs, outputs, and responsibilities can be stated cleanly

### Promote To `process_list.csv` When

- the process needs a stable `item_id`
- MADEIRA or HLK registry lookups should be able to find it
- parent project/workstream ownership is clear
- the process is no longer just an isolated case note

### Promote To `baseline_organisation.csv` When

- no existing owner role can responsibly own the content
- repeated overload or ambiguity shows the org model itself is incomplete

## Anti-Patterns

Avoid these failure modes:

- putting raw adviser statements directly into canonical docs
- creating multiple owner copies of the same idea
- adding process rows for concepts that are still case-specific notes
- expanding the org model when ownership can already be expressed by existing roles
- hiding open issues inside "final" docs with no visible change trigger

## Lower-Layer Scaling Rule

The founder-governance lower layer scales properly when the same progression happens every time:

1. capture and clean source evidence
2. synthesize in `docs/wip`
3. promote stable founder-specific decisions into role-owned case docs
4. formalize repeatable procedures as SOPs
5. register only the repeatable processes in `process_list.csv`
6. sync operator-facing docs when the canonical pattern changes

This keeps the lower layer modular. New founder cases can reuse the SOP and registry layer while generating fresh case docs without destabilizing the canon.

## Maintenance Triggers

Review this lifecycle note when:

- a new founder-governance document type appears
- a case note begins to behave like a repeatable process
- registry growth starts outpacing case-doc clarity
- ownership repeatedly feels ambiguous between Legal, Finance, Compliance, Research, or Brand

## Linked Documents

- Knowledge index: [../Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md](../Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md)
- Working synthesis: [../../../../../../../wip/planning/04-holistika-company-formation/reports/founder-incorporation-report.md](../../../../../../../wip/planning/04-holistika-company-formation/reports/founder-incorporation-report.md)
- ENISA SOP: [SOP-ENISA_READINESS_001.md](SOP-ENISA_READINESS_001.md)
