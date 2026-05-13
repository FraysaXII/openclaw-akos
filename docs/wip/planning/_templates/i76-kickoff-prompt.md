---
language: en
status: active
authored: 2026-05-13
last_review: 2026-05-13
target_initiative: I76 (candidate)
target_phase: P-1 Strand A external research → C-76-1 ratification → Plan-Author → P0 charter
classification: fact
ssot: false
---

# I76 kickoff — Strand A external research + C-76-1 ratification + Plan-Author + P0 charter (MADEIRA elevation)

> **Copy everything below the `--- BEGIN PROMPT ---` line into a fresh Cursor chat (Plan mode preferred — Strand A is research, not edits).**
>
> **Special posture**: I76 is the only kickoff that has a **mandatory pre-charter research phase (P-1)** because the operator's load-bearing conundrum (C-76-1: AICs framing F1–F5) cannot be ratified without external evidence. **DO NOT skip Strand A.** The operator explicitly asked for outside research before adopting the AICs framing.

## --- BEGIN PROMPT ---

```
Goal: Drive INIT-OPENCLAW_AKOS-76 (MADEIRA elevation) from "candidate" to "active P0 charter
shipped on main", in the same inline-AskQuestion style as the I70 transcript. Strand A external
research is MANDATORY pre-charter; do not skip it.

Read first (in this order; do not skip):
- .cursor/rules/akos-inline-ratification.mdc
- .cursor/rules/akos-planning-traceability.mdc
- .cursor/rules/akos-governance-remediation.mdc
- docs/wip/planning/_candidates/i76-madeira-elevation.md (lift; this is the load-bearing input)
- docs/wip/planning/_templates/initiative-planning-prompts.md (generic prompt trio)

Internal canonicals to read:
- docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/MADEIRA-AKOS/STATUS.md
  (the MADEIRA-AKOS reserved folder + 4 OS-migration triggers + AIC-as-category codification)
- docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md
  section 15.2 (4 OS-migration triggers) and section 16.3 (transition triggers)
- docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md
  section 8 (AKOS-complete-enough trigger gates MADEIRA productization)
- docs/wip/planning/11-madeira-ops-copilot/master-roadmap.md (active stack; scope-overlap audit)
- docs/wip/planning/13-madeira-research-followthrough/master-roadmap.md (active stack)
- docs/wip/planning/17-madeira-cursor-mode-parity/master-roadmap.md (active stack;
  mode parity scope; load-bearing for I76 Strand B)
- DECISION_REGISTER.csv: D-IH-70-V (AIC-as-category framing), D-IH-70-I (brand-jargon hygiene
  strict; constrains MADEIRA's brand-voice; load-bearing for Strand F).

STRAND A — External research (MANDATORY; budget ≥1 hour of focused web research; cite ≥6 sources):

Topic 1 — Multi-agent frameworks landscape (cite ≥3):
- AutoGen (Microsoft) — supervisor + worker pattern; recent 2025/2026 changes via AG2 fork.
- CrewAI — role-based crews; peer-companion pattern.
- LangGraph (LangChain) — stateful agent graphs; tool-call subgraphs as ad-hoc dispatchers.
- Anthropic engineering blog — "Building effective agents" (2024-2025); single-agent + tools
  posture vs multi-agent.
- Microsoft AI agent design patterns — orchestrator + swarm + sequential + concurrent.
- OpenAI Swarm (experimental, 2024) — handoff-based orchestration.

Topic 2 — Companion vs supervisor patterns (cite ≥2):
- "Constitutional AI" (Anthropic, 2022+) — single-agent doctrine.
- Microsoft Research / academic literature on multi-agent LLM systems.
- Cursor's own subagent_types architecture (browse Cursor docs at docs.cursor.com/agents) — the
  reference implementation operator already uses; map its shape onto MADEIRA framings.

Topic 3 — Mode parity benchmarks (Ask / Plan / Agent / Debug; cite ≥2):
- Cursor's mode taxonomy (docs.cursor.com).
- Replit Agent / Aider modes / Continue.dev / Cody.

Topic 4 — Persistence + memory (cite ≥2):
- Anthropic context-window strategies; OpenAI Assistants memory; Letta (formerly MemGPT); A-MEM.

Topic 5 — Tool catalog discipline (cite ≥1):
- Anthropic tool-use best practices; OpenAI function-calling guidance; MCP spec ecosystem.

Topic 6 — Personality / voice (cite ≥1):
- Constitutional AI; Inflection Pi (lessons from deprecation); Character.AI as anti-pattern;
  brand-voice agent literature.

For EACH cited source, the agent records: what it solves, where it fits in MADEIRA, what it does
NOT solve, what license/IP posture it carries.

Output of Strand A: a research report at
docs/wip/planning/_candidates/i76-strand-a-research-<date>.md with:
1. Per-topic synthesis (1-2 paragraphs each).
2. Mapping table: "F1 framing fits if X; F2 fits if Y; F3 fits if Z; F4 fits if W; F5 fits if V".
3. Recommended F-choice with rationale + cited evidence + opposing-evidence acknowledgement.
4. Refined enumeration of conundrums C-76-1 through C-76-7 (some may collapse, some may split).

C-76-1 RATIFICATION (operator AskQuestion, after Strand A report is read):

```
Q: Which AIC framing does MADEIRA adopt? (Strand A research at <path>; recommended:
   <agent-recommended-framing> based on <cited-evidence>)

