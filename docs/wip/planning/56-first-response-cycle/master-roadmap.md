---
language: en
status: gated_external
initiative: 56-first-response-cycle
initiative_id: INIT-OPENCLAW_AKOS-56
report_kind: master-roadmap
program_id: shared
plane: advops
authority: Founder
last_review: 2026-05-03
gated_on: All execution phases after P0 are blocked until the first external adviser reply arrives and is captured.
---
# Initiative 56 — First advisor response cycle (close the return-trip rails)

**Folder:** `docs/wip/planning/56-first-response-cycle/`

**Status:** **Bootstrapped 2026-05-03 (P0 only).** All phases P1–P8 are forwarded as **OPS-56-1** — they cannot fire until **two events** in order:

1. The I55 loop *first* proposes an advisor send (`propose_advisor_update.py` writes `proposal-advisor-send-*.md`).
2. The operator finalises that proposal and fires G-24-3 IRREVERSIBLE (off-repo SMTP).

Only after the advisor *replies* can I56 P1 (capture response) execute. AKOS does not send; AKOS does not synthesise advisor replies. This initiative ships zero execution phases in cycle 1; it ships only the **rails**: the governance scaffold + cross-links + the SOP cite-graph that makes the response cycle one-command when the reply lands.

**Authoritative Cursor plan:** `~/.cursor/plans/i50–i56_madeira_kb_completion_87cc767e.plan.md` §"Initiative 56".

**Depends:** **First G-24-3 fire from the I55 loop** (any time after I55/P8). Not gated on I55 closure since I55 stays Open as a continuous loop (D-IH-55-F).

**Origin:** [Initiative 21](../21-hlk-adviser-engagement-and-goipoi/master-roadmap.md) ADVOPS plane is the rail (closed 2026-04-28; 4 ADVOPS canonical CSVs + 4 mirrors + plane SOP + `EXTERNAL_ADVISER_ROUTER.md` live); [I22](../22-hlk-scalability-and-i21-closures/master-roadmap.md) closed deferred actions; [I55](../55-brand-ops-continuous-loop/master-roadmap.md) ships the first outbound (eventually) via its continuous loop. **I56 specifically closes the return-trip so the rails get exercised end-to-end exactly once before scaling.** Subsequent response cycles then run via I55 loop step **L1** (operator captures response → updates registers → next regression cycle eventually proposes a follow-up); I56 doctrine becomes operating norm after closure.

## Goal

Exercise the **first** complete advisor response cycle end-to-end:

- Incoming reply → response capture (transcript redaction per `SOP-HLK_TRANSCRIPT_REDACTION_001.md`) → register updates (`ADVISER_OPEN_QUESTIONS.csv` + `FOUNDER_FILED_INSTRUMENTS.csv` + `GOI_POI_REGISTER.csv` if new POI) → mirror sync → operator-decided next-step composer → optional second outbound (gated).
- Bidirectional contract: feeds I21 plane evidence + I55 loop telemetry; produces ADVOPS plane SOP refinements as living-doctrine output.
- After I56 closes, response cycles operate as **L1 of the I55 loop** without their own initiative.

## Asset classification

| Class | Paths | Rule |
|:------|:------|:-----|
| **Modified canonical (registers)** | [`ADVISER_OPEN_QUESTIONS.csv`](../../../references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv), [`FOUNDER_FILED_INSTRUMENTS.csv`](../../../references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv), [`GOI_POI_REGISTER.csv`](../../../references/hlk/compliance/GOI_POI_REGISTER.csv) | Each register tranche is its own G-3..G-5 (I21 pattern) gate; **no fabricated `ref_id`s** per AKOS rule |
| **New reference-only** | Redacted transcript MD under [`docs/references/hlk/business-intent/delete-legal-transcripts/`](../../../references/hlk/business-intent/delete-legal-transcripts/) (or current canonical home per [I22 layout](../22-hlk-scalability-and-i21-closures/master-roadmap.md)) | Per `SOP-HLK_TRANSCRIPT_REDACTION_001` — references `POI-*`/`GOI-*` only; raw originals stay off-repo |
| **Modified canonical (vault)** | `SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md` refinements based on first-cycle lessons (if any) | Operator decision; non-required |
| **Mirror sync run** | `compliance_mirror_emit` for `compliance.adviser_open_questions_mirror`, `compliance.founder_filed_instruments_mirror`, `compliance.goipoi_register_mirror`, `compliance.adviser_engagement_disciplines_mirror` | Standard per-tranche cadence |
| **New scripts** | **None expected.** Reuse [`scripts/export_adviser_handoff.py`](../../../../scripts/export_adviser_handoff.py) + [`scripts/compose_adviser_message.py`](../../../../scripts/compose_adviser_message.py). I56 is rails-exercise, not new tooling. |
| **New reports** | `reports/p<N>-*-YYYY-MM-DD.md` per phase; **`reports/uat-adviser-cycle-1-YYYY-MM-DD.md`** at closure | |

