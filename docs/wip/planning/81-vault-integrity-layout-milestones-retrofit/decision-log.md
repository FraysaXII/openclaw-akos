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

- ~~T1: `FINOPS_COUNTERPARTY_REGISTER.csv` -> `finops/` plane (operator discretion). **Blocked on FINOPS end-to-end synthesis pass** per Wave R lane batch operator framing 2026-05-22.~~ **Unblocked 2026-05-22 per D-IH-81-N (synthesis ratification). Closed 2026-05-23 per D-IH-81-Q (see below) — Bundle A of three-bundle commit strategy; q1-a synthesis §6.2 amendment + q2-a atomic-commit + q5-a closure-class label all executed.**
- ~~T2: `ADVISER_ENGAGEMENT_DISCIPLINES.csv` + `ADVISER_OPEN_QUESTIONS.csv` -> `advops/` plane.~~ **Closed 2026-05-23 per D-IH-81-R under D-IH-81-G umbrella — Bundle D of three-bundle commit strategy; s2-a atomic-commit shape; move-only, no rename. Deprecation aliases preserved for one initiative cycle.**
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

### D-IH-81-N — FINOPS end-to-end synthesis ratification (2026-05-22)

**Tranche umbrella:** D-IH-81-G (T1 gating decision now unblocked).

**Operator ratification:** Inline `AskQuestion` four-question batch 2026-05-22 against the [502-line FINOPS end-to-end synthesis](reports/i81/p2-tranche-t1-finops-synthesis-2026-05-22.md). Operator picked: A1 (ratify synthesis as authored) + B1 (mint all 18 forward-charters as OPS rows now) + D1 (author CFOaaS activation policy now + engage CFOaaS firm at incorporation). Decision C resolved via novel-framing path captured in **D-IH-81-O** below.

**What the ratification commits Holistika to:**

