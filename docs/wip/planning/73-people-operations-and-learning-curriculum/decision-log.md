---
initiative_id: INIT-OPENCLAW_AKOS-73
title: I73 decision log
status: active
authored: 2026-05-15
last_review: 2026-05-15
role_owner: PMO
language: en
---

# I73 decision log

> Per-decision register companion to the canonical [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv). This file holds full rationale + alternatives considered + close-out tracking per decision; the canonical CSV holds the queryable row.

## D-IH-73-A — Mega vs split scope ratification

- **Question.** Does I73 cover all 8 strands (Learning + Ethics+Learning + People Ops engagement-lifecycle + Compliance/Ethics boundary + Engagement Model Registry + Historical pattern codification + KB human-readability + Methodology IP minting) as a single mega-initiative, or split into siblings (I73a / I73b / I73c)?
- **Options considered.**
  - **A. Mega-i73** (recommended) — single initiative; one master-roadmap; one decision-log; one risk-register. Pros: coherent narrative; cross-strand integration verification at P10; single closure UAT. Cons: pause-fatigue risk; longer time-to-close (~6-8 weeks).
  - **B. Split into 3 siblings** (I73a People Ops + I73b Engagement Models + I73c IP minting) — three smaller initiatives. Pros: smaller blast radius per initiative; faster closure per. Cons: cross-strand integration becomes ad-hoc; three separate master-roadmaps to keep in sync; engagement-as-unit reframe drifts if not coherent.
  - **C. Hybrid** (I73 People Ops + Engagement Models; spin off I73-IP as candidate for later) — middle ground. Pros: faster People Ops closure. Cons: methodology IP minting cadence depends on engagement-lifecycle SOPs anyway.
- **Decision.** **Option A — Mega-i73.** Operator picked explicitly via Gate 1 AskQuestion 2026-05-15 ("mega-i73").
- **Rationale.** Cross-strand coherence wins. The engagement-as-unit reframe IS the strand-crossing structural insight; splitting forces it to be re-explained in three places. Pause-fatigue mitigation lives in `akos-agent-checkpoint-discipline.mdc` cadence heuristic (front-load substantive review at P0+P1; soft-pause for P4+ if validators clean).
- **Decision source.** `operator_inline_explicit_via_askquestion` (Gate 1 AskQuestion 2026-05-15).
- **Status.** active.
- **Reversibility.** low (mega scope is the narrative; reversing would require splitting the entire workspace folder + master-roadmap).
- **Close-out.** P0 (this commit).

## D-IH-73-B — Hold-gate reframing (charter-satisfies-gate)