## Phase plan (~5–7 op-days; mostly elapsed time waiting on advisor)

| Phase | Focus | Cycle 1 status |
|:-:|:----|:---------------|
| **P0** | Bootstrap I56 folder + 6 artefacts; cross-link I21 + I55; README row. | **DONE** (this commit) |
| **P1** | **Capture response (operator):** Advisor replies (when ever); operator copies body into off-repo identity store; runs redaction per SOP; commits redacted MD with `POI-*`/`GOI-*` references only; raw transcripts stay off-repo. | **OPS-56-1** (waits on first reply) |
| **P2** | **Update registers (G-56-1, three sub-gates):** **G-56-1a** add answered Q-rows to `ADVISER_OPEN_QUESTIONS.csv`; **G-56-1b** promote any committed instruments to `FOUNDER_FILED_INSTRUMENTS.csv`; **G-56-1c** add new `POI-*` rows if previously-unknown participants appear; each tranche its own commit + validator. | **OPS-56-1** (depends on P1 content) |
| **P3** | **Mirror sync:** Run `compliance_mirror_emit` for the 4 ADVOPS mirrors; verify row counts CSV vs mirror via MCP `execute_sql`; commit `reports/p3-mirror-sync-YYYY-MM-DD.md`. | **OPS-56-1** (depends on P2 commits) |
| **P4** | **Hand back to I55 loop (preferred path):** Treat the response as a loop-input; operator improves brand/ops/registers based on response content; next regression cycle (I55 L1) runs; if it surfaces a material follow-up, the I55 loop will *propose* a send via `propose_advisor_update.py`. **No forced second send in I56.** | **OPS-56-1** (operator step) |
| **P5** | **Decision-log entries:** D-IH-56-* per substantive engagement decision; cross-reference to `POI-*`/`GOI-*` ref_ids only (no PII); decisions captured to inform future loop runs. | **OPS-56-1** (per-cycle) |
| **P6** | **(Optional) G-56-2 follow-up send:** Compressed I55 L5–L6; commits `reports/p6-follow-up-send-YYYY-MM-DD.md`. If the loop does *not* propose, P6 stays empty. | **OPS-56-1** (optional; loop-driven) |
| **P7** | **Telemetry capture + SOP refinement:** Lessons learned for ADVOPS plane + I55 loop SOP refinement; surface in I21 reports as `2026-MM-DD-cycle-1-feedback.md`; consider tightening I55 material-change thresholds if the response revealed false signal. | **OPS-56-1** (post-P3) |
| **P8** | **Cycle-1 UAT closure:** Dated `reports/uat-adviser-cycle-1-YYYY-MM-DD.md` with redaction sanity check + register diff + I55-loop continuity. **After I56 closes, response handling becomes I55 L1.** | **OPS-56-1** (depends on P7) |

## Verification matrix (re-run when each OPS-56-1 phase fires)

| Check | Cadence |
|:------|:--------|
| `py scripts/validate_adviser_questions.py` | After P2 |
| `py scripts/validate_founder_filed_instruments.py` | After P2 (if instruments committed) |
| `py scripts/validate_goipoi_register.py` | After P2 (if new POI) |
| `py scripts/validate_hlk.py` (full vault incl. all four ADVOPS register validators) | Every commit |
| `py scripts/verify.py compliance_mirror_emit` | After P3 |
| MCP `execute_sql` row-count parity (4 ADVOPS mirrors) | P3 + P8 |
| **Transcript redaction sanity check (no raw transcript paths committed)** | Every commit P1+ |
| `py -m pytest tests/test_compose_adviser_message.py -v` | P4 |
| Pre-commit grep guard for SMTP recipient-address pattern (R-55-2 reuse) | Every commit |

