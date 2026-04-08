"""Check dedicated pod status."""
import runpod, os, json
from akos.io import load_runtime_env, resolve_openclaw_home, set_process_env_defaults
set_process_env_defaults(load_runtime_env(resolve_openclaw_home()))
runpod.api_key = os.environ.get("RUNPOD_API_KEY", "")
pod = runpod.get_pod("t9vsl773yowieu")
status = pod.get("desiredStatus", "?")
runtime = pod.get("runtime", {}) or {}
gpus = runtime.get("gpus", []) or []
uptime = runtime.get("uptimeInSeconds", 0)
print(f"Pod status: {status}")
print(f"Uptime: {uptime}s")
print(f"GPUs: {len(gpus)}")
for g in gpus:
    gid = g.get("id", "?")
    util = g.get("gpuUtilPercent", 0)
    mem = g.get("memoryUtilPercent", 0)
    print(f"  GPU {gid}: {util}% compute, {mem}% memory")

# Also try vLLM health on the pod
import urllib.request
pod_health = f"https://t9vsl773yowieu-8000.proxy.runpod.net/health"
try:
    resp = urllib.request.urlopen(pod_health, timeout=10)
    print(f"\nvLLM health: {resp.read().decode()[:200]}")
except Exception as e:
    print(f"\nvLLM not responding yet: {type(e).__name__}")
