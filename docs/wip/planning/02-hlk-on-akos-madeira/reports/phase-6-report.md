# Phase 6 Status Report: Runtime Remediation (RunPod, Branding, Workspace Recovery)

**Source plan**: `C:\Users\Shadow\.cursor\plans\madeira_flagship_hardening_4f22c4ab.plan.md`
**Phase**: 6 -- Runtime Remediation and UAT Recovery
**Timeline**: 2026-04-03
**Outcome**: **GO WITH RESIDUAL** -- Runtime hardening shipped, but live GPU providers are blocked by external account/policy constraints
**Author**: AKOS runtime remediation execution

---

## 1. Executive Summary

This phase resumed a failed live UAT run and repaired the highest-impact runtime defects first: serverless worker crashes, missing orchestrator workspace startup scaffolding, Shadow tenant config mismatches, and documentation drift for operator troubleshooting. The serverless endpoint reached `workers.ready > 0`, served completions, and no longer crashed on the earlier AWQ dtype/FlashInfer boot errors. Shadow connectivity now succeeds and live tenant inventory is known-good. The remaining live GPU blockers are external: RunPod account balance is too low for fresh endpoint/pod creation, and the current Shadow role is forbidden from creating servers.

## 2. Asset Classification (Governance)

| Scope | Classification | Notes |
|-------|----------------|-------|
| RunPod runtime overlays, model catalog, AKOS models, GPU scripts | Runtime config/code (SSOT governed) | In scope; updated with deterministic compatibility defaults |
| Workspace scaffold files | Runtime/operator scaffold | In scope; Orchestrator `WORKFLOW_AUTO.md` added and deployed |
| HLK canonical compliance vault (`docs/references/hlk/compliance/*.csv`) | Canonical compliance assets | **Not in scope** (no canonical CSV modifications) |

## 3. Deliverables

| Deliverable | Status | Notes |
|-------------|--------|-------|
| RunPod serverless crash triage with worker-log evidence | Done | Root causes captured: AWQ dtype mismatch, FlashInfer/nvcc startup failure, then GPU memory availability failure loop |
| RunPod serverless compatibility hardening | Done | `DTYPE=float16` for AWQ, `KV_CACHE_DTYPE=auto`, `VLLM_ATTENTION_BACKEND=TRITON_ATTN` |
| Live endpoint recovery and validation | Partial | Endpoint recreated; inference completed successfully at least once under new settings, but fresh endpoint creation is now blocked by account balance |
| Orchestrator workspace startup scaffold recovery | Done | Added `config/workspace-scaffold/orchestrator/WORKFLOW_AUTO.md` and deployed to `~/.openclaw/workspace-orchestrator/WORKFLOW_AUTO.md` |
| Local gateway post-reboot recovery | Done | Rebound runtime to `deepseek-r1:14b`, confirmed branded UI HTTP 200, and restored gateway RPC health via manual run |
| Documentation synchronization for troubleshooting and runtime behavior | Done | Updated `docs/USER_GUIDE.md`, `docs/ARCHITECTURE.md`, scaffold README |
| Dedicated RunPod pod remediation | Blocked | New pod creation failed: RunPod API returned account balance too low |
| ShadowGPU (OpenStack) API and tenant inventory validation | Done | Keystone auth, flavors, images, and networks now verified against the live tenant |
| ShadowGPU deployment compatibility hardening | Done | Corrected image/flavor/network defaults and made security-group/key handling policy-tolerant |
| ShadowGPU instance deployment | Blocked | Current OpenStack role is forbidden from `servers:create` |

## 4. Evidence and Verification Matrix

