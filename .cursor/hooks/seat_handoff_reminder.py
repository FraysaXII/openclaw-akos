#!/usr/bin/env python3
"""Cursor hook: remind operator of two-seat handoff markers at session stop."""

from __future__ import annotations

import json
import sys


def main() -> int:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass
    sys.stderr.write(
        "[akos] Session stop — if thinking work finished, paste "
        "=== OPUS DONE -> SWITCH TO COMPOSER === or "
        "=== THINKING DONE — operator review === for the next seat. "
        "(See docs/guides/cursor-two-seat-routing.md)\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
