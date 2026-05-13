---
candidate_id: I76
title: MADEIRA elevation — operator-interaction quality at Cursor-grade
status: candidate
authored: 2026-05-13
last_review: 2026-05-13
parent_initiative: 70 (closing scaffold) + I11/I13/I17 (active MADEIRA stack)
priority: 2
language: en
---

# I76 candidate — MADEIRA elevation

> **Candidate scaffold (deepened 2026-05-13).** Promoted to `active` only AFTER (a) external research (Strand A) is complete and the **AIC-as-people framing** is ratified or rejected via inline `AskQuestion`, and (b) the active MADEIRA stack (I11 / I13 / I17) is reviewed for scope-overlap. This is **explicitly framed as discovery-led**: the operator surfaced the AICs idea but asked for outside research first ("don't want to influence you... look outside"). Prompt 1 from [`docs/wip/planning/_templates/initiative-planning-prompts.md`](../_templates/initiative-planning-prompts.md) is the right entry point when promoting.

## 1. Operating story

I70 codified MADEIRA at two levels:

1. **Methodology**: MADEIRA is the **founder method** — the personal research-and-decision discipline that produces v3.x of the Holistika OS. Every `LOGIC_CHANGE_LOG` row, every `D-IH` decision, every founder principle 2.x is a methodology artifact.
2. **Agent shape**: MADEIRA is the **L6 founder-companion AI agent** that today's Cursor-agent interactions empirically embody (per [`D-IH-70-V`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) — AIC-as-category framing). When the operator opens Cursor and chats with an agent, that interaction is, in operational terms, the operator interfacing with their own method through a generic agent runtime.

The gap I76 closes: **the operator's interaction with MADEIRA today is fragmented across three active initiatives** ([I11](../11-madeira-ops-copilot/), [I13](../13-madeira-research-followthrough/), [I17](../17-madeira-cursor-mode-parity/)) **but lacks the polish of Cursor itself as an interaction surface**. The operator's quote: *"this is a huge win to bring my interaction with MADEIRA to be like the one I have with Cursor."* So: bring the **shape of how MADEIRA operates and feels** up to a bar where it's a tool the operator reaches for **deliberately** — not a default agent runtime that incidentally implements the method.

The strategic angle the operator surfaced: *"we can strategically have a win there if we craft correctly."* This points at productization — the [I74](i74-brand-tooling-productization.md) Strand C (`@holistika/madeira-agent`) becomes credible only after MADEIRA's operator-interaction is polished. So I76 is the **prerequisite** to I74 Strand C, even though I74 is a candidate today (TRIGGER-2 dormant). I76 builds the asset; I74 packages it when the trigger fires.

The cohering principle: **MADEIRA is a method that runs on an agent runtime; bring the runtime fit to method-grade**. Today's Cursor-as-runtime is generic; MADEIRA-the-method is specific. The fit is structural mismatch. I76 closes the mismatch by making MADEIRA's operating posture (rules, hooks, skills, MCPs, sub-agents-or-not, mode parity, tool catalog, persistence) explicitly designed for the method, not borrowed from a generic agent's defaults.

## 2. The "MADEIRA has people" question (operator-surfaced; deliberately unanswered here)

The operator's framing: *"MADEIRA needs to have people right? We can [call] them AICs."*

This is the **load-bearing architectural conundrum** of I76. There are at least four defensible answers from the broader agentic-AI community, and I am **deliberately not pre-committing to one** because the operator explicitly asked for outside research first. Strand A below scopes the research; Strand C surfaces the conundrum to inline-ratify after the research lands.

The four candidate framings (placeholder enumeration, to be refined by Strand A):

| Framing | One-line shape | Industry analogue (to be cited via Strand A) |
|:---|:---|:---|
| **F1 — AICs as supervised sub-agents** | MADEIRA is a supervisor agent; AICs are specialized workers (one per discipline / persona / tool family) that MADEIRA dispatches. | Cursor's `subagent_types` (explore, browser-use, render-assistant…); Anthropic's "research" agents pattern. |
| **F2 — AICs as peer companions** | MADEIRA + AICs are peers in a multi-agent group; the operator interacts with whichever fits the moment. No supervisor. | CrewAI's role-based crews; AutoGen's group-chat pattern. |
| **F3 — AICs as ad-hoc dispatchers** | MADEIRA is the only persistent agent. "AIC" is the verb (dispatch a sub-task) not the noun (a being). | LangGraph's tool-call subgraphs; OpenAI Assistants tool-orchestration. |
| **F4 — No AICs; MADEIRA is solo with rich tools** | MADEIRA is a single agent with a deep tool catalog. The team-shape is a leaky metaphor. | Single-agent ReAct loops; Anthropic's "Claude Code" architecture (single agent + tools). |

