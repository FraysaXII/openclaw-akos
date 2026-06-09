# Universal Canonical Governance Charter

**Initiative:** INIT-OPENCLAW_AKOS-95 (governance overlay)  
**Date:** 2026-06-09  
**Authoring seat:** Thinking (readonly planner)  
**Operator ratification:** Option B — Tiered two-plane governance (binding)  
**Target save path:** `docs/wip/planning/95-canonical-articulation-model/reports/universal-canonical-governance-charter-2026-06-09.md`

---

## 1. Executive intent

Holistika has **73 vault CSVs**[^gov1-inventory] spread across nine O5-1 areas, but governance today is **implicit and Compliance-centric**: Plane 1 (git CSV + the HLK validator umbrella) covers many sibling-area CSVs only because `validate_hlk.py` dispatches per-file validators — not because every canonical is indexed, classified, and wired consistently. Plane 2 (Supabase mirror sync) is **hardcoded** to the People/Compliance folder path in CI and in `validate_mirror_emit_contract.py`, even though mirrors exist (or are forward-chartered) for assets outside that folder.

**Option B (operator-ratified)** establishes:

| Plane | Scope | Mechanism |
|:---|:---|:---|
| **Plane 1 — Universal** | **Every** vault CSV under `docs/references/hlk/v3.0/**/canonicals/**/*.csv` | Git SSOT + dedicated validator (or umbrella validator with explicit CSV gate) + `validate_hlk.py` dispatch + PRECEDENCE + CANONICAL_REGISTRY row |
| **Plane 2 — Explicit** | **Only** assets with mirror DDL **and** `mirror_sync_policy=active` in the new governance registry | Registry-driven emit path + `supabase-mirror-sync.yml` path filters + enum parity + delete-reconcile |
| **T3 — Graph projection** | HCAM articulation registries (`ENTITY_CATALOG`, `CANONICAL_RELATIONSHIP_REGISTRY`) | T1 git CSV + Neo4j projection via `sync_hlk_neo4j.py`; **not** compliance mirror unless operator ratifies later |

**Big-bang end state, thinking-first execution:** All 73 vault CSVs land in a single governance registry with correct `asset_class`, Plane-1 validator wiring, and Plane-2 posture (active / forward-charter / git-only / graph-projection). Mechanical rollout follows registry mint → index backfill → workflow refactor → mirror-emit gap closure (DDL-gated) → regression proof.

[^gov1-inventory]: **GOV-1 inventory @ 2026-06-09:** Filesystem SSOT is **73** CSVs under `docs/references/hlk/v3.0/**/canonicals/**/*.csv` (see [`synthesis-p95-gov-1-2026-06-09.md`](synthesis-p95-gov-1-2026-06-09.md)). The prior **74** figure was a planning estimate (likely counted `CANONICAL_GOVERNANCE_REGISTRY.csv` as an extra vault asset; the meta-registry is governance inventory, not an additional content CSV). Hygiene B ratified 2026-06-09 per [`i95-hygiene-research-2026-06-09.md`](i95-hygiene-research-2026-06-09.md).

**Non-goals (this charter):** Moving CSVs between folders (I94 placement work); minting new mirror DDL for forward-charter assets without operator SQL gate; collapsing HCAM into compliance mirrors without a separate ratification.

---

## 2. Asset inventory matrix

**Legend**

- **Plane-1 gate:** Primary `validate_hlk.py` dispatch label (or `release-gate` if not in HLK umbrella).
- **Plane-2 today:** `active` = emit + DDL exists; `partial` = DDL exists, emit missing; `gap-splice` = OPS-86-15 gap path only; `none` = no mirror; `forward-charter` = PRECEDENCE/doc declares mirror later; `n/a` = graph/git-only by design.
- **Plane-2 target (Option B):** Registry-driven explicit posture.
- **PREC:** Row in `PRECEDENCE.md` prose table (Y/N).

### 2.1 Summary by area

| Area | CSV count | Plane-1 coverage | Mirror DDL | Emit wired | Index gaps |
|:---|:---:|:---|:---:|:---:|:---|
| People/Compliance | 42 | Strong (core + dimensions) | ~35 tables | Main + gap-splice | CANONICAL_REGISTRY meta; some dimensions partial |
| People/People Operations | 6 | Strong (umbrella CS) | 6 tables | CS separate flag; EM in main | CS siblings not all in CANONICAL_REGISTRY |
| People/Learning | 1 | **None** (deferred) | none | none | **Not in PRECEDENCE or CANONICAL_REGISTRY** |
| Data/Architecture | 4 | Strong (HCAM + metrics + supabase module) | none | n/a | **HCAM pair missing from PRECEDENCE + CANONICAL_REGISTRY** |
| Data/Governance | 4 | Strong | none (RPA: **partial DDL missing**) | none | DATA_CONTRACT forward-charter noted |
| Finance/Governance | 3 | Strong | none | none | **Not in PRECEDENCE** |
| Marketing/Reach + Experimentation | 5 | Umbrella `ADAPTER_REGISTRIES` | 8 of 9 adapter mirrors | **partial — no emit for any adapter** | Reach 4 Y; Attribution Y |
| Operations/RevOps | 3 | Strong | 3 tables | **partial — template mirror, no emit** | Y |
| Operations/SMO | 2 | Partial (adapters Y; catalog **no validator**) | 1 adapter mirror | **partial** | CONTRACT Y; **SERVICE_CATALOG not indexed** |
| Research/Intelligence | 1 | Strong | Y | main path | Y |
| Envoy Tech Lab (Admin + root) | 3 | Mixed (rendering in HLK; MADEIRA release-gate only) | none | none | MADEIRA partial PREC; rendering in CANONICAL_REGISTRY only |

