"""Fetch RunPod pod logs to check vLLM status."""
import runpod, os
from akos.io import load_runtime_env, resolve_openclaw_home, set_process_env_defaults
set_process_env_defaults(load_runtime_env(resolve_openclaw_home()))
runpod.api_key = os.environ.get("RUNPOD_API_KEY", "")

pod_id = "t9vsl773yowieu"

# Try to get pod details with more info
pod = runpod.get_pod(pod_id)
print(f"Status: {pod.get('desiredStatus')}")
runtime = pod.get("runtime") or {}
ports = runtime.get("ports", []) or []
print(f"Ports: {ports}")

# Check if there's a different URL pattern
# RunPod proxy URL might need the pod host ID
machine = pod.get("machine", {}) or {}
pod_host = machine.get("podHostId", "")
print(f"Pod host: {pod_host}")
print(f"Machine ID: {pod.get('machineId', '?')}")

# Try different URL patterns
import urllib.request
urls_to_try = [
    f"https://{pod_id}-8000.proxy.runpod.net/v1/models",
    f"https://{pod_id}-8000.proxy.runpod.net/health",
]
for url in urls_to_try:
    try:
        req = urllib.request.Request(url, method="GET")
        resp = urllib.request.urlopen(req, timeout=15)
        print(f"  OK {url}: {resp.read().decode()[:300]}")
    except urllib.request.HTTPError as e:
        body = ""
        try:
            body = e.read().decode()[:200]
        except:
            pass
        print(f"  HTTP {e.code} {url}: {body}")
    except Exception as e:
        print(f"  ERR {url}: {e}")