**The conundrum is genuine.** The operator's framing has rhetorical and brand power (a "team of AICs" is a story people remember). The structural choice has multi-quarter consequences (data model, tool RBAC, persistence shape, orchestration runtime, cost). The wrong choice locked in a productizable pattern (I74 Strand C) that won't ship. Strand A → Strand C is the path to ratifying.

## 3. Strands

### Strand A — External research (must complete BEFORE planning)

| Topic | Why it matters | Suggested external sources (Strand A agent picks) |
|:---|:---|:---|
| Multi-agent frameworks landscape | Shape the F1–F4 ratification | AutoGen (Microsoft), CrewAI, LangGraph (LangChain), AG2 (formerly AutoGen2), Swarm (OpenAI experimental). |
| Companion vs supervisor patterns | Architectural lineage of "MADEIRA + AICs" | Anthropic engineering blog on "Building effective agents"; Microsoft AI agent design patterns (orchestrator + swarm + sequential). |
| Mode parity benchmarks (Ask / Plan / Agent / Debug) | I17 already scoped; bring it to Cursor's bar | Cursor's mode taxonomy; Replit Agent; Aider modes; Continue.dev. |
| Tool catalog discipline | Strand E scope | Anthropic's "tool use best practices"; OpenAI function-calling guidance; MCP spec ecosystem. |
| Persistence + memory | Strand F scope | Anthropic context-window strategies; OpenAI Assistants memory; Letta (formerly MemGPT); A-MEM framework. |
| Inline-ratify (operator-in-the-loop) | I70 already lives this; verify outside | Anthropic "human-in-the-loop"; LangChain interrupts; Cursor's `AskQuestion` tool. |
| Personality / voice for an agent | Brand voice + neutrality vs persona | "Constitutional AI" (Anthropic); Character.AI; Inflection's Pi (deprecated); brand-voice agent literature. |

Strand A does **not** make architectural commitments. It produces a discovery report (Prompt 1 output) with cited patterns + a refined enumeration of conundrums.

### Strand B — MADEIRA mode parity at Cursor-grade

Coordinates with [I17](../17-madeira-cursor-modes-as-akos-modes/) (already active) but pushes further:

- **Ask mode**: read-only research with grep / read / web search; no writes; no tool calls beyond observation.
- **Plan mode**: Cursor-plan authoring with inline `AskQuestion`; no commits; can write `.cursor/plans/*` files.
- **Agent mode**: full tool access (write, shell, MCPs, subagents — if F1/F3 ratified); commits per atomic-phase discipline.
- **Debug mode**: structured troubleshooting; runtime evidence gathering; explicit hypothesis ladders (Cursor has this; MADEIRA can too).
- **(NEW) Methodology mode**: a MADEIRA-specific mode where the agent treats every interaction as a methodology checkpoint — `LOGIC_CHANGE_LOG` candidate, decision-register candidate, brand-voice register check. This is the MADEIRA delta over generic Cursor modes.

### Strand C — AICs ratification (inline-ratify after Strand A)

The output of Strand A feeds an `AskQuestion` round:

```
Q: Which AIC framing does MADEIRA adopt?
[F1] Supervised sub-agents (Cursor-style) — recommended IF Strand A finds strong precedent
     for supervisor + worker shapes in our scale class.
[F2] Peer companions (CrewAI-style) — recommended IF Strand A finds the operator's
     "team" rhetoric maps better to peer dynamics than supervisor dynamics.
[F3] Ad-hoc dispatchers (LangGraph-style) — recommended IF Strand A finds that
     specialization pays off only at higher scale than today's engagements.
[F4] No AICs (single-agent rich-tools) — recommended IF Strand A finds that the team
     metaphor is a productization story, not an architectural one.
[F5] Hybrid — defer F-choice to a per-task setting (operator picks per session).
```

Whichever wins becomes `D-IH-76-A` (architectural). The decision is **load-bearing for I74 Strand C** — if F1/F3 wins, `@holistika/madeira-agent` ships as orchestrator; if F2 wins, it ships as a crew library; if F4 wins, it ships as a single-agent + rich-tools package.

### Strand D — Inline-ratify integration (MADEIRA-specific)

The [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) rule already binds **all** Cursor sessions in this repo. Strand D makes MADEIRA the **canonical reference implementation**: every MADEIRA session uses `AskQuestion` at architectural decision gates; never writes `OPERATOR PAUSE POINT`; the rule's worked example (today: I70 P8 §8.7 GOI hunt) gets extended with a MADEIRA-specific case.

### Strand E — Tool catalog standardization

