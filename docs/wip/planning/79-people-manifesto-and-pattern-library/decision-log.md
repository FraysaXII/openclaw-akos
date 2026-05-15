---
initiative_id: INIT-OPENCLAW_AKOS-79
status: active
authored: 2026-05-15
last_review: 2026-05-15
owner_role: People Operations Lead
---

# I79 Decision Log

This log records every `D-IH-79-*` decision with full rationale + decision_source classification per [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc). The canonical mint of every row is in [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv); this file holds the human-readable rationale.

Decision_source vocabulary: `operator_inline_explicit_via_askquestion` (operator clicked / typed an explicit answer), `operator_inline_default_accepted_via_skip` (operator skipped the AskQuestion using "use my recommended default"), `operator_inline_text_response_via_askquestion_freeform` (operator typed free-text covering multiple gates).

## Round 1 — Initial AskQuestion batch (2026-05-15)

### D-IH-79-A — Mega-charter scope

**Question.** Is I79 a single multi-strand mega-initiative, or split into multiple smaller initiatives?

**Decision.** Single mega-initiative across **10 phases** (P0..P8 with P3 split into P3a + P3b post round 3). Strands A (manifesto), B (pattern library), C-People + C-Tech-Lab (AI governance, split), D (breakthrough propagation), E (orphan hygiene), F (process_list FK).

**Rationale.** Same logic that ratified I72 + I73 as mega-initiatives: cross-strand dependencies (manifesto → pattern library → AI doctrine → breakthrough SOP) only land coherently together. Splitting would require artificial dep-blocking + duplicate charter overhead.

**Reversibility.** Low.

**Decision_source.** `operator_inline_explicit_via_askquestion` (round 1 — "let's go all out, just make it clear that it's a follow-up of I73 and craft efficiently").

---

### D-IH-79-B — Manifesto home

**Question.** Where does the People manifesto live?

