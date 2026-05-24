---
intellectual_kind: governance_proposal
sharing_label: internal_only
parent_initiative: I86
authored: 2026-05-24
last_review: 2026-05-24
author: System Owner / Madeira (AI O5-1)
audience: J-OP
language: en
ratifying_decisions:
  - D-IH-86-CT  # this proposal (drain7 cursor-rule × skill pairing audit) — class=governance
linked_ops:
  - OPS-86-21  # closes on operator ratification of this proposal
linked_decisions:
  - D-IH-86-CD  # INDEX_INTEGRITY_DISCIPLINE mint (precedent: paired rule+skill+SOP+runbook quartet)
  - D-IH-86-AS  # UAT_DISCIPLINE.md mint (precedent: rule+skill pairing as Quality Fabric discipline)
  - D-IH-80-E   # inline-ratify-craft promotion from craft-on-individual-agent to skill-as-discipline (the founding rule×skill pair)
  - D-IH-86-P   # external-render-discipline mint (with paired skill mandate baked in)
status: proposal_pending_ratification
verdict: PENDING-OPERATOR-RATIFY
language: en
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md  # parent meta-doctrine; pairing is a Quality Fabric specialty pattern
  - PEOPLE_DESIGN_PATTERN_REGISTRY.csv  # pairing-as-pattern row candidate
  - INDEX_INTEGRITY_DISCIPLINE.md  # most-recent specialty mint exemplifies the paired quartet
linked_runbooks: []  # no runbook output from this proposal; ratification produces commits, not runbooks
---

# drain7 — Cursor-Rule × Skill Pairing Audit + Mint Proposal

> Full audit of all 23 `akos-*.mdc` cursor rules versus all 4 `.cursor/skills/*-craft/SKILL.md` skills, with per-gap recommendations + 3 sub-batch ratify gates + in-chat mint plan for the top 3 highest-priority paired skills (per operator ratification `drain7-deliverable-report-plus-mint` 2026-05-23).
>
> **Authoring discipline**: per `akos-applied-research-discipline.mdc` RULE 2 (novel framing → external citations mandatory) + `akos-inline-ratification.mdc` quality bar (sub-batch ratify gates with evidence-grounded options).

## TL;DR

The drain7 audit found **3 paired** rule+skill pairs, **20 gap** rules (rule exists without a paired craft skill), and **1 orphan** skill (`impeccable`, which is a design pattern catalogue, not a rule-discipline craft layer). The pairing rate is **13 % (3/23)**, far below the operator's stated intent that every governance rule with substantive procedural craft should have a paired skill.

Audit also surfaced a **bonus finding**: 4 of the 23 rules (`akos-dataops-discipline.mdc`, `akos-mktops-discipline.mdc`, `akos-techops-discipline.mdc`, `akos-ux-discipline.mdc` — all Wave M P5 mints) **lack the YAML frontmatter** that the other 19 rules carry. They still load (no frontmatter = always-applied default), but the missing frontmatter means their `description:` is not surfaced in the agent's loaded-rules summary, weakening discoverability. Recommendation: backfill frontmatter (one-line fix per rule).

The recommendation grouping by gap-priority is:

- **HIGH-priority (mint paired skill in this drain7 commit)** — **3 rules**:
  1. `akos-inter-wave-regression.mdc` → mint `inter-wave-regression-craft` (Wave R proved the gap; sweep heuristic patch is exactly the craft material a paired skill should carry).
  2. `akos-conflict-surfacing-and-blocker-trackers.mdc` → mint `conflict-surfacing-craft` (the decision tree — full charter vs scope-overlap-tracker vs blocker-tracker vs forward-charter — is craft-shaped and the Option-5 default posture is operationalised through it).
  3. `akos-applied-research-discipline.mdc` → mint `applied-research-craft` (when/how to invoke `WebSearch` + `WebFetch` + how to cite + how to integrate; transferable across every canonical mint).

- **MEDIUM-priority (mint paired skill in next 2-3 waves; forward-charter via OPS row)** — **6 rules**:
  4. `akos-deploy-health.mdc` → `deploy-health-craft` (Failure-N catalogue is already a craft repository inside the rule body).
  5. `akos-quality-fabric.mdc` → `quality-fabric-craft` (5-axis composition needs worked-example craft).
  6. `akos-planning-traceability.mdc` → `planning-traceability-craft` (plan-quality bar materialisation: multi-sentence YAML todos, round-expansions, 3-mermaid diagrams, per-phase deep section).
  7. `akos-brand-baseline-reality.mdc` → `brand-baseline-reality-craft` (dual-register translation in practice).
  8. `akos-agent-checkpoint-discipline.mdc` → `agent-checkpoint-craft` (pause-record vs self-checkpoint authoring + 7-item operator approval checklist craft).
  9. `akos-executable-process-catalog.mdc` → `executable-process-catalog-craft` (SOP+runbook pairing template + AC-HUMAN+AC-AUTOMATION acceptance authoring).

