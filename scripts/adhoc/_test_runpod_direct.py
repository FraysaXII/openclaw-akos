"""Test RunPod serverless endpoint with a direct run request (queues until worker ready)."""
import runpod, os, json, time
from akos.io import load_runtime_env, resolve_openclaw_home, set_process_env_defaults
set_process_env_defaults(load_runtime_env(resolve_openclaw_home()))
runpod.api_key = os.environ.get("RUNPOD_API_KEY", "")

endpoint = runpod.Endpoint("52ss1838gaynf1")

print("Sending test request to serverless endpoint (will queue until worker ready)...")
print("This may take several minutes on cold start.")
start = time.time()

try:
    run = endpoint.run({"input": {
        "openai_route": "/chat/completions",
        "openai_input": {
            "model": "deepseek-r1-70b",
            "messages": [{"role": "user", "content": "Say hello in exactly one word."}],
            "max_tokens": 50,
        }
    }})
    print(f"Run submitted: {run.job_id}")

    # Poll for result
    while True:
        status = run.status()
        elapsed = time.time() - start
        print(f"  [{elapsed:.0f}s] Status: {status}")
        if status == "COMPLETED":
            output = run.output()
            print(f"\nResult: {json.dumps(output, indent=2)[:500]}")
            break
        elif status in ("FAILED", "CANCELLED", "TIMED_OUT"):
            print(f"\nFailed: {status}")
            try:
                print(f"Output: {run.output()}")
            except:
                pass
            break
        time.sleep(10)

except Exception as e:
    print(f"Error: {e}")

elapsed = time.time() - start
print(f"\nTotal time: {elapsed:.0f}s")
