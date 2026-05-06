---
language: en
status: active
initiative: 59-hlk-governance-clean-slate
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-06
---

# Initiative 59 — Decision log

Fourteen decisions seeded. Operator-ratified at the I59 master-roadmap greenlight session 2026-05-06 ("Add ... extend with similar standpoint as DECISION_REGISTER ... All in one initiative or put all planned initiatives in this plan, you choose"). The decisions below govern P0 → P10 execution.

## D-IH-59-A — HLK governance promotion model: five dimensions land atomically

**Decision:** Five new HLK-governed compliance CSV dimensions (`REPOSITORY_REGISTRY`, `INITIATIVE_REGISTRY`, `OPS_REGISTER`, `CYCLE_REGISTER`, `DECISION_REGISTER`) land in a single P1 commit per the established same-commit pattern (`.cursor/rules/akos-governance-remediation.mdc` "compliance.*_mirror" rule). All five share design language; revert is atomic.

**Alternatives considered:**

- *Incremental ship: one dimension per cycle (I59=REPOSITORY+INITIATIVE; I60=OPS+CYCLE; I61=DECISION).* Rejected because (a) the five dimensions are FK-coupled (INITIATIVE.cycle_id → CYCLE; OPS.initiative_id → INITIATIVE; DECISION.linked_ops_action_ids → OPS; etc.), so partial inception requires placeholder columns + later ALTER TABLE; (b) the explore-subagent recon confirmed the HLK pattern is highly consistent — five repetitions is mechanical, not innovative.
- *Defer DECISION_REGISTER to I60.* Rejected per D-IH-59-E.

**Rationale:** Same-commit atomicity matches the established pattern (B.4 in I58 shipped 3 dimensions in one commit; I22a P7 shipped 17 mirrors in one cycle). Operator approval at G-59-A covers all five; revert is a single `git revert`.

**Reversibility:** Low after P1 commits land. Sync validators become load-bearing for downstream phases (P2/P3/P4 all consume the dimensions).

---

## D-IH-59-B — Two-layer SSOT: markdown for prose, CSV for governed metadata

**Decision:** Per-initiative `master-roadmap.md` files stay **canonical** for prose, phase plans, decision logs, evidence matrices. New `INITIATIVE_REGISTRY.csv` is **canonical** for governed metadata (status / FK joins / lifecycle). A new sync validator (`validate_initiative_registry_frontmatter_sync.py`) asserts both agree at every CI run.

**Alternatives considered:**

- *Markdown-only (status quo).* Rejected because metadata is not queryable; cross-repo coordination impossible; drift detection manual.
- *CSV-only (replace markdown).* Rejected because prose is irreplaceable for design rationale + decision context + verification matrices.
- *Markdown canonical, CSV mirrored (sync direction = MD→CSV only).* Rejected because operator can't bulk-edit status across many initiatives via CSV; bidirectional read-of-record is more useful.

**Rationale:** Same pattern as `goipoi_register.csv` ↔ markdown SOP citations + `REPOSITORIES_REGISTRY.md` ↔ (new) `REPOSITORY_REGISTRY.csv`. The sync validator makes drift a CI failure rather than a tribal habit.

**Reversibility:** Medium — sync validator can be loosened to advisory mode if operator pushback materializes; CSV stays canonical regardless.

---

## D-IH-59-C — REPOSITORY_REGISTRY.csv promotes the existing markdown SSOT

**Decision:** Existing `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` (markdown table) stays as the **operator-readable canonical** authoring surface. New `docs/references/hlk/compliance/REPOSITORY_REGISTRY.csv` (machine-readable) becomes the **governed canonical** schema-of-record. Drift gate via `validate_repository_registry_md_csv_sync.py`.

**Alternatives considered:**

- *Replace markdown with CSV.* Rejected because the operator-readable narrative format is valuable + cross-references rely on the MD file path.
- *Keep both as freestanding canonicals without sync.* Rejected because drift is inevitable.

**Rationale:** Recon confirmed the markdown is referenced in `PRECEDENCE.md` as the canonical Holistika-tracked GitHub index. CSV adds the FK target for `INITIATIVE_REGISTRY.repo_slug`, joins to `COMPONENT_SERVICE_MATRIX.repo_slug` + `REPO_HEALTH_SNAPSHOT.repo_slug`. Both stay canonical-class per `PRECEDENCE.md`.