1. **Synthesis becomes citable SSOT.** Future agents + future CFOaaS firm reads the synthesis at `reports/i81/p2-tranche-t1-finops-synthesis-2026-05-22.md` to onboard the FINOPS doctrine layer (5-plane inventory + ideal-vs-current gap + multi-perspective challenge + ideal-state architecture sketch + external grounding). Status flipped `review → active`; verdict flipped `PENDING-OPERATOR-WALK → PASS`.
2. **18 forward-charter OPS rows minted** as OPS-81-2 through OPS-81-19 (renumbered from the synthesis's narrative `OPS-81-FINOPS-1..18` labels to match the `validate_ops_register.py` `OPS-NN-N` regex). Severity breakdown: 5 CRITICAL (counterparty backfill / revenue recognition policy / founder ledger first-pass / capital instruments register / tax compliance calendar) + 9 HIGH + 4 MEDIUM/LOW. All rows `status:open` + `linked_decision_ids: D-IH-81-N`.
3. **CFOaaS activation policy** committed: engage at incorporation (not at first revenue, not at first capital, not at first board) — the conservative posture per `FOUNDER_CAPITALIZATION_DECISION_NOTE_2026-04` philosophy of *prevention over remediation*. Selection rubric: Spain-fluent + SaaS-fluent + ENISA-fluent + bilingual EN+ES. Pricing target: EUR 2-3.5K/month Essentials tier per industry consensus (Fractional CFO School 2026 + Level CFO 2026 + SaaS Fractional CFO UK 2026). Onboarding pack: this synthesis + `SOP-FOUNDER_COMPANY_FUNDING_001` + `FOUNDER_CAPITALIZATION_DECISION_NOTE` + 5 CRITICAL OPS rows + counterparty register backfill (OPS-81-2). Tracked as **OPS-81-17** (status:open until firm contracted + first monthly close runs). **SUPERSEDED-IN-NARRATIVE 2026-05-23 by D-IH-81-P** (see next row) — the CFOaaS-at-incorporation-default framing was an agent failure-mode (industry-default outsource-path reflex) inconsistent with the operator's internal-first project thesis; replaced by three-layer FINOPS ownership model (AT-Pymes gestoria for compliance bookkeeping per D-IH-89-L + operator+Madeira for judgment/reporting/policy/advisory internal-first + external recruitment as operator-reserved option activated by discrete triggers). The rest of D-IH-81-N (synthesis ratification + 18 OPS rows minted) stays active.
4. **T1 (FINOPS_COUNTERPARTY_REGISTER → finops/) unblocked** for execution in same push window per Decision C c1 default (cheap layout migration first; substantive backfill follows per OPS-81-2 sequencing).

**Reversibility:** Reversible at the OPS-row level — each forward-charter row can be closed individually if operator judges it no longer needed. Synthesis itself is `active` doctrine but may be amended in §10.1 Operator amendments log (which already carries this row's narrative + a forward-pointer to the next inline-ratify batch).

**External research grounding (per `akos-applied-research-discipline.mdc` RULE 2):** cited inline in synthesis frontmatter `external_references:` — Stripe 2026 rev-rec (primary + best-practices) + HighRock CPA 2026 + NetSuite 2026 + Fractional CFO School 2026 + Level CFO 2026 + SaaS Fractional CFO UK 2026 + Sincro 2026 + Vademecum Legal 2026 + AEAT 2026 + Supplier.io/TealBook/Semarchy 2026.

### D-IH-81-O — Cross-area Ops-wiring review novel framing (2026-05-22)

**Tranche umbrella:** spawned at FINOPS synthesis Decision C gate; companion to D-IH-81-N.

**Operator ratification:** At Decision C (T1 timing relative to substantive backfill) the operator declined the c1/c2/c3/c4 options and proposed a more consequential framing — verbatim: *"add regressions or continuous revisions or enhancements or backfill for all of this. Because FINOPS is a backbone, main representative of finance + legal + PeopleOps + other area's Ops, needs to be wired properly and cleverly to ensure we can grow our all ops as we go. Think you could review each area's OPS to ensure proper wiring maintenance etc. Mint this in the operator scratchbook too to ensure audit trail."*

**What this novel framing commits Holistika to:**

1. **A new emergent discipline named explicitly:** backbone-class Ops areas (FINOPS / PeopleOps / RevOps / LegalOps) are not just per-area operational disciplines — they are *wiring spines* that compose how every other area touches money / talent / customers / contracts. They require explicit cross-area wiring review beyond per-area maintenance.
2. **The candidate file [`_candidates/i-nn-cross-area-ops-wiring-review.md`](../_candidates/i-nn-cross-area-ops-wiring-review.md)** is minted now. It carries: 4-area backbone inventory (FINOPS / PeopleOps / RevOps / LegalOps); 4 illustrative cross-area wiring checks (FINOPS↔RevOps engagement-event pairing; FINOPS↔LegalOps money-amount back-references; PeopleOps↔FINOPS role-activation employment counterparty; RevOps↔LegalOps engagement-contract pairing); 15-item quartet expectations at promotion (per `akos-quality-fabric.mdc` RULE 7); 4-item anti-patterns. Activation gates: A1 operator sets criteria; A2 at least one backbone area reaches "wired-enough to be reviewable" maturity; A3 either CFOaaS firm contracted OR operator declares interim ownership explicit.
3. **Structural analogy:** the discipline is shaped like `INTER_WAVE_REGRESSION_DISCIPLINE.md` and `INDEX_INTEGRITY_DISCIPLINE.md` — instead of dimensions over a cluster wave or baseline indexes, dimensions over a backbone wiring surface. When promoted, ships the full Wave M/N specialty quartet (doctrine + Pydantic + validator + runbook + cursor rule + skill + SOP+runbook pair + pattern-registry row + Quality Fabric §6 row).
4. **T1 execution unblocked per default-c1 path:** layout migration first; substantive backfill (OPS-81-2 sweep) follows. The novel framing did NOT delay T1; it expanded the *what-comes-after-T1* picture.

**Reversibility:** Architectural framing not yet a mechanical discipline; promotion path: candidate → active initiative when activation criteria meet (similar shape to I79 People-as-DoD emergence from operator framing). Pairs structurally with `akos-people-discipline-of-disciplines.mdc` RULE 1 but generalises further: backbone-class areas require explicit cross-area wiring review beyond per-area discipline. Reversible: discipline can be folded into existing PMO + People area ownership if cross-area-review proves redundant at activation review.

**Audit-trail entry:** `docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md` 2026-05-22 wave-R-lane-D-T1-gate (per operator request *"Mint this in the operator scratchbook too to ensure audit trail"*).

**Forward tranches now in-flight under D-IH-81-G:** T1 (FINOPS_COUNTERPARTY — **unblocked** per D-IH-81-N, executes in same push window per c1 default), T2 (paired adviser-engagement CSVs — operator discretion), T3 (FOUNDER_FILED_INSTRUMENTS rename+move — operator discretion). The synthesis's 18 OPS rows now drive the FINOPS-substantive work surface independently of the layout-tranche surface.

### D-IH-81-P — Internal-first FINOPS posture amendment (2026-05-23; supersedes D-IH-81-N D-portion)

**Tranche umbrella:** spawned at FINOPS synthesis Decision H gate; companion + corrective overlay to D-IH-81-N.

**Operator framing (verbatim, from scratchpad 2026-05-23 16:58):**

> *"doctrine correction: internal-first FINOPS posture; AT-Pymes already covers the gestoría floor; CFOaaS is a reserved option, not the default."*

The operator surfaced the doctrine correction via scratchpad entry rather than a direct AskQuestion reply to Decision H, and named the three-layer FINOPS ownership model explicitly:

- **Layer A — compliance bookkeeping**: AT-Pymes gestoría contracted EUR 250 pre-paid bundle (months 0-12; renew or replace at month 12) per [D-IH-89-L](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) incorporation route. Monthly tax filings + autónomo societario quota management + basic accounting hygiene.
- **Layer B — judgment + reporting + policy authoring + advisory**: internal-first by operator + Madeira (AI O5-1) with external research grounding per [`akos-applied-research-discipline.mdc`](../../../.cursor/rules/akos-applied-research-discipline.mdc) RULE 1 + 2. Covers revenue recognition policy + capital structure + tax strategy + vendor concentration + board reporting.
- **Layer C — external recruitment** (CFOaaS / fractional CFO / hire): OPERATOR-RESERVED OPTION, NEVER default-at-incorporation. Activated when ANY of the discrete signals listed below fires.

**Ratification (inline-ratify P1-c + P2-b + P3-b + P4-a batch 2026-05-23 17:00 UTC+2):**

- **P1-c** — EXTENDED 8-item amendment scope (see synthesis §10.1 amendment entry for the full list).
- **P2-b** — 8 OPS rows amended (`OPS-81-3`, `OPS-81-6`, `OPS-81-7`, `OPS-81-8`, `OPS-81-9`, `OPS-81-10`, `OPS-81-17`, `OPS-81-18`) — each stripped of CFOaaS-default framing + encoded AT-Pymes-floor + internal-first-judgment + activation-trigger-gated recruitment.
- **P3-b** — concrete external-recruitment activation triggers committed (ANY of):
  - **INVESTMENT MILESTONE**: ENISA loan disbursed OR first investor SAFE/equity closed OR EUR 50K+ external capital received in 90d window.
  - **PROJECT COMPLEXITY**: Modelo 720 fires OR Hacienda Foral cross-territory split OR M&A discussion entered OR multi-CFO-grade engagement (Series A prep / audit / fundraise diligence).
  - **OPERATOR-JUDGMENT**: always-available override.
- **P4-a** — decision ID `D-IH-81-P` (sequential letter after D-IH-81-O).

**What the amendment commits Holistika to:**

1. **Three-layer FINOPS ownership model becomes canonical doctrine** — to be encoded as `FINOPS_INTERNAL_FIRST_POSTURE.md` canonical authored per OPS-81-18 (HIGH; bumped from MEDIUM per amendment).
2. **8 OPS rows reframed** — owner_class / owner_role / summary / notes columns rewritten to encode the three-layer model. OPS-81-17 downgraded from HIGH to MEDIUM (external recruitment is no longer the headline action). OPS-81-18 bumped from MEDIUM to HIGH (the internal-first posture canonical is the new headline action).
3. **OPS-81-20 minted** — forward-charters the internal-judgment-layer SOP+runbook quintet (revenue-rec policy + capital-structure posture + tax-strategy + vendor-concentration analysis + board-reporting cadence). HIGH; staggered execution one SOP+runbook pair per push window over 2-3 push windows.
4. **OPS-81-21 minted** — forward-charters the agent-recommends-outsource-path failure-mode guard: skill-craft principle addition to [`.cursor/skills/inline-ratify-craft/SKILL.md`](../../../.cursor/skills/inline-ratify-craft/SKILL.md) + cross-references in [`.cursor/rules/akos-inline-ratification.mdc`](../../../.cursor/rules/akos-inline-ratification.mdc) + [`.cursor/rules/akos-applied-research-discipline.mdc`](../../../.cursor/rules/akos-applied-research-discipline.mdc). Forwarded to I80 for execution; pairs with D-IH-80-E (skill-craft promotion). Cross-area Ops-wiring discipline implication: failure-mode sanity-check becomes part of every backbone-Ops-area sweep (per D-IH-81-O cross-area discipline emergence).
5. **D-IH-81-N D-portion superseded-in-narrative** — the CFOaaS-at-incorporation-default framing is replaced. D-IH-81-N row stays active because Decisions A (synthesis truth) + B (mint all 18 OPS rows) + C (cross-area Ops-wiring novel framing → D-IH-81-O) remain ratified.
6. **I-NN-CROSS-AREA-OPS-WIRING-REVIEW candidate §2 A3 gate amended** — the activation criterion "either CFOaaS firm contracted OR operator declares interim ownership explicit" is rewritten to remove the CFOaaS-default framing, replacing it with the three-layer model + activation-trigger framing per this decision.

**Why this matters beyond FINOPS:** the agent's reflexive industry-default outsource-path framing (CFOaaS for FINOPS) is a class of failure-mode likely to recur in future synthesis work for LegalOps / PeopleOps / RevOps / MarOps. The cluster coordinator + inline-ratify-craft skill must include the sanity-check (codified at OPS-81-21) at next People-area sweep. The cross-area Ops-wiring discipline (per D-IH-81-O) inherits the same sanity-check at promotion.

**Reversibility:** Medium. All underlying synthesis content stays; only ownership columns + activation timing re-frame. D-IH-81-N row remains active for A/B/C portions. If operator chooses to flip back to CFOaaS-at-incorporation at any future ratify cycle (e.g. an activation trigger fires + onboarding logistics dictate earlier engagement), the amendment can be reversed at the OPS-row level + synthesis §10.1 logged-in-place. No mechanical lock-in.

**External research grounding** (per `akos-applied-research-discipline.mdc` RULE 1): D-IH-89-L (AT-Pymes route confirmation 2026-05-18) provides the contracted-bookkeeping-floor evidence. RULE 2: internal-first thesis is the operator's own framing, not a novel industry framing — RULE 2 external citation requirement is satisfied by the prior synthesis's external-references list (Stripe 2026 + HighRock 2026 + Fractional CFO School 2026 etc.); no additional external citation required for the amendment itself.

**Audit-trail entry:** `docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md` 2026-05-23 16:58 marked [processed 2026-05-23] when this commit lands.

### D-IH-81-Q — P2 Tranche T1 closure: FINOPS_COUNTERPARTY_REGISTER → finops/ + synthesis §6.2 re-frame (2026-05-23)

**Tranche umbrella:** D-IH-81-G (closure-class child; sibling of D-IH-81-L for T5 + D-IH-81-M for T4).

**Operator ratification:** Inline `AskQuestion` five-question batch 2026-05-23 PM UTC+2 — `q1-a` (amend synthesis §6.2 NOW in same Bundle A for internal-first consistency) + `q2-a` (single atomic commit for T1 mirroring T5 precedent) + `q3-b` (cross-area Ops-wiring discipline → Bundle C forward-charter; promote candidate to charter — later refined to keep-as-candidate via r3-b agent_inline_default) + `q4-d` (counterparty backfill as Madeira-AI-assisted internal-judgment rehearsal → Bundle B forward-charter) + `q5-a` (closure-class decision label `D-IH-81-Q` under `D-IH-81-G` umbrella; preserve N/O/P letter gap as audit signal).

**Bundle A scope (this decision's actual surface)**:

1. **Synthesis §6.2 re-frame** (per q1-a): CFOaaS tier table re-headed as `"reserved-option reference (amended 2026-05-23 per D-IH-81-P)"` + reading-in-context preamble + AT-Pymes Layer (a) engagement description (EUR 250 bundle months 0-12 per D-IH-89-L) + when-the-reference-table-becomes-operationally-relevant prose tied to OPS-81-17 activation triggers + Holistika activation trigger column on the tier table + CFOaaS-onboarding-pack-assembly note + cost-arithmetic confirmation (EUR 24-42K/year saved by internal-first posture). Net effect: §6.2 now reads consistently with §6.1 + §6.4 internal-first framing; future readers cannot mistake the tier table for default architecture. Synthesis §10.1 "Operator amendments" log entry appended documenting the re-frame + T1 execution + Bundle B/C forward-pointers. Frontmatter `ratifying_decisions` appends `D-IH-81-Q`.

2. **T1 layout migration** (per q2-a): `git mv docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv → .../canonicals/finops/FINOPS_COUNTERPARTY_REGISTER.csv` (history preserved; aligns FINOPS canonicals under the I22 forward-layout `finops/` plane sibling to `techops/` minted at T5). 30+ consumer surfaces updated in lock-step in the same commit:
   - **5 validators** updated path + deprecation alias: `validate_finops_counterparty_register.py`, `sync_compliance_mirrors_from_csv.py`, `validate_compliance_schema_drift.py`, `validate_review_stamps.py`, `probe_compliance_mirror_drift.py`. Deprecation alias allows legacy path to resolve for one initiative cycle; removal scheduled for I81 P9 closure.
   - **1 dispatcher**: `validate_hlk.py` entry for `FINOPS_COUNTERPARTY_REGISTER` re-pointed to `finops/`.
   - **1 Pydantic SSOT**: `akos/hlk_finops_counterparty_csv.py` docstring + comments updated; tuple SSOT unchanged.
   - **1 test file**: `tests/test_sync_compliance_mirrors_from_csv.py` `_COUNTED_CSVS` path updated.
   - **4 canonical doctrine files**: `PRECEDENCE.md` (canonical row 31 + mirror lineage 127); `CANONICAL_REGISTRY.csv` (finops_counterparty_register location + inception_at + notes); `canonicals/README.md` (forward-layout tree + transition alias table); `migration-manifest-2026-05-12.yml` (`i81_p2_t1` wave entry appended + cross-reference note on wave-1 entry).
   - **4 cross-cutting docs**: `ARCHITECTURE.md` (HLK Registry section); `USER_GUIDE.md` (HLK Operator Model registry row); `index.md` (registry table link); `SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md` (two body references + transition note).
   - **Reviewed-no-change** (bare filename references): `DEVELOPER_CHECKLIST.md`, `GLOSSARY.md`, `SOP-FINOPS_BRIDGE_001.md`, `.cursor/rules/akos-adviser-engagement.mdc`, `.cursor/rules/akos-holistika-operations.mdc`.

3. **Closure-class decision label** (per q5-a): `D-IH-81-Q` under `D-IH-81-G` umbrella following sequential precedent (T5 = D-IH-81-L, T4 = D-IH-81-M, T1 = D-IH-81-Q). Letter gap N/O/P preserved as intentional audit signal for the synthesis interlude (N = synthesis ratification 2026-05-22, O = cross-area Ops-wiring novel framing 2026-05-22, P = internal-first FINOPS posture amendment 2026-05-23) that happened between T4 closure and T1 execution.

**Bundle B + Bundle C** (forward-chartered; execute in subsequent push windows with their own closure decision rows):

- **Bundle B** (per q4-d novel framing + r2-c hybrid default): Madeira-AI-assisted counterparty inventory pass. Obvious recurring SaaS subscriptions inventoried in one batch (operator approves with single AskQuestion); ambiguous counterparties (PCI scope questions, partner-vs-vendor ambiguity, multi-role) inline-ratified per row. Retrospective in OPS-81-20 close-out documents lessons from ambiguous rows only — that's where the judgment-layer actually fires. Closes OPS-81-2 + OPS-81-3 + provides OPS-81-20 internal-judgment-layer rehearsal evidence.

- **Bundle C** (per q3-b + r3-b + r4-c agent_inline_default): Cross-area Ops-wiring discipline stays at CANDIDATE status (existing `_candidates/i-nn-cross-area-ops-wiring-review.md`); activation criteria amended to "exercised on FINOPS (this synthesis = exercise #1) AND on ONE additional area's Ops surface (PeopleOps OR RevOps OR TechOps)"; promotion to full initiative + Quality Fabric 12th specialty charter on second exercise. This avoids the charter-then-defer anti-pattern that produced I86 cluster bloat. Quick 30-min research-sweep (per r4-c) adds external grounding to candidate body + external_references frontmatter (operational maturity models like CMMI; cross-functional KPI alignment frameworks; consulting-firm practice management; OKR-cascade methodologies) for `akos-applied-research-discipline.mdc` RULE 2 minimal compliance.

**Reversibility:** Low. T1 layout migration is a git operation captured atomically; rollback is `git revert` + validator re-run. Synthesis §6.2 amendment preserves all underlying content; only the framing-text changes. Decision row stays active; can be amended if Bundle B execution surfaces gaps in the framing.

**External research grounding** (per `akos-applied-research-discipline.mdc`): RULE 1 satisfied by T5 + T4 precedent (this is the third I81 P2 tranche execution; methodology proven). RULE 2 not applicable (no novel framing introduced by this closure — D-IH-81-N/O/P carried the novel framings; D-IH-81-Q is a mechanical execution + amendment closure).

**Mechanical evidence:**

- `py scripts/validate_finops_counterparty_register.py`: PASS (1 row at new `finops/` path).
- `py scripts/validate_hlk.py`: umbrella OVERALL PASS.
- `py scripts/validate_decision_register.py`: PASS (405 active + 2 superseded after D-IH-81-Q lands).
- `py scripts/validate_ops_register.py`: PASS (118 rows; 66 open + 52 closed; no row delta from Bundle A scope).
- `py -m pytest tests/test_sync_compliance_mirrors_from_csv.py tests/test_validate_review_stamps.py tests/test_validate_hlk_dispatcher.py`: 25/25 PASS.
- Pre-existing data-quality findings in `validate_review_stamps.py` (invalid `last_review_decision_id` for D-IH-82-S and OPS-86-14) are unrelated to T1 scope.

**Forward tranches still gated by D-IH-81-G:**

- **T2** (`ADVISER_ENGAGEMENT_DISCIPLINES.csv` + `ADVISER_OPEN_QUESTIONS.csv` → `advops/`) — operator discretion at per-tranche inline-ratify gate.
- **T3** (`FOUNDER_FILED_INSTRUMENTS.csv` → `advops/FILED_INSTRUMENTS.csv`; rename + move; highest blast radius) — operator discretion at per-tranche inline-ratify gate.

Tranche-status table updated: T1 flipped `unblocked → closed`. T5 + T4 + T1 = 3 of 5 tranches closed.

---

## D-IH-81-R — I81 P2 T2 ADVISER_* layout migration close

**Decided**: 2026-05-23. **Owner**: PMO. **Status**: active. **Class**: execution. **Reversibility**: medium (git-revertable, deprecation alias preserves legacy paths for one cycle).

**Parent umbrella**: `D-IH-81-G` (I81 P2 forward layout convention enforcement). Following the sequential precedent T5 = `D-IH-81-L`, T4 = `D-IH-81-M`, T1 = `D-IH-81-Q`.

**Question**: Execute T2 (`ADVISER_ENGAGEMENT_DISCIPLINES.csv` + `ADVISER_OPEN_QUESTIONS.csv` → `advops/`) as an atomic move-only commit per Bundle D of the Wave R lane-batch operator framing (per s2-a ratification 2026-05-22 + post-Wave-R-Lane-B-drain priority queue 2026-05-23).

**Decision**: Move both CSVs to `compliance/canonicals/advops/` as a single atomic commit. Move-only — no rename, no schema change. Deprecation aliases for one initiative cycle (removal scheduled at I81 P9 closure). T3 (rename + move FOUNDER_FILED_INSTRUMENTS → advops/FILED_INSTRUMENTS) deferred to a separate atomic commit with its own inline-ratify gate, given the higher blast radius (Pydantic module name, validator name, mirror table DDL all potentially affected by the rename).

**Mechanical scope** (atomic commit):

- 2 file renames (history preserved via `git mv`).
- 13 script path-constant updates with deprecation-alias pattern: `validate_adviser_disciplines.py`, `validate_adviser_questions.py`, `validate_review_stamps.py`, `validate_compliance_schema_drift.py`, `validate_program_id_consistency.py`, `validate_founder_filed_instruments.py` (FK reader), `validate_hlk.py` (dispatcher), `sync_compliance_mirrors_from_csv.py`, `probe_compliance_mirror_drift.py`, `export_adviser_handoff.py`, `render_pmo_hub.py`, `compose_adviser_message.py`, `tests/test_render_dossier.py`.
- 1 test-data-path update: `tests/test_sync_compliance_mirrors_from_csv.py` (`EXPECTED_PATHS` dict).
- 2 Pydantic SSOT docstring updates: `akos/hlk_adviser_disciplines_csv.py`, `akos/hlk_adviser_questions_csv.py`.
- 6 governance doc updates: `CANONICAL_REGISTRY.csv` (2 path cells), `PRECEDENCE.md` (4 path refs), `migration-manifest-2026-05-12.yml` (2 target paths), `compliance/canonicals/README.md` (tree comment + deferred-moves table), `docs/ARCHITECTURE.md` (HLK Registry CSV listing).
- 1 cursor rule update: `.cursor/rules/akos-adviser-engagement.mdc` frontmatter `globs:` (added new advops/ paths; kept legacy paths active for one initiative cycle so rule still activates on legacy-referenced docs).
- 3 active body-doc cross-reference updates: `_assets/advops/2026-holistika-incorporation/README.md`, `People/Legal/FOUNDER_FILED_INSTRUMENT_REGISTER.md`, `People/Legal/canonicals/FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md`.

**Mechanical evidence:**

- `py scripts/validate_adviser_disciplines.py`: PASS (6 rows at new `advops/` path).
- `py scripts/validate_adviser_questions.py`: PASS (12 rows at new `advops/` path).
- `py scripts/validate_compliance_schema_drift.py`: PASS (24 canonical CSVs aligned; both advops/* paths align to their SSOT tuples).
- `py scripts/validate_review_stamps.py`: PASS (adviser_engagement_disciplines 6/6 stamped; adviser_open_questions 12/12 stamped).
- `py scripts/validate_founder_filed_instruments.py`: PASS (FK reader on advops/ADVISER_ENGAGEMENT_DISCIPLINES.csv resolves correctly).
- `py scripts/validate_hlk.py`: umbrella OVERALL PASS.
- `py scripts/validate_hlk_vault_links.py`: PASS (no broken internal .md links after body-doc edits).
- `py -m pytest tests/ -x -q`: **3059 passed, 17 skipped, 17 warnings** (5m11s; full suite, no failures).

**Forward tranche still gated by D-IH-81-G:**

- **T3** (`FOUNDER_FILED_INSTRUMENTS.csv` → `advops/FILED_INSTRUMENTS.csv`; rename + move; highest blast radius — affects Pydantic module name `hlk_founder_filed_instruments_csv.py`, validator `validate_founder_filed_instruments.py`, mirror table `compliance.founder_filed_instruments_mirror`) — operator discretion at per-tranche inline-ratify gate. Recommended shape: surface explicit AskQuestion before execution with options for (a) move-only keep-name, (b) move + rename now, (c) defer to a successor initiative.

Tranche-status table updated: T2 flipped `pending → closed`. T5 + T4 + T1 + T2 = **4 of 5** tranches closed. T3 = last remaining tranche.

**External research grounding** (per `akos-applied-research-discipline.mdc`): RULE 1 satisfied by T5 + T4 + T1 precedent (this is the fourth I81 P2 tranche execution; deprecation-alias pattern proven across three prior tranches). RULE 2 not applicable (no novel framing introduced by this closure — D-IH-81-G/Q already carried the doctrine).

---

## D-IH-81-S — I81 P2 T3 FOUNDER_FILED_INSTRUMENTS rename+move layout migration close (Bundle D completion; I81 P2 5-of-5)

**Decided**: 2026-05-23. **Owner**: PMO. **Status**: active. **Class**: closure (per CSV) / execution (per markdown convention). **Reversibility**: medium (git-revertable; deprecation shims preserve old module + script names for one cycle; Supabase ALTER TABLE rollback via inverse migration).

**Parent umbrella**: `D-IH-81-G` (I81 P2 forward layout convention enforcement). Following the sequential precedent T5 = `D-IH-81-L`, T4 = `D-IH-81-M`, T1 = `D-IH-81-Q`, T2 = `D-IH-81-R`. T3 = the highest-blast-radius tranche; deferred to its own atomic commit with its own inline-ratify gate per D-IH-81-R closure note.

**Question** (inline `AskQuestion` 2026-05-23 PM UTC+2, post-T2 + post-Wave R Lane B drain): execute T3 (`FOUNDER_FILED_INSTRUMENTS.csv` → `advops/FILED_INSTRUMENTS.csv`) with what scope — move-only keep-name (least cleanup, max alias debt), move + rename CSV file only (medium), or full cascade rename CSV + Pydantic module + validator script + Supabase mirror table (max cleanliness, max blast radius)? And for the Supabase mirror, which strategy — keep current table name forever (alias-debt anti-pattern), rename via ALTER TABLE in same commit (atomic, requires aligned index + RLS handling), or defer to a successor initiative?

**Decision** (operator ratification `t3-a` + `sup-a` 2026-05-23): execute the **full cascade rename** with the **Supabase ALTER TABLE migration in same commit**. Scope:

- CSV: `git mv FOUNDER_FILED_INSTRUMENTS.csv → advops/FILED_INSTRUMENTS.csv` (history preserved).
- Pydantic SSOT: `akos/hlk_founder_filed_instruments_csv.py` → `akos/hlk_filed_instruments_csv.py`. Old module becomes a deprecation shim re-exporting the new tuple + model + valid sets for one initiative cycle (removal scheduled at I81 P9 closure).
- Validator: `scripts/validate_founder_filed_instruments.py` → `scripts/validate_filed_instruments.py`. Old script becomes a thin shim delegating to the new one for one initiative cycle.
- Supabase mirror: `compliance.founder_filed_instruments_mirror` → `compliance.filed_instruments_mirror` via ALTER TABLE migration `supabase/migrations/20260523000000_i81_p2_t3_alter_filed_instruments_mirror.sql`. Includes 4 index renames (PK + 3 secondary) + RLS policy drop+recreate with aligned identifiers (`ALTER TABLE RENAME` does NOT cascade to indexes or RLS policies in PostgreSQL; explicit handling required).

**Operator-discretion exemption** (stable downstream label): the `"founder_filed_instruments"` string in `scripts/validate_review_stamps.py` `CanonicalSpec.label` is **retained unchanged** as a stable identifier. Rationale: this label appears in `REVIEW_STAMP_INBOX.md`, historical UAT reports, and downstream tooling. Renaming the label would break review-stamp continuity with no operational benefit (the technical surface — file path + Pydantic module + validator script + mirror table — is fully renamed; the label is purely a stable string key). CLI flag `--founder-filed-instruments-only` on `sync_compliance_mirrors_from_csv.py` similarly retained for one cycle (now emits to renamed `compliance.filed_instruments_mirror` mirror table; flag rename scheduled at I81 P9 closure).

**Mechanical scope** (atomic commit):

- **1 CSV move-plus-rename**: `git mv` from canonicals/ root to canonicals/advops/ with renamed stem; history preserved.
- **2 Python module renames + 2 deprecation shims**: Pydantic SSOT + validator script; old names retained as shims for one cycle.
- **1 Supabase ALTER TABLE migration**: table rename + 4 index renames + RLS policy recreation with aligned identifiers (atomic in single migration file).
- **5 script path-constant updates with deprecation-alias pattern**: `sync_compliance_mirrors_from_csv.py` (path + mirror name + CLI flag name retained), `probe_compliance_mirror_drift.py` (path + mirror name in row-count SQL), `validate_compliance_schema_drift.py` (registry entry path), `validate_review_stamps.py` (CanonicalSpec path; label string kept stable), `validate_hlk.py` (dispatcher path + validator entrypoint).
- **18 governance + body-doc cross-reference updates**: `PRECEDENCE.md` (Layer 2 cite + mirror lineage row); `CANONICAL_REGISTRY.csv` (filed_instruments row path + notes); `migration-manifest-2026-05-12.yml` (T3 wave entry); `canonicals/README.md` (forward-layout tree + transition table); `ARCHITECTURE.md` (HLK Registry section); 3 cursor rules (`akos-adviser-engagement.mdc` globs + body refs; `akos-docs-config-sync.mdc` Code/Script changes table; `akos-holistika-operations.mdc` ADVOPS plane); 12 active body docs (`USER_GUIDE.md`, `DEVELOPER_CHECKLIST.md`, `EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md`, `SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`, `SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`, `SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`, `EXTERNAL_ADVISER_ROUTER.md`, `programs/PRJ-HOL-FOUNDING-2026/README.md`, `programs/PRJ-HOL-KIR-2026/README.md`, `Advisers/README.md`, `Advisers/_engagement-template/00-internal/README.md`, `Advisers/_engagement-template/02-adviser-pack/README.md`, `2026-holistika-incorporation/README.md` x2, `FOUNDER_FILED_INSTRUMENT_REGISTER.md` derived view, `FOUNDER_FACT_PATTERN_RELATED_ENTITIES.md`).
- **1 process_list.csv row update**: `thi_legal_dtp_304` (`Filed instruments register maintenance`) — canonical CSV path + validator script reference + last_review_at date updated to reflect T3 relocation/renaming. Column integrity verified post-edit (35 columns intact).

**Mechanical evidence:**

- `py scripts/validate_filed_instruments.py`: PASS (1 row at new `advops/FILED_INSTRUMENTS.csv` path).
- `py scripts/validate_founder_filed_instruments.py` (shim): PASS (delegates to renamed validator; legacy name still resolves for one cycle).
- `py scripts/validate_review_stamps.py`: PASS (filed_instruments 1/1 stamped under stable label).
- `py scripts/validate_program_id_consistency.py`: PASS (FK from filed_instruments to PROGRAM_REGISTRY resolves at new path).
- `py scripts/validate_hlk.py`: umbrella OVERALL PASS (all 24 canonical CSVs aligned with their SSOT tuples).
- `py scripts/validate_compliance_schema_drift.py`: PASS — 24/24 canonical CSVs aligned, including `advops/FILED_INSTRUMENTS.csv` → `akos.hlk_filed_instruments_csv.FILED_INSTRUMENTS_FIELDNAMES` (17 columns).
- `py scripts/sync_compliance_mirrors_from_csv.py --founder-filed-instruments-only`: emits INSERT/ON CONFLICT/UPDATE statements targeting `compliance.filed_instruments_mirror` correctly (verified via emitted SQL inspection — 3 mirror references, no residual `founder_filed_instruments_mirror` strings).
- `py scripts/probe_compliance_mirror_drift.py --emit-sql`: row-count SELECT now references `compliance.filed_instruments_mirror`; no residual references to old mirror name.
- `py scripts/validate_decision_register.py`: PASS (408 active + 2 superseded after D-IH-81-S lands).
- `py -m pytest tests/test_sync_compliance_mirrors_from_csv.py tests/test_probe_compliance_mirror_drift.py tests/test_validate_review_stamps.py -q`: 81/81 PASS.

**Why full cascade was the right call** (per operator `t3-a` ratification):

1. **Forward semantic clarity**: dropping the `FOUNDER_` prefix matches the broader-than-founder scope of the register (covers KiRBe SPV instruments, future entity-class instruments, banking arrangements, IP filings) — the canonical was named after founder-incorporation scope and outgrew it.
2. **One-time blast radius** vs. **forever alias debt**: a single commit with full cascade is cheaper than carrying the rename queue across multiple successor initiatives. The deprecation shim cost is bounded (one initiative cycle); the never-renamed alternative would have been unbounded.
3. **Atomic Supabase migration alignment**: doing the table rename in the same commit as the CSV rename keeps mirror name + canonical name in lockstep — operators reading either surface see the same identifier.
4. **Stable downstream label preservation**: the `founder_filed_instruments` label in `validate_review_stamps.py` is the only string that remained unchanged, by deliberate choice — review-stamp continuity for historical UAT reports and `REVIEW_STAMP_INBOX.md` matters more than label-name consistency. This is a healthy seam: the technical surface is cleanly renamed; the operator-facing identifier is stable.

**Reversibility:** Medium. Rollback path: `git revert` the atomic commit → file moves back, modules unrenamed, validators re-aliased; then run inverse Supabase migration (rename table back; recreate old indexes; recreate old RLS policies). Rollback complexity higher than T2 due to Supabase mirror table involvement, but bounded — the migration file documents the exact inverse operations needed.

**Forward tranches remaining under D-IH-81-G**: NONE. T5 + T4 + T1 + T2 + T3 = **5 of 5** tranches closed. **I81 P2 layout migration is complete.**

**External research grounding** (per `akos-applied-research-discipline.mdc`): RULE 1 satisfied by T5 + T4 + T1 + T2 precedent (this is the fifth and final I81 P2 tranche execution; deprecation-alias pattern proven across four prior tranches; Supabase ALTER TABLE pattern + RLS+index recreation is standard PostgreSQL discipline documented inline in the migration file). RULE 2 not applicable (no novel framing introduced by this closure).
