---
language: en
---

# L5b — Scattered-Topic Reconciliation Inventory (R2-07 expansion)

> **Initiative:** Canonical Articulation Model (CAM / I95) — Layer 5b (repo-wide topic reconciliation)
> **Operator ask (R2-07 expansion, ratified `D-IH-95-H`):** bring ALL "scattered topics" across the repo into `TOPIC_REGISTRY.csv` so the company's intelligence is fully governed. This doc is the **complete reconciliation inventory** of every topic-like artifact in the repo, so a follow-up tranche can mint/bind the missing ones.
> **Author:** MADEIRA inventory agent · **Date:** 2026-06-07
> **Mode:** Readonly + this ONE doc write. No CSV edits, no file moves.
> **Scope guard:** Internal repo only; ZERO web searches; bounded Glob/Grep discovery (no deep folder reads — each topic identified from path + manifest/README frontmatter only). A prior sibling agent died from over-broad scope; this run stays bounded.
> **Relationship to L5:** [`l5-topic-structure-findings-2026-06-07.md`](l5-topic-structure-findings-2026-06-07.md) already mapped the **17 `docs/wip/intelligence/` folders** + named the governed schema. This doc does **not** repeat that — it **extends** the reconciliation to the rest of the repo (`_assets/` manifest-folder topics, km-pilot, techops, topic-* outside wip/intelligence, and topic_ids referenced in manifests but absent from the registry).

---

## 1. METHOD + scope

### 1.1 Grounding read set (only these three, per the L5 contract)
- `TOPIC_REGISTRY.csv` — the **39 existing rows** (baseline; anything not here is a candidate).
- `l5-topic-structure-findings-2026-06-07.md` — the L5 design (already mapped the 17 `wip/intelligence/` folders; schema named).
- `HLK_KM_TOPIC_FACT_SOURCE.md` — the Topic→Fact→Source contract (defines what a governed topic needs: `topic_id` regex `^topic_[a-z0-9_]{2,64}$`, primary_owner_role FK, manifest/occurrence).

### 1.2 Discovery sweeps (bounded Glob + Grep only)

| # | Sweep | Pattern | Result |
|:--|:---|:---|:---|
| 1 | Manifest-folder topics | Glob `_assets/**/topic_*.manifest.md` | **3** manifests (all 3 already in registry) |
| 2 | Topic-prefixed md/csv | Glob `**/topic_*.md`, `**/topic_*.csv` | 8 md (incl. 2 uppercase `TOPIC_*.md`: 1 template + 1 PMO hub) + 1 csv (the registry itself) |
| 3 | KM pilot bundle | Glob `_assets/km-pilot/**` | **8** `VISUAL_km_pilot_*` manifests + assets → all bind `topic_km_governance` |
| 4 | Manifest topic references | Grep `topic_ids:` in `_assets/` | **9** distinct `topic_id`s referenced across manifests + deliverables |
| 5 | Self-declared topic ids | Grep `topic_id(**)?:` in `v3.0/` | 5 declarations (3 governed + 1 template placeholder + 1 orphan PMO hub) |
| 6 | Hyphenated topic folders | Glob `**/topic-*/**` | **5** folders — **all inside `docs/wip/intelligence/`** (L5-covered; none elsewhere) |
| 7 | Registry baseline | Grep `^topic_` in `TOPIC_REGISTRY.csv` | **39** existing ids (cross-check list in §1.3) |
| 8 | Full manifest inventory | Glob `_assets/**/*.manifest.md` | **16** manifests total (3 topic + 8 km-pilot + 5 SOP) — fully accounted |

**Scope note:** the 17 `docs/wip/intelligence/` folders are intentionally NOT re-tabled here — they are L5's deliverable ([`l5-topic-structure-findings`](l5-topic-structure-findings-2026-06-07.md) §3.1). This doc covers everything *else* (the `_assets/` plane topics, km-pilot, techops/pmo SOP manifests, the ENISA dossier bundles, and the PMO hub) + the orphan `topic_id`s referenced anywhere but absent from the registry.

### 1.3 The 39 existing registry ids (cross-check baseline)

