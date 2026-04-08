import json, urllib.request, os, sys
sys.path.insert(0, '.')
from akos.io import REPO_ROOT, load_env_file
env = load_env_file(REPO_ROOT / 'config' / 'environments' / 'gpu-runpod.env')
api_key = env.get('RUNPOD_API_KEY', '')
url = 'https://api.runpod.ai/v2/zu6v3o2gnsz7j8/openai/v1/chat/completions'
payload = json.dumps({
    'model': 'deepseek-r1-70b',
    'messages': [{'role': 'user', 'content': 'Reply with exactly one word: READY'}],
    'max_tokens': 20,
    'temperature': 0
}).encode()
req = urllib.request.Request(url, data=payload, headers={'Content-Type':'application/json','Authorization':'Bearer ' + api_key})
with urllib.request.urlopen(req, timeout=180) as resp:
    body = resp.read().decode()
print(body[:1000])
