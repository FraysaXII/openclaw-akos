---
language: en
status: active
initiative: 58-cycle-2-multi-track-forward
report_kind: decision-log
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-06
---

# Initiative 58 — Decision log

Eight decisions seeded; operator-ratified at the I58 master-roadmap greenlight session 2026-05-05 via `AskQuestion` (D-IH-58-D explicitly chose "sequential"; D-IH-58-A through H were authored under operator delegation "decide the operator dependencies for me; if you see something you really need, ask"). The decisions below govern P0 → E.0 execution.

## D-IH-58-A — Coordinating-initiative model: single I58 vs distributed close-out

**Decision:** **Single coordinating Initiative 58.** All five tracks (A live cycle + B strategy + C KM + D hygiene + E closure) land under one master-roadmap with one closure UAT.

**Alternatives considered:**

- *Split into I58 (Phase A only, operator-funded) + I59 (Phases B+C+D+E, agent-driven).* Rejected because creating a new initiative folder for "fire one sitting" is overkill given the I57 stub-mode-then-OPS-* precedent already handles operator-funded forward cleanly.
- *Wait for Phase A to fire before closing I58.* Rejected because it makes engineering closure hostage to operator scheduling on the live cycle; violates the principle "engineering closure is independent of operator funding".
- *Distributed close-out: drive each of I28/I29/I30/I31 to closure on its own cadence with no coordinating folder.* Rejected because it scatters the closure decision across four folders and loses the through-line that ties Track A live cycle to Track B strategy completion.

**Rationale:** The I57 precedent demonstrated that a coordinating folder with one closure UAT works at scale (six engineering phases + one operator forward + three master-roadmap status flips). I58 inherits the pattern with one extra track (D explicit hygiene) and follows the same "engineering closes; OPS-* forwards if not fired" semantics.

**Reversibility:** High at planning time, low after P0 commits land — the through-line becomes load-bearing for the closure UAT.

---

## D-IH-58-B — OPS-57-1 fires inside I58 Phase A (not detached)

**Decision:** **OPS-57-1 fires inside Phase A of I58**, not as a parallel detached cycle. If it fires, its outcomes feed directly into E.0 closure UAT. If it does not fire by E.0, it re-forwards as **OPS-58-1** with the OPS-57-1 runbook verbatim.

**Alternatives considered:**

- *Keep OPS-57-1 detached and let I58 close on engineering tracks only.* Rejected because the live cycle is the highest-leverage operator action this cycle; coupling it inside I58's coordinating envelope makes the "what's the next operator window" question concrete (it's G-58-1).
- *Force I58 to wait for OPS-57-1.* Rejected per D-IH-58-A reasoning (engineering ≠ operator funding).

**Rationale:** Phase A.0 (`scripts/preflight_g58_1.py`) gives the operator a one-command "am I ready" check. If the env is loaded, the agent re-evaluates G-58-1 and drives A.1 → A.4. If not, Phase A stays a forwarded gate without blocking Phase B/C/D/E.

**Reversibility:** High — operator can fire OPS-58-1 at any time after I58 closure with the unchanged runbook.

---

## D-IH-58-C — GraphRAG NO-SHIP is a closure event, not a failure