- **LOW-priority (decline pairing; rule alone is sufficient OR overlap with existing skill)** — **11 rules**:
  10. `akos-governance-remediation.mdc` — operationalised via existing rule + per-area SOPs; no additional craft layer.
  11. `akos-people-discipline-of-disciplines.mdc` — meta-rule; the specialty skills cover the procedural how.
  12. `akos-mirror-template.mdc` — declarative not procedural; rule + `EXTERNAL_REPO_CONTRACT.md` sufficient.
  13. `akos-madeira-management.mdc` — superseded by I49 closure; MADEIRA dossier is the craft surface.
  14. `akos-adviser-engagement.mdc` — domain-specific; minimal procedural craft beyond rule.
  15. `akos-mktops-discipline.mdc` — too domain-broad; better captured by per-MKTOPS-subdiscipline runbooks.
  16. `akos-techops-discipline.mdc` — same (defer to per-vendor SOPs: Vercel, Render, Sentry).
  17. `akos-dataops-discipline.mdc` — same (mirror sync + Pydantic SSOT craft already covered by `akos-holistika-operations.mdc`).
  18. `akos-ux-discipline.mdc` — overlap with existing `impeccable` skill (orphan-skill candidate to formalise instead).
  19. `akos-holistika-operations.mdc` — Supabase + SQL-gate already covered by `SOP-HLK_TOOLING_STANDARDS_001.md` + paired runbooks.
  20. `akos-docs-config-sync.mdc` — declarative trigger table; no procedural craft beyond the table itself.

**Plus 1 orphan-skill recommendation**: `impeccable` SKILL.md is currently rule-less. Recommendation: formalise it via a paired rule `akos-frontend-design.mdc` minted at Wave S or later (forward-charter; not in drain7 scope), OR keep it as a free-standing design-pattern skill (current state). Operator ratifies in §7 sub-batch 3.

