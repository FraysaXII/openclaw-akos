# OpenCLaw-AKOS documentation map

**Purpose:** this file is the **index for humans**—where to go first, by role. It does not replace the technical sources listed below. **Machine-verifiable commands and argv** for verification live in [config/verification-profiles.json](../config/verification-profiles.json), [DEVELOPER_CHECKLIST](DEVELOPER_CHECKLIST.md), and [reference/DEV_VERIFICATION_REFERENCE](reference/DEV_VERIFICATION_REFERENCE.md).

## Where different kinds of doc live

| Area | What belongs there | Examples |
|:-----|:---------------------|:---------|
| **Root of repo** | High-level product pitch, install hooks | [README.md](../README.md), [CONTRIBUTING.md](../CONTRIBUTING.md) |
| **`docs/` (this tree)** | Stable operator and developer reference | [ARCHITECTURE](ARCHITECTURE.md), [USER_GUIDE](USER_GUIDE.md), [SOP](SOP.md), [SECURITY.md](../SECURITY.md) |
| **[guides/](guides/)** | Tutorials and explanations (narrative, link-heavy) | [First-time contributor](guides/first_time_contributor.md), [Understanding verification](guides/understanding_verification.md) |
| **[reference/](reference/)** | Long command tables, optional script runbook slices | [DEV_VERIFICATION_REFERENCE](reference/DEV_VERIFICATION_REFERENCE.md) |
| **[wip/planning/](wip/planning/)** | Initiative roadmaps, decision logs, phase reports (governed; not “final” product docs) | [Planning index](wip/planning/README.md) |
| **[references/hlk/](references/hlk/)** | HLK v3.0 vault, compliance CSVs, SOPs | e.g. [PRECEDENCE](references/hlk/compliance/PRECEDENCE.md) |
| **[uat/](uat/)** | UAT scenarios, smoke checklists | [rollback guide](uat/rollback_guide.md) |

**Do not** put new initiative **proposals** under `docs/guides/`; use [wip/planning/99-proposals](wip/planning/99-proposals/) or a numbered folder per [wip/planning/README](wip/planning/README.md).

## Read by role

### I am contributing code or tests

1. [CONTRIBUTING.md](../CONTRIBUTING.md) — PR flow and standards.  
2. [guides/first_time_contributor](guides/first_time_contributor.md) — one happy-path tutorial (bootstrap, dry-run, targeted tests).  
3. [DEVELOPER_CHECKLIST](DEVELOPER_CHECKLIST.md) — what to run before commit.  
4. [guides/understanding_verification](guides/understanding_verification.md) — why `verify` / `release-gate` / `run-evals` exist and how they connect.  
5. [ARCHITECTURE](ARCHITECTURE.md) — components, APIs, and operator scripts when you touch runtime.

### I am operating or demoing the stack

1. [USER_GUIDE](USER_GUIDE.md) — operators, MCP, deployment.  
2. [SOP](SOP.md) — formal procedures.  
3. [reference/DEV_VERIFICATION_REFERENCE](reference/DEV_VERIFICATION_REFERENCE.md) — optional scripts, Playwright, gateway triage.  
4. [README.md](../README.md) — quick start and capabilities overview.

### I work on HLK / compliance / governance

1. [references/hlk/compliance/PRECEDENCE](references/hlk/compliance/PRECEDENCE.md) — canonical vs mirrored assets.  
2. [DEVELOPER_CHECKLIST](DEVELOPER_CHECKLIST.md) — HLK validators when vault CSVs change.  
3. [ARCHITECTURE](ARCHITECTURE.md) — HLK and registry sections.  
4. Planning initiatives: [wip/planning/README](wip/planning/README.md) for numbered folders and decision logs.  
5. [docs/GLOSSARY](GLOSSARY.md) — short definitions with pointers.

### I am planning or closing an initiative

1. [wip/planning/README](wip/planning/README.md) — index of `NN-` initiative folders.  
2. [`.cursor/rules/akos-planning-traceability.mdc`](../.cursor/rules/akos-planning-traceability.mdc) (in repo) — UAT evidence and verification matrix expectations.  
3. [DEVELOPER_CHECKLIST](DEVELOPER_CHECKLIST.md) — golden path and doc sync triggers.

## Quick links

| Doc | Use when |
|:----|:---------|
| [GLOSSARY](GLOSSARY.md) | Unfamiliar acronyms (SSOT, HLK, release gate, profile, …) |
| [CHANGELOG](../CHANGELOG.md) | What shipped when |
| [tests/evals/README](../tests/evals/README.md) | Eval suite layout and `run-evals` CLI |
| [config/verification-profiles.json](../config/verification-profiles.json) | SSOT for `pre_commit` steps and governance eval suite list |

## Narrative vs reference

- **Narrative** (`guides/`, this README): *why* and *which path*; may summarize; if anything disagrees with config or the checklist, **config and checklist win**.  
- **Reference** (checklist, `reference/`, JSON): *exactly what to run*; keep in sync with code via [akos-docs-config-sync](../.cursor/rules/akos-docs-config-sync.mdc) habits.

---

*Last structurally significant update: documentation digest layer (map + guides + glossary).*
