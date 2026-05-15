---
title: SOP — Tech Lab Agentic Infrastructure Operations
language: en
intellectual_kind: tech-lab-canonical-sop
sop_id: SOP-TECH_AGENTIC_INFRA_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - System Owner
  - Tech Lead
last_review: 2026-05-15
last_review_by: System Owner
ratifying_decisions:
  - D-IH-79-A
  - D-IH-79-F
  - D-IH-79-L
  - D-IH-79-M
status: active
register: internal
linked_canonicals:
  - AGENTIC_FRAMEWORK_LANDSCAPE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - ETHICAL_AGENTIC_BOUNDARIES.md
linked_runbooks:
  - scripts/tech_agentic_landscape_audit.py
linked_processes:
  - env_tech_dtp_agentic_infra_ops_001
cadence: scheduled
cadence_schedule: quarterly
cadence_secondary: event_triggered
cadence_secondary_trigger: framework upgrade or MCP posture change
---

# SOP — Tech Lab Agentic Infrastructure Operations

## Purpose

Operationalise the Tech Lab side of the agentic governance split. This SOP carries the cadence — framework upgrades, MCP wiring, KB embedding/transformation pipelines, audit cycles — that keeps the Tech Lab canonical [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](AGENTIC_FRAMEWORK_LANDSCAPE.md) in sync with what is actually running in production.

