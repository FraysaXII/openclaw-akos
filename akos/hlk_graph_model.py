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

GraphLabel = Literal[
    "Role", "Process", "Program", "Topic",
    # Initiative 32 P5/P6 (D-IH-32-M): 6 new node labels for the 6-axis
    # Holistik Ops graph projection. Each label mirrors one canonical CSV
    # in compliance/dimensions/. Same governance pattern as :Program /
    # :Topic — Neo4j is a rebuildable read index, not an authoring surface.
    "Persona", "Channel", "Sourcing",
    "Skill", "TouchpointKitCell", "Policy",
]
EdgeType = Literal[
    "REPORTS_TO",
    "PARENT_OF",
    "OWNED_BY",
    "CONSUMES",
    "PRODUCES_FOR",
    "PROGRAM_PARENT_OF",
    "PROGRAM_SUBSUMES",
    "UNDER_PROGRAM",
    # Initiative 25 P-graph (D-IH-25-B): Topic-side typed edges, naming
    # disambiguated from PROGRAM_PARENT_OF + PROGRAM_SUBSUMES.
    "DEPENDS_ON",
    "TOPIC_PARENT_OF",
    "RELATED_TO",
    "TOPIC_SUBSUMES",
    # Initiative 32 P5/P6 (D-IH-32-A + D-IH-32-M): axis-6 typed edges.
    # UNDER_TOPIC is the cross-axis edge from any dimension node to its
    # declared :Topic via the row's topic_ids / linked_topic_ids column.
    "UNDER_TOPIC",
]


PERSONA_REGISTRY_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PERSONA_REGISTRY.csv"
)
CHANNEL_TOUCHPOINT_REGISTRY_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "CHANNEL_TOUCHPOINT_REGISTRY.csv"
)
SOURCING_REGISTER_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SOURCING_REGISTER.csv"
)
SKILL_REGISTRY_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "SKILL_REGISTRY.csv"
)
TOUCHPOINT_KIT_CELL_REGISTRY_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOUCHPOINT_KIT_CELL_REGISTRY.csv"
)
POLICY_REGISTER_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "POLICY_REGISTER.csv"
)


