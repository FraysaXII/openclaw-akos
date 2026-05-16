---
language: en
status: active
authored: 2026-05-15
last_review: 2026-05-15
role_owner: PMO
classification: fact
ssot: true
supersedes:
  - docs/wip/planning/_templates/initiative-planning-prompts.md
  - docs/wip/planning/_templates/i71-kickoff-prompt.md
  - docs/wip/planning/_templates/i72-kickoff-prompt.md
  - docs/wip/planning/_templates/i73-kickoff-prompt.md
  - docs/wip/planning/_templates/i74-kickoff-prompt.md
  - docs/wip/planning/_templates/i75-kickoff-prompt.md
  - docs/wip/planning/_templates/i76-kickoff-prompt.md
---

# Planning compendium — the SSOT for initiative discipline

> **What this file is.** The **single source of truth** for how Holistika initiatives are discovered, planned, ratified, and executed inside Cursor. It collapses the previous trio of generic prompts (`initiative-planning-prompts.md`) + the six per-initiative kickoff templates (`i71..i76-kickoff-prompt.md`) into one read-once, point-back artefact.
>
> **Why one file.** The trio + per-initiative files drifted out of sync: the generic trio taught a discipline the per-initiative files did not enforce; the per-initiative files inherited gaps (one-liner todos, thin mermaid coverage, shallow conundrums, no self-critique gate). One compendium with a per-initiative appendix that points at canonical files instead of re-encoding their content removes the drift surface.
>
> **How to use it.** Read this file end-to-end before authoring any plan or kicking off any initiative session. Paste-ready entry point is [`UNIVERSAL_KICKSTART.md`](UNIVERSAL_KICKSTART.md). Cross-initiative dependencies live in [`INITIATIVE_DEPENDENCIES.md`](INITIATIVE_DEPENDENCIES.md).
>
> **Authority.** Operationalises four always-applied Cursor rules:
>
> - [`.cursor/rules/akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) — plan-quality bar (12 enforced rows + self-critique gate), file-changes CSV, master-roadmap mirror discipline.
> - [`.cursor/rules/akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) — never write `OPERATOR PAUSE POINT`; surface options inline via `AskQuestion`.
> - [`.cursor/rules/akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) — phase + commit discipline; SCOPE / PREREQUISITES / DELIVERABLES / VERIFICATION shape; HLK asset class.
> - [`.cursor/rules/akos-agent-checkpoint-discipline.mdc`](../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) — operator pause points (rare; hard gates only) + agent self-checkpoints (voluntary discipline).

---

## §1. How to use this file

### §1.1 Three entry surfaces

| Surface | Purpose | When to use |
|:---|:---|:---|
| [`UNIVERSAL_KICKSTART.md`](UNIVERSAL_KICKSTART.md) | The paste-snippet for a fresh agent chat. ~120 lines. Routes the agent into the right mode (fresh / gated_operator activation / mid-execution / TRIGGER-watch) and tells it to read this compendium end-to-end. | Every time you open a new Cursor chat for an initiative. |
| `PLANNING_COMPENDIUM.md` (this file) | The full discipline. ~1500 lines. Sections §2–§10 are the *rules*; §11 is the *per-initiative appendix* (each active or candidate initiative gets a one-section pointer at canonicals). | Agent reads end-to-end at session start. Operator reads end-to-end once and then references sections by anchor. |
| [`INITIATIVE_DEPENDENCIES.md`](INITIATIVE_DEPENDENCIES.md) | The dep map. Mermaid graph of I59..I78 + blocker table + cross-strand linkages. | Agent reads in parallel with this compendium. Operator skims when promoting a candidate or unblocking a hold-gate. |

### §1.2 Mode routing (where the agent reads what)

| Mode | Trigger | Agent reads | Agent does |
|:---|:---|:---|:---|
| **fresh** | Operator says "let's plan a new initiative" with a loose idea. | This compendium §2..§10 + §11 (only the relevant candidate sub-section) + [`INITIATIVE_DEPENDENCIES.md`](INITIATIVE_DEPENDENCIES.md). | Discovery pipeline (§3) → Plan-author pipeline (§4) → Pre-flight pipeline (§5). |
| **gated_operator** | The candidate exists in [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) with `status: gated_operator` and the operator says "activate". | This compendium + [`INITIATIVE_DEPENDENCIES.md`](INITIATIVE_DEPENDENCIES.md) + the candidate scaffold under `docs/wip/planning/_candidates/`. | Confirm hold-gates met via §1.3 checklist → run Discovery skipping operator-context capture (use candidate's existing story) → Plan-author → Pre-flight. |
| **mid-execution** | Operator says "continue I7N P3" or similar. | This compendium §6 (inline-ratify) + §8 (per-phase template) + the initiative's `master-roadmap.md` + the Cursor plan. | Self-checkpoint (`reports/checkpoints/sc-pre-p<N>-<date>.md`) → execute phase → ONE atomic commit → inline-ratify gate before next phase. |
| **TRIGGER-watch** | Candidate is `gated_external` or `TRIGGER-watch` (e.g. I74 waiting on ≥2 external requests; I78 waiting on ≥2 regex-pushback signals). | This compendium §11 (the candidate's appendix sub-section). | No-op unless the trigger has fired. If asked to plan anyway, surface an `AskQuestion` confirming operator override. |

### §1.3 Hold-gate quick-check (before starting a new phase)

Before any phase commit, the agent confirms:

1. **Prior phase landed clean.** `git log --oneline -1` shows the prior phase commit; `master-roadmap.md` reflects the new commit SHA.
2. **Validators green for what changed.** Per [`config/verification-profiles.json`](../../../../config/verification-profiles.json) `pre_commit` profile, or the discrete commands in [`docs/DEVELOPER_CHECKLIST.md`](../../../DEVELOPER_CHECKLIST.md).
3. **No open architectural conundrums for the phase about to start.** Every entry in the plan's Conundrums section is either ratified (D-IH-7N-* row exists) or tagged "execution-time inline-ratify gate at §X.Y".
4. **Operator alignment.** A fresh `AskQuestion` (or a recent operator message in-chat) confirms green light for the next phase.

If any of (1–4) fail, the agent does NOT start the next phase; it surfaces the gap inline.

### §1.4 What this file is NOT

- It is **not** an alternative to the canonical files it points at. Per-initiative content lives under `docs/wip/planning/<NN-slug>/master-roadmap.md` + `.cursor/plans/<slug>_<8hex>.plan.md`. This compendium is the *discipline*, not the *content*.
- It is **not** a per-phase runbook. Phase execution is governed by the initiative's plan body + the always-applied Cursor rules. This compendium tells you how to *author* that plan body.
- It is **not** a substitute for the always-applied Cursor rules. The rules in `.cursor/rules/akos-*.mdc` load automatically on every Cursor session. This compendium operationalises them; it does not replace them.

---

## §2. The plan-quality bar — the 12 enforced rows + self-critique gate

> **Authority.** Codifies [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"Plan-quality bar (I66 / I68 precedent; mandatory for execution-grade Cursor plans)" — extended at this compendium revision with two additional rows (#11 self-critique gate, #12 CHANGELOG `[Unreleased]` entry) that I66/I70/I72 demonstrated were load-bearing but were not previously codified.
>
> **When this bar applies.** Plans with **≥ 5 phases**, **≥ 1 calendar week**, any canonical-CSV touch, any multi-repo (`bless_external_repo.py`-tracked) sibling-repo PRs, or any plan revision (Round-N pattern). Plans below this bar (1-3 phase quick fixes, single-file refactors, `99-proposals/` ad-hoc) are exempt; the basic Governance Content Requirements in `akos-planning-traceability.mdc` are sufficient for them.

### §2.1 The 12 rows (each must PASS for the plan to ship)

| # | Row | What | Why | Example link |
|:---:|:---|:---|:---|:---|
| 1 | **Multi-sentence YAML todos** | Frontmatter `todos:` entries are 3+ sentences each, declaring per phase: scope (1-2 sentences), files-to-create / files-to-modify (named with full paths), validators-to-mint (Pydantic model path + script path + test path), pause-point classification (`PAUSE POINT #N` or `none`), self-checkpoint count. Each todo has a stable `id` matching the phase header. | One-liner todos (`"P3 — author the SOP"`) hide the deliverable count, file paths, and validator obligations. The agent reading the plan later cannot tell whether the phase is half-done. | I66 plan frontmatter at [`~/.cursor/plans/brand_vision_ops_sweep_4f4c51dd.plan.md`](file:///~/.cursor/plans/brand_vision_ops_sweep_4f4c51dd.plan.md); I70 frontmatter at [`~/.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md`](file:///~/.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md). |
| 2 | **Three mermaid diagrams** | Architecture mermaid (system being designed) + module / sub-component mermaid (when ≥ 4 sub-components) + phase-dependency mermaid (execution sequence with explicit parallelism + gating). | One diagram cannot carry architecture + execution order simultaneously. The reader needs both. | I66 plan §§"Branded House tree" + "Module overview" + "Phase dependency"; I68 Round 2 plan same shape. |
| 3 | **Per-phase deep sections** | Every phase header `## P<N> — <name> (<effort>d; PAUSE POINT #M if applicable)` carries SCOPE / PREREQUISITES / DELIVERABLES / VERIFICATION + pause-point class + self-checkpoint count + cursor-rules adherence. | Without explicit scope-not-in-scope, phase boundaries drift mid-execution. Without explicit verification, "done" is whatever the agent says. | I70 plan P0 through P11 sections; I72 master-roadmap §"Phase-by-phase deep section". |
| 4 | **Inline decision-log preview table** | A table of every D-IH-7N-* decision the plan will mint: ID / question / owner / status / close-out phase. NEW/DROPPED markers on revisions. | The full register lives in the initiative's `decision-log.md`; the inline preview is for readers who skim the plan body. | I66 plan §"P0 — Charter" D-IH-66-A..T; I68 Round 2 §"Decisions (preview)" with NEW markers on D-IH-68-K + D-IH-68-L. |
| 5 | **Inline risk-register preview table** | A table of every R-IH-7N-N risk: ID / risk / likelihood / impact / mitigation. NEW/DROPPED markers on revisions. | Same logic as #4. The full register is in `risk-register.md`; the inline preview keeps the plan self-contained. | I66 plan §"P0" R1-R10; I68 Round 2 §"Risks" R-IH-68-1..12. |
| 6 | **Round-expansions narrative on revisions** | When a plan is revised in response to operator feedback, the new top of the body contains `## What changed since <prior-version>` organised as `### Round N` sub-blocks naming what changed and why per round. Each round paragraph cites operator-supplied evidence. | Plan history must be auditable without diffing the file. The Round-N narrative is the audit log. | I66 plan §"What expanded from the prior plan" (Round 1 + 2 + 3); I68 Round 2 §"What changed since the I68 charter"; I72 plan Round 4-8 amendment narrative. |
| 7 | **Clickable file paths on first mention** | Every commit, file, validator, route, mirror, view, template, and SOP referenced in the plan carries a clickable markdown link to its full repo path on first mention. Subsequent mentions may use bare backticks. | A plan that lists "Mint `validate_<X>.py`" without linking the script path fails the bar. Operator review should not need to flip to other docs to verify the validator's compliance. | I66 plan — every validator + canonical link is clickable; I70 plan same. |
| 8 | **CONTRIBUTING.md callouts on new validators** | Every plan that mints new Python validators notes inline that they follow [`CONTRIBUTING.md`](../../../../CONTRIBUTING.md) §"Python Code Standards": Pydantic models in `akos/<module>.py`, type hints, structured logging via `akos.log.setup_logging`, `akos.process.run` for subprocess, `pathlib.Path`, tests in `tests/test_<module>.py` with valid + invalid input pairs, wired into [`scripts/release-gate.py`](../../../../scripts/release-gate.py) + [`config/verification-profiles.json`](../../../../config/verification-profiles.json). | These callouts go inline in the per-phase **Files** sub-section that introduces the validator, not as a generic appendix — operator review should not need to flip to `CONTRIBUTING.md` to verify a validator's compliance. | I66 plan validators (`validate_brand_baseline_reality_drift.py`); I68 plan (`validate_cicd_baseline.py`); I72 plan (`validate_adapter_registries.py` + `validate_process_list_pairing.py`). |
| 9 | **≥4 external research sources** | Every plan cites at least 4 external sources with: name, URL, year, IP/license, maturity, adoption, relevance, what we adopt vs what we reject. Banned: uncited "industry best practice" claims. Preferred citation order: open-source canonicals → industry consensus → vendor docs → academic. | "Industry consensus" without citation is not consensus; it is assertion. The plan must show its work. | I66 plan §"External pattern catalog" (4 sources on brand architecture); I72 plan §"External pattern catalog" (Truto + Unified.to + Apideck on adapter pattern); I68 plan §"External research" on CICD baselines. |
| 10 | **Conundrum index with rationale + cited evidence + recommended default** | Every architectural fork is recorded as a conundrum (C-7N-1..C-7N-K) with: question, 2-4 ranked options, rationale per option, cited evidence per option (internal file path or external URL), recommended default with explicit reasoning, ratification timing (planning-time vs execution-time inline-ratify gate). | Conundrums without rationale + cited evidence force the operator to do the research themselves. That defeats the purpose of the discovery pipeline. | I70 plan conundrum index C-70-1..C-70-25; I72 plan §"Conundrums" Round 4-8 expansions. |
| 11 | **Self-critique gate** | Before declaring the plan "ready for operator ratification", the authoring agent runs this 12-row checklist against its own draft and reports per-row PASS / FAIL with the row's evidence (line numbers, anchor links). If any row FAILs, the agent revises and re-runs. | A plan that ships without a self-critique gate inherits the gaps the prior trio templates had: one-liner todos, missing mermaid, shallow conundrums. The gate is the forcing function. | NEW in this compendium revision (2026-05-15). I72 demonstrated the cost of skipping it (Round 4-R-A amendment retroactively added the cursor-rule hardening rows). |
| 12 | **CHANGELOG `[Unreleased]` entry** | Every plan-commit (P0 charter + every phase commit) carries a `[Unreleased]` line in [`CHANGELOG.md`](../../../../CHANGELOG.md) using imperative mood, naming the decision IDs minted, the validators minted, the canonical CSVs touched. | Without a CHANGELOG entry, the release-taxonomy (per SOP-RELEASE_TAXONOMY_001 from I71 P3) cannot classify the commit into a release row. | NEW in this compendium revision. I71 P3 made this a SOP; this row promotes it from SOP to plan-quality gate. |

### §2.2 The self-critique gate — how to run it

After authoring the plan draft, the agent runs this exact loop in-chat:

```
Self-critique against PLANNING_COMPENDIUM.md §2:

Row 1 (multi-sentence todos): PASS / FAIL — <evidence: frontmatter line range>
Row 2 (three mermaid diagrams): PASS / FAIL — <evidence: anchor names>
Row 3 (per-phase deep sections): PASS / FAIL — <evidence: phase header count + SCOPE/PREREQS/DELIVERABLES/VERIFICATION presence>
Row 4 (inline decision-log preview): PASS / FAIL — <evidence: anchor>
Row 5 (inline risk-register preview): PASS / FAIL — <evidence: anchor>
Row 6 (Round-expansions narrative): PASS / N/A (first version) — <evidence: anchor>
Row 7 (clickable file paths): PASS / FAIL — <evidence: spot-check 5 first-mention paths>
Row 8 (CONTRIBUTING.md callouts): PASS / N/A (no new validators) — <evidence: anchor>
Row 9 (≥4 external research sources): PASS / FAIL — <evidence: citation count>
Row 10 (conundrum index with rationale): PASS / FAIL — <evidence: anchor + spot-check on 3 conundrums>
Row 11 (self-critique gate): PASS (you are running it now) — <evidence: this block>
Row 12 (CHANGELOG entry): PASS / FAIL — <evidence: CHANGELOG.md [Unreleased] block diff>
```

If any row is FAIL: revise the plan, re-run the gate. The agent does NOT skip a FAIL by re-classifying it as "out of scope" — out-of-scope rows are N/A (with reason), not FAIL.

### §2.3 The bar is non-negotiable

Operators may waive specific rows in writing (e.g. "Row 8 N/A — no new validators this initiative") but the waiver lives in the plan's decision-log as a D-IH-7N-* row with rationale. Agents may not waive rows unilaterally.

---

## §3. Discovery pipeline (Prompt 1, reworked)

> **What's reworked.** Prior `initiative-planning-prompts.md` Prompt 1 had: candidate read pass, external research (≥3 sources, no IP/license/maturity/adoption fields), conundrum surfacing (no rationale-bearing template), inline questions (batched), discovery report. **This version adds:** operator-context capture (5-7 fields up front), MANDATORY architecture mermaid sketched during discovery (so it gets debated before plan-author starts), conundrum surfacing with the explicit rationale-bearing options template, self-critique gate before shipping the discovery report.

### §3.1 Operator-context capture (the 5-7 fields)

Before any read pass, the agent asks the operator for these fields via `AskQuestion` (one batched call):

1. **Surface change** — what concrete artefact (canonical CSV, SOP, ERP route, sibling-repo file, deck) will be different after this initiative ships?
2. **Problem statement** — what is broken or missing today that this initiative fixes? One sentence.
3. **Success criteria** — what is observable when the initiative is done? Operator-readable, not agent-readable (e.g. "Founder can recruit 3 candidates from the new curriculum without manual onboarding", not "validate_*.py returns 0").
4. **Blast radius** — what does this touch that other initiatives or external repos depend on? (e.g. "touches `process_list.csv` so I72 P2 has dependencies"; "touches `boilerplate/` so a sibling-repo PR is required").
5. **Time pressure** — is there a deadline (e.g. "before founder hire deadline 2026-06-01") or no calendar pressure?
6. **Operator's loose-thoughts dump** — free-form paste of whatever the operator already has in mind. Most operator-context capture rounds produce 80% of the conundrum index from this field alone.
7. *(Optional)* **External-fact anchor** — if there's a specific external pattern, paper, or vendor doc the operator wants the plan anchored to, name it now.

If the operator answers "I don't know yet" on (1–5), the agent does NOT proceed; it decomposes the unknown into sub-questions until each field has a concrete answer.

### §3.2 Read-pass requirements

After the context capture, the agent runs this read-pass in parallel where possible:

1. **Candidate scaffold** (if exists) — `docs/wip/planning/_candidates/i7N-<slug>.md`. Read end-to-end.
2. **[`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv)** — confirm whether an INIT row exists; check `status` (active / gated_operator / candidate / closed / archived); check `gated_on` for hold-gate language.
3. **Related initiatives' `master-roadmap.md`** — pull the dependency map from [`INITIATIVE_DEPENDENCIES.md`](INITIATIVE_DEPENDENCIES.md); read the blocking + blocked-by initiatives' roadmaps.
4. **[`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv)** — grep for any D-IH-* row whose summary mentions the topic. This surfaces prior architectural choices the new plan must inherit or supersede.
5. **Sibling Cursor rules** — every `.cursor/rules/akos-*.mdc` rule that applies to the touched surfaces (Supabase = `akos-holistika-operations.mdc`; trademark filings = `akos-planning-traceability.mdc` §"mandatory pause points"; brand prose = `akos-brand-baseline-reality.mdc`; adapter registries = `akos-executable-process-catalog.mdc`).
6. **Canonical files in scope** — `baseline_organisation.csv` if role changes; `process_list.csv` if process changes; `PRECEDENCE.md` if compliance asset class is touched; `BRAND_*` canonicals if external prose changes; `WORKSPACE_BLUEPRINT_HOLISTIKA.md` if engagement-folder shape changes.
7. **≥4 external research sources** — see §7 for the schema; the agent runs targeted web searches with the 2026 year suffix and cites at minimum 4 distinct sources with URLs.

### §3.3 MANDATORY architecture mermaid sketched during discovery

The agent sketches an **architecture mermaid** (not a phase-dependency mermaid — that comes during plan-author) inside the discovery report. The mermaid shows the system the initiative builds, with nodes for the major artefacts and edges for the relationships.

This mermaid is **mandatory** because it surfaces architectural disagreements before the plan-author phase starts. An operator can look at the mermaid and say "wait, you're putting X under Y but it should be under Z" — and the conundrum becomes explicit. Without the mermaid, that disagreement lurks until plan-author phase, costing a revision round.

Node-ID conventions per §10: camelCase / PascalCase / underscores; no spaces; avoid reserved words (`end`, `graph`, `subgraph`, `flowchart`); quote labels with parens / brackets / colons.

### §3.4 Conundrum surfacing — the rationale-bearing options template

Every architectural choice with 2+ defensible answers is recorded as a conundrum. Template per conundrum:

```
### C-7N-K — <one-sentence question>

**Why this is a conundrum.** <1-2 sentences explaining why both/all answers are defensible — what would push you toward each option.>

**Options:**

| Option | Description | Rationale | Cited evidence | Recommended default |
|:---:|:---|:---|:---|:---:|
| A | <1-line description> | <2-3 sentences why this option works> | <internal file path or external URL> | <X if recommended> |
| B | <1-line description> | <2-3 sentences why this option works> | <internal file path or external URL> | |
| C *(optional)* | … | … | … | |

**Ratification timing.** Planning-time (architectural; not deferrable to execution) OR execution-time inline-ratify gate at §<phase>.<subsection>.

**Decision ID placeholder.** D-IH-7N-K.
```

Conundrums without `Cited evidence` columns are not conundrums — they are guesses. Reject them and re-research.

### §3.5 Inline questions — operator ratification round

The agent surfaces planning-time conundrums via `AskQuestion`, batched up to 6 per call. Each option label carries the rationale snippet + the citation. The agent marks the recommended default with `(recommended …)` suffix.

If the operator answers "I don't know yet" to a conundrum, the agent decomposes the question into sub-options in a follow-up `AskQuestion` call. The agent does NOT proceed past an unresolved planning-time conundrum.

Execution-time conundrums (the ones tagged "inline-ratify gate at §X.Y") are NOT asked at discovery time; they are deferred to execution. But the gate location is pre-allocated in the plan body.

### §3.6 Discovery report (the bridge to plan-author)

The agent authors / updates `docs/wip/planning/_candidates/i7N-<slug>-discovery.md` (or updates the candidate file in place). Sections:

1. **Operating story** (1-2 paragraphs) — what the operator is actually trying to build, in their framing, refined by the agent's clarifying language. This becomes the plan body's "Operating story" anchor.
2. **Operator-context capture** — the 5-7 fields from §3.1 verbatim.
3. **Internal context map** (table: artefact / what it does / how this initiative touches it).
4. **External pattern catalog** (table: pattern / source URL / year / IP-license / maturity / adoption / fit / divergence point / what we adopt vs reject).
5. **Architecture mermaid** (per §3.3) with caption explaining what each node represents.
6. **Conundrum index** (table: ID / question / options / ratified verdict + decision_id placeholder + ratification timing).
7. **Recommended next step**: PROMOTE (ready for plan-author) / REFINE (more discovery needed) / DEFER (operator should park it) / RECONSIDER (operator's framing has a flaw).

### §3.7 Self-critique gate for the discovery report

Before shipping the report, the agent runs:

```
Discovery self-critique:

Operating story: PASS / FAIL — concrete? operator-language? agent-language refinement preserved?
Operator-context capture: PASS / FAIL — all 5-7 fields answered concretely?
Internal context map: PASS / FAIL — every cited file path clickable?
External pattern catalog: PASS / FAIL — ≥4 sources with URL + year + license + maturity + adoption?
Architecture mermaid: PASS / FAIL — node-IDs follow §10 conventions? caption explains nodes?
Conundrum index: PASS / FAIL — every conundrum has 2+ options + rationale + cited evidence + recommended default + ratification timing?
Recommended next step: PROMOTE / REFINE / DEFER / RECONSIDER — with one-sentence justification?
```

If any row FAILs, revise the report; re-run the gate. Then end with a single `AskQuestion` confirming the recommended next step.

---

## §4. Plan-author pipeline (Prompt 2, reworked)

> **What's reworked.** Prior Prompt 2 had: precondition check, output list (A-H), plan structure description, decision discipline, verification before commit. **This version adds:** explicit filename convention (Cursor `.cursor/plans/` slug + workspace mirror), plan-body skeleton with frontmatter shape, the three-mermaid mandate from §10, inline-ratify gate authoring (per §6 + [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc)), self-critique gate per §2.2.

### §4.1 Filename convention

| Surface | Path | Authority |
|:---|:---|:---|
| Cursor plan (SSOT for execution detail) | `~/.cursor/plans/<initiative-slug>_<8hex>.plan.md` (no phase prefix; no strand prefix). The 8-hex suffix is Cursor's auto-generated content hash; you do not pick it. | `akos-planning-traceability.mdc` §"Cursor plans (out-of-repo) and `.cursor/rules` hygiene". |
| Workspace mirror (collaboration surface) | `docs/wip/planning/<NN-slug>/master-roadmap.md` where `NN` is the next two-digit prefix per [`docs/wip/planning/README.md`](../README.md). | `akos-planning-traceability.mdc` §"Traceability Contract". |
| P0 charter ratification record | `docs/wip/planning/<NN-slug>/reports/p0-charter-<YYYY-MM-DD>.md`. | `akos-planning-traceability.mdc` §"UAT evidence contract". |
| Optional repo mirror of Cursor plan | `docs/wip/planning/<NN-slug>/reference/<slug>_<8hex>.plan.md` (collaborator + history surface only). | `akos-planning-traceability.mdc` §"Cursor plans". |

**Anti-pattern (binding).** Never mint phase-scoped or strand-scoped plan files (`i7N_p1_<thing>_<8hex>.plan.md`, `i7N_strand_a_<thing>_<8hex>.plan.md`). The whole initiative lives in ONE file. Heavy execution detail goes IN the file under the phase's section. Depth grows via REGRESSION ROUNDS inside the same file (Round 1 → Round 2 → Round N), not by spawning sibling files. Reference: I72 mid-execution divergence (a phase-scoped plan file was minted by accident; corrected by Round 4 amendment).

### §4.2 Plan-body skeleton

Every Cursor plan has this skeleton (sections in this order):

```
---
name: <initiative title>
overview: <1-paragraph overview, operator-readable>
todos:
  - id: p0-<short-purpose-slug>
    content: "P0 (<effort>d; PAUSE POINT #1 if applicable) — <one-sentence purpose>. (a) <deliverable 1 with file paths>. (b) <deliverable 2 with validator name + module>. (c) <verification rule>. (d) <decision close-outs>. ..."
    status: pending
  - id: p1-...
  - id: p2-...
  ...
isProject: false
---

# <Initiative title>

## What changed since <prior version> (revisions only; see §2 Row 6)

### Round N
<round-N narrative>

## Operating story

<1-2 paragraphs, lifted from discovery report and refined>

## Architecture

<architecture mermaid per §10>

## Module overview (when ≥ 4 sub-components)

<module mermaid per §10>

## Phase dependency

<phase-dependency mermaid per §10>

## Phase status table

| Phase | Title | Status | Commit | Notes |
|:---:|:---|:---:|:---:|:---|
| P0 | <name> | pending | — | charter |
| P1 | <name> | pending | — | <strand> |
...

## Phase-by-phase

### ## P0 — <name> (<effort>d; PAUSE POINT #1 if applicable)

**SCOPE.** <what this phase is and is NOT.>

**PREREQUISITES.** <what must be true before this phase starts; gates + prior phases + canonical-CSV row counts if applicable.>

**DELIVERABLES.**
- <file path 1> — <what it does>.
- <file path 2> — <what it does>.
- <validator: akos/<module>.py + scripts/<name>.py + tests/test_<module>.py> — <what it checks>.

**VERIFICATION.** <commands or vendor-API observable signals.>

**Pause-point class.** canonical-CSV gate / trademark / public-prose / page-spec / standard / none.

**Self-checkpoint count.** <N> per the cadence heuristic in §8.

**Cursor-rules adherence.** <1-line citation per phase; e.g. "akos-deploy-health.mdc §Step 3 operationalised; akos-holistika-operations.mdc two-plane Supabase respected">

### ## P1 — ...
(same shape)

...

## Conundrums (open at planning time + execution-time deferred)

<the C-7N-* index per §3.4>

## Decisions (preview; per §2 Row 4)

| ID | Question | Owner | Status | Close-out phase | NEW? |
|:---|:---|:---:|:---:|:---:|:---:|
| D-IH-7N-A | <q> | <role> | proposed | P0 | NEW |
...

## Risks (preview; per §2 Row 5)

| ID | Risk | Likelihood | Impact | Mitigation | NEW? |
|:---|:---|:---:|:---:|:---|:---:|
| R-IH-7N-1 | <r> | Med | High | <m> | NEW |
...

## External research (per §2 Row 9, §7)

<the ≥4-source citation block with full schema>

## Verification matrix (closing-UAT criteria)

<the per-band UAT acceptance criteria checklist>

## Cross-references

<every cited file / folder / decision / initiative / external URL>

## CHANGELOG entry (preview)

```
### Added
- <decision-id range>: <initiative title> P0 charter — <1-line summary>. (per §2 Row 12)
```
```

### §4.3 Outputs in order (the P0 atomic commit tranche)

A. Cursor plan at `~/.cursor/plans/<slug>_<8hex>.plan.md` (the authoritative SSOT for execution detail).
B. Workspace mirror at `docs/wip/planning/<NN-slug>/master-roadmap.md` (collaboration + git-history surface).
C. P0 charter report at `docs/wip/planning/<NN-slug>/reports/p0-charter-<YYYY-MM-DD>.md` (ratification record).
D. New rows in [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv): D-IH-7N-A (architecture/scope), D-IH-7N-B (sibling/cross-link), D-IH-7N-C (charter ratification), plus any conundrums ratified at planning time.
E. New row in [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) with `status: active` (or `status: gated_operator` if the operator wants P0 ratified but P1+ blocked on an external gate).
F. New rows in [`OPS_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv): one OPS-7N-K per execution strand, with `originating_initiative_id`, `owner_role`, `status: open`, and closure target phase in notes.
G. [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) cross-link entry if the initiative authors a workspace-wide canonical.
H. [`CHANGELOG.md`](../../../../CHANGELOG.md) `[Unreleased]` `### Added` entry per §2 Row 12.
I. Empty `files-modified.csv` at `docs/wip/planning/<NN-slug>/files-modified.csv` per `akos-planning-traceability.mdc` §"Per-initiative file-changes CSV".

ONE atomic commit. Commit message format: `i[7N] p0 inline charter + registries + workspace cross-links`.

### §4.4 Self-critique gate (the §2.2 12-row checklist applied to the plan draft)

Before declaring the plan ready for operator ratification, the agent runs the §2.2 gate verbatim and reports PASS/FAIL per row. FAIL rows are revised; re-run the gate. Then surface the operator-ratification `AskQuestion`.

### §4.5 Inline-ratify gates (per §6)

Every architectural decision the plan defers to execution time is tagged "inline-ratify gate at §<phase>.<subsection>" in the conundrums section. The plan body at that phase pre-allocates the `AskQuestion` shape (which options the gate will surface, what evidence each option needs).

---

## §5. Pre-flight pipeline (Prompt 3, reworked)

> **What's reworked.** Prior Prompt 3 had: P0 landed on main check, validator matrix, no open conundrums check, operator alignment, P1 kickoff. **This version adds:** sequential validator order with stop-on-first-failure, plan-quality audit (§2.2 gate applied to the actual plan file on disk), explicit operator-approval surface.

### §5.1 Sequential validator order

Run these in order; STOP at the first FAIL:

1. **[`scripts/validate_hlk_language_frontmatter.py`](../../../../scripts/validate_hlk_language_frontmatter.py)** — frontmatter `language:` field present on all touched markdown.
2. **[`scripts/validate_hlk_vault_links.py`](../../../../scripts/validate_hlk_vault_links.py)** — cross-vault markdown links resolve.
3. **[`scripts/validate_hlk_km_manifests.py`](../../../../scripts/validate_hlk_km_manifests.py)** — KM Output-1 manifests under `_assets/**/*.manifest.md` (only when touched).
4. **[`scripts/validate_decision_register.py`](../../../../scripts/validate_decision_register.py)** — every D-IH-7N-* row exists; regex shape matches.
5. **[`scripts/validate_initiative_registry.py`](../../../../scripts/validate_initiative_registry.py)** — INIT-OPENCLAW_AKOS-NN row shape; FK to decision-register intact.
6. **[`scripts/validate_ops_register.py`](../../../../scripts/validate_ops_register.py)** — OPS-7N-K row shape; FK to initiative + decision intact.
7. **[`scripts/validate_master_roadmap_frontmatter.py`](../../../../scripts/validate_master_roadmap_frontmatter.py)** — workspace mirror frontmatter shape.
8. **[`scripts/validate_canonical_registry.py`](../../../../scripts/validate_canonical_registry.py)** — every new canonical declared.
9. **[`scripts/validate_compliance_schema_drift.py`](../../../../scripts/validate_compliance_schema_drift.py)** — canonical CSV header drift.
10. **[`scripts/validate_hlk.py`](../../../../scripts/validate_hlk.py)** — the umbrella HLK gate (composes most of the above).
11. **[`scripts/release-gate.py`](../../../../scripts/release-gate.py)** — the strict matrix.
12. **[`scripts/render_operator_inbox.py`](../../../../scripts/render_operator_inbox.py)** — refresh [`OPERATOR_INBOX.md`](../OPERATOR_INBOX.md).

Alternative: run [`config/verification-profiles.json`](../../../../config/verification-profiles.json) `pre_commit` profile via `py scripts/verify.py pre_commit` — composes most of the above with the right order.

### §5.2 Plan-quality audit (§2.2 gate applied to the actual plan file)

After the validator matrix passes, the agent runs the §2.2 self-critique gate against the actual plan file on disk (not against the draft in chat). Every row must PASS or be N/A with reason. If any row is FAIL, the agent goes back to plan-author phase.

### §5.3 Operator approval surface

The agent surfaces a single `AskQuestion`:

> "P0 charter shipped commit `<sha>`. Validator matrix green. Plan-quality §2.2 gate PASS on all 12 rows. Confirm proceed to P1 execution? (yes / pause / re-plan)"

If "yes" → proceed to P1. If "pause" → stop and write a 5-line summary at `docs/wip/planning/<NN-slug>/reports/p0-pre-flight-summary-<date>.md`. If "re-plan" → jump back to §3.

### §5.4 P1 kickoff

- Open the Cursor plan; locate P1 todo; mark `in_progress`.
- File a self-checkpoint at `docs/wip/planning/<NN-slug>/reports/checkpoints/sc-pre-p1-<YYYY-MM-DD>.md` per §8 cadence heuristic.
- Begin execution; ONE atomic commit per phase; `AskQuestion` at every inline-ratify gate per §6.

### §5.5 Stop-on-first-failure (the opt-stop-report posture)

If any validator FAILs in §5.1 or any §2.2 row FAILs in §5.2, the agent writes a 5-line blocker report at `docs/wip/planning/<NN-slug>/reports/p0-pre-flight-blocker-<YYYY-MM-DD>.md` per the opt-stop-report posture in [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) and stops.

---

## §6. Inline-ratify authoring guide

> **Authority.** Operationalises [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc).

### §6.1 When to ask (the three triggers)

- **Evidence-dependent decision** — the agent must run an evidence sweep (Grep / Read / generate artefact) before the operator can ratify. Example: I70 P8 §8.7 GOI class regression hunt — agent ran 6-source sweep, surfaced candidate classes inline.
- **Spot-check / approval gate** — the agent generates an artefact (CSV row, SOP draft, deck slide body) that the operator must confirm looks right. Example: I72 P4 sub-area manager assignments.
- **Architectural fork inside discovery** — the discovery pipeline surfaces a conundrum that needs operator ratification before plan-author starts. This is the §3.5 inline-questions round.

### §6.2 When NOT to ask (use stop-and-clarify instead)

- **Validator failures, broken builds, missing files, security incidents** → opt-stop-report posture. Write `reports/p<N>-blocker-<date>.md` and stop. `AskQuestion` is for **decisions**, not **blockers**.
- **Decisions that change the plan's architecture** (sub-decision ripples back to multiple phases) → emit a STOP-AND-CLARIFY summary, then re-plan.
- **Decisions the operator already ratified during planning** → don't re-ask; consult the conundrum index + decision register first.

### §6.3 Option-label format

Each option in an `AskQuestion` carries:

- **1-line description** of the option.
- **Rationale snippet** (one sentence — why this option works).
- **Cited evidence** (internal file path or external URL).
- **`(recommended …)` suffix** when one option is the agent's recommended default.

Example:

> "Promote curriculum-version anchor to methodology-version anchor (recommended — review-stamp dimension lands at I71 P4 commit `<sha>` which adds `methodology_version_at_review` column; anchoring removes drift surface). Evidence: [`docs/wip/planning/71-.../master-roadmap.md`](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md) §P4."

### §6.4 Batching

One `AskQuestion` per gate, batched. Combine related sub-decisions into a single multi-question call (the tool supports up to 6 questions). Don't fire 6 separate `AskQuestion` calls in sequence — the operator answers one batched call faster than 6 separate calls.

### §6.5 Auto-decision fallback

If the operator doesn't respond within a reasonable window AND the agent has a sensible recommended default, the agent may fall back to the recommended option AND log the auto-decision in the decision register with `decision_source: agent_inline_default`. The fallback window is operator-set; default is 24h of operator silence + clean validators.

### §6.6 The plan-body authoring suffix

Phase headers tag inline-ratify gates explicitly: `## P8 — Engagement registry (inline-ratify gate at §8.7)`. NEVER use the suffix `(OPERATOR PAUSE POINT)`.

---

## §7. External research bar (≥4 sources)

> **Authority.** §2 Row 9.

### §7.1 Per-source schema

Every external source cited in a plan or discovery report carries these fields:

| Field | Description | Example |
|:---|:---|:---|
| Name | Pattern / paper / vendor doc name | "Normalized Adapter Pattern" |
| URL | Stable URL (prefer canonical doc over blog mirror) | `https://truto.one/normalized-adapter-pattern` |
| Year | Publication or last-major-revision year (use 2026 suffix in search queries) | 2026 |
| IP / license | License posture: open-source / closed proprietary / academic / mixed | Open documentation; pattern itself is unpatentable |
| Maturity | Specification stage: experimental / industry-emerging / industry-consensus / standard | Industry-consensus |
| Adoption | Who's using it: 1 vendor / few vendors / broad / standard | Truto + Unified.to + Apideck |
| Relevance | What this initiative adopts from the source (one sentence) | Adapter status enum (active / inactive / planned / deprecated) |
| What we adopt vs reject | Explicit — adopt X, reject Y because Z | Adopt status enum + normalised interface; reject Truto's specific JSON schema in favour of CSV-as-SSOT |

### §7.2 Ban on uncited claims

Phrases banned in plan bodies and discovery reports without a citation:

- "Industry best practice is …"
- "It is widely accepted that …"
- "Most teams use …"
- "Common consensus is …"

Replace with a cited source per §7.1, or remove the claim.

### §7.3 Preferred citation order

When multiple sources cover the same point, cite in this order:

1. **Open-source canonicals** — official protocol docs, governing-body standards (W3C, IETF, ISO, DAMA-DMBOK).
2. **Industry consensus documents** — multi-vendor agreement docs (e.g. OpenTelemetry semantic conventions).
3. **Vendor docs** — Supabase / Vercel / Sentry / Stripe / Truto / OpenAI etc.
4. **Academic** — papers with DOI; prefer cite-tracked papers over arxiv preprints unless preprint is widely cited.

Avoid: vendor marketing pages, founder blog posts (unless the founder is the canonical authority), slide decks (unless the deck is the canonical artefact).

---

## §8. Per-phase deep-section template (the 4-section + metadata pattern)

> **Authority.** §2 Row 3.

### §8.1 Template

```
### ## P<N> — <name> (<effort>d; PAUSE POINT #M if applicable)

**SCOPE.** <what this phase is and is NOT — 2-4 sentences naming the deliverable boundaries.>

**PREREQUISITES.**
- <gate 1: prior-phase commit landed on main>
- <gate 2: hold-gate from INITIATIVE_DEPENDENCIES.md, if any>
- <gate 3: canonical CSV row count baseline — e.g. "process_list.csv has N rows; this phase adds K rows for total N+K">
- <gate 4: operator approval if canonical-CSV-gate or trademark filing>

**DELIVERABLES.**

*Canonical (new + modified):*
- [`<path1>`](path1) — <what it does>.
- [`<path2>`](path2) — <what it does>.

*Mirrored / derived (per consumer-repo):*
- `repo=<slug>: <path>` — <what carries over>.

*Validators (new):*
- Pydantic model: [`akos/<module>.py`](../../../../akos/<module>.py) — model name `<ModelName>`.
- Script: [`scripts/<name>.py`](../../../../scripts/<name>.py) — what it checks.
- Test: [`tests/test_<module>.py`](../../../../tests/test_<module>.py) — valid + invalid input pairs.
- Wired into: [`scripts/release-gate.py`](../../../../scripts/release-gate.py) + [`config/verification-profiles.json`](../../../../config/verification-profiles.json) under profile `<profile_name>`.
- Follows [`CONTRIBUTING.md`](../../../../CONTRIBUTING.md) §"Python Code Standards" (per §2 Row 8).

*Templates (when introducing reusable bless-pattern templates):*
- `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/<template>.tmpl`.

**VERIFICATION.**
- <command 1, e.g. `py scripts/<name>.py` exits 0>
- <command 2, e.g. `py scripts/release-gate.py` PASS>
- <vendor-API observable signal, e.g. "Sentry release `<repo-slug>@<sha>` visible in dashboard within 5 min">
- <UAT row, e.g. "Operator confirms ERP route `/admin/<panel>` renders new column">

**Pause-point class.** canonical-CSV gate / trademark / public-prose / page-spec (I64 v2 precedent) / standard / none.

**Self-checkpoint count.** <N per the cadence heuristic in §8.2.>

**Cursor-rules adherence.**
- `<rule-file.mdc>` §<section> operationalised.
- `<rule-file.mdc>` §<section> respected.
- `<rule-file.mdc>` §<section> preserved.
```

### §8.2 Self-checkpoint cadence heuristic

| Phase scope | Recommended self-checkpoints |
|:---|:---:|
| 1-2 deliverables | 1 (pre-phase) |
| 3-5 deliverables | 2 (pre + mid) |
| 6+ deliverables / mixed-asset-class phase | 3 (pre + mid × 2 + post) |

Self-checkpoints land at `docs/wip/planning/<NN-slug>/reports/checkpoints/sc-<purpose>-<YYYY-MM-DD>.md` per `akos-agent-checkpoint-discipline.mdc` §"Agent self-checkpoint contract".

### §8.3 Pause-point class taxonomy

| Class | When it applies | Required artefact |
|:---|:---|:---|
| **canonical-CSV gate** | Phase commits new or amended rows in `process_list.csv` / `baseline_organisation.csv` / any `compliance/dimensions/*.csv`. | Operator approval **in writing** in `decision-log.md` before commit; `validate_hlk.py` in verification matrix. |
| **trademark** | Phase files or amends a trademark application or surfaces a TM dispute. | Operator approval **in writing**; legal counsel cited; `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_*.md` cross-linked. |
| **public-prose** | Phase publishes external-facing prose (boilerplate / press / decks / dossiers). | `validate_brand_baseline_reality_drift.py` PASS; `validate_brand_jargon.py` PASS; operator UAT row in `reports/uat-*.md`. |
| **page-spec** | Phase commits an ERP page spec or UI route spec (I64 v2 precedent). | Operator approval **on the spec PR**; sibling-repo PR drafted concurrently. |
| **standard** | Default for phases that produce internal artefacts (SOPs, registries, validators) without external surfaces or canonical-CSV touch. | Agent self-checkpoint + atomic commit + validator matrix green. |
| **none** | Phase is purely documentation refactor with no executable change. | Atomic commit + spot-check by operator post-commit. |

---

## §9. Decision-log + risk-register preview format

> **Authority.** §2 Row 4 + §2 Row 5.

### §9.1 Decision-log preview (inline table in plan body)

```
| ID | Question | Owner | Status | Close-out phase | NEW? |
|:---|:---|:---:|:---:|:---:|:---:|
| D-IH-7N-A | Architecture / scope ratification — does the initiative cover surfaces X / Y / Z? | PMO | proposed | P0 | NEW |
| D-IH-7N-B | Sibling-repo cross-link strategy — AKOS-as-SSOT or sibling-as-SSOT for surface W? | System Owner | proposed | P0 | NEW |
| D-IH-7N-C | Charter ratification — operator green-lights the plan as authored. | Founder | proposed | P0 | NEW |
| D-IH-7N-D | Strand A architecture — option A vs B vs C (per conundrum C-7N-1). | <role> | proposed | P1 | NEW |
...
| D-IH-7N-CLOSURE | Initiative closure — closing UAT passed; INITIATIVE row promoted to `closed`. | Founder | proposed | P<N> | NEW |
```

NEW markers on revisions only — first version has all NEW; Round 2 marks newly-added rows NEW and dropped rows DROPPED (kept in table with strikethrough).

Full register lives in `docs/wip/planning/<NN-slug>/decision-log.md` per the standard initiative scaffold.

### §9.2 Risk-register preview (inline table in plan body)

```
| ID | Risk | Likelihood | Impact | Mitigation | NEW? |
|:---|:---|:---:|:---:|:---|:---:|
| R-IH-7N-1 | <risk description> | Low / Med / High | Low / Med / High | <mitigation; cite phase that lands the mitigation> | NEW |
| R-IH-7N-2 | ... | ... | ... | ... | NEW |
...
```

Full register lives in `docs/wip/planning/<NN-slug>/risk-register.md`.

### §9.3 Round-marker discipline (per §2 Row 6)

When a plan is revised:

- **NEW** marker on rows added in this round.
- **DROPPED** marker on rows removed in this round (keep the row visible with strikethrough; the audit trail matters).
- **AMENDED** marker on rows whose status / owner / close-out phase changed in this round.

---

## §10. Mermaid diagram discipline

> **Authority.** §2 Row 2.

### §10.1 Three diagrams required for ≥5-phase plans

| Diagram | What it shows | Where it goes |
|:---|:---|:---|
| **Architecture** | The system being designed — major artefacts (SOPs, canonicals, validators, mirrors, ERP routes, sibling-repo files) as nodes; relationships (uses / mirrors / produces / consumes) as edges. | `## Architecture` section of plan body. Also in discovery report per §3.3. |
| **Module / sub-component** *(when ≥ 4 sub-components)* | Internal structure of the deliverable family — e.g. I68 InfraMonitor product/module model + operator-surface chassis sharing. | `## Module overview` section of plan body. |
| **Phase-dependency** | Execution sequence — phases as nodes; "phase A unblocks phase B" as edges. Explicit parallelism (parallel-branch syntax) when phases run concurrently. Explicit gates (dotted lines or labelled edges) when a phase is hold-gated on external trigger. | `## Phase dependency` section of plan body. |

When a previously-gating blocker clears (e.g. MCP auth fixed, external dep resolved), **redraw the diagram without the gating node** rather than leaving stale `<X>Clear`-style placeholders.

### §10.2 Node-ID conventions (mandatory)

- **Allowed**: `camelCase`, `PascalCase`, `underscores`. Examples: `brandManager`, `BrandManager`, `brand_manager`.
- **Forbidden**: spaces (`brand manager`), reserved keywords (`end`, `graph`, `subgraph`, `flowchart`, `direction`), special characters in IDs.
- **Labels** (the human-readable text in brackets) may contain parens / brackets / colons / commas IF they are quoted: `brandManager["Brand & Narrative Manager (M3 sub-area)"]`.

### §10.3 Style conventions

- **No explicit fill colours**. Renderer applies theme colours; explicit colours break in dark mode. Exception: explicit dotted/dashed/solid edge styling is OK (`A -.-> B` for dotted, `A --> B` for solid).
- **No `classDef` styling**. Keep diagrams stylesheet-free; the Cursor / GitHub renderer applies the right theme.
- **Quote labels with special characters**. `node["Label: with colon"]` works; `node[Label: with colon]` breaks the parser.

### §10.4 Example (correct shape)

```
flowchart LR
    p0[P0 — Charter] --> p1[P1 — Strand A]
    p0 --> p2[P2 — Strand B]
    p1 --> p3[P3 — Strand C: integration]
    p2 --> p3
    p3 --> p4[P4 — UAT]
    p4 --> p5[P5 — Closure]

    %% Gated relationships
    p3 -.-> ext[External hold-gate: I7M P0]
    ext -.-> p4
```

Anti-pattern (won't render):

```
flowchart LR
    p0[P0 — Charter] --> p1[P1 — Strand A]
    end[End]               %% reserved keyword as node ID
    p1 --> Strand B Node   %% spaces in node ID
```

---

## §11. Per-initiative appendix

> **Purpose.** One tight section per active or candidate initiative. Each subsection: state, hold-gates, scope summary (3-5 sentences), conundrums in flight, cross-link surfaces, references. NO duplication — point at canonical files; do not re-encode their content.

### §11.1 I70 — Holistika OS Self-Governance Foundation (CLOSED 2026-05-13)

| Field | Value |
|:---|:---|
| State | **closed** per [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) row `INIT-OPENCLAW_AKOS-70` (closed 2026-05-13 per D-IH-70-CLOSURE). |
| Why kept in appendix | Gold-standard reference plan. Future plans should match its shape (17 phases, 5 regression rounds, ~4 300 lines, inline-ratify throughout). |
| Cursor plan | [`~/.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md`](file:///~/.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md). |
| Workspace mirror | [`docs/wip/planning/70-holistika-os-self-governance/master-roadmap.md`](../70-holistika-os-self-governance/master-roadmap.md). |
| Key forward charters | I73 (People Operations + Learning curriculum, candidate); I75 (Research area governance, candidate); I76 (MADEIRA elevation, candidate). |

### §11.2 I71 — CI/CD Discipline and AIOps Baseline Maturity (CLOSED 2026-05-14)

| Field | Value |
|:---|:---|
| State | **closed** per registry row `INIT-OPENCLAW_AKOS-71` (closed 2026-05-14 per D-IH-71-CLOSURE). |
| Why kept in appendix | I71 P4 review-stamp dimension (column extension on 4 mirrored canonicals + `validate_review_stamps` + `REVIEW_STAMP_INBOX` sidecar + ERP freshness-dashboard panel slot) is the methodology-version anchor for downstream initiatives — every plan that touches review-stamped canonicals inherits the `methodology_version_at_review` column dependency. |
| Workspace mirror | [`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md`](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md). |
| Downstream dependencies | I73 P1 curriculum-versioning conundrum C-73-2 resolves toward methodology-anchor because of I71 P4. I77 P1 brand-bridge refresh cross-references I71 P1 Pack A1 (`BRAND_ENGLISH_PATTERNS.md` + `BRAND_LLM_TONE_TELLS.md`). |

### §11.3 I72 — Marketing Area Governance + Persona Registry + IntelligenceOps + RevOps + Process Catalog (CLOSED 2026-05-14)

| Field | Value |
|:---|:---|
| State | **closed** per registry row `INIT-OPENCLAW_AKOS-72` (closed 2026-05-14 per D-IH-72-CLOSURE; Round 4-8 regression amendments folded in). |
| Why kept in appendix | I72 ratified the [`.cursor/rules/akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) rule (SOP + executable runbook pairing). Every future initiative that mints a process_list.csv row must follow this rule. I72 P9 also shipped 8 adapter registries (CRM / REVOPS / EMAIL / ATTRIBUTION / BILLING / COMMUNICATION / SCHEDULING / CONTRACT) — future integration initiatives extend these registries rather than mint new ones. |
| Workspace mirror | [`docs/wip/planning/72-marketing-area-governance-and-persona-registry-expansion/master-roadmap.md`](../72-marketing-area-governance-and-persona-registry-expansion/master-roadmap.md). |
| Downstream dependencies | I73 P3 People Operations SOPs cross-link to I72 P9 paired SOP pattern (`acceptance_criteria_human` + `acceptance_criteria_automation`). I75 Research area governance inherits I72's plane × program × topic forward-layout convention. |

### §11.4 I73 — People Operations + Engagement Models + Methodology IP (ACTIVE)

| Field | Value |
|:---|:---|
| State | **active** per [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) row `INIT-OPENCLAW_AKOS-73` (P0 charter ratified 2026-05-15 per `D-IH-73-A`). Round-2 amendment to the candidate scaffold: 4 strands → 8 strands; engagement-as-unit reframe; charter-satisfies-gate per `D-IH-73-B`. |
| Hold-gates (all MET 2026-05-15) | (1) I70 closing UAT — **MET** 2026-05-13. (2) I71 P0 charter — **MET** (I71 fully closed 2026-05-14). (3) I72 P0 charter — **MET** (I72 fully closed 2026-05-14). (4) First Holistik Researcher hired (or hiring window committed) — **MET via charter-satisfies-gate reframe** per `D-IH-73-B` (bootstrapping reality: founder's own paid employment per [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §2 funds Holistika bootstrap; designing the 7-class engagement-model taxonomy IS the unblock). (5) Founder approval to onboard People Operations Lead — **MET via same reframe** (`D-IH-73-B`); People Operations Lead role minted at I70 P8.3 per [`PEOPLE_AREA_RESTRUCTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_AREA_RESTRUCTURE.md). |
| Scope summary | Mega-initiative absorbing 8 strands across 11 phases (P0..P11). Strand A Learning charter + Holistik Researcher curriculum; Strand B Ethics+Learning inseparability (quarterly co-review SOP + brand-voice refresh "we become unethical when we unlearn"); Strand C 4 Engagement-lifecycle SOPs (hiring + onboarding + payroll + offboarding) parameterized by `engagement_model_id`; Strand D People Compliance/Ethics boundary + process_list orphan reassignments; Strand E **ENGAGEMENT_MODEL_REGISTRY** sibling dimension at People Operations (7-class taxonomy: hourly / milestone / percentage / apprentice / investor / outsourced / operator_self); Strand F Historical case-law (Bâtard 2020 / Mark-II / Alias V / RCD Legal / L'Oréal arrangement); Strand G KB human-readability (4 persona views mapped 1:1 to engagement classes; hlk-erp panel filter routes); Strand H Methodology IP minting path (brand-vs-name decision matrix deferred to filing time per `D-IH-73-F`). PAUSE POINTS at P1 (canonical-CSV gate), P6 (process_list orphan reassignments), P8 (brand-vs-name decision matrix). |
| Charter-time decisions ratified (P0) | `D-IH-73-A` mega scope; `D-IH-73-B` charter-satisfies-gate; `D-IH-73-C` ENGAGEMENT_MODEL_REGISTRY home (People Operations sibling dimension); `D-IH-73-D` 7-class taxonomy; `D-IH-73-E` outsourced helper separate class with SOC; `D-IH-73-F` IP brand-vs-name deferred-with-criteria-matrix; `D-IH-73-G` 4 KB-readability personas. Decision-sources: A/C/D `operator_inline_explicit_via_askquestion`; B/E/F/G `operator_inline_default_accepted_via_skip` (Gate 1 batched AskQuestion 2026-05-15). |
| Conundrums (deferred to per-phase inline-ratify) | **C-73-1** cohort size (P2; default 1); **C-73-2** curriculum versioning anchor (P2; default methodology-anchor per I71 P4); **C-73-3** Ethics+Learning review owner (P5; default Ethics-led); **C-73-4** engagement-lifecycle SOP shape (P3; default parameterized); **C-73-5** Compliance/Ethics boundary edge cases (P6; default Compliance owns regulatory + Ethics owns AI-overreach + joint AI-content-disclosure); **C-73-6** Methodology IP licensing model (P8; default decision-deferred-with-criteria-matrix); **C-73-7** KB persona view technology (P7; default role-tagged single surface with per-persona ERP panel filters); **C-73-8** Historical case-law anonymization scope (P4; default anonymize counterparty names). |
| Cross-link surfaces | [`baseline_organisation.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv) People area (4 sub-discipline rows landed at I70 P8.3); [`process_list.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv) `tbi_peopl_*` rows (orphan reassignments at P6 + ~6-8 `tbi_peopl_dtp_engagement_*` rows mint at P1); [`ETHICAL_AUTOMATION_POSTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/ETHICAL_AUTOMATION_POSTURE.md) §5 quarterly review cadence (Strand B anchor); [`FINOPS_COUNTERPARTY_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FINOPS_COUNTERPARTY_REGISTER.csv) (Strand C payroll SOP cross-link); [`ENGAGEMENT_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/ENGAGEMENT_REGISTRY.csv) (16-col → 17-col extension at P1); [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §2 (Strand F case-law source; access_level=5); [`LOGIC_CHANGE_LOG.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/LOGIC_CHANGE_LOG.md) BT-01 brand-as-shield (Strand H anchor); [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §16 (Strand C SOP inheritance pattern); I71 P4 review-stamp dimension (`methodology_version_at_review`). |
| Cursor plan (authoritative) | [`~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md`](file:///~/.cursor/plans/i73-people-ops-engagement-models-methodology-ip-c9d4e7f3.plan.md). |
| Workspace mirror | [`docs/wip/planning/73-people-operations-and-learning-curriculum/master-roadmap.md`](../73-people-operations-and-learning-curriculum/master-roadmap.md). |

### §11.5 I74 — Brand-tooling productization (CANDIDATE — TRIGGER-watch)

| Field | Value |
|:---|:---|
| State | **candidate, dormant by design** per [`docs/wip/planning/_candidates/i74-brand-tooling-productization.md`](../_candidates/i74-brand-tooling-productization.md). TRIGGER-2 condition: ≥2 external orgs request AKOS doctrine consumption without source-fork. As of 2026-05-15 the trigger has **NOT fired** (0 external requests). |
| Scope summary (if triggered) | Refactor AKOS brand doctrine (`BRAND_VISION.md`, `BRAND_VOICE_FOUNDATION.md`, `BRAND_ENGLISH_PATTERNS.md`, etc.) into a consumable product API (likely a Supabase Edge Function + npm package + sibling-repo template). Brand canon stays SSOT in AKOS; the productization is the consumption surface. |
| Why candidate is held | Productization without market signal is premature optimization. The cost of premature productization is: (a) the brand canon ossifies around an API shape that won't fit future external requests; (b) maintenance cost across AKOS + product API doubles. Wait for signal. |
| Cursor plan (target if triggered) | TBD on promotion. |

### §11.6 I75 — Research area governance (CANDIDATE)

| Field | Value |
|:---|:---|
| State | **candidate** per [`docs/wip/planning/_candidates/i75-research-area-governance.md`](../_candidates/i75-research-area-governance.md). |
| Hold-gates per candidate | (1) I71 + I72 + I73 P0 charters ship — currently I71 + I72 CLOSED, I73 PENDING. (2) Research Director commitment (operator-level decision to formally name a Research Director). |
| Scope summary | I70 P3 promoted Research to a top-level area; I75 authors the Research area charter (governance shape, sub-disciplines, methodology-pillar registry, source-taxonomy maturation per [`source_taxonomy.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/source_taxonomy.md)). Cross-coordinates with I73 (Holistik Researcher onboarding curriculum). 5-7 phases. |
| Conundrums (open at candidate stage) | (Pending discovery; candidate file has scaffold but no conundrum index yet.) |
| Cross-link surfaces | Research area at [`docs/references/hlk/v3.0/Research/`](../../../references/hlk/v3.0/Research/); methodology-pillar registry (TBD); [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md). |

### §11.7 I76 — MADEIRA elevation (CANDIDATE)

| Field | Value |
|:---|:---|
| State | **candidate** per [`docs/wip/planning/_candidates/i76-madeira-elevation.md`](../_candidates/i76-madeira-elevation.md). |
| Hold-gates | (1) Strand A external research on AIC (Agent in Charge) F1-F5 framings completes (per the candidate's C-76-1 conundrum on AIC SOP-consumption posture). (2) Operator ratification of AIC architecture before plan-author starts. |
| Scope summary | MADEIRA is currently scaffolded but operationally thin. I76 elevates MADEIRA to a first-class operational agent: AIC role_owner architecture (F1-F5 framings — humans + AIC vs unattended runbook fire), MADEIRA-as-role-owner pattern, cross-area handoff bridges via I72's REVOPS_ADAPTER_REGISTRY pattern. Likely 7-10 phases. |
| Conundrums (open at candidate stage) | **C-76-1** AIC SOP-consumption posture — humans-and-AIC share SOP-reader role on the AC-HUMAN axis (per `D-IH-72-S`) vs AIC has its own intermediate axis. Strand A external research will inform this. |
| Cross-link surfaces | I72 `D-IH-72-S` (binary AC axis ratification); [`.cursor/rules/akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 1 (SOP + runbook pairing); I72 P9 adapter registries (cross-area handoff pattern). |

### §11.8 I77 — Impeccable Brand-Bridge Refresh + Drift Gate (ACTIVE)

| Field | Value |
|:---|:---|
| State | **active** per registry row `INIT-OPENCLAW_AKOS-77` (P0 charter ratified 2026-05-14 per D-IH-77-A). |
| Hold-gates for P1 | I71 P1 Pack A1 ship lands `BRAND_ENGLISH_PATTERNS.md` + `BRAND_LLM_TONE_TELLS.md` canonicals (MET — I71 fully closed). P1 Strand A may start. |
| Scope summary | Refresh `PRODUCT.md` + `DESIGN.md` bridges and author missing `BASELINE_REALITY.md` cross-referencing 15+ canonicals (Strand A); mint `scripts/generate_impeccable_bridges.py` + `scripts/validate_impeccable_bridge_drift.py` (Strand B); operator UAT at P3 (Strand C closing). |
| Workspace mirror | [`docs/wip/planning/77-impeccable-brand-bridge-refresh/master-roadmap.md`](../77-impeccable-brand-bridge-refresh/master-roadmap.md). |
| Conundrums (open at planning) | (Charter ratified; remaining open conundrums tracked in plan body.) |

### §11.9 I78 — Brand-voice LLM-as-judge advisory layer (CANDIDATE — TRIGGER-watch)

| Field | Value |
|:---|:---|
| State | **candidate** per [`docs/wip/planning/_candidates/i78-brand-voice-llm-judge.md`](../_candidates/i78-brand-voice-llm-judge.md). Forward-charter from I71 P1 strategic review 2026-05-14. |
| TRIGGER-condition | Promotes when the I71 regex list visibly pushes back (≥2 trigger signals per the candidate's §6 — e.g. operator-flagged false-positive cluster, sibling-repo authors complain about gate noise). |
| Scope summary (if triggered) | LLM-as-judge advisory layer on top of the I71 deterministic regex gate. Tier 2 validator that the deterministic gate calls when regex match is ambiguous. Cross-coordinates with I72 brand+storytelling sub-area generalists (per R-A regression amendment). |
| Cross-link surfaces | I71 P2 deliverables (`validate_brand_voice_register.py` + `validate_brand_french_patterns.py`); [`BRAND_LLM_TONE_TELLS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_LLM_TONE_TELLS.md). |

### §11.10 I79 — People Manifesto + Pattern Library + AI Governance + Knowledge Hygiene (CLOSED 2026-05-15)

| Field | Value |
|:---|:---|
| State | **closed** per [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) row `INIT-OPENCLAW_AKOS-79` (closed 2026-05-15 per `D-IH-79-CLOSURE`; 18 D-IH-79-* decisions across 7 inline-ratify rounds). |
| Why kept in appendix | I79 ratified the always-applied [`.cursor/rules/akos-people-discipline-of-disciplines.mdc`](../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) rule (People = discipline of disciplines; KB stewardship is People; agentic is recursive DoD; anti-jargon discipline mechanically enforced). Every future People-area canonical inherits the anti-jargon drift gate. The **`pattern_*` rows in [`PEOPLE_DESIGN_PATTERN_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv)** + the **process-singularity FK column `inherited_pattern_id`** in `process_list.csv` are the cross-area inheritance rails I81 + I82 + I83 build on. |
| Cursor plan (authoritative) | `~/.cursor/plans/i79_people_doctrine_4e309f45.plan.md`. |
| Workspace mirror | [`docs/wip/planning/79-people-manifesto-and-pattern-library/master-roadmap.md`](../79-people-manifesto-and-pattern-library/master-roadmap.md). |
| Forward charters | I80 (lessons-learned follow-up); I75 (Research design pattern library input); I76 (agentic doctrine input); I77 (design pattern library input). |

### §11.11 I80 — I79 Lessons-Learned (SOP Body/Addendum + Stakeholder Lenses + Inline-Ratify Skill + KNOWLEDGE_PAIRING_REGISTRY) (CLOSED 2026-05-16)

| Field | Value |
|:---|:---|
| State | **closed** per registry row `INIT-OPENCLAW_AKOS-80` (closed 2026-05-16 per `D-IH-80-CLOSURE`; 8 D-IH-80-* decisions A–H including charter A–G + closure). 8 atomic commits P0–P7 + P6.5 follow-on. |
| Why kept in appendix | I80 minted three durable rails the next planning rounds depend on: (a) **`pattern_sop_addendum_split`** (11th class in `PEOPLE_DESIGN_PATTERN_REGISTRY.csv`; level-4 body + level-5 addendum split with jargon-scan glob exemption for `*.addendum.md`); (b) **[`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv)** (16 cols, Pydantic SSOT in [`akos/hlk_knowledge_pairing_csv.py`](../../../../akos/hlk_knowledge_pairing_csv.py); validator [`scripts/validate_knowledge_pairing_registry.py`](../../../../scripts/validate_knowledge_pairing_registry.py); 11 governance tests; FK-resolved relationships between paired files); (c) **[`.cursor/skills/inline-ratify-craft/SKILL.md`](../../../../.cursor/skills/inline-ratify-craft/SKILL.md)** + extension to `.cursor/rules/akos-inline-ratification.mdc` §"Quality bar". |
| Workspace mirror | [`docs/wip/planning/80-i79-lessons-learned/master-roadmap.md`](../80-i79-lessons-learned/master-roadmap.md). |
| Forward charters | I81 (full-vault SOP retrofit + KB integrity per Option C; Wave 1 expansion); I82 (Capability Doctrine candidate stub minted at P7); I83 (AI Archivist / KiRBe ingestor candidate stub minted at P7). |
| Notable decisions for forward initiatives | **D-IH-80-D** (Option C forward-charter to I81 for full-vault retrofit); **D-IH-80-G** (`pattern_class` taxonomy extension `documentation_layering`); **D-IH-80-H** (KNOWLEDGE_PAIRING_REGISTRY mint as paired-file governance SSOT). |

### §11.12 I81 — Knowledge-base integrity sweep (vault + planning surface) + Compliance layout reorganisation + named-milestone migration + full-vault SOP retrofit (CANDIDATE — READY FOR P0 PROMOTION)

| Field | Value |
|:---|:---|
| State | **candidate** per [`docs/wip/planning/_candidates/i81-full-vault-sop-addendum-retrofit.md`](../_candidates/i81-full-vault-sop-addendum-retrofit.md). Stub minted at I80 P6 per `D-IH-80-D` Option C; **scope expanded twice on 2026-05-16** per operator directives — Wave 1 morning (vault integrity + DQ + Compliance layout reorg) + Wave 2 evening (planning-surface integrity + named-milestone schema + Class B drift validator + one-shot historical regression sweep). |
| Hold-gates for P0 promotion | (1) I80 closed (**MET 2026-05-16** per `D-IH-80-CLOSURE`); (2) `KNOWLEDGE_PAIRING_REGISTRY` pattern live (**MET 2026-05-16** per `D-IH-80-H`); (3) operator charter approval (**PENDING** — paste-into-fresh-chat kickoff prepared in `INITIATIVE_DEPENDENCIES.md` §5 history line 2026-05-16 evening + this appendix entry); (4) `baseline`/process approval gates queued for Compliance-layout-reorg tranches that touch validator paths (**PENDING — operator-gated per phase**); (5) named-milestone schema (**`D-IH-81-H`**) ratified at P0 charter inline-ratify (**PENDING — happens during P0 promotion chat**). |
| Scope summary | **Quadruple-strand foundation initiative** sequencing **P0 charter → P1 vault integrity + DQ baseline → P2 Compliance vault layout reorganisation (Initiative 22 forward layout: advops/finops/techops/dimensions waves) → P3 planning-surface integrity + named-milestone schema + Class B drift validator + one-shot regression sweep → P4–P8 SOP retrofit strands (RevOps/Marketing/Tech/Research-Compliance-Ethics-Learning/Operations-People-Finance) → P9 closing UAT**. ~40 SOP bodies remaining across 11 areas (per §2a in candidate stub); ~28-36 paired-files expected after the no-addendum-needed threshold applies. **Long-term governance pattern**: named milestones become permanent vocabulary across all future initiatives via `akos-planning-traceability.mdc` §"Plan-quality bar" extension at P3. |
| Conundrums (10 open at candidate stage) | **C-81-1** retrofit mode (continuous vs absorbed); **C-81-2** no-addendum-needed threshold; **C-81-3** author posture (role_owner vs single-agent batch); **C-81-4** forward-extension to non-SOP canonicals (P9 close-out); **C-81-5** per-area register-specific jargon-scan extension; **C-81-6** integrity matrix sign-off (PMO + System Owner produce + role_owners sign per area); **C-81-7** layout migration batching (wave-by-plane default); **C-81-8** named-milestone schema design (default `<I_ID>-<PURPOSE_SLUG>`); **C-81-9** validator strictness on first rollout (default fail-on-unresolved + transition allowlist); **C-81-10** closed-initiative migration policy (default frozen historical records). |
| Decisions to ratify (D-IH-81-A through D-IH-81-J + closure) | A retrofit mode + B no-addendum threshold + C author posture (P0); D forward-extension non-SOP (P9); E per-area jargon-scan extension (P0); F integrity matrix methodology (P1); G layout migration wave plan (P2); **H named-milestone vocabulary (P0)**; **I validator wiring scope (P3)**; **J closed-initiative frozen-reference policy (P3)**; CLOSURE at P9. |
| Effort estimate | P1 ~1-3d + P2 ~3-10d + **P3 ~0.5-1d** + P4-P8 ~5-8d (continuous) or absorbed into quarterly cadence; total continuously ≈ **two weeks** of QA, often better as parallel tracks (P1+P2+P3 foundation early; P4-P8 retrofits follow). |
| Cross-link surfaces | [`SOP-META_PROCESS_MGMT_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-META_PROCESS_MGMT_001.md) §4.6 body+addendum split (the authoring contract retrofit applies); [`PEOPLE_DESIGN_PATTERN_LIBRARY.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/PEOPLE_DESIGN_PATTERN_LIBRARY.md) §pattern-sop-addendum-split; [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) (every paired-body retrofit mints a row); [`compliance/canonicals/README.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/README.md) Initiative 22 forward-layout convention; [`process_list.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv) (P1 integrity matrix anchors here); to-be-minted at P3: [`akos/hlk_planning_milestone.py`](../../../../akos/hlk_planning_milestone.py) + [`scripts/validate_planning_cross_refs.py`](../../../../scripts/validate_planning_cross_refs.py) + [`tests/test_planning_cross_refs.py`](../../../../tests/test_planning_cross_refs.py) + dated `reports/p3-class-b-regression-sweep-<YYYY-MM-DD>.md` baseline. |
| Inline-ratify history (pre-P0) | Wave 1 expansion 2026-05-16 morning (operator directive on KB integrity + Compliance layout reorg + Talent activation in I82); Wave 2 expansion 2026-05-16 evening (operator inline-ratify selecting **option F+C combined, long-term target, properly governed, folded into existing initiatives**). One-shot Class B regression sweep run 2026-05-16 evening: **0 unresolved drifts in active surfaces** post commit `76838d3`; 4 phase-numbering drifts caught + fixed in `76838d3`; closed-initiative roadmaps + reports flagged as frozen historical records. |

### §11.13 I82 — Holistika Capability Doctrine and Commercial Readiness (CANDIDATE — gated on I81 P3)

| Field | Value |
|:---|:---|
| State | **candidate** per [`docs/wip/planning/_candidates/i82-holistika-capability-doctrine-and-commercial-readiness.md`](../_candidates/i82-holistika-capability-doctrine-and-commercial-readiness.md). Stub minted at I80 P7 per operator inline-ratify Round 9. |
| Hold-gates for P0 promotion | (1) operator charter approval; (2) doctrine name ratified (C-82-1); (3) **per operator directive 2026-05-16 evening: I82 promotion runs in PARALLEL with I81 P3 once I81 named-milestone schema (`D-IH-81-H`) is ratified** — earlier prep allowed (Talent baseline tranche prep, doctrine prose drafting), but `CAPABILITY_REGISTRY` mint at I82 P2 gates on **I81 P1 integrity CLOSED OR `D-IH-82-PREREQ` waiver**; (4) I83 (Archivist) is gated on I82 P4 closed (use-case archive minted) — that gate is forward-only. |
| Scope summary | **Third foundational doctrine of Holistika** (sibling to `HOLISTIKA_ORGANISING_DOCTRINE.md` and `HOLISTIKA_AGENTIC_DOCTRINE.md`): *audience-aware capability surfacing* — taking a request from any external counterparty (customer/advisor/investor/collaborator/regulator/recruiter) and producing a brand-faithful audience-appropriate response containing (1) capability rows from inventory; (2) confidence rating Keter/Euclid/Safe-style; (3) prior use-case proofs (POCs); (4) eloquence-translated message in the right register. **Operator motto: Concept → Use Case → Eloquence.** **Operator framing: "if we do it, we sell it."** Four facets across phases: P0 doctrine charter (paired body+addendum) → **P1 Talent activation in `baseline_organisation.csv` (canonical-CSV gate)** → **P2 `CAPABILITY_REGISTRY.csv` mint** (gated on I81 P1) → P3 confidence rating registry (numerical + SCP-cameo + plain-language audience-tailored) → **P4 `USE_CASE_ARCHIVE.csv`** (POCs from GDF/Hosteleria/RCD/documentation-team/Shopify) → P5 eloquence translation (`BRAND_BASELINE_REALITY_MATRIX` extension) → P6 ERP/mirrors path-hygiene → P7 live UAT + closure. ~7-10 engineer-days continuous. |
| Operator-stated intent (verbatim, 2026-05-16 inline-ratify Round 9) | *"From our side, we can guarantee that this knowledge base is worth investing in and selling out. Somehow."* — *"As the operation's motto goes: If we do it, we sell it."* — *"My motto: Concept to Use Case to Eloquence. We build capabilities, research use cases that are hot, actually do them with production-grade quality and translate them to operator, expert, user and business."* — *"Imagine you have a person telling you a capability and you tell them we've been able to surface it somewhere it actually helped? That's the kind of brand product knowledge research ops tech and more we talk about here in people."* — *"Hopefully Talent will be able to translate our inventory — process_list — into capabilities/skill list, governed and that will be the best talent I've seen because not many companies are able to explain to someone 'what you guys can do' in such a governed, clear, scalable, tangible, demonstrable way."* |
| Confidence-rating cameo lexicon (per operator Round 9 Q2) | **Keter** = Low ("we may know how to do but not enough to warrant we won't need external resources or research"). **Euclid** = Medium ("we know enough to warrant the e2e of the case but may not guarantee research is necessary"). **Safe** = High ("we can revisit after X time and activate at a moment's notice"). Cameo for methodology-curious audiences (investors/advisors/depths-readers); plain-language phrasing for general customers; numerical scale (0.3/0.7/0.95) for internal/operations. |
| Conundrums (6 open at candidate stage) | **C-82-1** doctrine final name (P0 inline-ratify); **C-82-2** confidence-rating naming policy primary register (P3 inline-ratify); **C-82-3** AI Archivist home (forward-charter to I83; ratified at P0 charter ack); **C-82-4** Talent CSV vs Capability registry vs integrity baseline sequencing (P0 inline-ratify; default = doctrine-P0-ratified → Talent-P1-queued → registry-awaits-I81-integrity-or-waiver); **C-82-5** confidence-rating cadence ownership; **C-82-6** skip/waive I81 integrity prerequisite criteria. |
| Decisions to ratify (D-IH-82-A through D-IH-82-E + PREREQ + closure) | A mega-charter scope (P0); B doctrine canonical home `People/canonicals/` (P0 — recommended default); C confidence-rating naming multi-register (P3); D capability inventory PK + FK posture (P2); **PREREQ** I81 integrity prerequisite acceptance/waiver (P2 entrance); E use-case archive redaction policy paraphrase-default (P4); CLOSURE at P7. |
| Cross-link surfaces | [`HOLISTIKA_ORGANISING_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md); [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md); [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) §N (P5 capability-messaging extension); [`SKILL_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SKILL_REGISTRY.csv) (P2 FK target); [`process_list.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv) (P2 FK target — primed via I81 P1 integrity matrix); [`baseline_organisation.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv) (P1 Talent activation operator gate); [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) (P0 doctrine paired body+addendum mints rows). |

### §11.14 I83 — AI Archivist / KiRBe Ingestor (CANDIDATE — gated on I82 P4)

| Field | Value |
|:---|:---|
| State | **candidate** per [`docs/wip/planning/_candidates/i83-ai-archivist-and-kirbe-ingestor.md`](../_candidates/i83-ai-archivist-and-kirbe-ingestor.md). Stub minted at I80 P7 per operator inline-ratify Round 9 (Tech-area-led product-shaped initiative; non-time-pressured forward-charter). |
| Hold-gates | (1) **I82 P4 closed** (`USE_CASE_ARCHIVE.csv` minted; KiRBe has a registry to ingest); (2) Tech Lab Lead bandwidth; (3) framework choice ratified (LangChain/LangGraph/CrewAI/MCP-only — Tech Lab decides per `AGENTIC_FRAMEWORK_LANDSCAPE.md`); (4) at least one concrete consumer surface (hlk-erp Knowledge panel OR external-facing capability surfacing event). |
| Scope summary (~9-12d MVP) | **Tech-area system that operationalises I82's audience-aware capability surfacing**. Conceptually similar to Composio (unified API to many tools) but wider scope: ingests internal KB + use case archive + capability registry + confidence registry + linked artefacts + external sources (engagement reports + research diagnoses + brand canon + decision logs); surfaces them through audience-aware translation layer using `BRAND_BASELINE_REALITY_MATRIX` rails. Phases P0 charter → P1 ingestor query layer → P2 audience translation layer → P3 surfacing API + consumer routes → P4 hlk-erp Knowledge panel → P5 closing UAT + closure. |
| Operator-stated intent (verbatim, 2026-05-16) | *"It's also good for other things we may build atop our system, like our AI Archivist and all-in-one ingestor (sort of like Composio, but with a wider scope), KiRBe. That's how it's tied to the knowledge base and why we also call it AI Archivist. We're from People so maybe the final specs are not like that, that for other areas to answer. We've just thought about archives and thanks to Research's info we thought of this, we leave other areas to decide what's best."* |
| Cross-link surfaces | [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) (primary registry KiRBe consumes — I80 P6.5); [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) (Tech Lab framework choice rails — I79 P3b); [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) (audience translation layer rails — I66); [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Two-plane model" (DDL via migrations + DML via emit if KiRBe lands a new schema). |

---

## §12. Anti-patterns (what NOT to do)

### §12.1 Phase-scoped or strand-scoped plan files

NEVER mint `i7N_p1_<thing>_<8hex>.plan.md`, `i7N_strand_a_<thing>_<8hex>.plan.md`, or any phase-prefixed or strand-prefixed plan file. The whole initiative lives in ONE `.plan.md` file. Heavy execution detail goes IN the file under the phase's section. Reference anti-pattern: I71 P1 Pack A1 mid-execution divergence (corrected by Round 4 amendment).

### §12.2 OPERATOR PAUSE POINT language

NEVER write the phrase "OPERATOR PAUSE POINT" in plan bodies or commit messages. Use `(inline-ratify gate at §X.Y)` instead per `akos-inline-ratification.mdc`. The only exceptions are the **mandatory pause points** classified in §8.3 (canonical-CSV gate / trademark / public-prose / page-spec) which carry explicit operator-approval-in-writing language — and even those are filed as inline `AskQuestion` calls plus a pause-record artefact, not as silent halts.

### §12.3 One-liner YAML todos

NEVER ship a plan with one-liner todos (`"P3 — author the SOP"`). Every todo is 3+ sentences declaring scope, files, validators, pause-point class, self-checkpoint count. See §2 Row 1.

### §12.4 Uncited "industry best practice" claims

NEVER write "industry best practice" / "widely accepted" / "common consensus" without a cited source per §7.1. Replace with a citation or remove the claim.

### §12.5 Skipping the self-critique gate

NEVER declare a plan "ready for operator ratification" without running the §2.2 self-critique gate. The gate is the forcing function that catches the gaps the templates would otherwise inherit.

### §12.6 Re-encoding canonical content in this compendium

NEVER duplicate content from canonical files (`process_list.csv`, `baseline_organisation.csv`, `BRAND_VISION.md`, etc.) in this compendium or in any plan body. Point at the canonical via clickable link; never copy-paste the content. Canonical drifts; copies don't auto-update.

### §12.7 Closing initiatives without UAT evidence

NEVER mark an initiative `closed` without dated UAT evidence under `docs/wip/planning/<NN-slug>/reports/` per `akos-planning-traceability.mdc` §"UAT evidence contract". Automated gates (release-gate.py + browser-smoke.py --playwright) are necessary but not sufficient when the plan promised browser/dashboard/MCP qualitative review.

---

## §13. Cross-references

### §13.1 Cursor rules (always-applied)

- [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) — plan-quality bar, master-roadmap mirror, UAT vs automated smoke, files-modified CSV.
- [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) — inline `AskQuestion` pattern; never `OPERATOR PAUSE POINT`.
- [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) — phase + commit discipline; SCOPE / PREREQUISITES / DELIVERABLES / VERIFICATION; HLK asset class.
- [`akos-agent-checkpoint-discipline.mdc`](../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) — operator pause-point contract + agent self-checkpoint contract.
- [`akos-mirror-template.mdc`](../../../../.cursor/rules/akos-mirror-template.mdc) — AKOS-as-SSOT for external repos.
- [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) — Supabase two-plane, ops planes, canonical CSV gate.
- [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) — SOP + executable runbook pairing; adapter status enum; cadence taxonomy.
- [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) — dual-register contract (internal CORPINT vs external).

### §13.2 Reference plans (gold-standard shape)

- I66 plan: [`~/.cursor/plans/brand_vision_ops_sweep_4f4c51dd.plan.md`](file:///~/.cursor/plans/brand_vision_ops_sweep_4f4c51dd.plan.md) — 8-phase Round 1/2/3 brand-ops sweep.
- I70 plan: [`~/.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md`](file:///~/.cursor/plans/holistika_os_self-governance_foundation_63841b81.plan.md) — 17-phase Round 1-5 federated SSOT.
- I68 Round 2 plan: `~/.cursor/plans/i68_cicd_activation_roadmap_592a78e2.plan.md` — Round-N revision pattern reference.

### §13.3 Canonical registers

- [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) — every initiative ever minted; state truth.
- [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) — every D-IH-* decision; FK target.
- [`OPS_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) — every OPS-* operational ops row.
- [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) — canonical vs mirrored vs reference asset class.
- [`process_list.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv) — every governed executable process.
- [`baseline_organisation.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv) — every role_owner.

### §13.4 Governed gate set

- [`config/verification-profiles.json`](../../../../config/verification-profiles.json) — profile registry (default profile `pre_commit`).
- [`docs/DEVELOPER_CHECKLIST.md`](../../../DEVELOPER_CHECKLIST.md) — operator-readable gate set.
- [`scripts/release-gate.py`](../../../../scripts/release-gate.py) — strict matrix.
- [`scripts/validate_hlk.py`](../../../../scripts/validate_hlk.py) — umbrella HLK gate.

### §13.5 Discovery + dep-map entry surfaces

- [`UNIVERSAL_KICKSTART.md`](UNIVERSAL_KICKSTART.md) — paste-snippet for fresh chats.
- [`INITIATIVE_DEPENDENCIES.md`](INITIATIVE_DEPENDENCIES.md) — dep map (mermaid + blocker table + cross-strand linkages).
- [`README.md`](README.md) — `_templates/` folder index.

---

## §14. Changelog of this compendium

| Date | Change | Author |
|:---|:---|:---|
| 2026-05-15 | Initial authoring. Collapses prior trio (`initiative-planning-prompts.md` + 6 `i7N-kickoff-prompt.md` files) into one SSOT. Adds Row 11 (self-critique gate) + Row 12 (CHANGELOG entry) to the 12-row plan-quality bar. Adds discovery-time architecture-mermaid mandate. Adds per-initiative appendix pointing at canonicals (no re-encoding). Author: PMO. | PMO |
