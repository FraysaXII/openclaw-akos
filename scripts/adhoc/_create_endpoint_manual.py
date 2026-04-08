import os, sys
sys.path.insert(0, '.')
from akos.io import REPO_ROOT, load_env_file, load_json

env = load_env_file(REPO_ROOT / 'config' / 'environments' / 'gpu-runpod.env')
for k,v in env.items():
    if v:
        os.environ[k] = v
import runpod
runpod.api_key = os.environ.get('RUNPOD_API_KEY', '')
endpoint = runpod.create_endpoint(
    name='akos-deepseek-r1-70b-awq',
    template_id='mic8s6xi7z',
    gpu_ids='AMPERE_80,ADA_80_PRO',
    workers_min=0,
    workers_max=2,
    idle_timeout=300,
)
print(endpoint)
