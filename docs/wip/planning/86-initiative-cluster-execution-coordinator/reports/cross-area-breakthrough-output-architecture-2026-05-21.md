---
intellectual_kind: cross_area_breakthrough_announcement
sharing_label: internal_only
authored: 2026-05-21
authored_by: Brand & Narrative Manager (acting via Madeira AIC)
parent_initiative: INIT-OPENCLAW_AKOS-86
wave: L
linked_decisions:
  - D-IH-86-BB  # 4-layer output-architecture meta-decision (Wave K)
  - D-IH-86-BC  # forward-charter I-NN-OUTPUT-ARCHITECTURE candidate (Wave K)
  - D-IH-86-BE  # Wave L pattern propagation to People DoD registry
linked_pattern_id: pattern_4layer_output_architecture_below_quality_fabric
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/OUTPUT_TYPE_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ARTIFACT_CLASS_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UAT_DISCIPLINE.md
language: en
audience: J-OP
access_level: 3
status: active
---

# Cross-area breakthrough announcement — 4-layer output architecture below the 5-axis Quality Fabric

> **Per [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md):** when a new design pattern row lands in [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv), People emits this announcement so consuming areas can ratify the pattern locally and migrate their `process_list.csv` rows to set `inherited_pattern_id` FK.

## 1. The pattern in one sentence

Every Holistika output (prose / slide / mermaid / gantt / image / voice / web / pdf) decomposes into **four orthogonal layers** that sit *below* the 5-axis Quality Fabric and are *parametrised by it*: **(L1) Output Type** (the medium / shape) → **(L2) Artifact Class** (the named purpose) → **(L3) Component Primitive** (the Shadcn-shape sub-units) → **(L4) Render Surface** (PDF / Web / ERP / Mail / Slide / Broadcast — already canonical per `akos-external-render-discipline.mdc` RULE 1). The fabric stays at 5 axes (audience × channel × scenario × brand × governance); the 4-layer hierarchy lets `compose()` return a **derived bar per layer**, which is what unlocks per-component doctrine depth at Shadcn quality.

## 2. Why this is a People-area breakthrough

Per [`akos-people-discipline-of-disciplines.mdc`](../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) RULE 1: People mints **patterns**; consuming areas author their **own processes** under their own area `canonicals/`. The 4-layer output architecture is exactly that shape — a design pattern (not a Marketing-only or Tech-Lab-only artifact). It is the load-bearing answer to the operator's verbatim 2026-05-20 framing:

> *"we need scalability or key parsing to go deeper into the items that compose our messages that we output with our different types over the different channels for the different audiences ... so research per component"*

The pattern resolves three structural failure modes the Wave J 5-axis fabric (alone) could not address:

