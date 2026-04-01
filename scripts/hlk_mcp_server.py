#!/usr/bin/env python3
"""HLK organisation and process registry MCP server for AKOS agents.

Exposes read-only HLK vault lookup tools:
- hlk_role: look up a role and its full description
- hlk_role_chain: traverse reports_to chain to Admin
- hlk_area: list all roles in an area
- hlk_process: look up a process by ID
- hlk_process_tree: list children of a process item
- hlk_projects: list all projects with child counts
- hlk_gaps: report items with missing metadata or TBD owners
- hlk_search: fuzzy search across roles and processes

All responses use the HlkResponse envelope from akos.models.

Requires: pip install mcp
Usage: python scripts/hlk_mcp_server.py
       or: uv run --with mcp scripts/hlk_mcp_server.py (stdio)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Install mcp: pip install mcp", file=sys.stderr)
    sys.exit(1)

from akos.hlk import get_hlk_registry

mcp = FastMCP("AKOS HLK Registry", host="127.0.0.1", port=8423)


@mcp.tool()
def hlk_role(role_name: str) -> str:
    """Look up an HLK organisation role by name.

    Returns the role's full description, access level, area, entity,
    reports_to chain position, and SOP URL if available.

    Use this when you need to understand what a role does or who it
    reports to. Role names are case-sensitive and match the canonical
    baseline_organisation.csv.
    """
    return get_hlk_registry().get_role(role_name).model_dump_json(indent=2, exclude_none=True)


@mcp.tool()
def hlk_role_chain(role_name: str) -> str:
    """Traverse the reporting chain from a role up to Admin.

    Returns an ordered list of roles from the given role to the top
    of the hierarchy. Useful for understanding governance authority
    and escalation paths.
    """
    return get_hlk_registry().get_role_chain(role_name).model_dump_json(indent=2, exclude_none=True)


@mcp.tool()
def hlk_area(area: str) -> str:
    """List all roles in a given organisational area.

    Areas include: Admin, AI, People, Operations, Finance, Marketing,
    Data, Tech, Legal, Research. Returns all roles with their access
    levels and reporting relationships.
    """
    return get_hlk_registry().get_area_roles(area).model_dump_json(indent=2, exclude_none=True)


@mcp.tool()
def hlk_process(item_id: str) -> str:
    """Look up a single process item by its ID.

    Process IDs follow patterns like hol_resea_dtp_99, env_tech_dtp_240,
    thi_opera_dtp_200. Returns the full process metadata including
    granularity, parent chain, role owner, and description.
    """
    return get_hlk_registry().get_process(item_id).model_dump_json(indent=2, exclude_none=True)


@mcp.tool()
def hlk_process_tree(item_name: str) -> str:
    """List all direct children of a process item by parent name.

    Use this to explore the process hierarchy. Pass a project name
    to see its workstreams, a workstream name to see its processes,
    or a process name to see its tasks.
    """
    return get_hlk_registry().get_process_tree(item_name).model_dump_json(indent=2, exclude_none=True)


@mcp.tool()
def hlk_projects() -> str:
    """List all HLK projects with their direct child counts.

    Returns the 11 top-level projects that organize all workstreams,
    processes, and tasks in the HLK vault. Each project includes
    its child count for navigation context.
    """
    return get_hlk_registry().get_project_summary().model_dump_json(indent=2, exclude_none=True)


@mcp.tool()
def hlk_gaps() -> str:
    """Report items with missing metadata, TBD owners, or empty descriptions.

    Use this to identify baseline remediation opportunities. Returns
    process items that need attention: unassigned owners, missing
    descriptions, or orphaned items without parent references.
    """
    return get_hlk_registry().get_gaps().model_dump_json(indent=2, exclude_none=True)


@mcp.tool()
def hlk_search(query: str) -> str:
    """Fuzzy search across HLK roles and processes.

    Searches role names, descriptions, process names, IDs, and
    descriptions. Use this when you need to find something but
    don't know the exact name or ID.
    """
    return get_hlk_registry().search(query).model_dump_json(indent=2, exclude_none=True)


if __name__ == "__main__":
    mcp.run(transport="stdio")
