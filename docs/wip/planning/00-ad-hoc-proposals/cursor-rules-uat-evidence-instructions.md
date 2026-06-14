# Patch instructions: UAT evidence in Cursor rules (2026-04-15)

Plan mode / tooling may not edit `.cursor/rules/*.mdc` directly. Apply the following **manually** in the repo (or run Agent mode with file write access).

## 1. `.cursor/rules/akos-planning-traceability.mdc`

Replace the block from the line starting with `- Store progress or completion notes` through the line before `## Scope Split` with the following (verbatim):

```markdown
- Store progress or completion notes beside it as:
  - `docs/wip/planning/<NN-initiative-slug>/reports/phase-<n>-report.md`
- Store **operator / browser UAT evidence** beside it as dated markdown under the same `reports/` folder (see **UAT evidence contract** below).

## UAT evidence contract (automated gates vs qualitative sign-off)

- **Automated verification** (inventory verify, drift, `py scripts/test.py all`, `py scripts/release-gate.py`, `py scripts/browser-smoke.py --playwright`, targeted pytest, HLK validators when in scope) is **necessary** but **not sufficient** to claim every initiative acceptance criterion when the plan or `master-roadmap.md` also promises **browser**, **dashboard WebChat**, **Cursor Browser MCP**, **Langfuse UI**, **Docker Desktop settings**, or other **human-in-the-loop** checks.
- **`browser-smoke.py --playwright`** exercises scripted control-plane / API parity scenarios; it does **not** replace a written **dimension checklist** or WebChat qualitative sign-off unless the initiative explicitly equates them.
- When closing a phase or marking an initiative **complete**, if the source Cursor plan or `master-roadmap.md` required any of those qualitative rows, the initiative **must** include **at least one** of:
  - A dated **`reports/uat-<topic>-<YYYYMMDD>.md`** (or `uat-<topic>-browser-<YYYYMMDD>.md`) with a **results table**: step, PASS / SKIP / N/A, short note; **SOC:** no secrets, API keys, or full prompts in evidence files.
  - Or a **link** to an existing canonical UAT doc under `docs/uat/` **plus** a short `reports/` stub that records **date**, **who ran it**, and **per-row outcomes** (not only "see USER_GUIDE").
- If a row was **not** run, record **SKIP** or **N/A** with a one-line reason (e.g. Langfuse not configured, Neo4j mirror absent). **Do not** close with only "run `docs/DEVELOPER_CHECKLIST.md`" when browser UAT was in scope.
- **Precedent:** [`docs/wip/planning/07-hlk-neo4j-graph-projection/reports/uat-graph-explorer-browser-20260415.md`](../../docs/wip/planning/07-hlk-neo4j-graph-projection/reports/uat-graph-explorer-browser-20260415.md) and [`reports/uat-neo4j-graph-evidence-template.md`](../../docs/wip/planning/07-hlk-neo4j-graph-projection/reports/uat-neo4j-graph-evidence-template.md). Madeira / gateway WebChat baselines live under [`docs/uat/hlk_admin_smoke.md`](../../docs/uat/hlk_admin_smoke.md); initiative reports should **point there** when reusing scenarios, and still record **closure-specific** outcomes when the plan added new acceptance rows.
```

Append this bullet to **`## Quality Checks`** (after the matrix-width bullet):

```markdown
- If the initiative promised browser or manual UAT, verify a **dated `reports/uat-*.md`** (or linked canonical UAT + outcome stub) exists before treating the initiative as **closed**.
```

## 2. `.cursor/rules/akos-governance-remediation.mdc`

Under **Planning + verification expectations**, after the “Planner agents should:” bullets, append:

```markdown
  - **UAT vs automated smoke:** Treat `py scripts/browser-smoke.py --playwright` as **automated** coverage. When a phase plan or initiative roadmap also specifies **dashboard WebChat**, **Cursor Browser MCP**, **Langfuse UI**, or similar **operator sign-off**, follow **`.cursor/rules/akos-planning-traceability.mdc`** — record dated outcomes under `docs/wip/planning/<NN-initiative-slug>/reports/` (e.g. `uat-*.md`) or explicit SKIP/N/A per row. Do not mark those phases **complete** on automated gates alone.
```

## 3. Repo markdown (companion to `.mdc` patch)

- [`docs/wip/README.md`](../../README.md) — Rules bullet for initiative UAT evidence.
- [`docs/DEVELOPER_CHECKLIST.md`](../../../DEVELOPER_CHECKLIST.md) — Planning closure subsection pointing at the traceability rule.
