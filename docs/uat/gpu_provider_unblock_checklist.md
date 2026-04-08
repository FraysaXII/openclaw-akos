# GPU Provider Unblock Checklist

Use this checklist to resume GPU UAT quickly after external provider blockers are cleared.

## Current Truth

- RunPod code/config fixes for AWQ startup, FlashInfer avoidance, and provider inventory preservation are already in the repo.
- Shadow/OpenStack auth and tenant inventory reads are already working from AKOS.
- The remaining blockers are external:
  - RunPod: account balance too low for fresh endpoint/pod creation.
  - Shadow: current role is forbidden from `os_compute_api:servers:create`.

## RunPod Checklist

### Prerequisites

1. **Balance gate (exact):** RunPod returns `QueryError: You must have at least $0.01 in your account balance to create an endpoint.` (and similar for dedicated pods) when balance is too low. Top up in the RunPod console billing area until **account balance ≥ $0.01** and payment method is valid. Without this, no new serverless endpoint and no new pod can be created regardless of code state.
2. Verify the **real** env files only (never point tooling at `*.env.example` for runtime):
   - `config/environments/gpu-runpod.env`
   - `config/environments/gpu-runpod-pod.env`
3. Ensure `RUNPOD_API_KEY` is set in those real files (or exported in the shell) and matches the key from the RunPod console.
4. Ensure `HF_TOKEN` is present for gated Hugging Face model downloads when deploying pods or custom images.
5. Install the serverless SDK dependency:

```bash
py -m pip install "runpod>=1.7.0"
```

### Worker logs (operator monitoring)

- RunPod **worker / endpoint logs** in the API may require the endpoint **`aiKey`** (from endpoint details in the console), not only the main `RUNPOD_API_KEY`, when `Authorization` returns `401` on log endpoints.
- In the console, open the endpoint → logs; correlate with template/env changes (`DTYPE=float16` for AWQ, `KV_CACHE_DTYPE=auto`, `VLLM_ATTENTION_BACKEND=TRITON_ATTN` for `runpod/worker-v1-vllm`).

### Resume Serverless

1. Recreate the endpoint:

```bash
py scripts/switch-model.py gpu-runpod
```

2. Confirm health:

```bash
curl http://127.0.0.1:8420/runpod/health
py scripts/gpu.py status
```

3. Confirm the worker no longer shows the previously fixed boot signatures:
   - no AWQ dtype mismatch
   - no `nvcc: not found`
   - no FlashInfer JIT startup failure loop

### Resume Dedicated Pod

1. Provision the pod:

```bash
py scripts/gpu.py deploy-pod
```

2. Confirm the proxy endpoint:

```bash
py scripts/gpu.py status
curl.exe "$env:VLLM_RUNPOD_URL/models"
```

3. If the pod URL in `gpu-runpod-pod.env` is stale, let the deploy flow overwrite it with the new live value before running UAT.

## Shadow Checklist

### Prerequisites

1. Verify the real env file:
   - `config/environments/gpu-shadow.env`
2. Ensure one of these auth paths is complete:
   - `OS_CLOUD=<cloud-name>` with a working `clouds.yaml`
   - direct Keystone vars (`OS_AUTH_URL`, `OS_PROJECT_ID`, `OS_USERNAME`, `OS_PASSWORD`, region/domain fields)
3. Ensure `HF_TOKEN` is valid for model download.
4. Install the SDK:

```bash
py -m pip install openstacksdk
```

### Tenant / Role Checks

1. In Skyline, open `Management > User Management`.
2. Confirm the acting user has a role that **includes Nova instance create** for this project (read-only or network-only roles are insufficient).
3. If AKOS still gets:

```text
Policy doesn't allow os_compute_api:servers:create to be performed
```

escalate with: **exact HTTP 403 body**, **project ID**, **username**, and request **`os_compute_api:servers:create`** (and attach `openstack server create --dry-run` or AKOS `deploy-shadow` output). Project admin or Shadow support must attach a role/policy that allows server create for that project.

**What you can do as operator:** Confirm auth works (`openstack catalog list`, `openstack flavor list`, `openstack image list`, `openstack network list`)—if these succeed but create fails, the blocker is **policy/role**, not AKOS wiring.

Reference:
- Shadow Project Management docs describe project roles.
- Shadow Limitations docs state that only documented/enabled features should be assumed available.

### Network / Security Group Checks

1. If security-group creation is forbidden, AKOS can fall back to project defaults.
2. If direct attach to `public` is not allowed in your tenant, create a project network/subnet/router in Skyline per the Shadow Networking guide and set `config/environments/gpu-shadow.json` `openstack.network` to that real project network name.
3. If a custom security group is required and supported in your tenant, pre-create it in Skyline/CLI and then point AKOS at that name instead of expecting AKOS to create it.

### Resume Shadow Deploy

1. Dry-run first:

```bash
py scripts/gpu.py deploy-shadow --dry-run
```

2. Deploy:

```bash
py scripts/gpu.py deploy-shadow
```

3. After the instance boots, confirm/update:
   - `VLLM_SHADOW_URL` in `config/environments/gpu-shadow.env`

4. Verify:

```bash
py scripts/gpu.py status
curl.exe "$env:VLLM_SHADOW_URL/models"
```

5. If policy still blocks creation, send Shadow support the exact Nova 403 plus your project ID and requested capability.

Support contact:
- `openstack@shadow.tech`

## Resume GPU UAT

Once either provider is unblocked:

1. Repair/start the local gateway if needed:

```bash
py scripts/doctor.py --repair-gateway
```

2. Re-run the fast governance checks:

```bash
py scripts/legacy/verify_openclaw_inventory.py
py scripts/check-drift.py
```

3. Re-run browser/local HLK UAT:
   - `docs/uat/hlk_admin_smoke.md`

4. Capture provider-specific evidence:
   - provider health
   - inference response
   - any remaining worker / Nova errors
