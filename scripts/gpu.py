#!/usr/bin/env python3
"""AKOS GPU Infrastructure Manager.

Interactive CLI for deploying, monitoring, and tearing down GPU inference
infrastructure on RunPod -- both dedicated pods and serverless endpoints.

Usage:
    py scripts/gpu.py              # interactive menu
    py scripts/gpu.py deploy-pod   # direct command
    py scripts/gpu.py status       # check health
    py scripts/gpu.py teardown     # stop infrastructure
    py scripts/gpu.py --dry-run    # preview without calling RunPod API

Zero copy-paste. Zero dashboard visits. Zero SSH.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT, load_env_file, load_json, resolve_openclaw_home, save_json
from akos.log import setup_logging
from akos.models import PodConfig
from akos.runpod_provider import PodManager, RunPodProvider
from akos.state import ActiveInfra, AkosState, load_state, save_state

logger = logging.getLogger("akos.gpu")

_GPU_CATALOG = [
    {"id": "NVIDIA A100-SXM4-80GB", "name": "A100 80GB SXM", "vram": 80, "price_hr": 1.64},
    {"id": "NVIDIA A100 80GB PCIe", "name": "A100 80GB PCIe", "vram": 80, "price_hr": 1.64},
    {"id": "NVIDIA H100 80GB HBM3", "name": "H100 80GB", "vram": 80, "price_hr": 2.69},
    {"id": "NVIDIA H200", "name": "H200", "vram": 141, "price_hr": 3.29},
    {"id": "NVIDIA L40S", "name": "L40S 48GB", "vram": 48, "price_hr": 0.74},
    {"id": "NVIDIA RTX A6000", "name": "RTX A6000 48GB", "vram": 48, "price_hr": 0.53},
    {"id": "NVIDIA GeForce RTX 4090", "name": "RTX 4090 24GB", "vram": 24, "price_hr": 0.44},
]


def _ensure_api_key() -> str:
    key = os.environ.get("RUNPOD_API_KEY", "")
    if key and key != "YOUR_RUNPOD_API_KEY":
        return key

    langfuse_env = REPO_ROOT / "config" / "eval" / "langfuse.env"
    for p in [REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.env",
              REPO_ROOT / "config" / "environments" / "gpu-runpod.env"]:
        if p.exists():
            env = load_env_file(p)
            if env.get("RUNPOD_API_KEY", "").startswith("YOUR"):
                continue
            if env.get("RUNPOD_API_KEY"):
                os.environ["RUNPOD_API_KEY"] = env["RUNPOD_API_KEY"]
                return env["RUNPOD_API_KEY"]

    print()
    print("  RunPod API key required.")
    print("  Get one at: https://www.runpod.io/console/user/settings")
    print()
    try:
        key = input("  Enter your RunPod API key: ").strip()
    except (EOFError, KeyboardInterrupt):
        return ""
    if key:
        os.environ["RUNPOD_API_KEY"] = key
        _save_key_to_env("RUNPOD_API_KEY", key)
    return key


def _ensure_hf_token() -> str:
    token = os.environ.get("HF_TOKEN", "")
    if token and not token.startswith("your"):
        return token

    print()
    print("  HuggingFace token required (for gated models).")
    print("  Get one at: https://huggingface.co/settings/tokens")
    print()
    try:
        token = input("  Enter your HF token (hf_...): ").strip()
    except (EOFError, KeyboardInterrupt):
        return ""
    if token:
        os.environ["HF_TOKEN"] = token
        _save_key_to_env("HF_TOKEN", token)
    return token


def _save_key_to_env(key: str, value: str) -> None:
    env_path = REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.env"
    if not env_path.exists():
        example = env_path.with_suffix(".env.example")
        if example.exists():
            env_path.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            env_path.write_text("", encoding="utf-8")
    lines = env_path.read_text(encoding="utf-8").splitlines()
    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            found = True
            break
    if not found:
        lines.append(f"{key}={value}")
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _pick_gpu(pod_config: PodConfig) -> tuple[str, int]:
    model_name = pod_config.modelName
    is_70b = "70b" in model_name.lower()

    print()
    print("  Select GPU configuration")
    print("  " + "-" * 40)
    if is_70b:
        print("  The 70B model needs ~140 GB VRAM (weights + KV cache).")
        print("  You need multiple GPUs. Recommended: 2x A100 80GB.")
    print()
    print(f"  {'#':<4} {'GPU':<25} {'VRAM':<10} {'~$/hr':<8}")
    print(f"  {'─'*4} {'─'*25} {'─'*10} {'─'*8}")

    for i, gpu in enumerate(_GPU_CATALOG, 1):
        marker = " *" if gpu["id"] == pod_config.gpuType else ""
        print(f"  {i:<4} {gpu['name']:<25} {gpu['vram']} GB{'':<4} ${gpu['price_hr']:.2f}{marker}")

    print()
    print(f"  Current default: {pod_config.gpuType} x{pod_config.gpuCount}")
    try:
        choice = input(f"  GPU number [Enter for default]: ").strip()
    except (EOFError, KeyboardInterrupt):
        return pod_config.gpuType, pod_config.gpuCount

    if choice and choice.isdigit() and 1 <= int(choice) <= len(_GPU_CATALOG):
        gpu = _GPU_CATALOG[int(choice) - 1]
        gpu_type = gpu["id"]
    else:
        gpu_type = pod_config.gpuType

    if is_70b:
        total_vram = next((g["vram"] for g in _GPU_CATALOG if g["id"] == gpu_type), 80)
        min_gpus = max(2, (140 + total_vram - 1) // total_vram)
        print(f"  70B model needs at least {min_gpus} GPUs of this type.")
        try:
            count_str = input(f"  GPU count [{min_gpus}]: ").strip()
        except (EOFError, KeyboardInterrupt):
            return gpu_type, min_gpus
        gpu_count = int(count_str) if count_str.isdigit() else min_gpus
        gpu_count = max(gpu_count, min_gpus)
    else:
        gpu_count = 1

    return gpu_type, gpu_count


def deploy_pod(*, dry_run: bool = False) -> int:
    print()
    print("=" * 60)
    print("  Deploy Dedicated Pod")
    print("=" * 60)

    api_key = _ensure_api_key()
    if not api_key:
        print("  No API key. Aborting.")
        return 1

    hf_token = _ensure_hf_token()

    config_path = REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.json"
    raw = load_json(config_path)
    pod_config = PodConfig.model_validate(raw.get("pod", {}))

    gpu_type, gpu_count = _pick_gpu(pod_config)
    pod_config.gpuCount = gpu_count
    pod_config.gpuType = gpu_type
    pod_config.envVars["TENSOR_PARALLEL_SIZE"] = str(gpu_count)

    vllm_cmd = pod_config.build_vllm_command()
    port = pod_config.vllmPort
    env_vars = {
        **({"HF_TOKEN": hf_token} if hf_token else {}),
    }

    print()
    print(f"  Model:     {pod_config.modelName}")
    print(f"  GPU:       {gpu_type} x{gpu_count}")
    print(f"  Port:      {port}")
    print(f"  Image:     {pod_config.containerImage}")
    print(f"  Volume:    {pod_config.volumeGb} GB")
    print(f"  TP size:   {gpu_count} (auto-derived from GPU count)")
    print()

    if dry_run:
        print("  [DRY-RUN] Would create pod with above config.")
        print(f"  [DRY-RUN] vLLM command: {' '.join(vllm_cmd)}")
        return 0

    oc_home = resolve_openclaw_home()
    state = load_state(oc_home)
    if state.activeInfra.type == "pod" and state.activeInfra.podId:
        pm_check = PodManager(api_key)
        existing = pm_check.get_pod(state.activeInfra.podId)
        if existing and existing.status in ("RUNNING", "CREATED"):
            print(f"  Existing pod found: {existing.pod_id} ({existing.status})")
            print(f"  Reusing it (idempotent). Use 'teardown' first to create a new one.")
            vllm_url = state.activeInfra.url or f"https://{existing.pod_id}-{port}.proxy.runpod.net/v1"
            health = RunPodProvider.probe_vllm_health(vllm_url, timeout=5.0)
            print(f"  vLLM health: {'healthy' if health.healthy else 'starting/unreachable'}")
            return 0

    print("  Creating pod on RunPod...")
    pm = PodManager(api_key)
    pod = pm.create_pod(
        name=f"akos-vllm-{pod_config.modelName.split('/')[-1][:30]}",
        gpu_type_id=gpu_type,
        gpu_count=gpu_count,
        image=pod_config.containerImage,
        volume_gb=pod_config.volumeGb,
        ports=[f"{port}/http", "22/tcp"],
        env=env_vars,
        docker_start_cmd=["bash", "-c", f"pip install vllm && {' '.join(vllm_cmd)}"],
    )

    if not pod:
        print("  Pod creation failed. Check your API key and GPU availability.")
        return 1

    print(f"  Pod created: {pod.pod_id}")
    print(f"  Status: {pod.status}")
    print()

    vllm_url = f"https://{pod.pod_id}-{port}.proxy.runpod.net/v1"

    print("  Waiting for vLLM to start (model download + load)...")
    print("  This takes 5-15 minutes for the first run.")
    print()

    start = time.monotonic()
    timeout = 20 * 60
    while time.monotonic() - start < timeout:
        elapsed = int(time.monotonic() - start)
        health = RunPodProvider.probe_vllm_health(vllm_url, timeout=5.0)
        if health.healthy:
            print(f"\n  vLLM is healthy! ({elapsed}s)")
            break
        mins, secs = divmod(elapsed, 60)
        print(f"  [{mins:02d}:{secs:02d}] Waiting for vLLM...", end="\r")
        time.sleep(15)
    else:
        print(f"\n  Timeout after {timeout//60} minutes. Pod may still be loading.")
        print(f"  Check RunPod dashboard for pod {pod.pod_id}")
        print(f"  URL will be: {vllm_url}")

    _save_key_to_env("VLLM_RUNPOD_URL", vllm_url)
    _save_key_to_env("RUNPOD_POD_ID", pod.pod_id)

    state.activeInfra = ActiveInfra(
        type="pod", podId=pod.pod_id, url=vllm_url,
        gpuType=gpu_type, gpuCount=gpu_count, modelName=pod_config.modelName,
    )
    save_state(oc_home, state)
    oc_env = oc_home / ".env"
    if oc_env.exists():
        lines = oc_env.read_text(encoding="utf-8").splitlines()
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith("VLLM_RUNPOD_URL="):
                lines[i] = f"VLLM_RUNPOD_URL={vllm_url}"
                updated = True
            elif line.strip().startswith("RUNPOD_POD_ID="):
                lines[i] = f"RUNPOD_POD_ID={pod.pod_id}"
                updated = True
        if not updated:
            lines.append(f"VLLM_RUNPOD_URL={vllm_url}")
            lines.append(f"RUNPOD_POD_ID={pod.pod_id}")
        oc_env.write_text("\n".join(lines) + "\n", encoding="utf-8")

    import akos.process as proc
    print()
    print("  Switching environment to gpu-runpod-pod...")
    result = proc.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "switch-model.py"), "gpu-runpod-pod", "--no-restart"],
        timeout=30,
    )
    if result.success:
        print("  Environment switched.")
    else:
        print(f"  Switch warning: {result.stderr[:100]}")

    print()
    print("=" * 60)
    print(f"  Done! Your agent is now using {pod_config.modelName.split('/')[-1]}")
    print(f"  on RunPod ({gpu_type} x{gpu_count})")
    print()
    print(f"  vLLM URL:  {vllm_url}")
    print(f"  Pod ID:    {pod.pod_id}")
    print()
    print("  Next: open the OpenClaw dashboard and send a message.")
    print("=" * 60)
    return 0


def deploy_serverless(*, dry_run: bool = False) -> int:
    print()
    print("=" * 60)
    print("  Deploy Serverless Endpoint")
    print("=" * 60)

    api_key = _ensure_api_key()
    if not api_key:
        print("  No API key. Aborting.")
        return 1

    if dry_run:
        print("  [DRY-RUN] Would run: py scripts/switch-model.py gpu-runpod")
        return 0

    import akos.process as proc
    result = proc.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "switch-model.py"), "gpu-runpod"],
        timeout=120,
        capture=False,
    )
    return 0 if result.success else 1


def check_status() -> int:
    print()
    print("  GPU Infrastructure Status")
    print("  " + "-" * 40)

    oc_home = resolve_openclaw_home()
    state = load_state(oc_home)

    print(f"  Environment:  {state.activeEnvironment or 'unknown'}")
    print(f"  Model:        {state.activeModel or 'unknown'}")
    print(f"  Tier:         {state.activeTier or 'unknown'}")
    print()

    vllm_url = os.environ.get("VLLM_RUNPOD_URL", "")
    oc_env = oc_home / ".env"
    if not vllm_url and oc_env.exists():
        for line in oc_env.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("VLLM_RUNPOD_URL="):
                vllm_url = line.split("=", 1)[1].strip()

    if vllm_url and vllm_url != "http://YOUR_POD_IP:8000/v1":
        print(f"  vLLM URL:     {vllm_url}")
        health = RunPodProvider.probe_vllm_health(vllm_url, timeout=5.0)
        print(f"  vLLM health:  {'healthy' if health.healthy else 'unreachable'}")
    else:
        print("  vLLM URL:     not configured")

    pod_id = os.environ.get("RUNPOD_POD_ID", "")
    if pod_id:
        api_key = os.environ.get("RUNPOD_API_KEY", "")
        if api_key:
            pm = PodManager(api_key)
            pod = pm.get_pod(pod_id)
            if pod:
                print(f"  Pod ID:       {pod.pod_id}")
                print(f"  Pod status:   {pod.status}")
                print(f"  Pod GPU:      {pod.gpu_type} x{pod.gpu_count}")

    print()
    return 0


def teardown_infra(*, dry_run: bool = False) -> int:
    print()
    print("  Tearing down GPU infrastructure...")
    print()

    pod_id = os.environ.get("RUNPOD_POD_ID", "")
    api_key = os.environ.get("RUNPOD_API_KEY", "")

    oc_home = resolve_openclaw_home()
    state = load_state(oc_home)

    if not pod_id and state.activeInfra.podId:
        pod_id = state.activeInfra.podId
    if not api_key:
        api_key = _ensure_api_key()

    if pod_id and api_key:
        if dry_run:
            print(f"  [DRY-RUN] Would terminate pod {pod_id}")
        else:
            pm = PodManager(api_key)
            if pm.terminate_pod(pod_id):
                print(f"  Terminated pod {pod_id}")
            else:
                print(f"  Failed to terminate pod {pod_id}")

    state.activeInfra = ActiveInfra(type="local")
    save_state(oc_home, state)

    if not dry_run:
        import akos.process as proc
        result = proc.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "switch-model.py"), "dev-local", "--no-restart"],
            timeout=30,
        )
        if result.success:
            print("  Switched back to dev-local.")
        print()
        print("  Teardown complete. GPU billing stopped.")
    return 0


def interactive_menu(*, dry_run: bool = False) -> int:
    oc_home = resolve_openclaw_home()
    state = load_state(oc_home)
    env_name = state.activeEnvironment or "dev-local"
    model_name = state.activeModel or "ollama/deepseek-r1:14b"

    print()
    print("  AKOS GPU Infrastructure Manager")
    print("  " + "=" * 36)
    print()
    print(f"  Current: {env_name} ({model_name})")
    print()
    print("  1. Deploy dedicated pod    (RunPod pod + vLLM)")
    print("  2. Deploy serverless       (RunPod auto-scaling)")
    print("  3. Check status            (health of GPU infra)")
    print("  4. Tear down               (stop pod, save money)")
    print("  5. Switch to local         (Ollama dev-local)")
    print("  6. Exit")
    print()

    try:
        choice = input("  Choice [1-6]: ").strip()
    except (EOFError, KeyboardInterrupt):
        return 0

    if choice == "1":
        return deploy_pod(dry_run=dry_run)
    elif choice == "2":
        return deploy_serverless(dry_run=dry_run)
    elif choice == "3":
        return check_status()
    elif choice == "4":
        return teardown_infra(dry_run=dry_run)
    elif choice == "5":
        import akos.process as proc
        proc.run([sys.executable, str(REPO_ROOT / "scripts" / "switch-model.py"), "dev-local"], timeout=30)
        print("  Switched to dev-local.")
        return 0
    else:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AKOS GPU Infrastructure Manager",
        epilog="Run without arguments for interactive menu.",
    )
    parser.add_argument("command", nargs="?", choices=["deploy-pod", "deploy-serverless", "status", "teardown"],
                        help="Direct command (skip menu)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without calling RunPod API")
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    for p in [REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.env",
              REPO_ROOT / "config" / "environments" / "gpu-runpod.env",
              REPO_ROOT / "config" / "eval" / "langfuse.env",
              resolve_openclaw_home() / ".env"]:
        if p.exists():
            for k, v in load_env_file(p).items():
                os.environ.setdefault(k, v)

    if args.command == "deploy-pod":
        return deploy_pod(dry_run=args.dry_run)
    elif args.command == "deploy-serverless":
        return deploy_serverless(dry_run=args.dry_run)
    elif args.command == "status":
        return check_status()
    elif args.command == "teardown":
        return teardown_infra(dry_run=args.dry_run)
    else:
        return interactive_menu(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