**Reversibility:** High — CSV can be deleted and validators removed; markdown stays untouched.

---

## D-IH-59-D — Status taxonomy: seven values with companion-field rules

**Decision:** Seven enum values: `closed` / `archived` / `active` / `continuous` / `program_line` / `gated_external` / `gated_operator`. Each has a fixed companion field (`closed_at`, `archived_at`+`superseded_by`, none, `continuous_rationale`, `cadence`, `gated_on`, `gated_on`+`operator_action`). Single SSOT in `akos/planning/status_taxonomy.py` imported by both the frontmatter validator AND the `INITIATIVE_REGISTRY.csv` Pydantic schema.

**Alternatives considered:**

- *Three values (`open` / `closed` / `archived`).* Rejected because it cannot distinguish "active by design" (loop / program-line) from "active in execution" — the user's primary ask.
- *Five values (collapse `continuous` + `program_line` into `ongoing`).* Rejected because `continuous` (loop) and `program_line` (cadence-driven) have different operator implications + different dashboard sections + different freshness-canary semantics.
- *Free-form text.* Rejected as the status quo's failure mode.

**Rationale:** The seven-value vocabulary maps cleanly to dashboard sections (Active / Gated-external / Gated-operator / Continuous / Program-line / Closed / Archived). The Operator Inbox auto-collects from one specific value (`gated_operator`). Future cycles add new initiatives by picking one of seven.

**Reversibility:** Medium — taxonomy values can be added (forward-compat); removing a value requires migration.

---

## D-IH-59-E — DECISION_REGISTER folded into I59 (not deferred to I60)

**Decision:** `DECISION_REGISTER.csv` ships in I59 P1.5 (instead of being deferred to I60 candidate). `INITIATIVE_REGISTRY.inception_decision_id` and `closure_decision_id` are **real FKs** (not strings).

**Alternatives considered:**

- *Defer to I60: ship inception_decision_id as string column; ALTER to FK later.* Rejected because: (a) marginal cost is ~3-4h additional (same HLK pattern reused for the 5th time); (b) string-then-FK migration adds an extra cycle of validation; (c) DECISION_REGISTER's seed audit is best done while the I58 decision-log content is fresh in the agent's context.

**Rationale:** Folding it in NOW is strictly cheaper than deferring (forward-compat by design). User explicitly asked to "extend with a similar standpoint as above" → user is opting for inclusion.

**Reversibility:** Low — once shipped, FKs become load-bearing for any decision-trace queries.

---

## D-IH-59-F — Process_list harmonisation deferred to I60 (proposal only in I59)

**Decision:** I59 produces the **process_list harmonisation proposal** (`reports/p8-process-list-harmonisation-proposal-2026-05-06.md`) + drafts `SOP-INITIATIVE_PROCESS_HARMONISATION_001.md` at `status: review`. **No `process_list.csv` row mints in I59.** I60 candidate is the operator-approval-gated minting cycle (G-60-A through G-60-F per program tranche).

**Alternatives considered:**

- *Mint process_list rows in I59 P8.* Rejected because `.cursor/rules/akos-governance-remediation.mdc` is unambiguous: "Changes to `baseline_organisation.csv` or `process_list.csv` require explicit operator approval before committing." Each program tranche needs its own G-60-N gate.
- *Skip the proposal entirely; defer the question to I60.* Rejected because the proposal is the artifact that lets the operator schedule I60 efficiently — the per-initiative manifests_processes recommendations + tranche grouping save ~2-3 hours of analysis time at I60 start.

**Rationale:** Proposal is operator-content-gated **research**, not a mutation. I60 mints with proper tranche discipline.

**Reversibility:** High — proposal report can be revised before I60 mints; SOP at `status: review` until G-59-D allows it to flip.

---

## D-IH-59-G — `manifests_processes` semicolon-list FK column added nullable in I59

**Decision:** New `manifests_processes` column on `INITIATIVE_REGISTRY.csv` is a semicolon-delimited list of FKs to `process_list.csv`. **Nullable by default** in I59. I60 populates per tranche.

