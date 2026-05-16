---
language: en
status: active
canonical: false
classification: way_of_working
intellectual_kind: decision_log
phase: P0
initiative: INIT-OPENCLAW_AKOS-80
authored: 2026-05-16
last_review: 2026-05-16
role_owner: People Operations Lead
ssot: false
companion_to:
  - master-roadmap.md
  - risk-register.md
  - reports/p0-charter-report.md
---

# I80 — Decision Log

> Workspace mirror of I80 charter-time and runtime decisions. Canonical row for each lands in [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) at the same commit; this file carries full rationale + decision_source per the I79 P0 precedent.

## Round 1 — P0 charter (2026-05-16)

### D-IH-80-A — I80 mega-charter (3-track lessons-learned absorption)

**Context.** I79 closed 2026-05-15 (D-IH-79-CLOSURE). Operator surfaced three lessons-learned at closure: (1) SOPs should read as plain-language as the manifesto/index — addendum concept invented to layer supporting documentation outside executor reading path; (2) stakeholder lenses (7 perspectives the agent surfaced post-closure) deserve canonical mint; (3) inline-ratify AskQuestion authoring quality was 3-month-equivalent brainstorming — should be transmitted to other agents via Cursor skill.

**Decision.** Mint I80 as a small charter-satisfies-gate initiative absorbing all three tracks under one closure. 8 phases (P0..P7); ~3-4 calendar days; single PAUSE at P7 closure; no real-stop pause for P1-P6 execution per `akos-inline-ratification.mdc` Round 5 worked-example posture (operator co-piloting in real-time).

**Rationale.** The three tracks are coherent (all flow from I79 closure observations); small enough to ship as one initiative without overloading scope; large enough to deserve initiative-level traceability (master-roadmap + decision-log + risk-register + closure pause record + files-modified CSV) rather than ad-hoc commits. Followup-commit option (precedent: I72 R-A..R-F regression amendment cycle) was considered and rejected because the work is **additive doctrinal expansion** rather than **post-closure regression amendment** — a structural distinction that warrants initiative ceremony.

**Reversibility.** Medium (initiative scope is bounded; track-level rollback possible per phase).

**Decision_source.** `operator_inline_explicit_via_askquestion` (AskQuestion `i80-packaging` selection `i80-candidate` with full reasoning chain).

**Closes.** Activates `OPS-80-1..OPS-80-7`.

---

### D-IH-80-B — SOP body/addendum naming convention: paired-file default

**Context.** Operator framing (verbatim): *"each area must speak their own jargon, that's ok. Data speaks data, tech speaks tech, finances the same, and people are plain terms because it's people."* The addendum concept layers extra documentation (especially **cross-area jargon**) outside the executor reading path. Three architectural options for instantiating the layered split at the file level: (a) single-file with `## Addendum` section; (b) paired-file `<name>.addendum.md`; (c) frontmatter-driven (mixed).

**Decision.** **Paired-file default** (`SOP-XYZ_001.md` body + `SOP-XYZ_001.addendum.md` addendum). Each file carries its own complete frontmatter (access_level, register, role_owner, classification, last_review, last_review_decision_id, methodology_version_at_review, ssot, intellectual_kind). Single-file remains the **degenerate case** when an SOP has no addendum-worthy content yet — body is fully self-sufficient.

**Rationale.** Operator's directive (verbatim): *"option B because it'll drive us to be DAMA ready, be sure that this is DAMA ready"*. Paired-file is structurally aligned with DAMA-DMBOK 2.0 across three knowledge areas:

1. **Metadata Management.** Paired files mean each artifact has a complete metadata row. KM ingestion pipelines (Supabase mirror, Neo4j projection, Obsidian vault, RAG pipelines, ERP panel filters, future external KM consumers) treat each file as a discrete row with discrete metadata. Single-file with `## Addendum` would force every consumer to *parse markdown structure* to separate body from addendum — fragile, custom per consumer, escalates to N consumers × N pipelines.
2. **Reference & Master Data Management.** Paired files enable independent versioning. Body might be reviewed annually; addendum (technical depth) might be reviewed per-major-event. Independent review cadences are an RMDM principle.
3. **Data Integration & Interoperability.** Supabase RLS becomes simpler — body mirror table at one access policy, addendum mirror table at a different policy. Query by classification, not by parsing. ERP panel filter routing becomes a join, not a regex.

Single-file alternative would couple body+addendum lifecycles, force markdown parsing in every downstream consumer, and complicate access-tier separation at the data layer.

**Reversibility.** Low (once paired-file is the default and SOPs migrate, reversing would require body+addendum recombination across the whole vault — costly).