1. **The "where do components live" question.** Without Layer 3, every area would have to invent its own primitive registry (Marketing's CTA registry vs Tech Lab's button registry vs Operations' checklist-row registry — all nearly the same primitives, all forked). Layer 3 is People-owned; consuming areas FK against it.
2. **The "where does UI start" question.** Without Layer 1, "UI components" and "PDF slide components" and "voice cadence components" are conflated. Layer 1 splits the medium concern from the purpose concern.
3. **The "components are not just UI" extension** the operator named verbatim (G4 extension 2026-05-20). Mermaids / Excalidraw / Gantts / voice for agents / reader-platform variants are all output-types — Layer 1 names them; Layer 2 binds them to artifact-class purposes; Layer 3 defines their primitive sub-units.

## 3. Consumption contract per consuming area

Per the pattern row's `consumer_areas` cell, **all 9 areas** consume this pattern: marketing / research / techlab / operations / legal / people / ethics / finance / compliance. Each area's adoption shape:

### 3.1 Marketing (Reach + Resonance + Brand)

**Primary consumer.** Marketing authors the highest density of artifacts under the 4-layer hierarchy:

- **Reach**: cover-emails (`AC-COVER-EMAIL` artifact class) + DM-bundles (`AC-INTRO-MESSAGE`) → composed of `CP-GREETING` + `CP-BRIDGE-CITATION` + `CP-HOOK` + `CP-CTA` + `CP-SIGNATURE` primitives → rendered to `mail` / `web` surfaces.
- **Resonance / RevOps**: engagement dossiers (`AC-DOSSIER`) + advisor packs (`AC-DECK-ADVISOR-PACK`) → composed of `CP-SLIDE-HERO` + `CP-SLIDE-PROOF-POINT` + `CP-SLIDE-THE-ASK` + `CP-EVIDENCE-BLOCK` + `CP-CONFIDENTIALITY-BLOCK` → rendered to `pdf` / `slide` surfaces.
- **Brand & Narrative Manager**: owns Layer 2 + Layer 3 doctrine (per absorption 2026-05-15 + I-NN-OUTPUT-ARCHITECTURE C-NN-5 default verdict). Acts as the discipline editor for component primitives' brand-voice rules + variants-by-audience matrix.

**Adoption action**: Marketing process_list rows that produce these artifacts (e.g. `tbi_mkt_prc_brand_canon_mtnce_001`, `hlk_mkt_advisor_handoff_render_001` if forward-chartered) should set `inherited_pattern_id: pattern_4layer_output_architecture_below_quality_fabric` once `process_list.csv` schema gains the column (forward-chartered with the I-NN-OUTPUT-ARCHITECTURE charter).

### 3.2 Research / IntelligenceOps

**Heavy consumer.** Research outputs (`AC-DOSSIER` for engagement context-memos; `AC-COUNTERPARTY-BRIEF` for internal-register briefs; `AC-OBJECTIONS-BRIEF` for pre-meeting prep) all decompose into Layer 3 primitives plus the new `CP-CONFIDENTIALITY-BLOCK` (which carries access-level + sharing-label scaffolding per `access_levels.md`). IntelligenceOps discovery dossiers map to `AC-DOSSIER` + `AC-TOPIC-GRAPH` (mermaid output).

**Adoption action**: Research SOPs that produce dossiers should reference the `ARTIFACT_CLASS_LIBRARY.md` worked-example for `AC-DOSSIER` rather than re-specifying authoring rules locally. The Research Director (Founder during pre-hire) is the named role-owner reviewer of Layer 2 + Layer 3 changes that affect Research outputs.

### 3.3 Tech Lab (Envoy / System Owner)

**Hybrid consumer.** Tech Lab consumes the architecture in two distinct postures:

- **Stack jargon side** — Tech Lab authors the *infrastructure* layer of the architecture: render scripts (11 `render_*.py` retro-classified into `ARTIFACT_CLASS_REGISTRY.render_script_path` at Wave K), validators (`scripts/validate_output_architecture_registries.py` at Wave L), Pydantic models (`akos/hlk_*_csv.py` at Wave L), Supabase migration (Wave L L4 + L6).
- **Doctrine consumer side** — Tech Lab uses the architecture for `AC-OPERATOR-INBOX`, `AC-WIP-DASHBOARD`, `AC-PMO-HUB-RENDER`, `AC-HLK_ERP_PANEL` (forward) — System Owner-authored operator surfaces consuming the same Layer 3 primitives (`CP-DASHBOARD-CARD`, `CP-NAV-NAVBAR`, `CP-NAV-SIDEBAR`, `CP-DATA-TABLE`, `CP-EMPTY-STATE`, `CP-LOADING-STATE`, `CP-ERROR-STATE`, `CP-FORM-FIELD`).

**Adoption action**: future HLK-ERP surface initiatives (forward-chartered as I-NN-OUTPUT-ARCHITECTURE P6) FK against the 3 mirror tables in Supabase rather than re-discovering primitives.

### 3.4 Operations (PMO + RevOps + IntelligenceOps + SMO)

**Heavy consumer.** Operations outputs governed by the architecture: `AC-INITIATIVE-CHARTER` (master-roadmap.md per `akos-planning-traceability.mdc`) + `AC-WAVE-CLOSURE` (wave reports per `akos-agent-checkpoint-discipline.mdc`) + `AC-PMO-HUB-RENDER` (auto-rendered PMO landing) + `AC-OPERATIONAL-COHESION-INDEX` (per `OPERATIONAL_COHESION_DOCTRINE.md`) + `AC-RUNBOOK-SCRIPT` (Python paired runbooks per `akos-executable-process-catalog.mdc` RULE 1).

**Adoption action**: PMO master-roadmap authoring against `akos-planning-traceability.mdc` plan-quality bar inherits the `CP-DIAGRAM-MERMAID-FLOWCHART` + `CP-DIAGRAM-MERMAID-GANTT` + `CP-EVIDENCE-BLOCK` primitives. Future master-roadmaps should explicitly reference the Component Primitive codes when prescribing content. PMO co-owners + System Owner co-owners review Layer 2 + Layer 3 changes that affect Operations outputs.

### 3.5 Legal + Compliance

**Light consumer.** Legal outputs: `AC-DOSSIER` for adviser-engagement handoffs (per `akos-adviser-engagement.mdc`) + `AC-CONTRACT` (forward-chartered with I-NN-CONTRACT-LIFECYCLE) + `AC-NDA` (forward). Compliance outputs: `AC-PRECEDENCE-LEDGER` (PRECEDENCE.md) + `AC-DECISION-REGISTER-ROW`. Both areas consume `CP-CONFIDENTIALITY-BLOCK` heavily for access-level / sharing-label scaffolding.

**Adoption action**: Legal Counsel + Compliance Officer co-sign on `CP-CONFIDENTIALITY-BLOCK` doctrine page when it lands at I-NN-OUTPUT-ARCHITECTURE P3.

### 3.6 People (self) + Ethics + Finance

**Self-consumer (People).** People-authored doctrine canonicals (`HOLISTIKA_ORGANISING_DOCTRINE.md`, `HOLISTIKA_AGENTIC_DOCTRINE.md`, `HOLISTIKA_QUALITY_FABRIC.md`, `UAT_DISCIPLINE.md`, `RESEARCH_HEAD_DISCIPLINE.md`, etc.) all instantiate `AC-DOCTRINE-CANONICAL` with `OT-PROSE-MARKDOWN` output type. Component primitives used: `CP-EVIDENCE-BLOCK`, `CP-DIAGRAM-MERMAID-FLOWCHART`, `CP-DATA-TABLE`.

**Light consumer (Ethics + Finance).** Both areas inherit the architecture but produce low artifact density today. Adoption action: when Ethics promotes `ETHICAL_AGENTIC_BOUNDARIES.md` to v2 or Finance promotes a new register beyond FINOPS, the architecture is the load-bearing organising lens.

## 4. Activation gates clearance trail

Per the candidate file [`docs/wip/planning/_candidates/i-nn-output-architecture.md`](../../_candidates/i-nn-output-architecture.md) §2.1, the per-row doctrine pages mature inside the forward-chartered initiative once **three activation gates** clear:

| Gate | Status today | Trigger |
|:----:|:---|:---|
| **A1** Quality Fabric at status:active + `compose()` runbook lands | **NOT MET** | Per `D-IH-86-BA`; compose() runbook (`scripts/derive_quality_bar.py`) forward-chartered |
| **A2** UAT_DISCIPLINE at status:active + 11-class taxonomy ratified | **NOT MET** | Per `D-IH-86-AY`; UAT 11-class promotion forward-chartered |
| **A3** ≥ 1 channel doctrine POC | **NOT MET** | Per `D-IH-86-AW`; first `<CHAN-CODE>_DOCTRINE.md` forward-chartered |

The Wave K + Wave L commits are **architectural skeleton** + **mechanical hardening** (registries land + Pydantic SSOT + composite validator + release-gate wiring + Supabase mirrors). Per-row doctrine depth (the ~52 component-primitive doctrine pages at Shadcn-shape) waits for activation gate clearance. This is consistent with the candidate file's own §2.3 "registries land NOW; doctrine pages mature post-activation" posture.

## 5. Mechanical surfaces shipped at Wave L (this commit)

For consuming areas to ratify the pattern locally, the following mechanical surfaces are now in production:

1. **3 canonical CSV registries** at [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/) — 17 + 21 + 25 rows respectively.
2. **3 Pydantic SSOT models** at [`akos/hlk_output_type_registry_csv.py`](../../../../akos/hlk_output_type_registry_csv.py) + [`akos/hlk_artifact_class_registry_csv.py`](../../../../akos/hlk_artifact_class_registry_csv.py) + [`akos/hlk_component_primitive_registry_csv.py`](../../../../akos/hlk_component_primitive_registry_csv.py) — frozen module-scope regex + canonical fieldnames + Pydantic `Field` + `Literal` enums per `CONTRIBUTING.md` §"Python Code Standards".
3. **1 composite validator** at [`scripts/validate_output_architecture_registries.py`](../../../../scripts/validate_output_architecture_registries.py) — header drift checks + per-row Pydantic validation + cross-FK resolution against `AUDIENCE_REGISTRY.csv` + `DECISION_REGISTER.csv` + sibling registries; `--json-log` + `--quiet` flags + `akos.log.setup_logging`.
4. **1 Supabase migration** at [`supabase/migrations/20260521003459_i86_wave_l_output_architecture_mirrors.sql`](../../../../supabase/migrations/20260521003459_i86_wave_l_output_architecture_mirrors.sql) — 3 mirror tables in `compliance.*` schema with PK + CHECK constraints + RLS deny-all-except-`service_role` + governance views filtering for `status=active`.
5. **3 Supabase mirror tables populated** via [`scripts/sync_compliance_mirrors_from_csv.py`](../../../../scripts/sync_compliance_mirrors_from_csv.py) `--output-type-registry-only` / `--artifact-class-registry-only` / `--component-primitive-registry-only` flags. Row counts: 17 OT + 21 AC + 25 CP, FK-consistent with canonical CSVs.
6. **Release-gate wiring** in [`scripts/release-gate.py`](../../../../scripts/release-gate.py) (PASS/FAIL gate) + [`config/verification-profiles.json`](../../../../config/verification-profiles.json) `pre_commit` profile.
7. **`validate_hlk.py` umbrella** in [`scripts/validate_hlk.py`](../../../../scripts/validate_hlk.py) dispatch table.
8. **Tests** at [`tests/test_hlk_output_architecture_registries.py`](../../../../tests/test_hlk_output_architecture_registries.py) — 20+ valid/invalid pairs across the 3 models; registered under `@pytest.mark.hlk`.

## 6. Acceptance criteria per consuming area (binding)

For each consuming area to count as "having ratified the pattern locally":

- **Mechanical AC**: when `process_list.csv` schema gains an `inherited_pattern_id` column (forward-chartered with I-NN-OUTPUT-ARCHITECTURE P0; depends on activation gates A1+A2+A3), the area's process rows that produce 4-layer-architecture artifacts set the FK.
- **Documentary AC**: the area's role_owner SOPs that prescribe artifact authoring reference the relevant `ARTIFACT_CLASS_LIBRARY.md` §<code> sub-section by name (e.g. Brand Manager's brand-canon-maintenance SOP references `AC-DOCTRINE-CANONICAL`; PMO's master-roadmap authoring SOP references `AC-INITIATIVE-CHARTER` + `CP-DIAGRAM-MERMAID-FLOWCHART`).
- **Governance AC**: any new artifact-class or component-primitive proposed by the consuming area routes through this pattern's `ratifying_decision_id: D-IH-86-BB` + a successor sub-decision in `DECISION_REGISTER.csv` (no parallel registries minted in consuming-area `canonicals/dimensions/` for output-architecture concerns).

## 7. Open follow-ups (forward-chartered to next wave or initiative)

| Follow-up | Owner | Target wave / initiative | Notes |
|:---|:---|:---|:---|
| Mint `process_list.csv` schema column `inherited_pattern_id` (FK to PEOPLE_DESIGN_PATTERN_REGISTRY.pattern_id) | PMO + Compliance Officer | I71 successor or I80 P3 | Per `akos-people-discipline-of-disciplines.mdc` RULE 1 process-singularity-lever wiring |
| Run [`scripts/peopl_cross_area_breakthrough_announce.py`](../../../../scripts/peopl_cross_area_breakthrough_announce.py) | People Operations Lead | Next operator session | Per SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001 — automated propagation runbook fires when this announcement file lands |
| Charter promotion `_candidates/i-nn-output-architecture.md` → active master-roadmap | PMO + Brand & Narrative Manager | Future wave when activation gates A1+A2+A3 cleared | Promotion is correctly gated; do not force |
| Per-row doctrine pages for ~52 codes at Shadcn-shape | Brand & Narrative Manager primary + Front-End Developer co-owner | I-NN-OUTPUT-ARCHITECTURE P1+P2+P3 (multi-wave) | ~25-35 days total per candidate file §3.1 |
| Backfill existing artifacts with 4-layer frontmatter | PMO + Brand & Narrative Manager | I-NN-OUTPUT-ARCHITECTURE P4 | 15 touchpoint-kit files retro-tagged at Wave K; remaining ~30 advops engagement files at I-NN P4 |

## 8. Cross-references

- **Pattern row**: [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) `pattern_4layer_output_architecture_below_quality_fabric`.
- **Originating Wave K narrative**: [`docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md`](../master-roadmap.md) §1.9 "Wave K — 4-layer output architecture".
- **Wave L hardening narrative**: same master-roadmap.md §1.10 "Wave L — output-architecture hardening + UAT backfill".
- **Candidate forward-charter**: [`docs/wip/planning/_candidates/i-nn-output-architecture.md`](../../_candidates/i-nn-output-architecture.md).
- **Cursor rule binding**: [`akos-people-discipline-of-disciplines.mdc`](../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) RULE 1 (People mints patterns; consuming areas author processes).
- **Sibling pattern**: `pattern_register_csv_pydantic_validator_mirror` (mechanical surface) + `pattern_classification_lattice` (lattice inheritance) + `pattern_drift_gate_validator` (CI enforcement shape).
- **Worked exemplar mature pages**: [`OUTPUT_TYPE_LIBRARY.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/OUTPUT_TYPE_LIBRARY.md) §3.OT-PROSE-EMAIL-RICH (Wave K worked example for Layer 1) + [`ARTIFACT_CLASS_LIBRARY.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/ARTIFACT_CLASS_LIBRARY.md) §3.AC-COVER-EMAIL (Wave K worked example for Layer 2) + [`COMPONENT_PRIMITIVE_LIBRARY.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/COMPONENT_PRIMITIVE_LIBRARY.md) §3.CP-CTA (Wave K worked example for Layer 3 at Shadcn-shape).