### 2.2 People/Compliance (42 CSVs)

| Path (relative to `.../People/Compliance/canonicals/`) | asset_class | Plane-1 gate | P2 today | P2 target | PREC |
|:---|:---|:---|:---|:---|:---:|
| `baseline_organisation.csv` | compliance_mirror | inline + `MIRROR_EMIT_CONTRACT` | active | active | Y |
| `process_list.csv` | compliance_mirror | inline + `MIRROR_EMIT_CONTRACT` | active | active | Y |
| `DECISION_REGISTER.csv` | compliance_mirror | `DECISION_REGISTER` + alignment | active | active | Y |
| `INITIATIVE_REGISTRY.csv` | compliance_mirror | `INITIATIVE_REGISTRY` + sync gates | active | active | Y |
| `OPS_REGISTER.csv` | compliance_mirror | `OPS_REGISTER` | active | active | Y |
| `CYCLE_REGISTER.csv` | compliance_mirror | `CYCLE_REGISTER` | active | active | Y |
| `REPOSITORY_REGISTRY.csv` | compliance_mirror | `REPOSITORY_REGISTRY` + MD sync | active | active | Y |
| `REPO_HEALTH_SNAPSHOT.csv` | compliance_mirror | `REPO_HEALTH_SNAPSHOT` | active | active | Y |
| `CANONICAL_REGISTRY.csv` | git_only | `validate_hlk` structural | n/a | n/a | Y |
| `finops/FINOPS_COUNTERPARTY_REGISTER.csv` | finops_mirror | `FINOPS_COUNTERPARTY_REGISTER` | active | active | Y |
| `advops/ADVISER_ENGAGEMENT_DISCIPLINES.csv` | compliance_mirror | `ADVISER_ENGAGEMENT_DISCIPLINES` | active | active | Y |
| `advops/ADVISER_OPEN_QUESTIONS.csv` | compliance_mirror | `ADVISER_OPEN_QUESTIONS` | active | active | Y |
| `advops/FILED_INSTRUMENTS.csv` | compliance_mirror | `FILED_INSTRUMENTS` | active | active | Y |
| `techops/COMPONENT_SERVICE_MATRIX.csv` | forward_charter | `COMPONENT_SERVICE_MATRIX` | none | forward-charter until DDL+emit | Y |
| `dimensions/CAPABILITY_REGISTRY.csv` | compliance_mirror | `CAPABILITY_REGISTRY` | gap-splice | active (registry) | Y |
| `dimensions/CAPABILITY_CONFIDENCE_REGISTRY.csv` | compliance_mirror | `CAPABILITY_CONFIDENCE_REGISTRY` | gap-splice | active | Y |
| `dimensions/AIC_REGISTRY.csv` | compliance_mirror | `AIC_REGISTRY` | gap-splice | active | Y |
| `dimensions/AUDIENCE_REGISTRY.csv` | compliance_mirror | `AUDIENCE_REGISTRY` | gap-splice | active | Y |
| `dimensions/COUNTRY_WORK_CALENDAR.csv` | compliance_mirror | (schema drift registry) | gap-splice | active | Y |
| `dimensions/TOPIC_REGISTRY.csv` | compliance_mirror | `TOPIC_REGISTRY` | active | active | Y |
| `dimensions/PROGRAM_REGISTRY.csv` | compliance_mirror | `PROGRAM_REGISTRY` | active | active | Y |
| `dimensions/PERSONA_REGISTRY.csv` | compliance_mirror | `PERSONA_REGISTRY` | active | active | Y |
| `dimensions/PERSONA_SCENARIO_REGISTRY.csv` | compliance_mirror | `PERSONA_SCENARIO_REGISTRY` | active | active | Y |
| `dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv` | compliance_mirror | `CHANNEL_TOUCHPOINT_REGISTRY` | active | active | Y |
| `dimensions/SOURCING_REGISTER.csv` | compliance_mirror | `SOURCING_REGISTER` | active | active | Y |
| `dimensions/SKILL_REGISTRY.csv` | compliance_mirror | `SKILL_REGISTRY` | active | active | Y |
| `dimensions/TOUCHPOINT_KIT_CELL_REGISTRY.csv` | compliance_mirror | `TOUCHPOINT_KIT_CELL` | active | active | Y |
| `dimensions/POLICY_REGISTER.csv` | compliance_mirror | `POLICY_REGISTER` | active | active | Y |
| `dimensions/GOI_POI_REGISTER.csv` | compliance_mirror | `GOI_POI_REGISTER` | active | active | Y |
| `dimensions/ENGAGEMENT_REGISTRY.csv` | compliance_mirror | (engagement validators) | DDL, **emit unclear** | active after emit wire | Y |
| `dimensions/SUBSTRATE_REGISTRY.csv` | compliance_mirror | `SUBSTRATE_REGISTRY` | active | active | Y |
| `dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv` | compliance_mirror | `PEOPLE_DESIGN_PATTERN_REGISTRY` | active | active | Y |
| `dimensions/OUTPUT_TYPE_REGISTRY.csv` | compliance_mirror | `OUTPUT_ARCHITECTURE_REGISTRIES` | mirror DDL | active (extend main/gap) | Y |
| `dimensions/ARTIFACT_CLASS_REGISTRY.csv` | compliance_mirror | `OUTPUT_ARCHITECTURE_REGISTRIES` | mirror DDL | active | Y |
| `dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv` | compliance_mirror | `OUTPUT_ARCHITECTURE_REGISTRIES` | mirror DDL | active | Y |
| `dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv` | git_only | `KNOWLEDGE_PAIRING_REGISTRY` | none | git-only | Y |
| `dimensions/BUILDOUT_BACKLOG.csv` | git_only | `BUILDOUT_BACKLOG` | none | git-only | Y |
| `dimensions/POC_TO_COMMERCIAL_MAP.csv` | git_only | (via capability/use-case) | none | git-only | partial |
| `dimensions/MADEIRA_AIC_PER_TASK_REGISTRY.csv` | git_only | `MADEIRA_AIC_PER_TASK` | forward-charter | git-only | Y |
| `dimensions/AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv` | git_only | matrix validator | none | git-only | Y |
| `dimensions/USE_CASE_ARCHIVE.csv` | git_only | `USE_CASE_ARCHIVE` | none | git-only | Y |