- Authoritative list of tools MADEIRA can call (`Read`, `Edit`, `Shell`, validators, MCPs, etc.).
- RBAC per mode (Ask = read-only; Plan = read + plan-files; Agent = full; Debug = read + observability).
- Audit log: every MADEIRA session emits a structured trace consumable by Langfuse (per [I71](../71-cicd-discipline-and-aiops-baseline-maturity/) Strand B).
- Out-of-scope tools: explicit deny-list (no auto-publish to PyPI / no GitHub release without operator ratification / etc.).

### Strand F — Operator UX

- Keyboard shortcuts / palette / persistence policy.
- Multi-tenancy: do MADEIRA sessions across operators share state, or is each session ephemeral? Today: ephemeral (Cursor default). Strand F asks if the method warrants persistence.
- Personality / voice: Strand A informs whether MADEIRA has a persona (operator's voice? a neutral assistant? a named character?).
- Brand-jargon hygiene: per [`D-IH-70-I`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv), MADEIRA must not leak `AKOS` / `topic_*` / `kirbe.*` etc. into customer-facing prose. UI/UX gates on this.

## 4. Phase scaffold

| Phase | Strand | Scope | Closes |
|:---|:---:|:---|:---:|
| **P-1** (pre-charter) | A | External research; discovery report; refined conundrum enumeration | — |
| **P0** | C+D | Charter + AICs ratification (`D-IH-76-A`) + INITIATIVE / OPS rows + WORKSPACE cross-link | — |
| **P1** | B | Mode parity P0 cut: Ask + Plan + Agent + Debug + Methodology mode definitions | OPS-76-1 |
| **P2** | E | Tool catalog standardization + per-mode RBAC + Langfuse trace shape | OPS-76-2 |
| **P3** | F | Operator UX + persistence policy + personality ratification + brand-jargon gates | OPS-76-3 |
| **P4** | C | AICs implementation (architecture per `D-IH-76-A`); only if F1/F2/F3/F5 wins; SKIPPED if F4 | OPS-76-4 |
| **P5** | — | First operator UAT cohort: 5 real engagements use MADEIRA at the new bar; collect drift signals | — |
| **P6** | — | Closing UAT + INITIATIVE_REGISTRY closure + handoff to I74 Strand C if productization triggers | — |

## 5. Conundrums (open at candidate stage; some pre-charter, some pre-execution)

1. **C-76-1 — AICs framing F1/F2/F3/F4/F5** (Strand C, post-Strand-A research). Charter-blocking. Pre-charter ratification.
2. **C-76-2 — Methodology mode as a real mode vs as an Ask-mode preset**: introducing a 5th mode raises cognitive load; a preset is lighter. Default = real mode IF it carries unique tool affordances; preset otherwise. Ratify at P1 inline-ratify gate.
3. **C-76-3 — Persistence shape**: ephemeral (Cursor default) vs session-scoped (Cursor + recent chats) vs methodology-scoped (MADEIRA carries `LOGIC_CHANGE_LOG` awareness across sessions). Default = methodology-scoped read-only (MADEIRA can read recent decisions, but doesn't write across sessions without explicit ratification). Ratify at P3 inline-ratify gate.
4. **C-76-4 — Personality / persona**: neutral assistant vs operator-voice mirror vs named character. Default = neutral with explicit operator-voice mirror under a flag (per Strand A research findings). Ratify at P3 inline-ratify gate.
5. **C-76-5 — MADEIRA scope vs I11/I13/I17 scope**: does I76 supersede them, extend them, or run parallel? Default = run parallel (I76 is the elevation layer; I11/I13/I17 are the substrate). Ratify pre-charter.
6. **C-76-6 — Productization split with I74 Strand C**: when does I76 hand off to I74 Strand C? Default = AKOS-complete-enough trigger (per [`HLK_ERP_ARCHITECTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md) §8). Ratify pre-charter.
7. **C-76-7 — Brand-voice for MADEIRA**: does MADEIRA write in `BRAND_VOICE_FOUNDATION.md`'s register, or in Cursor's neutral register, or operator-voice? Default = brand-voice register; per `D-IH-70-I` strict mode applies. Ratify at P3.

## 6. Decision preview (D-IH-76-* rows likely to mint)

- **D-IH-76-A** — AICs framing ratification (F1 / F2 / F3 / F4 / F5). Architectural. Pre-charter. Load-bearing for I74 Strand C.
- **D-IH-76-B** — Mode taxonomy (4 modes vs 5; Methodology mode shape). Pre-execution.
- **D-IH-76-C** — Tool catalog + per-mode RBAC architecture.
- **D-IH-76-D** — Persistence shape (ephemeral / session / methodology).
- **D-IH-76-E** — Personality ratification.
- **D-IH-76-F** — MADEIRA / I11 / I13 / I17 scope boundary.
- **D-IH-76-G** — I74 Strand C handoff trigger (productization gate).
- **D-IH-76-CLOSURE** — initiative closure.

## 7. Spin-out trigger conditions

- I71 P0 charter — **MET** 2026-05-13.
- I71 P1–P2 (validator packs A1–A3) — **PENDING** (MADEIRA's brand-voice gate depends on Pack A1).
- External research compiled (Strand A discovery report) — **PENDING**.
- Operator ratifies F-framing for AICs (`D-IH-76-A`) — **PENDING** (load-bearing).
- Active MADEIRA stack (I11 / I13 / I17) reviewed for scope overlap — **PENDING**.

## 8. Risk register (top 5)

| Risk | Severity | Mitigation |
|:---|:---:|:---|
| Premature AICs commitment locks pattern before external evidence supports it | Critical | Strand A is mandatory pre-charter; the AICs conundrum lands at C-76-1 with explicit "no default" until research lands. |
| MADEIRA personality conflict with brand voice | High | Strand F + C-76-4 inline-ratify; brand-jargon validator (I71 Pack A1) enforces hygiene at every MADEIRA-authored artifact. |
| Productization speculation drives architecture (I74 Strand C tail wags I76 dog) | High | C-76-6 explicit gate criteria; I76 ships the asset, I74 packages later; D-IH-76-G ratifies the handoff trigger. |
| Tool RBAC creep (MADEIRA gets too many tools too fast) | Medium | Strand E explicit deny-list + per-mode RBAC; auditor-readable Langfuse trace per session (Strand B of I71). |
| Persistence violates `D-IH-70-I` brand-jargon hygiene OR `D-IH-71-E` review-stamp dimension | Medium | C-76-3 default is methodology-scoped read-only; brand-jargon validator + review-stamp validator both gate persistent state. |

## 9. Dependencies

- **Hard dependencies (must be MET before I76 P0)**:
  - I71 P0 charter (MET).
  - I70 closing (MET).
- **Soft dependencies (nice-to-have; influence Strand C ratification)**:
  - I71 P1–P2 (validator packs A1–A3) — MADEIRA's brand-voice gates depend on Pack A1; multilingual gate depends on Pack A3.
  - I71 P4 (review-stamp dimension) — MADEIRA's persistence shape (C-76-3) cross-links the review-stamp schema.
  - I72 P2 (engagement-template promotion machine) — MADEIRA's "Methodology mode" produces engagement-template candidates.

## 10. Cross-references

- [`D-IH-70-V`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) — AIC-as-category framing; MADEIRA was originally conceived as the L6 founder-companion AI agent that today's Cursor-agent interactions empirically embody.
- [`MADEIRA-AKOS/STATUS.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/MADEIRA-AKOS/STATUS.md) — reserved folder + 4 OS-migration triggers + AIC-as-category codification.
- [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §15.2 — 4 OS-migration triggers (TRIGGER-1 through TRIGGER-4).
- [`HLK_ERP_ARCHITECTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md) §8 — AKOS-complete-enough trigger gates MADEIRA productization.
- [I11 master-roadmap](../11-madeira-ops-copilot/master-roadmap.md) — Madeira day-to-day ops copilot (active).
- [I13 master-roadmap](../13-madeira-research-followthrough/master-roadmap.md) — MADEIRA research follow-through (active).
- [I17 master-roadmap](../17-madeira-cursor-mode-parity/master-roadmap.md) — MADEIRA Cursor mode parity (Ask / Plan / Run; active).
- [I71 master-roadmap](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md) — validator packs + AIOps baseline + release taxonomy + review-stamp dimension; soft dependency.
- [I74 candidate](i74-brand-tooling-productization.md) Strand C — `@holistika/madeira-agent` productization downstream of I76.
- [`docs/wip/planning/_templates/initiative-planning-prompts.md`](../_templates/initiative-planning-prompts.md) — the right entry point for the agent that promotes this candidate.
- [`.cursor/rules/akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) — the discipline MADEIRA itself canonicalizes.
- [`.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md`](../../../../.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md) — the gold-standard plan shape; I76 plan should match it.

## 11. Out of scope (this candidate; punt to follow-on initiatives if they surface)

- Production deployment of a hosted MADEIRA service (consumer SaaS) — that's TRIGGER-2 territory (I74 Strand C).
- LLM model selection ratification (which provider / which model serves MADEIRA at runtime) — that's a runtime concern; covered by `config/openclaw.json` and the akos `model_catalog.py`.
- Multi-operator collaboration (MADEIRA serving ≥2 operators at once) — TRIGGER-3 territory (multi-tenant fork; not yet scoped).
- Voice / video / mobile interfaces — orthogonal; reactive trigger.
