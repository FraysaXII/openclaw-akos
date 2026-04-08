#!/usr/bin/env python3
"""AKOS GPU Infrastructure Manager.

Interactive CLI for deploying, monitoring, and tearing down GPU inference
infrastructure on RunPod and ShadowPC OpenStack.

Usage:
    py scripts/gpu.py                # interactive menu
    py scripts/gpu.py deploy-pod     # RunPod dedicated pod
    py scripts/gpu.py deploy-shadow  # ShadowPC OpenStack instance
    py scripts/gpu.py status         # check health
    py scripts/gpu.py teardown       # stop infrastructure
    py scripts/gpu.py --dry-run      # preview without calling any API

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

from akos.io import (
    REPO_ROOT,
    RUNTIME_ENV_PLACEHOLDERS,
    load_env_file,
    load_json,
    load_runtime_env,
    resolve_openclaw_home,
    save_json,
    set_process_env_defaults,
)
from akos.log import setup_logging
from akos.model_catalog import CatalogEntry, load_catalog
from akos.models import OpenStackInstanceConfig, PodConfig
from akos.runpod_provider import PodManager, RunPodProvider
from akos.state import ActiveInfra, AkosState, load_state, save_state

logger = logging.getLogger("akos.gpu")

_GPU_CATALOG = [
    {"id": "NVIDIA A100-SXM4-80GB", "name": "A100 80GB SXM", "vram": 80, "price_hr": 1.64, "price_sec": 1.64 / 3600, "provider": "runpod"},
    {"id": "NVIDIA A100 80GB PCIe", "name": "A100 80GB PCIe", "vram": 80, "price_hr": 1.64, "price_sec": 1.64 / 3600, "provider": "runpod"},
    {"id": "NVIDIA H100 80GB HBM3", "name": "H100 80GB", "vram": 80, "price_hr": 2.69, "price_sec": 2.69 / 3600, "provider": "runpod"},
    {"id": "NVIDIA H200", "name": "H200", "vram": 141, "price_hr": 3.29, "price_sec": 3.29 / 3600, "provider": "runpod"},
    {"id": "NVIDIA L40S", "name": "L40S 48GB", "vram": 48, "price_hr": 0.74, "price_sec": 0.74 / 3600, "provider": "runpod"},
    {"id": "NVIDIA RTX A6000", "name": "RTX A6000 48GB", "vram": 48, "price_hr": 0.53, "price_sec": 0.53 / 3600, "provider": "runpod"},
    {"id": "NVIDIA GeForce RTX 4090", "name": "RTX 4090 24GB", "vram": 24, "price_hr": 0.44, "price_sec": 0.44 / 3600, "provider": "runpod"},
    {"id": "RTX A4500", "name": "RTX A4500 20GB (Shadow)", "vram": 20, "price_hr": 0.35, "price_sec": 0.35 / 3600, "provider": "shadow"},
    {"id": "RTX 2000 Ada", "name": "RTX 2000 Ada (Shadow)", "vram": 16, "price_hr": 0.29, "price_sec": 0.29 / 3600, "provider": "shadow"},
]


def _ensure_api_key() -> str:
    key = os.environ.get("RUNPOD_API_KEY", "")
    if key and key != "YOUR_RUNPOD_API_KEY":
        return key

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


def _upsert_env_line(path: Path, key: str, value: str) -> None:
    """Insert or update a KEY=value line in an env file."""
    if not path.exists():
        path.write_text("", encoding="utf-8")
    lines = path.read_text(encoding="utf-8").splitlines()
    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            found = True
            break
    if not found:
        lines.append(f"{key}={value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _save_key_to_env(key: str, value: str) -> None:
    """Save a key to both the pod .env and the live ~/.openclaw/.env."""
    _upsert_env_line(REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.env", key, value)
    oc_env = resolve_openclaw_home() / ".env"
    if oc_env.exists():
        _upsert_env_line(oc_env, key, value)


def _ensure_env_placeholders(oc_home: Path) -> None:
    """Re-assert placeholder env vars that OpenCLAW requires for ${VAR} substitution.

    switch-model.py may overwrite ~/.openclaw/.env from a real profile env file.
    If any placeholder got wiped to empty, restore it so the gateway doesn't crash.
    """
    oc_env = oc_home / ".env"
    if not oc_env.exists():
        return
    env = load_env_file(oc_env)
    for key, default in RUNTIME_ENV_PLACEHOLDERS.items():
        if not env.get(key):
            _upsert_env_line(oc_env, key, default)


def _pick_model(catalog: list[CatalogEntry]) -> CatalogEntry:
    """Interactive model picker. Returns the selected catalog entry."""
    print()
    print("  Select model to deploy")
    print("  " + "-" * 40)
    print()
    print(f"  {'#':<4} {'Model':<26} {'Params':<8} {'VRAM':<8} {'Reason':<7} {'Tool parser'}")
    print(f"  {'-'*4} {'-'*26} {'-'*8} {'-'*8} {'-'*7} {'-'*14}")

    for i, entry in enumerate(catalog, 1):
        reason = "yes" if entry.reasoning else "no"
        marker = " *" if i == 1 else ""
        print(f"  {i:<4} {entry.displayName:<26} {entry.paramsBillions}B{'':<4} "
              f"{entry.vramGb}GB{'':<3} {reason:<7} {entry.toolCallParser}{marker}")

    print()
    try:
        choice = input("  Model [1]: ").strip()
    except (EOFError, KeyboardInterrupt):
        return catalog[0]

    if choice and choice.isdigit() and 1 <= int(choice) <= len(catalog):
        return catalog[int(choice) - 1]
    return catalog[0]


def _pick_gpu(model: CatalogEntry) -> tuple[str, int]:
    """Interactive GPU picker driven by the selected model's VRAM needs."""
    default_type = model.defaultGpu.type
    default_count = model.defaultGpu.count

    print()
    print(f"  Recommended GPU: {default_type} x{default_count}"
          f" (model needs {model.vramGb} GB VRAM)")
    print()
    print(f"  {'#':<4} {'GPU':<25} {'VRAM':<10} {'~$/hr':<8}")
    print(f"  {'-'*4} {'-'*25} {'-'*10} {'-'*8}")

    for i, gpu in enumerate(_GPU_CATALOG, 1):
        marker = " *" if gpu["id"] == default_type else ""
        print(f"  {i:<4} {gpu['name']:<25} {gpu['vram']} GB{'':<4} ${gpu['price_hr']:.2f}{marker}")

    print()
    try:
        choice = input("  GPU number [Enter for recommended]: ").strip()
    except (EOFError, KeyboardInterrupt):
        return default_type, default_count

    if choice and choice.isdigit() and 1 <= int(choice) <= len(_GPU_CATALOG):
        gpu = _GPU_CATALOG[int(choice) - 1]
        gpu_type = gpu["id"]
    else:
        gpu_type = default_type

    gpu_vram = next((g["vram"] for g in _GPU_CATALOG if g["id"] == gpu_type), 80)
    min_gpus = model.min_gpus_for(gpu_vram)

    if min_gpus > 1:
        print(f"  Model needs at least {min_gpus} GPUs of this type ({model.vramGb} GB / {gpu_vram} GB each).")
        try:
            count_str = input(f"  GPU count [{min_gpus}]: ").strip()
        except (EOFError, KeyboardInterrupt):
            return gpu_type, min_gpus
        gpu_count = int(count_str) if count_str.isdigit() else min_gpus
        gpu_count = max(gpu_count, min_gpus)
    else:
        gpu_count = 1

    return gpu_type, gpu_count


