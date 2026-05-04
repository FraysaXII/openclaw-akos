---
language: en
sop_id: SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001
status: review
role_owner: Brand Manager
co_owners:
  - PMO
  - Business Controller
  - System Owner
area: Marketing
entity: Holistika
program_id: shared
topic_ids:
  - topic_communication_methodology
  - topic_policy_register
artifact_role: canonical
intellectual_kind: methodology_map
related_process_ids:
  - thi_mkt_prj_1
authority: Initiative 55 P6 + Operator reframing 2026-05-03 ("we operate independently from the advisor")
last_review: 2026-05-03
---

# SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001 — Regression-to-advisor continuous loop

**Owner**: Brand Manager (CMO chain).
**Co-owners**: PMO, Business Controller, System Owner.
**Initiative**: 55 P6 (2026-05-03).
**Operator approval gates**:

- **G-55-loop-1** (one-time) — `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` field values + new `update_threshold` policy_class.
- **G-24-3** (per-fire) — Each individual advisor send is its own IRREVERSIBLE gate. May fire 0, 1, or N times across the loop's lifetime.

## 1. Purpose

Codify how Holistika improves brand and operations **independently of advisor cadence** while keeping advisor updates honest, evidence-based, and per-fire reversible-only-by-not-firing.

Per the operator reframing (2026-05-03):

> "We operate independently from the advisor. The advisor is just an advisor; we'll send him the latest regression. … HLK Ops contributes to sending clearer messages to the advisor or any party. I need to know we can keep improving brand and ops while doing regressions to review artifacts so that everything is updated (if relevant; if not, no update)."

The loop is **not** a one-shot send. It is a continuous operating posture in which each regression cycle produces either a send proposal (when artifacts have *materially changed* since the last advisor send) or a no-proposal log row (silence is also signal). The operator decides whether to fire G-24-3 for each individual proposal.

## 2. Scope

In scope:

- Outbound advisor messages (Legal/Fiscal/IP/Banking/Certification/Notary).
- The artifact pack produced by `scripts/render_uat_dossier.py` (snapshot, live, tier-b modes).
- The threshold POLICY (`POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1`) and per-axis tuning.

Out of scope:

- Internal informal chat (uses `casual_internal` register; no SOP discipline beyond brand voice).
- Auto-generated transactional messages (Stripe receipts, Supabase password resets) — those follow product/UX standards.
- Bulk marketing automation — the loop always asks for operator pre-flight before sending.

## 3. The loop (L1–L7)

The numbered steps below mirror the I55 master roadmap continuous-loop section. Any of L2 / L5 / L6 may be skipped on a given cycle.

### L1 — Run the regression

Operator (or schedule) runs:

```
py scripts/render_uat_dossier.py --filter madeira --mode live
```

Mode choice:

- `--mode snapshot` — fast (~10s); reads existing artifacts; offline-safe.
- `--mode live` — runs the 10 CLIs (~5min); requires LLM cost envelope.
- `--mode tier-b` — adds Tier-B paid evals (~15min + USD); opt-in via `AKOS_DOSSIER_TIER_B=1`.

Output: `artifacts/uat-dossier/dossier-<RUN>/{dossier.md,html,pdf,manifest.json,console.html}`. Operator reviews:

- Section 01 three-light verdict (conversational / operator / surface).
- Section 03 + 04 judge axes (brand voice, citation, persona fit) per I52 P6.
- Section 08 endpoint cost surface (RunPod/Kalavai per-GPU-hour) per I52 P5.
- Sections 05 + 07 + 10 (adversarial / drift / open governance debt).

### L2 — Improve brand / ops / registers (optional, any cadence)

Based on Section findings, operator improves any tranche that needs work:

- Brand voice: `BRAND_VOICE_FOUNDATION.md`, `BRAND_REGISTER_MATRIX.md`, `BRAND_DO_DONT.md` (run `scripts/wave2_backfill.py` for Wave-2-driven changes).
- Process list: `process_list.csv` tranches (G-24-2 if I24 P1 SOP).
- GOI/POI register: `GOI_POI_REGISTER.csv` voice profiles (G-24-1 ALTER if schema columns).
- Skill / topic / persona registries: any AKOS-gated path.

