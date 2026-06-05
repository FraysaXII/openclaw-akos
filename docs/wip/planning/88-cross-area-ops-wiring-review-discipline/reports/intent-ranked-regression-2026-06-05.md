---
report_kind: intent_ranked_regression
authored: 2026-06-05
program: INIT-OPENCLAW_AKOS-88
seat: thinking (Opus) + execution probes
ratifying_decisions: [D-IH-88-E]
candidate_decision: D-IH-88-F
verdict: PASS — 0 new regressions; 1 high-intent pre-existing drift repaired; 8 known/deferred dispositioned
---

# Intent-Ranked Regression — 2026-06-05

> Operator ask (2026-06-05): *"not mechanical — take all my intents, all the use
> cases I aspire to, my logic, my scenarios, my interactions (past/present/future),
> create a ranking system; research inside; research outside; review the ranking;
> then do the regression; mint findings; and if you achieved a lot, mint the
> workflow improvements so we can do regressions like these better and more often,
> no matter the seat."*

This is the value layer above the mechanical inter-wave regression (which asks *is
everything wired?*). This run asks **is what you care about most still served?**

## 1. Internal research — the intent corpus (what you care about)

Distilled from your own surfaces (not invented):

| Source | Signal |
|:---|:---|
| `operator-scratchpad.md` | "full-protocol" sessions: fleet sweep → sibling WIP → scratchpad drain → execute. Recent: Finance area, I90 routing, DATA clean-slate. |
| `OPERATOR_INBOX.md` (RICE-ranked) | Top: Brand/Vision/Ops apply (OPS-66-2, 2040), RevOps Discovery (OPS-67-1, 1920), trademark (OPS-66-1, 840); long FINOPS tail (I81). |
| `USE_CASE_ARCHIVE.csv` | Aspired realisations: KiRBe SaaS, HLK-ERP, Websitz/Rushly partner delivery, public site + CRM. |
| `OPS_REGISTER` open severities | OPS-81-13 tax calendar "single most consequential"; rev-rec CRITICAL; counterparty CRITICAL. |
| `INITIATIVE_REGISTRY` | 60+ initiatives; active spine = governance integrity, FINOPS, MADEIRA, ERP, routing. |

### Seven intent tiers (value 1-5, evidenced)

| Tier | Intent (plain language) | Value | Horizon |
|:---|:---|:---:|:---|
| **IT-1** | Get to first revenue (KiRBe SaaS, partner channel, pricing, rev-rec) | 5 | future |
| **IT-2** | Exist legally & fiscally (incorporation, tax, trademark, ENISA, capital) | 5 | present |
| **IT-3** | Keep the governed knowledge base internally true & auditable (the AKOS thesis) | 5 | all |
| **IT-4** | Operate with leverage (MADEIRA, dashboards, two-seat, full-protocol sessions) | 4 | all |
| **IT-5** | Be credible externally (brand baseline reality, render, deck, investor) | 4 | present |
| **IT-6** | Trust the evidence (eval harness, judge, persona scenarios, UAT, research) | 3 | all |
| **IT-7** | Stay deployable (OpenClaw runtime, CICD, sibling repos) | 3 | present |

## 2. External research — how mature orgs prioritize what to check

| ID | Source (reliability) | What it gives the ranking |
|:---|:---|:---|
| EXT-R1 | FMEA / Risk Priority Number — Jama Software; SixSigma.us; testRigor; vdiversify 2026 (A2, industry-standard) | RPN = Severity × Occurrence × Detection; **severity-first / Action-Priority override** (act on catastrophic regardless of composite); Detection is the weak axis worth manual eyes. |
| EXT-R2 | WSJF — SAFe / Reinertsen; Centercode; ideaplan 2026 (A2) | Cost of Delay = Business-Value + Time-Criticality + Risk-Reduction; **portfolio-altitude** weighting (right for an initiative portfolio, where RICE is too feature-level). |
| EXT-R3 | Test Impact Analysis + Predictive Test Selection — Microsoft Learn; Meta Engineering; Fowler 2026 (A1) | Bound candidate set by **what changed**, rank by **fault-likelihood**, keep the **full sweep as a periodic safety net** (never delete it). |

