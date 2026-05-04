---
language: en
status: active
initiative: 57-cycle-closeout-live-validation
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-04
---

# Initiative 57 — Decision log

Seven decisions seeded; operator-ratified at the I57 master-roadmap greenlight session 2026-05-04. D-IH-57-A and D-IH-57-B were resolved interactively at plan-time (`AskQuestion`); the remaining five are policy decisions that govern P1 through P6 execution.

## D-IH-57-A — Initiative model: single coordinating I57 vs distributed close-out

**Decision:** **Single coordinating Initiative 57.** All four buckets land under one master-roadmap with one closure UAT.

**Alternatives considered:**

- *Thin I57 for the live-cycle window only* + close-out work in existing I32 + I45 folders + new OPS-* register entries for Buckets 2 and 4. (Lighter-weight; rejected because it scattered the closure decision across three folders.)
- *No new initiative* — just register OPS-* entries and append phases to the existing I22a + I32 + I45 + I54 folders. (Rejected for the same reason; loses the through-line that ties Bucket 4 quick wins to Bucket 1 live cycle to Bucket 2 content fills.)

**Rationale:** The four buckets are sequenced by leverage: P1 quick wins remove friction for P2 (mirror cycle); P2 + P3 closures unlock P4 (live dossier reads from `compliance.eval_run` which I45 P4 shipped); P5 is parallel-tracked operator-content that closes I55 + I24 dependencies. One folder, one master-roadmap, one closure decision log.

**Reversibility:** High at planning time, low after P1 commits land — the through-line becomes load-bearing for the closure UAT.

---

## D-IH-57-B — Live cycle batching: single AKOS_RECORD_LIVE window

**Decision:** **Single window batching all three OPS items** (OPS-52-1 multi-judge calibration burn + OPS-50-1/51-1 persona cassettes + OPS-53-1 GraphRAG A/B); ~$30-50 sitting under `MAX_DOSSIER_USD=50`.

**Alternatives considered:**

- *Two windows by risk profile* — first a low-risk burn (OPS-52-1 + persona cassettes ~$10), then a higher-risk GraphRAG A/B (~$10-20) as a separate window. Rejected because the two have no shared dependency that benefits from sequencing; the operator-overhead of a second sitting outweighs the marginal risk reduction.
- *Three independent windows scheduled separately.* Rejected for the same reason multiplied.

**Rationale:** All three OPS items share the same upstream prerequisites (`AKOS_RECORD_LIVE=1`, Supabase service-role key, provider API keys). Running them in one window amortizes the operator setup cost and produces a single live `--filter madeira` dossier emit at the end (P4 (d)) that references all three sources of new data simultaneously.

**Reversibility:** High — if mid-flight cost crosses the abort threshold ($40 per D-IH-57-G), `endpoint_envelope_alarm.py` halts execution and partial outcomes are recorded. Remaining sub-steps re-forward to a future window.

---

## D-IH-57-C — P1 commit granularity: one commit per fix vs one bundled commit

**Decision:** **Recommend one commit per fix.** Four P1 commits: (1) F-22a-EMIT-1 DATE NULL coercion + regression test; (2) F-22a-EMIT-2 NOT NULL bool default + regression test; (3) OPS-54-1.a color-contrast CSS; (4) OPS-54-1.b tabindex on `#handoff-example`. Revisit at P1 execution if any two fixes are tightly coupled.

**Rationale:** Bisectability. The four fixes touch three different file surfaces (one Python script + two CSS/DOM hunks in `static/madeira_control.html`) and have independent regression tests. Bisecting is faster when each commit is single-concern; the alternative (one bundled commit) saves only one commit-overhead in exchange for losing per-fix `git revert` granularity.

**Exception:** OPS-54-1.a (CSS) and OPS-54-1.b (DOM) both edit `static/madeira_control.html`. If they touch overlapping lines, ship as one a11y commit with a combined message; otherwise stay separate.

**Reversibility:** High — `git revert` per commit.

---

## D-IH-57-D — Wave-2 Section 3 content authority

**Decision:** **Operator-only per D-IH-17.** Agent may not synthesise GOI/POI voice profiles even when given strong prior signal (e.g., adviser correspondence excerpts, brand voice foundation).

**Rationale:** D-IH-17 forbids fabrication of governed identifiers and operator-content. Section 3 of [`operator-answers-wave2.yaml`](../22a-i22-post-closure-followups/operator-answers-wave2.yaml) carries six GOI/POI voice profiles that drive `compose_adviser_message.py` Layer 4 eloquence rendering and feed `BRAND_REGISTER_MATRIX.md`. Wrong content here propagates into outbound advisor messages — a high-blast-radius surface where invention is unacceptable.

**Engineering ships:** the validation gate (`wave2_backfill.py --check-only` returns zero pending leaves), not the keystrokes.

**Reversibility:** N/A (the decision *is* the boundary).

---

## D-IH-57-E — GraphRAG ship verdict policy

**Decision:** **Re-affirm [D-IH-46-E](../46-neo4j-strategic-posture/decision-log.md) non-additive bar and [D-IH-53-C](../53-graphrag-poc-closure/decision-log.md) no-partial-credit.** If P4 (c) hits any single bar by **≥3pp** accuracy lift OR **≥30%** latency reduction OR **≥40%** cost reduction, **GO**; otherwise **NO-SHIP** and OPS-53-1 forwards. No mid-bar negotiation.

