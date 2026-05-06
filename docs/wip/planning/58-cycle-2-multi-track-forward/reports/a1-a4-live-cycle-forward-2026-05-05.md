---
language: en
status: forwarded
initiative: 58-cycle-2-multi-track-forward
report_kind: phase-report
phase: A.1-A.4
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-05-05
---

# I58 A.1 → A.4 — Live cycle forward as OPS-58-1 (2026-05-05)

## Outcome

The four operator-funded sub-steps of Phase A — A.1 (multi-judge calibration burn), A.2 (persona-keyed cassette dispatch), A.3 (GraphRAG A/B), A.4 (live MADEIRA dossier) — forward as a single coordinated **OPS-58-1** sitting because A.0's first invocation in this AKOS environment returned **G-58-1 NO-FIRE** (4 / 11 prerequisites met). Per D-IH-58-B + R-58-1 documented response, the four sub-steps share one operator window with the OPS-57-1 runbook applied verbatim.

A.5 (conditional `SKILL_REGISTRY.csv` `retrieval_mode` flip + `POL-NEO4J-GRAPH-RAG-ELIGIBILITY-V1` POLICY clone) stays gated on A.3 GO per D-IH-58-C; deferred until OPS-58-1 fires.

This is **not a regression** — it matches the documented design boundary (engineering closure independent of operator funding per D-IH-58-A). I58 still closes at E.0 with A.* re-forwarding if the operator does not fire by then.

## Pre-flight state (A.0 first run, 2026-05-05)

`py scripts/preflight_g58_1.py` returned **4 / 11** in this AKOS environment:

| # | Prerequisite | Status | Source |
|:-:|:-------------|:------:|:-------|
| 1 | `AKOS_RECORD_LIVE=1` | MISS | unset |
| 2 | `ANTHROPIC_API_KEY` | MISS | unset / empty placeholder |
| 3 | `OPENAI_API_KEY` | MISS | unset / empty placeholder |
| 4 | `SUPABASE_URL` | **OK** | P0 wrote literal value `https://swrmqpelgoblaquequzb.supabase.co` |
| 5 | `SUPABASE_SERVICE_ROLE_KEY` | MISS | unset / empty placeholder |
| 6 | `MAX_DOSSIER_USD=50` | MISS | unset (commented in P0 block per operator-uncomment-per-sitting pattern) |
| 7 | `VLLM_RUNPOD_URL` or `RUNPOD_ENDPOINT_URL` | **OK** | `VLLM_RUNPOD_URL=http://localhost:8000/v1` (canonical) |
| 8 | `VLLM_SHADOW_URL` or `KALAVAI_ENDPOINT_URL` | **OK** | `VLLM_SHADOW_URL` set to the Kalavai trial URL (canonical) |
| 9 | `AKOS_JUDGE_ROSTER` (anthropic + openai) | MISS | unset (commented in P0 block) |
| 10 | `AKOS_GRAPHRAG_POC_LIVE=1` | MISS | unset (commented in P0 block) |
| 11 | `scripts/endpoint_envelope_alarm.py` | **OK** | present at repo path |

**Result: 4 / 11 → G-58-1 NO-FIRE** ([per A.0 evidence report](a0-env-preflight-2026-05-05.md)).

The 7 MISS rows are all operator-paste-required by D-IH-58-F invariance: provider keys, Supabase service-role JWT, the cost ceiling, the judge roster spec, and the two cycle-control flags (`AKOS_RECORD_LIVE=1`, `AKOS_GRAPHRAG_POC_LIVE=1`). The agent context cannot self-load any of them.

## Forward content per sub-step

### A.1 — OPS-52-1 multi-judge calibration burn (forwarded)

**Engineering substrate:** [`scripts/judge_calibration_burn.py`](../../../../scripts/judge_calibration_burn.py) ship-ready as of [I52 P3 closure](../52-multi-model-judge-and-cost-discipline/reports/uat-i52-multi-model-judge-and-cost-discipline-2026-05-03.md). Dispatcher-validation alignment was 100%/100%/100% in offline-fallback mode at I52 P3; OPS-52-1 is the first real-API burn.

**Operator command (when env loaded):**

```powershell
py scripts/judge_calibration_burn.py --live --persona founder --n 50 --target-pp 80
```

