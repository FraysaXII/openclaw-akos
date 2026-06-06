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

- **Question.** The I73 candidate hold-gates ("first Holistik Researcher hired or hiring window committed" + "founder approval to formally onboard People Operations Manager") assumed traditional hires. Bootstrapping reality (operator + Madeira AI O5-1 + ad-hoc collaborators; founder's own paid employment funds Holistika's bootstrap per [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §2) doesn't match. Does the initiative wait for real hires, reframe the gate as charter-satisfies-gate, or use a hybrid?
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
  - **A. People Operations sibling dimension** (recommended) — at `docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv`. Owned by People Operations Manager per DAMA Data Owner pattern. Sibling to `ENGAGEMENT_REGISTRY.csv` at `People/Compliance/canonicals/dimensions/`.
  - **B. Cross-area canonical** at `compliance/dimensions/` (the umbrella dimension folder). Pros: visible to all areas. Cons: ownership becomes ambiguous.
  - **C. Operations/RevOps absorption** — under `Operations/RevOps/canonicals/dimensions/` per I72 Round 7 path migration. Pros: revenue-bearing engagement classes (percentage_collaborator, investor_advisor) align with RevOps value-mapping function. Cons: HR-side classes (apprentice_learner, hourly_consultant) don't fit RevOps.
- **Decision.** **Option A — People Operations sibling dimension.** Recommended default accepted via operator skip explicit at Gate 1.
- **Rationale.** People Operations Manager is the natural Data Owner; the registry feeds 4 People Ops SOPs in P3 (hiring/onboarding/payroll/offboarding); RevOps cross-references via the percentage_collaborator + investor_advisor classes (no FK; cross-link per `akos-holistika-operations.mdc` no-duplication rule).
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

## D-IH-73-H — Per-class enum ratification — eng_model_hourly_consultant

- **Question.** What are the canonical enum values for the `eng_model_hourly_consultant` row (retribution_pattern / soc_posture / access_level_default / ip_clause_class / knowledge_access_level / payment_cadence)?
- **Decision.** `retribution_pattern=hourly` / `soc_posture=cleared` / `access_level_default=4` (Confidential per [`access_levels.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/access_levels.md)) / `ip_clause_class=standard_consultant` / `knowledge_access_level=full_by_engagement` / `payment_cadence=per_hour`. Onboarding pattern `nda_then_sow_kickoff`; offboarding `final_invoice_then_access_revoke`. Default legal template: NDA + SoW (hourly).
- **Rationale.** Direct-engagement freelancer (Advisers-template shape per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §16). Cleared collaborator SOC with full access bounded by engagement scope. Maps to pre-bootstrapping consultant pattern. Standard work-for-hire IP clause.
- **Decision source.** `operator_inline_default_accepted_via_skip` (Gate B 2026-05-15; recommended defaults from operator brief).
- **Status.** active. **Reversibility.** low. **Close-out.** P1 (this commit).
- **Supersedes**: D-IH-73-D (parent taxonomy decision).

## D-IH-73-I — Per-class enum ratification — eng_model_milestone_consultant

- **Question.** Same as D-IH-73-H but for `eng_model_milestone_consultant`.
- **Decision.** `retribution_pattern=milestone` / `soc_posture=cleared` / `access_level_default=4` / `ip_clause_class=milestone_handoff` / `knowledge_access_level=partial_by_engagement` / `payment_cadence=per_milestone`. Onboarding `nda_then_milestone_kickoff`; offboarding `handoff_review_then_archive`. Default legal template: NDA + SoW + milestone schedule.
- **Rationale.** Milestone-deliverable retribution (Bâtard pattern of bundled deliverable handoff). Partial-by-engagement access scope (only context relevant to the milestone is exposed). Historical: RCD Legal landing as customer.
- **Decision source.** `operator_inline_default_accepted_via_skip` (Gate B 2026-05-15).
- **Status.** active. **Reversibility.** low. **Close-out.** P1.
- **Supersedes**: D-IH-73-D.

## D-IH-73-J — Per-class enum ratification — eng_model_percentage_collaborator

- **Question.** Same as D-IH-73-H but for `eng_model_percentage_collaborator`.
- **Decision.** `retribution_pattern=percentage` / `soc_posture=cleared` / `access_level_default=4` / `ip_clause_class=collaborator_share` / `knowledge_access_level=full_by_engagement` / `payment_cadence=per_deal_outcome`. Onboarding `nda_collaborator_share_agreement`; offboarding `final_payout_reconciliation_then_archive`. Default legal template: NDA + collaborator-share agreement.
- **Rationale.** Revenue-share retribution without cap-table presence (Bâtard 2020 percentage-collaborator pattern). Reconciliation cadence at deal outcome; cross-link to [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv) for payout tracking per [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) no-duplication rule.
- **Decision source.** `operator_inline_default_accepted_via_skip` (Gate B 2026-05-15).
- **Status.** active. **Reversibility.** low. **Close-out.** P1.
- **Supersedes**: D-IH-73-D.

## D-IH-73-K — Per-class enum ratification — eng_model_apprentice_learner

- **Question.** Same as D-IH-73-H but for `eng_model_apprentice_learner`.
- **Decision.** `retribution_pattern=barter_for_training` / `soc_posture=training_only` / `access_level_default=3` (Internal per access_levels.md) / `ip_clause_class=training_recipient` / `knowledge_access_level=training_curriculum_only` / `payment_cadence=barter_continuous`. Onboarding `nda_training_agreement_curriculum_assignment`; offboarding `graduation_review_then_optional_promotion`. Default legal template: NDA + training agreement (no money flow).
- **Rationale.** Work-for-training arrangement (Mark-II + Alias V archetype per `FOUNDER_TRAJECTORY_INTERNAL.md` §2). Training-only SOC posture (under-training cleared but bounded to curriculum). Apprentice ↔ curriculum binding executed at P2 (Learning charter + Holistik Researcher curriculum). No money flow; retribution is the curriculum itself.
- **Decision source.** `operator_inline_default_accepted_via_skip` (Gate B 2026-05-15).
- **Status.** active. **Reversibility.** low. **Close-out.** P1 + P2 (curriculum binding).
- **Supersedes**: D-IH-73-D.

## D-IH-73-L — Per-class enum ratification — eng_model_investor_advisor

- **Question.** Same as D-IH-73-H but for `eng_model_investor_advisor`.
- **Decision.** `retribution_pattern=equity_advisor` / `soc_posture=cleared` / `access_level_default=5` (Highly Confidential per access_levels.md) / `ip_clause_class=advisor_nda` / `knowledge_access_level=full_by_engagement` / `payment_cadence=per_round`. Onboarding `advisor_nda_safe_or_convertible`; offboarding `round_exit_review_then_archive`. Default legal template: advisor NDA + SAFE/convertible.
- **Rationale.** Equity / advisor-grant retribution; cap-table presence or formal advisor grant (Bâtard 2020 investor pattern). Cleared SOC at access_level=5 because cap-table participants see C-level / strategic governance content. Round-lifecycle cadence.
- **Decision source.** `operator_inline_default_accepted_via_skip` (Gate B 2026-05-15).
- **Status.** active. **Reversibility.** low. **Close-out.** P1.
- **Supersedes**: D-IH-73-D.

## D-IH-73-M — Per-class enum ratification — eng_model_outsourced_helper

- **Question.** Same as D-IH-73-H but for `eng_model_outsourced_helper` (cross-link to D-IH-73-E parent SOC posture decision).
- **Decision.** `retribution_pattern=hourly_low_trust` / `soc_posture=low_trust` / `access_level_default=1` (Community per access_levels.md) / `ip_clause_class=outsourced_workproduct_only` / `knowledge_access_level=work_product_scope_only` / `payment_cadence=per_hour_capped`. Onboarding `minimal_nda_workproduct_scope_brief`; offboarding `workproduct_handoff_then_access_revoke`. Default legal template: minimal NDA + work-product-only handoff (€400/mo cap default).
- **Rationale.** Portal-mediated freelancer (Fiverr/Cameroon helper pattern; €400/mo cap class). Low-trust SOC posture per D-IH-73-E (separate engagement class with extra access-control SOC, not sub-class of hourly). Access_level=1 — scoped + redacted KB view; no methodology exposure. Queryable canonical row (vs free-text contract-clause grep) is the load-bearing P7 KB-view low-trust route policy hook per [`akos-mirror-template.mdc`](../../../../.cursor/rules/akos-mirror-template.mdc).
- **Decision source.** `operator_inline_default_accepted_via_skip` (Gate B 2026-05-15).
- **Status.** active. **Reversibility.** low. **Close-out.** P1 (registry row) + P7 (KB-view enforcement).
- **Supersedes**: D-IH-73-E (parent SOC posture decision).

## D-IH-73-N — ENGAGEMENT_REGISTRY.csv 17-col extension

- **Question.** Add `engagement_model_id` FK column to existing 16-col `ENGAGEMENT_REGISTRY.csv` at P1, or defer to a separate maintenance commit?
- **Options considered.**
  - **A. Add column at P1** (recommended) — atomic landing with the sibling-dimension registry. Existing 6 rows backfill to empty; FK constraint NOT VALID until P9 UAT backfill. ENGAGEMENT_REGISTRY.md §2 updated to reflect 17-col schema. Companion `supabase/migrations/20260515180001_i73_engagement_registry_add_engagement_model_id.sql` migration.
  - **B. Defer column to separate commit** — keeps ENGAGEMENT_REGISTRY.csv frozen at 16-col for this commit; column-add lands in P9 UAT or in a P2/P3 backfill commit. Pros: smaller P1 diff. Cons: forces P3 SOPs to parameterize without a real FK column to dereference; orphans the registry from existing engagement instances.
- **Decision.** **Option A — add column at P1.** Recommended default accepted via Gate B (P1 inline-ratify) + Gate C (PAUSE POINT canonical CSV preview).
- **Rationale.** P3 engagement-lifecycle SOPs reference `engagement_model_id` for parameterization (C-73-4 default). Adding the column at P1 means P3 SOP commits can reference a real FK column from day 1 without retrofit. NULL-tolerant constraint preserves backwards-compat for existing rows; backfill happens at P9 first-engagement-onboarded UAT.
- **Decision source.** `operator_inline_default_accepted_via_skip` (Gate B + Gate C 2026-05-15).
- **Status.** active.
- **Reversibility.** medium (column can be dropped, but downstream SOPs and KB-view routes would need rewrite).
- **Close-out.** P1.

## C-73-1 — Default apprentice cohort size (P2 inline-ratify)

- **Question.** Default cohort size for Holistik Researcher onboarding backlog tracking (`LEARNING_OPS_BACKLOG.csv`) until hiring velocity materially exceeds solo-operator pacing?
- **Options.** **A.** Fixed cohort size 1 by default (append backlog rows one apprentice at a time). **B.** Variable cohort size with quarterly sizing ritual (extra CSV discipline).
- **Decision.** **Option A — default cohort size 1.** Accepted via operator skip / silent continuation during P2 execution (inline-ratify per [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc)); **no** companion `DECISION_REGISTER.csv` row minted (operator-discipline ratification recorded here only).
- **Close-out.** P2.

## C-73-2 — Curriculum methodology versioning anchor (P2 inline-ratify)

- **Question.** Anchor `methodology_version_at_onboarding` in `LEARNING_OPS_BACKLOG.csv` to I71 review-stamp posture (`methodology-anchor` / methodology lane) vs inventing a Learning-only cadence slug?
- **Options.** **A.** Default `methodology-anchor` for curriculum-bound rows (reuse I71 P4 column semantics). **B.** Separate Learning-only version token (extra taxonomy work).
- **Decision.** **Option A — default `methodology-anchor`.** Accepted via operator skip during P2 execution; **no** companion `DECISION_REGISTER.csv` row minted.
- **Close-out.** P2.

## C-73-3 — Quarterly Ethics + Learning review facilitator (P5 inline-ratify)

- **Question.** Who facilitates the quarterly co-review mandated by [`ETHICAL_AUTOMATION_POSTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md) §5 (*Ethics + Learning inseparability contract*)?
- **Options.** **A.** Ethics Advisor leads with Learning Curator as mandatory co-reviewer. **B.** Learning Curator leads; Ethics audits after-the-fact.
- **Decision.** **Option A — Ethics-led with mandatory Learning co-review.** Accepted via operator skip during P5 execution; ratification captured here only (**no** companion `DECISION_REGISTER.csv` row minted).
- **Close-out.** P5 (`SOP-ETHICS_LEARNING_REVIEW_001.md` + `hol_peopl_dtp_316`).

## Operator ratification — recruiter onboarding closure + methodology IP note (AskQuestion 2026-05-15)

- **Recruiter onboarding.** Closed `TODO[I73-SOP-RECRUITER_ONBOARDING_001]` / `TODO[I73-runbook-recruiter-onboarding]` placeholders on [`INTELLIGENCEOPS_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv) row **`IO-REC-PLACEHOLDER-001`** by wiring **`linked_sop_path`** → [`SOP-RECRUITER_ONBOARDING_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/People%20Operations/canonicals/SOP-RECRUITER_ONBOARDING_001.md) and **`linked_runbook_path`** → [`scripts/peopl_recruiter_onboarding_checklist_stub.py`](../../../../scripts/peopl_recruiter_onboarding_checklist_stub.py). Minted **`process_list.csv`** row **`tbi_peopl_dtp_recruiter_onboarding_001`** (`cadence_type=event_triggered`, `role_owner=People Operations Manager`, paired SOP/runbook cells). **`DECISION_REGISTER.csv`** rows **not** minted for this closure wave per operator scope (`validate_decision_register.py` FK hygiene unchanged).
- **`TODO[OPERATOR-goi-recruiter-001]`** — **Document-only / operator-supplied ID**: agents do **not** mint `goi_*` locally; clearing stub lives at [`reports/pending-goi-recruiter-001.md`](reports/pending-goi-recruiter-001.md) until the operator replaces the placeholder `target_id` on **`IO-REC-PLACEHOLDER-001`** with a governed GOI row.
- **methodology_IP_default (P8 seed).** Operator verbatim intent captured for Strand H: **Holistika** by default; founder sole investor; anchors — **process engineering** / **business engineering** / **foresight**.

## C-73-5 — Compliance vs Ethics boundary defaults (P6 inline-ratify)

- **Question.** When a People-area process sits ambiguously between Compliance methodology ownership and Ethics doctrine ownership (legacy Talent monolith residue), what default splits apply for GDPR vs AI-overreach vs AI customer disclosure?
- **Options.** **A.** Compliance owns regulatory/data-protection; Ethics owns AI-overreach posture; AI-assisted customer disclosure is joint (Compliance + Ethics RACI). **B.** Collapse everything under Compliance. **C.** Collapse everything under Ethics.
- **Decision.** **Option A.** Accepted via `operator_inline_default_accepted_via_skip` for P6 subagent execution (no AskQuestion in chat) after mechanical evidence landed in [`PEOPLE_COMPLIANCE_VS_ETHICS_BOUNDARY.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PEOPLE_COMPLIANCE_VS_ETHICS_BOUNDARY.md); **no** companion `DECISION_REGISTER.csv` row minted (ratification recorded here only).
- **Mechanical follow-through.** `process_list.csv` rows `hol_peopl_dtp_139` → `Ethics Advisor`; `hol_peopl_dtp_286` → `Learning Curator`; `OPS-73-6` closed.
- **Close-out.** P6.

## C-73-7 — Persona KB view implementation shape (P7 inline-ratify)

- **Question.** Separate static KB surfaces vs one role-tagged surface vs **HLK-ERP panel filter routes** per persona (**D-IH-73-G**)?
- **Options.** Per authoritative Cursor plan P7 todo: ERP panel filter routes (recommended default) vs alternatives.
- **Decision.** **HLK-ERP panel filter routes** — four presets under `/operator/people/kb-views/` (see **[`reports/kb-human-readability-erp-route-spec.md`](reports/kb-human-readability-erp-route-spec.md)**); AKOS carries charter + sibling PR spec only (`hlk-erp` absent from this repo). Ratified consistent with **`D-IH-73-G`** in [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv); **no** new `DECISION_REGISTER.csv` row minted for C-73-7.
- **Close-out.** P7 ([`KB_HUMAN_READABILITY_CHARTER.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md)).

## C-73-6 — Methodology IP licensing model (P8 inline-ratify)

- **Question.** Proprietary vs CC-BY-NC vs CC-BY-SA vs hybrid for methodology corpus outputs?
- **Options.** Per **D-IH-73-F**: **decision-deferred-with-criteria-matrix** at filing/editorial freeze vs forcing a single repo-wide license in P8.
- **Decision.** **Asset-deferred** — record per deliverable in Legal handoff + counsel memo; [`METHODOLOGY_IP_MINTING_PATH.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/METHODOLOGY_IP_MINTING_PATH.md) §"Licensing posture" encodes the hold. **No** new `DECISION_REGISTER.csv` row minted ( **`D-IH-73-F`** remains the governing decision row).
- **Close-out.** P8.

## Release gate Part C — deterministic FAIL backlog vs environmental FAIL backlog (2026-05-15)

- **Scope.** Sync deck pillar counts + dossier persona fixture + engagement estimation baseline-role parity + regenerated operator inbox; **`release-gate.py` verdict remains FAIL** until browser-smoke listener + strict BRAND voice register + Vale sibling rows green on operator host (recorded in [`reports/release-gate-triage-2026-05-15.md`](reports/release-gate-triage-2026-05-15.md)).

## Forward-charter decisions

Minted **`D-IH-73-CLOSURE`** (2026-05-15) — see [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) + P11 closure commit notes in [`master-roadmap.md`](master-roadmap.md).

Historical: conundrums **C-73-1..C-73-8** were ratified across P2–P8 (see sections above); **`D-IH-73-CLOSURE`** closes the initiative umbrella only — follow-on legal filings + `hlk-erp` implementation remain **out of I73 closure scope**.

## Cross-references

- Canonical decision register: [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv).
- Authoritative Cursor plan: [`~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md`](file:///~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md).
- P0 charter report: [`reports/p0-charter-report.md`](reports/p0-charter-report.md).
- Risk register: [`risk-register.md`](risk-register.md).
- Inline-ratification rule: [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc).