**Decision_source.** `operator_inline_explicit_via_askquestion` (AskQuestion `sop-addendum-naming` selection `paired-file-default` with explicit DAMA-readiness rationale appended).

**Closes.** Activates `OPS-80-1`. Operationalised at P1 (pattern mint + SOP-META extension + jargon-gate refinement).

---

### D-IH-80-C — Stakeholder lenses paired-file shape

**Context.** Agent-surfaced 7-perspective stakeholder content (CPO / CTO / CEO / investor / cleared collaborator / apprentice + low-trust / regulator + personal vision) is evergreen onboarding/positioning material. Founder-reflection layer is meaningfully more sensitive than the stakeholder lenses themselves. Question: instantiate as single-file (level 4 monolithic), single-file with `## Addendum` (level 4 body + level 5 addendum section), or paired-files (level 4 body file + level 5 addendum file)?

**Decision.** **Paired-files**: `HOLISTIKA_STAKEHOLDER_LENSES.md` (level 4; 7 stakeholder lens sections + I76 forward-vision section) + `HOLISTIKA_STAKEHOLDER_LENSES.addendum.md` (level 5; founder-reflection layer + agent vortion). First instantiation of `pattern_sop_addendum_split` from D-IH-80-B; demonstrates the architecture at the canonical-mint moment (the lenses canonical is its own meta-demonstration of the doctrine that minted it).

**Rationale.** Operator framing (verbatim): *"I understand option A but I wonder if option C is even better because I think it ensures DAMA, scalability and makes ready for more knowledge management system in a lot of supports because of the granularity we have in option C. What do you think?"*. Agent confirmed: option C IS more DAMA-mature for the same three reasons as D-IH-80-B (Metadata Management + RMDM + Data Integration). Specifically for the lenses: ERP panel filter at level 4 returns the body; level 5 access surfaces the addendum as a separate panel slot. Independent review cadences (lenses annual + event_triggered; founder reflection per-major-event). KM ingestion is granular.

**Reversibility.** Medium (recombination possible if the addendum proves not to need separate access classification; one operator session to re-merge).

**Decision_source.** `operator_inline_explicit_via_askquestion` with agent-confirmed reasoning chain (AskQuestion `lenses-access-level` operator-leaning option C with "what do you think?" → agent confirmed).

**Closes.** Activates `OPS-80-2`. Operationalised at P2.

---

### D-IH-80-D — Retrofit scope: I80 pilots Option B; Option C forward-charter to I81

**Context.** Existing SOPs in the vault (pre-I80) were authored without the addendum concept. Many carry cross-area jargon in the body. Retrofit scope choice: (a) I79 only (3 files); (b) I79 + I73 lifecycle (8-10 files); (c) full v3.0 vault pass (~30+ files); (d) no retrofit, grandfather existing SOPs.

**Decision.** **Option B as pilot at I80** (I79 SOP retrofit at P4 + I73 lifecycle SOP retrofit at P5; ~8 files total). **Option C full-vault retrofit forward-chartered to I81 candidate stub** at P6 — operator directive: *"option B as pilot but help me achieve option C please"*.

**Rationale.** Option B at I80 demonstrates DAMA-readiness at scale (~8 paired-file pairs ship with full metadata; 5 of them are I73 lifecycle SOPs that are user-facing for People Operations). Option C as forward-charter to I81 candidate keeps the full-vault retrofit visible without overloading I80 scope. I81 can run as continuous initiative (precedent: I01 AKOS Full Roadmap) absorbing retrofit naturally over 6-12 months as each SOP hits its review cadence — no urgency pressure; quality over speed.

**Reversibility.** Medium per pilot file; low at scale (once paired-file default is established, reversing across 30+ files would be costly).

**Decision_source.** `operator_inline_explicit_via_askquestion` with forward-charter directive (AskQuestion `retrofit-scope` selection `i79-plus-i73-lifecycle` + free-text *"help me achieve option C"*).

**Closes.** Activates `OPS-80-4` + `OPS-80-5`. Forward-charter operationalised at P6 (I81 candidate stub).

---

### D-IH-80-E — Inline-ratify craft skill home: Cursor skill + rule extension

**Context.** Operator framing (verbatim): *"the inline questions were extremely helpful and even helped me brainstorm a lot — it was like advancing 3 months of me + Mark-II in a single initiative. I'd like you to help other agents nail them like you did."* Question: where to mint the agent-facing teaching artifact? Options: (a) extend `akos-inline-ratification.mdc` rule only; (b) mint Cursor skill `.cursor/skills/inline-ratify-craft/SKILL.md`; (c) mint SOP at PMO area; (d) all of (a)+(b).

