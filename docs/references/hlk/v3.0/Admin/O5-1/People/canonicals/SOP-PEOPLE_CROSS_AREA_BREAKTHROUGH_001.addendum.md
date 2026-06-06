---
title: SOP — People Cross-Area Breakthrough Propagation — Addendum (Tech Lab + Auditor depth)
language: en
intellectual_kind: people-canonical-sop-addendum
sop_id: SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001
access_level: 5
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - System Owner
  - People Operations Manager
last_review: 2026-05-16
last_review_by: People Operations Manager
last_review_decision_id: D-IH-80-D
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-79-A
  - D-IH-79-I
  - D-IH-80-D
status: active
register: internal
parent_sop: SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md
companion_to:
  - SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md
  - SOP-TECH_AGENTIC_INFRA_001.md
  - AGENTIC_FRAMEWORK_LANDSCAPE.md
ssot: true
---

# SOP — People Cross-Area Breakthrough Propagation — Addendum

> Access level 5. This addendum carries the Tech Lab integration-posture detail, KB-infrastructure dimensions, audit trail mechanics, and operator-side framing decisions that the executor (People Operations Manager running the announcement digest) does not need to read but auditors / System Owner / Tech Lab Lead reference when the SOP fires.
>
> Authored at I80 P4 (D-IH-80-D Option B retrofit pilot) as the third instantiation of `pattern_sop_addendum_split` after the stakeholder lenses pair (P2) and the agentic-operations addendum (this phase).

---

## A. Tech Lab pingback — what System Owner specifically assesses

Body §4 names the pingback target ("System Owner reads the People-side change within one week and assesses whether the framework rows, the integration postures, or the knowledge base infrastructure dimensions need to revise to stay coherent"). The deeper detail belongs here:

### A.1 Framework rows — the eight tracked frameworks

Per [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) §1, Tech Lab tracks eight frameworks: LangChain (orchestration), LangGraph (state machines), LlamaIndex (data ingestion), OpenClaw (multi-agent), CrewAI (role-based), Ollama (local inference), VercelAI (frontend integration), Groq (inference acceleration). Each framework row carries: purpose / when-we-use / risk-posture / version-pin / known-incidents.

When `HOLISTIKA_AGENTIC_DOCTRINE.md` revises substantively, System Owner's assessment per framework row asks:

- Does the doctrine revision change *when* we use this framework? (e.g., a doctrine shift that says "no agent-to-agent autonomous handoff without operator-in-the-loop" would change the when-we-use cell for OpenClaw and CrewAI specifically.)
- Does it change the *risk posture*? (e.g., a doctrine shift that hardens red-line escalation cadence would tighten the risk-posture cell for any framework that auto-routes between agents.)
- Does it require a version pin update? (rare; only fires when the doctrine change exposes a known bug class in a tracked version.)

The assessment outcome per framework row is one of: revise (Tech Lab opens an editing PR within one week) / no-action (the framework row stays as-is) / scheduled-revise-at-next-quarterly (defer to the quarterly Tech Lab audit per `SOP-TECH_AGENTIC_INFRA_001.md` §3).

### A.2 Integration postures — three classes

Tech Lab carries three integration-posture classes per framework, each with operator-side semantics:

- **Internal-only** — the framework runs against AKOS-local data; no external API exposure. Doctrine revisions affecting confidentiality (red-line classes 1-3) usually leave this posture unchanged.
- **External-bridged** — the framework calls external APIs (OpenAI, Claude, Mistral) but data flow is one-way out and structured-out. Doctrine revisions affecting external-data-handling (red-line classes 4-5) may tighten this posture (e.g., add PII scrubbing layer).
- **External-embedded** — the framework runs as embedded SDK in external surfaces (Vercel deployments, customer-facing). Most doctrine revisions affect this posture; assess against the customer-facing register.

When the doctrine shift affects an integration-posture class, System Owner pings the affected framework rows AND the relevant SOP at Tech Lab (`SOP-TECH_AGENTIC_INFRA_001.md` §2 framework major-version ratification or §4 KB pipeline maintenance).

### A.3 KB-infrastructure dimensions — five tiers

Tech Lab's knowledge-base infrastructure stratifies into five tiers per [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) §2:

1. **Canonical KB** — the AKOS git repository itself (this file lives here).
2. **Mirrored KB** — Supabase compliance.* mirror tables (auto-synced from canonical CSVs).
3. **Vector KB** — pgvector embeddings of canonical Markdown for RAG retrieval.
4. **Graph KB** — Neo4j projection of the cross-canonical link structure.
5. **External-bridged KB** — vendor systems (Stripe metadata, Vercel deploy IDs) that AKOS reads via FDW.

Doctrine revisions can affect tier propagation:

- Tier 1 → Tier 2: changes to canonical CSVs trigger sync (per `compliance_mirror_emit` profile). System Owner confirms the mirror is current.
- Tier 1 → Tier 3: changes to canonical Markdown trigger embedding recomputation (per Tech Lab quarterly cadence). System Owner confirms the embedding job has run if the doctrine revision is access-level 4 or below (level 5 is excluded from RAG retrieval per `D-IH-79-Z`).
- Tier 1 → Tier 4: changes to cross-canonical link structure (e.g., new `companion_to:` rows from the body/addendum split) trigger Neo4j projection refresh. System Owner confirms via `validate_neo4j_compliance_mirror_drift_probe`.

