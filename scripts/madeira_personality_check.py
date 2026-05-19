"""Madeira self-policing call surface per I76 P3.

Paired runbook for the personality SOP (`SOP-TECH_MADEIRA_PERSONALITY_001.md`)
which is forward-chartered to Lane B of I76 P3 pending voice canonical
research closure. This runbook is already shipped as the call surface
because Madeira (current AI O5-1) self-polices EVERY output before showing
it to the operator: the BBR scanner from `akos.brand_baseline_reality`
checks the draft against the dual-register contract per `D-IH-66-M` +
`D-IH-89-E`.

Usage::

    py scripts/madeira_personality_check.py --text "Some draft text."
    echo "Some draft text." | py scripts/madeira_personality_check.py
    py scripts/madeira_personality_check.py --text "..." --json

Exit codes:

    0 - no internal-register tokens detected (output is clean for external
        audiences; safe to show operator).
    1 - one or more internal-register tokens detected (Madeira must
        translate to external register OR confirm the audience tag is
        operator-private / operator-only before showing operator).

Per `akos-brand-baseline-reality.mdc` and `akos-external-render-discipline.mdc`:
this runbook is the *vocabulary axis* check. Madeira pairs it with
`scripts/validate_external_render_trail.py` (the *render-format axis* check)
when the output is destined for an external recipient.

The runbook is intentionally lightweight (stdin / --text only; no file I/O
on the input). Madeira's normal flow: assemble a draft in memory, pipe
through this check, surface findings inline before responding.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.brand_baseline_reality import BaselineHit, scan_text
from akos.log import setup_logging

LOG = logging.getLogger("madeira_personality_check")


def _read_input(text_arg: str | None) -> str:
    """Resolve the input text from --text or stdin."""
    if text_arg is not None:
        return text_arg
    if sys.stdin.isatty():
        # No piped input AND no --text flag -- print a hint, return empty.
        return ""
    return sys.stdin.read()


def _format_hits_human(hits: list[BaselineHit]) -> str:
    if not hits:
        return "CLEAN — no internal-register tokens detected."
    lines = [f"FINDINGS — {len(hits)} internal-register hit(s) before showing operator:"]
    for hit in hits:
        lines.append(
            f"  line {hit.line}: token {hit.token.token!r} -- {hit.snippet}"
        )
    lines.append(
        "Translate to external register OR confirm audience is operator-private "
        "before depending on this output."
    )
    return "\n".join(lines)


def _format_hits_json(hits: list[BaselineHit]) -> str:
    payload = {
        "verdict": "CLEAN" if not hits else "FINDINGS",
        "findings_count": len(hits),
        "findings": [
            {
                "line": h.line,
                "token": h.token.token,
                "snippet": h.snippet,
            }
            for h in hits
        ],
    }
    return json.dumps(payload, indent=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Madeira per-output BBR self-policing check (I76 P3 paired runbook for the "
            "personality SOP). Scans for internal-register token leaks per "
            "BRAND_BASELINE_REALITY_MATRIX.md §3."
        )
    )
    parser.add_argument(
        "--text",
        type=str,
        default=None,
        help="Text to scan. Mutually exclusive with stdin pipe.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON to stdout (default: human-readable).",
    )
    parser.add_argument(
        "--strip-frontmatter",
        action="store_true",
        help=(
            "Blank YAML frontmatter before scanning (per D-IH-89-H "
            "operator-metadata exemption); set for markdown-shaped drafts."
        ),
    )
    args = parser.parse_args(argv)

    if not args.json:
        setup_logging(level=logging.INFO)

    text = _read_input(args.text)
    if not text.strip():
        if args.json:
            print(
                json.dumps(
                    {
                        "verdict": "EMPTY_INPUT",
                        "findings_count": 0,
                        "findings": [],
                        "hint": "Pass --text or pipe stdin.",
                    },
                    indent=2,
                )
            )
        else:
            LOG.error(
                "No input. Pass --text 'draft' or pipe a draft via stdin."
            )
        return 1

    hits = scan_text(text, strip_frontmatter=args.strip_frontmatter)

    if args.json:
        print(_format_hits_json(hits))
    else:
        print(_format_hits_human(hits))

    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
