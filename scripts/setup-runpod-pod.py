#!/usr/bin/env python3
"""Set up a RunPod dedicated pod for vLLM inference.

Interactive walkthrough: asks for pod ID, generates a single copy-paste
command block for the pod's web terminal, writes the local .env, and
optionally runs switch-model.

Usage:
    py scripts/setup-runpod-pod.py                    # interactive
    py scripts/setup-runpod-pod.py --pod-id <id>      # non-interactive

Requires: Python 3.10+ (stdlib only). vLLM runs on the pod, NOT locally.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT, load_json, resolve_openclaw_home


def _build_vllm_command(pod: dict) -> str:
    """Build the single vLLM launch command from pod config."""
    model = pod.get("modelName", "deepseek-ai/DeepSeek-R1-0528-Distill-Qwen-70B")
    port = pod.get("vllmPort", 8000)
    max_len = pod.get("maxModelLen", 131072)
    env = pod.get("envVars", {})

    parts = [
        "python -m vllm.entrypoints.openai.api_server",
        f"  --model {model}",
        f"  --host 0.0.0.0",
        f"  --port {port}",
        f"  --max-model-len {max_len}",
        f"  --served-model-name {env.get('OPENAI_SERVED_MODEL_NAME_OVERRIDE', 'deepseek-r1-70b')}",
        f"  --dtype {env.get('DTYPE', 'bfloat16')}",
        f"  --gpu-memory-utilization {env.get('GPU_MEMORY_UTILIZATION', '0.92')}",
        f"  --kv-cache-dtype {env.get('KV_CACHE_DTYPE', 'fp8')}",
        f"  --tensor-parallel-size {env.get('TENSOR_PARALLEL_SIZE', '1')}",
    ]
    if env.get("ENABLE_PREFIX_CACHING", "").lower() == "true":
        parts.append("  --enable-prefix-caching")
    if env.get("ENABLE_CHUNKED_PREFILL", "").lower() == "true":
        parts.append("  --enable-chunked-prefill")
    if env.get("ENABLE_AUTO_TOOL_CHOICE", "").lower() == "true":
        parts.append("  --enable-auto-tool-choice")
        if env.get("TOOL_CALL_PARSER"):
            parts.append(f"  --tool-call-parser {env['TOOL_CALL_PARSER']}")
    parts.append(f"  --max-num-seqs {env.get('MAX_NUM_SEQS', '128')}")
    return " \\\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Set up a RunPod dedicated pod for vLLM inference",
        epilog="This script runs LOCALLY. vLLM installs and runs on the POD.",
    )
    parser.add_argument("--pod-id", help="RunPod pod ID (from the dashboard URL or pod name)")
    parser.add_argument(
        "--config",
        default=str(REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.json"),
        help="Path to pod config JSON",
    )
    parser.add_argument("--switch", action="store_true", help="Run switch-model.py after setup")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"  Config not found: {config_path}", file=sys.stderr)
        return 1

    raw = load_json(config_path)
    pod = raw.get("pod")
    if not pod:
        print("  No 'pod' block in config. Use gpu-runpod-pod.json, not gpu-runpod.json.", file=sys.stderr)
        return 1

    port = pod.get("vllmPort", 8000)

    pod_id = args.pod_id
    if not pod_id:
        print()
        print("  RunPod Dedicated Pod Setup")
        print("  " + "-" * 40)
        print()
        print("  Your pod ID is in the RunPod dashboard URL or the pod name.")
        print("  Example: if your pod URL is https://www.runpod.io/console/pods/abc123xyz")
        print("           then the pod ID is: abc123xyz")
        print()
        try:
            pod_id = input("  Enter your RunPod pod ID: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Cancelled.")
            return 1
        if not pod_id:
            print("  No pod ID provided. Exiting.")
            return 1

    vllm_url = f"https://{pod_id}-{port}.proxy.runpod.net/v1"
    vllm_cmd = _build_vllm_command(pod)

    print()
    print("=" * 72)
    print("  RunPod Dedicated Pod Setup")
    print("=" * 72)
    print()
    print("  STEP 1: Expose port 8000 in the RunPod dashboard")
    print("  " + "-" * 50)
    print(f"  Your pod currently exposes: 8888 (Jupyter), 22 (SSH)")
    print(f"  You MUST also expose port {port} for vLLM:")
    print()
    print(f"    1. Go to RunPod dashboard > Pods > your pod > Edit Pod")
    print(f"    2. Under 'Expose HTTP ports', add: {port}")
    print(f"    3. Save (this resets the pod -- data in /workspace persists)")
    print()

    print("  STEP 2: Copy-paste this ENTIRE block into the pod's web terminal")
    print("  " + "-" * 50)
    print()
    print("  Open: RunPod dashboard > Pods > your pod > Connect > Web Terminal")
    print("  Then paste:")
    print()
    print("  " + "~" * 60)
    print()

    script_block = f"""pip install vllm && \\
{vllm_cmd}"""

    for line in script_block.split("\n"):
        print(f"  {line}")

    print()
    print("  " + "~" * 60)
    print()
    print("  Wait for: 'Uvicorn running on http://0.0.0.0:8000'")
    print("  The first run downloads the model (~140 GB). This takes 5-15 minutes.")
    print()

    print("  STEP 3: Verify (from your local machine)")
    print("  " + "-" * 50)
    print(f"  Once vLLM says 'running', test from PowerShell:")
    print()
    print(f'  Invoke-RestMethod -Uri "{vllm_url}/models"')
    print()
    print(f"  You should see a JSON response listing the model.")
    print()

    env_path = REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.env"
    env_example = REPO_ROOT / "config" / "environments" / "gpu-runpod-pod.env.example"
    source = env_path if env_path.exists() else env_example

    if source.exists():
        lines = source.read_text(encoding="utf-8").splitlines()
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("VLLM_RUNPOD_URL="):
                new_lines.append(f"VLLM_RUNPOD_URL={vllm_url}")
            else:
                new_lines.append(line)
        env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print(f"  STEP 4: Local .env updated automatically")
        print(f"  " + "-" * 50)
        print(f"  Wrote VLLM_RUNPOD_URL={vllm_url}")
        print(f"  To: {env_path}")
    else:
        print(f"  STEP 4: Set VLLM_RUNPOD_URL in your local .env")
        print(f"  " + "-" * 50)
        print(f"  VLLM_RUNPOD_URL={vllm_url}")
    print()

    print("  STEP 5: Switch to the dedicated pod environment")
    print("  " + "-" * 50)
    print("  Run this locally (NOT on the pod):")
    print()
    print("  py scripts/switch-model.py gpu-runpod-pod")
    print()

    if args.switch:
        print("  (--switch flag set, running switch-model.py now...)")
        import akos.process as proc
        result = proc.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "switch-model.py"), "gpu-runpod-pod"],
            timeout=30,
        )
        if result.success:
            print("  Switched to gpu-runpod-pod successfully.")
        else:
            print(f"  Switch failed: {result.stderr}")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
