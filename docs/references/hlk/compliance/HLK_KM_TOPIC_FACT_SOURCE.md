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

- `topic_id`: kebab-case or `hol_*` / `thi_*` style stable id (must not collide with `item_id` in `process_list.csv`; use distinct namespace such as `topic_km_*` for non-process topics).
- `title`: human-readable name.
- **primary_owner_role**: must match `role_name` in [baseline_organisation.csv](baseline_organisation.csv).
- Links to sources, facts, optional `process_list.csv` `item_id` anchors.

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
| `paths` | yes | Relative paths to raster and optional `.excalidraw` |
| `access_level` | yes | Integer 0–6 |
| `confidence` | recommended | Safe / Euclid / Keter or legacy mapping per confidence_levels |
| `artifact_role` | yes | Usually `canonical` or `source` |
| `intellectual_kind` | yes | See list above |
| `related_process_ids` | no | `item_id` from process_list |
| `supersedes` / `superseded_by` | no | Prior `source_id` chain |
| `file_sha256` | recommended | For drift detection |

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