**Decision.** [`docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md). Status `active`, access_level 5 (internal-cleared), register `internal`. Public/external translation lives downstream in marketing canonicals (BRAND_VOICE_FOUNDATION, BRAND_BASELINE_REALITY_MATRIX) per existing dual-register discipline.

**Rationale.** Manifesto is People-area canonical, not Marketing-area canonical. Cross-area shareable, but People owns SSOT.

**Reversibility.** Medium (could relocate, but low value).

**Decision_source.** `operator_inline_default_accepted_via_skip`.

---

### D-IH-79-C — Pattern library shape

**Question.** Markdown narrative only, machine-readable CSV only, or both paired?

**Decision.** **Both paired by `pattern_id`**: [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) (queryable, FK target for process_list 8th col) + [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md) (human narrative for collaborator onboarding). Shared `pattern_id` is the join key.

**Rationale.** Reconciles process-singularity (need machine query) with KB human-readability (need narrative). Same dual-surface logic as I71 SOPs + I72 process catalog.

**Reversibility.** Low.

**Decision_source.** `operator_inline_explicit_via_askquestion`.

---

### D-IH-79-D — CSV registry home

**Question.** Where does `PEOPLE_DESIGN_PATTERN_REGISTRY.csv` live?

**Decision.** [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/) (alongside existing dimension CSVs: TOPIC_REGISTRY, GOIPOI_REGISTER, etc.). Pydantic SSOT at `akos/hlk_design_pattern_csv.py`. Validator at `scripts/validate_design_pattern_registry.py`. Mirror table `compliance.people_design_pattern_registry_mirror` at Supabase.

**Rationale.** Compliance/canonicals/dimensions is the established home for all queryable People+Compliance dimensions. Mirrors I72 PERSONA_REGISTRY + I73 ENGAGEMENT_MODEL_REGISTRY (sibling at People Operations) placement logic — Compliance for cross-area dimensions, People Operations for Operations-specific dimensions.

**Reversibility.** Low.

**Decision_source.** `operator_inline_default_accepted_via_skip`.

---

### D-IH-79-E — process_list 8th col `inherited_pattern_id`

**Question.** Add a nullable FK from `process_list.csv` to `PEOPLE_DESIGN_PATTERN_REGISTRY.pattern_id`?

**Decision.** **Yes**, at P6 with PAUSE (canonical CSV gate). Column nullable. Validator extension to `validate_hlk.py` enforces FK resolution when populated. Process-singularity lever: `SELECT COUNT(*) FROM process_list WHERE inherited_pattern_id = '<X>'` yields adoption surface.

**Rationale.** Without this column, the design pattern library is documentary only. With it, doctrine is countable. PAUSE is mandatory because canonical CSV gate per `akos-governance-remediation.mdc`.

**Reversibility.** Medium (could drop the column later but FKs would need migration).

**Decision_source.** `operator_inline_default_accepted_via_skip`.

---

### D-IH-79-F (round 1 wording superseded by D-IH-79-F-amended below) — AI governance

**Question (round 1).** AI governance home: People canonical only, or Ethics canonical only, or both paired?

**Decision (round 1, recorded for history).** Both paired — Ethics POSTURE + People SOP — with Madeira named-explicit + role-class footnote.

**Decision (round 3 — D-IH-79-F amended; see also D-IH-79-L + D-IH-79-M below).** Refactored into **three-part architecture**:

- **People-side (jargon-free)**: [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) + [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_AGENTIC_OPERATIONS_001.md) + paired runbook.
- **Tech Lab-side (jargon-bearing)**: [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) + [`SOP-TECH_AGENTIC_INFRA_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md) + paired runbook.
- **Ethics anchor (minimal red lines)**: [`ETHICAL_AGENTIC_BOUNDARIES.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md) — refuse-conditions, audit triggers, harm-prevention only.

**Rationale.** Operator's CPO insight (round 3): *"agentic is a discipline of disciplines, recursive"*; *"all jargon goes to Tech Lab"*. People canonicals practising the anti-jargon mandate is non-negotiable because People is the area that drives process-singularity through clarity. AI governance under one Ethics canonical would frame AI as external; the three-part split correctly mirrors People-as-DoD recursively into agentic-as-DoD.

**Reversibility.** Low (architectural).

**Decision_source.** `operator_inline_text_response_via_askquestion_freeform` (round 3 — "option A but all jargon goes to Tech Lab, please refine where and make it robust").

---

### D-IH-79-G — Madeira role-class footnote

**Question.** Name Madeira explicitly with role-class footnote, or refer abstractly to "AI O5-1 / current AIC"?

**Decision.** **Named-explicit + role-class footnote**: *"Madeira (current AI O5-1)"* on first mention; *"Madeira"* thereafter; first-mention footnote anchors the role-class semantics.

**Rationale.** Operator preference for concrete naming ("we may add another Madeira instance to give better support; the AICs are AICs"). Footnote handles forward-compatibility when role-class population grows (I76 lineage).

**Reversibility.** Low.

**Decision_source.** `operator_inline_explicit_via_askquestion`.

---

### D-IH-79-H — Cursor rule mint at P0

**Question.** Mint a new always-applied Cursor rule for People-as-DoD discipline, or fold into existing rules?

**Decision.** **Mint new rule**: [`.cursor/rules/akos-people-discipline-of-disciplines.mdc`](../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc), always-applied. Codifies People-as-DoD + agentic-as-DoD-recursive + jargon-goes-to-Tech-Lab + KB-stewardship-is-People + anti-jargon discipline + Madeira role-class pattern.

**Rationale.** This is exactly the architecture-level discipline the existing `akos-executable-process-catalog.mdc` and `akos-brand-baseline-reality.mdc` rules pattern after — cross-cutting, always-applied, ratified by an initiative. Folding into an existing rule would dilute both.

**Reversibility.** Low.

**Decision_source.** `operator_inline_default_accepted_via_skip`.

---

### D-IH-79-I — Cross-area breakthrough propagation SOP

**Question.** Codify pattern propagation in its own SOP or fold into the manifesto?

**Decision.** **Own SOP** at [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) with paired runbook [`scripts/peopl_cross_area_breakthrough_announce.py`](../../../../scripts/peopl_cross_area_breakthrough_announce.py). Includes explicit Tech Lab pingback when pattern row affects `AGENTIC_FRAMEWORK_LANDSCAPE.md` (round 3 amendment).

**Rationale.** Propagation is operational (event-triggered when a `PEOPLE_DESIGN_PATTERN_REGISTRY` row gets minted or revised). Per `akos-executable-process-catalog.mdc` Rule 1, every executable process gets a paired SOP+runbook. Folding into manifesto would lose mechanical discoverability.

**Reversibility.** Low.

**Decision_source.** `operator_inline_default_accepted_via_skip`.

---

### D-IH-79-J — Orphan housekeeping policy

**Question.** Apply blanket housekeeping policy (delete-if-stale or promote-to-canon) or case-by-case?

**Decision.** **Case-by-case via inline-ratify per cluster**. P5 produces inventory report, then fires per-cluster `AskQuestion` with operator choosing per cluster among {DELETE / PROMOTE / KEEP-WIP / KEEP-AS-REFERENCE}. PAUSE only if any DELETE approved (canonical-CSV-class gate posture for destructive mutations).

**Rationale.** Operator quote (round 2): *"it's case per case, depending on the findings, go ask me inline if you want me to choose, if you think we need to delete, ask me. otherwise all options are correct"*. Scope: 7 doc trees (`docs/wip/`, `docs/references/hlk/Research & Logic/`, `docs/references/hlk/previous-project-for-product-owner-example-only/`, `docs/uat/`, `docs/wip/intelligence/`, `temp-context/`, `Clients/`).

**Reversibility.** High (each cluster decision can be reversed; delete recoverable from git history).

**Decision_source.** `operator_inline_explicit_via_askquestion`.

---

### D-IH-79-K — `baseline_organisation` posture

**Question.** Add a new role row for "Knowledge Base Steward" (or similar) to `baseline_organisation.csv`?

**Decision.** **No.** KB-stewardship is absorbed into the manifesto §3 as a People-area-wide responsibility across every existing role. Future I-NN may revisit if a dedicated steward role emerges, but I79 does not mint a new baseline row.

**Rationale.** Operator quote (round 2 free-text): *"we don't need a baseline_organisation new role, KB-stewardship is People's responsibility across every role we have"*. Adding a single baseline row would imply ownership concentration when the operator's intent is distributed responsibility.

**Reversibility.** Low.

**Decision_source.** `operator_inline_text_response_via_askquestion_freeform`.

---

## Round 3 — Strand C amendment + Cursor rule confirmation (2026-05-15)

### D-IH-79-L — Strand C P3a/P3b split

**Question.** Should Strand C land as a single P3 phase or split into P3a (People + Ethics) and P3b (Tech Lab landscape)?

**Decision.** **Split into P3a + P3b**. P3a authors People doctrine + ops SOP + Ethics anchor (jargon-free; AL5; PAUSE for Ethics canonical mint). P3b authors Tech Lab landscape + agent-infra SOP (jargon-bearing; legitimate framework names). Sequential dependency: P3a → P3b so jargon-free shape is ratified before jargon-bearing companion lands.

**Rationale.** The two halves have different review surfaces (Ethics review vs Tech Lab system-owner review), different jargon postures (anti-jargon drift gate must pass for P3a only; P3b is exempt), and different ratification cadences. Splitting makes pause-point classification clean.

**Reversibility.** Low.

**Decision_source.** `operator_inline_explicit_via_askquestion` (round 3 click `split-p3a-p3b`).

---

### D-IH-79-M — Tech Lab landscape canonical ownership

**Question.** Where does `AGENTIC_FRAMEWORK_LANDSCAPE.md` live and who owns it?

**Decision.** [`docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md), `role_owner: System Owner` (Tech Lab plane). Sibling SOP at [`SOP-TECH_AGENTIC_INFRA_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md). New `canonicals/` subfolder under Envoy Tech Lab created at P3b (currently the area only has External Repos / Cross Repo / Repositories / MADEIRA-AKOS subdirs).

**Rationale.** Operator quote (round 3): *"all jargon goes to Tech Lab"*. Envoy Tech Lab is the AKOS-side stewardship area for Tech (System Owner role). New `canonicals/` is the natural home for Tech Lab SSOT; existing subdirs are operational not doctrinal.

**Reversibility.** Low.

**Decision_source.** `operator_inline_text_response_via_askquestion_freeform`.

---

### D-IH-79-N — Anti-jargon drift gate

**Question.** Mint an anti-jargon drift gate as part of `validate_design_pattern_registry.py`, or as separate validator, or skip and rely on operator review?

**Decision.** **Extend the existing pattern-registry validator with `--jargon-scan` mode**. Two scan modes (registry mode + jargon-scan mode) within one script; wired into `validate_hlk.py` umbrella + `verification-profiles.json` `pre_commit`. Mirrors I66 brand-baseline-reality drift gate pattern (proven shape).

**Rationale.** Mechanical enforcement is non-negotiable: People canonicals practising anti-jargon discipline must be CI-enforced, not operator-policed. Extending an existing validator (vs minting a separate one) keeps script count manageable and groups jargon-scan with its sibling registry-scan logically.

**Reversibility.** Low.

**Decision_source.** `operator_inline_explicit_via_askquestion` (round 3 click `yes-extend-pattern-validator`).

---

## Decisions deferred to per-phase inline-ratify

The following conundrums (`C-79-*`) are **not** ratified at P0; they will be inline-ratified during the relevant phase via `AskQuestion`:

| Conundrum | Phase | Topic |
|:---|:---:|:---|
| C-79-1 | P1 | Specific manifesto §3 phrasing for KB-stewardship-across-every-role |
| C-79-2 | P2 | Initial pattern library row count (operator preview) — likely 8-12 patterns from I59..I77 lineage |
| C-79-3 | P3a | Knowledge-test rubric specifics in `SOP-PEOPLE_AGENTIC_OPERATIONS_001.md` (5-10 KB lookup tasks) |
| C-79-4 | P3a | `ETHICAL_AGENTIC_BOUNDARIES.md` access level (operator preview — likely AL5 internal-cleared) |
| C-79-5 | P3b | Initial `AGENTIC_FRAMEWORK_LANDSCAPE.md` row count (which frameworks land in v1) |
| C-79-6 | P5 | Per-cluster orphan verdict (DELETE / PROMOTE / KEEP-WIP / KEEP-AS-REFERENCE) |
| C-79-7 | P6 | Initial `inherited_pattern_id` seed FKs across existing process_list rows (which patterns parent which processes) |
| C-79-8 | P7 | UAT row outcomes (Madeira knowledge-test + jargon-scan + landscape audit) |

Each conundrum is recorded here with operator's answer + decision_source after the inline-ratify gate fires. This pattern follows `akos-inline-ratification.mdc` discipline.
