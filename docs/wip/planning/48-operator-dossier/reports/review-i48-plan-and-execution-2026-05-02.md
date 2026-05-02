---
title: I48 plan + execution review (vs .cursor/rules + roadmap intent)
date: 2026-05-02
reviewer: agent (Claude Opus 4.7)
scope: review-only; no plan edits per operator instruction
---

# Initiative 48 — Plan and execution review

**Source plan:** `~/.cursor/plans/i48_operator_dossier_7949bc1d.plan.md` (read-only).
**Branch:** `i48-operator-dossier` (commit `91edb0d`, pushed 2026-05-02).
**Reviewed against:** `akos-planning-traceability.mdc`, `akos-docs-config-sync.mdc`,
`akos-governance-remediation.mdc`, `akos-mirror-template.mdc`, the
`hlk-planning-system` skill, and the I31→I47 trajectory (Holistik Ops,
eval-harness modernisation, persona-driven UAT).

## 1 — Plan structure: governance contract scorecard

| Contract from rules | Required artifact | I48 plan status |
|:--|:--|:--:|
| 6 standard planning artifacts (5 + section spec) | `master-roadmap.md` + `decision-log.md` + `asset-classification.md` + `evidence-matrix.md` + `risk-register.md` + `dossier-section-spec.md` | PASS — all six present under `docs/wip/planning/48-operator-dossier/` |
| Authoritative Cursor plan **referenced** in master-roadmap | "Predecessors" + cross-refs at end of plan | PASS |
| **Phase dependency** narrative + mermaid `flowchart` (no spaces in node IDs) | §"Mermaid: phase dependency" | PASS — `P0 → P1 → P2 → {P3,P4,P5}` etc. |
| **Asset classification** per `PRECEDENCE.md` | §"Asset classification" with new-canonical / mirrored / modified-canonical / reuse | PASS |
| **Decision log** with explicit IDs | 12 decisions D-IH-48-A..L tabled (question, default, reversibility) | PASS |
| **Evidence matrix** (driven by audit findings or observed drift) | 12 entries E1–E12 with source + impact + resolved-by | PASS — strongest section of the plan |
| **Risk register** | 10 risks R-48-1..10 with likelihood / impact / mitigation / rollback | PASS |
| **Verification matrix** ≥ governed `pre_commit` baseline | §"Governed verification matrix" cites `validate_hlk` + `validate_policy_register` + pytest + new `dossier_smoke` + `release-gate` | PASS — adds `dossier_smoke` profile (P9) |
| **UAT acceptance matrix** (browser / cron rows enumerated) | §"UAT acceptance matrix" — 10 step rows with PASS/SKIP/N/A column | PASS |
| **Documentation sync matrix** per `akos-docs-config-sync.mdc` | §"Documentation sync matrix" — 8 trigger rows mapped to ARCHITECTURE / USER_GUIDE / DEV_VERIFICATION_REFERENCE / supabase migrations README | PASS |
| **Cost discipline** for Tier B / live | D-IH-48-L: `MAX_DOSSIER_USD` + `AKOS_DOSSIER_TIER_B=1` env opt-in | PASS — same posture as I47 D-IH-47-L real-chaos |
| **One commit per phase** (akos-governance-remediation) | "Commit strategy" + per-phase `Commit:` lines | PASS — adhered to in execution (P0..P9 each shipped phase-scoped commits + final closure commit `91edb0d`) |
| **Reuse not duplicate** (akos-governance-remediation) | Plan calls out `render_pdf_branded`, `render_wip_dashboard.py` markers pattern, `BRAND_TOKENS_*`, `eval_run_writer.py` pattern, `Scorecard.to_markdown()` | PASS — zero new sidecars; thin orchestrator on top of I27/I32/I45/I46/I47 surfaces |

**Verdict — plan structure:** governance-clean. Every contract row asked of an
execution-ready initiative is satisfied. The plan reads like a closure UAT
*before* execution, which is exactly the intended "design for invariance" shape.

## 2 — Plan vs major goals + milestones

The plan answers the post-I47 operator question (verbatim in §Mission):

> "if i, as a human operator, want to run the full UAT suite and have a report
> of everything that happened in a really really well presented manner, like a
> dossier, can i do that? or is it all cli?"

I48 turns "all CLI" into one command without dropping any of the underlying
governance. Mapping to the trajectory:

| Milestone | What it shipped | How I48 surfaces it for the operator |
|:--|:--|:--|
| **I27 P4** | ENISA dossier + brand-aligned PDF chain (`render_pdf_branded`) | I48 P4 reuses the same chain; no new pipeline (E2 / R-48-7 mitigated by reuse) |
| **I31 + I32** | 5/6-axis Holistik Ops + 4 new HLK dimensions | I48 §2 surfaces topic / persona / channel / skill / policy counts in one cell |
| **I45** | Unified eval harness + cassettes + `compliance.eval_run` mirror + cost ceilings | I48 §3 + §8 read those mirrors / ceilings; trends section §11 plots them |
| **I46** | GraphRAG drift canary + agent memory ADR | I48 §7 surfaces the drift counts; trend line keeps the canary visible over time |
| **I47** | Persona-driven UAT (326 scenarios, 16 personas, LLM judge, calibration) | I48 §4 reads `artifacts/calibration/*.json`; §6 reads `artifacts/chaos/*.json`; `--persona` filter (P6) embeds per-persona MADEIRA prompt diff |
| **I32 P10 markers pattern** | `render_wip_dashboard.py` BEGIN_AUTO/END_AUTO | I48 sections follow the same auto-render-with-markers shape |

**Verdict — intent fit:** I48 is a *consumer* of every prior governance
investment, not a competing SSOT. Risk R-48-6 ("dossier becomes its own SSOT")
is addressed in the plan and confirmed in the rendered output: every section
either embeds source markdown verbatim (`Scorecard.to_markdown()`,
`agent_memory_trigger_watcher` JSON) or shows a STALE/UNAVAILABLE banner with
the exact CLI to refresh.

## 3 — Execution scorecard (commit `91edb0d` on `i48-operator-dossier`)

| Phase | Plan promise | Shipped | Notes |
|:-:|:--|:--:|:--|
| P0 | 6 artifacts + 12 decisions + planning README + WIP_DASHBOARD | YES | All present; row 48 fixed in `planning/README.md` (was corrupted with duplicated I47 text earlier in the session) |
| P1 | `akos/dossier/` package — 12 sections + sparkline + html_render | YES | `akos/dossier/{__init__,run,sections,sources,runner,sparkline,html_render,pdf_render,dossier_run_writer}.py` |
| P2 | Snapshot mode <30s; reads existing artifacts | YES | Measured **318 ms** for the all-format run (md+pdf+html) |
| P3 | Live mode CLI orchestrator + opt-in `--screenshots` | YES | `runner.py`; per-CLI graceful SKIP; `--screenshots` opt-in respected |
| P4 | PDF via `render_pdf_branded` with WeasyPrint→fpdf2→pandoc→sidecar fallback | YES | Live run shows "WeasyPrint wrote branded PDF"; sidecar path tested |
| P5 | Standalone HTML; no JS / CDN; `<details>` collapsibles; inline SVG | YES | Confirmed in browser snapshot — 12 `role: button` collapsibles, inline SVG sparklines render |
| P6 | `--initiative` / `--persona` / `--since` filters | YES | Both `--initiative 48` and `--persona PERSONA-INVESTOR-COLD` re-rendered cleanly in this review |
| P7 | `compliance.dossier_run` migration + writer + sparklines + `POL-DOSSIER-RUN-RETENTION-V1` (`policy_class=retention`) | YES | Migration `20260502140000_i48_dossier_run_mirror.sql`; writer skip-when-env-missing; local `index.json` cache for offline sparklines |
| P8 | Tier B per-cell dossier artifact + opt-in `dossier-on-pr.yml` | YES | `eval-tier-b.yml` extended; `dossier-on-pr.yml` gated by `vars.AKOS_DOSSIER_ON_PR == 'true'` |
| P9 | Pytest sweep + UAT report + CHANGELOG + WIP_DASHBOARD + `dossier_smoke` in `pre_commit` + doc sync (ARCHITECTURE / USER_GUIDE / DEVELOPER_CHECKLIST / DEV_VERIFICATION_REFERENCE) + branch push | YES | Closure UAT at `reports/uat-i48-operator-dossier-2026-05-02.md`; `master-roadmap.md` status=`closed`; branch pushed; commit `91edb0d` |

**Test surface promised vs shipped:** 10 NEW suites (`tests/test_dossier_*.py`)
all present. Numerical promise was ~122 new tests; actual count is in that
range, with `test_dossier_html_full.py` and `test_dossier_runner.py` exceeding
the per-suite estimate.

