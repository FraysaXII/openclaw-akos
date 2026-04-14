# PMO client delivery hub — topic knowledge index (pilot)

**Document owner**: PMO  
**Version**: 0.1  
**Date**: 2026-04-09  
**Status**: Draft  
**topic_id**: `topic_pmo_client_delivery_hub`

---

## Purpose

Canonical entrypoint for **cross-entity client delivery**: links **Think Big** (non-repo artifacts), **Envoy Tech Lab** (GitHub repos), and PMO registries. One primary owner (PMO); other roles link here instead of duplicating engagement maps.

## Bundle structure

### Source synthesis

- Working synthesis: `docs/wip/...` (add when a specific engagement has redacted WIP notes)

### Procedural layer

- PMO processes: lookup `role_owner` = PMO in [process_list.csv](../../../../../compliance/process_list.csv) for repeatable delivery patterns.

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

## How to use

1. Register every tracked client-delivery repo in `REPOSITORIES_REGISTRY.md` (`class` = `client-delivery`).  
2. Keep commercials and non-repo deliverables under `Think Big/`.  
3. Promote stable, repeatable delivery steps toward SOPs and `process_list.csv` only when SOP-META criteria are met.  
4. Use Obsidian tags per KM contract, e.g. `topic/topic_pmo_client_delivery_hub`, `dim/entity/think_big`, `dim/entity/envoy_tech_lab`.

## Maintenance

Update this index when registry rows, Think Big paths, or major engagement scope changes.
