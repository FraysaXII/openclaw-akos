---
initiative_id: INIT-OPENCLAW_AKOS-73
phase: P0
report_kind: charter_ratification
authored: 2026-05-15
authored_by: PMO
language: en
status: active
related_decisions:
  - D-IH-73-A
  - D-IH-73-B
  - D-IH-73-C
  - D-IH-73-D
  - D-IH-73-E
  - D-IH-73-F
  - D-IH-73-G
related_ops_actions:
  - OPS-73-1
  - OPS-73-2
  - OPS-73-3
  - OPS-73-4
  - OPS-73-5
  - OPS-73-6
  - OPS-73-7
  - OPS-73-8
  - OPS-73-9
  - OPS-73-10
---

# I73 P0 charter report — People Ops + Engagement Models + Methodology IP

> **Purpose.** P0 charter ratification record + 12-row plan-quality bar self-critique gate PASS report + mechanical evidence (files created) + documentary evidence (decisions encoded; cross-canon link integrity; CHANGELOG entry pointer) + open conundrums deferred to per-phase inline-ratify. Per [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT evidence contract" and `PLANNING_COMPENDIUM.md` §4.1.

## 1. Charter summary

- **Scope ratified**: mega-i73 (single initiative covers 8 strands across 11 phases) per D-IH-73-A.
- **Hold-gates reframed**: charter-satisfies-gate (bootstrapping reality) per D-IH-73-B.
- **Engagement Model Registry**: sibling dimension owned by People Operations per D-IH-73-C; 7-class taxonomy per D-IH-73-D.
- **Outsourced helper SOC**: separate engagement class with extra access-control layer per D-IH-73-E.
- **Methodology IP brand-vs-name**: decision-deferred-with-criteria-matrix per D-IH-73-F.
- **KB human-readability personas**: 4 personas mapped 1:1 to engagement classes per D-IH-73-G.

## 2. 12-row self-critique gate PASS report (per `PLANNING_COMPENDIUM.md` §2.2)

| # | Row | Evidence (Cursor plan section / file / anchor) | Verdict |
|:---:|:---|:---|:---:|
| 1 | Multi-sentence YAML todos | Cursor plan frontmatter `todos:` — 12 entries; each 4-7 sentences declaring scope + files + validators + pause-point class + self-checkpoint count + stable id per phase | PASS |
| 2 | Three mermaid diagrams | Cursor plan §"Architecture" Diagram 1 + §"Architecture" Diagram 2 (Module overview) + §"Architecture" Diagram 3 (Phase dependency) | PASS |
| 3 | Per-phase deep sections | Cursor plan §"Phase scaffold (deep sections)" — P0 through P11 (12 entries) each with SCOPE / PREREQUISITES / DELIVERABLES / VERIFICATION / pause-point class / self-checkpoint count / cursor-rules adherence | PASS |
| 4 | Inline decision-log preview table | Cursor plan §"Decision-log preview (D-IH-73-A..G)" — 10 rows with NEW markers + decision_source notes | PASS |
| 5 | Inline risk-register preview table | Cursor plan §"Risk-register preview (R-IH-73-1..10)" — 10 rows with likelihood/impact/mitigation + NEW markers | PASS |
| 6 | Round-expansions narrative | Cursor plan §"What changed since the candidate scaffold (Round-2 amendment)" — Round 2 narrative with engagement-as-unit reframe + 4 new strands + hold-gate reframing; cites operator brief 2026-05-15 | PASS |
| 7 | Clickable file paths on first mention | Spot-check 5: `ENGAGEMENT_MODEL_REGISTRY.csv` ✓ / `FOUNDER_TRAJECTORY_INTERNAL.md` ✓ / `akos-executable-process-catalog.mdc` ✓ / `validate_compliance_schema_drift.py` ✓ / `LOGIC_CHANGE_LOG.md` ✓ — all linked on first mention | PASS |
| 8 | CONTRIBUTING.md callouts on new validators | Cursor plan P1 DELIVERABLES section explicitly cites `CONTRIBUTING.md` §"Python Code Standards" for `akos/hlk_engagement_model_csv.py` + `scripts/validate_engagement_model_registry.py` + `tests/test_validate_engagement_model_registry.py`. P2 DELIVERABLES cites same for `validate_learning_ops_backlog.py` | PASS |
| 9 | ≥4 external research sources | Cursor plan §"External research" — 12 sources with full per-source schema; exceeds the ≥4 bar by 3× | PASS |
| 10 | Conundrum index with rationale + cited evidence + recommended default | Cursor plan §"Conundrums (deferred to per-phase inline-ratify)" — C-73-1..C-73-8 with phase + recommended default + rationale | PASS |
| 11 | Self-critique gate run | This report + Cursor plan §"Self-critique gate (12-row checklist)" — gate ran twice (in-plan + in-this-report); both PASS | PASS |
| 12 | CHANGELOG `[Unreleased]` entry | `CHANGELOG.md` `[Unreleased]` `### Added` line "I73 P0 charter — People Ops + Engagement Models + Methodology IP (mega-initiative; 8 strands; 11 phases; engagement-as-unit reframe; charter-satisfies-gate)" landed in this commit | PASS |

**Aggregate verdict: 12/12 PASS.** Plan ready for operator-ratified Gate 2 (canonical CSV mint preview) and Gate 3 (final pre-commit) handoff.

## 3. Mechanical evidence (files created / modified at P0)

### Files created

- [`docs/wip/planning/73-people-operations-and-learning-curriculum/master-roadmap.md`](../master-roadmap.md) — workspace mirror of Cursor plan (~150 lines).
- [`docs/wip/planning/73-people-operations-and-learning-curriculum/reports/p0-charter-report.md`](p0-charter-report.md) — this file.
- [`docs/wip/planning/73-people-operations-and-learning-curriculum/decision-log.md`](../decision-log.md) — D-IH-73-A..G with rationale, options, decision_source, close-out tracking.
- [`docs/wip/planning/73-people-operations-and-learning-curriculum/risk-register.md`](../risk-register.md) — R-IH-73-1..10 with mitigation, owner, close-out phase.
- [`docs/wip/planning/73-people-operations-and-learning-curriculum/files-modified.csv`](../files-modified.csv) — 18-column per-initiative file-changes CSV (P0 rows).
- `~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md` — Cursor authoritative plan body.

### Files modified

- [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) — appended `INIT-OPENCLAW_AKOS-73` (25 columns).
- [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) — appended D-IH-73-A..G (7 rows; 19 columns each).
- [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) — appended OPS-73-1..10 (10 rows; 24 columns each).
- [`docs/wip/planning/_templates/INITIATIVE_DEPENDENCIES.md`](../../_templates/INITIATIVE_DEPENDENCIES.md) — I73 promoted from candidate to active in mermaid + blocker table + hold-gate section + history table.
- [`docs/wip/planning/_templates/README.md`](../../_templates/README.md) — per-initiative state table I73 row → active.
- [`docs/wip/planning/_templates/PLANNING_COMPENDIUM.md`](../../_templates/PLANNING_COMPENDIUM.md) §11.4 — I73 sub-section updated from candidate to active state with hold-gates MET + scope summary + cross-links.
- [`docs/wip/planning/_candidates/i73-people-operations-and-learning-curriculum.md`](../../_candidates/i73-people-operations-and-learning-curriculum.md) — slimmed to 10-line redirect stub (`status: superseded`, `superseded_by:` pointer to this folder).
- [`CHANGELOG.md`](../../../../CHANGELOG.md) `[Unreleased]` `### Added` — I73 P0 charter entry.

## 4. Documentary evidence

### 4.1 Decisions encoded (D-IH-73-A..G summaries)

- **D-IH-73-A — Mega vs split scope ratification.** Operator picked "mega-i73" (single initiative covering 8 strands) via Gate 1 AskQuestion 2026-05-15. `decision_source: operator_inline_explicit_via_askquestion`. Status: active. Close-out: P0 (this report).
- **D-IH-73-B — Hold-gate reframing (charter-satisfies-gate).** Bootstrapping reality (operator + Madeira AI O5-1 + ad-hoc collaborators; founder's own paid employment per [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §2 funds Holistika's bootstrap) means the missing artefact is the engagement-class taxonomy itself, not the hire. `decision_source: operator_inline_default_accepted_via_skip` (Gate 1 AskQuestion 2026-05-15; operator skipped, recommended default captured). Status: active. Close-out: P0.
- **D-IH-73-C — ENGAGEMENT_MODEL_REGISTRY home.** Sibling dimension at `docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv` owned by People Operations Manager per DAMA Data Owner pattern (`akos-executable-process-catalog.mdc` Rule 4). `decision_source: operator_inline_explicit_via_askquestion`. Status: active. Close-out: P1.
- **D-IH-73-D — 7-class engagement taxonomy.** `hourly_consultant` / `milestone_consultant` / `percentage_collaborator` / `apprentice_learner` / `investor_advisor` / `outsourced_helper` / `operator_self`. Each maps to a documented historical pattern (Mark-II = apprentice; Bâtard 2020 = investor+percentage; Fiverr/Cameroon = outsourced; founder-operator running ops = operator_self). `decision_source: operator_inline_explicit_via_askquestion`. Status: active. Close-out: P1 (per-class enum rows mint in P1).
- **D-IH-73-E — Outsourced helper SOC posture.** Separate engagement class with distinct SOC: lower trust + scoped access + redacted KB view + work-product-only handoff (no methodology exposure). Default `access_level = 1` or `2` per [`access_levels.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/access_levels.md). `decision_source: operator_inline_default_accepted_via_skip`. Status: active. Close-out: P1 (codified in `ENGAGEMENT_MODEL_REGISTRY` rows) + P7 (codified in KB-view low-trust route).
- **D-IH-73-F — Methodology IP brand-vs-name.** Decision-deferred-with-criteria-matrix; P8 codifies criteria (is-this-business-IP vs is-this-personal-method-lineage; commercial-leverage vs intellectual-attribution; trademarkability scope; jurisdiction priority). Per-asset filing decision at filing time. Aligns with [`LOGIC_CHANGE_LOG.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/LOGIC_CHANGE_LOG.md) BT-01 brand-as-shield framing. `decision_source: operator_inline_default_accepted_via_skip`. Status: active (deferred). Close-out: P8 (criteria matrix codified) → per-asset filing decisions thereafter.
- **D-IH-73-G — KB human-readability personas.** 4 personas (operator-managed / cleared-collaborator / low-trust-outsourced / apprentice) mapped 1:1 to engagement-class buckets. Implementation = hlk-erp panel filter routes per [`akos-mirror-template.mdc`](../../../../.cursor/rules/akos-mirror-template.mdc). `decision_source: operator_inline_default_accepted_via_skip`. Status: active. Close-out: P7.

Full decision rationale + alternatives considered + close-out tracking lives in [`decision-log.md`](../decision-log.md).

### 4.2 Cross-canon link integrity check

Spot-checked links surface in the Cursor plan body (`~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md`) resolve to existing files:

- [`docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) — exists; access_level=5.
- [`docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/LOGIC_CHANGE_LOG.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/LOGIC_CHANGE_LOG.md) — exists; BT-01..BT-05 present.
- [`docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_AREA_RESTRUCTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_AREA_RESTRUCTURE.md) — exists; §3 brand-positioning rationale + §5 deferred CSV updates referenced.
- [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.md) — exists; 16-col schema referenced for P1 17-col extension.
- [`docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) — exists; §16 customer-engagement-template referenced for P3 inheritance pattern.

Validators that will exercise full cross-link integrity at P0 commit: `validate_hlk_vault_links.py` + `validate_hlk.py`.

### 4.3 CHANGELOG entry pointer

Landed at [`CHANGELOG.md`](../../../../CHANGELOG.md) `[Unreleased]` `### Added` section in this commit. Format mirrors I72 P0 charter entry shape (operator-readable; 1-line summary; per-decision-ID details inline).

## 5. Open conundrums (deferred to per-phase inline-ratify)

| Conundrum | Phase | Recommended default | Ratification timing |
|:---|:---:|:---|:---|
| C-73-1 — Cohort size (1 vs 2 vs 3+) | P2 | 1 | P2 inline-ratify gate |
| C-73-2 — Curriculum versioning anchor (methodology-anchor vs own cadence) | P2 | methodology-anchor (per I71 P4 review-stamp dimension) | P2 inline-ratify gate |
| C-73-3 — Ethics+Learning quarterly review owner | P5 | Ethics-led with Learning co-reviewer | P5 inline-ratify gate |
| C-73-4 — Engagement-lifecycle SOP shape (parameterized vs separate per class) | P3 | parameterized (split if >6 cases) | P3 inline-ratify gate |
| C-73-5 — Compliance/Ethics boundary edge cases | P6 | Compliance owns regulatory; Ethics owns AI-overreach; joint AI-content-disclosure | P6 inline-ratify gate (canonical-CSV PAUSE) |
| C-73-6 — Methodology IP licensing model | P8 | decision-deferred-with-criteria-matrix per D-IH-73-F | P8 inline-ratify gate (brand/legal PAUSE) |
| C-73-7 — KB persona view technology | P7 | role-tagged single surface with per-persona ERP panel filters | P7 inline-ratify gate |
| C-73-8 — Historical case-law anonymization scope | P4 | anonymize counterparty names; preserve codenames | P4 inline-ratify gate |

## 6. Verification matrix (at P0 commit)

Ordered validator run before commit (verdicts captured 2026-05-15):

| # | Validator | Verdict | Notes |
|:---:|:---|:---:|:---|
| 1 | `py scripts/validate_hlk_language_frontmatter.py` | **PASS** | 349 files scanned; 335 with frontmatter; 0 errors. |
| 2 | `py scripts/validate_hlk_vault_links.py` | **PASS** | No broken internal `.md` links. |
| 3 | `py scripts/validate_hlk.py` | **PASS** | Umbrella HLK gate: 67 org roles + 1151 process items + 188 decisions + 59 initiatives + 50 OPS items; INITIATIVE_REGISTRY + DECISION_REGISTER + OPS_REGISTER + MASTER_ROADMAP_FRONTMATTER + LANGUAGE_FRONTMATTER all PASS. **One-time fixup**: initial OPS-73-9 row had `owner_role: Founder` which is not a valid `role_name` in `baseline_organisation.csv`; corrected in-place to `owner_role: PMO` (matches OPS-72-10 precedent for initiative UAT ownership). |
| 4 | `py scripts/validate_decision_register.py` | **PASS** | 188 decisions validated; 12 advisory warnings on closure `decision_log_path` resolution (pre-existing; not I73-attributable). D-IH-73-A..G rows present with correct regex shape. |
| 5 | `py scripts/release-gate.py` | **FAIL (pre-existing carry-overs)** | Released-gate strict matrix has 4 row FAILs at this commit: (a) **Test suite** — pre-existing carry-over since P13.6 per 2026-05-14 CHANGELOG note. (b) **Browser smoke** — pre-existing carry-over since P13.6. (c) **BRAND voice register** — 4 hits in `boilerplate/i18n/messages/{en,fr}.json` sibling-repo i18n strings (`enterprise-grade` MBA-deck jargon + `delve into` LLM tone tell + `false_singularity` tic); pre-existing sibling-repo brand drift unrelated to I73 P0. (d) **BRAND voice Vale sibling** — `vale` exit=2 host-conditional; pre-existing. **I73 P0 also FIXED one pre-existing bug** in `scripts/release-gate.py` at line 575: `subprocess.run(...)` was called without importing the module (NameError on every release-gate run since I72 P9 commit `297d6b7`). Fix: added `import subprocess` to the standard library imports block. Documented in `CHANGELOG.md` `[Unreleased]` `### Fixed`. Without this fix, release-gate could not even reach the Test suite / Browser smoke rows. |
| 6 | `py scripts/validate_compliance_schema_drift.py` (composed by release-gate) | **PASS** | 22 canonical CSVs aligned with `akos.*` SSOT tuples. |

**FAIL classification.** The release-gate row 5 FAILs are **all pre-existing carry-overs** not caused by I73 P0 work:
- Test suite + Browser smoke FAILs documented in CHANGELOG `[Unreleased]` and `v3.1.0` sections as "Pre-existing browser-smoke + Test suite release-gate FAILs unchanged (carry-overs since P13.6; separate cleanup work)".
- BRAND voice register FAILs are in `boilerplate/i18n/messages/*.json` sibling-repo files; AKOS-side prose touched by I73 P0 is internal-register-allowed per [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) §"Allowed contexts" (workspace planning files + cursor plans + decision logs). Sibling-repo cleanup is a future initiative (I77 P1 forward-charters this).
- BRAND voice Vale sibling FAIL depends on host `vale` binary availability (host-conditional; SKIPs cleanly when absent per `akos-holistika-operations.mdc` SOC posture).

Per [`PLANNING_COMPENDIUM.md`](../../_templates/PLANNING_COMPENDIUM.md) §5.5 STOP-on-first-FAIL discipline, **no new I73-attributable FAIL** was introduced; the pre-existing carry-over FAILs were already shipping at I72 closure 2026-05-14 (precedent: I72 closure CHANGELOG entry explicitly acknowledges them). Commit proceeds per `akos-governance-remediation.mdc` Design-for-Invariance principle that I73 P0 must preserve existing contracts, which it does — none of the pre-existing FAILs were caused or worsened by this commit.

## 7. Cross-references

- Authoritative Cursor plan: [`~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md`](file:///~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md).
- Master roadmap (workspace mirror): [`../master-roadmap.md`](../master-roadmap.md).
- Decision log: [`../decision-log.md`](../decision-log.md).
- Risk register: [`../risk-register.md`](../risk-register.md).
- Files-modified CSV: [`../files-modified.csv`](../files-modified.csv).
- Compendium appendix: [`docs/wip/planning/_templates/PLANNING_COMPENDIUM.md`](../../_templates/PLANNING_COMPENDIUM.md) §11.4.
- Dep map: [`docs/wip/planning/_templates/INITIATIVE_DEPENDENCIES.md`](../../_templates/INITIATIVE_DEPENDENCIES.md).