**Alternatives considered:**

- *Add column in I60 along with the mints.* Rejected because adding a nullable column in I59 is a free schema move that lets I60 ship faster.
- *Single-FK column (one process per initiative).* Rejected because cross-cutting initiatives manifest multiple processes (e.g., I58 = eval + governance + finance + brand).

**Rationale:** Forward-compat receiver column. Validator allows NULL.

**Reversibility:** High — column can be ALTER-dropped if model changes.

---

## D-IH-59-H — Two SOPs authored at v3.0 (governance + harmonisation)

**Decision:** Two new SOPs land under `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/`:

1. `SOP-INITIATIVE_GOVERNANCE_001.md` — initiative lifecycle reference (bootstrap → execution → status transitions → closure → archive)
2. `SOP-INITIATIVE_PROCESS_HARMONISATION_001.md` — process_list integration recipe + tranche-grouped candidate rows

Both authored at `status: review` in P1.6. **G-59-D at P9** flips both to `status: active` after operator approval.

**Alternatives considered:**

- *One combined SOP.* Rejected because lifecycle and harmonisation are different concerns; combined SOP would be too long + harder to maintain.
- *Defer harmonisation SOP to I60.* Rejected because the SOP IS the operator-readable artifact of the harmonisation proposal; landing it at `status: review` lets I60 approve + mint without re-authoring.

**Rationale:** Same-cycle landing of both SOPs ships the operator everything they need to evaluate I60 scope at G-60-A time. D-IH-17 invariance: agent never flips operator-authored canonical SOP `status:` field without approval (G-59-D is the trigger).

**Reversibility:** High — both SOPs at `status: review` are non-load-bearing until G-59-D ratifies.

---

## D-IH-59-I — OPS-58-3 path A: resolve persona in burn harness from `scenario.persona_id`

**Decision:** Implement OPS-58-3 via Path A: make `judge_calibration_burn.py` resolve persona from `scenario["persona_id"]` → `PERSONA_REGISTRY.csv` row → pass full persona dict to `JudgeRoster.score()` → `_heuristic_persona_fit` reads `typical_distance_band` / `typical_languages` / `qualification_gate` from the resolved persona.

**Alternatives considered:**

- *Path B: regex over scenario.expected_outcome_class.* Rejected — worse signal; couples persona scoring to outcome routing.
- *Path C: disable offline rubric when persona=None.* Rejected — hides the gap rather than fixing it; loses calibration signal.