def _apply_catalog_to_pod_config(pod_config: PodConfig, model: CatalogEntry) -> None:
    """Overwrite PodConfig fields from a catalog entry (mutates in place)."""
    pod_config.modelName = model.hfId
    pod_config.maxModelLen = model.maxModelLen
    pod_config.envVars["OPENAI_SERVED_MODEL_NAME_OVERRIDE"] = model.servedModelName
    pod_config.envVars["ENABLE_AUTO_TOOL_CHOICE"] = "true"
    pod_config.envVars["TOOL_CALL_PARSER"] = model.toolCallParser
    if model.reasoningParser:
        pod_config.envVars["REASONING_PARSER"] = model.reasoningParser
    else:
        pod_config.envVars.pop("REASONING_PARSER", None)
    if model.chatTemplate:
        pod_config.envVars["CHAT_TEMPLATE"] = model.chatTemplate
    else:
        pod_config.envVars.pop("CHAT_TEMPLATE", None)
    for k, v in model.envOverrides.items():
        pod_config.envVars[k] = v


def _update_overlay_json(model: CatalogEntry) -> None:
    """Rewrite gpu-runpod-pod.json to match the selected model."""
    overlay_path = REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.json"
    raw = load_json(overlay_path)
    raw.setdefault("agents", {}).setdefault("defaults", {})
    raw["agents"]["defaults"]["model"] = {
        "primary": f"vllm-runpod/{model.servedModelName}",
        "fallbacks": ["anthropic/claude-sonnet-4", "ollama/deepseek-r1:14b"],
    }
    raw["agents"]["defaults"]["thinkingDefault"] = "medium" if model.reasoning else "off"
    save_json(overlay_path, raw)


