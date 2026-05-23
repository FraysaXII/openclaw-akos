---
candidate_id: I-NN-CROSS-AREA-OPS-WIRING-REVIEW
title: Cross-area Ops-wiring review discipline — every area's Ops surface gets explicit cross-area wiring at its own hierarchy + ownership level (no small-vs-big prioritization)
status: candidate
authored: 2026-05-22
last_review: 2026-05-23
parent_initiatives: [81]
related_initiatives: [21, 72, 79, 86]
priority: 4
language: en
audience: J-OP;J-AIC
access_level: 5
parent_lane: I81 Wave R lane D T1-gate (FINOPS synthesis ratification) + Wave R Bundle C amendment (operator s4 novel framing)
charter_decisions:
  - D-IH-81-O
  - D-IH-81-P
  - D-IH-81-T
forward_charter_authority: D-IH-81-O (operator novel framing at FINOPS synthesis Decision C gate 2026-05-22 — backbone-class areas need cross-area wiring review); D-IH-81-P (internal-first FINOPS posture amendment 2026-05-23 — A3 gate reframed to remove CFOaaS-default; cross-area sweep inherits agent-recommends-outsource-path failure-mode sanity-check per OPS-81-21); D-IH-81-T (operator s4 second-novel framing at Wave R Bundle C amendment 2026-05-23 — "every area gets cross-area wiring review at its own hierarchy + ownership level; no such thing as small or big, only backfilling data; small or big is just backfilling data; all areas deserve cross-area review with their hierarchy + each thing has its owner; improve integrity where it counts" — supersedes original backbone-only scope; A2 activation gate amended to "exercised on FINOPS + ONE additional area's Ops surface (any area, not restricted to original backbone list)")
linked_canonicals:
  - docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/i81/p2-tranche-t1-finops-synthesis-2026-05-22.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv
  - .cursor/rules/akos-people-discipline-of-disciplines.mdc
  - .cursor/rules/akos-executable-process-catalog.mdc
  - .cursor/rules/akos-quality-fabric.mdc
  - .cursor/rules/akos-applied-research-discipline.mdc
linked_ops_action_ids:
  - OPS-81-2
  - OPS-81-3
  - OPS-81-4
  - OPS-81-5
  - OPS-81-6
  - OPS-81-17
  - OPS-81-18
  - OPS-81-20
  - OPS-81-21
external_research_sources:
  - https://teamtopologies.com/key-concepts
  - https://teamtopologies.com/key-concepts-content/team-interaction-modeling-with-team-topologies
  - https://codelit.io/blog/bounded-context-mapping
  - https://martinfowler.com/bliki/TeamTopologies.html
---

# I-NN-CROSS-AREA-OPS-WIRING-REVIEW — every-area cross-area Ops wiring review discipline

> **Originally spawned by D-IH-81-O** (operator novel framing at the FINOPS end-to-end synthesis ratification gate, 2026-05-22). Operator verbatim: *"add regressions or continuous revisions or enhancements or backfill for all of this. Because FINOPS is a backbone, main representative of finance + legal + PeopleOps + other area's Ops, needs to be wired properly and cleverly to ensure we can grow our all ops as we go. Think you could review each area's OPS to ensure proper wiring maintenance etc. Mint this in the operator scratchbook too to ensure audit trail."*
>
> **Amended 2026-05-23 by D-IH-81-T** (operator s4 second-novel framing at Wave R Bundle C amendment gate). Operator verbatim: *"This comes from every area each must get better at finding those bridges with each area. in that regard there is no such thing as a small area or not. each small or big is just s backfiling data. All area deserve cross with their hierarchy and each thing has their owner. We need to improve integrity and ensure it where it counts."* The s4 framing supersedes the original backbone-only scoping — see §1 + §2 + §3 + §5 below for the full reframing.

## 1. Doctrine in one sentence (amended 2026-05-23 per D-IH-81-T)

**Every area's Ops surface deserves explicit cross-area wiring review at its own hierarchy + ownership level — no small-vs-big prioritization, because small or big is just backfilling data.** Cross-area wiring integrity is checked across all area boundaries the same way Inter-Wave Regression checks cluster-coordinator integrity. FINOPS / PeopleOps / RevOps / LegalOps remain the first-mover surfaces (highest wiring density + the original "backbone" framing per D-IH-81-O), but the discipline applies horizontally across every area registered in `baseline_organisation.csv` — Marketing / Research / Tech Lab / Operations / Compliance / Ethics / Brand / Legal — at the cadence + density that each area's hierarchy + ownership warrants.

