# I82 — Decision log

Full rationale for every `D-IH-82-*` decision. Source-of-truth row lives in [`DECISION_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv); this file carries the human-readable narrative.

Cross-reference: [I82 master-roadmap §2](master-roadmap.md#2-charter-decisions-ratified-at-p0-agent-default-operator-skip-2026-05-16).

## D-IH-82-I — Talent P1 split-tree architecture (Q3 Wave 2 ratify)

**Source**: Operator inline ratify 2026-05-16 (Wave 2 Q3 batch); see [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/q1-q6-ratify-2026-05-16.md`](../../86-initiative-cluster-execution-coordinator/reports/q1-q6-ratify-2026-05-16.md).

**Question**: I82 P1 Talent activation — mint as a monolith (Talent role + sub-roles), defer entirely to I76 (MADEIRA elevation) for AI-side discipline, or split into Talent-Human (Talent-H) + Talent-Artificial (Talent-A) sub-trees from day-one?

**Options considered (per the AskQuestion batch)**:
- (A) `approve-now-human-only` — human-side rows only; AI Talent deferred to I76.
- (B) `approve-now-both` — combined: human-side rows + AI Talent slot linked to I76.
- (C) `defer-to-i76-first` (recommended at the time) — pause Talent canonical mint until I76 P0 lands; clean post-MADEIRA mint.
- (D) `split-talent-tree` (novel framing) — split into Talent-H + Talent-A sub-trees from day-one; each canonical row carries explicit class axis; AI-side rows forward-reference I76 candidate.

**Verdict**: **D — split-talent-tree**. Operator selected the novel framing. Rationale (operator-implicit): clean separation from day-one means the canonical CSV row schema carries an axis distinguishing human vs AI capability-bearers; each row knows its own class; cross-area cross-references stay typed; the I76 MADEIRA elevation lands cleanly as Talent-A rows (no schema migration needed when I76 promotes).

**Architectural implications**:

1. **`baseline_organisation.csv` row mint at P1** carries TWO role-name conventions:
   - **Talent-H** roles: human-bearer roles (e.g., "Talent Lead — Human Operations" or whatever the doctrine names them) with `reports_to=CPO`, `area=People`, `sub_area=Talent`, `status=active`.
   - **Talent-A** roles: AI-bearer roles (forward-reference to I76 MADEIRA elevation; e.g., "Talent Slot — Madeira (AI O5-1)") with `reports_to=Founder` (per [`akos-people-discipline-of-disciplines.mdc`](../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) RULE 5 — Madeira named-explicit), `area=People`, `sub_area=Talent`, `status=planned` (until I76 P0 charter lands), with explicit cross-reference to I76 in `role_full_description`.

2. **`process_list.csv` Talent rows at P1 sub-tranche** likewise carry the class axis — `Talent-H` process_ids prefixed `hol_peopl_talent_h_*`; `Talent-A` process_ids prefixed `hol_peopl_talent_a_*`. Process descriptions name the bearer class explicitly.

3. **`HOLISTIKA_CAPABILITY_DOCTRINE.md` (P0 followup)** must articulate the split — adds §"Capability bearer classes" with Talent-H + Talent-A axes; cross-references [`akos-people-discipline-of-disciplines.mdc`](../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) RULE 3 (agentic-as-DoD).

4. **Cross-reference to I76**: when I76 P0 charter lands, Talent-A `status` flips from `planned` → `active`; explicit forward-link recorded in `last_review_decision_id` of the Talent-A rows.

**Verdict prerequisites** (all blocking P1 operator-gate fire):