def _update_serverless_overlay_json(model: CatalogEntry) -> None:
    """Rewrite gpu-runpod.json to match the selected model."""
    overlay_path = REPO_ROOT / "config" / "environments" / "gpu-runpod.json"
    raw = load_json(overlay_path)
    raw.setdefault("agents", {}).setdefault("defaults", {})
    raw["agents"]["defaults"]["model"] = {
        "primary": f"vllm-runpod/{model.servedModelName}",
        "fallbacks": ["anthropic/claude-sonnet-4", "ollama/deepseek-r1:14b"],
    }
    raw["agents"]["defaults"]["thinkingDefault"] = "medium" if model.reasoning else "off"
    runpod = raw.setdefault("runpod", {})
    runpod["templateName"] = f"akos-vllm-{model.servedModelName}"
    runpod["modelName"] = model.hfId
    runpod["maxModelLen"] = model.maxModelLen
    env = runpod.setdefault("envVars", {})
    env["OPENAI_SERVED_MODEL_NAME_OVERRIDE"] = model.servedModelName
    env["ENABLE_AUTO_TOOL_CHOICE"] = "true"
    env["TOOL_CALL_PARSER"] = model.toolCallParser
    if model.reasoningParser:
        env["REASONING_PARSER"] = model.reasoningParser
    else:
        env.pop("REASONING_PARSER", None)
    if model.chatTemplate:
        env["CHAT_TEMPLATE"] = model.chatTemplate
    else:
        env.pop("CHAT_TEMPLATE", None)
    for k, v in model.envOverrides.items():
        env[k] = v
    image = str(runpod.get("vllmImage") or "runpod/worker-v1-vllm:v2.14.0")
    runpod["vllmImage"] = image
    if image.lower().startswith("runpod/worker-v1-vllm"):
        # RunPod's worker image can attempt FlashInfer JIT builds that require nvcc.
        # Keep serverless defaults on a non-JIT path for deterministic startup.
        if env.get("QUANTIZATION", "").lower() == "awq":
            env["DTYPE"] = "float16"
        if env.get("KV_CACHE_DTYPE", "").lower() == "fp8":
            env["KV_CACHE_DTYPE"] = "auto"
        env.setdefault("VLLM_ATTENTION_BACKEND", "TRITON_ATTN")
    save_json(overlay_path, raw)