**Rationale:** Path A is the cheapest fix that produces the strongest signal. Burn harness already has access to `PERSONA_REGISTRY` (it's loaded for scenario filtering). Wire-up is 1 helper function + 6 tests + re-run A.1+A.2 burns from I58 as evidence.

**Reversibility:** High — Path A is additive; if alignment fails to lift, can revert to current behavior (offline returns 3 by default) without breaking the multi-judge live API path.

---

## D-IH-59-J — Telemetry routine in operator's stead (proposal-only run in P7)

**Decision:** P7 runs `scripts/promote_telemetry_to_scenario.py --since-days 30` and produces `reports/p7-telemetry-triage-2026-05-06.md` with top-3 ranked clusters. **Auto-merge to `PERSONA_SCENARIO_REGISTRY.csv` is forbidden** per `artifacts/telemetry-proposals/README.md` design. P7 mints `OPS-59-1` row in `OPS_REGISTER.csv` pointing operator at the merge step.

**Alternatives considered:**

- *Skip P7 entirely (defer telemetry promotion to operator schedule).* Rejected because the script + triage is engineering work the operator already delegated; deferring means it never gets done.
- *Auto-merge in P7.* Rejected because `D-IH-17` (operator-content invariance) + `artifacts/telemetry-proposals/README.md` "Auto-merge is forbidden" are unambiguous.

**Rationale:** "You are the operator assistant, things you can do in my stead" (operator framing 2026-05-06) — generating proposals + triage is in stead; merging is operator's call.

**Reversibility:** High — proposals are gitignored artefacts; triage report is informational.

---

## D-IH-59-K — Operator approval gates G-59-A/B/C/D batched

**Decision:** Four operator approval gates spread across the cycle: G-59-A at end of P1, G-59-B at P3.6, G-59-C at P3.9, G-59-D at P9. Total operator review time ~2h spread.

**Alternatives considered:**

- *One mega-gate at P10 (operator approves everything at closure).* Rejected because it concentrates review cost into a single 4h+ session; also blocks downstream phases (P3 needs operator buy-in on the audit before flipping ~50 statuses).
- *Per-row approval (every CSV row).* Rejected as approval-gate fatigue.

**Rationale:** Batching matches the seed reports' design (each report has per-row rationale + cross-references; ~30-min reads).

**Reversibility:** High — gates can be re-batched mid-cycle if operator preference shifts.

---

## D-IH-59-L — `scripts/scaffold_initiative.py` stretch goal (defer to I60+ if effort exceeds budget)

**Decision:** A new `scripts/scaffold_initiative.py <slug>` helper that mints the next `initiative_id` + creates the planning folder + seeds six artefacts + appends INITIATIVE_REGISTRY.csv row is a **stretch goal** for I59. Lands if P1+P2+P3 finish under budget; defers to I60+ if not.

**Alternatives considered:**

- *Mandatory deliverable.* Rejected because manual initiative bootstrap takes ~30 min; not a critical path. Future automation can land any cycle.
- *Skip entirely.* Rejected because once INITIATIVE_REGISTRY exists, the marginal cost of the helper script is ~2h.

**Rationale:** Stretch positioning lets the cycle absorb effort drift without compromising core deliverables.

**Reversibility:** N/A — additive script.

---

## D-IH-59-M — Folder/role/artifact recommendations: keep convention; no new roles; codify in SOP

**Decision:** Per the operator's specific ask:

- **Folders:** keep `docs/wip/planning/<NN>-<slug>/` convention. Document in `SOP-INITIATIVE_GOVERNANCE_001.md`. Do **not** move WIP_DASHBOARD.md / OPERATOR_INBOX.md / README.md under a `_governance/` subfolder (purely cosmetic; would invalidate cross-references).
- **Roles:** existing `baseline_organisation.csv` covers everything (Founder, System Owner, PMO, Brand Manager, AI Engineer, etc.). Each new dimension's `owner_role_id` FK uses these existing rows. Forward-compat: split engineering/business/sponsor ownership via future ALTER TABLE if cross-functional needs surface.
- **Repo artifacts:** keep the six per-initiative artefacts (master-roadmap.md, decision-log.md, asset-classification.md, evidence-matrix.md, risk-register.md, reports/). Codify in the new SOP. **No new artefact-types.** The CSV layer is the only structural addition.

**Alternatives considered:**

- *Move governance files under `_governance/` subfolder.* Rejected — cosmetic; breaks cross-references; no functional gain.
- *Add new "Initiative Sponsor" / "PMO Lead" / "Cycle Coordinator" roles.* Rejected — existing roles cover; YAGNI.
- *Add per-artefact-type process_list rows.* Rejected — overkill; stays at initiative-as-deliverable granularity.

**Rationale:** Minimum-viable governance addition. The new dimensions provide all the structural power; folders/roles/artefacts stay stable.

**Reversibility:** High — recommendations are decisions to NOT change things.

---

## D-IH-59-N — I59 closure decision (recorded at P10)

**Decision:** Recorded retrospectively at P10 with the closure UAT verdict. Cycle ships P0 through P10 with all 22 verification-matrix checks PASS; flip `master-roadmap.md` `status: active` → `closed` with `closed_at`; flip `INITIATIVE_REGISTRY.csv` row for `INIT-OPENCLAW-AKOS-059`; flip `CYCLE_REGISTER.csv` row `CYC-59`.

**Alternatives considered:** N/A (closure decision; alternatives = "don't close" or "close partial").

**Rationale:** Standard closure ceremony per `D-IH-58-A` precedent.

**Reversibility:** Low — closed state is load-bearing for I60+ planning.

---

## Decisions made during execution

This section will be populated as P1 → P10 execute. Key execution-time decisions expected:

- D-IH-59-O+ (if needed): runtime course-corrections per the I58 D-IH-58-I precedent (e.g., model availability changes, mirror-emit edge cases, sync validator tuning).
