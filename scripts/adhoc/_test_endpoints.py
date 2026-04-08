"""Test both RunPod endpoints: serverless (API) and dedicated pod (vLLM direct)."""
import os, json, time, urllib.request
from akos.io import load_runtime_env, resolve_openclaw_home, set_process_env_defaults
set_process_env_defaults(load_runtime_env(resolve_openclaw_home()))
api_key = os.environ.get("RUNPOD_API_KEY", "")

SERVERLESS_ID = "52ss1838gaynf1"
POD_ID = "p3gw3ghvg6e8kv"

def check_serverless():
    print("=== SERVERLESS ENDPOINT ===")
    health_url = f"https://api.runpod.ai/v2/{SERVERLESS_ID}/health"
    req = urllib.request.Request(health_url, headers={"Authorization": "Bearer " + api_key})
    resp = urllib.request.urlopen(req, timeout=15)
    health = json.loads(resp.read().decode())
    w = health.get("workers", {})
    ready = w.get("ready", 0)
    init = w.get("initializing", 0)
    running = w.get("running", 0)
    print(f"  Workers: ready={ready} init={init} running={running}")

    if ready > 0 or running > 0:
        print("  Sending chat completion test...")
        chat_url = f"https://api.runpod.ai/v2/{SERVERLESS_ID}/openai/v1/chat/completions"
        payload = json.dumps({
            "model": "deepseek-r1-70b",
            "messages": [{"role": "user", "content": "Say hello in exactly one word."}],
            "max_tokens": 50,
        }).encode()
        req = urllib.request.Request(chat_url, data=payload, headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json",
        })
        start = time.time()
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            result = json.loads(resp.read().decode())
            elapsed = time.time() - start
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"  Response ({elapsed:.1f}s): {content[:200]}")
            print(f"  Model: {result.get('model', '?')}")
            return True
        except Exception as e:
            print(f"  Error: {e}")
    return False


def check_pod():
    print("\n=== DEDICATED POD ===")
    pod_base = f"https://{POD_ID}-8000.proxy.runpod.net"

    # Health check
    try:
        req = urllib.request.Request(pod_base + "/health", method="GET")
        resp = urllib.request.urlopen(req, timeout=10)
        print(f"  Health: {resp.read().decode()[:200]}")
    except urllib.request.HTTPError as e:
        print(f"  Health: HTTP {e.code}")
        return False
    except Exception as e:
        print(f"  Health: {type(e).__name__}")
        return False

    # Models
    try:
        req = urllib.request.Request(pod_base + "/v1/models", method="GET")
        resp = urllib.request.urlopen(req, timeout=10)
        print(f"  Models: {resp.read().decode()[:200]}")
    except Exception as e:
        print(f"  Models: {type(e).__name__}")

    # Chat test
    print("  Sending chat completion test...")
    chat_url = pod_base + "/v1/chat/completions"
    payload = json.dumps({
        "model": "deepseek-r1-70b",
        "messages": [{"role": "user", "content": "Say hello in exactly one word."}],
        "max_tokens": 50,
    }).encode()
    req = urllib.request.Request(chat_url, data=payload, headers={"Content-Type": "application/json"})
    start = time.time()
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read().decode())
        elapsed = time.time() - start
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        print(f"  Response ({elapsed:.1f}s): {content[:200]}")
        return True
    except Exception as e:
        print(f"  Error: {e}")
    return False


check_serverless()
check_pod()
