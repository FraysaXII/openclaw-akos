#!/usr/bin/env python3
"""Smoke-test Langfuse connectivity: send a single trace and verify it reaches the dashboard.

Use this to confirm Langfuse credentials work before running the full log-watcher pipeline.
Traces appear under the "Tracing" tab in your Langfuse project.

Usage:
    python scripts/test-langfuse-trace.py
    python scripts/test-langfuse-trace.py --environment gpu-runpod
    python scripts/test-langfuse-trace.py --env-file config/eval/langfuse.env

Requires: langfuse package, config/eval/langfuse.env with LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT, load_env_file, resolve_openclaw_home
from akos.telemetry import LangfuseReporter


def main() -> int:
    default_env = str(REPO_ROOT / "config" / "eval" / "langfuse.env")
    parser = argparse.ArgumentParser(description="Send a test trace to Langfuse")
    parser.add_argument(
        "--env-file",
        default=default_env,
        help="Path to Langfuse .env file",
    )
    parser.add_argument(
        "--environment", "-e",
        default=os.environ.get("AKOS_ENV", "dev-local"),
        help="Environment tag (dev-local, gpu-runpod, prod-cloud)",
    )
    args = parser.parse_args()

    env_path = Path(args.env_file)
    env_vars = load_env_file(env_path)
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value

    oc_env = resolve_openclaw_home() / ".env"
    oc_vars = load_env_file(oc_env)
    for key, value in oc_vars.items():
        if key not in os.environ:
            os.environ[key] = value

    env_tag = os.environ.get("AKOS_ENV", args.environment)
    reporter = LangfuseReporter(environment=env_tag)

    if not reporter.enabled:
        print("Langfuse telemetry disabled: no credentials (set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY)")
        return 1

    reporter.trace_request({
        "agent_role": "test-script",
        "tool_name": "test-langfuse-trace",
        "outcome": "Smoke test trace from openclaw-akos",
        "input": "scripts/test-langfuse-trace.py",
    })
    reporter.flush()

    print(f"Test trace sent to Langfuse successfully (environment={env_tag})")
    print("Check the Tracing tab in your Langfuse project to see it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
