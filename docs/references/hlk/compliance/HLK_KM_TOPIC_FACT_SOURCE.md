# HLK Knowledge Management: Topic, Fact, and Source Model

**Item Name**: HLK Knowledge Management Topic–Fact–Source Contract  
**Item Number**: HLK-COMPLIANCE-KM-001  
**Object Class**: Baseline Reference  
**Confidence Level**: Safe  
**Security Level**: 2 (Internal Use)  
**Entity Owner**: Holistika  
**Area Owner**: Compliance, Data Architecture, PMO  
**Version**: 1.0  
**Revision Date**: 2026-04-08  

---

## Purpose

Define the governed information model for Holistika knowledge: **Topic**, **Fact**, and **Source**, with **output type** metadata (0–4) and alignment to [PRECEDENCE.md](PRECEDENCE.md). This contract is the single schema authority for how canonical markdown, visual assets, manifests, and external backlogs relate to each other without duplicating folder ownership rules.

## Relationship to vault structure

- **Folder tree** under `docs/references/hlk/v3.0/` remains **role-owned** (see [v3.0/index.md](../v3.0/index.md)).
- **Topics** are logical bundles; they may span roles but must have **one primary owner** and **one canonical index** per bundle (see [TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md](../v3.0/Admin/O5-1/People/Compliance/TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md)).
- **Facts** cite **Sources**; promotion to canonical v3.0 docs follows the same ladder as founder governance (see [FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md](../v3.0/Admin/O5-1/People/Compliance/FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md)).

## Output types (`output_type`)

| Value | Name | Examples |
|-------|------|----------|
| 0 | Voice / audio | Recordings, dictation, meeting captures |
| 1 | Image / visual | Excalidraw exports, PNG/JPG diagrams, screenshots |
| 2 | Text | Plain or enriched markdown, transcripts (as text), SOPs |
| 3 | Structured data | CSV, tables, DB schemas, column/attribute definitions |
| 4 | Code / scripts | Application code, automation, queries |

Optional refinement for type **2**: use `text_mode: plain | enriched` in manifest or frontmatter without changing the integer.

## Artifact roles (`artifact_role`)

Aligns with precedence layers:

| Value | Meaning |
|-------|---------|
| `source` | Raw or primary capture (may live outside v3.0 or in `docs/wip/`) |
| `interpretation` | Redacted synthesis, gap analysis, working notes |
| `canonical` | Promoted role-owned document under `v3.0/` |
| `registry` | Authoritative row in `process_list.csv` or canonical index tables (e.g. PMO Trello registry) |
| `mirror` | KiRBe, Drive copy, DB projection — derived from canonical |

## Intellectual kind (`intellectual_kind`)

Used for review depth and retrieval; examples: `process_map`, `architecture`, `wireframe`, `methodology_map`, `manifesto`, `evidence_screenshot`, `brand_asset`, `pilot_placeholder`.

## Topic

A **topic** is a stable subject area with:

- `topic_id`: snake_case stable id matching `^topic_[a-z0-9_]{2,64}$` (must not collide with `item_id` in `process_list.csv`).
- `title`: human-readable name.
- **primary_owner_role**: must match `role_name` in [baseline_organisation.csv](baseline_organisation.csv).
- Links to sources, facts, optional `process_list.csv` `item_id` anchors.

### Topic registry (Initiative 25 P1; D-IH-12)

Topics are now first-class governed entities in the canonical CSV [`compliance/dimensions/TOPIC_REGISTRY.csv`](dimensions/TOPIC_REGISTRY.csv) (Initiative 25 P2). The CSV is the **single source of truth** for cross-topic edges:

- `parent_topic` — single optional parent topic_id.
- `related_topics` — semicolon-separated list (peer relationships).
- `depends_on` — semicolon-separated list (this topic's outputs require these upstream topics).
- `subsumes` / `subsumed_by` — semicolon-separated lists (used after a topic merge; the subsuming topic typically has `lifecycle_status = active` and the subsumed topics `superseded`).

The per-topic `*.manifest.md` may **project** these edges into the manifest's `topic_ids:` and (optionally) a `related_topics:` slot for human readability, but those manifest fields are **derived from the CSV and must FK-resolve** into `TOPIC_REGISTRY.csv` at validation time. **Drift = canonical wins** per [`PRECEDENCE.md`](PRECEDENCE.md) §"Conflict Resolution".

The Postgres mirror at `compliance.topic_registry_mirror` stores the same columns as TEXT (DAMA-pure projection); Neo4j projects typed relationships from the same edges (`:DEPENDS_ON`, `:TOPIC_PARENT_OF`, `:RELATED_TO`, `:TOPIC_SUBSUMES`, `:UNDER_PROGRAM`) per Initiative 25 P-graph (D-IH-18).

### Obsidian wikilinks (Initiative 25 P4; D-IH-12)

Topic companion `.md` files MAY use `[[topic_id]]` Obsidian-style wikilinks as a **secondary** navigation aid alongside primary markdown links. Wikilinks are **explicitly out of scope** for `validate_hlk_vault_links.py` — markdown links cover validator reachability; wikilinks are operator/Obsidian convention only.

## Fact

A **fact** is a short, auditable statement that:

- References at least one **source_id** (file path + version or manifest id).
- For intelligence-style content, may reference [source_taxonomy.md](source_taxonomy.md) (`source_category`, `source_level`).
- Does not replace canonical SOPs; repeatable behavior is still captured in SOPs and optionally registered in `process_list.csv`.

Facts may be stored in topic index sections, separate fact tables (markdown/CSV), or future derived indexes; **canonical prose** remains markdown in git unless otherwise listed in PRECEDENCE.

## Source

A **source** is a concrete artifact:

- Has `source_id` (unique string).
- Has `output_type` (0–4).
- Has `location` (repo-relative path or controlled URI).
- Carries **access_level** per [access_levels.md](access_levels.md) and **confidence** per [confidence_levels.md](confidence_levels.md) when promoted or when sensitive.

### Output 1 (visuals) — required companions

Every canonical **Output 1** asset under `v3.0/_assets/` MUST have:

1. **Manifest**: `*.manifest.md` (YAML frontmatter or structured markdown) with fields listed below.
2. **Stub text** (Output 2): `VISUAL_<source_id>.md` or equivalent short markdown that describes the diagram for search, RAG, and Obsidian; the image remains the visual evidence.

#### Directory convention (Initiative 22 P1, 2026-04-29)

Output 1 assets MUST be placed under a **plane × program × topic** path:

```
docs/references/hlk/v3.0/_assets/<plane>/<program_id>/<topic_id>/
  <topic_id>.manifest.md
  <topic_id>.md          (Output 2 companion stub)
  <topic_id>.png         (raster — required)
  <topic_id>.svg         (vector — recommended when source allows)
  <topic_id>.mmd         (Mermaid source — required when raster is auto-rendered)
  <topic_id>.excalidraw  (Excalidraw source — when curated by hand)
```

Where:

- `<plane>` is one of the planes documented in [`compliance/README.md`](README.md) (`advops`, `finops`, `techops`, `mktops`, `marops`, `devops`, `ops`, `dimensions`, `km-pilot`, etc.).
- `<program_id>` is the canonical program identifier (e.g. `PRJ-HOL-FOUNDING-2026`) from `process_list.csv` / register columns. Use `shared` when the asset is cross-program.
- `<topic_id>` matches the manifest's `topic_ids[0]` (and the file basename).

The historical `_assets/km-pilot/VISUAL_*` layout is grandfathered for the pilot bundle; new topics use the layout above.

#### Manifest minimum fields

| Field | Required | Description |
|-------|----------|-------------|
| `source_id` | yes | Stable id |
| `output_type` | yes | `1` for visuals |
| `title` | yes | Short title |
| `created` | yes | ISO date |
| `author_role` | yes | `role_name` from org baseline |
| `topic_ids` | yes | List of topic ids |
| `summary` | yes | 2–5 lines |
| `paths` | yes | Relative paths to **raster** (required), and optional **excalidraw**, **mermaid**, and **svg** sources (see below) |
| `access_level` | yes | Integer 0–6 |
| `confidence` | recommended | Safe / Euclid / Keter or legacy mapping per confidence_levels |
| `artifact_role` | yes | Usually `canonical` or `source` |
| `intellectual_kind` | yes | See list above |
| `related_process_ids` | no | `item_id` from process_list |
| `supersedes` / `superseded_by` | no | Prior `source_id` chain |
| `file_sha256` | recommended | For drift detection on the raster |

#### `paths` slots

```
paths:
  raster: ./<topic_id>.png           # required — sha256 covers this file
  svg: ./<topic_id>.svg              # optional — vector form of the same diagram
  mermaid: ./<topic_id>.mmd          # optional — Mermaid source-of-truth; rendered via scripts/render_km_diagrams.py
  excalidraw: ./<topic_id>.excalidraw # optional — hand-curated source-of-truth
```

**Source-of-truth rule**. When a manifest lists a `mermaid:` or `excalidraw:` source, that source is the editable SSOT and the raster is **derived**. Do not hand-edit derived rasters; regenerate from source. The manifest's `file_sha256` covers the raster only; the editable source carries no sha because it is human-edited.

## Obsidian and controlled tags

Tags are **governed**. Allowed prefix families (extend only by revising this document):

- `dim/role/<role_name_slug>`
- `dim/area/<area_slug>`
- `dim/entity/<entity_slug>`
- `topic/<topic_id>`
- `out/0` … `out/4`
- `src/<source_id>`
- `status/draft`, `status/review`, `status/final`

**Rule:** Do not introduce new top-level tag roots without updating this contract.

## Derived recall (optional)

Machine indexes (SQLite FTS, embeddings, graph projections) are **derived** and must be **rebuildable from** canonical markdown, CSVs, and manifests. They are not a second SSOT (see OpenClaw-style “canonical markdown + derived index” pattern).

## References

- [PRECEDENCE.md](PRECEDENCE.md)
- [access_levels.md](access_levels.md)
- [confidence_levels.md](confidence_levels.md)
- [source_taxonomy.md](source_taxonomy.md)
- [SOP-META_PROCESS_MGMT_001.md](SOP-META_PROCESS_MGMT_001.md)