`topic_external_adviser_handoff`, `topic_kirbe_billing_plane_routing`, `topic_enisa_evidence`, `topic_km_governance`, `topic_enisa_dossier_es`, `topic_business_strategy`, `topic_market_thesis`, `topic_competitive_landscape`, `topic_pricing_model`, `topic_channel_strategy`, `topic_sales_motion`, `topic_unit_economics`, `topic_bootstrapping_plan`, `topic_investment_thesis`, `topic_strategy_decisions`, `topic_poc_commercial_map`, `topic_brand_visual_identity`, `topic_madeira_platform`, `topic_governance_moat`, `topic_persona_registry`, `topic_channel_touchpoint_registry`, `topic_sourcing_register`, `topic_holistik_ops_discovery`, `topic_skill_registry`, `topic_touchpoint_kit_cell_registry`, `topic_policy_register`, `topic_repo_health_snapshot`, `topic_persona_scenario_registry`, `topic_office_automation`, `topic_people_research`, `topic_security_intelligence`, `topic_design_research`, `topic_system_design_research`, `topic_content_channel_strategy`, `topic_politics_research`, `topic_social_research`, `topic_logic_research`, `topic_ux_crm_research`, `topic_madeira_product_timeline`.

---

## 2. Master reconciliation TABLE

One row per discovered topic-like artifact **outside** the 17 `wip/intelligence/` folders L5 already handled. `subject_kind` uses the L5 facet enum (`deliverable_bundle / methodology / research_playlist / engagement / doctrine / evidence_pack / registry_anchor / other`). Default steward = **KM Officer** (per L5 §2.1 + `akos-research-area.mdc` RULE 3); subject owner varies.

### 2a. `_assets/` plane topics (the manifest-folder + dossier-bundle surface)

| source location | proposed/actual topic_id | inferred title | subject_kind | in registry? | recommended disposition | owner / steward |
|:---|:---|:---|:---|:---:|:---|:---|
| `_assets/advops/2026-holistika-incorporation/adviser_handoff/` (`topic_*.manifest.md` + `.md`/`.mmd`/`.svg`) | `topic_external_adviser_handoff` | External Adviser Engagement | engagement | **Y** (row 1) | **bind** — already bound (manifest_path set); add `working_area_path` if any | PMO / KM Officer |
| `_assets/advops/2026-holistika-incorporation/enisa_evidence/` (`topic_*.manifest.md` + `.md`/`.mmd`) | `topic_enisa_evidence` | ENISA evidence pack | evidence_pack | **Y** (row 4) | **bind** — already bound | Compliance / KM Officer |
| `_assets/advops/2026-holistika-incorporation/enisa_evidence/dossier_es.md` (+ `cover_email_es.md`) | `topic_enisa_dossier_es` | ENISA dossier (Spanish founder dossier) | evidence_pack | **Y** (row 6) | **bind** — already bound (frontmatter doubles as manifest) | Compliance / KM Officer |
| `_assets/advops/2026-holistika-incorporation/enisa_company_dossier/` (`deck_slides.yaml`, `deck_story_es.md`, `cover_email_company_dossier_es.md`, `deck-visual-system.md`, `mail-render.md`, `figma-link.md`) | `topic_enisa_company_dossier` | ENISA company dossier (deck + cover + Figma bundle) | deliverable_bundle | **N** ❌ | **MINT NEW ROW** — `parent_topic=topic_enisa_evidence`, relate→`topic_enisa_dossier_es`; OR fold into `topic_enisa_dossier_es` if operator deems same deliverable | Compliance (or PMO) / KM Officer |
| `_assets/techops/PRJ-HOL-KIR-2026/topic_kirbe_billing_plane_routing/` (`topic_*.manifest.md` + `.md`/`.svg`) | `topic_kirbe_billing_plane_routing` | KiRBe billing-plane routing | other (architecture) | **Y** (row 2) | **bind** — already bound | System Owner / KM Officer |
| `_assets/techops/SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.manifest.md`, `SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.manifest.md`, `SOP-EXTERNAL_REPO_BLESSING_001.manifest.md` (3) | `topic_holistik_ops_discovery` | (occurrences of) Holistik Ops Discovery | methodology | **Y** (row 23) | **bind** — manifests are occurrences of an existing topic; no new row | System Owner / KM Officer |
| `_assets/pmo/SOP-INITIATIVE_GOVERNANCE_001.manifest.md`, `SOP-INITIATIVE_PROCESS_HARMONISATION_001.manifest.md` (2) | `topic_holistik_ops_discovery` | (occurrences of) Holistik Ops Discovery | methodology | **Y** (row 23) | **bind** — occurrences; no new row | PMO / KM Officer |
| `_assets/advops/2026-holistika-incorporation/enisa_company_dossier/deck-visual-system.md` (2nd topic_id) | `topic_brand_visual_identity` | (occurrence of) Brand visual identity | methodology | **Y** (row 17) | **bind** — cross-reference occurrence; no new row | Brand & Narrative Manager / KM Officer |