**Rationale:** The non-additive trade-off was deliberately set high in I46 P5 to prevent ship-by-attrition. A 1pp accuracy lift + 10% latency reduction + 10% cost reduction is *not* a marginal-credit ship; it's a NO-SHIP that fails three bars by similar margins. The bar exists because GraphRAG carries operational complexity (Neo4j Aura SLA, embedding pipeline, drift canary) and only one of the three benefits at the documented magnitude justifies that complexity.

**Reversibility:** Medium — re-running the A/B against a different golden set or a tuned retrieval prompt is allowed, but constitutes a new OPS-53-N event with its own pre-flight cost estimate and decision-log entry.

---

## D-IH-57-F — Multi-judge calibration alignment minimum

**Decision:** **`POL-EVAL-JUDGE-THRESHOLD-{BRAND-VOICE,CITATION,PERSONA-FIT}-V1` rows stay at `min_pass_score=4`.** Gate re-arms on first <80% alignment event from the OPS-52-1 burn. If alignment <80%, recalibration cycle runs against the burn data; new POLICY versions land via the standard tranche pattern.

**Rationale:** I52 P3 set the dispatcher-validation alignment at 100%/100%/100% in offline-fallback mode; the live OPS-52-1 burn is the first real-world test of the consensus dispatcher. <80% alignment indicates judge models disagree more than expected, which is operationally meaningful (suggests prompt tuning or roster rotation) but not a blocker — the existing single-judge fallback covers production.

**Reversibility:** High — POLICY rows are git-canonical and version-bumped per recalibration.

---

## D-IH-57-G — Cost ceiling envelope for the live cycle

**Decision:** **`MAX_DOSSIER_USD=50` hard ceiling, `endpoint_envelope_alarm.py` abort at $40, kill switch wired to halt P4 execution mid-flight.** Per the I52 P5 cost discipline + I50 P2 prices truth-up.

**Rationale:** Pre-flight cost estimates: OPS-52-1 multi-judge burn ~$5; OPS-50-1/51-1 cassette population ~$5; OPS-53-1 GraphRAG A/B ~$10-15 (per I53 P1 estimate); live dossier emit ~$1-5. Total expected ~$25-30 under the $50 ceiling; $40 abort gives ~$10 buffer for Tier-B token-rate drift and surprise re-runs. The ceiling matches the I46 P5 R-46-1 $20 envelope * 2.5 (3 OPS items vs 1).

**Operator surfaces:** abort threshold is wired into `endpoint_envelope_alarm.py` (I52 P5); kill switch surfaces as the existing `MAX_DOSSIER_USD` env-var on `render_uat_dossier.py`. Both pre-existing; this decision sets the values.

**Reversibility:** High — operator can re-fire with a higher envelope if the first sitting hits $40 mid-OPS-53-1; logged as a separate decision event.

---

## Decisions made during execution

### P0 (2026-05-04) — Cycle-1 scope discipline

- **AKOS ships P0 + P1 + P2 + P3 + P6 in cycle 1; P4 forwards as OPS-57-1; P5 forwards as OPS-57-2.** Mirrors the I54 / I55 / I56 stub-mode-then-OPS-* pattern. The honest cycle-1 closure is "engineering closeout shipped; live validation + Wave-2 content forwarded".
- **Folder name is `57-cycle-closeout-live-validation/`** (matches the `CreatePlan` artifact name). Earlier shorthand `57-post-i56-followthrough/` was discarded because "live validation" is the headline new thing this initiative shipped (the OPS-57-1 forward) and "cycle closeout" is the engineering work.
- **No new scripts in I57** at the bootstrap level. P1 modifies existing scripts + statics; P2 + P3 + P6 use existing verification matrix entries; P4 (operator-side) calls existing scripts under `AKOS_RECORD_LIVE=1`. Per the master-roadmap "asset classification → no new scripts" the four ADVOPS register validators (from I21), the eval harness CLI (from I45), the GraphRAG PoC script (from I46/I53), the dossier renderer (from I48), and the WIP_DASHBOARD renderer (from I32 P10) cover P1 through P6 in their entirety.
- **I57 stays Open until P6 fires** even though P4 + P5 are forwarded. The README row records `Open` so the WIP_DASHBOARD reflects the in-flight engineering work; once P6 closes, the row flips to `Closed (engineering side); OPS-57-1 + OPS-57-2 forwarded`.
- **Cross-references explicit** — I22a (post-closure follow-ups, F-22a-EMIT-1/2 origin), I32 (Holistik Ops Maturation, P3 closure target), I45 (Live Eval Harness, P2 closure target), I46 + I53 (GraphRAG ship-bar; P4 (c) decision-log target), I52 (multi-judge dispatcher; P4 (a) source), I54 (a11y; OPS-54-1.a/b origin), I55 (continuous loop; OPS-57-2 closes the I55 P1-P5 content cluster), I56 (rails; unchanged by I57). The asset classification table cites all of these in the canonical column.
