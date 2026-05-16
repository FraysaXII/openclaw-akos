---
language: en
sop_id: SOP-RENDERING_PIPELINE_GOVERNANCE_001
title: Document-rendering pipeline governance (catalog + paired SOP+runbook discipline)
area: Tech
role_owner: System Owner
co_owner_role: Brand & Narrative Manager
status: active
version: 1.0
inception: 2026-05-16
last_review: 2026-05-16
linked_initiative: INIT-OPENCLAW_AKOS-77
linked_decisions:
  - D-IH-77-I (visual UAT rendering discipline + orphan-rendering-pipeline governance discovery)
  - D-IH-77-G (I77 P4 scope expansion that mints this SOP)
canonical_dependencies:
  - docs/references/hlk/v3.0/Envoy Tech Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv
  - akos/hlk_rendering_pipeline_csv.py
  - scripts/validate_rendering_pipeline_registry.py
  - scripts/list_rendering_pipelines.py
governance_rules:
  - .cursor/rules/akos-executable-process-catalog.mdc (Rule 1: SOP+runbook pairing; Rule 2: status taxonomy; Rule 3: cadence taxonomy; Rule 4: DAMA Data Owner)
  - .cursor/rules/akos-brand-baseline-reality.mdc (every brand-token-consuming pipeline must respect dual-register contract)
  - .cursor/rules/akos-planning-traceability.mdc (per-initiative file-changes CSV must record additions to this registry)
methodology_version: v3.0
---

# SOP-RENDERING_PIPELINE_GOVERNANCE_001 — Document-rendering pipeline governance

## 1 — Purpose

Every document-rendering pipeline in the repo (Impeccable bridges, deck-HTML, dossier-PDF, Figma, PMO-hub, KM-diagrams, touchpoint-kit messages, cover-emails, visual UAT renders, ERP-sibling renders) is catalogued in [`RENDERING_PIPELINE_REGISTRY.csv`](../../../../People/Compliance/canonicals/dimensions/) and governed under this SOP + its [paired runbook](../../../../../../../../scripts/list_rendering_pipelines.py).

> Codifies decision **D-IH-77-I** (I77 P4 amendment 2026-05-16): brand-DNA-driven document-rendering started as orphan processes spawned per initiative (Impeccable I29, deck-HTML I27/I28, dossier-PDF I27, Figma I29, PMO-hub I25, KM-diagrams I25, UAT-dossier I48). I77 P4 promotes these from "ad-hoc per initiative" to "governed-scalable pattern" via this SOP + registry, so future initiatives that mint new rendering pipelines (e.g., MADEIRA persona-aware render, advisor-update touchpoint render) inherit the catalog + validator discipline by default.

## 2 — Scope

In scope:

- Any script under `scripts/` or `akos/` that produces an output file (HTML / PDF / SVG / PNG / Figma / markdown report) from a structured input (YAML / CSV / markdown / brand tokens).
- Any manual operator workflow that produces a document-class output (e.g., manual cover-email send) — these enter the registry as `status=planned` + `governance_class=orphan` until a paired runbook script lands.
- Any sibling-repo rendering pipeline (e.g., HLK ERP) — entered as `status=active` + `governance_class=partial` with cross-reference to the sibling-repo bless cycle.

Out of scope:

- One-off scripts under `scripts/legacy/` that produce derived analysis (not document-class output).
- Internal helper functions inside `akos/` modules that don't directly emit a deliverable file.
- Test fixtures + tooling under `tests/` (these are infrastructure, not deliverables).

## 3 — Schema (`RENDERING_PIPELINE_REGISTRY.csv`)

20 columns per `akos/hlk_rendering_pipeline_csv.py` SSOT:

| Column | Type / Enum | Notes |
|:---|:---|:---|
| `pipeline_id` | `^[a-z0-9_]{3,80}$` | stable kebab-or-snake-case slug |
| `name` | free text | human-readable |
| `trigger_type` | `on_demand` / `scheduled` / `event_triggered` / `gated_operator` | per Rule 3 cadence taxonomy |
| `trigger_command` | literal CLI or workflow | required (non-empty) |
| `owning_area` | area slug | matches `process_list.csv` `area` |
| `owning_role` | FK → `baseline_organisation.csv` `role_name` | data owner per Rule 4 |
| `status` | `active` / `inactive` / `planned` / `experimental` / `deprecated` | per Rule 2 |
| `brand_tokens_consumed` | `yes` / `no` | governs whether `akos-brand-baseline-reality.mdc` dual-register contract applies |
| `input_paths` | semicolon-list | required (non-empty) |
| `output_paths` | semicolon-list | required (non-empty) |
| `sop_path` | path or `TODO[I-NN-...]` | per Rule 1 SOP pairing |
| `runbook_path` | path or `TODO[I-NN-...]` | per Rule 1 runbook pairing |
| `linked_processes` | semicolon-list of `process_list.csv` `item_id` | empty for meta pipelines |
| `linked_decision_id` | FK → `DECISION_REGISTER.csv` | mint decision lineage |
| `governance_class` | `governed` / `partial` / `orphan` | snapshot of pairing + tests + validator coverage |
| `added_at` | YYYY-MM-DD | when row was added to registry |
| `last_review_at` | YYYY-MM-DD | per-row review cadence |
| `last_review_decision_id` | FK → DECISION_REGISTER | review traceability |
| `methodology_version_at_review` | `v3.0` / `v3.1` / ... | vault version at review time |
| `notes` | free text | drift signals, dependency notes, etc. |