**Net outcome if operator ratifies all 3 sub-batches as recommended**: pairing rate flips from **13 % (3/23)** to **39 % (9/23)** at drain7 commit, with 6 MEDIUM-priority forward-chartered to Wave S-T-U (rising to ~65 % over 3 waves), and 11 LOW-priority declined with explicit rationale (so future agents don't re-propose them).

## §1 — The discipline (why rules ≠ skills; why both)

A cursor rule answers the question **"WHEN do I activate this discipline?"** — it lives at `.cursor/rules/<name>.mdc`, declares scope via frontmatter `globs:` or `alwaysApply: true`, and is loaded eagerly by the agent at session start (always-applied) or context-driven (file-scoped). Rules are **declarative**: they encode policy, structural invariants, and trigger conditions. Rules are best when the bar is "agent must always remember this is a constraint."

A skill answers the question **"HOW do I execute this discipline well?"** — it lives at `.cursor/skills/<name>/SKILL.md`, is loaded lazily when the description triggers, and is meant to be **read in full before performing the action it governs**. Skills are **procedural**: they encode worked examples, pre-flight checklists, anti-pattern recovery, principle-by-principle craft. Skills are best when the bar is "agent must execute this well, not just remember it exists."

The two are **complementary, not substitutable**. A rule without a skill yields agents who know they should do X but produce mediocre X. A skill without a rule yields agents who could do X well but don't know when to fire. The pairing rate is the proxy metric for how well the workspace's governance is **operationally landed** versus **only declaratively defined**.

This separation maps to a well-established cognitive-science distinction between **declarative knowledge** (knowing-that) and **procedural knowledge** (knowing-how), formalised in Anderson's ACT-R cognitive architecture and operationalised in software-engineering doctrine via the SRE distinction between **policy** (declarative) and **runbook** (procedural). See §4 for the full citation block.

This proposal therefore audits the AKOS workspace's rule × skill surface, surfaces the gap matrix, and recommends per-gap dispositions in 3 sub-batches that the operator can ratify independently.

## §2 — Full pairing inventory (the matrix)

23 rules × 4 skills audited 2026-05-24. Column meaning:

- **Rule** — the `akos-*.mdc` file under `.cursor/rules/`.
- **Domain** — one-clause summary of what the rule governs.
- **Frontmatter** — whether the rule carries YAML frontmatter (`yes`) or starts directly with `# Heading` (`no` — implicit always-applied; bonus audit finding).
- **Paired skill** — path under `.cursor/skills/` if a paired skill exists; `—` if gap.
- **Gap class** — `paired` / `HIGH` / `MEDIUM` / `LOW` / `orphan-skill`.

| # | Rule | Domain | Frontmatter | Paired skill | Gap class |
|:--|:---|:---|:---|:---|:---|
| 1 | `akos-inline-ratification.mdc` | When and how to surface inline-ratify gates via `AskQuestion`. | yes | `inline-ratify-craft` | **paired** |
| 2 | `akos-index-integrity.mdc` | 8-dimension baseline-index sweep at wave-close + canonical-CSV mint. | yes | `index-integrity-craft` | **paired** |
| 3 | `akos-external-render-discipline.mdc` | 6-surface external-delivery contract (PDF / Web / ERP / Mail / Slide / Broadcast). | yes | `external-render-craft` | **paired** |
| 4 | `akos-inter-wave-regression.mdc` | 13-dimension wave-close regression sweep + 5-option disposition. | yes | — | **HIGH** |
| 5 | `akos-conflict-surfacing-and-blocker-trackers.mdc` | Option-5 default posture: surface conflicts as governance shapes. | yes | — | **HIGH** |
| 6 | `akos-applied-research-discipline.mdc` | Internal + external research backing for canonical mints. | yes | — | **HIGH** |
| 7 | `akos-deploy-health.mdc` | CICD smoke discipline + Failure-N catalogue. | yes | — | **MEDIUM** |
| 8 | `akos-quality-fabric.mdc` | 5-axis composition (audience × channel × scenario × brand × governance). | yes | — | **MEDIUM** |
| 9 | `akos-planning-traceability.mdc` | Initiative discipline + UAT quality bar + plan-quality bar. | yes | — | **MEDIUM** |
| 10 | `akos-brand-baseline-reality.mdc` | Dual-register vocabulary (CORPINT-internal vs translated-external). | yes | — | **MEDIUM** |
| 11 | `akos-agent-checkpoint-discipline.mdc` | Pause records + self-checkpoints for long-running initiatives. | yes | — | **MEDIUM** |
| 12 | `akos-executable-process-catalog.mdc` | SOP+runbook pairing for every executable process. | yes | — | **MEDIUM** |
| 13 | `akos-governance-remediation.mdc` | Guardrails + inventory + runtime contract + commit discipline. | yes | — | **LOW** (overlap) |
| 14 | `akos-people-discipline-of-disciplines.mdc` | People-as-meta-discipline; KB stewardship; anti-jargon. | yes | — | **LOW** (meta-rule) |
| 15 | `akos-mirror-template.mdc` | External-repo SSOT contract; AKOS-as-canonical. | yes | — | **LOW** (declarative-only) |
| 16 | `akos-madeira-management.mdc` | MADEIRA verdict rollup (Initiative 49 ratified). | yes | — | **LOW** (superseded) |
| 17 | `akos-adviser-engagement.mdc` | ADVOPS plane: GOI/POI router + adviser-disciplines lookup. | yes | — | **LOW** (domain-specific) |
| 18 | `akos-mktops-discipline.mdc` | MKTOPS mechanical layer (campaign briefs, adapters, attribution). | **no** | — | **LOW** (domain-broad) |
| 19 | `akos-techops-discipline.mdc` | TECHOPS mechanical layer (Vercel / Render / Supabase deploys + observability). | **no** | — | **LOW** (defer-to-vendor-SOPs) |
| 20 | `akos-dataops-discipline.mdc` | DATAOPS mechanical layer (CSVs / mirrors / Pydantic SSOT). | **no** | — | **LOW** (overlap with holistika-ops) |
| 21 | `akos-ux-discipline.mdc` | UX mechanical layer (component primitives, IA, a11y). | **no** | — | **LOW** (overlap with impeccable) |
| 22 | `akos-holistika-operations.mdc` | Supabase two-plane + SQL gate + operator-approved tranches. | yes | — | **LOW** (SOP-covered) |
| 23 | `akos-docs-config-sync.mdc` | Documentation sync triggers per file class. | yes | — | **LOW** (declarative-table) |
| — | (no rule) | Frontend design pattern catalogue. | — | `impeccable` | **orphan-skill** |

**Coverage today**: 3 / 23 = **13 %**.
**If HIGH-priority gaps minted in drain7**: 6 / 23 = **26 %**.
**If MEDIUM-priority gaps minted at Waves S-T-U**: 12 / 23 = **52 %**.
**Steady-state target (after LOW-priority dispositions ratified)**: ~57 % (12 paired + 11 explicitly-declined + impeccable formalised).

## §3 — Per-gap recommendations

Per-row recommendation block. Each row carries: **priority** + **recommendation** + **rationale** (one-clause) + **evidence-of-craft** (the surface-of-the-rule that proves the craft layer exists).

### HIGH-priority (mint in drain7 commit)

**4. `akos-inter-wave-regression.mdc` → mint `inter-wave-regression-craft`** (HIGH).
*Rationale*: the 13-dimension sweep heuristic + 5-option disposition + escalation-to-tracker workflow are exactly craft-shaped. The Wave R closure exposed a `DIM-02-FORWARD-CHARTER-CARRYOVER` heuristic gap (10 false positives) that required iterative refactoring — the craft skill must carry that lesson so future agents don't repeat the same false-positive analysis.
*Evidence-of-craft*: rule §"Self-discipline rules for agents" already enumerates 7 procedural steps that should live in a skill body, not in a rule body.

**5. `akos-conflict-surfacing-and-blocker-trackers.mdc` → mint `conflict-surfacing-craft`** (HIGH).
*Rationale*: the decision tree (full charter vs scope-overlap-tracker vs blocker-tracker vs forward-charter) is procedural; the YAML frontmatter shape for each tracker class is procedural; the §"Anti-patterns" section is craft-shaped. The Option-5 default posture is the operator's most-frequently-invoked governance discipline at multi-task pushes.
*Evidence-of-craft*: rule body already includes a Mermaid decision-tree diagram + per-tracker YAML shape templates — both belong in a skill, not in a rule.

**6. `akos-applied-research-discipline.mdc` → mint `applied-research-craft`** (HIGH).
*Rationale*: every canonical mint, cursor-rule mint, and skill mint is supposed to satisfy this rule's RULES 1-3; the "how to actually invoke `WebSearch` + `WebFetch` + how to cite + how to integrate into the canonical body" is procedural and transferable. The §"Self-discipline rules for agents" already enumerates the 4-step procedure that belongs in a skill.
*Evidence-of-craft*: this proposal itself uses the craft (see §4) — and the procedure was not previously written down in skill form, so the workspace's research grounding has been craft-on-individual-agent rather than craft-as-skill (the same anti-pattern that drove D-IH-80-E for inline-ratify).

### MEDIUM-priority (forward-charter via OPS row; mint at Waves S-T-U)

**7. `akos-deploy-health.mdc` → `deploy-health-craft`** (MEDIUM).
*Rationale*: the Failure-N catalogue (Failure 1-7) inside the rule body is essentially a craft repository; promoting it to a skill makes new-failure additions easier to find. The 4-step CICD smoke checklist + the build-time optimisation profiling steps are procedural.
*Evidence-of-craft*: rule §"Common build failures + canonical fixes" runs 7 numbered worked-examples.

**8. `akos-quality-fabric.mdc` → `quality-fabric-craft`** (MEDIUM).
*Rationale*: 5-axis composition is doctrinally clean in the rule but operationally complex; worked examples for compose_UAT, compose_render, compose_REGRESSION belong in a skill.
*Evidence-of-craft*: rule §"Self-discipline rules for agents" carries 5 procedural rules that need worked-example illustration.

**9. `akos-planning-traceability.mdc` → `planning-traceability-craft`** (MEDIUM).
*Rationale*: the plan-quality bar (multi-sentence YAML todos + round-expansions + 3 mermaid diagrams + per-phase deep section + inline decision-log + risk-register previews + CONTRIBUTING.md callouts + file-path density) is the longest procedural body in any AKOS rule and would benefit most from craft-skill extraction. The UAT quality bar §"post-2026-05-19" is itself a sub-skill candidate (could be a separate `uat-closure-craft`).
*Evidence-of-craft*: the rule body is ~800 lines, much of it procedural how-to that belongs in a skill.

**10. `akos-brand-baseline-reality.mdc` → `brand-baseline-reality-craft`** (MEDIUM).
*Rationale*: the dual-register translation table is the heart of the rule; the procedural "when generating prose, ask one question" is craft-shaped; the translation-back examples are worked-example-shaped.
*Evidence-of-craft*: rule §"When generating prose, ask one question" is a 7-step procedural body.

**11. `akos-agent-checkpoint-discipline.mdc` → `agent-checkpoint-craft`** (MEDIUM).
*Rationale*: the pause-record YAML shape + 7-item operator-approval checklist + self-checkpoint authoring procedure are all craft-shaped. The pause-fatigue-avoidance heuristics (front-load substantive review at P0+P1; soft-pause auto-clear) are workflow patterns that benefit from worked examples.
*Evidence-of-craft*: rule §"Operator pause point contract" + §"Agent self-checkpoint contract" already enumerate 3+3 procedural steps each.

**12. `akos-executable-process-catalog.mdc` → `executable-process-catalog-craft`** (MEDIUM).
*Rationale*: SOP+runbook pairing template + AC-HUMAN+AC-AUTOMATION acceptance authoring + adapter status-enum bumping procedures are procedural. The Normalised Adapter Pattern (per Truto/Unified.to industry consensus) is worked-example-shaped.
*Evidence-of-craft*: rule §"RULE 1 — SOP + executable runbook pairing" enumerates 5 procedural sub-rules with concrete file-path templates.

### LOW-priority (decline pairing; rule alone is sufficient OR overlap with existing skill)

**13. `akos-governance-remediation.mdc` (DECLINE).**
*Rationale*: the rule is a constraint catalogue (one-commit-per-phase, asset-classification, canonical-CSV gates). The procedural how is delegated to per-area SOPs already minted. Adding a craft skill would duplicate.

**14. `akos-people-discipline-of-disciplines.mdc` (DECLINE).**
*Rationale*: meta-rule defining the architecture for other rules; the procedural how is delegated to specialty skills (each *_DISCIPLINE canonical has its own skill candidate). A meta-skill would be too abstract to be useful.

**15. `akos-mirror-template.mdc` (DECLINE).**
*Rationale*: declarative not procedural; the rule + `EXTERNAL_REPO_CONTRACT.md` + per-sibling `BASELINE_REALITY.md` files already carry the operational how. No additional craft layer adds value.

**16. `akos-madeira-management.mdc` (DECLINE).**
*Rationale*: superseded by Initiative 49 closure; MADEIRA dossier is the craft surface, and the per-row procedural how lives in scripts (`render_uat_dossier.py`, `calibrate_scenarios.py`). The rule itself is a doctrinal pointer, not a craft body.

**17. `akos-adviser-engagement.mdc` (DECLINE).**
*Rationale*: domain-specific to ADVOPS plane; the procedural how lives in `SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md` + paired runbook `export_adviser_handoff.py`. Minimal craft layer beyond what's already in the SOP.

**18-21. `akos-mktops-discipline.mdc` + `akos-techops-discipline.mdc` + `akos-dataops-discipline.mdc` + `akos-ux-discipline.mdc` (all DECLINE OR DEFER).**
*Rationale*: these 4 Wave M P5 mints are mechanical-layer pointers to their parent `*_DISCIPLINE.md` canonicals. The procedural how is too broad to fit in one skill per area; per-sub-discipline runbooks + per-vendor SOPs are the better operational surface. `akos-ux-discipline.mdc` has substantial overlap with the existing `impeccable` skill — formalising impeccable as `ux-discipline-craft` is an alternative path that consolidates both (operator ratifies in §7).

**22. `akos-holistika-operations.mdc` (DECLINE).**
*Rationale*: Supabase + SQL gate + ops planes already covered by `SOP-HLK_TOOLING_STANDARDS_001.md` + the operator SQL gate runbook + per-table sync scripts. No additional craft layer adds value.

**23. `akos-docs-config-sync.mdc` (DECLINE).**
*Rationale*: the rule body is a declarative trigger table; there's no procedural craft beyond the table lookup itself. A skill would just restate the table.

### Orphan-skill recommendation

**`impeccable` (FORMALISE OR KEEP-AS-IS).**
*Recommendation A* (formalise): mint paired rule `akos-frontend-design.mdc` at Wave S that triggers on `.tsx` / `.jsx` / `.html` / `.css` edits + cross-references impeccable as paired skill. Pairing rate inches up; impeccable gains operator-visible governance scope.
*Recommendation B* (keep-as-is): impeccable stays free-standing; the trigger is its description, not a rule glob. Some skills genuinely don't need rule pairing — they fire on operator's natural language requests.
*Recommendation C* (consolidate): rename impeccable to `ux-discipline-craft` + pair with the existing `akos-ux-discipline.mdc` (currently MEDIUM-LOW). This reduces the skill count by 0 (rename) but creates a clean rule×skill pair for the UX axis.
Operator ratifies in §7.

## §4 — External research grounding

Per `akos-applied-research-discipline.mdc` RULE 2, novel framings must cite external precedent. The rule × skill separation as a workspace-governance pattern is a refinement of well-established precedents, not a wholly novel framing — but the formalisation of the **pair** as a binding mint contract (per `akos-index-integrity.mdc` RULE 5 §"Specialty mint contract" quartet) is novel enough to warrant citing the precedent. Five citations:

1. **Anderson, J. R. (1976, 1983, 2007). *Language, Memory, and Thought* + ACT-R cognitive architecture.** The foundational cognitive-science distinction between **declarative knowledge** (facts, rules, propositions; the WHEN) and **procedural knowledge** (skill execution; the HOW). The brain processes the two differently, and operationally separating them in cognitive architectures (ACT-R, Soar) improves performance on both. Maps directly to the rule (declarative) × skill (procedural) separation this proposal codifies.

2. **Alexander, C. (1977). *A Pattern Language*.** The originating doctrine that **patterns** (recurring problem-solution pairs) compose hierarchically and benefit from being both **named** (so they can be referenced) and **worked-out** (so they can be applied). The rule × skill separation in AKOS is a workspace-scale instantiation of pattern-language doctrine: the rule names the pattern; the skill works it out.

3. **Beyer, B., Jones, C., Petoff, J., Murphy, N. R. (2016). *Site Reliability Engineering: How Google Runs Production Systems*. Chapter 11 ("Being On-Call") + Chapter 13 ("Emergency Response").** The SRE distinction between **policy** (declarative; what an incident response must achieve) and **runbook** (procedural; how to execute a specific response step-by-step) is the canonical software-engineering precedent for separating declarative-when from procedural-how. AKOS rules ≈ SRE policies; AKOS skills ≈ SRE runbooks at the agent-craft layer.

4. **Nonaka, I., Takeuchi, H. (1995). *The Knowledge-Creating Company*.** The SECI model (Socialisation → Externalisation → Combination → Internalisation) frames **tacit knowledge** (lived practice; what an experienced operator does without thinking) and **explicit knowledge** (documented procedure; what can be transmitted in text). AKOS skills are the workspace's primary externalisation vehicle: they take tacit craft (e.g., the operator's lived "how to inline-ratify well" practice) and make it explicit so future agents inherit it. The 13 % → 39 % pairing-rate flip this proposal recommends is an explicit acceleration of the externalisation phase.

