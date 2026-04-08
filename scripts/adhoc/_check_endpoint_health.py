import os, sys, json, time, urllib.request
sys.path.insert(0, '.')
from akos.io import REPO_ROOT, load_env_file

env = load_env_file(REPO_ROOT / 'config' / 'environments' / 'gpu-runpod.env')
api_key = env.get('RUNPOD_API_KEY', '')
endpoint_id = env.get('RUNPOD_ENDPOINT_ID', 'zu6v3o2gnsz7j8')
url = f'https://api.runpod.ai/v2/{endpoint_id}/health'
req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + api_key})
with urllib.request.urlopen(req, timeout=20) as resp:
    data = json.loads(resp.read().decode())
print(json.dumps(data, indent=2))