**Decision.** **Cursor skill at `.cursor/skills/inline-ratify-craft/SKILL.md`** as the primary new artifact (~300 lines: principles + good/bad examples + worked checklist). **Plus** Cursor rule extension at `.cursor/rules/akos-inline-ratification.mdc` adding §"Quality bar" sub-section cross-referencing the skill (6-8 bullets: every option carries rationale; recommended-default marked when sensible; evidence cited inline by file:line; batched calls group tightly-coupled decisions; novel framings welcome when they help operator brainstorm; time-box recovery; etc.).

**Rationale.** Skills get read on-demand by agents who recognize the trigger ("I'm about to author an AskQuestion") — they're light enough to be teaching material. Cursor rules apply structurally and always. The two are complementary: rule = structural quality bar always-applied; skill = read-on-demand craft guide. SOP form was rejected because the audience is agents, not human operators executing a process — Cursor skills are the right artifact class.

**Reversibility.** High (skill is one file; rule extension is one section).

**Decision_source.** `operator_inline_default_accepted_via_skip` (operator's free-text directive set the goal; agent picked the artifact form per Cursor platform conventions; operator confirmation implicit through ratification of i80-packaging).

**Closes.** Activates `OPS-80-3`. Operationalised at P3.

---

### D-IH-80-F — Anti-jargon drift gate refinement: `*.addendum.md` glob exclusion

**Context.** I79 P2 minted `validate_design_pattern_registry.py --jargon-scan` mode scanning 6 People canonicals for 15 forbidden tokens (Tech Lab framework names + infra jargon + codenames). With paired-file addendum default (D-IH-80-B), addenda may legitimately carry cross-area jargon (the executor doesn't read them; auditors/system-owners do). Two implementation options: (a) parse markdown headings to detect `## Addendum` section and skip everything after; (b) glob-exclude `*.addendum.md` from scan scope.

**Decision.** **Glob-exclude `*.addendum.md`** from `validate_design_pattern_registry.py --jargon-scan` file-list assembly. Parsing markdown structure inside files would be fragile (heading variants, nested headings, missing headings); glob-exclusion at file selection time is mechanically simpler and structurally aligns with DAMA Data Integration (consumers of the canonicals operate at file-level, not section-level).

**Rationale.** File-level filtering is the same posture every other consumer (Supabase mirror, Neo4j projection, Obsidian vault, RAG pipelines, ERP panel filters) will adopt. Aligning the validator with the data integration boundary makes the codebase coherent across data + governance layers. Operator's DAMA-readiness directive (D-IH-80-B) generalises here.

**Reversibility.** High (one-line glob change in validator).

**Decision_source.** `agent_inline_default` (consequence of D-IH-80-B paired-file default; no operator option choice presented because the implementation is mechanical).

**Closes.** Activates part of `OPS-80-1`. Operationalised at P1.

---

### D-IH-80-G — Pattern_class taxonomy extension: `documentation_layering` as 11th class

**Context.** I79 P2 minted `PEOPLE_DESIGN_PATTERN_REGISTRY.csv` with 10-class `pattern_class` enum: register_dimension / paired_sop_runbook / lifecycle_taxonomy / cross_area_propagation / classification_lattice / dual_register / drift_gate / inline_ratify / forward_layout / adapter. The new `pattern_sop_addendum_split` doesn't fit cleanly into any existing class — it's about how documentation is layered for different reader audiences (executor vs auditor), not about register patterns or runbook pairing.

**Decision.** Add **`documentation_layering`** as 11th class to the `pattern_class` enum. Update Pydantic Literal in `akos/hlk_design_pattern_csv.py`. Update validator + tests. The new class anchors `pattern_sop_addendum_split` and forward-charters future patterns of the same shape (e.g., `pattern_executor_first_documentation` if a sibling pattern surfaces; `pattern_per_audience_view` for area-specific summaries).

**Rationale.** Forcing the pattern into an existing class would dilute that class's signal. `paired_sop_runbook` is about SOP+runbook pairing (executable artifacts); `dual_register` is about brand-vocabulary translation (internal vs external register). Documentation layering by reader audience is its own architectural shape.

**Reversibility.** High (Pydantic enum extension is additive; existing 12 patterns keep their classes).

**Decision_source.** `agent_inline_default` (taxonomy extension is mechanical consequence of new pattern; operator confirmation implicit through D-IH-80-A i80-candidate ratification).

**Closes.** Activates part of `OPS-80-1`. Operationalised at P1.