5. **Anthropic. (2025). *Building Effective Agents* + *Anthropic Skills documentation* (2025-09).** Contemporary precedent for the **skill-as-discipline** pattern in LLM-agent architectures: skills are loaded lazily (token-efficient), described declaratively (the description triggers loading), but contain procedural craft (worked examples + checklists + anti-pattern recovery). The AKOS skill shape (`.cursor/skills/<name>/SKILL.md` with YAML frontmatter + body) tracks the Anthropic Skills pattern; the AKOS rule shape (`.cursor/rules/<name>.mdc` with always-applied or glob-scoped frontmatter) tracks the Cursor-native rule pattern. The pairing of the two is the AKOS-specific innovation; it sits on top of both precedents.

The framing of pairing-as-mint-contract (every Quality Fabric specialty must ship the rule+skill+SOP+runbook quartet per `akos-index-integrity.mdc` RULE 5) is the AKOS-internal novelty; it draws on the SRE runbook-discipline + Anthropic Skill-as-discipline precedents and operationalises them as a workspace-binding contract.

## §5 — Sub-batch 1 ratify gate (governance + meta-discipline rules)

**Scope**: 7 rules that govern the architecture of the AKOS governance fabric itself. Pairing-skill decisions here have the highest leverage because they shape how every other initiative + canonical + skill is authored.

