---
language: en
status: active
initiative: 55-brand-ops-continuous-loop
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 55 — Decision log

Six decisions seeded; operator-ratified at I50-I56 master-roadmap session 2026-05-03 ("we operate independently from the advisor … keep improving brand and ops while doing regressions").

## D-IH-55-A — Pre-flight checklist authoritative location

**Decision:** Per-fire pre-flight checklist lives in I55 `reports/uat-adviser-send-N-YYYY-MM-DD.md` (N increments). Cumulative log in `reports/loop-history.md` records every regression cycle (proposal or no-proposal) so the loop shows both signal and silence.

**Rationale:** The I24 P6 pre-flight template exists; rather than fork it, I55 reuses the per-fire pattern with N-incrementing reports — each fire is its own UAT closure. The cumulative `loop-history.md` is what makes the loop's *velocity* visible (D-IH-55-E + R-55-7).

---

## D-IH-55-B — SMTP send path: off-repo identity store

**Decision:** Recipient email address **never enters git**. Pre-commit grep guard for SMTP-recipient pattern. Off-repo identity store (operator's personal email client / address book).

**Rationale:** R-55-2 mitigation. PII in git is a hard incident; the cost of preventing it is one regex. SOP cite per `SOP-HLK_TRANSCRIPT_REDACTION_001`.

---

## D-IH-55-C — I24 vs I55 folder split

**Decision:** I24 stays Closed at capability landing (P8). I55 stays **Open as continuous loop** (D-IH-55-F). Both linked via cross-references.

**Rationale:** I24's deliverables are *capabilities* (composer, brand foundation, GOI/POI ALTER, register schema). Once those exist, I24's mission is complete. The *operating loop* (regression → review → improve → maybe-send) is a different shape — it's a continuously running process, not a project. Splitting them keeps the planning README readable and the open-vs-closed signal honest.

---

## D-IH-55-D — Material-change threshold default values

**Decision (default values):**
- `min_changed_scenarios ≥ 3` (at least 3 PERSONA_SCENARIO rows must move).
- `min_judge_axis_movement_pp ≥ 2` (at least one judge axis must shift ≥2 percentage points up).
- `min_register_rows_added ≥ 1` (at least one canonical-register row added or materially edited since last send).

**Rationale:** Conservative defaults trade off R-55-5 (too tight: never triggers; advisor never updated) vs R-55-6 (too loose: spam). The bias is toward "tight" because G-24-3 is IRREVERSIBLE per fire; the operator can always force a proposal via `propose_advisor_update.py --force-proposal`. Field values can be tuned per-advisor or per-tier (POLICY-row edit, not code edit).

**Reversibility:** High — POLICY row edit + decision-log update.

---

## D-IH-55-E — Loop telemetry

**Decision:** Every G-24-3 fire writes a `reports/uat-adviser-send-N-YYYY-MM-DD.md`. Every regression cycle that **does not** trigger a proposal also logs to `reports/loop-history.md` (one-line entry: timestamp + diff summary + reason for no-proposal). The operator sees both signal and silence.

**Rationale:** R-55-7 mitigation. If the loop runs 12 times in 90 days with 0 sends, that's a visible metric ("N regressions, 0 sends since YYYY-MM-DD") that surfaces "operator independence is working" or "advisor relationship cooling" depending on the operator's read. Without telemetry of the silence, the operator only sees fires.

---

## D-IH-55-F — Closure of I55 itself

**Decision:** **No fixed end date.** Revisit closure trigger only if doctrine changes (e.g., advisor relationship ends; communication methodology rewritten; operator decides loop is no longer worth running).

**Rationale:** This is the heart of the operator's reframing — the loop is the deliverable, not a one-time send. I55 stays Open as a tracked initiative with a continuous-loop status; it never auto-closes.

---

## Decisions made during execution

### P6 (2026-05-03) — Tooling shape decisions

- **Diff record schema_version=1**, with five families (`cite_counts`, `scenario_deltas`, `judge_axes`, `endpoint_cost`, `brand_voice`) plus per-file sha256 status. Status vocabulary: `unchanged` / `changed` / `new` / `removed`. Numeric `delta` carried on `int|float` pairs only. Locked in tests.
- **Section 03 + 04 merged for judge-axis diff** with Section 04 winning on overlap (`{**s03, **s04}`). Rationale: Section 04 (Persona library + calibration) carries the per-persona judge means in the I52 P6 dossier surface; Section 03 (Eval health) is currently a placeholder for many runs. Both are read so a future re-introduction of Section 03 means doesn't require re-coding the diff.
- **First-cycle handling = silence by default; `--allow-first-cycle` opts in.** When the very first regression has no `last-sent` baseline, the diff record is generated but `propose_advisor_update.py` does not auto-propose. The operator must explicitly opt in to a first-send proposal via `--allow-first-cycle`. Symmetric with the silence-is-also-signal D-IH-55-E posture: the first cycle is the prototypical silence row in `loop-history.md`.
- **`min_files_changed=2` added to the threshold POLICY's default token set** (D-IH-55-D defaults extended). Rationale: when no other axis moves but multiple dossier files have new sha256s, that is itself a material change worth a proposal review (e.g. major dossier-section refactor, brand-voice template overhaul). The operator can suppress by setting `min_files_changed=999` if undesired.
- **SOP `status: review`** without a new `process_list.csv` row, because the SOP introduces no new `process_id` of its own — it codifies the loop *around* the existing `thi_mkt_prj_1` "Communication methodology" tranche. The named sub-tranche `thi_mkt_dtp_NN` for "Communication methodology maintenance" is still operator-pending (G-24-2 / OPS-55-1) and is referenced by the SOP, not invented inside it.

### P7 (2026-05-03) — Threshold POLICY shape decisions

- **`G-55-loop-1` FIRED** — operator-pre-registered gate in master-roadmap; no separate operator email round-trip needed because (a) the policy_class enum extension is mechanical, (b) the field values match the conservative D-IH-55-D defaults, and (c) the row is reversible by editing `policy_text` + bumping `last_review`. If operator wants different field values they edit the row.
- **`policy_class=update_threshold` as a new value, not an extension of `cost_ceiling`** — separating "how much spend before halting" (USD/run unit) from "how much change before proposing" (count-of-rows unit) keeps cost-ceiling alarms (I52 P5 G-52-4) from misfiring on advisor-loop telemetry, and follows the D-IH-52-E generalisation that mixed-unit ceilings are a category error.
- **Owner = Brand Manager** for the threshold POLICY. Co-owners on the loop SOP cover Business Controller (cost discipline of regression cycles) + System Owner (CI integration), but the *authoritative* owner of the threshold values is Brand because the threshold governs *when* an advisor message is proposed, which is brand/comms territory.
- **Tests lock the contract**: `test_seed_includes_i55_advisor_update_threshold` asserts both POLICY-row presence AND parser extraction. If either side drifts in isolation, CI fails fast. Same posture as I47 P12 / I50 P2 / I51 P4 contract-locks for their respective POLICY rows.
- **`min_files_changed=2` is in the POLICY row** despite not being in the original D-IH-55-D enumeration. Rationale documented in P6 decisions; the POLICY row is the canonical source. If operator wants a 3-axis-only threshold, they set `min_files_changed=999`.

---

## D-IH-55-G — Wave-2 brand voice traits operator-confirmed as canonical

**Decision (2026-05-04):** The Wave-2 `brand_voice.voice_is` and `brand_voice.voice_is_not` traits in [operator-answers-wave2.yaml](../22a-i22-post-closure-followups/operator-answers-wave2.yaml) — agent-derived from the operator-supplied narrative pillars (Structure that scales / Plain words / Evidence over assertion) — are accepted as canonical without further refinement. YAML inline comments updated from "operator review and refinement" to "operator-confirmed 2026-05-04 (D-IH-55-G)".

**Rationale:** The agent-derived traits faithfully extend the operator's supplied charter ("rigorous peer who removes uncertainty without performing expertise") and the three narrative pillars. Six weeks of dossier rendering against the existing [BRAND_VOICE_FOUNDATION.md](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md) (status: active since 2026-04-29) have not surfaced register conflicts. Continuing to mark them "pending operator review" understates the actual operator posture and blocks Wave-2 backfill validation paths from showing READY.

**Reversibility:** High — the YAML comment is documentation-only; trait edits remain a single-PR change against this file with a corresponding decision-log update. `BRAND_VOICE_FOUNDATION.md` is not affected by this decision.

**Cross-references:** rule [akos-planning-traceability.mdc](../../../../.cursor/rules/akos-planning-traceability.mdc) § Decision log; closes the Wave-2 voice-content cluster on the loop history (see master-roadmap).

---

## D-IH-55-H — First dry-run regression cycle establishes baseline manifest

**Decision (2026-05-04):** The dossier rendered at `artifacts/uat-dossier/uat-dossier-20260504T174458Z/` (filter=`madeira`, mode=`snapshot`, format=`all`) is recorded as the **baseline `manifest.json`** for future `regression_artifact_diff.py --last-sent <…>` invocations. The first-cycle `is_first_cycle: true` outcome is exactly the prototypical silence row contemplated by D-IH-55-E and the P6 first-cycle handling decision; `propose_advisor_update.py` correctly engaged the threshold parser, surfaced `should_propose: true` due to `min_files_changed=4` ≥ 2, and held the proposal in dry-run mode (no `proposal-advisor-send-2026-05-04.md` written).

**Rationale:** The loop's value proposition only materializes when a `--last-sent` baseline exists; until then every cycle is a "first cycle" and the threshold logic engages on file-count alone. This dry-run produces the very first baseline candidate, unblocking the next cycle from starting against meaningful deltas. **The decision is purely operational** — no POLICY values or code change.

**Reversibility:** High — re-running the dossier render at any point produces a new candidate baseline; the operator chooses which manifest is "last-sent" by passing it to `--last-sent` on the next diff invocation. The first-cycle threshold tuning candidate (raise `min_files_changed` to 999, or add `is_first_cycle` gating in `evaluate_thresholds`) is documented in the UAT report and deferred until at least one real-baseline cycle has run.

**Cross-references:** [reports/uat-i55-dry-run-regression-cycle-20260504.md](reports/uat-i55-dry-run-regression-cycle-20260504.md) (the full evidence); D-IH-55-D (threshold defaults); D-IH-55-E (silence-is-also-signal telemetry); P6 + P7 closure reports for the underlying tooling.