def _print_completion_summary(
    *,
    mode: str,
    model: CatalogEntry,
    url: str = "",
    gpu_type: str = "",
    gpu_count: int = 0,
    cost_hint: str = "",
) -> None:
    print()
    print("=" * 60)
    print(f"  Deployment Summary ({mode})")
    print("=" * 60)
    print(f"  Model:      {model.displayName}")
    print(f"  HF ID:      {model.hfId}")
    if gpu_type:
        print(f"  GPU:        {gpu_type} x{gpu_count}")
    if url:
        print(f"  URL:        {url}")
    if cost_hint:
        print(f"  Cost:       {cost_hint}")
    print(f"  Reasoning:  {'yes' if model.reasoning else 'no'}")
    print("  Next:       open the OpenClaw dashboard and send a message.")
    print("=" * 60)


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

    catalog = load_catalog()
    model = _pick_model(catalog)

    gpu_type, gpu_count = _pick_gpu(model)

    config_path = REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.json"
    raw = load_json(config_path)
    pod_config = PodConfig.model_validate(raw.get("pod", {}))

    pod_config.gpuCount = gpu_count
    pod_config.gpuType = gpu_type
    pod_config.envVars["TENSOR_PARALLEL_SIZE"] = str(gpu_count)
    _apply_catalog_to_pod_config(pod_config, model)

    vllm_cmd = pod_config.build_vllm_command()
    port = pod_config.vllmPort
    env_vars = {
        **({"HF_TOKEN": hf_token} if hf_token else {}),
        **pod_config.envVars,
    }

    print()
    print(f"  Model:     {model.hfId}")
    print(f"  Family:    {model.family} (parser: {model.toolCallParser})")
    print(f"  GPU:       {gpu_type} x{gpu_count}")
    print(f"  Port:      {port}")
    print(f"  Image:     {pod_config.containerImage}")
    print(f"  Volume:    {pod_config.volumeGb} GB")
    print(f"  TP size:   {gpu_count} (auto-derived from GPU count)")
    print(f"  Reasoning: {'yes' if model.reasoning else 'no'}")
    print()

    if dry_run:
        print("  [DRY-RUN] Would create pod with above config.")
        print(f"  [DRY-RUN] vLLM command: {' '.join(vllm_cmd)}")
        return 0

    _update_overlay_json(model)

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
        name=f"akos-vllm-{model.servedModelName[:30]}",
        gpu_type_id=gpu_type,
        gpu_count=gpu_count,
        image=pod_config.containerImage,
        container_disk_gb=pod_config.containerDiskGb,
        volume_gb=pod_config.volumeGb,
        ports=[f"{port}/http", "22/tcp"],
        env=env_vars,
        docker_start_cmd=vllm_cmd,
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
        gpuType=gpu_type, gpuCount=gpu_count, modelName=model.hfId,
    )
    save_state(oc_home, state)

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

    _save_key_to_env("VLLM_RUNPOD_URL", vllm_url)
    _save_key_to_env("RUNPOD_POD_ID", pod.pod_id)
    _ensure_env_placeholders(oc_home)

    print()
    print("=" * 60)
    print(f"  Done! Your agent is now using {model.displayName}")
    print(f"  on RunPod ({gpu_type} x{gpu_count})")
    print()
    print(f"  vLLM URL:  {vllm_url}")
    print(f"  Pod ID:    {pod.pod_id}")
    print(f"  Tools:     {model.toolCallParser}")
    if model.reasoning:
        print(f"  Reasoning: {model.reasoningParser}")
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

    catalog = load_catalog()
    model = _pick_model(catalog)
    _update_serverless_overlay_json(model)

    if dry_run:
        _print_completion_summary(
            mode="Serverless endpoint",
            model=model,
            cost_hint="pay-per-request / no idle cost",
        )
        print("  [DRY-RUN] Would run: py scripts/switch-model.py gpu-runpod")
        return 0

    import akos.process as proc
    result = proc.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "switch-model.py"), "gpu-runpod"],
        timeout=120,
        capture=False,
    )
    if not result.success:
        return 1

    oc_home = resolve_openclaw_home()
    env = load_env_file(oc_home / ".env")
    state = load_state(oc_home)
    state.activeInfra = ActiveInfra(
        type="serverless",
        endpointId=env.get("RUNPOD_ENDPOINT_ID", ""),
        url=env.get("VLLM_RUNPOD_URL", ""),
        modelName=model.hfId,
    )
    save_state(oc_home, state)
    _ensure_env_placeholders(oc_home)

    _print_completion_summary(
        mode="Serverless endpoint",
        model=model,
        url=env.get("VLLM_RUNPOD_URL", ""),
        cost_hint="pay-per-request / no idle cost",
    )
    return 0


