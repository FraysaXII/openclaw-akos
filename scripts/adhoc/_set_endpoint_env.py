import sys
sys.path.insert(0, '.')
from akos.io import REPO_ROOT, resolve_openclaw_home
from scripts.gpu import _upsert_env_line
endpoint_id = 'zu6v3o2gnsz7j8'
url = f'https://api.runpod.ai/v2/{endpoint_id}/openai/v1'
_upsert_env_line(REPO_ROOT / 'config' / 'environments' / 'gpu-runpod.env', 'RUNPOD_ENDPOINT_ID', endpoint_id)
_upsert_env_line(REPO_ROOT / 'config' / 'environments' / 'gpu-runpod.env', 'VLLM_RUNPOD_URL', url)
oc_env = resolve_openclaw_home() / '.env'
if oc_env.exists():
    _upsert_env_line(oc_env, 'RUNPOD_ENDPOINT_ID', endpoint_id)
    _upsert_env_line(oc_env, 'VLLM_RUNPOD_URL', url)
print(url)
