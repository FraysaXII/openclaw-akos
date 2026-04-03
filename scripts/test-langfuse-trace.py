#!/usr/bin/env python3
"""Smoke-test Langfuse connectivity: send a single trace and verify it reaches the dashboard.

Use this to confirm Langfuse credentials work before running the full log-watcher pipeline.
Traces appear under the "Tracing" tab in your Langfuse project.

Usage:
    python scripts/test-langfuse-trace.py
    python scripts/test-langfuse-trace.py --environment gpu-runpod

Requires: langfuse package and LANGFUSE_* credentials in process env or ~/.openclaw/.env.
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import load_runtime_env, resolve_openclaw_home, set_process_env_defaults
from akos.telemetry import LangfuseReporter


def main() -> int:
    parser = argparse.ArgumentParser(description="Send a test trace to Langfuse")
    parser.add_argument(
        "--environment", "-e",
        default=os.environ.get("AKOS_ENV", "dev-local"),
        help="Environment tag (dev-local, gpu-runpod, prod-cloud)",
    )
    args = parser.parse_args()

    oc_env = resolve_openclaw_home() / ".env"
    set_process_env_defaults(load_runtime_env(oc_env.parent))

    env_tag = os.environ.get("AKOS_ENV", args.environment)
    reporter = LangfuseReporter(environment=env_tag)

    if not reporter.enabled:
        print("Langfuse telemetry disabled: no credentials (set LANGFUSE_* in process env or ~/.openclaw/.env)")
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
