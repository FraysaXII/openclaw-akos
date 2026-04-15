#!/usr/bin/env python3
"""Validate internal markdown links under docs/references/hlk/v3.0/.

Excludes PMO ``imports/`` JSON-heavy trees. Exits 1 on any broken same-repo
``.md`` target resolved from each source file.

Usage:
    py scripts/validate_hlk_vault_links.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_vault_links import validate_vault_internal_links


def main() -> int:
    errors = validate_vault_internal_links()
    if not errors:
        print("validate_hlk_vault_links: PASS (no broken internal .md links)")
        return 0
    for msg in errors:
        print(msg, file=sys.stderr)
    print(f"validate_hlk_vault_links: FAIL ({len(errors)} broken link(s))", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