All improvements ride normal AKOS gates: `validate_hlk.py`, `release-gate.py`, pre-commit, etc. **No advisor pressure on this step.** Brand and ops keep moving regardless of when (or if) the next send fires.

### L3 — Re-run the regression + diff

Operator (or schedule) runs the regression again, then diffs:

```
py scripts/regression_artifact_diff.py \
    --current  artifacts/uat-dossier/dossier-<NEW>/manifest.json \
    --last-sent artifacts/uat-dossier/last-sent/manifest.json \
    --out diff.json --md diff.md
```

`last-sent` is whatever the operator captured at L6 of the previous cycle (or absent on first cycle). The diff record reports five families of signal:

1. **cite_counts** — Section 02 totals (scenarios, personas, topics, skills, policies).
2. **scenario_deltas** — Section 04 churn (scenarios, outside-tolerance personas, quarantined).
3. **judge_axes** — Sections 03 + 04 per-axis means + fail counts (delta in pp).
4. **endpoint_cost** — Section 08 endpoint count + ceiling status + cost.
5. **brand_voice** — Section 01 three-light flags + ship verdict.

File-level sha256 status (changed / new / removed / unchanged) is also captured.

### L4 — Maybe propose a send

Operator (or schedule) runs:

```
py scripts/propose_advisor_update.py --diff diff.json
```

Behaviour governed by `POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1`:

- If any threshold tripped → emit `proposal-advisor-send-YYYY-MM-DD.md` under `docs/wip/planning/55-brand-ops-continuous-loop/reports/`.
- If no threshold tripped → append a "no" row to `loop-history.md` and exit (D-IH-55-E both-signal-and-silence).
- `--force-proposal` overrides silence (R-55-5 mitigation: thresholds may be too tight).
- `--allow-first-cycle` emits a first-send proposal when no baseline exists.

### L5 — Operator pre-flight (compressed I24 P6)

Operator opens the proposal markdown and works the checklist:

- Review brand voice deltas (Section 01 + Section 03 brand axis).
- Review judge-axis movement (Section 03 + Section 04).
- Review register churn (Section 02 cite-counts + Wave-2 fills).
- Confirm composer renders cleanly: `py scripts/verify.py export_adviser_handoff_smoke`.
- Confirm brand-voice linter green: `py scripts/lint_brand_voice_offline.py`.
- Confirm pre-commit SMTP-pattern grep clean (R-55-2).
- Recipient: GOI/POI `ref_id` only (off-repo identity store; D-IH-55-B).
- Final draft path: from `compose_adviser_message.py`.

If the operator is **not convinced**, the proposal is filed (no fire) and the loop returns to L2. The loop's silence path is fully supported.

### L6 — G-24-3 IRREVERSIBLE SEND (per-fire operator action)

If the operator is convinced:

1. Operator finalises the draft from `compose_adviser_message.py` and presses Send via off-repo SMTP. **AKOS does not send.** The recipient address never enters git (R-55-2; pre-commit grep guard active).
2. **Immediately** after the send, operator captures the real-world fact:

   - Real timestamp (UTC; from the SMTP server's `Date:` header).
   - SMTP manifest (server, sender ref_id, sha256s of the final draft + attachments).
   - Material-change diff snapshot (the `diff.json` from L3 + `proposal-*.md` from L4).

3. Operator writes `reports/uat-adviser-send-N-YYYY-MM-DD.md` (N increments per fire; per D-IH-55-A).
4. Operator copies the L1 dossier `manifest.json` to `artifacts/uat-dossier/last-sent/manifest.json` so the next L3 run has the right baseline.
5. Operator appends a `proposed=YES` row to `loop-history.md` with the proposal filename.

### L7 — Loop returns to L1

There is no fixed cadence. The loop runs whenever the operator runs a regression or whenever a schedule does (e.g., the I51 P5 `eval_tier_b_weekly --hard-fail-on-drift` profile).

## 4. Material-change threshold (POLICY)

`POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1` (`policy_class=update_threshold`; introduced I55 P7) encodes operator-tuned thresholds in `policy_text` as `key=value` tokens:

| Threshold | Default (D-IH-55-D) | Source |
|:----------|--------------------:|:-------|
| `min_changed_scenarios` | 3 | Section 02 + Section 04 `total_scenarios` abs delta |
| `min_judge_axis_movement_pp` | 2 | Max abs delta across `judge_score_*_mean` (×100 to pp) |
| `min_register_rows_added` | 1 | Sum of positive deltas across personas/topics/skills/policies |
| `min_files_changed` | 2 | Count of dossier files with a different sha256 |

Any single threshold being met triggers a proposal (conservative-by-default: motion in any one axis is signal). Operator may tune per-advisor or per-tier in subsequent reviews.

## 5. Telemetry (D-IH-55-E)

`docs/wip/planning/55-brand-ops-continuous-loop/reports/loop-history.md` is the cumulative log. Both signal and silence are recorded so the operator sees both motion and stillness over time:

```
| date | mode | run_id | scenarios_delta | judge_pp | register+ | files_changed | proposed | proposal |
```

If a year of "no" rows accumulates without any "YES", the loop is working as designed (operator independence) but `loop-history.md` makes that visibility explicit (R-55-7 mitigation).

## 6. Failure modes + mitigations

- **R-55-2 — Recipient email leaks into git.** Mitigation: pre-commit grep guard for SMTP recipient pattern; off-repo identity store; SOP cite per `SOP-HLK_TRANSCRIPT_REDACTION_001.md`. The proposal markdown only carries the GOI/POI `ref_id`.
- **R-55-3 — Brand voice authoring slips into invention** (vs. operator-lived). Mitigation: D-IH-17 "we cite operator's lived protocols, not invent"; `wave2_backfill.py` is the only path.
- **R-55-4 — Composer adds language jargon that fails brand lint** at runtime. Mitigation: I49 `lint_brand_voice_offline.py` runs in `pre_commit`; composer tests assert linter green on rendered fixtures.
- **R-55-5 — Threshold too tight** (real improvements never trigger a proposal). Mitigation: per-axis thresholds tunable in POLICY; operator may manually trigger via `--force-proposal`.
- **R-55-6 — Threshold too loose** (advisor gets spammed with non-improvements). Mitigation: G-24-3 is per-fire operator-gated; threshold defaults err on the conservative side; operator review before any send.
- **R-55-7 — Operator improves brand/ops indefinitely without ever sending; advisor relationship cools.** Mitigation: this is a feature (operator independence); `loop-history.md` surfaces "N regressions, 0 sends since YYYY-MM-DD" so it's visible.

## 7. Cross-references

- [`SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](SOP-HLK_COMMUNICATION_METHODOLOGY_001.md) — Four-layer methodology that governs *how* the message is composed (Layer 1 brand foundation → Layer 4 eloquence). This SOP governs *when* it is sent and how the loop continues regardless.
- [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md) — Off-repo identity store and pattern guards for recipient addresses.
- [`scripts/regression_artifact_diff.py`](../../../../../../scripts/regression_artifact_diff.py) — L3 diff implementation.
- [`scripts/propose_advisor_update.py`](../../../../../../scripts/propose_advisor_update.py) — L4 proposal/silence implementation.
- [`scripts/compose_adviser_message.py`](../../../../../../scripts/compose_adviser_message.py) — L5 draft composition (I24 P4).
- [`POL-ADVISOR-UPDATE-MATERIAL-THRESHOLD-V1`](../../../../compliance/dimensions/POLICY_REGISTER.csv) — material-change threshold POLICY (I55 P7).
- [`I55 master-roadmap.md`](../../../../../wip/planning/55-brand-ops-continuous-loop/master-roadmap.md) — full phase + loop spec.
- [`I24 master-roadmap.md`](../../../../../wip/planning/24-hlk-communication-methodology/master-roadmap.md) — capability lineage that the loop closes.

## 8. What this is NOT

- An automated send. G-24-3 is per-fire IRREVERSIBLE; AKOS never inlines a recipient address.
- A blocking dependency between brand/ops improvement and advisor cadence (decoupled by design; the loop's silence path is fully supported).
- A guarantee of material improvement. The threshold detects motion, not virtue. The operator's pre-flight is what protects quality.
- A one-shot send + close. The loop is the deliverable; closure is per-fire (each `uat-adviser-send-N-*.md`), not per-initiative.