**Expected pre-flight cost:** ~$5 (per [I53 P1 estimate](../53-graphrag-poc-closure/reports/p1-golden-set-audit-2026-05-03.md)).

**Acceptance:** alignment ≥80% on ≥2/3 axes (Brand Voice / Citation / Persona Fit). On miss, `POL-EVAL-JUDGE-THRESHOLD-{BRAND-VOICE,CITATION,PERSONA-FIT}-V1` recalibration row drafted per D-IH-57-F inheritance; OPS-52-1 partially closes; gate re-arms for next cycle.

**Capture:** `reports/a1-judge-burn-2026-MM-DD.md` with calibration matrix + JSON sidecar under `artifacts/judge-calibration/<timestamp>/`.

### A.2 — OPS-50-1 / 51-1 persona-keyed cassette dispatch (forwarded)

**Engineering substrate:** Multi-judge harness from [I52 P2](../52-multi-model-judge-and-cost-discipline/master-roadmap.md); persona scenarios from [I51 P3](../51-persona-calibration-cleanup/master-roadmap.md). Persona-keyed cassette dispatch was the deferral path from I50 P4 (`OPS-50-1`) through I51 P3 (`OPS-51-1`) into I52 P3 (re-deferred to OPS-52-1 cycle).

**Operator command (when env loaded):**

Record-mode cassette dispatch under `AKOS_RECORD_LIVE=1` via the standard Madeira cassette flow; ≥2 personas populated under `tests/evals/cassettes/<persona_id>/`.

**Expected pre-flight cost:** ~$5.

**Acceptance:** ≥2 distinct `persona_id` cassette folders populated; `compliance.eval_run` row count delta ≥ N (where N = 2 personas × scenario count; verifiable via Supabase MCP `execute_sql`).

**Capture:** `reports/a2-cassettes-2026-MM-DD.md` with per-persona cassette manifest + `compliance.eval_run` row count delta.

### A.3 — OPS-53-1 GraphRAG A/B (forwarded)

**Engineering substrate:** [`scripts/graphrag_poc.py`](../../../../scripts/graphrag_poc.py) ship-ready as of [I53 P6 closure](../53-graphrag-poc-closure/reports/uat-i46-i53-graphrag-2026-05-03.md). Cassettes preserved under `tests/evals/cassettes/graph_rag/`. Golden set (20 queries; 60% multi-hop / 40% single-hop) audited at [I53 P1](../53-graphrag-poc-closure/reports/p1-golden-set-audit-2026-05-03.md).

**Operator command (when env loaded):**

```powershell
py scripts/graphrag_poc.py --live --max-spend 20 --golden-set
```