[F1] Supervised sub-agents (Cursor-style)
[F2] Peer companions (CrewAI-style)
[F3] Ad-hoc dispatchers (LangGraph-style)
[F4] No AICs; single-agent + rich tools
[F5] Hybrid; operator picks per session
```

The verdict becomes D-IH-76-A. Decision_log_path =
docs/wip/planning/_candidates/i76-strand-a-research-<date>.md.

Step 2 — Plan-Author (per generic Prompt 2; ONLY after Strand A + D-IH-76-A landed):
- Author .cursor/plans/i76-madeira-elevation_<8hex>.plan.md
- Author docs/wip/planning/76-madeira-elevation/master-roadmap.md (lift candidate;
  expand per the F-framing winner)
- Author docs/wip/planning/76-madeira-elevation/reports/p0-charter-<date>.md
- git mv the candidate to promoted-candidate-<date>.md (and the Strand A research report
  to docs/wip/planning/76-madeira-elevation/reports/p-1-strand-a-research-<date>.md)

Step 3 — Mint registry rows (one atomic commit):
- DECISION_REGISTER.csv: D-IH-76-A (already minted at Strand A close; verify), D-IH-76-B
  (mode taxonomy), D-IH-76-C (tool catalog + RBAC), D-IH-76-D (persistence shape), D-IH-76-E
  (personality), D-IH-76-F (MADEIRA / I11 / I13 / I17 scope boundary), D-IH-76-G (I74 Strand C
  handoff trigger), plus charter row.
- INITIATIVE_REGISTRY.csv: row INIT-OPENCLAW_AKOS-76 with status=active.
- OPS_REGISTER.csv: rows OPS-76-1 through OPS-76-4, status=open.

Step 4 — Cross-link surfaces:
- WORKSPACE_BLUEPRINT_HOLISTIKA.md section 15.2: link the master-roadmap (TRIGGER-1 +
  TRIGGER-2 cross-references).
- HLK_ERP_ARCHITECTURE.md section 8: cross-link the AKOS-complete-enough trigger to D-IH-76-G.
- MADEIRA-AKOS/STATUS.md: update Scenario A status to reflect I76 active.
- I11 / I13 / I17 master-roadmaps: add cross-link "I76 elevation initiative active; scope
  boundary per D-IH-76-F".
- I74 candidate: update Strand C cross-link to point at D-IH-76-G.
- CHANGELOG.md [Unreleased] / Added: charter entry.

Verification (same suite as I72/I73/I74/I75):
- validate_decision_register, validate_initiative_registry, validate_ops_register, validate_hlk,
  validate_master_roadmap_frontmatter, validate_hlk_vault_links, render_operator_inbox.

Commit messages (TWO atomic commits, in order):
1. "i76 strand a external research report (mandatory pre-charter)"
   - Includes: Strand A research report + D-IH-76-A row.
2. "i76 p0 inline charter + registries + workspace cross-links (madeira elevation; F<X> ratified)"
   - Includes: Cursor plan + master-roadmap + p0-charter report + INIT/OPS rows + cross-links + CHANGELOG.

DECISION DISCIPLINE (binding; this is the load-bearing posture):
- DO NOT skip Strand A. The operator explicitly asked for external research before adopting
  the AICs framing. Skipping would violate the operator instruction logged in this candidate's
  operating story.
- The Strand A report MUST cite ≥6 distinct sources with URLs.
- C-76-1 ratification MUST happen via AskQuestion after the operator has had a chance to read
  the report. If the operator says "I want to think more", the agent waits.
- C-76-5 (MADEIRA / I11 / I13 / I17 scope boundary) MUST be ratified pre-charter; the agent
  cannot promote the candidate without an explicit boundary decision.

OPERATOR NOTES (paste your latest thoughts here; the operator's "I prefer you look outside,
there are lots of people thinking on it" instruction is logged in the candidate operating story):
[paste-here]
```

## --- END PROMPT ---

## Why this kickoff is shaped differently

The other candidates' kickoffs collapse Discovery + Plan-Author into one flow. I76 cannot — the load-bearing conundrum (C-76-1) is **architectural** and the operator explicitly asked for **external evidence before ratification**. So I76 has a **two-commit P0**: first the Strand A research report (with `D-IH-76-A` minted at the end), then the charter tranche (everything else).

This protects against the **Critical risk** in the candidate: premature AICs commitment locks pattern before evidence supports it.

## After P0 ships

P1 (Mode parity at Cursor-grade) is the heaviest phase; cross-coordinates with active I17. P4 (AICs implementation) is **conditional** on the F-framing winner — if F4 wins, P4 is SKIPPED and the master-roadmap is updated to remove it.