## 3. Review — what the external sweep changed in the ranking

The v1 draft was a flat intent-weighted sum. The external grounding tightened it into a defensible model:

1. **Adopted WSJF's additive Cost-of-Delay** (intent_value + time_criticality + risk_reduction) instead of a single intent number — captures urgency that pure RICE-style reach misses (EXT-R2).
2. **Added FMEA's Detection axis, inverted** (`detection_gap`) — surfaces with no always-on gate get manual eyes even at lower intent (EXT-R1). This is what caught finding F-2 below.
3. **Added the severity-first override** — existence-critical surfaces (IT-2/IT-3 with a live gap) lead regardless of composite (EXT-R1 Action-Priority).
4. **Kept the full mechanical sweep as the safety net** and treated this layer as TIA-style ranking on top, not a replacement (EXT-R3).
5. **Deliberate deviation:** omitted WSJF's ÷ job-duration — "checking" duration is ~uniform across surfaces and the operator wants depth-ordering, not effort-economy. Documented in the SSOT module.

Result: **ICS = 3·intent_value + 2·time_criticality + 2·risk_reduction + 1·detection_gap** (max 40), with severity-first surfaces leading.

## 4. The ranked sweep (run top-down)

From `py scripts/intent_ranked_regression.py --rank`:

| # | Surface | ICS | Severity-first |
|:-:|:---|:-:|:-:|
| 1 | S-06 Legal/fiscal existence artifacts (tax calendar, instruments, trademark) | 36 | ! |
| 2 | S-04 FINOPS commercial substrate (rev-rec, pricing, counterparty spine) | 35 | ! |
| 3 | S-01 Governance SSOT integrity (`validate_hlk`) | 34 | |
| 4 | S-05 Release-gate composite | 32 | |
| 5 | S-12 Schema drift (CSV/Pydantic/mirror three-surface sync) | 32 | |
| 6 | S-02 Area-completeness matrix | 31 | |
| 7 | S-03 Structural inter-wave regression | 29 | |
| 8 | S-07 Operator interaction surfaces | 27 | |
| 9 | S-08 Brand & external-render trail | 26 | |
| 10 | S-11 Index integrity | 26 | |
| 11 | S-09 Eval / MADEIRA quality | 24 | |
| 12 | S-10 Runtime / deploy health | 24 | |

## 5. Run results (probes, in ICS order)

| Surface | Probe | Result |
|:---|:---|:---|
| S-06 | `validate_finops_tax_calendar.py` | PASS (8 obligations) |
| S-04 | `dataops_quality_check.py --data-fam FINOPS-SPINE`; `finops_monthly_recon.py --self-test`; pricing validator | PASS (3/3 clean; recon PASS) |
| S-01 | `validate_hlk.py` | OVERALL PASS |
| S-05 | `release-gate.py` | **3552 pass / 9 fail** (see §6 attribution) |
| S-12 | `check-drift.py` + per-registry pytest | drift clean; **1 enum-lag found** (F-2) |
| S-02 | `validate_area_completeness.py --matrix` | Finance 93%, Data 92%, no Finance gaps |
| S-03 | `inter_wave_regression_sweep.py --self-test` | PASS (13 probes) |
| S-10 | `check-drift.py`; `workspace_fleet_hygiene_sweep.py` | clean=11, WARN=1 (sibling WIP) |

## 6. Findings — attributed (the load-bearing move)

**Headline: 0 of the 9 release-gate failures were introduced by this session's Finance F2a/F2b/F3 work.** The 3552 passing total includes the new pricing / tax / FINOPS-spine tests.