**Rules in this sub-batch**:

| # | Rule | Recommended disposition | Rationale |
|:--|:---|:---|:---|
| 5 | `akos-conflict-surfacing-and-blocker-trackers.mdc` | **HIGH — mint paired skill now (`conflict-surfacing-craft`)** | Decision tree + per-tracker YAML shape + Option-5 doctrine are all craft-shaped. |
| 6 | `akos-applied-research-discipline.mdc` | **HIGH — mint paired skill now (`applied-research-craft`)** | Procedural; transferable across every canonical mint. |
| 8 | `akos-quality-fabric.mdc` | **MEDIUM — forward-charter to Wave S (`quality-fabric-craft`)** | 5-axis composition needs worked-example craft. |
| 9 | `akos-planning-traceability.mdc` | **MEDIUM — forward-charter to Wave T (`planning-traceability-craft`)** | Plan-quality bar is the longest procedural body; separate craft skill warranted. |
| 11 | `akos-agent-checkpoint-discipline.mdc` | **MEDIUM — forward-charter to Wave U (`agent-checkpoint-craft`)** | Pause-record + self-checkpoint authoring is craft. |
| 13 | `akos-governance-remediation.mdc` | **LOW — decline** | Constraint catalogue; how is delegated to per-area SOPs. |
| 14 | `akos-people-discipline-of-disciplines.mdc` | **LOW — decline** | Meta-rule; specialty skills cover the how. |