def _update_shadow_overlay_json(model: CatalogEntry) -> None:
    """Rewrite gpu-shadow.json to match the selected model."""
    overlay_path = REPO_ROOT / "config" / "environments" / "gpu-shadow.json"
    raw = load_json(overlay_path)
    raw.setdefault("agents", {}).setdefault("defaults", {})
    raw["agents"]["defaults"]["model"] = {
        "primary": f"vllm-shadow/{model.servedModelName}",
        "fallbacks": ["anthropic/claude-sonnet-4", "ollama/deepseek-r1:14b"],
    }
    raw["agents"]["defaults"]["thinkingDefault"] = "medium" if model.reasoning else "off"
    os_cfg = raw.setdefault("openstack", {})
    os_cfg["modelName"] = model.hfId
    os_cfg["maxModelLen"] = model.maxModelLen
    env = os_cfg.setdefault("envVars", {})
    env["OPENAI_SERVED_MODEL_NAME_OVERRIDE"] = model.servedModelName
    env["ENABLE_AUTO_TOOL_CHOICE"] = "true"
    env["TOOL_CALL_PARSER"] = model.toolCallParser
    if model.reasoningParser:
        env["REASONING_PARSER"] = model.reasoningParser
    else:
        env.pop("REASONING_PARSER", None)
    if model.chatTemplate:
        env["CHAT_TEMPLATE"] = model.chatTemplate
    else:
        env.pop("CHAT_TEMPLATE", None)
    if model.quantization:
        env["QUANTIZATION"] = model.quantization
    for k, v in model.envOverrides.items():
        env[k] = v
    save_json(overlay_path, raw)


def _save_shadow_key_to_env(key: str, value: str) -> None:
    """Save a key to both the Shadow .env and the live ~/.openclaw/.env."""
    _upsert_env_line(REPO_ROOT / "config" / "environments" / "gpu-shadow.env", key, value)
    oc_env = resolve_openclaw_home() / ".env"
    if oc_env.exists():
        _upsert_env_line(oc_env, key, value)


