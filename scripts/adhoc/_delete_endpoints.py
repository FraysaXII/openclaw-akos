import json, os, sys, urllib.request
sys.path.insert(0, '.')
from akos.io import REPO_ROOT, load_env_file, load_json

env = load_env_file(REPO_ROOT / 'config' / 'environments' / 'gpu-runpod.env')
api_key = env.get('RUNPOD_API_KEY', '')
headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
for eid in ['11jvky5tb185cd', '52ss1838gaynf1']:
    req = urllib.request.Request(f'https://rest.runpod.io/v1/endpoints/{eid}', method='DELETE', headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print('Deleted', eid, 'status', resp.status)
    except Exception as e:
        print('Delete failed', eid, e)