### 2.3 Sibling-area CSVs (32 outside Compliance root)

| Area | Path | asset_class | Plane-1 gate | P2 today | P2 target | PREC |
|:---|:---|:---|:---|:---|:---|:---:|
| **Data/Architecture** | `.../ENTITY_CATALOG.csv` | graph_projection | `CANONICAL_ARTICULATION` | n/a | graph-only | **N** |
| | `.../CANONICAL_RELATIONSHIP_REGISTRY.csv` | graph_projection | `CANONICAL_ARTICULATION` + `FK_VERB_COVERAGE` | n/a | graph-only | **N** |
| | `.../METRICS_REGISTRY.csv` | git_only | `METRICS_REGISTRY` | none | git-only | Y |
| | `.../SUPABASE_MODULE_REGISTRY.csv` | git_only | `SUPABASE_MODULE_REGISTRY` | none | git-only | **N** |
| **Data/Governance** | `.../DATA_CONTRACT_REGISTRY.csv` | data_contract_mirror | `DATA_CONTRACT_REGISTRY` | forward-charter | forward-charter | Y |
| | `.../BI_CONSUMER_REGISTRY.csv` | git_only | `BI_CONSUMER_REGISTRY` | none | git-only | Y |
| | `.../AREA_BI_PROFILE.csv` | git_only | `AREA_BI_PROFILE` | none | git-only | Y |
| | `.../RPA_ADAPTER_REGISTRY.csv` | compliance_mirror | `ADAPTER_REGISTRIES` | **no DDL** | forward-charter OR DDL tranche | Y |
| **Finance** | `.../PRICING_TIER_REGISTRY.csv` | finops_mirror | `PRICING_TIER_REGISTRY` | none | forward-charter | **N** |
| | `.../FINOPS_TAX_CALENDAR.csv` | finops_mirror | `FINOPS_TAX_CALENDAR` | none | forward-charter | **N** |
| | `.../FINOPS_PERFORMANCE_OBLIGATION_REGISTRY.csv` | finops_mirror | (bundled w/ pricing) | none | forward-charter | **N** |
| **Marketing/Reach** | 4× `*_ADAPTER_REGISTRY.csv` | compliance_mirror | `ADAPTER_REGISTRIES` | DDL, **no emit** | active after emit | Y |
| **Marketing/Experimentation** | `ATTRIBUTION_ADAPTER_REGISTRY.csv` | compliance_mirror | `ADAPTER_REGISTRIES` | DDL, **no emit** | active | Y |
| **Operations/RevOps** | `ENGAGEMENT_TEMPLATE_REGISTRY.csv` | compliance_mirror | `ENGAGEMENT_TEMPLATE_*` | DDL, **no emit** | active | Y |
| | `REVOPS_ADAPTER_REGISTRY.csv` | compliance_mirror | `ADAPTER_REGISTRIES` | DDL, **no emit** | active | Y |
| | `BILLING_ADAPTER_REGISTRY.csv` | compliance_mirror | `ADAPTER_REGISTRIES` | DDL, **no emit** | active | Y |
| **Operations/SMO** | `CONTRACT_ADAPTER_REGISTRY.csv` | compliance_mirror | `ADAPTER_REGISTRIES` | DDL, **no emit** | active | Y |
| | `SERVICE_CATALOG.csv` | git_only | **none** | none | git-only + mint validator | **N** |
| **People/People Ops** | `ENGAGEMENT_MODEL_REGISTRY.csv` | compliance_mirror | `ENGAGEMENT_MODEL_REGISTRY` | active | active | Y |
| | 5× collaborator-share CSVs | compliance_mirror | `COLLABORATOR_SHARE` | separate emit flag | active (registry unified) | Y |
| **People/Learning** | `LEARNING_OPS_BACKLOG.csv` | git_only | **none** | none | git-only + mint validator | **N** |
| **Research/Intelligence** | `INTELLIGENCEOPS_REGISTER.csv` | compliance_mirror | `INTELLIGENCEOPS_REGISTER` | active | active | Y |
| **Envoy Admin** | `MADEIRA_TOOL_RBAC.csv` | git_only | release-gate strict | none | git-only | Y |
| | `MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv` | git_only | release-gate strict | none | git-only | Y |
| **Envoy root** | `RENDERING_PIPELINE_REGISTRY.csv` | git_only | `RENDERING_PIPELINE_REGISTRY` | none | git-only | **N** |

