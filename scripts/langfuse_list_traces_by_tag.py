#!/usr/bin/env python3
"""List Langfuse trace IDs filtered by tag (datasets / eval prep).

Uses the Langfuse public REST API. Requires ``LANGFUSE_PUBLIC_KEY``,
``LANGFUSE_SECRET_KEY``, and optional ``LANGFUSE_HOST`` (default
``https://cloud.langfuse.com``), loaded from process env or
``~/.openclaw/.env`` via ``akos.io``.

Example::

    py scripts/langfuse_list_traces_by_tag.py --tag madeira --limit 25

Prints one trace id per line (stdout). Traces whose ``tags`` array
contains the requested tag (case-insensitive) are emitted; other
traces in the page are ignored.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import httpx

from akos.io import load_runtime_env, resolve_openclaw_home, set_process_env_defaults


def main() -> int:
    parser = argparse.ArgumentParser(description="List Langfuse trace IDs by tag")
    parser.add_argument("--tag", required=True, help="Tag value to match (e.g. madeira, executor)")
    parser.add_argument("--limit", type=int, default=50, help="Max traces to fetch from API (client-side filter)")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print full JSON objects for matched traces instead of ids only",
    )
    args = parser.parse_args()

    oc_env = resolve_openclaw_home() / ".env"
    set_process_env_defaults(load_runtime_env(oc_env.parent))

    pk = os.environ.get("LANGFUSE_PUBLIC_KEY")
    sk = os.environ.get("LANGFUSE_SECRET_KEY")
    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")

    if not pk or not sk:
        print("Missing LANGFUSE_PUBLIC_KEY or LANGFUSE_SECRET_KEY", file=sys.stderr)
        return 1

    auth = base64.b64encode(f"{pk}:{sk}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    url = f"{host}/api/public/traces"
    params: dict[str, str | int] = {"limit": int(args.limit)}

    try:
        resp = httpx.get(url, headers=headers, params=params, timeout=45.0)
    except httpx.RequestError as exc:
        print(f"HTTP request failed: {exc}", file=sys.stderr)
        return 1

    if resp.status_code != 200:
        print(f"Langfuse API HTTP {resp.status_code}: {resp.text[:500]}", file=sys.stderr)
        return 1

    payload = resp.json()
    traces = payload.get("data") or payload.get("traces") or []
    if not isinstance(traces, list):
        print("Unexpected API response shape (no trace list)", file=sys.stderr)
        return 1

    want = args.tag.strip().lower()
    matched: list[dict] = []
    for tr in traces:
        if not isinstance(tr, dict):
            continue
        tags_raw = tr.get("tags") or []
        tags = [str(t).lower() for t in tags_raw if t is not None]
        if want in tags:
            matched.append(tr)

    if args.json:
        print(json.dumps(matched, indent=2))
    else:
        for tr in matched:
            tid = tr.get("id")
            if tid:
                print(tid)

    if not matched:
        print(
            f"# No traces matched tag {args.tag!r} in this page (limit={args.limit}).",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