**Decision:** **NO-SHIP at A.3 is a valid closure event.** I46 P5 (`SKILL-MADEIRA-LOOKUP-V1.retrieval_mode` flip + `POL-NEO4J-GRAPH-RAG-ELIGIBILITY-V1` row) stays deferred under NO-SHIP; I58 still closes. Re-affirms [D-IH-46-E](../46-neo4j-strategic-posture/decision-log.md#d-ih-46-e) non-additive bar and [D-IH-53-C](../53-graphrag-poc-closure/decision-log.md#d-ih-53-c) no-partial-credit.

**Verdict thresholds (re-affirmed from D-IH-46-E):**

- **GO** = ≥3pp accuracy lift OR ≥30% latency reduction OR ≥40% cost reduction (any single bar).
- **NO-SHIP** = none of the three bars hit at the documented magnitude.

**Rationale:** The non-additive bar was deliberately set high in I46 P5 to prevent ship-by-attrition. NO-SHIP is the documented expected outcome under D-IH-53-C operator framing; treating it as a "fail" of I58 would create pressure to negotiate the bar mid-flight, which D-IH-46-E explicitly forbids.

**Reversibility:** Medium — re-running A/B against a different golden set or tuned retrieval prompt is allowed but constitutes a new OPS-53-N event with its own pre-flight cost estimate and decision-log entry.

---

## D-IH-58-D — Strategy track sequencing: B.1 → B.2 → B.3 → B.4

**Decision:** **Sequential `B.1 → B.2 → B.3 → B.4`.** Operator-confirmed at greenlight 2026-05-05 via `AskQuestion`. Estimated ~20–25h serial across multiple sittings; low merge risk.

**Alternatives considered:**

- *Parallel pairs (I28+I29, then I30+I31).* Rejected — operator preferred low merge risk over speed.
- *Fully parallel (all four at once).* Rejected — highest merge risk; needs strict per-phase commit isolation that strategy track content work doesn't guarantee.

**Rationale:** Strategy initiatives have content drift between phases (I28 outputs feed I29 P4 strategy SSOT; I30 deck restructure consumes I29 strategy artifacts; I31 doctrine references I30 governance moat metrics). Sequential ordering matches the natural data flow.

**Order rationale:**

1. **I28 first** — investor-style dossier is the primary external send; foundation for I29's deck wiring.
2. **I29 second** — Multi-phase consolidation finishes Impeccable + Business Strategy SSOT scaffolds + deck wiring; depends on I28 deck shape.
3. **I30 third** — Deck moat surgery consumes I29 strategy artifacts (`MADEIRA_PLATFORM.md`, `GOVERNANCE_MOAT.md`, joint-equity Channel 6).
4. **I31 fourth** — Holistik Ops Discovery 6-axis doctrine references I30 governance moat metrics in the `HOLISTIK_OPS_DISCOVERY.md` body; founder ratification (G-58-3) is the final operator gate before E.0.

**Reversibility:** Medium — if a downstream initiative reveals a defect in an upstream one, the upstream stays Closed and the downstream files a follow-up under its own decision-log.

---

## D-IH-58-E — I31 ships 6-axis Holistik Ops doctrine (not 5-axis)

**Decision:** **Phase B.4 finalizes the 6-axis Holistik Ops doctrine** per [`HOLISTIK_OPS_DISCOVERY.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md), not the original 5-axis framing. The 6-axis upgrade was already established in the always-applied AKOS mirror template rule (`.cursor/rules/akos-mirror-template.mdc` references "the 6-axis Holistik Ops doctrine").

**Original 5-axis framing (deprecated):** Persona × Channel × Distance × Language × Artifact-class.

**6-axis upgrade (current canonical):** Persona × Channel × Distance × Language × Artifact-class × Topic.

**Rationale:** Topic was promoted to a first-class axis in I32 P10 (Holistik Ops Maturation). I31 was authored before that promotion landed and still references 5-axis. Closing I31 in I58 means finalizing the doctrine document with the 6-axis shape that matches the rest of the canonical surface (TOPIC_REGISTRY, KM Topic-Fact-Source, the always-applied rule).

**Reversibility:** High — the doctrine document is a single MD file under v3.0/; updating from 5-axis to 6-axis is one section + one diagram regeneration.

---

## D-IH-58-F — `~/.openclaw/.env` enrichment is operator-driven (D-IH-17 invariance)

**Decision:** **Agent writes structure (Supabase URL, alias-seam stubs, commented Phase A flags) in P0; operator pastes secret values.** Mirrors D-IH-17 invariance ("never invent governed identifiers locally"; secret values are governance-equivalent). Agent never authors `OPENAI_API_KEY=sk-...` or similar.

**Rationale:** Per `.cursor/rules/akos-mirror-template.mdc` and `.cursor/rules/akos-governance-remediation.mdc` SOC discipline ("No secret keys or Vault material in git"). Even though `~/.openclaw/.env` is gitignored, the agent's authoring posture should be the same: no fabrication of secret values. Empty placeholders + comments make the operator's paste workflow trivial without ever putting the agent in a position where it could invent a key.

**Operator workflow:**

1. P0 writes the structure (empty `OPENAI_API_KEY=`, `ANTHROPIC_API_KEY=`, etc., plus `SUPABASE_URL=...` literal value, plus commented Phase A flags).
2. Operator pastes secret values into the empty placeholders.
3. Operator uncomments Phase A flags only at the start of an OPS-58-1 sitting (recommended: export in shell rather than persist).

**Reversibility:** N/A — this is a doctrine boundary.

---

## D-IH-58-G — RunPod/Kalavai env-var alias seam (no rename)

**Decision:** **Keep `VLLM_RUNPOD_URL` + `VLLM_SHADOW_URL` as canonical names; introduce read-aliases `RUNPOD_ENDPOINT_URL` and `KALAVAI_ENDPOINT_URL` in `akos/runpod_provider.py` so I57-era doc references stay live.** `VLLM_*` wins precedence when both set; alias is fallback. Drop nothing.

**Why an alias seam vs a rename:**

- I57's `p4-live-cycle-forward-2026-05-04.md` and `ops-57-1-env-recheck-2026-05-04.md` use `RUNPOD_ENDPOINT_URL` / `KALAVAI_ENDPOINT_URL`.
- `config/environments/dev-local.env.example` and the runtime use `VLLM_RUNPOD_URL` / `VLLM_SHADOW_URL`.
- Renaming either side breaks one doc surface or one runtime surface.
- An alias seam in `akos/runpod_provider.py` (the single read point) makes both names resolve to the same underlying URL, with `VLLM_*` winning precedence to preserve runtime semantics.

**Test contract (D.2):** +1 unit test in `tests/test_runpod_provider.py` asserts both names resolve to the same URL when set; asserts deterministic precedence (`VLLM_*` wins).

**Reversibility:** High — single-line revert in `akos/runpod_provider.py` if the alias inverts precedence and breaks production gateway.

---

## D-IH-58-H — I05 + I20 archive (not deletion)

**Decision:** **Minimal `master-roadmap.md` with `status: archived`** for both `05-hlk-vault-envoy-repos` and `20-kalavai-shadow-llamacpp-trial`. One-paragraph history reason in each. Folders kept (preserves git history of intent).

**Alternatives considered:**

- *Delete folders.* Rejected — git history of original intent (Envoy Tech Lab repo registry alignment in I05; Kalavai trial endpoint in I20) is operationally useful for future repo-history queries.
- *Leave as `status: unknown` (current state).* Rejected — `WIP_DASHBOARD.md` showing `unknown` is dashboard hygiene debt that compounds.

**Rationale:** Both initiatives served their purpose at the time (I05 was the early Envoy repo registry alignment exercise; I20 was the Kalavai DeepSeek-R1-Distill-Llama-70B trial). Their content has been superseded by I22 (HLK scalability) and the production VLLM_SHADOW_URL respectively. An `archived` marker captures "this work happened, was useful, and is no longer the active surface" without losing the trail.

**Reversibility:** High — un-archiving is one frontmatter edit if either folder needs to be re-activated.

---

## D-IH-58-I — Wire `_call_member_via_api` and pivot roster to all-Anthropic (OPS-58-1)

**Decision:** During OPS-58-1 execution (2026-05-06), wire the live multi-judge API path that I52 P3 had left as a `NotImplementedError` stub, and pivot the roster from `anthropic:claude-3-5-sonnet-20241022 + openai:gpt-4o` to `anthropic:claude-sonnet-4-5 + anthropic:claude-haiku-4-5` for the live calibration burn.

**Why this was the missing piece (vs. what `D-IH-58-F` covers):**

- `D-IH-58-F` governed env / secret authoring posture (operator pastes secret values; agent never fabricates). It did **not** describe the actual transport plumbing.
- `akos.eval_harness.judge._call_member_via_api` was a deliberate placeholder from I52 P3 ("activated in P3 follow-up commit"). The follow-up never landed because every prior cycle deferred OPS-* live operator action.
- Without the wiring, OPS-58-1 A.1 / A.2 / A.4 could never produce live evidence — every roster member would fall through the exception path with `NotImplementedError`, the calibration burn banner would say "no API credentials" (incorrectly), and the operator would have no way to tell whether the obstacle was env, code, or both.

**Wiring shape (DI-clean; reuse-only):**

- Provider dispatch (`anthropic:*` → Anthropic SDK; `openai:*` → OpenAI SDK; raise on other prefixes).
- System prompt loaded from `prompts/judge/JUDGE_PROMPT_V1.md` (front-matter stripped); user message is the JSON payload the prompt mandates.
- Test seam: `_anthropic_client_factory` / `_openai_client_factory` module globals that tests monkey-patch with stub callables — no real network in tests.
- Cost tracking via `_JUDGE_PRICING_USD_PER_MTOK` table (USD per 1M tokens). Unknown models raise so an operator never silently overspends a roster expansion.
- Strict JSON output parsing (axis ∈ [1,5]; missing axis raises). Tolerates a `` ```json … ``` `` fence even though the prompt forbids it.
- On parse / transport failure, raise so `_default_member_scorer`'s exception fallback attributes `fallback-offline-api-error` to the result.

**Roster pivot — best-effort under operator's "go all out" directive:**

- Probed available models on the new operator credentials. **Anthropic** account serves `claude-sonnet-4-5` + `claude-haiku-4-5`; legacy `claude-3-5-sonnet-20241022` returns 404 not_found. **OpenAI** account returned 401 (key rejected; either rotated, expired, or a placeholder).
- Decision: pivot roster to `anthropic:claude-sonnet-4-5,anthropic:claude-haiku-4-5` (flagship + cheap-tier) rather than block A.1 on operator OpenAI rotation. This actually **strengthens** the burn because it informs `D-IH-52-B` cost-aware tiered escalation (sonnet flagship + haiku cheap-tier from the same family is cleaner data than sonnet + gpt-4o from different families). The OpenAI auth failure is forwarded as `OPS-58-2` (key rotation) — non-blocking, single-step operator action.

**Banner discrimination (companion fix):**

- `JudgeRoster.score()` now appends `fallback-reasons:<csv>` to its `notes` string (extracted from `MemberScore.notes` axis-suffixes: `no-api-key` / `no-live-api-flag` / `api-error`).
- `judge_calibration_burn.py` parses this and prints a discriminating banner ("Reasons observed: …") instead of the generic "no API credentials present or AKOS_JUDGE_LIVE_API unset" message.
- Adds `live_total_cost_usd` to the JSON sidecar so the operator can verify the per-burn spend without parsing per-scenario logs.

**Verification (mocked-SDK seam; no network):**

- 17 new tests in `tests/test_judge_live_api.py` covering provider dispatch, payload shape, prompt loading, cost computation, JSON parsing, fence tolerance, schema-violation rejection, fallback-reason surfacing.
- Updated 1 pre-existing test in `tests/test_eval_judge_multi.py` whose assertion was tied to the old `NotImplementedError` stub.
- Targeted regression: 154 / 154 passed across `tests/test_judge_live_api.py`, `test_eval_judge.py`, `test_eval_judge_multi.py`, `test_i52_p7_tier_b_multi_judge_endpoint.py`, `test_dossier_judge_axes_endpoint.py`, `test_preflight_g58_1.py`, `test_runpod_provider.py`.

**Live evidence produced (A.1 + A.2 burn):**

- A.1 OPERATOR n=50 → brand_voice=100% / citation=96% / persona_fit=0% / overall=65.3% (FAIL vs 80% target).
- A.2 PERSONA-INVESTOR-COLD n=35 → brand_voice=100% / citation=100% / persona_fit≈5.7% / overall=68.6% (FAIL).
- Pattern is uniform across both personas: roster scores `5` on persona_fit, offline rubric scores `3`. This is a **rubric calibration gap** (the offline `_heuristic_persona_fit` defaults to a conservative 3 when `persona=None` is passed by the burn harness) — **not** a judge disagreement. Real signal that justifies the wiring.
- Burn cost stayed well under the per-run $5 envelope (Anthropic-only roster; sonnet + haiku token mix).

**Reversibility:** High — `_call_member_via_api` reverts to the placeholder `raise NotImplementedError(...)` body if the wiring needs to be unwound; the test seam (`_anthropic_client_factory` / `_openai_client_factory`) is idempotent with default `None`. Reverting would re-block OPS-58-1 cleanly without breaking offline-tier code paths.

---

## D-IH-58-J — Persona-aware offline rubric (forward as OPS-58-3)

**Decision:** Forward the offline `_heuristic_persona_fit` calibration gap as **OPS-58-3** (engineering follow-up). The current rubric scores `3` (neutral) when `persona=None` is passed; the live judge has access to `persona_id` from the scenario and reads `persona_context` if provided, so they score higher on actually persona-appropriate stub responses. This produces uniform 5-vs-3 misalignment that drags the overall alignment percentage below the 80% target despite brand_voice + citation aligning perfectly.

**Why forward (vs. fix in OPS-58-1):**

- The fix is non-trivial — either (a) load `PERSONA_REGISTRY.csv` lazily inside `_heuristic_persona_fit`, (b) plumb `persona` from the scenario through the burn harness, or (c) recalibrate the offline default from `3` to `4` for known personas. Each option needs its own decision (axis weighting, default-vs-strict).
- The wiring + roster + banner work in OPS-58-1 already produces real, actionable evidence. Forwarding the rubric fix preserves the cycle-2 closure cadence.

**Reversibility:** High — OPS-58-3 ships as a normal engineering follow-up; if any of the three paths above is chosen, it's a one-PR change with a regression burn re-run.

---

## D-IH-58-K — OpenAI key rotation forwarded as OPS-58-2

**Decision:** Forward OpenAI provider key rotation as **OPS-58-2** (operator-funded; single-step). Current operator credential returns 401 (likely placeholder or rotated). Roster stays on Anthropic-only until rotation lands; on rotation, the original `anthropic + openai` cross-family roster can be re-exercised in a follow-up burn to validate cross-family consensus alignment (a separate D-IH-52-B input independent of the in-family flagship-vs-cheap data already collected in OPS-58-1).

**Reversibility:** N/A — secret rotation is operator-owned; agent never authors keys (D-IH-58-F).

---

## Decisions made during execution

### OPS-58-1 (2026-05-06) — Live cycle fired, real evidence collected

- See `D-IH-58-I` (judge wiring + roster pivot), `D-IH-58-J` (rubric gap forwarded), `D-IH-58-K` (OpenAI rotation forwarded).
- Phase A.0 re-evaluated: G-58-1 GREEN at 11/11 prerequisites met after operator updated `~/.openclaw/.env` with Anthropic + Supabase + Neo4j + Kalavai credentials and the agent set Phase A flags in shell per `D-IH-58-F` recommendation (export-not-persist).
- Phase A.1 / A.2 fired live (real Anthropic API; ~580s combined; 85 scenarios). See `reports/ops-58-1-2026-05-06.md`.
- Phase A.3 stayed scaffold-only (`P3 SCAFFOLD` exit per existing `cmd_run_live` body). NO-GO verdict per `D-IH-58-C`. **Expected**.
- Phase A.4 fired with `--filter madeira --mode live`: PASS in 9.5s; 12 sections; MADEIRA three-light all GREEN; `madeira_ship_go=true`. Manifest sha256: `363de24651a6911b0124f5f27275bb5c4523aeba3c7ea92fc2b20f093215e8ef`.
- Phase A.5 auto-skipped per A.3 NO-GO (conditional gate).

### P0 (2026-05-05) — Cycle-2 scope discipline

- **AKOS ships P0 + B + C + D + E in cycle 2; A forwards as OPS-58-1 if not fired by E.0.** Mirrors the I57 stub-mode-then-OPS-* pattern. The honest cycle-2 closure is "engineering closeout shipped; live validation forwarded if operator hasn't sat".
- **Folder name is `58-cycle-2-multi-track-forward/`** (matches the `CreatePlan` artifact name). The "multi-track" headline distinguishes I58 from I57 ("cycle-closeout") — Cycle 2 has five explicit tracks (A/B/C/D/E) rather than four buckets.
- **One new script in I58:** `scripts/preflight_g58_1.py` (A.0). Per the master-roadmap "asset classification → new canonical (script)". All other A.* sub-steps reuse existing scripts (`judge_calibration_burn.py`, `graphrag_poc.py`, `render_uat_dossier.py`, `endpoint_envelope_alarm.py`).
- **One modified script in I58:** `akos/runpod_provider.py` (D.2 alias seam).
- **I58 stays Open until E.0 fires** even though Phase A may forward. The README row records `Active` so the WIP_DASHBOARD reflects the in-flight engineering work; once E.0 closes, the row flips to `Closed (engineering side); OPS-58-1 forwarded if applicable`.
- **Cross-references explicit** — I05 + I20 (D.1 archive targets), I28/I29/I30/I31 (B.1–B.4 closure targets), I46 + I53 (A.3 GraphRAG ship verdict target; D-IH-46-E non-additive bar enforced per D-IH-58-C), I50/I51/I52/I53/I54 (preceding cycle 1 closures), I55 (continuous loop, runs through I58 unaffected), I56 (rails-ready, unchanged by I58), I57 (engineering predecessor).