The pingback-audit step in `SOP-TECH_AGENTIC_INFRA_001.md` §1 (the cross-area pingback step on the Tech Lab side) confirms each tier's sync state aligns with the People-side doctrine revision date.

## B. Substantive-edit boundary — what counts as substantive

Body §1 names the trigger but does not explicitly define "substantive". Auditor-facing precision:

A registry edit is substantive when *any* of these are true:

- A new row is added (always substantive).
- An existing row's `pattern_class` changes (always substantive — class change is a re-classification with downstream consumers).
- An existing row's `consumer_areas` changes (always substantive — adds or removes downstream pingbacks).
- An existing row's `acceptance_criteria_human` or `acceptance_criteria_automation` changes (always substantive — changes the contract).
- An existing row's `status` changes (always substantive — lifecycle move; e.g., `experimental` → `active` or `active` → `deprecated`).
- An existing row's `discipline_origin` changes (always substantive — changes which area the pattern propagated from).

A registry edit is NOT substantive when:

- Typos / formatting fixes / link rewrites.
- `last_review` date update without other field changes.
- Trailing whitespace / encoding normalization.

When the author is unsure, the `--dry-run` flag of the runbook surfaces what the announcement digest would say if the edit were treated as substantive; the operator can review and decide.

The quarterly reconciliation run (body §6) catches missed substantive-vs-non-substantive calls by comparing `last_review` dates across all rows in the registry against the announcement log. Mismatches surface as candidates for late announcement.

## C. Per-area decision audit trail — where decisions land

Body §3 names where decisions go ("each consuming area's decision log") but does not specify the schema. Auditor reference:

Each consuming area maintains a decision log under `docs/wip/planning/<NN-area-initiative>/decision-log.md` or under `docs/references/hlk/v3.0/<area>/<role>/decision-logs/`. When the area receives a breakthrough digest, the role-owner appends a row to the area's log with:

- `decision_id` — area-scoped (e.g., `D-IH-MKT-NN-X` for Marketing-area initiative-NN); cross-references to the AKOS-global `D-IH-NN-X` register only when the decision changes a canonical asset.
- `pattern_id` — the pattern row from the registry.
- `decision_date` — when the area decided.
- `decision_outcome` — one of `adopt_now` / `adopt_later` / `decline`.
- `consuming_process_id` — if `adopt_now`, the `process_list.csv` row that operationalises the adoption.
- `expected_adoption_window` — if `adopt_later`, the calendar quarter the area expects to adopt.
- `decline_reason` — if `decline`, a one-line rationale.

The runbook's `--reconcile` mode (body §6) reads each area's decision log and emits the quarterly summary. Areas that have not authored a decision log row for a digest within four weeks are flagged in the summary as "decision pending — role-owner ping required".

## D. Operator framing decisions encoded in this SOP

**D-IH-79-I (round 4 inline-ratify, 2026-05-15) — cross-area propagation as SOP, not just runbook.** Operator framed the cross-area mechanism as needing both an executable runbook (the announcement digest) AND a human-readable SOP (the contract that names *who* decides + *who* supports + *how* the propagation flows). This addendum lives at the SOP-side; the runbook lives at `scripts/peopl_cross_area_breakthrough_announce.py`. Both surfaces are SSOT for the same process per `akos-executable-process-catalog.mdc` Rule 1.

**D-IH-79-A (round 1 inline-ratify, 2026-05-13) — charter-satisfies-gate.** The cross-area breakthrough SOP was authored under the charter-satisfies-gate posture: I79 charter ratified at round 1; this SOP authored at P4 with no separate plan-vs-execution gate. The audit trail starts at the charter.

**D-IH-79-N (round 5 inline-ratify, 2026-05-15) — anti-jargon drift gate.** The body of this SOP must read in plain language; the cross-area technical depth (framework names + integration postures + KB tiers) lives here in the addendum. This addendum file is exempt from `validate_design_pattern_registry.py --jargon-scan` per `D-IH-80-F` (I80 P1 mint).

These three decisions together explain the SOP's structural shape. The body answers "what do I do when a registry edit lands"; this addendum answers "why is the propagation routed this way and what auditor dimensions ride on top".

## E. Cross-references and provenance

- Body file: [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md).
- Sibling Tech Lab SOP: [`SOP-TECH_AGENTIC_INFRA_001.md`](../../Envoy%20Tech%20Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md) — covers infrastructure operations (framework lifecycle + KB pipeline + MCP postures + Tech Lab pingback acknowledgement).
- Tech Lab landscape: [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) — framework rows + KB infrastructure dimensions + integration postures.
- People doctrine: [`HOLISTIKA_ORGANISING_DOCTRINE.md`](HOLISTIKA_ORGANISING_DOCTRINE.md) — the manifesto framing People-as-discipline-of-disciplines (the why).
- Pattern registry: [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv) — the SSOT the body's announcement digest reads.
- Pattern provenance: [`PEOPLE_DESIGN_PATTERN_LIBRARY.md #pattern-sop-addendum-split`](PEOPLE_DESIGN_PATTERN_LIBRARY.md#pattern-sop-addendum-split) — the pattern this addendum instantiates.
- I80 retrofit charter: [`docs/wip/planning/80-i79-lessons-learned/master-roadmap.md`](../../../../wip/planning/80-i79-lessons-learned/master-roadmap.md) §"P4 — I79 SOP retrofit pilot".
