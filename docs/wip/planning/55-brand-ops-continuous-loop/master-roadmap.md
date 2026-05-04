---
language: en
status: active-continuous-loop
initiative: 55-brand-ops-continuous-loop
report_kind: master-roadmap
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 55 — Brand/Ops continuous improvement loop + advisor-update triggers (closes I24 capability; stays open as ongoing loop)

**Folder:** `docs/wip/planning/55-brand-ops-continuous-loop/`

**Status:** **Loop tooling SHIPPED 2026-05-03 (P0 + P6 + P7 + P8).** I55 stays **Open as continuous loop** per **D-IH-55-F** — no fixed end date; revisit only if doctrine changes. Operator-content phases (P1–P5) deferred and forwarded as **OPS-55-1**. I24 master-roadmap stays **Open** (not Closed at capability) until P1–P5 land. See [`reports/uat-i55-loop-tooling-closure-2026-05-03.md`](reports/uat-i55-loop-tooling-closure-2026-05-03.md).

**Authoritative Cursor plan:** `~/.cursor/plans/i50–i56_madeira_kb_completion_87cc767e.plan.md` §"Initiative 55".

**Depends:** I50 closure ✓ (clean baseline + telemetry + drift-clean state); I52 P6 ✓ (multi-judge + endpoint cost surface so regression artifacts include cost-aware judge signal).

**Origin:** [Initiative 24](../24-hlk-communication-methodology/master-roadmap.md) is currently `P0 + P0a-scaffold + P1 in progress (2026-04-29)`; phases P1-P5 are partial; P6 is operator-gated G-24-3 (IRREVERSIBLE real adviser email send). [Wave-2 YAML](../22a-i22-post-closure-followups/operator-answers-wave2.yaml) Sections 2 + 3 + 5 are partly filled.

**Operator direction (2026-05-03):**
> "We operate independently from the advisor. The advisor is just an advisor; we'll send him the latest regression. I'm still at the dossier-sending stage because I'm not convinced yet. HLK Ops contributes to sending clearer messages to the advisor or any party. I need to know we can keep improving brand and ops while doing regressions to review artifacts so that everything is updated (if relevant; if not, no update)."

## Reframing

I55 is **not** a one-shot "fire G-24-3 and close". It's a **continuous operating loop**:

1. Each regression cycle emits artifacts (dossier, cover email draft, register diffs).
2. The operator reviews artifacts to **improve brand/ops/registers**.
3. After improvements, re-run regression. If artifacts have **materially changed since the last advisor send** AND improvement is real (not noise), surface a **send proposal**.
4. Operator decides yes/no per proposal. G-24-3 is **IRREVERSIBLE-per-fire**; may trigger 0, 1, or N times over the loop's lifetime.
5. If no material change → no send. Loop continues; brand/ops keeps improving regardless.

## Goal

(a) Drive I24 P1-P5 deliverables to **Closed (capability)** so the *capability* exists (composer, brand foundation, GOI/POI ALTER, register schema).
(b) Build the **regression→review→improve→maybe-send** loop tooling so brand/ops improvement is decoupled from advisor cadence.
(c) Define **material-change detection** so the system suggests sends only when worth it.
(d) Allow G-24-3 to fire when the operator is convinced the artifact is meaningfully better.

**Bidirectional contract:** I24 status → Closed (capability); I55 stays **Open as continuous loop**; each fire produces a dated `reports/uat-adviser-send-N-YYYY-MM-DD.md`.

## Asset classification