## Operator approval gates

- **G-56-1a** (P2) — `ADVISER_OPEN_QUESTIONS.csv` tranche.
- **G-56-1b** (P2) — `FOUNDER_FILED_INSTRUMENTS.csv` tranche (only if instruments committed in cycle 1).
- **G-56-1c** (P2) — `GOI_POI_REGISTER.csv` new POI rows (only if previously-unknown participants).
- **G-56-2** (P6, **optional**) — Follow-up send only if I55 loop proposes one while I56 is still open. Routes through I55 L5–L6 pre-flight + IRREVERSIBLE per-fire G-24-3 pattern; **never forced**.

## Decisions seeded (D-IH-56-A..D)

- **D-IH-56-A** — Redaction depth: full anonymization (default) vs partial (operator may relax for low-sensitivity exchanges); SOP-driven default stays full.
- **D-IH-56-B** — Answer-vs-instrument classification: an adviser-supplied draft document = instrument candidate; an adviser-supplied opinion = answered question; ambiguous = both rows + cross-reference.
- **D-IH-56-C** — Second-message timing: operator-clock; no automated "follow up after N days" loop in I56.
- **D-IH-56-D** — PII-leak guard pattern: extend `lint_brand_voice_offline.py` with optional `--pii-guard` mode if cycle-1 surfaces a category not covered by `SOP-HLK_TRANSCRIPT_REDACTION_001` (decision deferred until P7 telemetry).

## Risks

- **R-56-1** — Adviser response includes PII / sensitivities not anticipated by current redaction SOP. Mitigation: extend SOP rather than store raw; redacted commit happens AFTER SOP coverage; if SOP needs extension, P1 pauses and SOP-update PR runs first.
- **R-56-2** — Second outbound triggers unanticipated cost or commitment (e.g., adviser quotes legal fee in response). Mitigation: G-56-2 pre-flight per send; founder-level operator approval per AKOS governance.
- **R-56-3** — Mirror sync drift between cycle-1 commits and Supabase mirror state (race with another tranche). Mitigation: I50 closure leaves drift-clean state; mirror-emit smoke test in pre-commit.
- **R-56-4** — Composer Layer 4 (eloquence) auto-renders jargon that fails offline brand lint. Mitigation: I49 `lint_brand_voice_offline.py` runs in `pre_commit`; second-send blocked if lint fails on rendered fixture.

## Success metrics (per fire; not in this cycle)

- 1 advisor response cycle closed end-to-end: incoming → redacted commit → 4 ADVOPS registers updated → mirror synced → response routed back into I55 loop.
- Redacted transcript committed with **0** raw-PII tokens (validator probes confirm).
- ≥1 question moved from open → answered in `ADVISER_OPEN_QUESTIONS.csv`.
- ≥1 instrument added to `FOUNDER_FILED_INSTRUMENTS.csv` OR explicit decision-log row explaining why none.
- Cycle-1 UAT report cross-references all 4 ADVOPS mirrors with row-count parity.
- I55 loop seamlessly resumes after closure (next regression cycle either proposes a follow-up or doesn't; either is correct).

## What this is NOT

- Building a CRM; cycle-1 is rails-exercise, not tooling expansion.
- Multiple round-trip cycles in I56; subsequent cycles run as I55 L1 (response handling becomes loop-native).
- Replacing operator judgment in advisor conversation (composer always drafts; operator always finalizes).
- Sending automated follow-ups; D-IH-56-C explicitly forbids time-based auto-follow-up.
- A blocking gate on I55's continuous loop; I55 keeps running while I56 elapses.
- Synthesised by AKOS: this initiative ships **zero execution phases** in cycle 1 because the upstream (G-24-3 fire + advisor reply) has not happened. Inventing a fake reply to demonstrate the rails would violate AKOS doctrine ("never invent governed identifiers / never fabricate operator content"). The honest posture is rails-ready, awaiting first reply.