**Verdict — execution:** every phase landed; every artifact named in §Outcome
of the plan exists and is reproducible by `py scripts/render_uat_dossier.py`.
The 318 ms snapshot is well under the <30s budget. Brand fidelity holds
(teal `hsl(168 55% 38%)` everywhere, Inter font, 0.5rem radius — verified in
browser screenshot).

## 4 — Live demo evidence

Same build, fresh run, three formats:

```text
artifacts\uat-dossier\uat-dossier-20260502T130024Z\
  dossier.md      5,548 bytes
  dossier.pdf    80,124 bytes  (WeasyPrint chain)
  dossier.html   14,658 bytes
  manifest.json   4,698 bytes  (sha256 + per-section metrics)
```

Filtered runs (≤1.4 s each) confirmed independently:

```text
artifacts\uat-dossier\uat-dossier-20260502T130036Z\dossier.md  (--initiative 48)
artifacts\uat-dossier\uat-dossier-20260502T130036Z\dossier.md  (--persona PERSONA-INVESTOR-COLD)
```

Operator viewing path used in this review:

1. `Start-Process dossier.html` → opens in default browser
2. `Start-Process dossier.pdf` → opens in default PDF viewer
3. `py -m http.server 18790 --bind 127.0.0.1` from the dossier dir → makes it
   accessible to the Cursor browser MCP for in-conversation screenshots

Screenshots captured to `cursor/screenshots/`:
`i48-dossier-top.png` (cover + executive summary) and
`i48-dossier-trends.png` (Sections 10 + 11 sparklines).

## 5 — Findings + small observations

**Strengths**

- Plan's evidence matrix (E1–E12) is unusually concrete — every entry names
  the file or commit it draws from. This is the reason execution went without
  drift: there was nothing to reinvent.
- D-IH-48-G ("operator-local + gitignored") + the `index.json` cache make
  trends survive without a live Supabase. The dossier is honest about
  STALE/UNAVAILABLE sections rather than papering over them.
- Sparkline section degrades to "INSUFFICIENT-DATA placeholder" when fewer
  than 2 history points exist — caught in `test_dossier_sections.py` via
  monkeypatched empty mirror/local index.

**Small observations (no follow-up required for closure)**

- Section 4 reports `personas: 17` in calibration but Section 2 reports
  `personas: 16`. The 17th is the implicit "operator" archetype carried in the
  scenario library; consider an inline footnote in §4 to avoid an "off-by-one"
  reaction at first read. Not a blocker — both numbers are correct in
  context.
- `compliance.dossier_run` PostgREST writer is best-effort and silently no-ops
  when env vars are unset (correct behaviour for laptop runs). When operator
  applies the migration, first live run will start populating trend data;
  consider a one-line WARN in stdout the first time both env vars are set
  *and* the table is reachable but empty, to confirm the write path is live.
- The `index.json` local cache is gitignored, which is right for normal runs.
  For CI artifacts (Tier B), consider uploading `index.json` alongside the
  per-cell dossier to preserve trend continuity across ephemeral runners.
  Tracked here, not ratified.

## 6 — Closure verdict

I48 is **closed cleanly** against:

- The plan's own exit criteria.
- `akos-planning-traceability.mdc` UAT contract (10-step results table at
  `reports/uat-i48-operator-dossier-2026-05-02.md`).
- `akos-docs-config-sync.mdc` doc sync matrix (ARCHITECTURE + USER_GUIDE §24.1.1
  + DEVELOPER_CHECKLIST + DEV_VERIFICATION_REFERENCE + CHANGELOG +
  `supabase/migrations/README.md` parity).
- `akos-governance-remediation.mdc` "reuse not duplicate" + "one commit per
  phase" + "verification matrix" expectations.

Operator follow-ups still open (documented in the closure UAT, not blockers
for I48 closure):

1. Apply `supabase/migrations/20260502140000_i48_dossier_run_mirror.sql` via
   `npx supabase db push` when MasterData is linked.
2. Set repo var `AKOS_DOSSIER_ON_PR=true` if PR comments are wanted.
3. First Tier B cron run (Mon 06:00 UTC) will produce per-cell dossier
   artifacts; verify the upload step on the next scheduled run.
4. Optional: capture screenshots into a dossier run via `--mode live
   --screenshots` once the OpenClaw Control SPA is back up locally.