**Critical systemic finding:** **9 adapter-class mirrors + engagement_template mirror have DDL but zero emit functions in `sync_compliance_mirrors_from_csv.py`** — Plane-2 is structurally broken for I72 MarTech/RevOps surfaces despite Plane-1 PASS.

---

## 3. I95 HCAM quintet backfill

Per operator ratification, HCAM registries are **T1 + Neo4j T3**, not compliance mirror. Backfill = index surfaces only.

### 3.1 PRECEDENCE.md rows (proposed prose-table entries)

| Asset | Classification | Mirror posture | Validator |
|:---|:---|:---|:---|
| `CANONICAL_ARTICULATION_MODEL.md` | Canonical doctrine | **graph-projection SSOT; no compliance mirror** (D-IH-95-B) | `validate_canonical_articulation.py` |
| `ENTITY_CATALOG.csv` | Canonical CSV (Data/Architecture) | T1 git; T3 Neo4j; **no T2 mirror** unless later ratified | `validate_canonical_articulation.py` |
| `CANONICAL_RELATIONSHIP_REGISTRY.csv` | Canonical CSV (Data/Architecture) | T1 git; T3 Neo4j; **no T2 mirror** unless later ratified | `validate_canonical_articulation.py` + `validate_fk_verb_coverage.py` |
| `SEMANTIC_LAYER.md` | Companion doctrine | Reference to HCAM + metrics | `validate_metrics_registry.py` (FK) |
| `SUPABASE_ECOSYSTEM_GOVERNANCE.md` | Architecture doctrine | References `SUPABASE_MODULE_REGISTRY.csv`; not mirrored | `validate_supabase_module_registry.py` |

### 3.2 CANONICAL_REGISTRY.csv rows (exact column fill)

| canonical_id | name | owning_area | file_path | artifact_type | mirror_table | validator | status | notes |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `hcam_doctrine` | HCAM Doctrine | Data | `.../CANONICAL_ARTICULATION_MODEL.md` | md | *(empty)* | `validate_canonical_articulation.py` | active | I95 P1; T3 graph projection |
| `entity_catalog` | Entity Catalog | Data | `.../ENTITY_CATALOG.csv` | csv | *(empty)* | `validate_canonical_articulation.py` | active | ~31 entity types; D-IH-95-B |
| `canonical_relationship_registry` | Canonical Relationship Registry | Data | `.../CANONICAL_RELATIONSHIP_REGISTRY.csv` | csv | *(empty)* | `validate_canonical_articulation.py` | active | ArchiMate verb closed set |
| `supabase_module_registry` | Supabase Module Registry | Data | `.../SUPABASE_MODULE_REGISTRY.csv` | csv | *(empty)* | `validate_supabase_module_registry.py` | active | R2-03 EG governance |
| `rendering_pipeline_registry` | Rendering Pipeline Registry | Envoy Tech Lab | `v3.0/Envoy Tech Lab/.../RENDERING_PIPELINE_REGISTRY.csv` | csv | *(empty)* | `validate_rendering_pipeline_registry.py` | active | Path split vs Admin O5-1 |

**Operator gate:** Canonical CSV mint for PRECEDENCE edits + 5 CANONICAL_REGISTRY appends (same commit).

---

## 4. CANONICAL_GOVERNANCE_REGISTRY.csv — proposed schema

**Location (proposed):** `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CANONICAL_GOVERNANCE_REGISTRY.csv`

**Row count estimate:** **73 rows** (1:1 with vault CSV inventory) + **1 header**; grows when new canonicals mint. The governance meta-registry (`CANONICAL_GOVERNANCE_REGISTRY.csv`) indexes these rows but is not itself one of the 73 vault content CSVs — see [^gov1-inventory].

### 4.1 Columns