| Class | Paths | Rule |
|:------|:------|:-----|
| **Modified canonical (vault)** | `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md`, `BRAND_REGISTER_MATRIX.md`, `BRAND_DO_DONT.md` | Operator-confirmed via Wave-2 Section 2 + `wave2_backfill.py` |
| **Modified canonical (registry)** | [`process_list.csv`](../../references/hlk/compliance/process_list.csv) — tranche `thi_mkt_dtp_NN` "Communication methodology maintenance" | G-24-2 operator approval |
| **Modified canonical (registry + DDL)** | [`GOI_POI_REGISTER.csv`](../../references/hlk/compliance/GOI_POI_REGISTER.csv) — adds `voice_register`, `language_preference`, `pronoun_register` columns; `compliance.goipoi_register_mirror` ALTER via Supabase MCP `apply_migration` | G-24-1 operator approval |
| **New canonical (vault)** | `SOP-HLK_COMMUNICATION_METHODOLOGY_001.md` (4-layer methodology); **`SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001.md`** (the regression→review→send doctrine) | Brand area; CSV-before-SOP per SOP-META |
| **Modified script** | [`scripts/compose_adviser_message.py`](../../../scripts/compose_adviser_message.py) — finalize 4-layer composer | I24 P4 |
| **New scripts** | **`scripts/regression_artifact_diff.py`** — compares current dossier/cover-email artifact vs last-sent artifact; emits material-change report (cite-counts, scenario deltas, judge-axis movement, brand-voice diff). **`scripts/propose_advisor_update.py`** — when material change ≥ threshold AND operator-flagged improvement, emit a send proposal with diff summary. | |
| **Modified profile** | [`config/verification-profiles.json`](../../../config/verification-profiles.json) — `regression_loop_smoke` profile; `export_adviser_handoff_*_smoke` if missing | |
| **New canonical (POLICY)** | `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` (reuses I50 `cost_ceiling`-style POLICY pattern but `policy_class=update_threshold`); operator-set fields `min_changed_scenarios`, `min_judge_axis_movement_pp`, `min_register_rows_added` | G-55-loop-1 |
| **New reports (per fire)** | `reports/uat-adviser-send-N-YYYY-MM-DD.md` for each G-24-3 fire (N increments); per-fire SMTP manifest + sha256s + material-change diff snapshot | |
| **New reports (capability closure of I24)** | `reports/uat-i24-capability-closure-YYYY-MM-DD.md` (when P1-P5 land) — separate from any send fire | |

## Phase plan (capability close ~4-6 op-days; loop runs continuously after)

**Capability phases (close I24, then keep tooling running):**

| Phase | Focus |
|:-:|:----|
| **P0** | Bootstrap I55 folder + 6 artefacts; cross-link I24 (read-only); README row. |
| **P1** | **Wave-2 Section 2 finalize:** Operator confirms `voice_charter`, `archetype`, `narrative_pillars`, `voice_is`, `voice_is_not`, `register_matrix`; run `py scripts/wave2_backfill.py --section brand_voice --dry-run` then full write; commit `BRAND_VOICE_FOUNDATION.md` + `BRAND_REGISTER_MATRIX.md` + `BRAND_DO_DONT.md`. **Operator-input gated** — D-IH-17 forbids invention. |
| **P2** | **Wave-2 Section 3 finalize:** Operator confirms 6 GOI/POI voice profiles; run `py scripts/wave2_backfill.py --section goi_poi_voice`; verify with `validate_goipoi_register.py`. **Operator-input gated.** |
| **P3** | **I24 P1 SOP finalize (G-24-2):** Author `SOP-HLK_COMMUNICATION_METHODOLOGY_001.md` (4-layer methodology); add `process_list.csv` tranche `thi_mkt_dtp_NN` under `thi_mkt_prj_1`; **CSV-before-SOP per SOP-META-PROCESS-MGMT-001 §4.2-4.3**. **Operator-approval gated (G-24-2).** |
| **P4** | **I24 P2 ALTER (G-24-1):** Extend `GOI_POI_REGISTER.csv` with the 3 nullable columns; add Supabase migration; apply via user-supabase MCP `apply_migration`; verify mirror row count + new columns via MCP `execute_sql`. **Operator-approval gated (G-24-1).** |
| **P5** | **I24 P4 + P5 composer:** Finalize `compose_adviser_message.py` 4-layer composition; add multi-format export profile (`_html_smoke`, `_pdf_smoke`); pytest sweep. **Depends on P1-P2 brand voice content.** |
| **P6** | **Regression-loop tooling (the new heart of I55):** Author `regression_artifact_diff.py` + `propose_advisor_update.py`; commit `SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001.md`; add `regression_loop_smoke` profile. **Operator-content-independent — ships in this cycle.** |
| **P7** | **Material-change threshold POLICY (G-55-loop-1):** Author `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` with operator-set fields; `policy_class=update_threshold` added to `VALID_POLICY_CLASSES`; tests assert proposal triggers only when threshold crossed. **Ships in this cycle.** |
| **P8** | **Capability closure UAT:** Dated `reports/uat-i55-loop-tooling-closure-YYYY-MM-DD.md`; flip I55 to **partial-capability close** if P1-P5 deferred. I24 master-roadmap stays Open until Wave-2 brand voice content lands (forwarded as **OPS-55-1**). **I55 itself stays Open as continuous loop** (D-IH-55-F). |

