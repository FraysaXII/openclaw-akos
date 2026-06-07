# L5 Topic Structure — Findings & Governed-Schema Design (R2-07)

> **Initiative:** Canonical Articulation Model (CAM / I95) — Layer 5 (Topic structure)
> **Operator ask (R2-07):** "finish + govern the *topic data structure* I already minted but never governed; help me migrate the `docs/wip/intelligence` corpus into it, and confirm/complete the IntelligenceOps register's home in Research."
> **Author:** MADEIRA research+design agent · **Date:** 2026-06-07
> **Mode:** Readonly research + single-doc write. No CSV / file moves / other edits performed.
> **Scope guard:** Bounded read set + ≤6 web searches (prior run died `resource_exhausted` on too-broad scope).
> **STATUS: RATIFIED** — `D-IH-95-H` (operator 2026-06-07): physical move authorized + research-area
> rule amended; schema + KM Officer steward accepted; data cleanup expanded to a repo-wide scattered-topic sweep; two-tranche execution.

---

## 0. TL;DR

- **The chassis already exists.** `TOPIC_REGISTRY.csv` (39 rows / 18 cols) already has a fieldnames SSOT, a validator **wired into `validate_hlk.py`**, a schema-drift gate, a Supabase mirror, a Neo4j projection, an HCAM `topic` entity row, and a Topic→Fact→Source contract. R2-07 is therefore a **govern + curate + bind** problem, **not** a build problem — the correction to "minted but never governed."
- **Six real gaps:** no row-level Pydantic enum model (confirm-item); mono-dimensional `topic_class` (39 rows collapse to ~2 values); **11 stranded `proposed` rows** with no corpus; **no working-corpus binding** (folders aren't keyed by `topic_id` — the missing "occurrences"); scattered ownership with **no named steward**; methodology-version drift.
- **Proposed schema (additive, non-breaking):** re-spec `topic_class`→`subject_kind` as an orthogonal facet; add `working_area_path`, `knowledge_index_path`, `steward_role`, `physical_model`; mint the Pydantic enum model; add a **lifecycle gate** (a topic can't be `active` without an occurrence).
- **Migration = reconciliation, key-by-`topic_id`, NO physical move** (doctrine-backed: `akos-research-area.mdc` RULE 2). The registry and the corpus drifted *both* ways — 10 registry rows have no folder; 5 `topic-*` folders have no row.
- **IntelligenceOps register is already in Research/Intelligence.** What remains: the (deliberately gated) legacy→promoted-top-level path move, and **activating the dormant KM Officer steward seat** (Research Director accountable) — which closes the steward gap for the topic registry, the IntelligenceOps register, and Tier-1 WIP all at once.
- **7 ratify gates** surfaced (§5), batched into 2 `AskQuestion` rounds. No canonical edits were made; the schema/data tranches need the operator-approval gate first.

---

## 1. Assessment — `TOPIC_REGISTRY.csv` as it stands

### 1.1 What was actually minted

`TOPIC_REGISTRY.csv` (the *topic structure*, the thing the operator means by "this I already minted") lives at `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv`. It carries **39 topic rows** across **18 columns**:

`topic_id, title, topic_class, lifecycle_status, primary_owner_role, program_id, plane, parent_topic, related_topics, depends_on, subsumes, subsumed_by, manifest_path, notes, last_review_at, last_review_by, last_review_decision_id, methodology_version_at_review`

The columns split into four functional groups:

- **Identity** — `topic_id` (regex `^topic_[a-z0-9_]{2,64}$`, must not collide with a `process_list.csv` `item_id`), `title`.
- **Classification** — `topic_class` (enum: `process_map | architecture | wireframe | methodology_map | manifesto | evidence_pack | brand_asset | other`), `lifecycle_status` (enum: `proposed | active | paused | closed | superseded`).
- **Edges** (the cross-topic graph) — `parent_topic` (single), `related_topics` / `depends_on` / `subsumes` / `subsumed_by` (semicolon lists).
- **Provenance / governance** — `primary_owner_role` (FK to `baseline_organisation.csv`), `program_id` (FK to `PROGRAM_REGISTRY.csv` or `shared`), `plane`, `manifest_path`, the four `last_review_*` review-stamp columns (added I71 P4, **D-IH-71-R**), `notes`.

### 1.2 What IS already governed (the key correction to "never governed")

The operator's framing — *minted but never governed* — is **only half true**, and the half that is true is the important half. Mechanically, the registry already satisfies most of the workspace's **`pattern_register_csv_pydantic_validator_mirror`** pattern:

| Governance leg | Status | Evidence |
|:---|:---|:---|
| Canonical CSV | ✅ present | `…/dimensions/TOPIC_REGISTRY.csv` (39 rows) |
| Fieldnames SSOT | ✅ present | `akos/hlk_topic_registry_csv.py` → `TOPIC_REGISTRY_FIELDNAMES` (18-tuple) |
| Validator | ✅ present **and wired** | `scripts/validate_topic_registry.py`, registered in `scripts/validate_hlk.py` (import L15; validator table L467–468) |
| Schema-drift gate | ✅ present | `scripts/validate_compliance_schema_drift.py` L90–92 (CSV path + module + tuple) |
| Supabase mirror | ✅ present | `supabase/migrations/20260429173828_i25_compliance_topic_registry_mirror.sql` → `compliance.topic_registry_mirror` (TEXT projection) |
| Graph projection | ✅ present | `scripts/render_topic_graph.py`; Neo4j `:DEPENDS_ON / :TOPIC_PARENT_OF / :RELATED_TO / :TOPIC_SUBSUMES / :UNDER_PROGRAM` |
| HCAM entity | ✅ present | `ENTITY_CATALOG.csv`: `topic,Topic,…/TOPIC_REGISTRY.csv,passive_structure,what,Topic,Research,active,"Knowledge topic; parent/child tree"` |
| Topic→Fact→Source contract | ✅ present | `HLK_KM_TOPIC_FACT_SOURCE.md` (topic→fact→source; manifest edges FK-resolve; drift = canonical wins) |
| Manifest FK enforcement | ✅ present | `validate_hlk_km_manifests.py` FK-resolves manifest `topic_ids:` into the registry |

So the registry is **not** an ungoverned sidecar. It has an SSOT tuple, a wired validator, a drift gate, a Postgres mirror, a Neo4j projection, an HCAM entity row, and a contract doc. **This is the single most important finding: the next move is not "build the chassis" — the chassis exists. The next move is to govern the *semantics, the lifecycle, and the corpus binding* that the chassis does not yet enforce.**

### 1.3 What is genuinely *ungoverned* today (why it still feels unfinished)

Six real gaps remain — none of them mechanical-chassis gaps:

1. **No row-level Pydantic enum model (confirm-item).** The SSOT today is a flat `FIELDNAMES` *tuple*, not a frozen Pydantic `BaseModel` with `topic_class` / `lifecycle_status` enum frozensets + `topic_id` regex + FK-column validators in the workspace's standard shape. Whether `validate_topic_registry.py` internally enforces those is **not verified in this bounded pass** (the validator script was outside the read set). First confirm-item before any schema work.

2. **Mono-dimensional classification.** `topic_class` is a small *enumerative* list, and in practice the 39 rows collapse into essentially **two** values — `methodology_map` and `evidence_pack`. The registry conflates three genuinely different *kinds* of subject under one axis: deliverable bundles (the 11 business-strategy artifacts), methodology/registry topics, and **research playlists** (rows 30–40). This is exactly the mono-dimensional-taxonomy smell that the faceted-classification literature flags as "intuitively a bad idea" [E2].

3. **11 stranded `proposed` rows.** Rows 30–40 (`topic_office_automation` … `topic_madeira_product_timeline`) were promoted from Trello on 2026-05-29 (**D-IH-75-G**) and have sat at `lifecycle_status=proposed` ever since — **no `manifest_path`, no `program_id`, no parent/related edges, no `TOPIC_KNOWLEDGE_INDEX`**. There is no promotion ladder or review cadence moving them forward. This is the APQC "content decay / no review timeline" failure mode [E5] and the NISO "orphan vocabulary" risk [E6].

4. **No working-corpus binding (the missing "occurrences").** `docs/wip/intelligence/` folders are **not keyed by `topic_id`**; the WIP `README.md` never references the registry. In ISO 13250 / Topic-Maps terms the registry has *topics* and *associations* but almost no *occurrences* — the links from a topic to the working artifacts that are "about" it [E1]. The registry therefore does not actually *index the corpus it exists to govern*.

5. **Ownership articulation gap.** The CSV physically lives under **People/Compliance** (its governance home), but the HCAM `topic` entity is owned by **Research**, and per-row `primary_owner_role` is scattered (PMO / CPO / Holistik Researcher / Compliance / Brand & Narrative Manager / Tech Lead / Product Owner). No single **steward of the vocabulary-as-a-vocabulary** is named — which both NISO/TDWG vocabulary-management practice [E6] and APQC taxonomy governance [E5] treat as the load-bearing role.

6. **Review-stamp / methodology-version drift.** Rows 2–29 are stamped `methodology_version_at_review = v3.0`; rows 30–40 are stamped `v3.2`. `last_review_at` clusters at two dates (2026-05-14 closure backfill, 2026-05-29 promotion). The review cadence is not actually running.

**Net:** the registry is a well-built chassis that was never *driven*. R2-07 is a **governance + curation + binding** problem, not a build problem.

---

## 2. Proposed governed schema (pattern_register_csv_pydantic_validator_mirror)

**Design stance:** do **not** break the existing chassis. The mirror, drift gate, and Neo4j projection all read the current 18-column tuple, so the proposal is **additive + facet-respecified**, not a rewrite. Three moves: (a) fix the mono-dimensional classification with **orthogonal facets** [E2]; (b) add the missing **occurrence-binding** columns so a topic points at its working corpus [E1]; (c) add a **steward** column so the vocabulary has a named owner [E6].

### 2.1 Column set — keep 18, re-specify 1, add 5

| Column | Action | Governed rule |
|:---|:---|:---|
| `topic_id` | keep | `^topic_[a-z0-9_]{2,64}$`; globally unique; must not collide with `process_list.csv item_id`; **subject-based, date-free** (the working folder may carry a date; the topic must not — subject identity is stable [E1]). |
| `title` | keep | non-empty; human-readable. |
| `topic_class` | **re-specify as the `subject_kind` facet** | enum tightened to orthogonal kinds: `deliverable_bundle \| methodology \| research_playlist \| engagement \| doctrine \| evidence_pack \| registry_anchor \| other`. `other` is allowed but **flagged** by the validator (faceted-classification caution against an overused catch-all [E2]). |
| `lifecycle_status` | keep (this is the **stage facet**) | `proposed \| active \| paused \| closed \| superseded`; **gated** (see 2.2 rule G). |
| `primary_owner_role` | keep | FK → `baseline_organisation.csv role_name`; this is the **subject-matter** owner (varies by topic). |
| **`steward_role`** | **ADD** | FK → `baseline_organisation.csv`; **default `KM Officer`**; the vocabulary steward (distinct from subject owner) — the NISO/TDWG "maintenance owner" who runs the cadence [E6]. |
| `program_id` | keep | FK → `PROGRAM_REGISTRY.csv` or `shared`. |
| `plane` | keep | enum per `compliance/README.md` planes. |
| `parent_topic` | keep (= SKOS `broader`) | single; FK → existing `topic_id`; **not transitive** [E4]. |
| `related_topics` | keep (= SKOS `related`) | `;`-list; each FK → existing `topic_id`. |
| `depends_on` | keep | `;`-list; FK → existing `topic_id`; **acyclic** (DAG; no `depends_on` cycle) [E2]. |
| `subsumes` / `subsumed_by` | keep | `;`-list; FK → existing `topic_id`; used on merge. |
| `manifest_path` | keep (= Output-1 occurrence) | resolves to an existing `_assets/<plane>/<program>/<topic_id>/…manifest.md` when non-null. |
| **`working_area_path`** | **ADD** (= the missing occurrence) | repo-relative path to the `docs/wip/intelligence/<slug>/` working area; resolves when non-null; the topic→corpus binding [E1]. |
| **`knowledge_index_path`** | **ADD** | path to the topic's `TOPIC_KNOWLEDGE_INDEX` md (the canonical entrypoint per the template); resolves when non-null. |
| **`physical_model`** | **ADD** | enum `keyed_in_place \| physically_moved`; records the §3 decision per topic (default `keyed_in_place`). |
| `notes` | keep | free-form. |
| `last_review_*` (×4) | keep | review-stamp cadence (D-IH-71-R); see rule H. |
| **`methodology_version_at_review`** | keep but normalize | single current version; drift between rows is itself a finding. |

> Sixth optional/forward column: **`subject_identifier`** (a stable URI-like string per ISO 13250 subject identity [E1]) — defer unless the Neo4j/KiRBe merge story needs it; `topic_id` is the de-facto subject identifier today.

### 2.2 Validation rules (the Pydantic + validator the chassis still needs)

Mint/confirm a frozen Pydantic `TopicRegistryRow` model (workspace standard, per `CONTRIBUTING.md`) enforcing:

- **A — enums** as frozensets: `subject_kind`, `lifecycle_status`, `plane`, `physical_model`.
- **B — id**: regex + uniqueness + no `item_id` collision.
- **C — FK resolution**: `primary_owner_role`, `steward_role` → baseline; `program_id` → program registry/`shared`.
- **D — edge integrity**: every `parent_topic` / `related_topics` / `depends_on` / `subsumes` / `subsumed_by` element FK-resolves to an existing `topic_id`; `depends_on` is acyclic; `parent_topic` non-transitive [E4].
- **E — path resolution**: `manifest_path`, `working_area_path`, `knowledge_index_path` resolve to existing repo paths when non-null.
- **F — facet orthogonality**: `subject_kind` and `lifecycle_status` are independent (a `research_playlist` may be `proposed` or `active`); `other` emits a soft finding.
- **G — lifecycle gate (the curation rule):** a row may be `active` **only if** it has *at least one occurrence* — i.e. a non-null `manifest_path` **or** (`working_area_path` **and** `knowledge_index_path`). This is what stops the 11 stranded rows from silently sitting at `proposed` forever, and it is the APQC "no active content without an owner + an artifact" discipline [E5].
- **H — review cadence**: `last_review_at` not older than the topic's cadence band; stamp consistency on `methodology_version_at_review`.

Wire the model into the **existing** `validate_topic_registry.py` (already in `validate_hlk.py`); the drift gate and mirror DDL get the 5 new columns via the standard add-column sync contract (`akos-docs-config-sync.mdc`).

### 2.3 Relationship to `HLK_KM_TOPIC_FACT_SOURCE` (topic → fact → source)

The registry is the **Topic** layer of the Topic→Fact→Source contract. The two added occurrence columns are precisely what makes the *Fact* and *Source* layers reachable from a topic row:

- `manifest_path` → the governed Output-1 **source** (visual + stub + sha).
- `working_area_path` → the `docs/wip/intelligence/<slug>/` **facts-in-progress** (syntheses, source ledgers, checkpoints) before promotion.
- `knowledge_index_path` → the `TOPIC_KNOWLEDGE_INDEX` that bundles source-synthesis + procedural + case + visual + registered-process anchors (the template's five layers).

In Topic-Maps terms [E1]: `topic_id` is the **topic**, the edge columns are the **associations**, and these three path columns are the **occurrences**. Today the occurrences are mostly empty — which is exactly why the structure "doesn't feel usable."

### 2.4 Relationship to HCAM (is `topic` an entity? yes — and it should articulate as a *dimension*)

`topic` **is already** a registered HCAM entity (`ENTITY_CATALOG.csv`: grain `Topic`, question `what`, owner `Research`, `passive_structure`, lifecycle `active`). The clean articulation is the **taxonomy-vs-ontology** split [E3]:

- **HCAM = the ontology / enterprise metamodel** (the I95/CAM semantic layer; `D-IH-95-A/C`). It defines entity classes, grains, and the relations between them.
- **`TOPIC_REGISTRY` = the governed taxonomy / SKOS-style concept scheme** [E4] that *populates* the `topic` dimension of that ontology. `parent_topic`/`related_topics`/`depends_on` are the SKOS `broader`/`related` semantic relations made concrete.

So the registry should **articulate up** into HCAM as the authoritative instance set for the `topic` entity (the mirror + Neo4j projection are the join surfaces), and **articulate down** into the Topic→Fact→Source contract as the Topic layer. It is the seam between the ontology (HCAM) and the corpus (`wip/intelligence`). Governance home stays **People/Compliance** (the canonical-CSV gate + `pattern_register_csv_pydantic_validator_mirror` are People-owned patterns), while **content ownership is Research** (Research Director accountable, KM Officer steward) — the People-authors-the-pattern / Research-owns-the-instance split from `akos-people-discipline-of-disciplines.mdc` RULE 1 + the Research charter.

---

## 3. Migration map — `docs/wip/intelligence/` → governed topics

### 3.1 Folder → topic mapping

The 17 top-level entries under `docs/wip/intelligence/` (one, `_templates`, is structural and not a topic) map as follows. "Registry status" is the crucial column: it shows whether a topic row already exists, must be minted, or was explicitly promised but never created.

| `wip/intelligence/` folder | Proposed `topic_id` | Topic name | `subject_kind` | Owning role (subject / steward) | Registry status |
|:---|:---|:---|:---|:---|:---|
| `2026-05-10-suez-webuy-procure-to-pay` | `topic_engagement_suez_webuy_p2p` | Suez/WeBuy procure-to-pay engagement | `engagement` | Lead Researcher / KM Officer | **new** |
| `agentic-os-and-aic-taxonomy-2026-05-29` | `topic_agentic_os_taxonomy` | Agentic-OS + AIC taxonomy | `doctrine` | System Owner / KM Officer | **new** |
| `area-completeness-doctrine-2026-06-05` | `topic_area_governance` | Area-governance/completeness doctrine | `doctrine` | People (Compliance) / KM Officer | **new** |
| `brand-domain-naming-2026-05-31` | `topic_brand_domain_naming` | Brand + domain naming | `research_playlist` | Brand & Narrative Manager / KM Officer | **new** |
| `canonical-articulation-model-2026-06-05` | `topic_canonical_articulation_model` | Canonical Articulation Model (I95/CAM) | `doctrine` | Data (Semantic Council) / KM Officer | **new** |
| `investor-briefs-2026-05-27` | `topic_investor_briefs` | Investor briefs | `deliverable_bundle` | PMO / KM Officer | **new** (relate → `topic_investment_thesis`) |
| `investor-stability-brief` | `topic_investor_stability_brief` | Investor stability brief | `deliverable_bundle` | Business Controller / KM Officer | **new** |
| `model-selection-2026-05-28` | `topic_model_selection` | Model-selection / routing | `methodology` | System Owner / KM Officer | **new** |
| `research-grounded-wave-r-plus-4-2026-05-27` | `topic_research_grounding` | Research-grounding (wave enrichment) | `methodology` | Research Director / KM Officer | **new** |
| `research-lifecycle-doctrine-2026-05-29` | `topic_research_lifecycle` | Research lifecycle doctrine | `doctrine` | Research Director / KM Officer | **new** |
| `research-radar-2026-05-29` | `topic_research_radar` | Research Radar (IntelligenceOps freshness) | `methodology` | Lead Researcher / KM Officer | **new** (ties → §4 register) |
| `substrate-audit-2026-Q2` | `topic_substrate_landscape` | Substrate landscape audit cadence | `methodology` | System Owner / KM Officer | **new** |
| `topic-ai-landscape-research` | `topic_ai_landscape_research` | AI landscape research | `research_playlist` | Holistik Researcher / KM Officer | **known-missing** |
| `topic-legal-research` | `topic_legal_research` | Legal research | `research_playlist` | Legal Counsel / KM Officer | **known-missing** |
| `topic-macro-investment-research` | `topic_macro_investment_research` | Macro/investment research | `research_playlist` | PMO / KM Officer | **known-missing** |
| `topic-madeira-research-radar` | `topic_madeira_research_radar` | MADEIRA research radar | `research_playlist` | Product Owner / KM Officer | **known-missing** (row 40 note already references it) |
| `topic-research-pipeline` | `topic_research_pipeline` | Research pipeline | `methodology` | Research Director / KM Officer | **known-missing** |

> `proposed` `topic_id`s above are recommendations, not commitments — naming is an inline-ratify item (§5). All inherit `steward_role = KM Officer` per §2.1 default.

### 3.2 The bidirectional drift (the real reason it feels broken)

The registry and the corpus evolved **independently**, producing drift in *both* directions:

- **Registry rows with NO working folder (10 of the 11 `proposed` playlists):** `topic_office_automation`, `topic_people_research`, `topic_security_intelligence`, `topic_design_research`, `topic_system_design_research`, `topic_content_channel_strategy`, `topic_politics_research`, `topic_social_research`, `topic_logic_research`, `topic_ux_crm_research`. These are Trello-promoted shells with no corpus behind them. (`topic_office_automation`'s note even promises a folder `docs/wip/intelligence/topic-office-automation/` that **does not exist**.)
- **`topic-*` working folders with NO registry row (5):** `topic-ai-landscape-research`, `topic-legal-research`, `topic-macro-investment-research`, `topic-madeira-research-radar`, `topic-research-pipeline`. Someone created `topic-`-prefixed working areas *expecting* a registry row that was never minted — `topic_madeira_product_timeline` (row 40) literally says its `related_topics` are "cleared until `topic_madeira_research_radar` registers."

**Migration is therefore a reconciliation, not a one-way import:** (a) bind every existing working folder to a `topic_id` (new or existing) via `working_area_path`; (b) decide, per stranded `proposed` row, whether to seed a working folder, fold it into a sibling, or close it; (c) mint the 5 known-missing rows so the `topic-*` folders stop being orphans.

### 3.3 Physical model — RECOMMENDATION: **key-by-`topic_id`, do NOT physically move**

Bind, don't move. Concretely: `docs/wip/intelligence/` **stays exactly where it is**; each folder gains a `topic_id:` in its README frontmatter, and the registry's new `working_area_path` column points back at the folder. The pairing is a bidirectional FK, not a relocation.

Rationale (doctrine-backed, not preference):

1. **Moving it is explicitly forbidden.** `akos-research-area.mdc` RULE 2 + its anti-patterns: *"Never move/rename `docs/wip/intelligence/` without a topology decision superseding D-IH-70-O"* and *"Proposing to physically move `docs/wip/intelligence/` (contradicts the ratified topology)"* is named as a known amnesia failure. The Research charter §5 makes Research the Tier-1 owner *in place*.
2. **It matches the occurrence model.** In ISO 13250 a topic's *occurrences* point at resources **wherever they live**; you reference the corpus, you don't ingest it into the taxonomy [E1]. `working_area_path` is exactly an occurrence pointer.
3. **It preserves the promotion ladder.** The existing Investigate→Propose→Ratify→Promote ladder (WIP README) already moves an artifact into a canonical home **at promotion only**, leaving a `_promoted/<date>-superseded-by-…` audit trail. A wholesale physical move would pre-empt that ladder and destroy the working/promoted distinction.
4. **It is reversible and low-blast-radius.** Adding a column + frontmatter key touches no paths, breaks no validator FK, and needs no migration of `_assets/` or mirror rows.

The one nuance to ratify (§5): research *playlists* (the proposed rows) may not warrant a `wip/intelligence/` folder at all until work starts — for those, `working_area_path` stays null and the lifecycle gate (rule G) keeps them at `proposed`, which is correct.

---

## 4. IntelligenceOps register landing in Research

### 4.1 What is already done

The `INTELLIGENCEOPS_REGISTER.csv` **already sits under Research** — `…/Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv` — i.e. under the **Intelligence discipline**. All four current rows confirm the Research wiring end-to-end:

- `responsible_role = Lead Researcher` (all 4 rows).
- `linked_sop_path = …/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md`.
- `linked_runbook_path = scripts/research_radar_sweep.py`.
- `intro_decision_id = D-IH-86-FG / D-IH-86-FH` (Wave R+5 radar mint).
- Freshness columns (`volatility_class / staleness_days / staleness_posture / next_verify_by`) present and wired to `akos-research-radar.mdc`.

So the **area-ownership leg of R2-07 is effectively closed**: the register is Research/Intelligence, executed by Lead Researcher, governed by the Research Radar discipline. The placement decision was ratified long ago (**D-IH-70-W** — IntelligenceOps placement under Research/Intelligence).

### 4.2 What remains for R2-07

Two items, one structural and one ownership:

1. **Legacy-tree → promoted-top-level path move (gated follow-up, deferred by design).** The register physically lives in the **legacy** `Admin/O5-1/Research/` sub-tree, not the **promoted top-level** `v3.0/Research/Intelligence/canonicals/` home that `RESEARCH_AREA_CHARTER` §4 created. The charter explicitly lists "the **IntelligenceOps register CSV**" under *"Still pending migration (separate gated follow-up, NOT husks)"* because it is an SSOT-CSV whose path change ripples into `PRECEDENCE.md` + validators + the `akos/…_csv.py` FIELDNAMES + the mirror-emit path. This is **deliberately gated**, not forgotten — it is a path-migration initiative of its own, parallel to the SUBSTRATE_LANDSCAPE_DOCTRINE + Methodology/Intelligence SOP moves named in the same charter paragraph. R2-07 should **confirm and schedule** it, not silently execute it.

2. **Confirm no Operations-owned maintenance process + activate the steward seat (confirm-item).** Not verified in this bounded pass (the `process_list.csv` / `OPS_REGISTER.csv` were outside the read set): whether any *register-maintenance* process row still carries `area = Operations` / an Operations owner. Note the **legitimate** Operations home — the operator-private CORPINT SOPs under `…/Operations/IntelligenceOps/` (created I66 P3) — which is a **deliberate dual-register home** (`akos-brand-baseline-reality.mdc`), *not* a mis-home. The thing to re-point (if it exists) is the **register-freshness maintenance process**, which is Research work.

### 4.3 Ownership — tie to round-2 §2 (Research Director accountable; KM Officer steward; NO new role)

Round-2 synthesis §2 is unambiguous and should be the RACI for *both* registers in this initiative:

| RACI | Seat | Source |
|:---|:---|:---|
| **Accountable** | **Research Director** | round2 §2 ("Research Director accountable"); `RESEARCH_AREA_CHARTER` §3 |
| **Steward / curation** | **KM Officer** (activate the dormant seat) | round2 §2 ("activate the dormant KM Officer seat"); charter §3 ("KM Officer … owns Tier 1 WIP curation") |
| **Execute (quality + methodology)** | **Lead Researcher** | round2 §2; register `responsible_role` |
| **Truth-gate** | **Research / Validation** | round2 §2 ("Research/Validation is the truth-gate") |
| **NOT** | a new "Knowledge Manager" title | round2 §2 (re-fuses what should stay split) |

The convergence worth naming: **the KM Officer seat is the single steward across three surfaces** — (a) the `TOPIC_REGISTRY` (`steward_role` default, §2.1), (b) the `INTELLIGENCEOPS_REGISTER` freshness cadence, and (c) the `docs/wip/intelligence/` Tier-1 WIP curation (charter §5). Activating that one dormant seat closes the steward gap for the entire L5 topic surface at once — and it does so *without* the People-relegation failure mode round2 §2 warns against (sellable-CI-quality is a Research/Validation competence because, per the CNAE + ENISA identity, **intelligence is the product**).

---

## 5. Resurface to operator — sub-decisions needing ratification

Seven inline-ratify gates (`gate_type: inline-ratify` per `akos-inline-ratification.mdc`). Each carries options + a recommended default with a one-clause reason + evidence. They are tightly coupled (all concern the same L5 topic surface), so they are batched into two `AskQuestion` rounds: **Round A = D1–D4 (design)**, **Round B = D5–D7 (execution/gate)**.

### R2-07-D1 — Physical model of the corpus
*Does `docs/wip/intelligence/` physically move into a topic-keyed tree, or stay in place and bind by `topic_id`?*
- **(A) Key-by-`topic_id`, no move** *(recommended — `akos-research-area.mdc` RULE 2 forbids moving the Tier-1 home; matches the ISO-13250 occurrence model [E1])*.
- (B) Physically move folders under a `topic_*/` tree (requires a topology decision superseding D-IH-70-O).
- (C) Hybrid: keep working WIP in place, but relocate *promoted* artifacts into a topic-keyed canonical tree (this is roughly the status-quo promotion ladder).

### R2-07-D2 — Taxonomy depth / facet model
*Adopt the orthogonal facet split, keep the single `topic_class`, or go to a full ontology?*
- **(A) Orthogonal facets, additive** — re-spec `topic_class`→`subject_kind`, add `working_area_path` / `knowledge_index_path` / `steward_role` / `physical_model` *(recommended — fixes the mono-dimensional smell [E2] without breaking the chassis)*.
- (B) Keep the single `topic_class` enum (status quo; cheapest; leaves the conflation).
- (C) Promote to a full OWL-style ontology now (rejected for now — taxonomy-with-rich-concepts is sufficient; "add an ontology later" [E3]).

### R2-07-D3 — HCAM articulation direction
*How does the registry relate to the HCAM metamodel?*
- **(A) Registry = governed taxonomy / SKOS concept scheme that POPULATES the HCAM `topic` dimension** *(recommended — `topic` is already an `ENTITY_CATALOG` entity owned by Research; this is the clean taxonomy-vs-ontology seam [E3][E4])*.
- (B) Fold the registry's semantics up into HCAM entities (heavier; blurs the dimension/ontology boundary).
- (C) Leave them unrelated (rejected — leaves the `passive_structure` entity row dangling).

### R2-07-D4 — Steward seat
*Who owns the topic vocabulary as a vocabulary?*
- **(A) Activate the dormant KM Officer seat as steward across the topic registry + IntelligenceOps register + Tier-1 WIP; Research Director accountable; Lead Researcher executes; no new role** *(recommended — verbatim round-2 §2 + charter §3; closes all three steward gaps at once)*.
- (B) Keep stewardship implicit on PMO/per-row owners (status quo; leaves the cadence un-run).
- (C) Mint a new "Knowledge Manager" role (rejected by round-2 §2 — re-fuses what should stay split [E5]).

### R2-07-D5 — Disposition of the 11 stranded `proposed` rows
*What happens to the Trello-promoted playlists with no corpus?*
- **(A) Apply the lifecycle gate (rule G) + KM Officer triages each at first review: seed a `working_area_path`, fold into a sibling, or flip to `paused`/`closed`** *(recommended — APQC review-cadence + ruthless-curation discipline [E5]; stops orphan-vocabulary decay [E6])*.
- (B) Bulk-activate them all (rejected — activates shells with no occurrences).
- (C) Bulk-close them all (too blunt; some are real future research areas).

### R2-07-D6 — Mint the 5 known-missing rows + ratify the `topic_id` names
*Register the 5 orphan `topic-*` working folders, and approve the §3.1 `topic_id` names?*
- **(A) Mint all 5 (`topic_ai_landscape_research`, `topic_legal_research`, `topic_macro_investment_research`, `topic_madeira_research_radar`, `topic_research_pipeline`) with the §3.1 names** *(recommended — ends the bidirectional drift; row 40 already references `topic_madeira_research_radar`)*.
- (B) Mint a subset (operator names which).
- (C) Rename any `topic_id` before minting (operator supplies corrections — names are date-free + subject-based per §2.1).

### R2-07-D7 — Canonical-CSV tranche scope + gate
*This touches a canonical dimension CSV (+5 columns, +5–16 rows) → mandatory operator approval gate.*
- **(A) Two tranches: (1) schema tranche — add 5 columns + Pydantic model + mirror DDL + drift-registry + `validate_hlk` + USER_GUIDE/ARCHITECTURE sync; then (2) data tranche — reconcile bindings + mint missing rows + disposition stranded rows** *(recommended — separates reversible schema from judgement-heavy data; each gets its own `validate_hlk` gate per `akos-baseline-governance.mdc` + `akos-holistika-operations.mdc`)*.
- (B) One combined tranche (faster; larger blast radius; harder to review).
- (C) Schema-only now, defer all data reconciliation to a successor initiative.

> **Out of scope for this readonly doc:** no CSV/column/mirror edits were made; D7's tranches require the operator-approval gate before any canonical edit.

---

## Citations

### Internal (workspace)

*The minted structure & its chassis*
- [I1] `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv` — the minted topic structure (39 rows, 18 cols).
- [I2] `akos/hlk_topic_registry_csv.py` — `TOPIC_REGISTRY_FIELDNAMES` SSOT tuple + enum docstring.
- [I3] Existing governance legs — `scripts/validate_topic_registry.py` (wired in `scripts/validate_hlk.py` L15 + L467–468); `scripts/validate_compliance_schema_drift.py` L90–92; `supabase/migrations/20260429173828_i25_compliance_topic_registry_mirror.sql`; `scripts/render_topic_graph.py`.

*The contracts it plugs into*
- [I4] `…/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md` — Topic→Fact→Source contract (`topic_id` regex; manifest FK-resolution; drift = canonical wins).
- [I5] `…/Compliance/TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md` — canonical topic entrypoint (5 bundle layers).
- [I6] `…/Data/Architecture/canonicals/dimensions/ENTITY_CATALOG.csv` row `topic` — HCAM entity (grain `Topic`, question `what`, owner Research, `passive_structure`).

*Research home & ownership*
- [I7] `…/Research/canonicals/RESEARCH_AREA_CHARTER.md` §3 (roles incl. KM Officer), §4 (register migration pending), §5 (Tier-1 ownership); D-IH-70-S / D-IH-70-W.
- [I8] `docs/wip/intelligence/canonical-articulation-model-2026-06-05/round2-research-synthesis-2026-06-06.md` §2 — KM 3-way split; activate KM Officer; Research/Validation truth-gate; no new role.
- [I9] `…/Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv` — Research/Intelligence home; `responsible_role = Lead Researcher`; D-IH-86-FG/FH; radar SOP + runbook.
- [I10] `.cursor/rules/akos-research-area.mdc` RULE 2 + anti-patterns (do not move `wip/intelligence/`; D-IH-70-O) · `.cursor/rules/akos-people-discipline-of-disciplines.mdc` RULE 1 (People owns the *pattern*; areas own the *instance*).

### External (web)

*Topic / subject modeling*
- [E1] ISO/IEC 13250 Topic Maps — TAO model (Topics, Associations, **Occurrences**) + subject identity: Pepper, "The TAO of Topic Maps" <https://ontopia.net/topicmaps/materials/tao.html>; ISO/IEC 13250-2 Data Model <http://www.jtc1sc34.org/repository/0696.pdf>.

*Classification structure*
- [E2] Faceted classification / Ranganathan — orthogonal facets, the mono-dimensional anti-pattern, the "Other" caution: *The Discipline of Organizing* (Berkeley) <https://berkeley.pressbooks.pub/tdo4p/chapter/faceted-classification/>; ISKO, "Facet analysis" <https://www.isko.org/cyclo/facet_analysis.htm>.
- [E3] Taxonomy vs ontology (NISO Z39.19 taxonomy definition; navigation vs reasoning; "add an ontology later"): Access Innovations <https://www.accessinn.com/part-1-taxonomy-thesaurus-or-ontology/>; Hedden Information Management <https://www.hedden-information.com/taxonomy-benefits-over-an-ontology/>.
- [E4] W3C SKOS — concept scheme; `skos:broader`/`narrower`/`related`; broader is **non-transitive**: SKOS Reference <https://www.w3.org/TR/2009/REC-skos-reference-20090818/>; SKOS Primer <https://www.w3.org/2006/07/SWD/SKOS/primer/primer-20090427.html>.

*Curation lifecycle & stewardship*
- [E5] APQC — KM governance + content lifecycle (standard workflows creation→archival; taxonomy owners + category stewards; review timelines + escalation; ruthless curation): "Establishing Governance for KM" <https://www.apqc.org/resource-library/resource-listing/establishing-governance-knowledge-management>; "Better Content Management…" <https://www.apqc.org/blog/better-content-management-demands-hard-work-behavior-change>.
- [E6] Controlled-vocabulary maintenance & steward model — ANSI/NISO Z39.19 (construction/maintenance/management) <https://www.niso.org/publications/ansiniso-z3919-2005-r2010>; NISO Vocabulary Management (use/reuse, versioning, **orphan vocabularies**) <https://www.niso.org/standards-committees/vocab-mgmt>; TDWG vocabulary maintenance specification (maintenance Interest Group / steward) <https://github.com/tdwg/vocab/blob/master/vms/maintenance-specification.md>.