| Column | Type | Purpose |
|:---|:---|:---|
| `governance_id` | slug PK | Stable key (`gov_<area>_<file_stem>`) |
| `csv_path` | repo-relative POSIX path | SSOT file location |
| `owning_area` | enum | O5-1 area slug |
| `owning_role` | string | From area charter / baseline |
| `asset_class` | enum | `compliance_mirror` \| `finops_mirror` \| `data_contract_mirror` \| `git_only` \| `graph_projection` \| `forward_charter` |
| `plane1_validator` | string | Primary script or dispatch label |
| `plane1_in_validate_hlk` | bool | Wired in `validate_hlk.py` dispatch |
| `plane2_mirror_table` | string | `compliance.*` or empty |
| `plane2_sync_policy` | enum | `active` \| `forward_charter` \| `git_only` \| `graph_projection` \| `disabled` |
| `plane2_emit_profile` | string | `main` \| `gap_splice` \| `scoped_flag` \| `none` |
| `plane2_workflow_paths` | semicolon-list | Glob fragments for CI path filter |
| `precedence_registered` | bool | PRECEDENCE.md row exists |
| `canonical_registry_id` | FK | → CANONICAL_REGISTRY.canonical_id (nullable) |
| `mirror_ddl_migration` | string | Latest supabase migration ref |
| `enum_parity_required` | bool | Subject to `validate_mirror_enum_parity.py` |
| `delete_reconcile_pk` | string | PK column for shrink-sync |
| `last_review` | date | |
| `last_review_decision_id` | FK | → DECISION_REGISTER |
| `status` | enum | `active` / `planned` / `deprecated` |
| `notes` | string | Forward-charter pointer, area surprises |

### 4.2 Relationship to Option B

- **Plane 1 universal:** Every row must have non-empty `plane1_validator` + `plane1_in_validate_hlk=true` OR documented exception in `notes` with forward-charter OPS row.
- **Plane 2 explicit:** `plane2_sync_policy=active` **only** when `mirror_ddl_migration` is populated **and** emit profile is implemented. CI reads registry — not folder hardcoding.
- **HCAM / articulation:** `asset_class=graph_projection`, `plane2_sync_policy=graph_projection`, empty mirror columns.
- **Single SSOT for workflow refactor:** `validate_mirror_emit_contract.py` iterates rows where `plane2_sync_policy=active`.

---

## 5. Workflow refactor spec

### 5.1 `.github/workflows/supabase-mirror-sync.yml`

| Current | Target |
|:---|:---|
| `paths:` hardcoded to `People/Compliance/canonicals/**/*.csv` | `paths:` built from registry `plane2_workflow_paths` union |
| Always runs full Compliance emit | Step 0: `py scripts/validate_canonical_governance_registry.py` (new) |
| Gap splice hardcoded in workflow YAML | Emit orchestrator reads registry `plane2_emit_profile` (`main`, `gap_splice`, `scoped_flag`) |
| Enum parity on all emitted SQL | Unchanged; table list from registry active rows |

**Add step:** Registry drift check — fail if a CSV with `plane2_sync_policy=active` changed but path filter wouldn't trigger workflow.

### 5.2 `validate_mirror_emit_contract.py`

| Current | Target |
|:---|:---|
| `_EMIT_CONTRACTS` hardcoded 10 Compliance-relative paths | Load from `CANONICAL_GOVERNANCE_REGISTRY.csv` where `plane2_sync_policy=active` |
| `CANONICALS` constant points at Compliance folder only | Resolve `csv_path` per row |
| Workflow wiring check for gap/enum/reconcile | Extend to verify registry path filters match workflow `on.push.paths` |

**Acceptance:** Changing a sibling-area mirrored CSV (e.g. `Operations/RevOps/.../ENGAGEMENT_TEMPLATE_REGISTRY.csv`) triggers emit-contract validation and CI path filter.

### 5.3 `sync_compliance_mirrors_from_csv.py` (follow-on packet)

- Replace ad-hoc `--*-only` flags with `--registry-id <governance_id>` OR auto-emit all `active` rows.
- **Priority gap closure:** adapter registries (8+1), engagement_template, engagement_registry (if confirmed), output-architecture mirrors not in main bundle.

---

## 6. Regression strategy

### 6.1 Pre-tranche synthesis (canonical_csv_mint class)

Before **each** registry/index/mirror tranche commit:

```powershell
py scripts/synthesis_before_tranche_check.py --tranche-class canonical_csv_mint `
  --tranche-id P95-GOV-<N> --ratifying-decisions D-IH-95-<X> --reversibility medium