### 2b. KM pilot bundle (grandfathered layout)

| source location | proposed/actual topic_id | inferred title | subject_kind | in registry? | recommended disposition | owner / steward |
|:---|:---|:---|:---|:---:|:---|:---|
| `_assets/km-pilot/VISUAL_km_pilot_001..008.manifest.md` (8 manifests) + `README.md` | `topic_km_governance` | Knowledge Management governance (pilot bundle) | methodology | **Y** (row 5) | **bind** — 1 topic / 8 occurrences; already governed (manifest_path = VISUAL_km_pilot_001) | Holistik Researcher / KM Officer |

### 2c. Self-declared topic hubs outside `_assets/`

| source location | proposed/actual topic_id | inferred title | subject_kind | in registry? | recommended disposition | owner / steward |
|:---|:---|:---|:---|:---:|:---|:---|
| `Admin/O5-1/Operations/PMO/canonicals/TOPIC_PMO_CLIENT_DELIVERY_HUB.md` (frontmatter `**topic_id**: topic_pmo_client_delivery_hub`, Status: Draft v0.2) | `topic_pmo_client_delivery_hub` | PMO client delivery hub (topic knowledge index / portfolio SSOT) | registry_anchor | **N** ❌ | **MINT NEW ROW** — `knowledge_index_path` = this file; it is already a canonical TOPIC_KNOWLEDGE_INDEX-style hub; promote Draft→active on mint | PMO / KM Officer |
| `Admin/O5-1/People/Compliance/TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md` (frontmatter `topic_<stable_slug>` placeholder) | — (template) | Topic Knowledge Index TEMPLATE | n/a | **N** (n/a) | **close / not a topic** — this is the template all topic hubs instantiate; never gets a registry row | People (Compliance) / — |

### 2d. Hyphenated `topic-*/` working folders (L5-covered — reference only, NOT re-tabled)

All 5 hyphenated `topic-*` folders live under `docs/wip/intelligence/` and are the **known-missing** rows already inventoried in [`l5-topic-structure-findings`](l5-topic-structure-findings-2026-06-07.md) §3.1 + ratify gate **R2-07-D6**: `topic_ai_landscape_research`, `topic_legal_research`, `topic_macro_investment_research`, `topic_madeira_research_radar`, `topic_research_pipeline`. **No hyphenated topic folder exists anywhere else in the repo.** Disposition: **mint per L5 D6** (not re-counted as new findings of *this* doc).

---

## 3. SUMMARY counts

**This doc's scope (repo-wide, EXCLUDING the 17 `wip/intelligence/` folders L5 handled):**

| Metric | Count | Detail |
|:---|:---:|:---|
| Distinct `topic_id`s touched across `_assets/` + vault | **9** | 7 governed + 2 orphan |
| …already governed (in `TOPIC_REGISTRY.csv`) | **7** | `topic_external_adviser_handoff`, `topic_enisa_evidence`, `topic_enisa_dossier_es`, `topic_kirbe_billing_plane_routing`, `topic_km_governance`, `topic_holistik_ops_discovery`, `topic_brand_visual_identity` |
| **…NEW rows to mint (orphans surfaced by THIS doc)** | **2** | `topic_enisa_company_dossier`, `topic_pmo_client_delivery_hub` |
| Manifest/occurrence artifacts bound to existing topics | **21** | km-pilot ×8 → `topic_km_governance`; SOP manifests ×5 → `topic_holistik_ops_discovery`; enisa_company_dossier bundle ×6 → (new) `topic_enisa_company_dossier`; deck-visual-system cross-ref ×1 → `topic_brand_visual_identity`; +1 PMO hub self-index |
| Templates (never a topic row) | **1** | `TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md` |
| Hyphenated `topic-*` folders outside `wip/intelligence/` | **0** | all 5 are inside `wip/intelligence/` (L5 §3.1) |

**Combined repo-wide reconciliation (this doc + L5):**

| Bucket | New rows to mint |
|:---|:---:|
| L5 — `wip/intelligence/` (12 net-new + 5 known-missing `topic-*`) | **17** |
| **L5b — this doc (2 orphans)** | **2** |
| **TOTAL new topic rows to mint** | **19** |