**Expected pre-flight cost:** ~$10–15 (per [I53 P1 estimate](../53-graphrag-poc-closure/reports/p1-golden-set-audit-2026-05-03.md); R-46-1 mitigated; abort threshold $25 inside the script's own envelope).

**Acceptance — D-IH-46-E non-additive bar (re-affirmed by D-IH-58-C):**

- **GO** = ≥3pp accuracy lift OR ≥30% latency reduction OR ≥40% cost reduction (any single bar).
- **NO-SHIP** = none of the three bars hit at the documented magnitude.

**Capture:** `D-IH-46-Decision-P3-2026-MM-DD` written to **BOTH** [I46 decision-log](../46-neo4j-strategic-posture/decision-log.md) AND [I53 decision-log](../53-graphrag-poc-closure/decision-log.md) with the verdict, the per-bar measurements, the cassette sha256s, and the one-line GO/NO-SHIP. Also: `reports/a3-graphrag-2026-MM-DD.md`.

**On NO-SHIP:** A.5 SKIPPED; I46 P5 stays deferred per D-IH-58-C; I58 still closes.

**On GO:** A.5 fires (see below).

### A.4 — Live MADEIRA dossier (forwarded)

**Engineering substrate:** [`scripts/render_uat_dossier.py`](../../../../scripts/render_uat_dossier.py) ship-ready since [I48 closure](../48-operator-dossier/reports/uat-i48-operator-dossier-2026-05-02.md); MADEIRA filter shipped at [I49 P0](../49-madeira-management-rollup/master-roadmap.md). Sections 3 (Eval health), 5 (Adversarial), 7 (Drift canaries) read from `compliance.eval_run` + `compliance.dossier_run` mirrors that A.1 + A.2 + A.3 populate.

**Operator command (when env loaded):**

```powershell
py scripts/render_uat_dossier.py --filter madeira --mode live
```

**Expected pre-flight cost:** ~$1–5 (rendering only; no fresh model calls beyond a brand-voice three-light recheck).

**Acceptance:** Sections 3, 5, 7 each return `status: PASS` (not `SKIP`) with `data_age_seconds` near zero. The MADEIRA three-light verdict transitions from "ship-ready in dispatcher-validation mode but NO-GO on snapshot data" to **GREEN-on-data** (assuming A.1 + A.2 + A.3 populated successfully).

**Capture:** `reports/a4-live-dossier-2026-MM-DD.md` with three-light verdict, manifest sha256, and per-section row counts. Artifact under `artifacts/dossier-i58-live-cycle/<timestamp>/` (gitignored).

## Operator runbook (verbatim from OPS-57-1, updated for I58)

If you want to fire A.1 → A.4 from this session (or a future session), follow these steps:

### Step 1 — Paste 7 missing values into `~/.openclaw/.env`

Open `C:\Users\Shadow\.openclaw\.env` (or whatever `OPENCLAW_HOME` resolves to) and fill in the 7 empty placeholders P0 wrote:

```bash
ANTHROPIC_API_KEY=sk-ant-...                              # provider key
OPENAI_API_KEY=sk-...                                     # provider key
SUPABASE_SERVICE_ROLE_KEY=eyJ...                          # JWT (NOT the anon key)
HF_TOKEN=hf_...                                           # optional but recommended
LANGFUSE_PUBLIC_KEY=pk-lf-...                             # optional but recommended
LANGFUSE_SECRET_KEY=sk-lf-...                             # optional but recommended
RUNPOD_API_KEY=...                                        # only if using a real RunPod pod (else leave empty)
```

Then **uncomment** the four Phase A flag lines (already in the long-lived block):

```bash
AKOS_RECORD_LIVE=1
AKOS_GRAPHRAG_POC_LIVE=1
AKOS_JUDGE_ROSTER=anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o
MAX_DOSSIER_USD=50
```

> **Recommended:** export the four Phase A flags in the calling shell rather than persist them in the file, so `AKOS_RECORD_LIVE=1` doesn't accidentally bleed into a regression run between sittings.

### Step 2 — Re-run preflight

```powershell
py scripts/preflight_g58_1.py
```

Expected: `Result: 11 / 11 prerequisites met. G-58-1 GREEN.`

If anything is still missing, the script tells you exactly what.

### Step 3 — Restart gateway with loaded env

```powershell
py scripts/serve-api.py --no-graph-explorer
```

Browse to `http://127.0.0.1:18789/health` and confirm the loaded provider list (Anthropic + OpenAI active, Supabase URL set, RunPod/Kalavai endpoint reachable).

### Step 4 — Wire the alarm

```powershell
$env:ENDPOINT_ENVELOPE_ABORT_AT = "40"
py scripts/endpoint_envelope_alarm.py --abort-at 40 --watch
```

Or simply pass `--abort-at 40` to each of the four sub-step invocations below.

### Step 5 — Fire the four sub-steps

```powershell
# A.1 — multi-judge calibration burn (~$5)
py scripts/judge_calibration_burn.py --live --persona founder --n 50 --target-pp 80

# A.2 — persona-keyed cassette dispatch (~$5)
# (uses the standard madeira cassette flow under AKOS_RECORD_LIVE=1; >=2 personas)
# operator-defined per the I50/51 cassette taxonomy

# A.3 — GraphRAG A/B (~$10-15)
py scripts/graphrag_poc.py --live --max-spend 20 --golden-set

# A.4 — live MADEIRA dossier (~$1-5)
py scripts/render_uat_dossier.py --filter madeira --mode live
```

### Step 6 — Capture outcomes

Write the four sub-step phase reports under `docs/wip/planning/58-cycle-2-multi-track-forward/reports/`:

- `a1-judge-burn-2026-MM-DD.md`
- `a2-cassettes-2026-MM-DD.md`
- `a3-graphrag-2026-MM-DD.md` (+ append `D-IH-46-Decision-P3-2026-MM-DD` to BOTH I46 and I53 decision-logs)
- `a4-live-dossier-2026-MM-DD.md`

If A.3 = GO, also fire A.5 (see [`a5-conditional-flip-2026-05-05.md`](a5-conditional-flip-2026-05-05.md) for the gated-out commit shape).

### Step 7 — Re-prompt agent for E.0 closure UAT

The agent picks up the captured outcomes and runs the closure verification matrix at E.0.

## Why the agent cannot fire this from the current session

Identical to the [I57 OPS-57-1 env recheck](../57-cycle-closeout-live-validation/reports/ops-57-1-env-recheck-2026-05-04.md):

- **Provider keys** are off-repo identity material; the agent has no read path to the operator's secret store and no permission to fabricate them (D-IH-58-F / D-IH-17 invariance).
- **Supabase service-role key** is a privileged write credential. Even if reachable, executing the live cycle from a non-operator context would violate the one-operator-per-cycle audit assumption that `compliance.eval_run` mirror parity depends on.
- **Spend authorization** is an operator decision. The ~$30–50 envelope under `MAX_DOSSIER_USD=50` (per D-IH-57-G inheritance) is the operator's budget call; auto-firing would breach G-58-1.

This is the documented design boundary (engineering ≠ operator funding per D-IH-58-A), not a missing capability.

## Engineering substrate verified

| Component | Path | State |
|:----------|:-----|:------|
| Pre-flight gate | [`scripts/preflight_g58_1.py`](../../../../scripts/preflight_g58_1.py) | NEW (A.0); 14 / 14 tests PASS; first run returned 4 / 11 (NO-FIRE) |
| Long-lived env block | `~/.openclaw/.env` | Written by P0; structure + commented Phase A flags + 7 empty placeholders |
| Multi-judge burn script | [`scripts/judge_calibration_burn.py`](../../../../scripts/judge_calibration_burn.py) | Ship-ready (I52 P3 dispatcher-validation 100% / 100% / 100%) |
| GraphRAG PoC script | [`scripts/graphrag_poc.py`](../../../../scripts/graphrag_poc.py) | Ship-ready (I53 P6 closure) |
| Live dossier renderer | [`scripts/render_uat_dossier.py`](../../../../scripts/render_uat_dossier.py) | Ship-ready (I48 closure + I49 P0 MADEIRA filter) |
| Endpoint envelope alarm | [`scripts/endpoint_envelope_alarm.py`](../../../../scripts/endpoint_envelope_alarm.py) | Present (G-58-1 check 11) |
| Supabase target | `compliance.eval_run` + `compliance.dossier_run` mirrors | Drift-clean (per [I22a P7 17/17 mirrors parity](../22a-i22-post-closure-followups/reports/uat-i24-supabase-apply-20260504.md)) |

No regression since I57 closure: all four scripts present, `--help`-clean, and load without import errors.

## Cross-references

- A.0 evidence: [`a0-env-preflight-2026-05-05.md`](a0-env-preflight-2026-05-05.md)
- I57 P4 forward (the OPS-57-1 origin): [`p4-live-cycle-forward-2026-05-04.md`](../57-cycle-closeout-live-validation/reports/p4-live-cycle-forward-2026-05-04.md)
- I57 OPS-57-1 env recheck: [`ops-57-1-env-recheck-2026-05-04.md`](../57-cycle-closeout-live-validation/reports/ops-57-1-env-recheck-2026-05-04.md)
- I52 P3 dispatcher validation: [`uat-i52-multi-model-judge-and-cost-discipline-2026-05-03.md`](../52-multi-model-judge-and-cost-discipline/reports/uat-i52-multi-model-judge-and-cost-discipline-2026-05-03.md)
- I53 P6 closure (GraphRAG ship-ready): [`uat-i46-i53-graphrag-2026-05-03.md`](../53-graphrag-poc-closure/reports/uat-i46-i53-graphrag-2026-05-03.md)
- D-IH-58-B (OPS-57-1 inside Phase A): [`decision-log.md`](../decision-log.md#d-ih-58-b--ops-57-1-fires-inside-i58-phase-a-not-detached)
- D-IH-58-C (NO-SHIP is closure event, not failure): [`decision-log.md`](../decision-log.md#d-ih-58-c--graphrag-no-ship-is-a-closure-event-not-a-failure)
- D-IH-58-F (env enrichment is operator-driven): [`decision-log.md`](../decision-log.md#d-ih-58-f--openclawenv-enrichment-is-operator-driven-d-ih-17-invariance)