| ID | Finding | Intent | Attribution | Disposition |
|:---|:---|:---:|:---|:---|
| **F-1** | 7 eval failures (adversarial ×3 + promotion ×4) — MADEIRA cassettes route `gtm_project` vs expected | IT-6 | **known-deferred** — `OPS-90-9` cassette replay, ETA 2026-06-11 | defer-OPS (cite existing row) |
| **F-2** | `area_governance` pattern-class absent from `VALID_PATTERN_CLASSES` enum (test pinned at 15) while CSV + wired validator already accept it | **IT-3** | **pre-existing** — I93 `D-IH-93-B` mint; dual-SSOT lag | **rework-now** (fixed this session) |
| **F-3** | Company-deck slide 11 quotes `1.188` vs live `1205` processes | IT-5 | **pre-existing** — accumulated process-count drift (recurring; you hand-fix it) | defer-OPS + recommend de-brittle (auto-sync the quote) |
| **F-4** | Fleet hygiene WARN: `hlk-erp` sibling worktree dirty (`KIRBE_API_ENV.md`) | IT-7 | **pre-existing** — operator WIP, not AKOS | accept (operator-owned) |

### F-2 fixed-now rationale (why this one, not the others)

The ranking earns its keep here. Of 9 flat release-gate failures, F-2 is the one that is **(a) highest-intent (IT-3 governance integrity = the AKOS thesis), (b) low-effort (one enum entry + one test constant), (c) reversible, and (d) severity-first eligible.** FMEA's severity-first rule says fix it regardless of composite. The others are either owned+deferred (F-1), brand-chore drift better fixed at its source (F-3), or not ours (F-4). A mechanical "9 failed" buries this; the intent rank surfaces it as the one to act on.

Repair: added `area_governance` to `akos/hlk_design_pattern_csv.py` `VALID_PATTERN_CLASSES`; updated the size test 15→16 + added `test_area_governance_class_in_enum`. `tests/test_design_pattern_registry.py` 23/23 PASS. Release-gate failures 9 → 8.

## 7. Dispositions (5-option enum)

- **F-1 → defer-OPS:** `OPS-90-9` already owns it (ETA 2026-06-11). No new row.
- **F-2 → rework-now:** done this session.
- **F-3 → defer-OPS + improvement note:** the deck quote should auto-derive the process count (de-brittle) rather than hardcode; recurring manual fix is the smell. Recommend folding into the brand/deck owner's next pass.
- **F-4 → accept:** sibling-repo operator WIP; surfaced by fleet hygiene, not an AKOS regression.

## 8. Did we achieve a lot? → workflow improvement minted

Yes — enough to harden the method so either seat can repeat it cheaply:

| Artifact | Purpose | Seat |
|:---|:---|:---|
| `akos/hlk_intent_ranked_regression.py` | Pydantic SSOT: 7 tiers + 12 surfaces + ICS | both |
| `scripts/intent_ranked_regression.py` | `--rank` / `--tiers` / `--self-test` | execution |
| `tests/test_intent_ranked_regression.py` | 8 tests incl. determinism + severity-first | execution |
| `.cursor/skills/intent-ranked-regression-craft/SKILL.md` | the judgment HOW (corpus → score → run → attribute → disposition) | thinking |
| `.cursor/rules/akos-intent-ranked-regression.mdc` | the WHEN (candidate; agent-requested, no glob — zero always-on cost) | both |

"No matter the seat": the execution seat runs `--rank` for the ordered checklist and `--self-test` as a pre_commit circuit-breaker; the thinking seat reads the skill for corpus distillation + attribution + disposition.

## 9. Gated next step (operator)

Canonical registration of this as a governed discipline (a `pattern_intent_ranked_regression` row, a `process_list` row, a `CANONICAL_REGISTRY` row, and ratifying decision `D-IH-88-F`) touches canonical CSVs and therefore needs your approval per baseline governance. Surfaced via AskQuestion at session end. Until then the rule stays **candidate** and the runbook/skill operate unregistered.

## 10. Verification

`intent_ranked_regression.py --self-test` PASS · `test_intent_ranked_regression.py` 8/8 · `test_design_pattern_registry.py` 23/23 · `validate_hlk.py` OVERALL PASS · `validate_area_completeness.py --matrix` Finance 93%.