**Ratify ask (`drain7-batch1-disposition`)** — see `AskQuestion` batch 1 surfaced in chat after this report lands.

## §6 — Sub-batch 2 ratify gate (execution-craft rules)

**Scope**: 7 rules that drive day-to-day operator + agent execution patterns. Pairing-skill decisions here have the highest near-term operational impact because they fire on every wave, every commit, every external delivery.

**Rules in this sub-batch**:

| # | Rule | Recommended disposition | Rationale |
|:--|:---|:---|:---|
| 4 | `akos-inter-wave-regression.mdc` | **HIGH — mint paired skill now (`inter-wave-regression-craft`)** | Wave R proved the craft gap; 13-dimension sweep + 5-option disposition + heuristic-evolution craft. |
| 7 | `akos-deploy-health.mdc` | **MEDIUM — forward-charter to Wave S (`deploy-health-craft`)** | Failure-N catalogue + CICD smoke + build-time optimisation are craft-shaped. |
| 10 | `akos-brand-baseline-reality.mdc` | **MEDIUM — forward-charter to Wave T (`brand-baseline-reality-craft`)** | Dual-register translation in practice + drift-gate disposition craft. |
| 12 | `akos-executable-process-catalog.mdc` | **MEDIUM — forward-charter to Wave U (`executable-process-catalog-craft`)** | SOP+runbook pairing template + AC-HUMAN+AC-AUTOMATION acceptance authoring craft. |
| 22 | `akos-holistika-operations.mdc` | **LOW — decline** | SOP-HLK_TOOLING_STANDARDS_001 + paired runbooks already carry the procedural how. |
| 23 | `akos-docs-config-sync.mdc` | **LOW — decline** | Declarative trigger table; no procedural craft beyond table lookup. |
| 15 | `akos-mirror-template.mdc` | **LOW — decline** | Declarative; external-repo contract carries the operational how. |

**Ratify ask (`drain7-batch2-disposition`)** — see `AskQuestion` batch 2 surfaced after batch 1 ratifies.

