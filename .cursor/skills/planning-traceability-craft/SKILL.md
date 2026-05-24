---
name: planning-traceability-craft
description: Use when authoring or revising any Cursor plan or initiative roadmap in this AKOS workspace that meets the plan-quality bar trigger conditions (≥ 5 phases, ≥ 1 calendar week, touches canonical CSV, multi-repo, or is a revision). Codifies the craft for materialising the plan-quality bar — multi-sentence YAML todos, round-expansions narrative, 3 mermaid diagrams, per-phase deep section, inline decision-log + risk-register previews, CONTRIBUTING.md validator callouts, file-path density. Triggers on plan-quality bar, master-roadmap, phase-plan, multi-sentence YAML todos, round-expansions, phase-dependency diagram, per-phase deep section, plan revision, UAT quality bar, closure UAT template. Pairs with .cursor/rules/akos-planning-traceability.mdc (the WHEN); this skill is the HOW.
version: 1.0.0
ratifying_decisions: D-IH-86-CT
authored: 2026-05-24
---

# Planning-Traceability Craft

> Codified at I86 Wave R close (drain7) to operationalise the I66 + I68 plan-quality bar precedent + the post-2026-05-19 UAT quality bar. The craft turns "write a plan" from informal brainstorm into a structured artifact that future agents inherit fully. Ratified by D-IH-86-CT.

## When to use this skill

Read this skill before:

- Authoring any Cursor plan that meets the plan-quality bar trigger (≥ 5 phases, ≥ 1 calendar week, touches canonical CSV, multi-repo, or is a revision of a prior plan).
- Authoring any `docs/wip/planning/<NN-slug>/master-roadmap.md` for an execution-relevant initiative.
- Revising an existing plan in response to operator feedback (adds a Round N narrative).
- Authoring any closure UAT report under the post-2026-05-19 quality bar (mandatory when initiative has ≥ 5 phases OR touches canonical CSV OR ships sibling-repo work OR is I86-cluster OR promised browser/dashboard/WebChat UAT).

This skill assumes you have already read [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc) (the *when*).

## Core principles

### Principle 1 — Multi-sentence YAML todos (not one-liners)

Every Cursor-plan `todos:` entry must be multi-sentence with the following content density per todo:

- Scope (1-2 sentences: what + why).
- Files-to-create or files-to-modify (named with full paths).
- Validators-to-mint (with module path + Pydantic model name where applicable).
- Pause-point classification (`PAUSE POINT #N` or `none`).
- Self-checkpoint count.

Reference template:

```yaml
todos:
  - id: pN-<short-purpose-slug>
    content: "PN (<effort> days; PAUSE POINT #M if applicable) — <one-sentence purpose>. (a) <deliverable 1 with file paths>. (b) <deliverable 2 with validator name + module>. (c) <verification rule>. (d) <decision close-outs>. ..."
    status: pending
```

One-liner todos are the most common failure mode; they hide scope, hide file inventory, and break operator-side audit.

### Principle 2 — Round-expansions narrative on revisions

When a plan is revised in response to operator feedback, the body's top section becomes `## What changed since <prior-version>` with `### Round N` sub-blocks per round. Each round paragraph cites:

- Operator-supplied evidence (timestamp, quote, decision ID).
- Structural delta to the plan (sections added, removed, scope shifts, gates dropped).

This makes plan history auditable without diffing the file. I66 Round 3 + I68 Round 2 are the worked examples.

### Principle 3 — Three mermaid diagrams (required for ≥ 5-phase plans)

Every qualifying plan body MUST include:

1. **Architecture mermaid** — the system being designed.
2. **Module / sub-component mermaid** — internal structure of the deliverable family (optional but encouraged if ≥ 4 sub-components).
3. **Phase-dependency mermaid** — execution sequence with explicit parallelism + gating.

Mermaid syntax rules (binding):