def deploy_shadow(*, dry_run: bool = False) -> int:
    """Deploy vLLM on a ShadowPC OpenStack GPU instance."""
    from akos.openstack_provider import OpenStackProvider

    print()
    print("=" * 60)
    print("  Deploy ShadowPC OpenStack Instance")
    print("=" * 60)

    shadow_env_path = REPO_ROOT / "config" / "environments" / "gpu-shadow.env"
    if shadow_env_path.exists():
        for k, v in load_env_file(shadow_env_path).items():
            if v:
                os.environ.setdefault(k, v)

    auth_url = os.environ.get("OS_AUTH_URL", "")
    if not auth_url:
        print("  OS_AUTH_URL not set. Populate config/environments/gpu-shadow.env")
        print("  with your OpenStack credentials or a valid OS_CLOUD entry.")
        return 1

    hf_token = _ensure_hf_token()

    catalog = load_catalog()
    model = _pick_model(catalog)

    config_path = REPO_ROOT / "config" / "environments" / "gpu-shadow.json"
    raw = load_json(config_path)
    os_config = OpenStackInstanceConfig.model_validate(raw.get("openstack", {}))

    print()
    print(f"  Model:     {model.hfId}")
    print(f"  Family:    {model.family} (parser: {model.toolCallParser})")
    print(f"  GPU:       {os_config.gpuType} x{os_config.gpuCount} ({os_config.gpuVramGb}GB each)")
    print(f"  Region:    {os_config.region}")
    print(f"  Flavor:    {os_config.flavor}")
    print(f"  Image:     {os_config.image}")
    print(f"  Quant:     {model.quantization or 'none'}")
    print(f"  Reasoning: {'yes' if model.reasoning else 'no'}")
    print()

    total_vram = os_config.gpuCount * os_config.gpuVramGb
    if model.vramGb > total_vram:
        print(f"  WARNING: Model needs {model.vramGb}GB VRAM but instance has {total_vram}GB.")
        print(f"  Consider a quantized variant or more GPUs.")
        print()

    if dry_run:
        print("  [DRY-RUN] Would create instance with above config.")
        return 0

    _update_shadow_overlay_json(model)

    provider = OpenStackProvider()
    if not provider.enabled:
        print("  OpenStack provider could not connect. Check credentials.")
        return 1

    security_groups: list[dict[str, str]] | None = None
    if os_config.securityGroup:
        sg_id = provider.ensure_security_group(
            name=os_config.securityGroup,
            vllm_port=os_config.vllmPort,
        )
        if sg_id:
            print(f"  Security group: {sg_id}")
            security_groups = [{"name": os_config.securityGroup}]
        else:
            print("  Security group: policy-restricted or unavailable; using project defaults")
    else:
        print("  Security group: omitted (project defaults)")

    env_vars = dict(os_config.envVars)
    env_vars["TENSOR_PARALLEL_SIZE"] = str(os_config.gpuCount)
    env_vars["OPENAI_SERVED_MODEL_NAME_OVERRIDE"] = model.servedModelName
    env_vars["ENABLE_AUTO_TOOL_CHOICE"] = "true"
    env_vars["TOOL_CALL_PARSER"] = model.toolCallParser
    if model.reasoningParser:
        env_vars["REASONING_PARSER"] = model.reasoningParser
    if model.quantization:
        env_vars["QUANTIZATION"] = model.quantization
    for k, v in model.envOverrides.items():
        env_vars[k] = v

    pod_config = PodConfig(
        vllmPort=os_config.vllmPort,
        modelName=model.hfId,
        maxModelLen=os_config.maxModelLen,
        gpuCount=os_config.gpuCount,
        envVars=env_vars,
    )
    vllm_cmd = pod_config.build_vllm_command()

    instance_name = f"akos-vllm-{model.servedModelName[:24]}"
    print(f"  Creating instance '{instance_name}'...")

    use_spot = os_config.spotFlavor != ""
    flavor = os_config.spotFlavor if use_spot else os_config.flavor

    instance = provider.create_instance(
        name=instance_name,
        flavor=flavor,
        image=os_config.image,
        network=os_config.network,
        security_groups=security_groups,
        vllm_args=vllm_cmd,
        vllm_port=os_config.vllmPort,
        hf_token=hf_token,
    )

    if not instance:
        print("  Instance creation failed. Check flavor availability and credentials.")
        return 1

    print(f"  Instance created: {instance.instance_id}")
    print(f"  Status: {instance.status}")
    print()

    if not instance.floating_ip:
        print("  Assigning floating IP...")
        fip = provider.assign_floating_ip(instance.instance_id)
        if fip:
            instance.floating_ip = fip
            instance.url = f"http://{fip}:{os_config.vllmPort}/v1"
            print(f"  Floating IP: {fip}")
        else:
            print("  WARNING: Could not assign floating IP. Set VLLM_SHADOW_URL manually.")

    vllm_url = instance.url or f"http://{instance.ip_address}:{os_config.vllmPort}/v1"

    print()
    print("  Waiting for vLLM to start (cloud-init + model download)...")
    print("  This takes 10-20 minutes for the first run.")
    print()

    start = time.monotonic()
    timeout = 25 * 60
    while time.monotonic() - start < timeout:
        elapsed = int(time.monotonic() - start)
        health = OpenStackProvider.probe_vllm_health(vllm_url, timeout=5.0)
        if health.get("healthy"):
            print(f"\n  vLLM is healthy! ({elapsed}s)")
            break

        if use_spot:
            term = provider.check_spot_termination(instance.instance_id)
            if term.scheduled:
                print(f"\n  SPOT TERMINATION scheduled at {term.termination_at}!")
                print("  Attempting to save state...")
                break

        mins, secs = divmod(elapsed, 60)
        print(f"  [{mins:02d}:{secs:02d}] Waiting for vLLM...", end="\r")
        time.sleep(20)
    else:
        print(f"\n  Timeout after {timeout // 60} minutes. Instance may still be loading.")
        print(f"  Check Skyline dashboard: https://portal.{os_config.region.lower()}.os.shadow.tech/")
        print(f"  URL will be: {vllm_url}")

    _save_shadow_key_to_env("VLLM_SHADOW_URL", vllm_url)

    oc_home = resolve_openclaw_home()
    state = load_state(oc_home)
    state.activeInfra = ActiveInfra(
        type="openstack",
        podId=instance.instance_id,
        url=vllm_url,
        gpuType=os_config.gpuType,
        gpuCount=os_config.gpuCount,
        modelName=model.hfId,
    )
    save_state(oc_home, state)

    import akos.process as proc
    print()
    print("  Switching environment to gpu-shadow...")
    result = proc.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "switch-model.py"), "gpu-shadow", "--no-restart"],
        timeout=30,
    )
    if result.success:
        print("  Environment switched.")
    else:
        print(f"  Switch warning: {result.stderr[:100]}")

    _save_shadow_key_to_env("VLLM_SHADOW_URL", vllm_url)
    _ensure_env_placeholders(oc_home)

    _print_completion_summary(
        mode="ShadowPC OpenStack",
        model=model,
        url=vllm_url,
        gpu_type=os_config.gpuType,
        gpu_count=os_config.gpuCount,
        cost_hint=f"~EUR {os_config.gpuCount * 0.35:.2f}/hr (spot)" if use_spot else f"~EUR {os_config.gpuCount * 250}/mo (guaranteed)",
    )
    return 0


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

    vllm_url_shadow = os.environ.get("VLLM_SHADOW_URL", "")
    if not vllm_url_shadow and oc_env.exists():
        for line in oc_env.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("VLLM_SHADOW_URL="):
                vllm_url_shadow = line.split("=", 1)[1].strip()

    active_url = vllm_url or vllm_url_shadow
    if state.activeInfra.type == "openstack" and vllm_url_shadow:
        active_url = vllm_url_shadow

    if active_url and active_url not in ("http://YOUR_POD_IP:8000/v1", "http://localhost:8080/v1"):
        print(f"  vLLM URL:     {active_url}")
        health = RunPodProvider.probe_vllm_health(active_url, timeout=5.0)
        print(f"  vLLM health:  {'healthy' if health.healthy else 'unreachable'}")
    else:
        print("  vLLM URL:     not configured")

    if state.activeInfra.type == "openstack":
        print(f"  Provider:     ShadowPC OpenStack")
        print(f"  Instance ID:  {state.activeInfra.podId}")
        print(f"  GPU:          {state.activeInfra.gpuType} x{state.activeInfra.gpuCount}")
    else:
        pod_id = os.environ.get("RUNPOD_POD_ID", "")
        if pod_id:
            api_key = os.environ.get("RUNPOD_API_KEY", "")
            if api_key:
                pm = PodManager(api_key)
                pod = pm.get_pod(pod_id)
                if pod:
                    print(f"  Provider:     RunPod")
                    print(f"  Pod ID:       {pod.pod_id}")
                    print(f"  Pod status:   {pod.status}")
                    print(f"  Pod GPU:      {pod.gpu_type} x{pod.gpu_count}")

    print()
    return 0


