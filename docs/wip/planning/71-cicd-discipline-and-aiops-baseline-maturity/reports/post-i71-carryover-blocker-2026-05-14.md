---
title: Post-I71-closure release-gate carry-over blocker — `[FAIL] Browser smoke (scripts/browser-smoke.py)`
date: 2026-05-14
status: blocker
classification: opt-stop-report
authored_by: agent
authored_at: 2026-05-14T22:00+02:00
post_initiative: 71
related_decisions:
  - D-IH-71-CLOSURE
related_files:
  - scripts/browser-smoke.py
  - scripts/release-gate.py
  - akos/api.py
gate_type: stop-and-clarify
predecessor_pass: post-`d52a33a` 2026-05-14
---

## 1. Failure label (verbatim)

`[FAIL] Browser smoke (scripts/browser-smoke.py)` — release-gate row produced
by `scripts/release-gate.py::main` calling
`py scripts/browser-smoke.py --playwright`.

## 2. Root cause (precise)

The 16-scenario Playwright smoke worker (Phase 1 + Phase 2 + Scenario 0
HTTP slice) requires the AKOS FastAPI control plane on
`http://127.0.0.1:8420` (and the OpenClaw gateway on
`http://127.0.0.1:18789` for `dashboard_health` / `workflow_launch`). On the
operator host neither service is running, so every Playwright `Page.goto`
fails with `net::ERR_CONNECTION_REFUSED at http://127.0.0.1:8420/...` and
every `urlopen` Scenario 0 HTTP call fails with `WinError 10061`. Worker
output: `PASS: 0 | SKIP: 0 | FAIL: 17`.

The smoke script does include a SKIP-on-unreachable guard (`scripts/browser-smoke.py`
line 927):

```python
if not _gateway_reachable() and not _api_reachable():
    results = [{"scenario": s, "status": "SKIP", "detail": "Gateway unreachable"}
               for s in PHASE1_SCENARIOS]
```

…but the guard is `AND` semantics across **two** services, only seeds Phase 1
(not Phase 2 / Scenario 0), and the Windows worker subprocess re-evaluates the
guard inside the worker — by which point one of the services may have
transiently answered (or the Phase 2/Scenario 0 scenarios bypass the guard
entirely). In any case, on this host with both services down the smoke does
not gracefully skip; it executes every scenario and reports FAIL.

## 3. Why this is Bucket C (operator decision required)

Per the task framing in the kickoff message:

> If `browser-smoke` fails because the dev-server isn't running: that's
> Bucket C (operator needs to ensure dev-server is up; or smoke needs a
> stub server). Document.

Three plausible remediation paths exist, each with cross-cutting effects the
agent cannot resolve unilaterally:

- **(a) Spawn the dev server inside `release-gate.py`** — would change the
  release-gate from a pure verification tool into a service-launching tool.
  Touches `akos/api.py` startup semantics (Langfuse / RunPod cold-init can
  exceed 5 s; current `AKOS_BROWSER_SMOKE_HTTP_TIMEOUT` budget is 30 s but
  startup can stretch). Has knock-on effects on CI runners that don't expect
  a long-lived FastAPI process. Needs operator ratification of the new
  contract (and a corresponding update to `docs/USER_GUIDE.md` Section 14.x
  + `.cursor/rules/akos-deploy-health.mdc`).
- **(b) Tighten the SKIP guard so the smoke skips when API is unreachable
  (regardless of gateway)** — would silently turn the smoke into a no-op on
  CI hosts that don't run the API, masking real regressions when an
  agent forgets to start the server. Needs operator ratification of the
  new SKIP semantics + the matching release-gate row treatment (PASS-as-INFO
  vs PASS-as-SKIP-flagged).
- **(c) Add a stub-server / mock fixture for the smoke** — proper engineering
  fix; biggest scope. Would need a new `scripts/serve-api-stub.py` (or a
  pytest-xdist-style fixture in the smoke runner) that returns canned
  responses for the ~20 endpoints the smoke exercises. Largest design call;
  affects the AKOS test harness contract.

None of (a) / (b) / (c) is mechanical; each requires an architectural
decision on what the release-gate's "browser smoke" row is **for**. That
decision belongs to the operator + System Owner.

## 4. Suggested fix path (recommended order)

1. **Short-term (this commit):** leave the smoke as-is; document this carry-over
   here. The Test suite gate now flips to PASS so release-gate verdict moves
   from `FAIL` to `FAIL` (still — only one row left red), but the chronic-
   noise inventory shrinks from 2 rows → 1 row.
2. **Next planning round (I72 P-N or a dedicated I-NN):** operator ratifies
   path (b) or (c). Path (b) is faster (≤ 50 LOC change in `browser-smoke.py`
   line 927 to make the guard `OR` semantics + add a top-level
   `AKOS_BROWSER_SMOKE_REQUIRE_API` env knob); path (c) is more work but
   removes the host-dependency entirely.
3. **Cross-rule update:** whichever path lands needs a corresponding update
   to `.cursor/rules/akos-deploy-health.mdc` § "Step 3 — Visual smoke" so
   the CI / pre-merge contract is documented.

## 5. Pre-existing-since marker

This FAIL has been red since the **I70 P13.6 baseline (2026-05-11 release-gate
hygiene pass)** per the kickoff context — the Phase-2 + Scenario-0 expansion
of the smoke catalogue (which made the row environment-dependent on both API
and gateway being up) predates I71's P0..P6 scope and was explicitly out of
I71's working surface. Sibling chronic-noise row `[FAIL] Test suite
(scripts/test.py all)` was cleared in this same commit by:

- Updating `akos/hlk_graph_model.py` to read the canonical
  `TOPIC_REGISTRY_FIELDNAMES` SSOT tuple from `akos.hlk_topic_registry_csv`
  instead of a stale local `TOPIC_REGISTRY_FIELDNAMES_MIN` duplicate that
  silently drifted when I71 P4 D-IH-71-R appended the 4-column review-stamp
  suffix. (Drift class identical to the BASELINE_FIELDNAMES bug class
  documented in the release-gate hygiene 2026-05-11 sync contract.)
- Updating `tests/test_validate_goipoi_register.py::test_stance_*` +
  `test_fieldnames_*` tests to recognize the I71 P4 D-IH-71-R review-stamp
  trailing-block doctrine: `stance` is the last column **before** the
  4-tuple `(last_review_at, last_review_by, last_review_decision_id,
  methodology_version_at_review)` review-stamp suffix, not the absolute
  last column.

Browser-smoke remains the sole pre-existing chronic FAIL on the
`origin/main @ d52a33a` release-gate after this cleanup.

## 6. Operator action requested

Pick one of:

- **Option A** (recommended for I72-N) — accept Bucket B path (b) "tighten
  SKIP guard"; agent will lift it in a follow-up commit once you ratify the
  new SKIP semantics (`AKOS_BROWSER_SMOKE_REQUIRE_API=0` defaults to
  current behavior; `=1` makes API-down a hard FAIL; SKIP otherwise).
- **Option B** — full path (c) "stub server"; charter a dedicated
  initiative (~3–5 phases) under the CICD discipline lineage.
- **Option C** — leave as documented chronic-noise; release-gate row stays
  FAIL on the operator host but is treated as known-environment in the
  release-gate verdict (similar to how operator inbox staleness emits
  `[INFO]` not `[FAIL]`).

Until ratification, this row is the only chronic FAIL in the release-gate
output. All other rows are green or advisory (`[INFO]` / `[SKIP]`).
