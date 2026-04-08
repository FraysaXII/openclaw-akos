"""Check both serverless and pod endpoint status."""
import os, urllib.request, json
from akos.io import load_runtime_env, resolve_openclaw_home, set_process_env_defaults
set_process_env_defaults(load_runtime_env(resolve_openclaw_home()))
api_key = os.environ.get("RUNPOD_API_KEY", "")

print("=== Serverless Endpoint ===")
try:
    req = urllib.request.Request(
        "https://api.runpod.ai/v2/52ss1838gaynf1/health",
        headers={"Authorization": "Bearer " + api_key},
    )
    resp = urllib.request.urlopen(req, timeout=15)
    health = json.loads(resp.read().decode())
    w = health.get("workers", {})
    print(f"  ready={w.get('ready',0)} init={w.get('initializing',0)} running={w.get('running',0)}")
except Exception as e:
    print(f"  Error: {e}")

print("\n=== Dedicated Pod ===")
pod_base = "https://t9vsl773yowieu-8000.proxy.runpod.net"
try:
    req = urllib.request.Request(pod_base + "/v1/models")
    resp = urllib.request.urlopen(req, timeout=10)
    print(f"  Models: {resp.read().decode()[:300]}")
except Exception as e:
    print(f"  Not ready yet: {type(e).__name__}: {str(e)[:200]}")

# Also try the pod health endpoint
try:
    req = urllib.request.Request(pod_base + "/health")
    resp = urllib.request.urlopen(req, timeout=10)
    print(f"  Health: {resp.read().decode()[:200]}")
except Exception as e:
    print(f"  Health check: {type(e).__name__}")
