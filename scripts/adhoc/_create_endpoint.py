import os, sys
sys.path.insert(0, '.')
from akos.io import REPO_ROOT, load_env_file, load_json

env = load_env_file(REPO_ROOT / 'config' / 'environments' / 'gpu-runpod.env')
for k,v in env.items():
    if v:
        os.environ[k] = v

from akos.models import RunPodEndpointConfig
from akos.runpod_provider import RunPodProvider

overlay = load_json(REPO_ROOT / 'config' / 'environments' / 'gpu-runpod.json')
cfg = RunPodEndpointConfig.model_validate(overlay['runpod'])
provider = RunPodProvider(cfg)
print('Provider enabled:', provider.enabled)
info = provider.ensure_endpoint()
print('Endpoint info:', info)
if info:
    print('URL:', info.url)
    print('ID:', info.endpoint_id)