Paired with the runbook [`scripts/tech_agentic_landscape_audit.py`](../../../../../../../../scripts/tech_agentic_landscape_audit.py) per [`akos-executable-process-catalog.mdc`](../../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1. Either a System Owner (or Tech Lead) can run it via the SOP; the runbook is the unattended path. Both surfaces are SSOT for the same process.

## Scope

In scope:

- **Framework upgrade cadence** for the 8 framework rows in `AGENTIC_FRAMEWORK_LANDSCAPE.md` §1: scheduled quarterly review of each row's upstream release notes; ratification of major-version bumps; pin-version updates in our agent runtimes.
- **MCP wiring** for the MCP servers in `AGENTIC_FRAMEWORK_LANDSCAPE.md` §3: adding a new server, retiring an existing server, promoting a server's posture (read → write, write → suggest, suggest → decide).
- **KB embedding pipeline** for the KB infrastructure dimensions in `AGENTIC_FRAMEWORK_LANDSCAPE.md` §2: embedder swaps, transformer swaps, ERP-projection rebuilds, Obsidian-compatibility regression checks.
- **Landscape audit** via `scripts/tech_agentic_landscape_audit.py`: scheduled quarterly + event-triggered when any of the above three sub-scopes change. Confirms framework rows still resolve to live releases, MCP server postures match configured state, KB pipelines emit the expected derived artefacts.

Out of scope:

- The **why** of agentic governance — at [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) (People-side).
- The **People-side cadence** for testing agents honour the doctrine — at [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](../../People/canonicals/SOP-PEOPLE_AGENTIC_OPERATIONS_001.md).
- **Ethical red lines** — at [`ETHICAL_AGENTIC_BOUNDARIES.md`](../../People/Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md). Tech Lab actions that propose to cross a red line route to Ethics Advisor before execution.

## Inputs

- The current `AGENTIC_FRAMEWORK_LANDSCAPE.md` framework rows + MCP postures + KB infrastructure dimensions.
- The set of agent runtimes in production (`scripts/openclaw_*` family + sibling-repo agent surfaces when blessed).
- The set of MCP servers configured under `~/.cursor/projects/.../mcps/` (per-environment) and `mcp.json` (per-repo).
- Upstream release notes for the 8 framework rows (LangChain / LangGraph / LlamaIndex / OpenClaw / CrewAI / Ollama / VercelAI / Groq).
- The previous quarterly audit report (under `docs/wip/planning/79-people-manifesto-and-pattern-library/reports/landscape-audits/<YYYY-Q>/`).

## Steps

### 1. Quarterly landscape audit (scheduled)

Once per quarter, System Owner runs the full landscape audit:

1. Run `py scripts/tech_agentic_landscape_audit.py` — confirms every framework row's upstream link still resolves (HTTP 200 or local-runtime probe), every MCP server's configured posture matches the matrix in `AGENTIC_FRAMEWORK_LANDSCAPE.md` §3, every cross-reference inside the canonical resolves.
2. Read each framework row's upstream release notes since the last audit. Flag major-version bumps for ratification (step 2 below). Note minor-version bumps for the quarterly report.
3. Inventory new MCP servers added during the quarter; classify each at the appropriate posture; flag any that drifted up the autonomy ladder (e.g. read → write) without explicit ratification.
4. Review the KB infrastructure dimensions for swaps that landed during the quarter (embedder change, transformer change, ERP migration). Each swap should already have its own `D-IH-*` decision row; confirm the canonical reflects the current state.
5. Write the report to `docs/wip/planning/79-people-manifesto-and-pattern-library/reports/landscape-audits/<YYYY-Q>/landscape-audit.md`.

### 2. Framework major-version ratification (event-triggered)

When a framework row's upstream releases a major version (semver `X+1.0.0`):

1. Tech Lead opens a ratification thread: cite the release notes, identify breaking changes that affect our agent runtimes, propose pin-version bump or migration plan.
2. System Owner reviews; if migration is non-trivial, opens an `OPS-*` row in `OPS_REGISTER.csv` to track the migration.
3. The People agentic operations cadence is pinged (per `SOP-PEOPLE_AGENTIC_OPERATIONS_001.md` step 6 escalation routing) so an event-triggered knowledge-test runs against any agent whose scope intersects the upgraded framework. The knowledge-test confirms the upgrade has not changed the agent's behaviour against the doctrine.
4. The cross-area breakthrough propagation SOP (P4 deliverable) is invoked when the upgrade introduces capability that other areas may want to consume.
5. After migration lands, `AGENTIC_FRAMEWORK_LANDSCAPE.md` §1 row is updated; the audit cadence at step 1 verifies parity at the next quarterly run.

### 3. MCP server lifecycle (event-triggered)

When a new MCP server is added:

1. The default posture is **read** (per `AGENTIC_FRAMEWORK_LANDSCAPE.md` §3). The server is wired in this default posture and used by agents in that posture for at least one full audit cycle.
2. Promotion to **write** requires: the agent's named role explicitly carrying the write mandate; the canonical defining the role naming the write surfaces; an `OPS-*` row tracking the change; ratification by System Owner.
3. Promotion to **suggest** requires the same plus an explicit human checkpoint design (the operator approves each suggestion before execution); ratification by System Owner + Tech Lead.
4. Promotion to **decide** is rare and requires Ethics review per `ETHICAL_AGENTIC_BOUNDARIES.md` red-line 3 (no autonomous action on canonical CSVs without operator gate); ratification by System Owner + Ethics Advisor + the role-owner of the canonicals the MCP server can mutate.

When an MCP server is retired:

1. Tech Lead documents the retirement reason; opens an `OPS-*` row.
2. All agents that referenced the server are audited for fallback handling; agents whose named-role contract depends on the server are reduced in scope until a successor server (or a workflow change) is ratified.
3. The canonical is updated; the audit cadence at step 1 verifies the next quarterly run.

### 4. KB pipeline maintenance (event-triggered)

When the embedder is swapped, transformer is swapped, or ERP projection contract changes:

1. Tech Lead opens an `OPS-*` row; cites the trigger (cost / latency / accuracy / vendor consolidation / regulatory).
2. The Obsidian-compatibility regression test runs: every Markdown canonical re-renders cleanly without the new tooling.
3. The ERP projection re-emits via [`scripts/sync_compliance_mirrors_from_csv.py`](../../../../../../../../scripts/sync_compliance_mirrors_from_csv.py); SQL-side queries confirm parity.
4. The People agentic operations cadence is pinged so an event-triggered knowledge-test runs against any agent whose KB-lookup behaviour may have shifted.
5. The canonical §2 row is updated.

### 5. Cross-area pingback when People doctrine revises

When [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) revises substantively:

1. The cross-area breakthrough propagation SOP (P4 deliverable) fires; this canonical receives the pingback.
2. System Owner + Tech Lead read the People-side change; assess whether the framework rows / MCP postures / KB infrastructure rows need to revise to stay coherent.
3. Substantive Tech Lab revisions land in this canonical; minor revisions land in the next quarterly audit.

## Outputs

- Quarterly landscape audit report under `docs/wip/planning/79-people-manifesto-and-pattern-library/reports/landscape-audits/<YYYY-Q>/landscape-audit.md`.
- `OPS-*` rows for major-version bumps, MCP posture changes, KB pipeline swaps.
- Updated `AGENTIC_FRAMEWORK_LANDSCAPE.md` rows when changes ratify.
- Cross-area breakthrough digest entries (consumed by the P4 propagation SOP).

## Failure modes

- **Audit skipped.** Mitigation: the SOP's primary cadence is `scheduled` quarterly in `process_list.csv`; the row's last-run column flags overdue. The runbook can dry-run any time without operator gate.
- **Framework row drift (canonical out of date).** Mitigation: `tech_agentic_landscape_audit.py` runs as the first step of every quarterly cycle; 404 on an upstream link is the canonical evidence of drift.
- **MCP server posture creep (write surface used as suggest, etc.).** Mitigation: posture promotion requires explicit ratification; the audit step 1.3 inventories drift each quarter.
- **People doctrine revises without Tech Lab pingback.** Mitigation: the cross-area breakthrough propagation SOP (P4) explicitly pings Tech Lab when `HOLISTIKA_AGENTIC_DOCTRINE.md` is touched; this is the structural defence against the People/Tech Lab triangle going out of sync.

## Cross-references

- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](AGENTIC_FRAMEWORK_LANDSCAPE.md) — the canonical this SOP operationalises.
- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) — sibling People-side doctrine.
- [`ETHICAL_AGENTIC_BOUNDARIES.md`](../../People/Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md) — Ethics-side red lines; consulted on **decide**-posture promotions.
- [`SOP-PEOPLE_AGENTIC_OPERATIONS_001.md`](../../People/canonicals/SOP-PEOPLE_AGENTIC_OPERATIONS_001.md) — sibling People-side SOP; receives pingbacks when frameworks upgrade.
- [`scripts/tech_agentic_landscape_audit.py`](../../../../../../../../scripts/tech_agentic_landscape_audit.py) — paired runbook.
- [`PRECEDENCE.md`](../../People/Compliance/canonicals/PRECEDENCE.md) — registers this SOP.
