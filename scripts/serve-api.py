#!/usr/bin/env python3
"""Launch the AKOS FastAPI control plane.

Usage:
    python scripts/serve-api.py                # default port 8420
    python scripts/serve-api.py --port 9000    # custom port
    python scripts/serve-api.py --reload       # auto-reload for dev

Preflight: binds the listen socket before uvicorn starts; on failure prints a
hint (port in use). See USER_GUIDE.md section 9.10.

Requires: Python 3.10+, fastapi, uvicorn.
"""

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

    uvicorn.run(
        "akos.api:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
