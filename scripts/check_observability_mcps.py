#!/usr/bin/env python3
"""Verify observability MCP reachability (I71 P5 Strand B hardening; advisory).

Lightweight offline-friendly smoke check (Option C from the I71 P5 kickoff):
inspects the operator-side Cursor MCP project cache at
``~/.cursor/projects/<workspace>/mcps/`` for the expected ``user-sentry`` and
``user-langfuse`` MCP server folders + tool descriptor directories. Returns:

    0 -- both MCPs reachable on this host (folders + tools/ subdirs present).
    1 -- at least one MCP unreachable (folder missing or empty).

This is **advisory only** -- the release-gate consumes the result as an INFO
row (never blocks). Per WORKSPACE_BLUEPRINT_HOLISTIKA.md §18 every CI gate
gets its own routing row (C-71-5 every-gate-its-own-row verdict ratified at
P5 inline-ratify via D-IH-71-T default); this script populates the Strand B
observability rows with deterministic reachability data.

SOC posture per ``.cursor/rules/akos-holistika-operations.mdc``: the script
does NOT log MCP secret values, environment values, dashboard URLs, or any
sensitive credentials. It only logs the MCP slug + tool-count + folder path
relative to ``~/.cursor/projects/``. Dashboard URLs surface in WORKSPACE §18
behind role-based access pointers, not in CI output.

Why filesystem-check instead of live MCP probe? Cursor MCP servers register
in the operator's Cursor session at runtime; the project cache directory is
the durable on-disk artifact that proves the MCP has been configured at
least once on this host. A live ping would require running inside a Cursor
session with MCP routing; CI runs outside that surface. The filesystem
check is the deterministic, host-portable signal that the MCP is
provisioned.

Cross-references::

    WORKSPACE_BLUEPRINT_HOLISTIKA.md §18 (observability routing matrix; Pack
        A4 + Strand B rows; per-CI-gate cardinality per C-71-5).
    .cursor/rules/akos-holistika-operations.mdc (SOC posture; URL surfacing).
    D-IH-71-B (AIOps tool selection: Sentry + Langfuse via operator MCPs).
    D-IH-71-T (Strand B observability cardinality ratification + C-71-5
        every-gate-its-own-row default applied).
    I71 P5 master-roadmap + initiative-scoped plan §P5 Strand B.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.log import setup_logging

logger = logging.getLogger("akos.observability_mcps")

EXPECTED_MCPS: tuple[str, ...] = ("user-sentry", "user-langfuse")


# -----------------------------------------------------------------------------
# Result type
# -----------------------------------------------------------------------------


@dataclass
class MCPStatus:
    slug: str
    reachable: bool
    tool_count: int
    relative_path: str
    note: str


# -----------------------------------------------------------------------------
# MCP project-cache discovery
# -----------------------------------------------------------------------------


def _candidate_cursor_projects_roots() -> list[Path]:
    """Enumerate plausible Cursor projects roots on this host.

    Cursor stores the per-workspace MCP project cache at
    ``~/.cursor/projects/<workspace_id>/mcps/`` (the workspace_id is a
    deterministic encoding of the workspace path). The script does not need
    to identify which workspace_id corresponds to the current workspace --
    any workspace on the host that has the expected MCPs proves the MCPs
    are provisioned for the operator.
    """
    candidates: list[Path] = []
    home = Path(os.path.expanduser("~"))
    projects_root = home / ".cursor" / "projects"
    if projects_root.exists():
        candidates.append(projects_root)
    return candidates


def _scan_mcps(projects_roots: Iterable[Path]) -> dict[str, MCPStatus]:
    """Walk all Cursor project caches; build a {slug -> latest-status} map.

    The latest status wins if multiple workspace_ids carry the same MCP
    (operators with multiple Cursor projects on a host can configure the
    same MCP per-project; we accept the first reachable encounter).
    """
    results: dict[str, MCPStatus] = {}
    for slug in EXPECTED_MCPS:
        results[slug] = MCPStatus(
            slug=slug,
            reachable=False,
            tool_count=0,
            relative_path="",
            note="not found in any Cursor project cache",
        )

    for root in projects_roots:
        if not root.exists():
            continue
        for project_dir in sorted(root.iterdir()):
            if not project_dir.is_dir():
                continue
            mcps_dir = project_dir / "mcps"
            if not mcps_dir.exists():
                continue
            for slug in EXPECTED_MCPS:
                if results[slug].reachable:
                    continue
                candidate = mcps_dir / slug
                if not candidate.exists() or not candidate.is_dir():
                    continue
                tools_dir = candidate / "tools"
                tool_count = 0
                if tools_dir.exists() and tools_dir.is_dir():
                    tool_count = sum(
                        1
                        for child in tools_dir.iterdir()
                        if child.is_file() and child.suffix == ".json"
                    )
                # Surface only relative path (anchored at ~/.cursor/projects/)
                # per the SOC posture (no full absolute path; no env values).
                try:
                    rel = candidate.relative_to(root)
                except ValueError:
                    rel = candidate
                reachable = tool_count > 0 or (tools_dir.exists() and tools_dir.is_dir())
                results[slug] = MCPStatus(
                    slug=slug,
                    reachable=reachable,
                    tool_count=tool_count,
                    relative_path=str(rel).replace("\\", "/"),
                    note=(
                        f"folder present with {tool_count} tool descriptor(s)"
                        if reachable
                        else "folder present but tools/ subdir empty or missing"
                    ),
                )
    return results


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify user-sentry + user-langfuse MCP reachability via Cursor "
            "project cache (I71 P5 Strand B; D-IH-71-T; advisory INFO row in "
            "release-gate; never blocks)."
        )
    )
    parser.add_argument("--json-log", action="store_true")
    parser.add_argument(
        "--projects-root",
        action="append",
        default=[],
        help=(
            "Override the Cursor projects root path (repeatable). Defaults to "
            "~/.cursor/projects/ (host-discovered)."
        ),
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    setup_logging(json_output=args.json_log)

    if args.projects_root:
        roots = [Path(os.path.expanduser(p)) for p in args.projects_root]
    else:
        roots = _candidate_cursor_projects_roots()

    if not roots:
        logger.warning(
            "OBSERVABILITY MCP SMOKE: no Cursor projects root found at "
            "~/.cursor/projects/. Both expected MCPs (user-sentry + "
            "user-langfuse) treated as unreachable. Advisory only (release-"
            "gate INFO row; never blocks)."
        )
        if args.json_log:
            print(
                json.dumps(
                    {
                        "reachable_count": 0,
                        "total": len(EXPECTED_MCPS),
                        "mcps": [
                            {
                                "slug": slug,
                                "reachable": False,
                                "tool_count": 0,
                                "relative_path": "",
                                "note": "no Cursor projects root found",
                            }
                            for slug in EXPECTED_MCPS
                        ],
                    },
                    indent=2,
                )
            )
        return 1

    statuses = _scan_mcps(roots)
    reachable_count = sum(1 for s in statuses.values() if s.reachable)
    total = len(EXPECTED_MCPS)

    if args.json_log:
        payload = {
            "reachable_count": reachable_count,
            "total": total,
            "mcps": [asdict(statuses[slug]) for slug in EXPECTED_MCPS],
        }
        print(json.dumps(payload, indent=2))
    else:
        for slug in EXPECTED_MCPS:
            status = statuses[slug]
            log_fn = logger.info if status.reachable else logger.warning
            log_fn(
                "OBSERVABILITY MCP SMOKE: %s -> reachable=%s tool_count=%d (%s)",
                status.slug,
                status.reachable,
                status.tool_count,
                status.note,
            )

    logger.info(
        "OBSERVABILITY MCP SMOKE summary: %d/%d MCPs reachable on this host "
        "(advisory; release-gate consumes as INFO row; never blocks)",
        reachable_count,
        total,
    )
    return 0 if reachable_count == total else 1


if __name__ == "__main__":
    sys.exit(main())