```

Fire set: SYN-01, SYN-04, SYN-05, SYN-07, SYN-08, SYN-09 (+ SYN-02/03/10 when CSV surfaces in dashboards).

Report: `docs/wip/planning/95-canonical-articulation-model/reports/synthesis-p95-gov-<N>-2026-06-09.md`

### 6.2 Inter-wave DIM-4 (canonical_csv_pair_completeness)

At each packet close, run inter-wave sweep focusing **dimension 4**:

```powershell
py scripts/inter_wave_regression_sweep.py --wave-closing P95-GOV-<N>
```

Disposition via inline-ratify 5-option enum per `akos-inter-wave-regression.mdc`.

### 6.3 Intent-ranked regression (conditional)

Trigger if packet touches **HCAM competency questions** or operator-facing ERP join surfaces:

```powershell
py scripts/intent_ranked_regression.py --initiative 95 --ics-order
```

Reference prior run: `reports/intent-ranked-regression-2026-06-06.md`.

### 6.4 Verification profile matrix

| Gate | When | Command |
|:---|:---|:---|
| **Fast loop** | Every packet commit | `py scripts/verify.py pre_commit_fast` |
| **Full bar** | P95-GOV-6 closure only | `py scripts/verify.py pre_commit` |
| **HLK umbrella** | Any CSV/index change | `py scripts/validate_hlk.py` |
| **Mirror emit contract** | P95-GOV-3+ | `py scripts/validate_mirror_emit_contract.py` |
| **DataOps two-plane** | Mirror packets | `py scripts/dataops_quality_check.py` |
| **Area completeness** | After index backfill | `py scripts/validate_area_completeness.py --matrix` |
| **Release gate** | Closure | `py scripts/release-gate.py` |

### 6.5 Mirror apply evidence (operator gate)

Per Holistika ops two-plane doctrine — automated emit ≠ live mirror proof:

1. CI emit artifact `mirror-upsert.sql` PASS
2. Enum parity preflight PASS (when creds present)
3. Operator apply via `gh workflow run supabase-mirror-sync.yml -f apply=true` **or** `docs/guides/holistika-mirror-dml-apply.md`
4. Row-count evidence logged in packet report (pattern: `two-plane-data-integrity-remediation-2026-06-08.md`)

---

## 7. Phased execution packets (P95-GOV-1..8)

### P95-GOV-1 — Governance registry mint (foundation)

| Field | Spec |
|:---|:---|
| **Scope** | Mint `CANONICAL_GOVERNANCE_REGISTRY.csv` + `akos/hlk_canonical_governance_registry_csv.py` + `scripts/validate_canonical_governance_registry.py`; seed all 73 rows from §2 inventory |
| **Prerequisites** | This charter operator-approved |
| **Files** | Registry CSV; Pydantic module; validator; `validate_hlk.py` dispatch; `config/verification-profiles.json` self-test step |
| **Verification** | `validate_canonical_governance_registry.py`; `validate_hlk.py`; `pre_commit_fast` |
| **Operator gate** | **Yes** — canonical CSV mint |
| **Rollback** | Revert registry commit; validators SKIP when CSV absent |

### P95-GOV-2 — HCAM quintet + index backfill tranche A

| Field | Spec |
|:---|:---|
| **Scope** | PRECEDENCE rows §3.1; CANONICAL_REGISTRY rows §3.2; link registry FKs for 5 HCAM surfaces |
| **Prerequisites** | P95-GOV-1 |
| **Files** | `PRECEDENCE.md`; `CANONICAL_REGISTRY.csv`; `CANONICAL_GOVERNANCE_REGISTRY.csv` precedence flags |
| **Verification** | `validate_hlk.py`; `validate_index_freshness.py` (if in profile); `validate_canonical_articulation.py` |
| **Operator gate** | **Yes** |
| **Rollback** | Revert index commit; registry flags → `precedence_registered=false` |

### P95-GOV-3 — Workflow + emit-contract registry refactor

| Field | Spec |
|:---|:---|
| **Scope** | Refactor `validate_mirror_emit_contract.py` + `supabase-mirror-sync.yml` to registry-driven paths (§5) |
| **Prerequisites** | P95-GOV-1 |
| **Files** | `.github/workflows/supabase-mirror-sync.yml`; `scripts/validate_mirror_emit_contract.py`; tests |
| **Verification** | `validate_mirror_emit_contract.py`; workflow lint; `pre_commit_fast` |
| **Operator gate** | No (mechanical) |
| **Rollback** | Revert to hardcoded Compliance paths |

### P95-GOV-4 — Index backfill tranche B (Finance, Learning, SMO, Envoy, SUPABASE_MODULE)

| Field | Spec |
|:---|:---|
| **Scope** | Close PRECEDENCE + CANONICAL_REGISTRY gaps from §2.3 **N** rows; mint validators for `SERVICE_CATALOG.csv`, `LEARNING_OPS_BACKLOG.csv` |
| **Prerequisites** | P95-GOV-2 |
| **Files** | PRECEDENCE; CANONICAL_REGISTRY; new validators; process_list rows if SOP pairing required |
| **Verification** | `validate_hlk.py`; DIM-4 sweep; synthesis report |
| **Operator gate** | **Yes** (CSV + optional process_list) |
| **Rollback** | Revert tranche |

### P95-GOV-5 — Mirror emit gap closure (DDL exists, emit missing)

| Field | Spec |
|:---|:---|
| **Scope** | Wire emit for **9 adapter mirrors + engagement_template**; extend `_EMIT_CONTRACTS` via registry; **no new DDL** |
| **Prerequisites** | P95-GOV-3; operator confirms prod DDL applied for pending migrations |
| **Files** | `sync_compliance_mirrors_from_csv.py`; `akos/hlk_adapter_registry_csv.py`; tests in `tests/test_sync_compliance_mirrors_from_csv.py` |
| **Verification** | `validate_mirror_emit_contract.py`; `compliance_mirror_emit` profile; enum parity |
| **Operator gate** | **Yes** if mirror apply to prod |
| **Rollback** | Revert emit functions; mirrors stay stale (documented) |

### P95-GOV-6 — Universal Plane-1 hardening sweep

| Field | Spec |
|:---|:---|
| **Scope** | Every registry row `plane1_in_validate_hlk=true`; wire MADEIRA validators into HLK dispatch (not release-gate only); COLLABORATOR_SHARE INFO→FAIL ramp decision |
| **Prerequisites** | P95-GOV-4 |
| **Files** | `validate_hlk.py`; release-gate wiring; registry status columns |
| **Verification** | Full `pre_commit`; `inter_wave_regression_sweep` |
| **Operator gate** | Inline-ratify for FAIL ramp |
| **Rollback** | Revert dispatch entries |

### P95-GOV-7 — Forward-charter mirror DDL tranche (optional, gated)

| Field | Spec |
|:---|:---|
| **Scope** | **Only** rows with `asset_class=forward_charter` + operator-approved SQL proposal: Finance plane-2, DATA_CONTRACT, RPA adapter, COMPONENT_SERVICE_MATRIX |
| **Prerequisites** | P95-GOV-5; operator SQL gate per `akos-holistika-operations.mdc` |
| **Files** | `supabase/migrations/`; registry mirror columns; emit functions |
| **Verification** | `validate_pydantic_mirror_enum_ssot.py`; operator mirror apply evidence |
| **Operator gate** | **Mandatory** DDL + CSV |
| **Rollback** | Migration forward-fix; delete-reconcile |

### P95-GOV-8 — Closure UAT + area matrix re-proof

| Field | Spec |
|:---|:---|
| **Scope** | I95 competency questions spot-check; `validate_area_completeness.py --matrix` no Data/Finance/People regression; closure UAT mint |
| **Prerequisites** | P95-GOV-1..6 (P95-GOV-7 optional PWF) |
| **Files** | `reports/uat-universal-canonical-governance-2026-06-09.md` |
| **Verification** | Full `pre_commit`; Neo4j parity (P2); intent-ranked if ICS≥ threshold |
| **Operator gate** | Closure sign-off |
| **Rollback** | N/A (evidence-only) |

---

## 8. Risk register (top 8)

| ID | Risk | L×I | Mitigation |
|:---|:---|:---:|:---|
| R95-GOV-01 | **CI breakage** when workflow paths expand to 73 CSV globs | H×H | Registry-driven path union with max-size guard; `pre_commit_fast` on every packet |
| R95-GOV-02 | **Enum parity FAIL** when emit added for adapters/templates | H×M | Run `validate_mirror_enum_parity.py` before apply; migration-first pattern from BT-09 |
| R95-GOV-03 | **Forward-charter mirrors** promoted without DDL | M×H | Registry `plane2_sync_policy` gate; P95-GOV-7 isolated; operator SQL gate |
| R95-GOV-04 | **Area governance conservative skip** — registry mint treated as “complete area” | M×M | `validate_area_completeness.py --matrix` at P95-GOV-8; no mirror claim for graph_projection rows |
| R95-GOV-05 | **Prod DDL lag** (collaborator-share, radar cols) blocks emit proof | H×M | Inventory-before-greenfield; MCP read-only; OPS rows from I86 sweep |
| R95-GOV-06 | **Path split Envoy** (Admin O5-1 vs root) breaks workflow filters | M×M | Explicit `plane2_workflow_paths` per row; placement-integrity forward-charter |
| R95-GOV-07 | **Umbrella validators hide per-CSV gaps** (adapters, CS) | M×H | Registry row per CSV; emit-contract per mirror table |
| R95-GOV-08 | **Big-bang scope creep** into CSV moves / Neo4j rework | H×M | Packet scope guards; HCAM stays T3; I94/I95 lanes unchanged |

---

## 9. Per-area research notes

### Data (Governance + Architecture)

**Key files:** `DATAOPS_DISCIPLINE.md` (two-plane contract §2.1); `DATA_GOVERNANCE_POLICY.md`; `CANONICAL_ARTICULATION_MODEL.md` (T1→T3); `SUPABASE_ECOSYSTEM_GOVERNANCE.md` (27 modules, 11 ungoverned baseline).

**Surprises:** Richest validator wiring but weakest PRECEDENCE coverage for HCAM pair; DATA_CONTRACT explicitly forward-charters mirror; RPA is 9th adapter class without mirror DDL.

### People/Compliance

**Key files:** `PRECEDENCE.md`; `CANONICAL_REGISTRY.csv`; `README.md` (plane×program×topic forward layout); `DATAOPS` cross-link.

**Surprises:** Main sync bundle ends at IntelligenceOps — **does not include** collaborator-share, output-architecture, capability (except gap-splice), adapters, engagement_template; `validate_mirror_emit_contract` checks only 10 tables.

### People/People Operations + Learning

**Key files:** `COLLABORATOR_SHARE_DOCTRINE.md`; `ENGAGEMENT_MODEL_REGISTRY.md`; `LEARNING_CHARTER.md`.

**Surprises:** Collaborator-share mirrors require `--collaborator-share-only`; Learning backlog has **zero validator** (deferred I73).

### Finance/Governance

**Key files:** `FINOPS_DISCIPLINE.md`; Finance area charter.

**Surprises:** Three plane-2 CSVs validated in HLK but **absent from PRECEDENCE**; counterparty SSOT remains Compliance `finops/` (cross-area split intentional).

### Marketing/Reach + Experimentation

**Key files:** `REACH_AREA_CHARTER.md`; `SOP-CRM_INTEGRATION_001.md`.

**Surprises:** Four Reach adapters share one umbrella validator; mirrors exist but **no emit path** — highest-impact Plane-2 gap.

### Operations/RevOps + SMO

**Key files:** `REVOPS_AREA_CHARTER.md`; `SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md`; `SERVICE_CATALOG.csv` (5 pre-sold services).

**Surprises:** Engagement template mirror DDL without emit; **SERVICE_CATALOG has no validator** despite being operational SSOT.

### Research/Intelligence

**Key files:** `INTELLIGENCEOPS_REGISTER` + Research Radar discipline; dual home `v3.0/Research/` vs `Admin/O5-1/Research/Intelligence/`.

**Surprises:** Well-wired end-to-end (validator + mirror + main emit); radar freshness cols need prod migration parity.

### Envoy Tech Lab

**Key files:** `MADEIRA_MODE_PARITY.md`; `RENDERING_PIPELINE_REGISTRY` at **non-O5-1 path**.

**Surprises:** MADEIRA CSVs validated in **release-gate only**, not HLK dispatch; no mirrors by design today.

---

## 10. AskQuestion deferrals (post-charter review)

These need operator ratification **after** charter review, not during P95-GOV-1:

1. **RPA adapter mirror:** Mint DDL for 9th adapter class now (P95-GOV-7) vs keep git-only until MarTech tranche?
2. **Finance plane-2 timing:** Forward-charter all three Finance/Governance CSVs vs prioritize `PRICING_TIER` only for FINOPS mirror?
3. **COMPONENT_SERVICE_MATRIX mirror:** Active Plane-2 vs remain git-only (TechOps doctrine)?
4. **HCAM T2 exception:** Any future compliance mirror for relationship registry (operator said no unless ratified — confirm permanence)?
5. **COLLABORATOR_SHARE FAIL ramp:** Promote to FAIL in P95-GOV-6 or defer until first settlement tranche?
6. **CSV path normalization:** Big-bang physical moves to `compliance/<plane>/` (I22 forward layout) in scope or explicitly OUT?

---

## Recommended packet order for Composer executor

1. **P95-GOV-1** — Registry mint (blocks everything else)  
2. **P95-GOV-2** — HCAM quintet index backfill  
3. **P95-GOV-3** — Workflow + emit-contract refactor  
4. **P95-GOV-4** — Index backfill tranche B  
5. **P95-GOV-5** — Mirror emit gap closure (adapters + template)  
6. **P95-GOV-6** — Plane-1 hardening  
7. **P95-GOV-7** — Forward-charter DDL (optional; operator SQL gate)  
8. **P95-GOV-8** — Closure UAT  

Run synthesis before commits for packets 1, 2, 4, 5, 7; inter-wave DIM-4 after packets 2, 4, 5, 6, 8.

---

## Scope guard — what NOT to do in packet 1

Packet 1 is **registry-only**. Do **not** refactor `sync_compliance_mirrors_from_csv.py`, change `supabase-mirror-sync.yml` paths, mint Supabase migrations, add mirror emit for adapters/templates, move CSV files between areas, wire HCAM to compliance mirrors, promote COLLABORATOR_SHARE to FAIL, or apply mirror DML to production. P95-GOV-1 delivers the SSOT inventory + validator self-test + HLK dispatch entry — nothing that triggers CI mirror sync or DDL.

---

```
=== THINKING DONE — operator review ===

