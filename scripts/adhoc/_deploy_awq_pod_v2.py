#!/usr/bin/env python3
"""Deploy AWQ pod on RunPod with pinned vLLM image to avoid Docker Hub rate limits."""
import os, sys, time
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from akos.io import REPO_ROOT, load_env_file, load_json, resolve_openclaw_home
from akos.model_catalog import load_catalog
from akos.models import PodConfig
from akos.runpod_provider import PodManager, RunPodProvider
from akos.state import ActiveInfra, load_state, save_state

env = load_env_file(REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.env")
api_key = env.get("RUNPOD_API_KEY", "")
hf_token = env.get("HF_TOKEN", "")

catalog = load_catalog()
awq_entry = next(e for e in catalog if "awq" in e.hfId.lower())
print(f"Model: {awq_entry.displayName} ({awq_entry.hfId})")

config_raw = load_json(REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.json")
pod_config = PodConfig.model_validate(config_raw.get("pod", {}))

# Pin to a specific vLLM version to avoid Docker Hub rate limit on :latest
PINNED_IMAGE = "vllm/vllm-openai:v0.8.4"
pod_config.containerImage = PINNED_IMAGE
print(f"Image: {PINNED_IMAGE} (pinned to avoid Docker Hub rate limit)")

vllm_cmd = pod_config.build_vllm_command()
port = pod_config.vllmPort
print(f"GPU: {pod_config.gpuType} x{pod_config.gpuCount}")
print(f"vLLM CMD flags: quantization={'--quantization' in vllm_cmd}, enforce-eager={'--enforce-eager' in vllm_cmd}")
print(f"Max seqs: {pod_config.envVars.get('MAX_NUM_SEQS')}")
print()

env_vars = {}
if hf_token:
    env_vars["HF_TOKEN"] = hf_token
env_vars.update(pod_config.envVars)

print("Creating pod on RunPod...")
pm = PodManager(api_key)
pod = pm.create_pod(
    name="akos-d1-70b-awq-v4",
    gpu_type_id=pod_config.gpuType,
    gpu_count=pod_config.gpuCount,
    image=PINNED_IMAGE,
    container_disk_gb=pod_config.containerDiskGb,
    volume_gb=pod_config.volumeGb,
    ports=[f"{port}/http", "22/tcp"],
    env=env_vars,
    docker_start_cmd=vllm_cmd,
)

if not pod:
    print("Pod creation failed! Check RunPod dashboard for GPU availability.")
    sys.exit(1)

vllm_url = f"https://{pod.pod_id}-{port}.proxy.runpod.net/v1"
print(f"Pod created: {pod.pod_id}")
print(f"Status: {pod.status}")
print(f"URL: {vllm_url}")

oc_home = resolve_openclaw_home()
state = load_state(oc_home)
state.activeInfra = ActiveInfra(
    type="pod", podId=pod.pod_id, url=vllm_url,
    gpuType=pod_config.gpuType, gpuCount=pod_config.gpuCount,
    modelName=awq_entry.hfId,
)
save_state(oc_home, state)

from scripts.gpu import _upsert_env_line
_upsert_env_line(REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.env", "VLLM_RUNPOD_URL", vllm_url)
_upsert_env_line(REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.env", "RUNPOD_POD_ID", pod.pod_id)
oc_env = oc_home / ".env"
if oc_env.exists():
    _upsert_env_line(oc_env, "VLLM_RUNPOD_URL", vllm_url)
    _upsert_env_line(oc_env, "RUNPOD_POD_ID", pod.pod_id)

print()
print("Pod is booting. Polling for vLLM health every 30s...")
print("(AWQ model ~37GB download + ~2min load)")
print()

start = time.monotonic()
timeout = 20 * 60
while time.monotonic() - start < timeout:
    elapsed = int(time.monotonic() - start)
    health = RunPodProvider.probe_vllm_health(vllm_url, timeout=8.0)
    if health.healthy:
        mins, secs = divmod(elapsed, 60)
        print(f"\n=== vLLM HEALTHY after {mins}m{secs}s ===")
        print(f"URL: {vllm_url}")
        print(f"Pod: {pod.pod_id}")
        sys.exit(0)

    mins, secs = divmod(elapsed, 60)
    print(f"  [{mins:02d}:{secs:02d}] waiting... (pod={pod.pod_id})", flush=True)
    time.sleep(30)

elapsed = int(time.monotonic() - start)
print(f"\nTimeout after {elapsed//60}m. Check RunPod logs at:")
print(f"  https://www.runpod.io/console/pods/{pod.pod_id}/logs")
sys.exit(1)