PROGRAM_REGISTRY_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "PROGRAM_REGISTRY.csv"
)
TOPIC_REGISTRY_CSV = (
    REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "TOPIC_REGISTRY.csv"
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
    topic_nodes = sum(1 for n in nodes if n.label == "Topic")
    return {
        "registry_roles": len(registry._roles),  # noqa: SLF001
        "registry_processes": len(registry._processes),  # noqa: SLF001
        "graph_role_nodes": role_nodes,
        "graph_process_nodes": proc_nodes,
        "graph_program_nodes": prog_nodes,
        "graph_topic_nodes": topic_nodes,
        "graph_edges": len(edges),
        "edge_reports_to": sum(1 for e in edges if e.edge_type == "REPORTS_TO"),
        "edge_parent_of": sum(1 for e in edges if e.edge_type == "PARENT_OF"),
        "edge_owned_by": sum(1 for e in edges if e.edge_type == "OWNED_BY"),
        "edge_consumes": sum(1 for e in edges if e.edge_type == "CONSUMES"),
        "edge_produces_for": sum(1 for e in edges if e.edge_type == "PRODUCES_FOR"),
        "edge_program_parent_of": sum(1 for e in edges if e.edge_type == "PROGRAM_PARENT_OF"),
        "edge_program_subsumes": sum(1 for e in edges if e.edge_type == "PROGRAM_SUBSUMES"),
        "edge_under_program": sum(1 for e in edges if e.edge_type == "UNDER_PROGRAM"),
        "edge_depends_on": sum(1 for e in edges if e.edge_type == "DEPENDS_ON"),
        "edge_topic_parent_of": sum(1 for e in edges if e.edge_type == "TOPIC_PARENT_OF"),
        "edge_related_to": sum(1 for e in edges if e.edge_type == "RELATED_TO"),
        "edge_topic_subsumes": sum(1 for e in edges if e.edge_type == "TOPIC_SUBSUMES"),
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


TOPIC_REGISTRY_FIELDNAMES_MIN: tuple[str, ...] = (
    "topic_id",
    "title",
    "topic_class",
    "lifecycle_status",
    "primary_owner_role",
    "program_id",
    "plane",
    "parent_topic",
    "related_topics",
    "depends_on",
    "subsumes",
    "subsumed_by",
    "manifest_path",
    "notes",
)


def _read_topic_registry_rows(csv_path: Path = TOPIC_REGISTRY_CSV) -> list[dict[str, str]]:
    """Read TOPIC_REGISTRY.csv. Returns [] if absent or header-mismatched."""
    if not csv_path.is_file():
        return []
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if list(reader.fieldnames or []) != list(TOPIC_REGISTRY_FIELDNAMES_MIN):
            return []
        return [dict(r) for r in reader]


def _topic_props(row: dict[str, str]) -> dict[str, str | int]:
    return {
        "topic_id": row.get("topic_id", ""),
        "title": row.get("title", ""),
        "topic_class": row.get("topic_class", ""),
        "lifecycle_status": row.get("lifecycle_status", ""),
        "primary_owner_role": row.get("primary_owner_role", ""),
        "program_id": row.get("program_id", ""),
        "plane": row.get("plane", ""),
        "manifest_path": row.get("manifest_path", ""),
        "notes": (row.get("notes") or "")[:1024],
    }


def build_topic_graph(
    registry: HlkRegistry,
    csv_path: Path = TOPIC_REGISTRY_CSV,
    program_registry_path: Path = PROGRAM_REGISTRY_CSV,
) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Initiative 25 P-graph (D-IH-12 + D-IH-18 + D-IH-25-B). Project the TOPIC_REGISTRY
    into ``:Topic`` nodes and typed edges. CSV is SSOT; this projector is read-only.

    Edges emitted:

    - ``(:Topic)-[:DEPENDS_ON]->(:Topic)`` from ``depends_on`` (semicolon list).
    - ``(:Topic)-[:TOPIC_PARENT_OF]->(:Topic)`` from ``parent_topic`` (single).
    - ``(:Topic)-[:RELATED_TO]->(:Topic)`` from ``related_topics`` (semicolon list).
    - ``(:Topic)-[:TOPIC_SUBSUMES]->(:Topic)`` from ``subsumes`` (semicolon list).
    - ``(:Topic)-[:UNDER_PROGRAM]->(:Program)`` from ``program_id`` (when not 'shared').
    - ``(:Topic)-[:OWNED_BY]->(:Role)`` from ``primary_owner_role`` (when role is registered).

    Forward references that don't resolve are silently skipped (validator is
    the gate). Edge naming is disambiguated from ``:PROGRAM_PARENT_OF`` and
    process-tree ``:PARENT_OF``.
    """
    rows = _read_topic_registry_rows(csv_path)
    if not rows:
        return [], []

    topic_ids = {(r.get("topic_id") or "").strip() for r in rows}
    topic_ids.discard("")
    role_names = {r.role_name for r in registry._roles}  # noqa: SLF001

    program_ids: set[str] = set()
    if program_registry_path.is_file():
        with program_registry_path.open(encoding="utf-8", newline="") as fh:
            program_ids = {row["program_id"].strip() for row in csv.DictReader(fh) if row.get("program_id")}

    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []

    for row in rows:
        tid = (row.get("topic_id") or "").strip()
        if not tid:
            continue
        nodes.append(GraphNode(label="Topic", id=tid, properties=_topic_props(row)))

    for row in rows:
        tid = (row.get("topic_id") or "").strip()
        if not tid:
            continue
        # TOPIC_PARENT_OF (parent -> child)
        parent = (row.get("parent_topic") or "").strip()
        if parent and parent in topic_ids and parent != tid:
            edges.append(
                GraphEdge(
                    edge_type="TOPIC_PARENT_OF",
                    from_label="Topic",
                    from_id=parent,
                    to_label="Topic",
                    to_id=tid,
                )
            )
        # DEPENDS_ON (this -> upstream)
        for ref in _split_semicolon(row.get("depends_on", "")):
            if ref in topic_ids and ref != tid:
                edges.append(
                    GraphEdge(
                        edge_type="DEPENDS_ON",
                        from_label="Topic",
                        from_id=tid,
                        to_label="Topic",
                        to_id=ref,
                    )
                )
        # RELATED_TO (this -> related)
        for ref in _split_semicolon(row.get("related_topics", "")):
            if ref in topic_ids and ref != tid:
                edges.append(
                    GraphEdge(
                        edge_type="RELATED_TO",
                        from_label="Topic",
                        from_id=tid,
                        to_label="Topic",
                        to_id=ref,
                    )
                )
        # TOPIC_SUBSUMES (this -> subsumed)
        for ref in _split_semicolon(row.get("subsumes", "")):
            if ref in topic_ids and ref != tid:
                edges.append(
                    GraphEdge(
                        edge_type="TOPIC_SUBSUMES",
                        from_label="Topic",
                        from_id=tid,
                        to_label="Topic",
                        to_id=ref,
                    )
                )
        # UNDER_PROGRAM (this -> :Program)
        prog = (row.get("program_id") or "").strip()
        if prog and prog != "shared" and prog in program_ids:
            edges.append(
                GraphEdge(
                    edge_type="UNDER_PROGRAM",
                    from_label="Topic",
                    from_id=tid,
                    to_label="Program",
                    to_id=prog,
                )
            )
        # OWNED_BY (this -> :Role)
        owner = (row.get("primary_owner_role") or "").strip()
        if owner and owner in role_names:
            edges.append(
                GraphEdge(
                    edge_type="OWNED_BY",
                    from_label="Topic",
                    from_id=tid,
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


# =====================================================================
# Initiative 32 P5/P6 — 6-axis Holistik Ops graph projection extension
# =====================================================================

def _read_csv_rows(csv_path: Path, header_check: tuple[str, ...] | None = None) -> list[dict[str, str]]:
    """Read CSV rows; return [] when file absent. Header-check mismatches return [] (validator-side gate)."""
    if not csv_path.is_file():
        return []
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if header_check is not None and list(reader.fieldnames or []) != list(header_check):
            return []
        return [dict(r) for r in reader]


def _under_topic_edges(
    from_label: GraphLabel,
    from_id: str,
    topic_ids_field: str,
    topic_ids: set[str],
) -> list[GraphEdge]:
    """Emit (X)-[:UNDER_TOPIC]->(:Topic) edges for every topic in the row's topic_ids list."""
    edges: list[GraphEdge] = []
    for tid in _split_semicolon(topic_ids_field):
        if tid in topic_ids:
            edges.append(GraphEdge(
                edge_type="UNDER_TOPIC",
                from_label=from_label,
                from_id=from_id,
                to_label="Topic",
                to_id=tid,
            ))
    return edges


def _topic_ids_from_registry() -> set[str]:
    """Load topic_id set from TOPIC_REGISTRY.csv for cross-axis FK resolution."""
    return {
        (r.get("topic_id") or "").strip()
        for r in _read_csv_rows(TOPIC_REGISTRY_CSV)
        if (r.get("topic_id") or "").strip()
    }


def build_persona_graph(csv_path: Path = PERSONA_REGISTRY_CSV) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Project PERSONA_REGISTRY.csv as :Persona nodes + :UNDER_TOPIC edges (axis 6)."""
    rows = _read_csv_rows(csv_path)
    if not rows:
        return [], []
    topic_ids = _topic_ids_from_registry()
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    for r in rows:
        pid = (r.get("persona_id") or "").strip()
        if not pid:
            continue
        nodes.append(GraphNode(
            label="Persona", id=pid,
            properties={
                "persona_id": pid,
                "name": (r.get("name") or "")[:256],
                "direction": r.get("direction", ""),
                "value_band": r.get("value_band", ""),
                "typical_distance_band": r.get("typical_distance_band", ""),
                "handoff_role": r.get("handoff_role", ""),
            },
        ))
        edges.extend(_under_topic_edges("Persona", pid, r.get("linked_topic_ids", ""), topic_ids))
    return nodes, edges


def build_channel_graph(csv_path: Path = CHANNEL_TOUCHPOINT_REGISTRY_CSV) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Project CHANNEL_TOUCHPOINT_REGISTRY.csv as :Channel nodes + :UNDER_TOPIC edges."""
    rows = _read_csv_rows(csv_path)
    if not rows:
        return [], []
    topic_ids = _topic_ids_from_registry()
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    for r in rows:
        cid = (r.get("channel_id") or "").strip()
        if not cid:
            continue
        nodes.append(GraphNode(
            label="Channel", id=cid,
            properties={
                "channel_id": cid,
                "name": (r.get("name") or "")[:256],
                "direction": r.get("direction", ""),
                "supported_languages": r.get("supported_languages", ""),
                "typical_distance_band_inbound": r.get("typical_distance_band_inbound", ""),
                "response_owner_role": r.get("response_owner_role", ""),
            },
        ))
        edges.extend(_under_topic_edges("Channel", cid, r.get("linked_topic_ids", ""), topic_ids))
    return nodes, edges


def build_sourcing_graph(csv_path: Path = SOURCING_REGISTER_CSV) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Project SOURCING_REGISTER.csv as :Sourcing nodes + :UNDER_TOPIC edges."""
    rows = _read_csv_rows(csv_path)
    if not rows:
        return [], []
    topic_ids = _topic_ids_from_registry()
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    for r in rows:
        vid = (r.get("vendor_id") or "").strip()
        if not vid:
            continue
        nodes.append(GraphNode(
            label="Sourcing", id=vid,
            properties={
                "vendor_id": vid,
                "discipline": r.get("discipline", ""),
                "engagement_type": r.get("engagement_type", ""),
                "languages_supported": r.get("languages_supported", ""),
                "current_distance_band": r.get("current_distance_band", ""),
            },
        ))
        edges.extend(_under_topic_edges("Sourcing", vid, r.get("linked_topic_ids", ""), topic_ids))
    return nodes, edges


def build_skill_graph(csv_path: Path = SKILL_REGISTRY_CSV) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Project SKILL_REGISTRY.csv as :Skill nodes + :UNDER_TOPIC edges (Initiative 32 P2)."""
    rows = _read_csv_rows(csv_path)
    if not rows:
        return [], []
    topic_ids = _topic_ids_from_registry()
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    for r in rows:
        sid = (r.get("skill_id") or "").strip()
        if not sid:
            continue
        nodes.append(GraphNode(
            label="Skill", id=sid,
            properties={
                "skill_id": sid,
                "name": (r.get("name") or "")[:256],
                "agents_supported": r.get("agents_supported", ""),
                "axes_consumed": r.get("axes_consumed", ""),
                "version": r.get("version", ""),
                "owner_role": r.get("owner_role", ""),
                "tenant_scope": r.get("tenant_scope", ""),
                "lifecycle_status": r.get("lifecycle_status", ""),
            },
        ))
        edges.extend(_under_topic_edges("Skill", sid, r.get("topic_ids", ""), topic_ids))
    return nodes, edges


def build_touchpoint_kit_cell_graph(
    csv_path: Path = TOUCHPOINT_KIT_CELL_REGISTRY_CSV,
) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Project TOUCHPOINT_KIT_CELL_REGISTRY.csv as :TouchpointKitCell nodes + :UNDER_TOPIC edges."""
    rows = _read_csv_rows(csv_path)
    if not rows:
        return [], []
    topic_ids = _topic_ids_from_registry()
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    for r in rows:
        cid = (r.get("cell_id") or "").strip()
        if not cid:
            continue
        nodes.append(GraphNode(
            label="TouchpointKitCell", id=cid,
            properties={
                "cell_id": cid,
                "persona_id": r.get("persona_id", ""),
                "channel_id": r.get("channel_id", ""),
                "language": r.get("language", ""),
                "template_path": r.get("template_path", ""),
                "distance_variants_in_file": r.get("distance_variants_in_file", ""),
                "lifecycle_status": r.get("lifecycle_status", ""),
            },
        ))
        edges.extend(_under_topic_edges("TouchpointKitCell", cid, r.get("topic_ids", ""), topic_ids))
    return nodes, edges


def build_policy_graph(csv_path: Path = POLICY_REGISTER_CSV) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Project POLICY_REGISTER.csv as :Policy nodes + :UNDER_TOPIC edges (Initiative 32 P4)."""
    rows = _read_csv_rows(csv_path)
    if not rows:
        return [], []
    topic_ids = _topic_ids_from_registry()
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    for r in rows:
        pid = (r.get("policy_id") or "").strip()
        if not pid:
            continue
        nodes.append(GraphNode(
            label="Policy", id=pid,
            properties={
                "policy_id": pid,
                "policy_class": r.get("policy_class", ""),
                "applies_to_schema": r.get("applies_to_schema", ""),
                "applies_to_table": r.get("applies_to_table", ""),
                "cadence": r.get("cadence", ""),
                "owner_role": r.get("owner_role", ""),
                "last_review": r.get("last_review", ""),
                "next_review": r.get("next_review", ""),
            },
        ))
        edges.extend(_under_topic_edges("Policy", pid, r.get("topic_ids", ""), topic_ids))
    return nodes, edges


def build_holistik_ops_axis_graph() -> tuple[list[GraphNode], list[GraphEdge]]:
    """Initiative 32 P5/P6 convenience: build all 6 new node-label graphs in one call.

    Returns the union of (:Persona, :Channel, :Sourcing, :Skill, :TouchpointKitCell, :Policy)
    nodes and their :UNDER_TOPIC edges. The Topic nodes themselves are produced
    by ``build_topic_graph`` (existing); this function only adds the new dimension
    nodes and their cross-axis edges to topics.
    """
    all_nodes: list[GraphNode] = []
    all_edges: list[GraphEdge] = []
    for build_fn in (
        build_persona_graph,
        build_channel_graph,
        build_sourcing_graph,
        build_skill_graph,
        build_touchpoint_kit_cell_graph,
        build_policy_graph,
    ):
        nodes, edges = build_fn()
        all_nodes.extend(nodes)
        all_edges.extend(edges)
    return all_nodes, all_edges