## 4 — Cadence + governance ladder

### 4.1 — `governance_class` definitions

- **`governed`**: paired SOP + runbook exist + validator gates the schema + tests cover happy/sad paths + pipeline is wired into `release-gate.py` or `verification-profiles.json`. Example today: `impeccable_bridge_consumption` (I77 P2 chassis + drift gate + 19 tests).
- **`partial`**: runbook script exists but missing one of {SOP, validator, tests}. Example today: `company_dossier_html_deck` (script exists; this SOP is paired now; no dedicated validator for the YAML schema; tests live in `tests/test_company_deck.py`).
- **`orphan`**: manual workflow OR script with no SOP, no runbook variant, no validator. Example today: `touchpoint_kit_message_render` (currently manual operator copy-paste; `TODO[I-NN-peopl-outbound-send]` placeholder for the future runbook).

### 4.2 — Promotion paths

`orphan` → `partial`: when a runbook script is added OR a SOP is paired.
`partial` → `governed`: when ALL of {SOP, runbook, validator, tests} are paired.
`active` → `deprecated`: when a successor pipeline supersedes; original row stays as historical record with `notes` pointing to successor `pipeline_id`.

### 4.3 — When to add a row

A new row is added when ANY of the following ships:

- A new `scripts/<verb>_<noun>.py` that emits a document-class file (HTML/PDF/SVG/markdown report).
- A new `akos/<module>.py` helper that other render scripts depend on (e.g., `akos/hlk_pdf_render.py`).
- A manual operator workflow that the operator wants visible in the catalog (so it's not invisible-as-orphan).
- A sibling-repo rendering pipeline (registered with `status=active` + `governance_class=partial`).

## 5 — Inputs

| Input | Source |
|:---|:---|
| Registry CSV | [`RENDERING_PIPELINE_REGISTRY.csv`](../../../../People/Compliance/canonicals/dimensions/) (this SOP's SSOT) |
| Pydantic chassis | [`akos/hlk_rendering_pipeline_csv.py`](../../../../../../../../akos/hlk_rendering_pipeline_csv.py) — fieldnames + enums |
| Validator | [`scripts/validate_rendering_pipeline_registry.py`](../../../../../../../../scripts/validate_rendering_pipeline_registry.py) |
| Paired runbook | [`scripts/list_rendering_pipelines.py`](../../../../../../../../scripts/list_rendering_pipelines.py) |
| Decision lineage | `DECISION_REGISTER.csv` (D-IH-77-I + future review decisions) |

## 6 — Steps

### 6.1 — Register a new pipeline (human or AIC)

1. Determine the `pipeline_id` slug (matches `^[a-z0-9_]{3,80}$`).
2. Identify `owning_area` + `owning_role` (must exist in `baseline_organisation.csv`).
3. Classify `trigger_type` per Rule 3 cadence taxonomy.
4. Classify `status` per Rule 2 status taxonomy.
5. Classify `governance_class` per §4.1 above.
6. Decide `brand_tokens_consumed` based on whether the pipeline applies brand HSL palette + typography.
7. Identify `input_paths` + `output_paths` (semicolon-list; required non-empty).
8. Determine `sop_path` + `runbook_path` (either real paths OR `TODO[I-NN-...]` marker per akos-governance-remediation precedent for forward-charter scaffolds).
9. Note `linked_processes` (semicolon-list of `process_list.csv` item_ids; empty for meta).
10. Mint `linked_decision_id` in `DECISION_REGISTER.csv` if scope warrants a new decision row.
11. Append the row to `RENDERING_PIPELINE_REGISTRY.csv` (CSV append; alphabetical-by-pipeline_id is convention, not enforced).
12. Run `py scripts/validate_rendering_pipeline_registry.py` locally; must PASS.
13. Add a `tests/test_*` row covering the new pipeline if `governance_class=governed`.

### 6.2 — Review cycle (quarterly per akos-governance-remediation)

1. Run `py scripts/list_rendering_pipelines.py --all --format json` to enumerate.
2. For each row, verify:
   - `runbook_path` still resolves (script not renamed/removed).
   - `sop_path` still resolves.
   - `status` matches reality (active pipelines still run; deprecated pipelines actually retired).
   - `governance_class` reflects current pairing + test coverage.
3. Update `last_review_at` + `last_review_decision_id` per row reviewed.
4. Run `py scripts/validate_rendering_pipeline_registry.py` to confirm green.

### 6.3 — Promote orphan → partial → governed

1. Identify orphan rows via `py scripts/list_rendering_pipelines.py --governance orphan`.
2. For each, propose a paired runbook script (if absent) — open a phase plan + decision.
3. For each, propose a paired SOP (if absent) — author under `docs/references/hlk/v3.0/<area>/<role>/canonicals/SOP-<purpose>_<NNN>.md`.
4. When paired-runbook ships, flip `governance_class` from `orphan` to `partial`.
5. When validator + tests ship, flip to `governed`.

## 7 — Outputs

| Output | Sink |
|:---|:---|
| Validated registry CSV | git canonical SSOT |
| `py scripts/list_rendering_pipelines.py` | terminal markdown table or JSON (operator-facing) |
| `py scripts/validate_rendering_pipeline_registry.py` | PASS/FAIL stdout (release-gate-facing) |

## 8 — Failure modes

| Mode | Detection | Recovery |
|:---|:---|:---|
| Schema drift (column added/removed without updating Pydantic SSOT) | validator FAILs schema check | update `akos/hlk_rendering_pipeline_csv.py` first, then CSV |
| Duplicate `pipeline_id` | validator FAILs duplicate check | rename one row's `pipeline_id` |
| Broken `sop_path` / `runbook_path` | validator FAILs path-resolution check | fix path OR replace with `TODO[I-NN-...]` marker |
| Invalid enum value | validator FAILs enum check | correct cell |
| Pipeline ships but no registry row | quarterly review catches it via `py scripts/list_rendering_pipelines.py --all` cross-checked against `git ls-files scripts/render_*.py` | add row per §6.1 |
| Pipeline retired but `status` still `active` | quarterly review §6.2 | flip to `deprecated` |

## 9 — Verification

| Check | Command | Owner |
|:---|:---|:---|
| Schema + enum + FK validation | `py scripts/validate_rendering_pipeline_registry.py` | System Owner |
| Operator visibility into orphans | `py scripts/list_rendering_pipelines.py --governance orphan` | Brand Manager + System Owner |
| Brand-token coverage | `py scripts/list_rendering_pipelines.py --brand-tokens-only` | Brand Manager |
| Cross-area awareness | `py scripts/list_rendering_pipelines.py --owning-area Marketing/Brand` | Brand Manager |
| Tests | `py -m pytest tests/test_rendering_pipeline_registry.py -v` | System Owner |
| Release-gate integration | `py scripts/release-gate.py` (this validator runs at INFO level) | System Owner |

## 10 — Cross-references

- `.cursor/rules/akos-executable-process-catalog.mdc` — Rules 1-4 (this SOP operationalises every rule for the rendering-pipeline class)
- `.cursor/rules/akos-brand-baseline-reality.mdc` — dual-register contract applies to every brand-token-consuming pipeline
- `.cursor/rules/akos-planning-traceability.mdc` — per-initiative `files-modified.csv` must record additions to this registry
- `.cursor/rules/akos-holistika-operations.mdc` — new canonical CSV registers pattern (this registry follows that pattern)
- I77 master-roadmap §"P4 — Brand-canon collapse remediation + rendering-governance discovery" — origin
- I77 P4 UAT report at `docs/wip/planning/77-impeccable-brand-bridge-refresh/reports/uat-impeccable-all-surfaces-2026-05-16.md` §10 — orphan-rendering-pipeline discovery seed that this registry implements
- DAMA-DMBOK 2.0 Metadata Management knowledge area — status metadata is load-bearing for operator + agent decision-making
- Future I-NN candidate: rendering-pipeline productization (`@holistika/akos-render` library export per the I74 productization pattern when TRIGGER-2 fires)

## 11 — Change log

| Version | Date | Author | Change | Decision |
|:---|:---|:---|:---|:---|
| 1.0 | 2026-05-16 | Brand Manager + System Owner | Initial author. Seeded with 18 pipelines discovered during I77 P4.C orphan-process sweep. | D-IH-77-I |
