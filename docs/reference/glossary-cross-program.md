# HLK cross-program glossary

**Owner**: Compliance, Data Architecture (joint)  
**Purpose**: Single source of vocabulary referenced by 3+ first-class HLK docs. When in doubt, link **here** rather than redefining a term inline.  
**Initiative**: 23 P5 (2026-04-29).  
**Authority**: [`PRECEDENCE.md`](../references/hlk/compliance/PRECEDENCE.md) + [`compliance/README.md`](../references/hlk/compliance/README.md) (forward layout convention) + Initiative-specific decision logs.

> **Pointer rule** — When a term appears in **3+ first-class docs** (`docs/ARCHITECTURE.md`, `docs/USER_GUIDE.md`, `docs/DEVELOPER_CHECKLIST.md`, `CONTRIBUTING.md`, `README.md`, `CHANGELOG.md`, `PRECEDENCE.md`, or any `SOP-*.md` under `v3.0/`), **add a one-line entry in [`docs/GLOSSARY.md`](../GLOSSARY.md) with a "see" link to the relevant section here**. This keeps the wide-audience glossary scannable while the deep entries cluster here.

## Axes (forward layout convention — Initiative 22 D-IH-1)

Three axes structure every canonical surface (`compliance/`, `_assets/`, `v3.0/<role>/`):

- **Plane** — operational governance lane: `advops`, `finops`, `mktops`, `techops`, `marops`, `devops`, `ops`, `dimensions` (cross-plane). See [`akos-holistika-operations.mdc`](../../.cursor/rules/akos-holistika-operations.mdc) "Holistika operations planes".
- **Program / engagement** — delivery vehicle keyed by `program_id` (PRJ-HOL-style). See "Program identifiers" below.
- **Topic / register name** — subject matter and CSV file basename / KM `topic_id`. See [`HLK_KM_TOPIC_FACT_SOURCE.md`](../references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md).

## Program identifiers

`program_id` is the canonical handle used across CSVs, vault folders, and graph projections (Initiative 23 D-IH-8). Two ID systems coexist:

| Field | Format | Example | Purpose |
|:------|:-------|:--------|:--------|
| `program_id` | `PRJ-HOL-<CODE>-<YYYY>` (`^PRJ-HOL-[A-Z0-9-]+-\d{4}$`) | `PRJ-HOL-FOUNDING-2026`, `PRJ-HOL-KIR-2026` | Path-stable; used in `_assets/<plane>/<program_id>/<topic_id>/` and `v3.0/<role>/programs/<program_id>/` |
| `process_item_id` | `<entity>_<area>_prj_<n>` | `env_tech_prj_2`, `thi_legal_prj_1` | FK to `process_list.csv` `item_id` of `item_granularity = project` rows; **may be empty** for casework programs (e.g. `PRJ-HOL-FOUNDING-2026` has none) |
| `program_code` | `^[A-Z]{3}$` (unique) | `FND`, `KIR`, `LEG` | Short handle; used in graph node properties and slug shortcuts |

Active programs (live): see `docs/references/hlk/compliance/dimensions/PROGRAM_REGISTRY.csv`.

## Lifecycle status (programs)

Per `PROGRAM_REGISTRY.csv` `lifecycle_status` enum:

| Value | Meaning |
|:------|:--------|
| `proposed` | Drafted in the registry; not yet executing |
| `active` | Executing now; receiving operator attention |
| `paused` | Temporarily on hold; will resume |
| `closed` | Finished; rows kept for traceability |
| `superseded` | Subsumed by another program (see `subsumes_program_ids` on the successor) |

## Risk class (programs)

| Value | Examples |
|:------|:---------|
| `low` | Foundational umbrellas (`PRJ-HOL-RES-2026`, `PRJ-HOL-PEO-2026`) |
| `medium` | Most ongoing operational programs (default) |
| `high` | Time-bounded with regulatory or compliance window (`PRJ-HOL-FOUNDING-2026`) |
| `critical` | Production failure would harm clients or compromise trust |

## Discipline codes (ADVOPS)

Per `ADVISER_ENGAGEMENT_DISCIPLINES.csv` `discipline_code` (Initiative 21):

| Code | Discipline | Plane | Canonical role |
|:-----|:-----------|:------|:---------------|
| LEG | Legal & Corporate | advops | Legal Counsel |
| FIS | Fiscal & Tax | advops | Business Controller |
| IPT | IP & Trademark | advops | Legal Counsel |
| BNK | Banking | advops | Legal Counsel |
| CRT | Startup Certification | advops | Compliance |
| NOT | Notary | advops | Legal Counsel |

## Sensitivity bands (GOI/POI; D-CH-7 from Initiative 21)

| Sensitivity | Sharing label | Notes |
|:------------|:--------------|:------|
| `public` | `counsel_ok` (free) | Public authorities (AEAT, ENISA, OEPM) and `is_public_entity = true` GOIs |
| `internal` | `counsel_ok` | Default for internal-use rows; counsel and named counterparty may see |
| `confidential` | `counsel_and_named_counterparty` | Bank/desk-level details; limit forwarding |
| `restricted` | `internal_only` | Excluded from automated exports unless `--include-restricted` is explicitly set |

