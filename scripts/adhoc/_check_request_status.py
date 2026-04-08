import json, urllib.request, os, sys
sys.path.insert(0, '.')
from akos.io import REPO_ROOT, load_env_file
env = load_env_file(REPO_ROOT / 'config' / 'environments' / 'gpu-runpod.env')
api_key = env.get('RUNPOD_API_KEY', '')
url = 'https://api.runpod.ai/v2/zu6v3o2gnsz7j8/status/aeb2c984-c60b-4803-85f8-c4990555f649-e1'
req = urllib.request.Request(url, headers={'Authorization':'Bearer ' + api_key})
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode())
print(json.dumps(data, indent=2)[:2000])