| Check | Result | Evidence |
|------|--------|----------|
| Serverless health probe | PASS (intermittent) | `/health` showed `ready=1`, `throttled=0`, later reverted when workers recycled |
| Serverless inference smoke | PASS | `chat.completions` returned a valid response payload (`model=deepseek-r1-70b`) |
| Worker log root-cause extraction | PASS | `Worker startup failed`, `nvcc: not found`, and later `Free memory on device cuda:0 ... less than desired GPU memory utilization` |
| Orchestrator workspace `WORKFLOW_AUTO.md` presence | PASS | File created and confirmed at `~/.openclaw/workspace-orchestrator/WORKFLOW_AUTO.md` |
| Local gateway health RPC | PASS | `openclaw gateway call health` returned `ok: true` and enumerated all 5 agents |
| Strict inventory verification | PASS | `py scripts/legacy/verify_openclaw_inventory.py` returned `OVERALL: PASS` after provider reseeding and env-aware default-model expectation |
| Drift verification | PASS | `py scripts/check-drift.py` returned `No drift detected. Runtime matches repo state.` |
| Dedicated pod redeploy | FAIL (blocked) | RunPod REST: `"Your account balance is too low to rent a pod"` |
| Shadow OpenStack connectivity | PASS | `OpenStack connection: SUCCESS`; live flavor/image/network enumeration succeeded |
| Shadow instance create | FAIL (blocked) | Nova policy: `Policy doesn't allow os_compute_api:servers:create to be performed` |

## 5. Issues and Decisions

1. **Decision P6-D1 (AWQ dtype enforcement)**  
   AWQ deployments are forced to `DTYPE=float16` via config + model/schema normalization to prevent repeat startup crashes.

2. **Decision P6-D2 (RunPod worker backend hardening)**  
   For `runpod/worker-v1-vllm`, defaults are normalized to `KV_CACHE_DTYPE=auto` and `VLLM_ATTENTION_BACKEND=TRITON_ATTN` to avoid FlashInfer JIT dependency on `nvcc`.

3. **Decision P6-D3 (Cost protection while unstable)**  
   Endpoint `workersMin` was reduced back to `0` to prevent continuous spend during worker crash loops.

4. **Issue P6-I1 (Dedicated pod blocked)**  
   Dedicated pod remediation cannot be completed until RunPod account balance is replenished.

5. **Issue P6-I2 (Serverless stability residual)**  
   Current worker logs show occasional memory-availability failures (`free memory < desired utilization`). This is now a tuning/placement residual rather than the original hard boot crash.

6. **Decision P6-D4 (Shadow tenant compatibility)**  
   Shadow deployment defaults are aligned to the live tenant inventory: `Ubuntu-22.04`, `power-c32m112-gpu-A4500-4`, `public` network, and no explicit security group when policy forbids creation.

7. **Issue P6-I3 (Shadow policy blocker)**  
   The authenticated OpenStack role can read inventory but cannot create servers. This blocks live Shadow GPU bring-up until project permissions are expanded.

8. **Decision P6-D5 (Local fallback restoration)**  
   Because both live GPU providers hit external blockers, `dev-local` was realigned to the documented medium-tier path (`ollama/deepseek-r1:14b` primary, `qwen3:8b` fallback) so browser/UAT recovery has a stronger local lane.

## 6. Next Steps

1. Re-top up RunPod balance, then re-run serverless endpoint creation and dedicated pod deployment and verify `/health`, `/v1/models`, and `/v1/chat/completions`.
2. Ask the ShadowGPU / OpenStack operator to grant `os_compute_api:servers:create` for this project/role, then retry `deploy-shadow`.
3. Run final browser UAT matrix (`docs/uat/hlk_admin_smoke.md`) with pass/fail evidence capture after at least one live GPU provider path is restored.
4. Tune serverless residual memory churn (candidate knobs: lower `GPU_MEMORY_UTILIZATION`, lower `MAX_MODEL_LEN`, lower `MAX_NUM_SEQS`, constrain GPU pool) based on new worker logs.
5. Execute full governed verification matrix before commit:
   - `py scripts/legacy/verify_openclaw_inventory.py`
   - `py scripts/check-drift.py`
   - `py scripts/test.py all`
   - `py scripts/browser-smoke.py --playwright`
   - `py -m pytest tests/test_api.py -v`
   - `py scripts/release-gate.py`
