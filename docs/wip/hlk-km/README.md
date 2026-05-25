---
language: en
status: deprecated
deprecated_at: 2026-05-25
deprecated_by_decision: D-IH-86-CY-D
superseded_by: docs/wip/intelligence/
role_owner: Research Director + KM Officer
classification: way_of_working
authored: 2026-05-25
---

# docs/wip/hlk-km/ — DEPRECATED (folder superseded by `docs/wip/intelligence/`)

> Per **D-IH-86-CY-D** (2026-05-25): this folder is the historical predecessor of [`docs/wip/intelligence/`](../intelligence/). It was the Tier 1 WIP home until the **WORKSPACE_BLUEPRINT_HOLISTIKA §17 + D-IH-70-O 3-tier WIP topology** ratification (2026-05-12) reassigned Tier 1 to Research-area-owned `intelligence/`. **The 5 stub files below remain in place** as historical reference + to preserve Trello-card linkage; they should not receive new authoring. New cross-area research, engagement intelligence folders, substrate-audit folders, and KM drafts land under `docs/wip/intelligence/` per its [README.md](../intelligence/README.md).

## Why this folder is deprecated (and why the stubs stay)

Between 2026-04-09 (when these 5 stub files were authored) and 2026-05-12 (D-IH-70-O ratification), the Tier 1 WIP home moved from this folder to `docs/wip/intelligence/`. The 5 stubs here are *pointer-only* files that index Trello-registered research backlog cards — none carry substantive content; they're 1-2 paragraph hooks for the [RESEARCH_BACKLOG_TRELLO_REGISTRY.md](../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md). Deleting them would break Trello-card → repo linkage; promoting them prematurely would mint canonical content without the operator review the 3-tier topology requires. Leaving them in place with this deprecation notice is the safest disposition.

When a backlog card matures into substantive research, the right next move is:

1. Open a new sub-folder under `docs/wip/intelligence/<topic-slug>/` per the new Tier 1 SSOT.
2. Cross-reference the original Trello card from the new folder's README.
3. Update [RESEARCH_BACKLOG_TRELLO_REGISTRY.md](../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md) row to point at the new `intelligence/` home.
4. Annotate the corresponding stub in this folder with a `superseded_by:` frontmatter line pointing at the new sub-folder.

When ALL 5 stubs have been superseded this way, this folder can be archived entirely to `docs/wip/_archived/hlk-km-pre-2026-05-12/` (deferred to a future hygiene wave; not blocking).

## Stub inventory (5 files, all dated 2026-04-09)

| Stub file | Trello card name | Trello id | Successor in `intelligence/` |
|:---|:---|:---|:---|
| [`research-synthesis-ai-landscape.md`](research-synthesis-ai-landscape.md) | AI | `6769932a2e14f16f0004e6cd` | not yet minted |
| [`research-synthesis-legal-research.md`](research-synthesis-legal-research.md) | Legal | `6769932ce223d38514d3fc5c` | not yet minted |
| [`research-synthesis-macro-investment.md`](research-synthesis-macro-investment.md) | Macro Economists & Investments | `6769932a916c78afe2611081` | not yet minted |
| [`research-synthesis-madeira-radar.md`](research-synthesis-madeira-radar.md) | MADEIRA Project list | `676992d120f3b43df103aac7` | not yet minted |
| [`research-synthesis-research-pipeline.md`](research-synthesis-research-pipeline.md) | Research Material | `67699325c36ae35b88747a30` | not yet minted |

## Cross-references

- **Active Tier 1 home**: [`docs/wip/intelligence/`](../intelligence/) — Research-area-owned per WORKSPACE_BLUEPRINT_HOLISTIKA §17 + D-IH-70-O.
- **Ratifying decision**: D-IH-86-CY-D (2026-05-25 — deprecate `hlk-km/` as Tier 1; preserve stubs).
- **Architectural decision**: D-IH-70-O (3-tier WIP topology — Tier 1 = `intelligence/`, Tier 2 = `planning/`, Tier 3 = `<area>/<role>/wip/`).
- **Blueprint**: [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §17.
- **Trello registry**: [`RESEARCH_BACKLOG_TRELLO_REGISTRY.md`](../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md).
- **`docs/wip/README.md`** — updated in the same commit (2026-05-25) to reflect Tier 1 = `intelligence/`.

## Doctrine reminder

This folder is **NOT canonical SSOT for any compliance asset**. Per [`PRECEDENCE.md`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md), canonical material lives under `docs/references/hlk/v3.0/`. WIP folders (Tier 1, 2, 3) are working spaces, never SSOT.
