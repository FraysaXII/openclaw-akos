#!/usr/bin/env python3
"""Generate vLLM launch commands for a RunPod dedicated pod.

Reads the vLLM configuration from gpu-runpod-pod.json and outputs
copy-paste commands for the pod's SSH session or web terminal.

Usage:
    python scripts/setup-runpod-pod.py
    python scripts/setup-runpod-pod.py --pod-id <id>   # include proxy URL in output

Requires: Python 3.10+ (stdlib only).
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT, load_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate vLLM pod setup commands")
    parser.add_argument(
        "--pod-id",
        help="RunPod pod ID (for generating proxy URL)",
    )
    parser.add_argument(
        "--config",
        default=str(REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.json"),
        help="Path to pod config JSON",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config not found: {config_path}", file=sys.stderr)
        return 1

    raw = load_json(config_path)
    pod = raw.get("pod")
    if not pod:
        print("No 'pod' block in config -- use gpu-runpod-pod.json, not gpu-runpod.json", file=sys.stderr)
        return 1

    model_name = pod.get("modelName", "deepseek-ai/DeepSeek-R1-0528-Distill-Qwen-70B")
    max_model_len = pod.get("maxModelLen", 131072)
    port = pod.get("vllmPort", 8000)
    env_vars = pod.get("envVars", {})

    env_flags = " \\\n    ".join(f"--{k.lower().replace('_', '-')} {v}" for k, v in env_vars.items()
                                  if k not in ("MAX_MODEL_LEN", "OPENAI_SERVED_MODEL_NAME_OVERRIDE",
                                               "MAX_CONCURRENCY", "DISABLE_LOG_STATS", "RAW_OPENAI_OUTPUT"))

    env_exports = "\n".join(f"export {k}={v}" for k, v in env_vars.items())

    print("=" * 72)
    print("  vLLM Setup Commands for RunPod Dedicated Pod")
    print("=" * 72)
    print()
    print("Run these commands in your pod's SSH session or web terminal.")
    print("Config source:", config_path.name)
    print()

    print("# Step 1: Install vLLM")
    print("pip install vllm")
    print()

    print("# Step 2: Set environment variables")
    print(env_exports)
    print()

    print("# Step 3: Launch vLLM OpenAI-compatible server")
    print(f"python -m vllm.entrypoints.openai.api_server \\")
    print(f"    --model {model_name} \\")
    print(f"    --host 0.0.0.0 \\")
    print(f"    --port {port} \\")
    print(f"    --max-model-len {max_model_len} \\")
    print(f"    --served-model-name {env_vars.get('OPENAI_SERVED_MODEL_NAME_OVERRIDE', 'deepseek-r1-70b')} \\")
    print(f"    --dtype {env_vars.get('DTYPE', 'bfloat16')} \\")
    print(f"    --gpu-memory-utilization {env_vars.get('GPU_MEMORY_UTILIZATION', '0.92')} \\")
    print(f"    --kv-cache-dtype {env_vars.get('KV_CACHE_DTYPE', 'fp8')} \\")
    print(f"    --tensor-parallel-size {env_vars.get('TENSOR_PARALLEL_SIZE', '1')} \\")
    if env_vars.get("ENABLE_PREFIX_CACHING", "").lower() == "true":
        print(f"    --enable-prefix-caching \\")
    if env_vars.get("ENABLE_CHUNKED_PREFILL", "").lower() == "true":
        print(f"    --enable-chunked-prefill \\")
    if env_vars.get("ENABLE_AUTO_TOOL_CHOICE", "").lower() == "true":
        print(f"    --enable-auto-tool-choice \\")
        if env_vars.get("TOOL_CALL_PARSER"):
            print(f"    --tool-call-parser {env_vars['TOOL_CALL_PARSER']} \\")
    print(f"    --max-num-seqs {env_vars.get('MAX_NUM_SEQS', '128')}")
    print()

    print("# Step 4: Set VLLM_RUNPOD_URL in your local .env")
    if args.pod_id:
        url = f"https://{args.pod_id}-{port}.proxy.runpod.net/v1"
        print(f"# Your pod proxy URL:")
        print(f"VLLM_RUNPOD_URL={url}")
    else:
        print("# Replace <pod-id> with your RunPod pod ID:")
        print(f"VLLM_RUNPOD_URL=https://<pod-id>-{port}.proxy.runpod.net/v1")
    print()

    print("# Step 5: Switch to the dedicated pod environment locally")
    print("py scripts/switch-model.py gpu-runpod-pod")
    print()
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
