#!/usr/bin/env python3
"""Launch the AKOS FastAPI control plane.

Usage:
    python scripts/serve-api.py                # default port 8420
    python scripts/serve-api.py --port 9000    # custom port
    python scripts/serve-api.py --reload       # auto-reload for dev

Requires: Python 3.10+, fastapi, uvicorn.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


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

    from akos.io import load_env_file
    langfuse_env = Path(__file__).resolve().parent.parent / "config" / "eval" / "langfuse.env"
    for key, value in load_env_file(langfuse_env).items():
        os.environ.setdefault(key, value)

    if args.api_key:
        os.environ["AKOS_API_KEY"] = args.api_key

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
