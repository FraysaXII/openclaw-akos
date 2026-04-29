#!/usr/bin/env python3
"""Test ShadowGPU (OpenStack) connectivity and list available resources."""
import os, sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from akos.io import REPO_ROOT, load_env_file

env = load_env_file(REPO_ROOT / "config" / "environments" / "gpu-shadow.env")
for k, v in env.items():
    if v:
        os.environ.setdefault(k, v)

from akos.openstack_provider import OpenStackProvider

print("Testing ShadowGPU (OpenStack) connectivity...")
print(f"Auth URL: {os.environ.get('OS_AUTH_URL', 'NOT SET')}")
print(f"Project:  {os.environ.get('OS_PROJECT_ID', 'NOT SET')[:16]}...")
print(f"User:     {os.environ.get('OS_USERNAME', 'NOT SET')}")
print(f"Region:   {os.environ.get('OS_REGION_NAME', 'NOT SET')}")
print()

provider = OpenStackProvider()
if provider.enabled:
    print("OpenStack connection: SUCCESS")
    print()

    flavors = provider.list_flavors()
    print(f"Available flavors: {len(flavors)}")
    gpu_flavors = [f for f in flavors if "gpu" in f["name"].lower() or "boost" in f["name"].lower()]
    for f in (gpu_flavors or flavors[:15]):
        print(f"  {f['name']:50s}  vCPUs={f.get('vcpus', '?'):>3}  RAM={f.get('ram_mb', 0)//1024:>3}GB")
    print()

    images = provider.list_images()
    print(f"Available images: {len(images)}")
    for img in images[:10]:
        print(f"  {img['name']:50s}  status={img.get('status', '?')}")
    print()
    print("ShadowGPU tenant is READY for deployment.")
else:
    print("OpenStack connection FAILED")
    print("Check OS_AUTH_URL, OS_USERNAME, OS_PASSWORD, OS_PROJECT_ID")