Ready:
- Option B tiered two-plane charter drafted with 73-CSV inventory, governance registry schema, 8 execution packets, regression matrix, and 6 deferred ratification questions

Packets (run in order):
1. P95-GOV-1 — Mint CANONICAL_GOVERNANCE_REGISTRY.csv + validator (73 rows)
2. P95-GOV-2 — HCAM quintet PRECEDENCE + CANONICAL_REGISTRY backfill
3. P95-GOV-3 — Registry-driven mirror-sync workflow + emit-contract refactor
4. P95-GOV-4 — Index backfill tranche B (Finance/Learning/SMO/Envoy gaps)
5. P95-GOV-5 — Mirror emit gap closure (adapters + engagement template)
6. P95-GOV-6 — Universal Plane-1 hardening (HLK dispatch completeness)
7. P95-GOV-7 — Forward-charter mirror DDL tranche (operator SQL gate; optional)
8. P95-GOV-8 — Closure UAT + area-completeness re-proof

Hard gates todo-#1:
- P95-GOV-1 + P95-GOV-2 + P95-GOV-4 canonical CSV mint (operator approval before commit)

Stop-and-report contract:
- Validator FAIL / ambiguity → halt; cite path + line; no silent defaults.

Operator: switch to execution seat (Composer 2.5) or fresh Composer thread, then
invoke `.cursor/agents/executor.md` with packet 1.
`
