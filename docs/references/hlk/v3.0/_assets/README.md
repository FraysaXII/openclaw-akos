# HLK `_assets/` — Output 1 directory contract

**Owner**: Compliance, Data Architecture (joint), with PMO as primary author for ADVOPS topics.  
**Status**: Forward layout convention (Initiative 22 P2, 2026-04-29).  
**Schema authority**: [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md) §"Output 1 (visuals) — required companions" and §"Directory convention".

This folder hosts canonical **Output 1** assets (visuals, diagrams, screenshots) referenced by Topic-Fact-Source manifests. Each asset bundle ships with its `*.manifest.md` sidecar, a short companion stub (`*.md`), the rendered raster (`*.png` — required), and any editable source-of-truth (`*.mmd`, `*.svg`, `*.excalidraw`).

## Layout

```
_assets/
├── README.md                                    (this file)
│
├── <plane>/                                     (one of advops, finops, mktops, techops, marops, devops, ops, dimensions, …)
│   └── <program_id>/                            (e.g. PRJ-HOL-FOUNDING-2026; or `shared` for cross-program assets)
│       └── <topic_id>/                          (matches manifest topic_ids[0])
│           ├── <topic_id>.manifest.md           (Output 1 manifest)
│           ├── <topic_id>.md                    (Output 2 companion stub)
│           ├── <topic_id>.png                   (raster — required; sha256 in manifest)
│           ├── <topic_id>.svg                   (vector — recommended)
│           ├── <topic_id>.mmd                   (Mermaid source-of-truth — when raster is auto-rendered)
│           └── <topic_id>.excalidraw            (Excalidraw source-of-truth — when curated by hand)
│
└── km-pilot/                                    (grandfathered legacy bundle from Phase 0 KM pilot — do not extend)
    └── VISUAL_km_pilot_NNN.{md,manifest.md,png,jpg}
```

## Adding a new asset bundle

1. **Pick a plane** from the canonical list documented in [`compliance/README.md`](../../compliance/README.md) (axis 1).
2. **Pick a `program_id`** from `process_list.csv` registered programs, or `shared` for cross-program assets (axis 2).
3. **Pick a `topic_id`** that matches the manifest's `topic_ids[0]` (axis 3). Topic ids use `snake_case`.
4. **Create the folder** `_assets/<plane>/<program_id>/<topic_id>/` and add the four required files (manifest, companion, raster, source).
5. **Validate** with `py scripts/validate_hlk_km_manifests.py`.

## Diagram source-of-truth

For diagrams that can be expressed in Mermaid (most flowcharts, sequence diagrams, ER diagrams), commit a `.mmd` source and **regenerate** the raster via `py scripts/render_km_diagrams.py <path-to-mmd>`. The renderer prefers `mmdc` (Mermaid CLI) when on PATH and falls back to the public `mermaid.ink` SVG endpoint when not. Both produce deterministic output for the same source.

For visuals that cannot be expressed in Mermaid (mockups, photos, hand-drawn artefacts), commit either the original Excalidraw file (`.excalidraw`) or the raster directly. Hand-edited rasters MUST NOT be regenerated.

## Conventions

- **Plane = single-p** (`advops`, `finops`, `mktops`, …) to match the operations-plane vocabulary in [`akos-holistika-operations.mdc`](../../../../../.cursor/rules/akos-holistika-operations.mdc) and the discipline codes in `ADVISER_ENGAGEMENT_DISCIPLINES.csv` (`LEG`, `FIS`, `IPT`, `BNK`, `CRT`, `NOT`).
- **`program_id` = canonical identifier** from `process_list.csv` (e.g. `PRJ-HOL-FOUNDING-2026`); use `shared` for cross-program topics.
- **`topic_id` = `snake_case`**; identical between folder name, manifest field `topic_ids[0]`, and file basenames.
- **`source_id` = `topic_id`** for Output-1 topic bundles (one-to-one). Use `VISUAL_<topic_id>` only for grandfathered km-pilot rows.

## Cross-references

- KM contract: [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md)
- Compliance layout convention: [`compliance/README.md`](../../compliance/README.md)
- Validator: [`scripts/validate_hlk_km_manifests.py`](../../../../../scripts/validate_hlk_km_manifests.py)
- Diagram renderer: [`scripts/render_km_diagrams.py`](../../../../../scripts/render_km_diagrams.py) (Initiative 22 P5)
- Initiative 22: [`docs/wip/planning/22-hlk-scalability-and-i21-closures/master-roadmap.md`](../../../wip/planning/22-hlk-scalability-and-i21-closures/master-roadmap.md)
