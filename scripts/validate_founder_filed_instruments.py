#!/usr/bin/env python3
"""DEPRECATION SHIM — renamed to scripts/validate_filed_instruments.py at I81 P2 T3.

Provides backward-compatible CLI invocation for one initiative cycle
(removal scheduled at I81 P9 closure per D-IH-81-S under D-IH-81-G
umbrella, 2026-05-23). New invocations should use:

    py scripts/validate_filed_instruments.py

This shim simply imports and runs the renamed validator's ``main()``.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_filed_instruments import main  # type: ignore[import-not-found]


if __name__ == "__main__":
    raise SystemExit(main())