The pre-amendment framing carried an implicit "backbone areas are reviewable; non-backbone areas are not" hierarchy. The operator s4 framing rejects that. Every area gets reviewed; the *depth* of review scales with the area's wiring density (FINOPS gets weekly counterparty + engagement-event wiring sweeps; a quieter area like Brand may get a quarterly cross-Brand-to-Marketing wiring check). Density-of-review varies; **scope-of-discipline does not** — every area is in scope.

## 2. Activation gates (amended 2026-05-23 per D-IH-81-T)

- **A1.** Operator sets activation criteria explicitly (this candidate names *that* the discipline should exist; *when* it activates is operator-discretion at next ratify cycle). UNCHANGED.
- **A2 AMENDED.** **Discipline has been exercised end-to-end on at least TWO areas' Ops surfaces** before promotion — one of which SHOULD (but is not required to) be FINOPS given its first-mover status from D-IH-81-O. The second area can be ANY area (not restricted to the original backbone list of PeopleOps / RevOps / LegalOps). Each exercised area must show: counterparty/role/process register populated to at least illustrative threshold + at least one paired SOP+runbook exercised end-to-end + at least one cross-area event-trigger documented (e.g., engagement signed → counterparty registered → Stripe customer linked per SOP-FINOPS_BRIDGE_001 for FINOPS; analogous for other areas at their hierarchy + ownership level). The two-area exercise floor protects against single-area generalisation — a discipline minted from one area's pattern is not yet a discipline.
- **A3.** Area-ownership is explicit per the three-layer ownership posture model (per D-IH-81-P; original A3 framing of "CFOaaS firm contracted OR operator declares interim ownership" was superseded). Concretely per area: (a) Layer A compliance bookkeeping owner is named (AT-Pymes gestoría for FINOPS per D-IH-89-L; analogous per-area gestoría-equivalent for PeopleOps / LegalOps / etc. when those areas mature, OR explicit "internal-first only, no compliance layer needed yet" declaration); (b) Layer B judgment + reporting + policy is named (operator + Madeira internal-first per `akos-applied-research-discipline.mdc` for FINOPS; analogous internal-first owner per area, typically the area's role_owner from `baseline_organisation.csv`); (c) Layer C external recruitment activation triggers are documented per area when applicable (for FINOPS: INVESTMENT MILESTONE / PROJECT COMPLEXITY / OPERATOR-JUDGMENT per D-IH-81-P; analogous per area, OR explicit "no Layer C trigger today" declaration). External recruitment is **not required** for A3 — internal-first ownership with documented activation triggers (or explicit no-trigger declaration) satisfies the gate per area.

When all three gates clear, this candidate promotes to a numbered initiative folder under `docs/wip/planning/<NN>-cross-area-ops-wiring-review/`.

**Amendment 2026-05-23 per D-IH-81-P (prior):** the original A3 framing carried the agent's CFOaaS-at-incorporation-default reflex (industry-default outsource-path framing). This was inconsistent with the operator's internal-first project thesis. The amended A3 above encodes the three-layer model + activation-trigger framing; cross-area sweeps inherit the agent-recommends-outsource-path failure-mode sanity-check per **OPS-81-21** (forwarded to I80 for skill-craft execution).

**Amendment 2026-05-23 per D-IH-81-T (this commit):** the original A2 gate required "at least one backbone area" reaching wired-enough maturity. This carried an implicit backbone-vs-non-backbone hierarchy the operator s4 framing rejected. The amended A2 above requires TWO areas exercised (any areas — FINOPS recommended but not mandated) — generalising the discipline beyond the original backbone list while preserving the two-area floor that protects against single-area pattern over-generalisation.

## 3. Scope sketch (amended 2026-05-23 per D-IH-81-T; subject to operator refinement at promotion)

### 3.1 Every-area scope with review-density tiers (NEW per D-IH-81-T)

The discipline applies to every area registered in [`baseline_organisation.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv). Per the s4 operator framing, there is no small-vs-big prioritization — only **review-density tiers** that scale with each area's current wiring density. An area's tier may evolve as that area matures + accumulates wiring surface; tier assignment is operator-discretion at each sweep.

| Tier | Cadence floor | Typical areas at this tier today | Wiring review depth |
|:---|:---|:---|:---|
| **Tier 1 — Dense wiring spines** (highest review density) | Weekly to monthly | FINOPS / PeopleOps / RevOps / LegalOps (the original D-IH-81-O backbone list) | Full cross-area sweep per cadence: counterparty/role/engagement/instrument registers fully reconciled; every paired SOP+runbook exercised; every cross-area event-trigger verified; per-tier inline-ratify of new gaps |
| **Tier 2 — Active but quieter wiring** | Quarterly | Marketing (Resonance + Reach + Experimentation), Operations (PMO + SMO), Research (Methodology) | Targeted cross-area check on the area's most wiring-dense surface (e.g., Marketing ↔ RevOps for campaign-to-engagement-event wiring; PMO ↔ everything via initiative-level governance) |
| **Tier 3 — Reference-frame areas** (lowest density today) | Semi-annual or on-trigger | Brand (within Marketing), Ethics, Compliance, Legal-as-canon-set (separate from LegalOps as operational ADVOPS plane) | Sanity-check the area's cross-pointers are still resolvable; backfill if drift detected; no requirement to mint sweep-grade machinery until tier promotes |

**Tier assignment principle:** an area's tier is a function of its **current** wiring density, not an a-priori "this area matters more" hierarchy. Areas can promote tier (Brand might move from Tier 3 to Tier 2 when an Account Management RevOps tie-in matures) or demote tier (an Operations sub-area may quiet down post-initiative-closure). Per the s4 framing: *"each small or big is just s backfiling data"* — tier is descriptive, not prescriptive.

### 3.2 Cross-area wiring checks (illustrative — to be refined at promotion; non-exhaustive)

The pre-amendment checks below remain Tier 1 examples. Per the s4 reframing, analogous Tier 2 + Tier 3 checks get added at promotion for every area-pair where wiring actually exists (the discipline's job at sweep time is **first to inventory which pairs even exist**, then check each pair).

**Tier 1 (illustrative):**

- **FINOPS ↔ RevOps**: every `process_list.csv` row tagged `area=Finance` that mentions an engagement event has a paired `area=Operations` RevOps row with matching event trigger.
- **FINOPS ↔ LegalOps**: every `advops/FILED_INSTRUMENTS.csv` row carrying a money amount (when the money-amount field exists per OPS-81-15) has a paired counterparty_id back-reference. *(Path updated per D-IH-81-S 2026-05-23.)*
- **PeopleOps ↔ FINOPS**: every role activation in `baseline_organisation.csv` (post-incorporation; first hire) has paired employment-counterparty row in FINOPS counterparty register.
- **RevOps ↔ LegalOps**: every active engagement has paired contract instrument in `advops/FILED_INSTRUMENTS.csv` (or the SME-counterparty equivalent when minted). *(Path updated per D-IH-81-S 2026-05-23.)*

**Tier 2 (NEW — illustrative; per D-IH-81-T):**

- **Marketing/Reach ↔ RevOps**: every active outbound campaign in CRM_ADAPTER-registered systems has a paired engagement-funnel stage in the engagement template registry (OPS-72-* lineage).
- **PMO ↔ every area**: every active initiative in `INITIATIVE_REGISTRY.csv` has a paired `role_owner` resolvable to `baseline_organisation.csv` AND a paired primary `process_list.csv` row owning the initiative's deliverable class.
- **Research/Methodology ↔ Marketing**: every published methodology canonical has a paired Marketing-side dossier-shape or deck-shape consumer surface (if the methodology was meant to land externally).

**Tier 3 (NEW — illustrative; per D-IH-81-T):**

- **Brand ↔ Marketing/Reach**: every BRAND_* canonical referenced by an outbound surface (deck / dossier / web page) has resolvable cross-reference + sha256 freshness (no stale brand-canon citations).
- **Ethics ↔ every area**: every area-canonical that names a People/Ethics red-line (e.g., AI agentic doctrine boundaries) has a resolvable cross-reference to `ETHICAL_AGENTIC_BOUNDARIES.md`.
- **Compliance ↔ canonical-CSV surfaces**: every canonical CSV under `compliance/canonicals/` + `compliance/canonicals/dimensions/` has resolvable PRECEDENCE.md row (this is also INDEX_INTEGRITY_DISCIPLINE IDX-02; cross-area sweep cross-checks the same surface).

The review is structurally analogous to [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md) — instead of dimensions over a cluster wave, **dimensions over every area's wiring surface at its appropriate review-density tier**.

## 4. Quartet expectations at promotion

Per [`akos-quality-fabric.mdc`](../../../../.cursor/rules/akos-quality-fabric.mdc) RULE 7 + the Wave M/N specialty-mint contract, promotion ships:

1. Canonical doctrine: `docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/CROSS_AREA_OPS_WIRING_REVIEW_DISCIPLINE.md`.
2. Pydantic chassis: `akos/hlk_cross_area_ops_wiring.py` (per-area wiring row Pydantic model).
3. Validator: `scripts/validate_cross_area_ops_wiring.py` (release-gate-wired self-test; INFO ramp).
4. Runbook: `scripts/cross_area_ops_wiring_sweep.py` (paired with SOP per [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1).
5. Cursor rule: `.cursor/rules/akos-cross-area-ops-wiring.mdc` (the *when*).
6. Skill: `.cursor/skills/cross-area-ops-wiring-craft/SKILL.md` (the *how*).
7. SOP+runbook pair: `SOP-PEOPLE_CROSS_AREA_OPS_WIRING_001.md` with AC-HUMAN + AC-AUTOMATION acceptance.
8. PEOPLE_DESIGN_PATTERN_REGISTRY row (pattern_id `pattern_cross_area_ops_wiring_review`, class `cross_area_ops_wiring_cadence`).
9. PRECEDENCE canonical + mirror rows when the discipline ships a registry.
10. HOLISTIKA_QUALITY_FABRIC §6 row (12th specialty if minted after the 11th INDEX_INTEGRITY).
11. CHANGELOG entry.
12. `process_list.csv` row(s) per area.
13. `validate_hlk.py` umbrella registration when umbrella-scoped.
14. `config/verification-profiles.json` `pre_commit` step (INFO ramp).
15. `scripts/release-gate.py` advisory wiring.

## 5. Anti-patterns to avoid at promotion (amended 2026-05-23 per D-IH-81-T)

- **Conflating with INTER_WAVE_REGRESSION.** That discipline checks wave-close integrity inside a cluster initiative. This discipline checks every-area wiring across area boundaries, independent of wave cadence.
- **REPLACED — Treating non-Tier-1 areas as out-of-scope.** ⚠️ The pre-amendment version of this anti-pattern read *"Forcing all areas into the discipline. Non-backbone areas (e.g., Marketing/Reach) may not need cross-area wiring review at this granularity."* The operator s4 framing (D-IH-81-T) explicitly rejected this — every area is in scope; only the **density** of review varies. The failure mode this REPLACED anti-pattern was trying to guard against (governance theatre on quiet areas) is genuine, but the right protection is *tier assignment + cadence floor*, not *exclusion*. See §3.1 tier table.
- **Authoring the discipline before TWO areas are mature enough to be reviewed end-to-end.** Pre-mature discipline becomes governance theatre. Hold candidate at this status until A2 gate clears (two areas exercised; not just FINOPS alone).
- **Treating it as a sub-discipline of People DoD.** It generalises beyond what People-as-DoD covers (which is per-area pattern stewardship); cross-area wiring review is a **horizontal slice** across every area boundary at the area's hierarchy + ownership level.
- **NEW — Single-area generalisation.** Minting the discipline from FINOPS patterns alone and assuming the patterns generalise to PeopleOps / Marketing / Brand without empirical exercise. Operator s4 framing implies the discipline must be exercised on at least two areas before promotion (A2 amendment) precisely to prevent single-area generalisation failure mode.
- **NEW — Tier-as-hierarchy.** Treating tier assignment as a permanent ranking ("FINOPS is more important than Brand"). Tier is **descriptive of current wiring density**, not a permanence claim about area importance. Areas legitimately promote + demote tier as their wiring matures or quiets.

## 6. External research grounding (NEW — per D-IH-81-T + `akos-applied-research-discipline.mdc` RULE 2)

The "every area gets explicit cross-area wiring at its own hierarchy + ownership level" framing is novel in this repo but well-established in two adjacent industry disciplines:

### 6.1 Team Topologies (Skelton & Pais, 2019; refined 2024–2026)

Team Topologies (the model behind much of modern platform-engineering team design) frames every team relationship through exactly **three interaction modes**: Collaboration (joint discovery for a bounded period), X-as-a-Service (one team consumes, one team provides), or Facilitating (one team helps another remove an impediment). The model's load-bearing claim — quoted from the canonical reference: *"Most team dependencies are messy because nobody defines how teams should work together. These three modes solve that by making it crystal clear when teams should collaborate closely, provide services to each other or offer temporary assistance."* ([teamtopologies.com/key-concepts](https://teamtopologies.com/key-concepts))

The interaction-mode framework is applied **per team pair** — not "backbone teams get explicit modes; small teams are exempt." Team Topologies' own 2025 update calls out a common failure mode: *"Interaction modes are dynamic, not static. Teams should flow between different modes based on their current needs and objectives... Each mode has a specific purpose and timeframe"* ([teamtopologies.com Feb 2025 update](https://teamtopologies.com/news-blogs-newsletters/2025/2/21/team-topologies-interaction-modes-breaking-through-common-misconceptions)). The directly transferable insight to this candidate's amended scope: every area-pair deserves an explicit wiring contract (analog of an interaction mode); the contract evolves as the area's wiring density evolves (analog of the dynamic-modes principle).

Cross-reference: Martin Fowler's bliki summary at [martinfowler.com/bliki/TeamTopologies.html](https://martinfowler.com/bliki/TeamTopologies.html) — *"Team Topologies is a model for describing the organization of software development teams... It defines four forms of teams and three modes of team interactions."*

### 6.2 DDD Context Mapping (Eric Evans 2003; Vaughn Vernon refinement; Codelit/Software Architecture Guild 2024–2026 industry consensus)

Domain-Driven Design's strategic context-mapping pattern frames every bounded context's integration with every other bounded context explicitly — via one of a small set of named patterns (Shared Kernel, Customer-Supplier, Conformist, Partnership, Separate Ways, Anti-Corruption Layer, Open-Host Service, Published Language). The canonical formulation: *"every term has a precise, unambiguous meaning within its bounded context... The hard problem is not what happens inside each context — it is what happens at the boundaries where contexts interact"* ([codelit.io/blog/bounded-context-mapping](https://codelit.io/blog/bounded-context-mapping)).

The pattern allows for "Separate Ways" — explicit no-integration — but the operator framing parallel here is critical: *"sometimes the right choice is 'separate ways' (no integration) when overlap isn't worth the cost"* still **names the relationship explicitly** as Separate Ways. There is no "this bounded context is too small to participate in the context map." DDD context mapping has converged on this principle over 20+ years of community refinement. The directly transferable insight to this candidate's amended scope: every area, even quiet ones, gets an explicit cross-area relationship declaration (which may be "no current wiring needed; revisit on trigger" — the Tier 3 cadence floor), but the area is *always in the map*.

Cross-reference: Software Architecture Guild's 2024 synthesis at [software-architecture-guild.com/guide/architecture/domains/integration-of-bounded-contexts/](https://software-architecture-guild.com/guide/architecture/domains/integration-of-bounded-contexts/) — *"Integration of bounded contexts is where domain design meets reality: contracts, upstream/downstream power, release schedules, and all the messy human factors..."* Plus Arho Huttunen's 2025 deep-dive at [arhohuttunen.com/domain-driven-design-integrating-bounded-contexts](https://www.arhohuttunen.com/domain-driven-design-integrating-bounded-contexts/) on integration decisions as load-bearing design choices, not implementation details.

### 6.3 Synthesis — how these ground the operator s4 framing

Both Team Topologies' interaction-mode framework and DDD's context-mapping pattern converge on the same principle the operator articulated at the Wave R Bundle C gate: **every X-pair gets an explicit relationship contract; the contract type varies with the X-pair's density + maturity; no X is too small to be in the map.** The operator's s4 verbatim — *"All area deserve cross with their hierarchy and each thing has their owner. We need to improve integrity and ensure it where it counts"* — names the same load-bearing claim from the org-Ops side. The discipline this candidate charters operationalises that claim at the Holistika area level + at the cadence each area's hierarchy + ownership warrants.

## 7. Cross-references

- Parent decisions: D-IH-81-O (architecture, active 2026-05-22); D-IH-81-P (Layer-A/B/C amendment, active 2026-05-23); D-IH-81-T (every-area amendment, active 2026-05-23 — this commit).
- Synthesis context: [`p2-tranche-t1-finops-synthesis-2026-05-22.md`](../81-vault-integrity-layout-milestones-retrofit/reports/i81/p2-tranche-t1-finops-synthesis-2026-05-22.md) §10.1.
- Sister disciplines:
  - [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md) — structural analogue (review-cadence discipline shape).
  - [`INDEX_INTEGRITY_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md) — sister 11th specialty.
- Parent rules:
  - [`akos-people-discipline-of-disciplines.mdc`](../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) RULE 1 (People owns patterns; this candidate names a pattern People will own).
  - [`akos-applied-research-discipline.mdc`](../../../../.cursor/rules/akos-applied-research-discipline.mdc) RULE 2 (novel framings require external citation — §6 above satisfies this for the s4 reframing).
- Operator-scratchpad audit-trail entries:
  - `docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md` 2026-05-22 wave-R-lane-D-T1-gate drain (original D-IH-81-O framing).
  - `docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md` 2026-05-23 wave-R-bundle-C-amendment drain (D-IH-81-T amendment — this commit).