- Node IDs use `camelCase` / `PascalCase` / underscores; NO spaces; NO reserved keywords (`end`, `graph`, `subgraph`, `flowchart`).
- Labels containing parentheses, brackets, colons, or commas must be quoted.
- NO explicit fill colours or `classDef` styling (breaks in dark mode).
- When a previously-gating blocker clears, redraw the diagram without the gating node (don't leave stale `<X>Clear` placeholders).

### Principle 4 — Per-phase deep-section template

Each phase header uses `## P<N> — <name> (<effort> days; PAUSE POINT #M if applicable)` and contains:

- **Scope** (1 paragraph: what + why).
- **Files** (organised as: canonical [new + modified, full paths]; mirrored/derived [per consumer-repo, `repo=<slug>` notation]; validators [Pydantic model path + script path + test path]; templates [when introducing reusable bless-pattern templates]).
- **Verification** (commands or vendor-API observable signals).
- **Pause-point classification** (per `akos-agent-checkpoint-discipline.mdc` category).
- **Self-checkpoint count** (per the checkpoint-discipline cadence heuristic).
- **Cursor-rules adherence** (1-line citation per phase: "this phase operationalises `akos-X.mdc §Y` + respects `akos-Z.mdc`").

### Principle 5 — Inline decision-log + risk-register previews

The plan body MUST contain:

- A table preview of every `D-IH-NN-X` decision: ID, question (one line), owner, status entering plan, close-out phase. New decisions in revision Round flagged with **NEW**.
- A table preview of every `R-IH-NN-N` risk: ID, risk, likelihood, impact, mitigation. Added/dropped risks flagged with **NEW** / **DROPPED**.

The full register stays in initiative's `decision-log.md` / `risk-register.md`; the inline preview is for readers who skim.

### Principle 6 — CONTRIBUTING.md adherence callouts for new validators

Every plan that mints new Python validators must explicitly note that they follow `CONTRIBUTING.md` §"Python Code Standards":

- Pydantic models in `akos/<module>.py` (never hand-written assert chains).
- Type hints on every function signature + return type.
- Structured logging via `akos.log.setup_logging` (not `print()`).
- `akos.process.run` for subprocess shell-out (with timeout; never bare `subprocess.run`).
- Cross-platform `pathlib.Path` + `os.environ`.
- Tests in `tests/test_<module>.py` with valid + invalid input pairs + `@pytest.mark.<group>` + `scripts/test.py` group registration.
- Wired into `scripts/release-gate.py` and `config/verification-profiles.json`.

Callouts go inline in the per-phase **Files** sub-section, not as a generic appendix.

### Principle 7 — File-path density

Every commit, file, validator, route, mirror, view, template, and SOP referenced in the plan MUST carry a clickable markdown link to its full repo path on first mention. Subsequent mentions may use bare backticks.

## UAT quality bar craft (post-2026-05-19 closure UAT)

The 11-section closure UAT template at `docs/wip/planning/_templates/uat-closure-template.md` is the binding shape. Highlights:

- Mandatory frontmatter: `verdict:` (PASS / PASS-WITH-FOLLOWUP / FAIL / PENDING-OPERATOR-WALK), `closure_decision_source:`, `ratifying_decisions:`, `linked_runbooks:`, optional `verdict_history:`.
- §1 Closure summary — TL;DR table; < 30 s read for J-OP.
- §2 Closure-criteria verification — every row with a `Verification command` column.
- §3 Mechanical evidence — verbatim validator outputs + pytest counts + browser-evidence pattern when in scope (screenshot + a11y snapshot + sha256 + timestamp).
- §4 Per-dimension findings — multi-column table for multi-dimension acceptance.
- §5 D-IH-86-D mechanical cross-check — 4-signal table (release-gate INFO / validate_hlk PASS / paired-runbook contract / UAT report present) when cluster sibling.
- §6 SOP+runbook pair — AC-HUMAN + AC-AUTOMATION acceptance when applicable.
- §7 Risk-register closure — every R-IH-NN-N row.
- §8 Decision close-outs — every D-IH-NN-X row.
- §9 Closure registry edits — INITIATIVE_REGISTRY / DECISION_REGISTER / OPS_REGISTER after-states.
- §10 Verdict + 7-item operator sign-off checklist.
- §11 Cross-references.

The Wave R closure UAT at `docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/uat-wave-r-closure-2026-05-24.md` is the worked example.

## Pre-flight checklist

1. Trigger conditions verified (≥ 5 phases OR ≥ 1 week OR canonical-CSV touch OR multi-repo OR revision).
2. YAML todos are multi-sentence with file inventory + validators + pause-points + self-checkpoints.
3. Round-expansions narrative authored if revision.
4. 3 mermaid diagrams (architecture + module + phase-dependency).
5. Per-phase deep section uses the 6-element template.
6. Inline decision-log + risk-register previews present.
7. CONTRIBUTING.md adherence callouts present per phase that mints validators.
8. File-path density: every artefact linked on first mention.
9. If closure UAT: 11-section structure + mandatory frontmatter fields populated.

## Anti-patterns

- **AP1 — One-liner YAML todos.** Hides scope; breaks operator audit.
- **AP2 — Skip the round-expansions on revisions.** Plan history not auditable.
- **AP3 — Single mermaid diagram.** Architecture diagrams alone don't show phase-dependency.
- **AP4 — Per-phase prose without file inventory.** Reviewers can't tell what lands.
- **AP5 — Hidden decision-log.** Full register not in plan body; readers must hunt.
- **AP6 — Generic CONTRIBUTING.md appendix.** Not inline per validator; reviewer skips.
- **AP7 — Bare backticks on first mention.** Reader can't click through to the file.

## Cross-references

- Parent rule: [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc).
- Closure UAT template: [`docs/wip/planning/_templates/uat-closure-template.md`](../../../docs/wip/planning/_templates/uat-closure-template.md).
- Worked examples: I66 plan (`~/.cursor/plans/brand_vision_ops_sweep_4f4c51dd.plan.md`) + I68 Round 2 plan (`~/.cursor/plans/i68_cicd_activation_roadmap_592a78e2.plan.md`) + Wave R closure UAT.
- Sister skills: [`agent-checkpoint-craft`](../agent-checkpoint-craft/SKILL.md) (pause-points + self-checkpoints), [`inline-ratify-craft`](../inline-ratify-craft/SKILL.md), [`quality-fabric-craft`](../quality-fabric-craft/SKILL.md).
- Ratifying decision: D-IH-86-CT (this skill mint).