**Continuous loop phases (run any time after P8; can fire 0, 1, or N times):**

| Loop step | Focus |
|:-:|:----|
| **L1** | Operator runs `py scripts/render_uat_dossier.py --filter madeira --mode live`; reviews artifact + judge axes + endpoint costs (from I52). |
| **L2** | Operator improves brand / ops / registers based on findings (any tranche, any time); commits via normal AKOS gates. |
| **L3** | Operator (or schedule) re-runs the regression; `regression_artifact_diff.py` compares current artifact vs last-sent artifact. |
| **L4** | If `propose_advisor_update.py` fires (material change ≥ threshold), emit a proposal at `reports/proposal-advisor-send-YYYY-MM-DD.md` with diff summary. If not, loop returns to L1. |
| **L5** | Operator reviews proposal; if convinced, runs pre-flight checklist (compressed I24 P6) and commits intent into Wave-2 YAML or replacement section. |
| **L6** | **G-24-3 IRREVERSIBLE SEND (per-fire operator action):** Operator presses Send via off-repo SMTP; **immediately** captures real timestamp + SMTP manifest + sha256s into `reports/uat-adviser-send-N-YYYY-MM-DD.md`; `regression_artifact_diff.py` records this as the new "last-sent" baseline. |
| **L7** | Loop returns to L1. |

## Verification matrix

| Check | Cadence |
|:------|:--------|
| `py scripts/validate_hlk.py` (each phase touching CSVs) | Every commit |
| `py scripts/validate_goipoi_register.py` (P4 — 3 new optional columns) | Every commit P4+ |
| `py scripts/validate_program_id_consistency.py` | Every commit P4+ |
| `py scripts/wave2_backfill.py --section brand_voice --dry-run` | After Section 2 fill |
| `py scripts/wave2_backfill.py --section goi_poi_voice --check-only` | After Section 3 fill |
| `py -m pytest tests/test_compose_adviser_message.py -v` | P5 |
| `py -m pytest tests/test_regression_artifact_diff.py tests/test_propose_advisor_update.py -v` | After P6 |
| `py scripts/verify.py export_adviser_handoff_smoke` + `_pdf_smoke` + `_html_smoke` | P5 + per-fire pre-flight |
| `regression_loop_smoke` profile (P6 + ongoing) | Per regression run |
| `validate_policy_register.py` (incl. `update_threshold` policy_class after P7) | Every commit |
| MCP `execute_sql` row-count probe + column-existence on `compliance.goipoi_register_mirror` after ALTER | P4 |
| Pre-commit grep guard for SMTP recipient-address pattern (R-55-2) | Every commit |
| `propose_advisor_update.py` returns "no proposal" when no material change | Every regression cycle |

## Operator approval gates

- **G-24-1** (P4) — `ALTER TABLE compliance.goipoi_register_mirror` (3 nullable columns) via MCP. **Operator-pending; OPS-55-1.**
- **G-24-2** (P3) — `process_list.csv` named tranche `thi_mkt_dtp_NN` "Communication methodology maintenance". **Operator-pending; OPS-55-1.**
- **G-55-loop-1** (P7) — `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` field values; new `update_threshold` policy_class. **Fires this cycle.**
- **G-24-3** (L6, **per-fire**) — Each individual advisor send is its own IRREVERSIBLE gate; pre-flight checklist signed; operator finalizes + sends; never fires automatically; can fire 0, 1, or N times across the loop's lifetime.

## Decisions seeded