def teardown_infra(*, dry_run: bool = False) -> int:
    print()
    print("  Tearing down GPU infrastructure...")
    print()

    oc_home = resolve_openclaw_home()
    state = load_state(oc_home)

    if state.activeInfra.type == "openstack":
        from akos.openstack_provider import OpenStackProvider
        instance_id = state.activeInfra.podId
        if instance_id:
            if dry_run:
                print(f"  [DRY-RUN] Would delete OpenStack instance {instance_id}")
            else:
                provider = OpenStackProvider()
                if provider.enabled and provider.delete_instance(instance_id):
                    print(f"  Deleted OpenStack instance {instance_id}")
                else:
                    print(f"  Failed to delete instance {instance_id}")
    else:
        pod_id = os.environ.get("RUNPOD_POD_ID", "")
        api_key = os.environ.get("RUNPOD_API_KEY", "")
        if not pod_id and state.activeInfra.podId:
            pod_id = state.activeInfra.podId
        if not api_key:
            api_key = _ensure_api_key()
        if pod_id and api_key:
            if dry_run:
                print(f"  [DRY-RUN] Would terminate RunPod pod {pod_id}")
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
    print("  How do you want to run your model?")
    print()
    print("  1. RunPod Pod        Always-on GPU, fixed cost, fastest cold start")
    print("                       Best for: development, testing, sustained workloads")
    print()
    print("  2. RunPod Serverless Auto-scaled, pay-per-request, zero idle cost")
    print("                       Best for: intermittent usage and production entry points")
    print()
    print("  3. ShadowPC (EU)     OpenStack GPU instance, sovereign EU data center")
    print("                       Best for: GDPR compliance, RTX A4500 spot/guaranteed")
    print()
    print("  4. Check status            (health of GPU infra)")
    print("  5. Tear down               (stop pod/instance, save money)")
    print("  6. Switch to local         (Ollama dev-local)")
    print("  7. Exit")
    print()

    try:
        choice = input("  Choice [1-7]: ").strip()
    except (EOFError, KeyboardInterrupt):
        return 0

    if choice == "1":
        return deploy_pod(dry_run=dry_run)
    elif choice == "2":
        return deploy_serverless(dry_run=dry_run)
    elif choice == "3":
        return deploy_shadow(dry_run=dry_run)
    elif choice == "4":
        return check_status()
    elif choice == "5":
        return teardown_infra(dry_run=dry_run)
    elif choice == "6":
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
    parser.add_argument("command", nargs="?",
                        choices=["deploy-pod", "deploy-serverless", "deploy-shadow", "status", "teardown"],
                        help="Direct command (skip menu)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without calling RunPod API")
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    for p in [REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.env",
              REPO_ROOT / "config" / "environments" / "gpu-runpod.env",
              REPO_ROOT / "config" / "environments" / "gpu-shadow.env"]:
        if p.exists():
            for k, v in load_env_file(p).items():
                if v:
                    os.environ.setdefault(k, v)
    set_process_env_defaults(load_runtime_env(resolve_openclaw_home()))

    if args.command == "deploy-pod":
        return deploy_pod(dry_run=args.dry_run)
    elif args.command == "deploy-serverless":
        return deploy_serverless(dry_run=args.dry_run)
    elif args.command == "deploy-shadow":
        return deploy_shadow(dry_run=args.dry_run)
    elif args.command == "status":
        return check_status()
    elif args.command == "teardown":
        return teardown_infra(dry_run=args.dry_run)
    else:
        return interactive_menu(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