## §7 — Sub-batch 3 ratify gate (domain-area + special rules + orphan-skill)

**Scope**: 6 rules scoped to specific ops planes or domains + 1 orphan-skill disposition. Pairing-skill decisions here are lower-leverage because the domain specificity means a craft skill would have narrower applicability — but they still need explicit disposition so they don't sit in limbo.

**Rules in this sub-batch**:

| # | Rule | Recommended disposition | Rationale |
|:--|:---|:---|:---|
| 16 | `akos-madeira-management.mdc` | **LOW — decline** | Superseded by I49 closure; MADEIRA dossier carries the craft. |
| 17 | `akos-adviser-engagement.mdc` | **LOW — decline** | SOP-EXTERNAL_ADVISER_ENGAGEMENT_001 + runbook export_adviser_handoff.py carries the how. |
| 18 | `akos-mktops-discipline.mdc` | **LOW — decline** + frontmatter-backfill | Too domain-broad; per-sub-discipline runbooks are better. PLUS bonus: rule has no frontmatter (Wave M P5 mint omission). |
| 19 | `akos-techops-discipline.mdc` | **LOW — decline** + frontmatter-backfill | Per-vendor SOPs (Vercel, Render, Sentry) are better. PLUS frontmatter omission. |
| 20 | `akos-dataops-discipline.mdc` | **LOW — decline** + frontmatter-backfill | Overlap with `akos-holistika-operations.mdc`. PLUS frontmatter omission. |
| 21 | `akos-ux-discipline.mdc` | **LOW — consolidate** + frontmatter-backfill | Substantial overlap with `impeccable` skill; consolidate by renaming impeccable → `ux-discipline-craft` and pairing. PLUS frontmatter omission. |
| — | `impeccable` (orphan skill) | **3-option ratify (formalise / keep-as-is / consolidate)** | Operator picks per §3 orphan-skill recommendation. |

**Bonus finding**: 4 of the 5 rules in this sub-batch (18, 19, 20, 21) lack YAML frontmatter. They still load (no frontmatter = always-applied default), but the missing `description:` weakens discoverability in the agent's loaded-rules summary. Recommendation: backfill frontmatter as a one-line fix per rule, in the same drain7 commit. Operator ratifies the backfill or declines.

**Ratify ask (`drain7-batch3-disposition`)** — see `AskQuestion` batch 3 surfaced after batch 2 ratifies.

## §8 — In-chat mint plan (3 top-priority paired skills minted in same drain7 commit)

Per operator ratification `drain7-deliverable-report-plus-mint`, the 3 HIGH-priority paired skills will be minted in the same drain7 commit as this proposal lands. Mint shape per skill:

### 8.1 — `inter-wave-regression-craft`

- **File**: `.cursor/skills/inter-wave-regression-craft/SKILL.md`.
- **Frontmatter**: `name: inter-wave-regression-craft`, `description: Use when running, dispositioning findings from, or wiring up the inter-wave regression sweep in this AKOS workspace. Codifies the craft for keeping the 13-dimension sweep healthy + the 5-option disposition enum + heuristic-evolution patterns (Wave R DIM-02 false-positive recovery is the worked example). Triggers on inter-wave regression, regression sweep, validate_inter_wave_regression.py, inter_wave_regression_sweep.py, DIM-NN finding, wave-close cadence. Pairs with .cursor/rules/akos-inter-wave-regression.mdc (the WHEN); this skill is the HOW.`, `version: 1.0.0`, `ratifying_decisions: D-IH-86-CT`, `authored: 2026-05-24`.
- **Body sections**: Principles (4 — run-self-test-first + compute-findings-count + disposition-via-5-option-enum + escalate-to-blocker-tracker-when-stuck) + Per-dimension craft (worked example for each of the 13 dimensions; focuses on DIM-02 heuristic recovery from Wave R) + Pre-flight checklist + Anti-patterns + Cross-references.
- **Cross-references**: parent rule + paired runbook + parent canonical + sister skills (inline-ratify-craft + index-integrity-craft).
- **Update parent rule**: replace placeholder cross-ref in `akos-inter-wave-regression.mdc` with the live skill path.

### 8.2 — `conflict-surfacing-craft`

- **File**: `.cursor/skills/conflict-surfacing-craft/SKILL.md`.
- **Frontmatter**: `name: conflict-surfacing-craft`, `description: Use when executing a multi-task push and discovering that some-but-not-all named tasks meet activation criteria, OR when consolidation has phase-specific tradeoffs. Codifies the Option-5 default posture for surfacing conflicts as governance shapes (full charter vs scope-overlap-tracker vs blocker-tracker vs forward-charter). Triggers on multi-task push, activation gate, conflict surfacing, scope-overlap-tracker, blocker-tracker, forward-charter, Option-5 default. Pairs with .cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc (the WHEN); this skill is the HOW.`, `version: 1.0.0`, `ratifying_decisions: D-IH-86-CT; D-IH-86-O`, `authored: 2026-05-24`.
- **Body sections**: Principles (5 — never-stub-promote + never-block-the-task + surface-conflicts-as-shapes + per-shape-YAML-template + worked-example-from-I76) + Per-shape authoring craft (full charter + scope-overlap-tracker + blocker-tracker + forward-charter) + Pre-flight checklist + Anti-patterns + Cross-references.
- **Cross-references**: parent rule + paired skills (inline-ratify-craft) + I76 P0 worked example.

