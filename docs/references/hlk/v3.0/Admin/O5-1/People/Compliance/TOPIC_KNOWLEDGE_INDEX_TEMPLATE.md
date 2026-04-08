# Topic Knowledge Index — Template

**Document owner**: &lt;Primary owner role, e.g. Compliance or Legal Counsel&gt;  
**Version**: 0.1  
**Date**: YYYY-MM-DD  
**Status**: Draft | Review | Final  
**topic_id**: `topic_<stable_slug>`  

---

## Purpose

Canonical entrypoint for one **topic bundle**. One primary owner; cross-functional content links here instead of duplicating prose. Follow [FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md](../Legal/FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md) as a completed example.

## Bundle structure

### Source synthesis

- Working synthesis: `docs/wip/...` (link when non-canonical)

### Procedural layer

- SOP links (v3.0, role-owned)

### Case layer

- Decision memos, evidence packs, dated case notes

### Visual / Output 1 sources

- Link each `VISUAL_*.md` stub under `_assets/<topic_id>/` or list `source_id` values

### Registered process anchors

- `item_id` — short label (from [process_list.csv](../../../../../compliance/process_list.csv))

### Facts (optional)

- Short bullet facts with `source_id` citations; or link to a fact table file

## How to use

1. Start from wip synthesis for context.  
2. Use case layer for current decisions.  
3. Use SOP layer for repeatable operations.  
4. Update [FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md](FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md) patterns before inventing new document types.  
5. Add `process_list.csv` rows only when behavior is repeatable and owned.

## Maintenance

Update this index when any linked SOP, case doc, or registry anchor changes materially.

## Governance tags (Obsidian)

Use prefixes from [HLK_KM_TOPIC_FACT_SOURCE.md](../../../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md), e.g. `topic/<topic_id>`, `dim/role/...`, `status/...`.
