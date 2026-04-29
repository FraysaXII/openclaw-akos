"""In-repo HLK graph projection model (CSV layer).

Builds a deterministic node/edge snapshot from ``HlkRegistry`` for Neo4j sync
and parity checks. No Neo4j driver dependency here.

Initiative 23 P-graph (D-IH-18) extends the schema with a ``Program`` node label
and program-side edge types so the registry's ``compliance/dimensions/PROGRAM_REGISTRY.csv``
is projected into Neo4j alongside the existing Role / Process trees. CSVs remain
SSOT per ``PRECEDENCE.md`` §"Conflict Resolution"; Neo4j is rebuildable read index.

Edge naming is **disambiguated** so the program tree and the process tree can
coexist in the same graph without collision: ``PROGRAM_PARENT_OF`` /
``PROGRAM_SUBSUMES`` (programs) vs ``PARENT_OF`` (processes).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from akos.hlk import HlkRegistry
from akos.hlk_program_registry_csv import PROGRAM_REGISTRY_FIELDNAMES
from akos.io import REPO_ROOT
from akos.models import OrgRole, ProcessItem

GraphLabel = Literal["Role", "Process", "Program"]
EdgeType = Literal[
    "REPORTS_TO",
    "PARENT_OF",
    "OWNED_BY",
    "CONSUMES",
    "PRODUCES_FOR",
    "PROGRAM_PARENT_OF",
    "PROGRAM_SUBSUMES",
    "UNDER_PROGRAM",
]


PROGRAM_REGISTRY_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PROGRAM_REGISTRY.csv"
)


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
    prog_nodes = sum(1 for n in nodes if n.label == "Program")
    return {
        "registry_roles": len(registry._roles),  # noqa: SLF001
        "registry_processes": len(registry._processes),  # noqa: SLF001
        "graph_role_nodes": role_nodes,
        "graph_process_nodes": proc_nodes,
        "graph_program_nodes": prog_nodes,
        "graph_edges": len(edges),
        "edge_reports_to": sum(1 for e in edges if e.edge_type == "REPORTS_TO"),
        "edge_parent_of": sum(1 for e in edges if e.edge_type == "PARENT_OF"),
        "edge_owned_by": sum(1 for e in edges if e.edge_type == "OWNED_BY"),
        "edge_consumes": sum(1 for e in edges if e.edge_type == "CONSUMES"),
        "edge_produces_for": sum(1 for e in edges if e.edge_type == "PRODUCES_FOR"),
        "edge_program_parent_of": sum(1 for e in edges if e.edge_type == "PROGRAM_PARENT_OF"),
        "edge_program_subsumes": sum(1 for e in edges if e.edge_type == "PROGRAM_SUBSUMES"),
        "edge_under_program": sum(1 for e in edges if e.edge_type == "UNDER_PROGRAM"),
    }


def _read_program_registry_rows(csv_path: Path = PROGRAM_REGISTRY_CSV) -> list[dict[str, str]]:
    """Return the rows of `PROGRAM_REGISTRY.csv` (empty list when the file is absent).

    Initiative 23 P-graph: this is read-only; the CSV is canonical SSOT.
    """
    if not csv_path.is_file():
        return []
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if list(reader.fieldnames or []) != list(PROGRAM_REGISTRY_FIELDNAMES):
            # Header drift: refuse to project (validator catches this elsewhere).
            return []
        return [dict(r) for r in reader]


def _split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(";") if part.strip()]


def _program_props(row: dict[str, str]) -> dict[str, str | int]:
    return {
        "program_id": row.get("program_id", ""),
        "process_item_id": row.get("process_item_id", ""),
        "program_name": row.get("program_name", ""),
        "program_code": row.get("program_code", ""),
        "lifecycle_status": row.get("lifecycle_status", ""),
        "primary_owner_role": row.get("primary_owner_role", ""),
        "default_plane": row.get("default_plane", ""),
        "start_date": row.get("start_date", ""),
        "target_close_date": row.get("target_close_date", ""),
        "risk_class": row.get("risk_class", ""),
        "notes": (row.get("notes") or "")[:1024],
    }


def build_program_graph(
    registry: HlkRegistry, csv_path: Path = PROGRAM_REGISTRY_CSV
) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Return ``:Program`` nodes plus typed program-side edges.

    Reads ``PROGRAM_REGISTRY.csv`` directly (registry has no in-memory program
    list; the CSV is small enough — N ~= 12 — that re-reading is fine). Edges
    emitted (D-IH-9, D-IH-18):

    - ``(:Program)-[:CONSUMES]->(:Program)`` from ``consumes_program_ids``
    - ``(:Program)-[:PRODUCES_FOR]->(:Program)`` from ``produces_for_program_ids``
    - ``(:Program)-[:PROGRAM_PARENT_OF]->(:Program)`` from ``parent_program_id``
    - ``(:Program)-[:PROGRAM_SUBSUMES]->(:Program)`` from ``subsumes_program_ids``
    - ``(:Program)-[:OWNED_BY]->(:Role)`` when ``primary_owner_role`` resolves
      to a known role in the registry (generalizes the existing ``OWNED_BY``
      edge from ``Process``).

    Forward references that don't resolve (target row absent at projection
    time) are **silently skipped** — the validator (`scripts/validate_program_registry.py`)
    is the gate; the projector trusts the validated CSV. This matches the
    Process tree's silent skip on missing parents.
    """
    rows = _read_program_registry_rows(csv_path)
    if not rows:
        return [], []

    program_ids = {(r.get("program_id") or "").strip() for r in rows}
    program_ids.discard("")
    role_names = {r.role_name for r in registry._roles}  # noqa: SLF001

    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []

    for row in rows:
        pid = (row.get("program_id") or "").strip()
        if not pid:
            continue
        nodes.append(GraphNode(label="Program", id=pid, properties=_program_props(row)))

    for row in rows:
        pid = (row.get("program_id") or "").strip()
        if not pid:
            continue
        # PROGRAM_PARENT_OF (parent -> child): edge points from parent to this child.
        parent = (row.get("parent_program_id") or "").strip()
        if parent and parent in program_ids and parent != pid:
            edges.append(
                GraphEdge(
                    edge_type="PROGRAM_PARENT_OF",
                    from_label="Program",
                    from_id=parent,
                    to_label="Program",
                    to_id=pid,
                )
            )
        # CONSUMES (this -> upstream)
        for ref in _split_semicolon(row.get("consumes_program_ids", "")):
            if ref in program_ids and ref != pid:
                edges.append(
                    GraphEdge(
                        edge_type="CONSUMES",
                        from_label="Program",
                        from_id=pid,
                        to_label="Program",
                        to_id=ref,
                    )
                )
        # PRODUCES_FOR (this -> downstream)
        for ref in _split_semicolon(row.get("produces_for_program_ids", "")):
            if ref in program_ids and ref != pid:
                edges.append(
                    GraphEdge(
                        edge_type="PRODUCES_FOR",
                        from_label="Program",
                        from_id=pid,
                        to_label="Program",
                        to_id=ref,
                    )
                )
        # PROGRAM_SUBSUMES (this -> subsumed)
        for ref in _split_semicolon(row.get("subsumes_program_ids", "")):
            if ref in program_ids and ref != pid:
                edges.append(
                    GraphEdge(
                        edge_type="PROGRAM_SUBSUMES",
                        from_label="Program",
                        from_id=pid,
                        to_label="Program",
                        to_id=ref,
                    )
                )
        # OWNED_BY (program -> role)
        owner = (row.get("primary_owner_role") or "").strip()
        if owner and owner in role_names:
            edges.append(
                GraphEdge(
                    edge_type="OWNED_BY",
                    from_label="Program",
                    from_id=pid,
                    to_label="Role",
                    to_id=owner,
                )
            )

    return nodes, edges


def assert_graph_registry_parity(registry: HlkRegistry, nodes: list[GraphNode], edges: list[GraphEdge]) -> None:
    """Raise ValueError if node counts diverge from registry.

    Program-side parity is intentionally omitted here because the CSV row
    count is the source of truth (no in-memory `HlkRegistry._programs`). Use
    ``len(_read_program_registry_rows())`` directly for program parity probes.
    """
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
