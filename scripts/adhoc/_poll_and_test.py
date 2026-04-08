"""Poll both endpoints and test the first one that becomes ready."""
import os, json, time, urllib.request
from akos.io import load_runtime_env, resolve_openclaw_home, set_process_env_defaults
set_process_env_defaults(load_runtime_env(resolve_openclaw_home()))
api_key = os.environ.get("RUNPOD_API_KEY", "")

SERVERLESS_ID = "52ss1838gaynf1"
POD_ID = "p3gw3ghvg6e8kv"
MAX_WAIT = 1800  # 30 min max

start = time.time()
print(f"Polling both endpoints every 30s (max {MAX_WAIT//60}min)...\n")

while time.time() - start < MAX_WAIT:
    elapsed = time.time() - start

    # Check serverless
    try:
        req = urllib.request.Request(
            f"https://api.runpod.ai/v2/{SERVERLESS_ID}/health",
            headers={"Authorization": "Bearer " + api_key},
        )
        resp = urllib.request.urlopen(req, timeout=10)
        h = json.loads(resp.read().decode())
        w = h.get("workers", {})
        s_ready = w.get("ready", 0)
        s_init = w.get("initializing", 0)
        s_run = w.get("running", 0)
    except:
        s_ready = s_init = s_run = -1

    # Check pod
    pod_ready = False
    try:
        req = urllib.request.Request(f"https://{POD_ID}-8000.proxy.runpod.net/health")
        resp = urllib.request.urlopen(req, timeout=5)
        pod_ready = True
    except:
        pass

    print(f"[{elapsed:.0f}s] Serverless: ready={s_ready} init={s_init} run={s_run} | Pod: {'READY' if pod_ready else 'waiting'}")

    # Test serverless if ready
    if s_ready > 0 or s_run > 0:
        print("\n>>> SERVERLESS READY! Testing chat completion...")
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
        t0 = time.time()
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            result = json.loads(resp.read().decode())
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"  Serverless response ({time.time()-t0:.1f}s): {content[:200]}")
        except Exception as e:
            print(f"  Serverless error: {e}")
        break

    # Test pod if ready
    if pod_ready:
        print("\n>>> POD READY! Testing chat completion...")
        chat_url = f"https://{POD_ID}-8000.proxy.runpod.net/v1/chat/completions"
        payload = json.dumps({
            "model": "deepseek-r1-70b",
            "messages": [{"role": "user", "content": "Say hello in exactly one word."}],
            "max_tokens": 50,
        }).encode()
        req = urllib.request.Request(chat_url, data=payload, headers={"Content-Type": "application/json"})
        t0 = time.time()
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            result = json.loads(resp.read().decode())
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"  Pod response ({time.time()-t0:.1f}s): {content[:200]}")
        except Exception as e:
            print(f"  Pod error: {e}")
        break

    time.sleep(30)

else:
    print(f"\nTimed out after {MAX_WAIT//60} minutes. Neither endpoint became ready.")

print(f"\nTotal elapsed: {time.time()-start:.0f}s")
