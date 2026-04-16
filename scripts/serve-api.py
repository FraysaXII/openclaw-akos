#!/usr/bin/env python3
"""Launch the AKOS FastAPI control plane.

Usage:
    python scripts/serve-api.py                # default port 8420
    python scripts/serve-api.py --port 9000    # custom port
    python scripts/serve-api.py --reload       # auto-reload for dev

When ``NEO4J_*`` is set to non-placeholder values and Bolt is reachable, starts
the Streamlit graph explorer as a **supervised child process** (never inside the
OpenClaw gateway). Disable with ``--no-graph-explorer`` or ``AKOS_GRAPH_EXPLORER=0``.

Preflight: binds the listen socket before uvicorn starts; on failure prints a
hint (port in use). See USER_GUIDE.md section 9.10.

Requires: Python 3.10+, fastapi, uvicorn.
"""

from __future__ import annotations

import argparse
import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def _preflight_bind(host: str, port: int) -> None:
    """Fail fast with operator hint if the listen port is already in use."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
    except OSError as exc:
        print(
            f"ERROR: cannot bind {host}:{port} ({exc}). "
            "Another process may be using this port (stale serve-api or wrong app). "
            f"Windows: netstat -ano | findstr :{port} then tasklist /FI \"PID eq <pid>\". "
            "See docs/USER_GUIDE.md section 9.10 (control plane default URL and port conflicts).",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    finally:
        s.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="AKOS Control Plane API")
    parser.add_argument("--port", type=int, default=8420, help="Port to listen on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--reload", action="store_true", help="Auto-reload on changes")
    parser.add_argument(
        "--no-graph-explorer",
        action="store_true",
        help="Do not auto-start Streamlit graph explorer (CI / headless)",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        dest="open_browser",
        help="Open graph explorer URL in default browser after start (avoid on shared jump hosts)",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Bearer token for API auth (overrides AKOS_API_KEY env var)",
    )
    args = parser.parse_args()

    import os

    from akos.io import load_runtime_env, resolve_openclaw_home, set_process_env_defaults

    set_process_env_defaults(load_runtime_env(resolve_openclaw_home()))

    if args.api_key:
        os.environ["AKOS_API_KEY"] = args.api_key

    _preflight_bind(args.host, args.port)

    import uvicorn

    from akos.graph_stack import GraphStackSupervisor, set_graph_stack_supervisor

    sup: GraphStackSupervisor | None = None
    if not args.reload:
        import akos.api as akos_api

        sup = GraphStackSupervisor(
            api_host=args.host,
            api_port=args.port,
            on_sync_success=akos_api.reset_neo4j_driver_cache,
        )
        sup.start_explorer_if_enabled(
            no_graph_explorer=args.no_graph_explorer,
            open_browser=args.open_browser,
        )
        sup.start_mirror_autosync_if_enabled()
        set_graph_stack_supervisor(sup)
        url = sup.explorer_public_url()
        if url:
            print(f"AKOS_GRAPH_EXPLORER_URL={url}", flush=True)
    else:
        print(
            "Note: --reload skips graph explorer + mirror autosupervisor (avoid duplicate children). "
            "Use serve-api without --reload for full graph stack.",
            flush=True,
        )

    try:
        uvicorn.run(
            "akos.api:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="info",
        )
    finally:
        if sup is not None:
            sup.shutdown()
        set_graph_stack_supervisor(None)


if __name__ == "__main__":
    main()