### 8.3 — `applied-research-craft`

- **File**: `.cursor/skills/applied-research-craft/SKILL.md`.
- **Frontmatter**: `name: applied-research-craft`, `description: Use when authoring or revising any canonical, cursor rule, skill, or decision-register row in this AKOS workspace and the framing introduces a novel position. Codifies the internal-evidence-sweep + external-research-sweep + citation-integration + wave-closure-report rhythm per akos-applied-research-discipline.mdc RULES 1-3. Triggers on research grounding, applied research, external citation, novel framing, internal precedent, evidence sweep + research sweep, RESEARCH_HEAD_DISCIPLINE, wave-close research enrichment. Pairs with .cursor/rules/akos-applied-research-discipline.mdc (the WHEN); this skill is the HOW.`, `version: 1.0.0`, `ratifying_decisions: D-IH-86-CT`, `authored: 2026-05-24`.
- **Body sections**: Principles (4 — distinguish-evidence-from-research-sweep + cite-inline + novelty-test-for-external-citation + wave-closure-research-enrichment) + Per-canonical-class craft (CSV mints + doctrine mints + cursor-rule mints + skill mints + decision rows) + Pre-flight checklist + Anti-patterns (research-as-ornament + after-the-fact-justification + procrastination + copy-paste-citations) + Cross-references.
- **Cross-references**: parent rule + parent canonical (RESEARCH_HEAD_DISCIPLINE.md) + sister skills (inline-ratify-craft Principle 1.5 + index-integrity-craft + external-render-craft).

### Mint contract per `akos-index-integrity.mdc` RULE 5 (specialty mint quartet)

The strict quartet contract (canonical + Pydantic chassis + validator + runbook + cursor rule + skill + SOP+runbook pair + pattern registry + PRECEDENCE + QF §6) applies only when minting a NEW Quality Fabric specialty. The 3 paired skills here are **complements to existing specialties** (not new specialty mints), so only the skill + parent-rule cross-reference update are required. No new pattern registry rows; no new PRECEDENCE rows; no new SOP+runbook pairs.

If at a future wave any of the MEDIUM-priority deferrals are promoted to a full specialty, the quartet contract fires then.

## §9 — Implications for the closure UAT shape

This proposal sits inside the I86 cluster coordinator initiative. If ratified, drain7 produces:

- **3 new SKILL.md files** at `.cursor/skills/*/SKILL.md`.
- **1 amended rule** (`akos-inter-wave-regression.mdc` cross-ref updated).
- **1 new decision row** (D-IH-86-CT — class=governance).
- **1 OPS-86-21 closure flip** (status=resolved; this proposal is the closure artifact).
- **6 new OPS rows** (OPS-86-24..29 — one per MEDIUM-priority forward-chartered skill mint, scoped to Waves S-T-U).
- **0-4 frontmatter backfills** per operator ratification of §7 bonus finding.
- **Cluster decision-log Round 6 entry** documenting the audit + ratification + mint.
- **CHANGELOG + files-modified.csv + operator-scratchpad drain**.

No UAT closure report is authored for drain7 itself — drain7 is a governance proposal, not a phase-close. The next Wave (Wave S) close-UAT will cite drain7 as evidence-of-discipline-mint in its mechanical-evidence section.

## §10 — Cross-references

- Parent initiative: I86 cluster execution coordinator (`docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md`).
- Parent OPS row: `OPS-86-21` (drain7 cursor-rule × skill pairing audit + mint).
- Parent decision: D-IH-86-CT (to be minted on operator ratification of this proposal).
- Predecessor: Wave R closure UAT at `reports/uat-wave-r-closure-2026-05-24.md` + decision-log Round 5.
- Sister specialty mints: `INDEX_INTEGRITY_DISCIPLINE.md` (most recent quartet mint; Wave N), `INTER_WAVE_REGRESSION_DISCIPLINE.md` (Wave M), `UAT_DISCIPLINE.md` (Wave J).
- Governing rules: `akos-applied-research-discipline.mdc` RULE 2 (external citations) + `akos-inline-ratification.mdc` quality bar + `akos-people-discipline-of-disciplines.mdc` (KB-stewardship is People discipline).
- External research: ACT-R (Anderson), Pattern Language (Alexander), SRE Book (Beyer et al.), SECI model (Nonaka & Takeuchi), Building Effective Agents + Anthropic Skills (Anthropic 2025).

---

*End of drain7 proposal. Operator ratification proceeds in 3 sub-batches via separate `AskQuestion` calls; mint commit lands on full ratification of sub-batches 1 + 2 + 3.*