After the two tranches, the registry grows **39 → 58 rows** (39 existing + 19 new), at which point every topic-like artifact in the repo is bound to a governed row.

> **Naming-collision / date-stamp audit:** **0 violations.** All proposed `topic_id`s are subject-based and date-free (the rule from L5 §2.1 / `HLK_KM_TOPIC_FACT_SOURCE` regex `^topic_[a-z0-9_]{2,64}$`). Working folders carry dates (`2026-holistika-incorporation`, `…-2026-06-05`) but the `topic_id`s do not. No two distinct subjects collide on one id — though see RISK-1 (`topic_enisa_company_dossier` vs `topic_enisa_dossier_es` are *near-neighbours* by name, not a collision).

---

## 4. RISKS / notes

- **RISK-1 — orphan manifest `topic_enisa_company_dossier` (mint vs fold; needs operator input).** Referenced as a `topic_id` in **4 files** (`deck_story_es.md`, `cover_email_company_dossier_es.md`, `deck-visual-system.md`, `figma-link.md`) all under `_assets/advops/2026-holistika-incorporation/enisa_company_dossier/`, with `parent_topic: topic_enisa_evidence` — but **no registry row and no `topic_*.manifest.md`** for it. It sits beside the *registered* `topic_enisa_dossier_es` (row 6). The folder is a full deliverable bundle (deck slides YAML + ES deck story + cover email + Figma link + visual system + mail render). **Recommend: mint as a distinct `deliverable_bundle`** (a *company* dossier deck is a different artifact from the *Spanish founder* dossier), child of `topic_enisa_evidence`, related to `topic_enisa_dossier_es`. **Operator to confirm** it is not meant to fold into `topic_enisa_dossier_es`. This is the one true "orphan manifest" (topic_id referenced with no row) per the brief's RISK ask.

- **RISK-2 — `topic_pmo_client_delivery_hub` self-declares but is unregistered + Draft.** `TOPIC_PMO_CLIENT_DELIVERY_HUB.md` carries `**topic_id**: topic_pmo_client_delivery_hub` and `Status: Draft (v0.2, 2026-04-15)` and already behaves as a canonical TOPIC_KNOWLEDGE_INDEX (portfolio SSOT entrypoint), yet has no registry row. **Recommend: mint as `registry_anchor`**, set `knowledge_index_path` to this file, and promote Draft→active on mint. **Operator to confirm** governing-now vs leaving as pilot draft.

- **NOTE-3 — `_assets/` is otherwise clean.** All 16 manifests resolve: the **3** `topic_*.manifest.md` folders, the **8** km-pilot manifests (→ `topic_km_governance`), and the **5** SOP manifests (→ `topic_holistik_ops_discovery`) all FK-resolve to existing registry rows. No drift, no dangling manifest `topic_ids:` other than the two orphans above.

- **NOTE-4 — km-pilot is a bundle, not 8 topics.** The 8 `VISUAL_km_pilot_*` manifests are **occurrences** of one topic (`topic_km_governance`, row 5), not eight topics. Do **not** mint per-visual rows — that would inflate the registry and break the L5 occurrence model.

- **NOTE-5 — SOP manifests are occurrences, not topics.** The 5 techops/pmo `SOP-*.manifest.md` files bind to `topic_holistik_ops_discovery`; they are Output-1 occurrences. No new rows.

- **NOTE-6 — no double-counting with L5.** The 5 hyphenated `topic-*` folders and the 12 net-new `wip/intelligence/` topics are **L5's** deliverable; this doc references them (§2d) so the follow-up tranche sees the full 19-row picture, but counts only its own **2** orphans as net-new findings.

- **AMBIGUITY-7 (low) — `subject_kind` of the two ENISA dossiers + the PMO hub.** L5's `subject_kind` facet is proposed, not yet ratified (L5 ratify gate R2-07-D2). The recommendations here (`deliverable_bundle` for the company dossier, `registry_anchor` for the PMO hub) assume the facet lands; if the operator keeps the legacy single `topic_class`, map `deliverable_bundle`→`evidence_pack` and `registry_anchor`→`methodology_map` respectively.

---

### Handoff

This inventory is **readonly + single-doc**: no CSV edits, no file moves. The follow-up **data tranche** (L5 ratify gate **R2-07-D7** option A) should mint the **2** orphan rows here alongside L5's **17**, under the canonical-CSV operator-approval gate (`akos-baseline-governance.mdc` + `akos-holistika-operations.mdc`), with `py scripts/validate_hlk.py` in the verification matrix.
