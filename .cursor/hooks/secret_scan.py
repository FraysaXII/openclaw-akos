#!/usr/bin/env python3
"""Cursor hook: block obvious secret patterns in submitted prompts."""

from __future__ import annotations

import json
import re
import sys

_PATTERNS = (
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        json.dump({"continue": True}, sys.stdout)
        return 0

    prompt = str(payload.get("prompt") or payload.get("text") or "")
    for pattern in _PATTERNS:
        if pattern.search(prompt):
            json.dump(
                {
                    "continue": False,
                    "userMessage": "Prompt appears to contain a secret or private key — remove before submitting.",
                },
                sys.stdout,
            )
            return 0

    json.dump({"continue": True}, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