- **Question.** The I73 candidate hold-gates ("first Holistik Researcher hired or hiring window committed" + "founder approval to formally onboard People Operations Lead") assumed traditional hires. Bootstrapping reality (operator + Madeira AI O5-1 + ad-hoc collaborators; founder's own paid employment funds Holistika's bootstrap per [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §2) doesn't match. Does the initiative wait for real hires, reframe the gate as charter-satisfies-gate, or use a hybrid?
- **Options considered.**
  - **A. Charter-satisfies-gate** (recommended) — the missing artefact is the engagement-class taxonomy itself, not the hire. Designing the engagement models IS the unblock. Once registry + SOPs exist, future hires/engagements flow through them.
  - **B. Await-real-hire** — hold I73 until first Holistik Researcher hire commits. Pros: closer to candidate-scaffold posture. Cons: blocks the operator's own engagement codification (operator_self class, RCD Legal arrangement) which is already happening.
  - **C. Hybrid** — charter-satisfies-gate for P0..P8; await-real-hire only for P9 first-engagement UAT. Pros: middle ground. Cons: P9 is already operator-driven option (a) — operator-self ratification — so the hybrid collapses to A in practice.
- **Decision.** **Option A — Charter-satisfies-gate.** Recommended default accepted via operator skip (Gate 1 AskQuestion 2026-05-15).
- **Rationale.** The seven engagement classes are today's reality (operator_self funding bootstrap; ad-hoc collaborators; RCD Legal full-time arrangement; Madeira AI O5-1). The taxonomy needs to exist to make the ad-hoc reality governable; waiting for a traditional hire to ratify the taxonomy inverts the dependency.
- **Decision source.** `operator_inline_default_accepted_via_skip` (Gate 1 AskQuestion 2026-05-15; recommended default captured per `akos-inline-ratification.mdc` §6.5 auto-decision fallback).
- **Status.** active.
- **Reversibility.** medium (charter prose can be rewritten; CSV rows are permanent until closure).
- **Close-out.** P0.

## D-IH-73-C — ENGAGEMENT_MODEL_REGISTRY home

- **Question.** Where does the new `ENGAGEMENT_MODEL_REGISTRY.csv` live in the canonical filesystem — People area sibling dimension, cross-area canonical (e.g. `compliance/dimensions/`), or absorbed into Operations/RevOps?
- **Options considered.**
  - **A. People Operations sibling dimension** (recommended) — at `docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv`. Owned by People Operations Lead per DAMA Data Owner pattern. Sibling to `ENGAGEMENT_REGISTRY.csv` at `People/Compliance/canonicals/dimensions/`.
  - **B. Cross-area canonical** at `compliance/dimensions/` (the umbrella dimension folder). Pros: visible to all areas. Cons: ownership becomes ambiguous.
  - **C. Operations/RevOps absorption** — under `Operations/RevOps/canonicals/dimensions/` per I72 Round 7 path migration. Pros: revenue-bearing engagement classes (percentage_collaborator, investor_advisor) align with RevOps value-mapping function. Cons: HR-side classes (apprentice_learner, hourly_consultant) don't fit RevOps.
- **Decision.** **Option A — People Operations sibling dimension.** Recommended default accepted via operator skip explicit at Gate 1.
- **Rationale.** People Operations Lead is the natural Data Owner; the registry feeds 4 People Ops SOPs in P3 (hiring/onboarding/payroll/offboarding); RevOps cross-references via the percentage_collaborator + investor_advisor classes (no FK; cross-link per `akos-holistika-operations.mdc` no-duplication rule).
- **Decision source.** `operator_inline_explicit_via_askquestion` (Gate 1 AskQuestion 2026-05-15).
- **Status.** active.
- **Reversibility.** low (mirror table path encoded in `validate_compliance_schema_drift.py` registry + Supabase migration + Pydantic SSOT — moving costs 4 file edits + 1 migration).
- **Close-out.** P1 (CSV path locked at P1 commit).

## D-IH-73-D — 7-class engagement taxonomy

- **Question.** What are the engagement-model classes for the registry? Operator brief 2026-05-15 named 7 classes; should the registry hold 7 or a different cut?
- **Options considered.**
  - **A. 7 classes** (recommended) — `hourly_consultant` / `milestone_consultant` / `percentage_collaborator` / `apprentice_learner` / `investor_advisor` / `outsourced_helper` / `operator_self`. Each maps to a documented historical pattern.
  - **B. Broader (~10 classes)** — split percentage_collaborator into percentage-of-revenue vs percentage-of-equity; split outsourced_helper into portal-mediated (Fiverr) vs direct-engagement; split apprentice_learner into cohort vs 1:1. Pros: finer-grained. Cons: most splits have N=1 today; over-engineered.
  - **C. Narrower (~5 classes)** — collapse hourly + milestone into "consultant"; collapse investor + percentage into "equity collaborator". Pros: simpler. Cons: hourly vs milestone retribution structures differ materially; investor (cap-table presence) vs percentage (revenue-share without cap-table) are different governance instruments.
- **Decision.** **Option A — 7 classes.** Operator picked explicitly via Gate 1 AskQuestion 2026-05-15.
- **Rationale.** Each class maps to a real historical pattern documented in [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §2: Mark-II = apprentice_learner; Bâtard 2020 = investor_advisor + percentage_collaborator hybrid; Fiverr/Cameroon = outsourced_helper (€400/mo cap); RCD Legal = hourly_consultant + percentage hybrid; current L'Oréal Europe = operator_self carrier. Splitting further has no evidence today; collapsing loses retribution-structure distinctions.
- **Decision source.** `operator_inline_explicit_via_askquestion` (Gate 1 AskQuestion 2026-05-15).
- **Status.** active.
- **Reversibility.** low (per-class enum rows mint in P1; downstream P3 SOPs parameterize by `engagement_model_id`; changing taxonomy mid-execution forces SOP rewrites).
- **Close-out.** P1 (per-class enum rows mint with rationale + retribution_kind + soc_posture + default_access_level).

## D-IH-73-E — Outsourced helper SOC posture

- **Question.** Is `outsourced_helper` a separate engagement class with extra access-control SOC, or a sub-class of `hourly_consultant` with extra clauses?
- **Options considered.**
  - **A. Separate engagement class with extra SOC** (recommended) — lower trust + scoped access + redacted KB view + work-product-only handoff (no methodology exposure). Default `access_level = 1` or `2` per [`access_levels.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/access_levels.md). Maps to Fiverr/Cameroon class (~€400/mo cap).
  - **B. Sub-class of hourly with clauses** — same enum row as `hourly_consultant`; extra contract clauses for low-trust scope. Pros: fewer enum rows. Cons: P7 KB-view routing can't filter by class; SOC posture becomes a clause-readability problem instead of a query-able row.
- **Decision.** **Option A — Separate engagement class.** Recommended default accepted via operator skip.
- **Rationale.** SOC posture must be queryable from `ENGAGEMENT_MODEL_REGISTRY` for P7 KB-view filtering. Putting low-trust posture in contract clauses (Option B) makes the KB-view route policy a free-text grep, which fails the canonical-CSV gate discipline. The €400/mo cap class is structurally different in retribution + SOC + KB access from cleared collaborators.
- **Decision source.** `operator_inline_default_accepted_via_skip` (Gate 1 AskQuestion 2026-05-15).
- **Status.** active.
- **Reversibility.** medium (one enum row collapse; P7 KB-view route needs rewrite if collapsed).
- **Close-out.** P1 (codified in `ENGAGEMENT_MODEL_REGISTRY` row) + P7 (codified in KB-view low-trust route).

## D-IH-73-F — Methodology IP brand-vs-name decision

- **Question.** When the Tech Lab pipeline (P8) mints a new methodology asset, does it ship under the Holistika brand, the operator's personal name, or via a decision-deferred-with-criteria-matrix (per-asset filing decision at filing time)?
- **Options considered.**
  - **A. Decision-deferred-with-criteria-matrix** (recommended) — P8 codifies criteria; per-asset filing decision deferred. Criteria axes: is-this-business-IP vs is-this-personal-method-lineage; commercial-leverage vs intellectual-attribution; trademarkability scope; jurisdiction priority. Aligns with [`LOGIC_CHANGE_LOG.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/LOGIC_CHANGE_LOG.md) BT-01 brand-as-shield framing (versioning founder's own understanding under brand umbrella precedes solid proof).
  - **B. Holistika brand by default** — every methodology asset ships under Holistika trademark. Pros: brand consolidation. Cons: forecloses personal-name option for methods with strong personal lineage (e.g. method-anchor #2 multinational-governance from BICG 2015-2016 + Volvo 2018-2020 traces personally).
  - **C. Operator personal name by default** — every methodology asset ships under founder's name; Holistika is the commercial vehicle. Pros: clear authorship. Cons: dilutes brand IP; future Holistika collaborators can't carry method-anchors.
- **Decision.** **Option A — decision-deferred-with-criteria-matrix.** Recommended default accepted via operator skip.
- **Rationale.** The brand-vs-name decision is not symmetrical across methodology assets. Some methods (e.g. the engagement-as-unit reframe codified by I73 itself) are commercial IP belonging to Holistika; others (e.g. personal-anchor methods traceable to specific employers per [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §4) are personal-lineage with attribution rights. P8 criteria matrix captures the decision logic; per-asset filing decision happens at filing time.
- **Decision source.** `operator_inline_default_accepted_via_skip` (Gate 1 AskQuestion 2026-05-15).
- **Status.** active (deferred to per-asset filing time).
- **Reversibility.** medium (criteria matrix can be rewritten; filed assets cannot be un-filed without IP litigation).
- **Close-out.** P8 (criteria matrix codified) → per-asset filing decisions thereafter.

## D-IH-73-G — KB human-readability personas

- **Question.** How many personas drive the P7 KB human-readability charter, and how are they cut?
- **Options considered.**
  - **A. 4 personas mapped 1:1 to engagement classes** (recommended) — operator-managed / cleared-collaborator / low-trust-outsourced / apprentice. Maps to engagement classes from P1: operator_self → operator-managed; hourly/milestone/percentage/investor → cleared-collaborator; outsourced_helper → low-trust-outsourced; apprentice_learner → apprentice. Implementation via hlk-erp panel filter routes per `akos-mirror-template.mdc`.
  - **B. 7 personas mapped 1:1 to all 7 classes** — finer-grained. Pros: per-class KB view. Cons: most classes overlap in KB access posture (cleared-collaborator covers hourly + milestone + percentage + investor naturally).
  - **C. 3 personas (cleared / scoped / restricted)** — collapsed. Pros: simplest. Cons: collapses operator-managed and apprentice into "cleared", losing the apprentice's learning-curriculum overlay.
- **Decision.** **Option A — 4 personas mapped 1:1 to engagement-class buckets.** Recommended default accepted via operator skip.
- **Rationale.** 4 personas match the operator + cleared + low-trust + apprentice cut that the operator brief 2026-05-15 implicitly named. Operator-managed gets full access; cleared-collaborator gets all-but-strategic; low-trust gets work-product-only; apprentice gets learning-overlay + access-level-gated views. Maps cleanly to hlk-erp panel filter routes.
- **Decision source.** `operator_inline_default_accepted_via_skip` (Gate 1 AskQuestion 2026-05-15).
- **Status.** active.
- **Reversibility.** medium (4 hlk-erp routes can be merged or split; KB charter prose can be rewritten).
- **Close-out.** P7.

## Forward-charter decisions

The following decisions are pre-allocated to per-phase inline-ratify gates:

- **D-IH-73-H..M** — per-class enum ratifications (one per engagement model class; P1).
- **D-IH-73-N** — `ENGAGEMENT_REGISTRY.csv` 17-col extension ratification (P1).
- **D-IH-73-CLOSURE** — initiative closure (P11).

Additional D-IH-73-* rows will be minted as conundrums C-73-1..C-73-8 are ratified at their per-phase inline-ratify gates.

## Cross-references

- Canonical decision register: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv).
- Authoritative Cursor plan: [`~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md`](file:///~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md).
- P0 charter report: [`reports/p0-charter-report.md`](reports/p0-charter-report.md).
- Risk register: [`risk-register.md`](risk-register.md).
- Inline-ratification rule: [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc).