1. `HOLISTIKA_CAPABILITY_DOCTRINE.md` minted at `status: review` (P0 followup) — currently NOT minted; deferred to sc-resume-wave2-architectural.md per Q6.
2. Doctrine §"Capability bearer classes" authored explicitly naming Talent-H + Talent-A axes.
3. Talent role-name conventions decided (operator co-sign with Brand & Narrative Manager).
4. I76 P0 charter exists at least as `status: candidate` for the Talent-A forward-reference to point at — I76 candidate exists at [`_candidates/i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md) per I76 forward-charter; PASS.

**Closes**: Q3 architectural fork. **Activated**: 2026-05-16 (architecture-only; canonical rows pending P1 operator gate after doctrine mint). **decision_source**: `operator_inline_ratify` (not default).

**Cross-link**: This decision shapes the I82 P1 phase definition; master-roadmap §3 P1 description is updated in the same commit to reflect the split-tree posture.

## P0 — ratified 2026-05-16 (`decision_source: agent_inline_default`; user confirmation 2026-05-16 evening: "answered all 18 questions; please continue")

### D-IH-82-A — Mega-charter scope (4-facet doctrine vs split)

**Question:** Should the four named instruments (capability inventory + confidence rating + use case archive + eloquence translation) cohere as a single doctrine with 4 facets, OR split into separate initiatives?

**Verdict:** **Single 4-facet doctrine.** Per operator Round 9 framing (verbatim): *"My motto: Concept to Use Case to Eloquence. We build capabilities, research use cases that are hot, actually do them with production-grade quality and translate them to operator, expert, user and business."* The four instruments form one coherent meta-capability (audience-aware capability surfacing); splitting them creates artificial seams that operators would have to constantly cross-reference.

**Trade-off accepted:** I82 has 7 phases. Mitigated by D-IH-82-SEQUENCE staging (doctrine P0 → Talent P1 → registries P2-P4 → translation P5 → integration P6 → UAT closure P7).

### D-IH-82-B — Doctrine canonical home

**Question:** Where does `HOLISTIKA_CAPABILITY_DOCTRINE.md` live?

**Verdict:** **`docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/`** — same path as existing two doctrines. Sibling to ORGANISING + AGENTIC, completing the "how we structure / how AI fits / how we surface what we do" triad. Per [`akos-people-discipline-of-disciplines.mdc`](../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) Rule 1 — People owns design-pattern-shaped doctrines that other areas inherit.

### D-IH-82-F — Doctrine final filename (closes candidate C-82-1)

*(Note: ID renamed from D-IH-82-NAME to conform to `DECISION_REGISTER.csv` regex `^D-IH-\d{1,3}-[A-Z]{1,2}$`. Letters C/D/E reserved for deferred decisions per candidate stub; F is the next available letter.)*

**Question:** `HOLISTIKA_CAPABILITY_DOCTRINE.md` vs `HOLISTIKA_ELOQUENCE_DOCTRINE.md` vs other?

**Verdict:** **`HOLISTIKA_CAPABILITY_DOCTRINE.md`** — most descriptive of the four-facet capability framing. "ELOQUENCE_DOCTRINE.md" captures only the translation facet (1 of 4); "CONCEPT_TO_USE_CASE_DOCTRINE.md" captures the cycle motto but is awkward as a filename. The 4 facets all serve the **capability** surfacing event; "capability" is the load-bearing noun.

**Marketing/Brand co-sign:** Brand & Narrative Manager may revise the public-facing rendering (banner copy, deck mention) but the canonical filename stays `HOLISTIKA_CAPABILITY_DOCTRINE.md` for FK stability with `PEOPLE_DESIGN_PATTERN_REGISTRY.csv` cross-references.

### D-IH-82-G — AI Archivist / KiRBe ingestor home (closes candidate C-82-3)

*(Note: ID renamed from D-IH-82-ARCHIVIST to conform to validator regex.)*

**Question:** Does the AI Archivist / KiRBe ingestor system land in I82 internal OR forward-charter to I83?

**Verdict:** **I83 forward-charter.** Per operator Round 9 framing: *"It's also good for other things we may build atop our system, like our AI Archivist and all-in-one ingestor (sort of like Composio, but with a wider scope), KiRBe."* The Archivist is a Tech-area-led **product**-shaped initiative — it surfaces I82's use-case archive (P4) data layer through a query interface. The clean split: I82 owns the **data layer** (`USE_CASE_ARCHIVE.csv` + seed POCs); I83 owns the **surfacing system** (ingestor + query + AI agent surfacing).

This keeps I82 People-area-led (doctrine + governance + Talent activation) and I83 Tech-area-led (engineering + AI architecture + observability).

### D-IH-82-H — Phase-sequencing posture (closes candidate C-82-4)

*(Note: ID renamed from D-IH-82-SEQUENCE to conform to validator regex.)*

**Question:** What sequence relative to I81 (vault integrity)? Hard gate, soft gate, or parallel?

**Options surveyed:**

- A: **Doctrine P0 ratified → Talent CSV P1 queued → Capability registry P2 awaits I81 integrity OR waiver.** Default.
- B: Hard gate — I82 fully blocks until I81 P1 closed.
- C: Parallel — I82 P2 mints CAPABILITY_REGISTRY on un-audited `process_list.csv` paths; rely on later sweep to fix.

**Verdict:** **A — staged with waiver escape hatch.** Doctrine (P0) is independent prose work; can land immediately. Talent activation (P1) is a canonical-CSV gate independent of vault integrity. CAPABILITY_REGISTRY (P2) genuinely needs integrity-matrix evidence to avoid minting on orphaned paths — but operator may waive via `D-IH-82-PREREQ` when timing forces it (e.g., live customer call coming up and rough-cut registry better than no registry).

**Risk accepted:** B blocks too aggressively; C creates downstream cleanup work. A is the operator-friendly middle.

## Deferred decisions (close at later phases)

| ID | Question | Owner | Close-out phase |
|:---|:---|:---|:---|
| **D-IH-82-PREREQ** | Prerequisite waiver bridging I81 integrity ↔ I82 Capability registry — when is it acceptable to mint CAPABILITY_REGISTRY without I81 P1 evidence? | Founder + PMO | **P2** entrance (per-mint OR explicit waiver narrative) |
| **D-IH-82-C** | Confidence rating naming policy — SCP-cameo (Keter/Euclid/Safe) vs numbers (0.3/0.7/0.95) vs plain-language as PRIMARY | Founder + Brand Manager | **P3** |
| **D-IH-82-D** | Capability inventory PK + FK posture — `SKILL_REGISTRY` linkage cardinality + `process_list` anchoring policy | People Operations Manager | **P2** |
| **D-IH-82-E** | Use case archive redaction policy — paraphrase default; case-by-case anonymise; explicit `redaction_class` enum | Compliance Officer | **P4** |