- **D-IH-55-A** — Pre-flight checklist authoritative location: I55 `reports/uat-adviser-send-N-YYYY-MM-DD.md` per fire; cumulative log in `reports/loop-history.md`.
- **D-IH-55-B** — SMTP send path: off-repo identity store; recipient address never enters git; pre-commit grep guard.
- **D-IH-55-C** — I24 vs I55 folder split: I24 stays Closed at capability landing (P8); I55 stays Open as continuous loop; both linked.
- **D-IH-55-D** — Material-change threshold default values: `min_changed_scenarios≥3`, `min_judge_axis_movement_pp≥2`, `min_register_rows_added≥1`. Operator may tune per-advisor or per-tier.
- **D-IH-55-E** — Loop telemetry: every fire writes a `reports/uat-adviser-send-N-*.md`; every "no proposal" regression also logs to `reports/loop-history.md` so the operator sees both signal and silence.
- **D-IH-55-F** — Closure of I55 itself: **no fixed end date**; revisit closure trigger only if doctrine changes (e.g., advisor relationship ends; communication methodology rewritten).

## Risks

- **R-55-1** — Operator changes mind mid-pre-flight or after send. Mitigation: pre-flight is reversible (drafts hold composer); G-24-3 is IRREVERSIBLE by definition per fire; no retry/recall policy.
- **R-55-2** — Recipient email address leaks into git. Mitigation: pre-commit grep for SMTP pattern; off-repo identity store; SOP cite per `SOP-HLK_TRANSCRIPT_REDACTION_001`.
- **R-55-3** — Brand voice authoring slips into invention (vs operator-lived). Mitigation: D-IH-17 "we cite operator's lived protocols, not invent"; P1 explicitly runs Wave-2 backfill, not free-form. **In this cycle: P1-P2 deferred to operator wave-2 fill (OPS-55-1).**
- **R-55-4** — `compose_adviser_message` adds language jargon that fails brand lint at runtime. Mitigation: I49 `lint_brand_voice_offline.py` runs in `pre_commit`; composer tests assert linter green on rendered fixtures.
- **R-55-5** — Material-change threshold too tight: real improvements never trigger a proposal; advisor never gets updated. Mitigation: per-axis thresholds tunable in POLICY; operator can manually trigger via `propose_advisor_update.py --force-proposal`.
- **R-55-6** — Material-change threshold too loose: advisor gets spammed with non-improvements. Mitigation: G-24-3 is per-fire operator-gated; threshold defaults err on the conservative side; operator review before any send.
- **R-55-7** — Operator improves brand/ops indefinitely without ever sending; advisor relationship cools. Mitigation: this is a feature (operator independence); but `loop-history.md` surfaces "N regressions, 0 sends since YYYY-MM-DD" so it's visible.

## Success metrics

- I24 master-roadmap status = **Closed (capability)** after P8 — **deferred** in this cycle to OPS-55-1 (Wave-2 brand voice fill).
- I55 stays Open with the **loop tooling working**: every regression run produces either a proposal or a no-proposal log entry. **Ships this cycle (P6 + P7).**
- ≥1 G-24-3 fire over the loop's lifetime (when operator is convinced); each fire has real timestamp + sha256s + material-change diff snapshot. **Per-fire; not in this cycle.**
- 0 sends fired without operator pre-flight + decision.
- Wave-2 YAML Sections 2 + 3 fully filled; Section 5 evolves to per-fire log. **Operator-pending.**
- `compliance.goipoi_register_mirror` has 3 new columns + populated rows for the 6 voice profiles. **Operator-pending.**
- Brand/ops improvement velocity is **measurable** independently of send cadence (metric: register edits per week; brand-foundation refinements per month).

## What this is NOT

- Marketing automation; the loop always asks operator before sending; threshold suppression is the default.
- A blocking dependency between brand/ops improvement and advisor cadence (decoupled by design).
- Sending without operator hand-final-review (G-24-3 is per-fire IRREVERSIBLE).
- Authoring brand voice from scratch (D-IH-17; we cite operator's lived protocols).
- A one-shot send + close (the loop is the deliverable).

## Loop history

One-line ledger per material loop event (operator confirmations, dry-run regressions, send fires, threshold tunes). Cumulative log of cycles + silences lives at [`reports/loop-history.md`](reports/loop-history.md) per **D-IH-55-E**.

- 2026-05-04: brand voice operator-confirmed (D-IH-55-G); Wave-2 voice content cluster closed.
