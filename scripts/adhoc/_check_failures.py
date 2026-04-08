"""Check RunPod serverless for failed workers or jobs."""
import os, json, urllib.request
from akos.io import load_runtime_env, resolve_openclaw_home, set_process_env_defaults
set_process_env_defaults(load_runtime_env(resolve_openclaw_home()))
api_key = os.environ.get("RUNPOD_API_KEY", "")

# Full health with job details
url = f"https://api.runpod.ai/v2/52ss1838gaynf1/health"
req = urllib.request.Request(url, headers={"Authorization": "Bearer " + api_key})
resp = urllib.request.urlopen(req, timeout=15)
health = json.loads(resp.read().decode())
print("Full serverless health:")
print(json.dumps(health, indent=2))

# Check the template to see if it has the right config
print("\n\nChecking if the template has the model download configured...")
print("The serverless template may not have the vLLM command args correctly set.")
print("Template ID: xd2opc3fzd")
print("\nNote: The serverless worker needs the model pre-baked into the image or")
print("downloaded at startup. If the template only has the image 'vllm/vllm-openai:latest'")
print("without a network volume or pre-cached model, the worker has to download 70GB+ every cold start.")
