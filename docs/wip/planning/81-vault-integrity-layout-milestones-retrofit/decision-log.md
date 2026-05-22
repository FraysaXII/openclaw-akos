# I81 — Decision log

Full rationale for every `D-IH-81-*` decision. Source-of-truth row lives in [`DECISION_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv); this file carries the human-readable narrative.

Cross-reference: [I81 master-roadmap §2](master-roadmap.md#2-charter-decisions-ratified-at-p0-agent-default-operator-skip-2026-05-16).

## P0 — ratified 2026-05-16 (`decision_source: agent_inline_default`; user confirmation 2026-05-16 evening: "answered all 18 questions; please continue")

### D-IH-81-A — Retrofit mode (continuous vs absorbed)

**Question:** Should the 40-SOP retrofit run as a continuous 5-8 day sprint or absorbed into per-area quarterly review?

**Options surveyed:**

- A: **Continuous** — single-initiative ~5-8 days; fastest closure; high context-switch risk.
- B: **Absorbed** — each area's role_owner retrofits during their existing quarterly canonical-review window. Slower aggregate closure but lower fatigue and better register-discipline preservation.

**Verdict:** **B — Absorbed.** Default per candidate §5 C-81-1. P4-P8 schedulable as parallel waves rather than forced linear sequence; allows role_owners to retrofit alongside other area work.

**Trade-off accepted:** I81 closure stretches across ≥ 2 quarterly cycles; mitigated by per-strand phase tracking (each P4-P8 phase closes when its strand is complete; the initiative closes when all five strands close).

### D-IH-81-B — No-addendum-needed threshold

**Question:** When does an SOP legitimately not need an addendum?

**Verdict:** Heuristic — body word-count ≥ 600 OR cross-area integration count ≥ 2 → addendum recommended. Below threshold: body-only acceptable; record `addendum_needed: false` in retrofit log. Per-pair author judgement is final (heuristic guides, doesn't gate).

**Expected outcome:** 10-30% of the 40 remaining SOPs end up body-only, narrowing actual paired-file count to ~28-36.

### D-IH-81-C — Author posture

**Question:** Each area's `role_owner` authors retrofits OR a single agent batch-retrofits all?

**Verdict:** **Each area's `role_owner` with agent assistance.** Preserves register-discipline expertise per area (Tech speaks tech; Marketing speaks brand-voice; Research speaks CORPINT; Compliance speaks classification-routing). Agent does mechanical scaffolding (split body → body + addendum.md; populate frontmatter; mint KNOWLEDGE_PAIRING row); role_owner reviews + signs off on register choices.

### D-IH-81-E — Per-area register-specific jargon-scan extension

**Question:** Should `validate_design_pattern_registry.py --jargon-scan` extend to non-People area canonicals (Marketing brand register; Tech framework register) using their own register-specific forbidden-token lists?

**Verdict:** **Out-of-scope for I81.** Per-area register-jargon is legitimate by design (the I79 doctrine explicitly carves out Tech jargon → Tech Lab; brand jargon → Marketing/Brand). Cross-area jargon contamination is a real risk but mechanical detection requires per-area forbidden-token list authoring upstream of the validator — that authoring is its own governance work, not I81 scope. Logged as future-gate candidate in P1 integrity report; no validator extension this run.

### D-IH-81-H — Named-milestone schema vocabulary

**Question:** What ID format for the named-milestone schema that replaces magic-number cross-references?

**Options surveyed:**

- A: `<I_ID>-<PURPOSE_SLUG>` — e.g., `I82-CAPABILITY-REGISTRY-MINT`. Simple, stable, no embedded sequence (phase position lives in frontmatter `milestones:` array, not the ID).
- B: `<I_ID>-M<NN>-<PURPOSE_SLUG>` — e.g., `I82-M02-CAPABILITY-REGISTRY-MINT`. Orderable but reintroduces magic numbers.
- C: `<I_ID>:<PURPOSE_SLUG>` — e.g., `I82:CAPABILITY-REGISTRY-MINT`. Colon awkward in markdown anchors.

**Verdict:** **A — `<I_ID>-<PURPOSE_SLUG>`.** Simplest stable form. `INITIATIVE_ID` matches `^I\d{2,3}$`; `PURPOSE_SLUG` is `UPPER-KEBAB-CASE`, ≤ 6 hyphenated tokens, semantically meaningful (not `PHASE-2`). Frontmatter `milestones:` array carries `id`, `phase` (informational `P\d+(\.\d+)?` mapping), `purpose` (1 sentence), `status` (`planned` / `in_progress` / `closed` / `cancelled`). Body headers retain `## P<N> — <name>` AND add `(milestone: I<NN>-<SLUG>)` parenthetical on first occurrence.

**Validation rule:** `scripts/validate_planning_cross_refs.py` (P3 deliverable) loads each plan's frontmatter `milestones:` and resolves every `I<NN>-<SLUG>` reference in body; fails loudly on unresolved IDs. Phase parenthetical drift (e.g., body says `(currently P2)` but frontmatter says `phase: P3`) is **warn-only** because the parenthetical is informational and the canonical ID is the FK.

**Finalisation:** If P3 migration of the first wave reveals corner cases, schema may be refined at P3 close.

## Deferred decisions (close at later phases)

| ID | Question | Owner | Close-out phase | Status |
|:---|:---|:---|:---|:---|
| D-IH-81-D | Forward-extension to non-SOP canonicals (registries + doctrines) | People Operations Lead | P9 | open |
| D-IH-81-F | Integrity matrix methodology + PASS threshold — what constitutes CLOSED-P1? | PMO + System Owner | P1 | **ratified 2026-05-19 at P1 close (Wave H lane-2)** |
| D-IH-81-G | Layout migration wave plan — which root files move in which tranche; deprecation-alias policy | Data Architect + Compliance Officer | P2 (per-tranche) | open |
| D-IH-81-I | Validator wiring scope + strictness — `validate_hlk.py` umbrella + `release-gate.py` + `pre_commit` profile + transition-window allowlist | System Owner | P3 | open |
| D-IH-81-J | Closed-initiative frozen-reference policy — closed roadmaps never retroactively migrated | PMO | P3 | open |

## P1 — ratified 2026-05-19 (Wave H lane-2 subagent stream)

### D-IH-81-F — Integrity matrix methodology + PASS threshold

**Question:** What constitutes the I81 P1 "vault integrity matrix" methodology + PASS threshold per the master-roadmap §3 P1 deliverable + §9 closure criteria?

**Verdict:** **5 coverage signals per executable row, aggregated to a 3-value verdict via deterministic `compute_verdict()`, with a 95% pass-rate threshold gated at I81 P9 closure UAT (NOT at P1 baseline).**

- **Executable predicate**: `item_granularity in {task, process}` per `process_list.csv` (1085 rows in the real corpus today).
- **5 signals**: `knowledge_pairing_status` (substring scan against KNOWLEDGE_PAIRING_REGISTRY.csv) + `paired_sop_status` (substring scan against v3.0 SOP corpus) + `mirror_coverage_status` (default `covered_by_emit` by construction; future commits can flip individual rows to `mirror_skip`) + `audience_tags_status` (deferred at P1 baseline; forward-charter to I85 wire follow-up) + `cadence_status` (lookup against the 4-value canonical enum per `akos-executable-process-catalog.mdc` RULE 3).
- **Verdict aggregation**: `pass` when ALL 5 signals in good state; `fail` when `mirror_coverage_status == mirror_skip`; `partial` otherwise.
- **PASS threshold**: 95% matches I71 + I80 retrofit precedent. Not enforced at P1 baseline (the audit runs as CI INFO advisory); strict-mode promotion gated at I81 P9 closure UAT when pass_rate has been lifted to ≥ 95% by P4-P8 retrofits + the I85 audience-tags wire follow-up commit.

Full rationale + reversibility in [`reports/2026-05-19-p1-closure.md`](reports/2026-05-19-p1-closure.md) §2.1.

### D-IH-81-K — I81 P1 vault-integrity baseline milestone closed

**Question:** Is I81 P1 (milestone `I81-VAULT-INTEGRITY-BASELINE`) ready to close?

**Verdict:** **Yes.** Deliverables landed per master-roadmap §3:

1. [`akos/hlk_kb_integrity.py`](../../../../akos/hlk_kb_integrity.py) — Pydantic chassis (2 models + 3 type aliases + ITEM_ID_RE + path constants; frozen + extra-forbid per `CONTRIBUTING.md`).
2. [`scripts/audit_kb_integrity.py`](../../../../scripts/audit_kb_integrity.py) — paired runbook per `akos-executable-process-catalog.mdc` RULE 1.
3. [`reports/i81/kb-integrity-matrix-2026-05-19.csv`](i81/kb-integrity-matrix-2026-05-19.csv) — 1085 executable rows × 12 columns.
4. [`reports/i81/kb-integrity-audit-2026-05-19.md`](i81/kb-integrity-audit-2026-05-19.md) — 8-section narrative + per-area distribution + top-gap analysis + next-action routing.
5. [`tests/test_audit_kb_integrity.py`](../../../../tests/test_audit_kb_integrity.py) — 26 tests at `@pytest.mark.hlk`; all PASS in 0.68s including 2 smoke tests against real corpus.
6. CI wiring (release-gate INFO advisory + verification-profile step).
7. [`reports/2026-05-19-p1-closure.md`](reports/2026-05-19-p1-closure.md) — closure report with 3 executive calls + reversibility documented per `akos-inline-ratification.mdc` recovery pattern.

I81 itself stays `active` per the absorbed-mode plan; P2-P9 remain open. Cluster sibling count unchanged at 7/13 closed.

**Reversibility:** Single-diff at three sites — (a) milestone frontmatter `status: closed → planned`; (b) revert audit-script commits; (c) mint a new `D-IH-81-REOPEN` decision row. Phase closures are reversible in principle but the underlying artifacts (chassis + audit + matrix + tests) are forward-only and any reopen would be a no-op unless the data sources change materially.

## Executive calls under D-IH-81-K (Wave H lane-2 subagent stream)

The subagent stream cannot post `AskQuestion` to inline-ratify; instead each architectural choice is documented with the 4-line executive-call pattern per [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) + [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc):

1. **5-signal methodology + 95% threshold (closes D-IH-81-F).** Operator override via heuristic change request or threshold tune. Full trace at [`reports/2026-05-19-p1-closure.md`](reports/2026-05-19-p1-closure.md) §2.1.
2. **Matrix as report-class, not canonical SSOT.** Operator override via PRECEDENCE row + Supabase mirror request. Full trace §2.2.
3. **Audience-tags wire forward-chartered to follow-up commit.** Operator override via authoring the join logic in `build_matrix_rows`. Full trace §2.3.


## P2 — Layout migration (deferred-decision D-IH-81-G; per-tranche operator-gated)

### D-IH-81-L — P2 Tranche T5: COMPONENT_SERVICE_MATRIX -> techops/ (2026-05-22)

**Tranche umbrella:** D-IH-81-G (deferred at P0; per-tranche operator-gating per akos-conflict-surfacing-and-blocker-trackers.mdc Option 5).

**Operator ratification:** Inline `AskQuestion` at Wave R lane batch (2026-05-22). After the agent surfaced five candidate I81 P2 tranches with risk profiles (T5 = single-file move + 4-file consumer surface = lowest-risk), the operator selected T5 first.

**Move:**

- Source: `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/COMPONENT_SERVICE_MATRIX.csv`
- Target: `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/techops/COMPONENT_SERVICE_MATRIX.csv`
- Rationale: Initiative 22 forward layout convention places CTO / component & service registers under `techops/`. Single file move (no rename); aligns first canonical of the forward target list.

**Deprecation alias:** Supported in `scripts/validate_component_service_matrix.py` + `scripts/validate_finops_counterparty_register.py` for one initiative cycle (validator falls back to legacy path when `techops/` path is absent). Alias removal scheduled for I81 P9 closure.

**Consumer surface (updated in same commit):**

| Surface | Type | Update |
|:---|:---|:---|
| `scripts/validate_component_service_matrix.py` | code | `MATRIX_CSV` path + alias fallback |
| `scripts/validate_finops_counterparty_register.py` | code | FK lookup path + alias fallback |
| `scripts/validate_hlk.py` | code | dispatcher entry path |
| `scripts/ingest_matriz_componentes_to_matrix.py` | code | `OUT` path |
| `.../canonicals/PRECEDENCE.md` | canonical | path + relocation note |
| `.../canonicals/CANONICAL_REGISTRY.csv` | canonical | `location` + `inception_at` + `notes` |
| `.../canonicals/README.md` | canonical | forward-target row + transition table |
| `.../Tech/System Owner/canonicals/SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001.md` | SOP | §1 + §3 path references |
| `docs/USER_GUIDE.md` | docs | HLK Operator Model rows |
| `docs/ARCHITECTURE.md` | docs | Component-and-service-matrix section |
| `docs/references/hlk/v3.0/index.md` | docs | HLK Registry table |
| `.../canonicals/migration-manifest-2026-05-12.yml` | canonical | append-only I81 P2 tranches section |

**Postgres mirror:** None for this CSV (validated via `rg COMPONENT_SERVICE_MATRIX` of `sync_compliance_mirrors_from_csv.py` + `validate_compliance_schema_drift.py`). No DDL migration required.

**Mechanical evidence:**

- `py scripts/validate_component_service_matrix.py`: PASS (97 components).
- `py scripts/validate_finops_counterparty_register.py`: PASS (2 rows; FK to `component_id` preserved).
- `py scripts/validate_hlk.py`: umbrella OVERALL PASS.
- `py scripts/validate_decision_register.py`: PASS (400 rows).

**Forward tranches (still gated by D-IH-81-G):**

- T1: `FINOPS_COUNTERPARTY_REGISTER.csv` -> `finops/` plane (operator discretion). **Blocked on FINOPS end-to-end synthesis pass** per Wave R lane batch operator framing 2026-05-22.
- T2: `ADVISER_ENGAGEMENT_DISCIPLINES.csv` + `ADVISER_OPEN_QUESTIONS.csv` -> `advops/` plane.
- T3: `FOUNDER_FILED_INSTRUMENTS.csv` -> `advops/FILED_INSTRUMENTS.csv` (rename + move; higher blast radius).
- ~~T4: `CHANNEL_TOUCHPOINT_REGISTRY.csv` -> `dimensions/` confirm (already correctly placed; verification-only tranche).~~ **Closed 2026-05-22 per D-IH-81-M (see below).**

Each remaining tranche requires its own inline-ratify gate at next push window.

### D-IH-81-M — P2 Tranche T4: CHANNEL_TOUCHPOINT_REGISTRY verification-only closure (2026-05-22)

**Tranche umbrella:** D-IH-81-G.

**Operator ratification:** Inline `AskQuestion` at Wave R lane batch (2026-05-22) paired with T5 selection. Operator picked option A (T4 + T1 in same push window) with the caveat that T1 must be preceded by a FINOPS end-to-end synthesis pass.

**Outcome:** Verification-only — no `git mv` was needed.

- `CHANNEL_TOUCHPOINT_REGISTRY.csv` was minted-in-place at `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/` from inception (Initiative 86 Wave F P3 2026-05-19; per `D-IH-86-Q` external-render strict-promotion + sibling 5-axis channel mint per `akos-external-render-discipline.mdc` RULE 7).
- All consumers point at the correct `dimensions/` path: validator (`scripts/validate_channel_touchpoint_registry.py` L34), [`PRECEDENCE.md`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) L86, [`CANONICAL_REGISTRY.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/CANONICAL_REGISTRY.csv) L53, `scripts/validate_external_render_trail.py` (resolves via Pydantic chassis import).
- No legacy root-level copy exists; no deprecation alias needed.

**Mechanical evidence:**

- `py scripts/validate_channel_touchpoint_registry.py`: PASS (10 rows).
- `py scripts/validate_external_render_trail.py --strict`: PASS (76 surfaces scanned; 6 channel-tagged; 0 unknown codes).
- `py scripts/validate_decision_register.py`: PASS (399 active + 2 superseded after this row appends).
- Full verification report: [`reports/i81/p2-tranche-t4-verification-2026-05-22.md`](reports/i81/p2-tranche-t4-verification-2026-05-22.md).

**Why this tranche was inventoried even though no migration was needed:** The I81 P2 enumeration walks every legacy Compliance canonical to confirm it either conforms to the I22 forward layout or schedules a `git mv` tranche. T4 closes the conform-by-construction case so future readers do not assume the work was skipped.

**Forward tranches still gated by D-IH-81-G:** T1 (FINOPS_COUNTERPARTY — blocked on operator engagement with FINOPS synthesis pass per Wave R framing), T2 (paired adviser-engagement CSVs), T3 (FOUNDER_FILED_INSTRUMENTS rename+move).