## GOI/POI class taxonomy (extended)

Initiative 21 D-CH-3 + Initiative 22 D-IH-5 enum (validated by `scripts/validate_goipoi_register.py`):

- Initiative-21 seed: `external_adviser`, `banking_channel`, `supplier`, `research_benchmark`, `lead`, `client_org`, `collaborator`, `public_authority`, `other`.
- Initiative-22 multi-program extension: `client`, `partner`, `investor`, `regulator`, `vendor`, `media`.

See [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) §4.7 for disambiguation guidance.

## Lens

Free-form lowercase-snake string on GOI/POI rows (e.g. `entity_readiness`, `fiscal_readiness`, `incorporation`, `marketing_benchmark`). Not enum-bounded; coined per program. Pattern: `^[a-z][a-z0-9_]{1,40}$`.

## Question / instrument id schemes (Initiative 21 D-CH-6)

- Adviser open questions: `Q-<DISC3>-<NNN>` — e.g. `Q-LEG-001`, `Q-FIS-001`, `Q-CRT-002`.
- Filed instruments: `INST-<DISC3>-<SLUG>-<YYYY>` — e.g. `INST-LEG-ESCRITURA-DRAFT-2026`.
- POI: `POI-<CLASS3>-<SLUG>-<YYYY>` — e.g. `POI-LEG-ENISA-LEAD-2026`.
- GOI: `GOI-<CLASS3>-<SLUG>-<YYYY>` — e.g. `GOI-ADV-ENTITY-2026`.

Slug discipline: ASCII uppercase + digits + hyphen; never recycle after retirement.

## Voice register (recipient profile)

Initiative 22 / 24 (D-IH-11) extension on `GOI_POI_REGISTER.csv`:

- `voice_register` enum: `formal_legal`, `peer_consulting`, `casual_internal`, `regulator_neutral`, `investor_aspirational`. Composer reads this; falls back to discipline default + brand foundation default.
- `language_preference`: `es`, `en`, `bilingual`.
- `pronoun_register`: `tu`, `usted`, or empty (non-Spanish).

## Output types (KM Topic-Fact-Source)

Per `HLK_KM_TOPIC_FACT_SOURCE.md`:

| Value | Name | Examples |
|:-----:|:-----|:---------|
| 0 | Voice / audio | Recordings |
| 1 | Image / visual | Excalidraw exports, PNG/JPG diagrams, Mermaid renders |
| 2 | Text | Plain or enriched markdown, transcripts, SOPs |
| 3 | Structured data | CSV, tables, DB schemas |
| 4 | Code / scripts | Application code, automation, queries |

## Artifact roles

| Value | Meaning |
|:------|:--------|
| `source` | Raw or primary capture |
| `interpretation` | Redacted synthesis, gap analysis, working notes |
| `canonical` | Promoted role-owned document under `v3.0/` |
| `registry` | Authoritative row in `process_list.csv` or canonical index tables |
| `mirror` | KiRBe, Drive copy, DB projection — derived from canonical |

## Graph projection (Neo4j)

Initiative 07 baseline + Initiative 23 P-graph extension (D-IH-18):

- Labels: `:Role`, `:Process`, `:Document` (optional), `:Program` (Initiative 23).
- Edges (process tree): `:REPORTS_TO`, `:OWNED_BY`, `:PARENT_OF`, `:LINKS_TO`.
- Edges (program tree, Initiative 23): `:CONSUMES`, `:PRODUCES_FOR`, `:PROGRAM_PARENT_OF`, `:PROGRAM_SUBSUMES`, `:OWNED_BY` (program → role). **Edge naming disambiguated** to coexist with the existing `:PARENT_OF` (process → process).

CSVs are SSOT; Neo4j is rebuildable read index. Allowlisted Cypher only in `akos/hlk_neo4j.py`.

## Verification profile names

| Profile | Purpose |
|:--------|:--------|
| `pre_commit` | Strict inventory + drift + tests + smoke + release-gate |
| `compliance_mirror_emit` | Generate compliance mirror upsert SQL bundle |
| `compliance_mirror_drift_probe` | Verify CSV-vs-mirror parity (operator-pasted JSON; SKIPs gracefully) |
| `export_adviser_handoff_smoke` | Render ADVOPS handoff (Markdown) |
| `export_adviser_handoff_pdf_smoke` | Render ADVOPS handoff (PDF; SKIPs when no renderer) |
| `wave2_backfill_check` | Sentinel scan of `operator-answers-wave2.yaml` (informational) |

## Cross-references

- [`PRECEDENCE.md`](../references/hlk/compliance/PRECEDENCE.md) — canonical / mirrored / reference-only authority ledger.
- [`compliance/README.md`](../references/hlk/compliance/README.md) — forward layout convention with deprecation-alias map.
- [`HLK_KM_TOPIC_FACT_SOURCE.md`](../references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md) — KM contract.
- [`docs/GLOSSARY.md`](../GLOSSARY.md) — wide-audience one-liners with "see" links here.
- Initiative 21 master roadmap (ADVOPS plane + GOI/POI dimension).
- Initiative 22 master roadmap (forward layout convention).
- Initiative 23 master roadmap (Program Registry + onboarding program 2).
