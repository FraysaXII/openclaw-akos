"""In-repo HLK graph projection model (CSV layer).

Builds a deterministic node/edge snapshot from ``HlkRegistry`` for Neo4j sync
and parity checks. No Neo4j driver dependency here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from akos.hlk import HlkRegistry
from akos.models import OrgRole, ProcessItem

GraphLabel = Literal["Role", "Process"]
EdgeType = Literal["REPORTS_TO", "PARENT_OF", "OWNED_BY"]


@dataclass(frozen=True)
class GraphNode:
    label: GraphLabel
    id: str
    properties: dict[str, str | int]


@dataclass(frozen=True)
class GraphEdge:
    edge_type: EdgeType
    from_label: GraphLabel
    from_id: str
    to_label: GraphLabel
    to_id: str


def _role_props(role: OrgRole) -> dict[str, str | int]:
    return {
        "role_name": role.role_name,
        "area": role.area,
        "entity": role.entity,
        "org_id": role.org_id,
        "access_level": int(role.access_level or 0),
        "reports_to": role.reports_to,
        "role_description": (role.role_description or "")[:512],
    }


def _process_props(p: ProcessItem) -> dict[str, str | int]:
    return {
        "item_id": p.item_id,
        "item_name": p.item_name,
        "item_granularity": p.item_granularity,
        "role_owner": p.role_owner,
        "area": p.area,
        "entity": p.entity,
        "item_parent_1": p.item_parent_1,
        "item_parent_1_id": p.item_parent_1_id,
        "item_parent_2": p.item_parent_2,
        "item_parent_2_id": p.item_parent_2_id,
        "description": (p.description or "")[:1024],
    }


def build_hlk_csv_graph(registry: HlkRegistry) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Return Role and Process nodes plus REPORTS_TO, PARENT_OF, OWNED_BY edges."""
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []

    roles = registry._roles  # noqa: SLF001 — intentional registry snapshot
    processes = registry._processes  # noqa: SLF001
    by_name: dict[str, ProcessItem] = {}
    for p in processes:
        name = (p.item_name or "").strip()
        if name and name not in by_name:
            by_name[name] = p

    role_names = {r.role_name for r in roles}

    for role in roles:
        nodes.append(GraphNode(label="Role", id=role.role_name, properties=_role_props(role)))

    for p in processes:
        iid = (p.item_id or "").strip()
        if not iid:
            continue
        nodes.append(GraphNode(label="Process", id=iid, properties=_process_props(p)))

    for role in roles:
        boss = (role.reports_to or "").strip()
        if not boss or boss == role.role_name:
            continue
        if boss in role_names:
            edges.append(
                GraphEdge(
                    edge_type="REPORTS_TO",
                    from_label="Role",
                    from_id=role.role_name,
                    to_label="Role",
                    to_id=boss,
                )
            )

    skip_owners = {"", "TBD", "Process Owner"}
    for p in processes:
        iid = (p.item_id or "").strip()
        if not iid:
            continue
        owner = (p.role_owner or "").strip()
        if owner and owner not in skip_owners and owner in role_names:
            edges.append(
                GraphEdge(
                    edge_type="OWNED_BY",
                    from_label="Process",
                    from_id=iid,
                    to_label="Role",
                    to_id=owner,
                )
            )

    for child in processes:
        cid = (child.item_id or "").strip()
        if not cid:
            continue
        gran = (child.item_granularity or "").strip().lower()
        if gran == "project":
            continue
        parent_id = (child.item_parent_1_id or "").strip()
        parent: ProcessItem | None = registry._processes_by_id.get(parent_id) if parent_id else None  # noqa: SLF001
        if parent is None:
            pname = (child.item_parent_1 or "").strip()
            parent = by_name.get(pname)
        if parent is None:
            continue
        pid = (parent.item_id or "").strip()
        if not pid:
            continue
        edges.append(
            GraphEdge(
                edge_type="PARENT_OF",
                from_label="Process",
                from_id=pid,
                to_label="Process",
                to_id=cid,
            )
        )

    return nodes, edges


def graph_parity_counts(registry: HlkRegistry, nodes: list[GraphNode], edges: list[GraphEdge]) -> dict[str, int]:
    """Return counts for parity logging (no Neo4j)."""
    role_nodes = sum(1 for n in nodes if n.label == "Role")
    proc_nodes = sum(1 for n in nodes if n.label == "Process")
    return {
        "registry_roles": len(registry._roles),  # noqa: SLF001
        "registry_processes": len(registry._processes),  # noqa: SLF001
        "graph_role_nodes": role_nodes,
        "graph_process_nodes": proc_nodes,
        "graph_edges": len(edges),
        "edge_reports_to": sum(1 for e in edges if e.edge_type == "REPORTS_TO"),
        "edge_parent_of": sum(1 for e in edges if e.edge_type == "PARENT_OF"),
        "edge_owned_by": sum(1 for e in edges if e.edge_type == "OWNED_BY"),
    }


def assert_graph_registry_parity(registry: HlkRegistry, nodes: list[GraphNode], edges: list[GraphEdge]) -> None:
    """Raise ValueError if node counts diverge from registry."""
    counts = graph_parity_counts(registry, nodes, edges)
    if counts["graph_role_nodes"] != counts["registry_roles"]:
        raise ValueError(
            f"role node count mismatch: graph={counts['graph_role_nodes']} registry={counts['registry_roles']}"
        )
    if counts["graph_process_nodes"] != counts["registry_processes"]:
        raise ValueError(
            "process node count mismatch: "
            f"graph={counts['graph_process_nodes']} registry={counts['registry_processes']}"
        )
