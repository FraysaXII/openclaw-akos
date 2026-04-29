"""Neo4j driver helpers and allowlisted read queries for the HLK CSV projection.

Secrets: read ``NEO4J_URI``, ``NEO4J_USERNAME``, ``NEO4J_PASSWORD`` from the
process environment (bootstrap via ``bootstrap_openclaw_process_env`` first).
Optional TLS: ``NEO4J_TRUST`` (``system`` default, ``all`` for relaxed verify —
see docs). Optional ``NEO4J_CA_BUNDLE`` with ``NEO4J_TRUST=custom`` for extra CA
paths. Never log passwords or full URIs with credentials.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

from akos.hlk import HlkRegistry
from akos.hlk_graph_model import GraphEdge, GraphNode, assert_graph_registry_parity, build_hlk_csv_graph

if TYPE_CHECKING:
    from neo4j import Driver, Session

logger = logging.getLogger("akos.hlk_neo4j")


def neo4j_configured() -> bool:
    return bool(os.environ.get("NEO4J_URI", "").strip() and os.environ.get("NEO4J_PASSWORD", "").strip())


def neo4j_env_non_placeholder() -> bool:
    """True when Bolt env vars look like real operator configuration (not template text)."""
    if not neo4j_configured():
        return False
    uri = os.environ.get("NEO4J_URI", "").strip()
    pwd = os.environ.get("NEO4J_PASSWORD", "").strip()
    blob = f"{uri}\n{pwd}".upper()
    for token in ("YOUR_", "CHANGE_ME", "REPLACE-", "CHANGEME", "<PASSWORD>", "TODO_"):
        if token in blob:
            return False
    return True


def get_neo4j_driver() -> Driver | None:
    """Return a Neo4j driver or ``None`` when not configured."""
    if not neo4j_configured():
        return None
    try:
        from neo4j import GraphDatabase
    except ImportError:
        logger.warning("neo4j package not installed; graph features disabled")
        return None

    uri = os.environ["NEO4J_URI"].strip()
    user = (os.environ.get("NEO4J_USERNAME") or "neo4j").strip()
    pwd = os.environ["NEO4J_PASSWORD"].strip()

    driver_kwargs: dict[str, Any] = {}
    trust_raw = (os.environ.get("NEO4J_TRUST") or "system").strip().lower()
    # ``neo4j+s`` / ``bolt+s`` URIs bundle encryption + system CA verify; they cannot be combined
    # with ``trusted_certificates=`` in the Python driver. For broken chains (corporate TLS
    # inspection, mis-scoped Aura copy), use ``neo4j+ssc`` / ``bolt+ssc`` in the URI **or** set
    # ``NEO4J_TRUST=all`` to auto-rewrite ``+s`` → ``+ssc`` (encryption without CA pin).
    if trust_raw in ("all", "insecure", "unsafe"):
        if uri.startswith("neo4j+s://"):
            uri = uri.replace("neo4j+s://", "neo4j+ssc://", 1)
            logger.warning(
                "Neo4j TLS: NEO4J_TRUST=%s - rewrote neo4j+s to neo4j+ssc (relaxed verify). "
                "Prefer the neo4j+ssc:// URI from Neo4j Aura or fix corporate CA trust.",
                trust_raw,
            )
        elif uri.startswith("bolt+s://"):
            uri = uri.replace("bolt+s://", "bolt+ssc://", 1)
            logger.warning(
                "Neo4j TLS: NEO4J_TRUST=%s - rewrote bolt+s to bolt+ssc (relaxed verify).",
                trust_raw,
            )
        elif uri.startswith(("neo4j+ssc://", "bolt+ssc://")):
            # URI already encodes relaxed verify; NEO4J_TRUST=all is redundant (common after Aura console copy).
            pass
        else:
            logger.warning(
                "Neo4j TLS: NEO4J_TRUST=%s but URI is not neo4j+s/bolt+s; no rewrite applied. "
                "Prefer neo4j+ssc:// in NEO4J_URI when Aura or your network requires it.",
                trust_raw,
            )
    elif trust_raw == "custom":
        import neo4j

        bundle = (os.environ.get("NEO4J_CA_BUNDLE") or "").strip()
        if not bundle:
            logger.error("NEO4J_TRUST=custom requires NEO4J_CA_BUNDLE (path to PEM CA file)")
            return None
        p = Path(bundle)
        if not p.is_file():
            logger.error("NEO4J_CA_BUNDLE is not a file: %s", bundle)
            return None
        if uri.startswith(("neo4j+s://", "bolt+s://", "neo4j+ssc://", "bolt+ssc://")):
            logger.error(
                "NEO4J_TRUST=custom is only supported with bolt:// or neo4j:// URIs in this driver; "
                "use neo4j+ssc:// without custom bundle, or ask Aura for full-chain URI"
            )
            return None
        driver_kwargs["trusted_certificates"] = neo4j.TrustCustomCAs(str(p.resolve()))
    elif trust_raw not in ("system", "default", ""):
        logger.warning("Unknown NEO4J_TRUST=%r; using URI defaults", trust_raw)

    return GraphDatabase.driver(uri, auth=(user, pwd), **driver_kwargs)


def _node_to_dict(node: Any) -> dict[str, Any]:
    """Map Neo4j Node to JSON-serializable dict (element_id + labels + props)."""
    return {
        "element_id": node.element_id,
        "labels": list(node.labels),
        "properties": dict(node),
    }


def _ensure_constraints(session: Session) -> None:
    session.run(
        "CREATE CONSTRAINT hlk_role_name IF NOT EXISTS FOR (r:Role) REQUIRE r.role_name IS UNIQUE"
    )
    session.run(
        "CREATE CONSTRAINT hlk_process_id IF NOT EXISTS FOR (p:Process) REQUIRE p.item_id IS UNIQUE"
    )
    # Initiative 23 P-graph (D-IH-18): :Program node identity + range indexes
    # for the projected wave-2 dimension.
    session.run(
        "CREATE CONSTRAINT hlk_program_id IF NOT EXISTS FOR (n:Program) REQUIRE n.program_id IS UNIQUE"
    )
    session.run(
        "CREATE INDEX hlk_program_lifecycle IF NOT EXISTS FOR (n:Program) ON (n.lifecycle_status)"
    )
    session.run(
        "CREATE INDEX hlk_program_code IF NOT EXISTS FOR (n:Program) ON (n.program_code)"
    )
    session.run(
        "CREATE INDEX hlk_program_plane IF NOT EXISTS FOR (n:Program) ON (n.default_plane)"
    )
    # Initiative 25 P-graph (D-IH-12 + D-IH-18): :Topic node identity + indexes.
    session.run(
        "CREATE CONSTRAINT hlk_topic_id IF NOT EXISTS FOR (n:Topic) REQUIRE n.topic_id IS UNIQUE"
    )
    session.run(
        "CREATE INDEX hlk_topic_lifecycle IF NOT EXISTS FOR (n:Topic) ON (n.lifecycle_status)"
    )
    session.run(
        "CREATE INDEX hlk_topic_class IF NOT EXISTS FOR (n:Topic) ON (n.topic_class)"
    )
    session.run(
        "CREATE INDEX hlk_topic_plane IF NOT EXISTS FOR (n:Topic) ON (n.plane)"
    )


def sync_csv_graph(driver: Driver, registry: HlkRegistry, *, wipe: bool = True) -> dict[str, int]:
    """Full rebuild of Role/Process/Program nodes and edges from *registry* + CSVs.

    Initiative 23 P-graph (D-IH-18): the rebuild now also projects the
    Program registry from `compliance/dimensions/PROGRAM_REGISTRY.csv` when the
    file exists. The CSV is the SSOT; this graph layer is rebuildable read
    index. Programs join Roles via `:OWNED_BY` and other Programs via the
    typed edges defined in `akos.hlk_graph_model`.
    """
    nodes, edges = build_hlk_csv_graph(registry)
    assert_graph_registry_parity(registry, nodes, edges)

    # Initiative 23 P-graph: program-side projection (CSV-driven; no in-memory
    # registry mirror). Append nodes/edges to the same lists so the wipe-then-
    # rebuild transaction below sees them all.
    from akos.hlk_graph_model import build_program_graph, build_topic_graph

    prog_nodes, prog_edges = build_program_graph(registry)
    # Initiative 25 P-graph: topic projection (CSV-driven). Topics depend on
    # Program nodes for UNDER_PROGRAM edges, so we project after Programs.
    topic_nodes, topic_edges = build_topic_graph(registry)
    nodes = nodes + prog_nodes + topic_nodes
    edges = edges + prog_edges + topic_edges

    role_rows = [n.properties for n in nodes if n.label == "Role"]
    proc_rows = [n.properties for n in nodes if n.label == "Process"]
    prog_rows = [n.properties for n in nodes if n.label == "Program"]
    topic_rows = [n.properties for n in nodes if n.label == "Topic"]
    edge_rows = [
        {
            "etype": e.edge_type,
            "fa": e.from_label,
            "fid": e.from_id,
            "ta": e.to_label,
            "tid": e.to_id,
        }
        for e in edges
    ]

    with driver.session() as session:
        if wipe:
            session.run("MATCH (n) DETACH DELETE n")
        _ensure_constraints(session)

        batch = 400
        for i in range(0, len(role_rows), batch):
            chunk = role_rows[i : i + batch]
            session.run(
                """
                UNWIND $rows AS row
                MERGE (r:Role {role_name: row.role_name})
                SET r.area = row.area,
                    r.entity = row.entity,
                    r.org_id = row.org_id,
                    r.access_level = row.access_level,
                    r.reports_to = row.reports_to,
                    r.role_description = row.role_description
                """,
                rows=chunk,
            )
        for i in range(0, len(proc_rows), batch):
            chunk = proc_rows[i : i + batch]
            session.run(
                """
                UNWIND $rows AS row
                MERGE (p:Process {item_id: row.item_id})
                SET p.item_name = row.item_name,
                    p.item_granularity = row.item_granularity,
                    p.role_owner = row.role_owner,
                    p.area = row.area,
                    p.entity = row.entity,
                    p.item_parent_1 = row.item_parent_1,
                    p.item_parent_1_id = row.item_parent_1_id,
                    p.item_parent_2 = row.item_parent_2,
                    p.item_parent_2_id = row.item_parent_2_id,
                    p.description = row.description
                """,
                rows=chunk,
            )
        # Initiative 23 P-graph: project :Program nodes after Role/Process
        # so OWNED_BY edges can match the existing :Role nodes.
        for i in range(0, len(prog_rows), batch):
            chunk = prog_rows[i : i + batch]
            session.run(
                """
                UNWIND $rows AS row
                MERGE (n:Program {program_id: row.program_id})
                SET n.process_item_id = row.process_item_id,
                    n.program_name = row.program_name,
                    n.program_code = row.program_code,
                    n.lifecycle_status = row.lifecycle_status,
                    n.primary_owner_role = row.primary_owner_role,
                    n.default_plane = row.default_plane,
                    n.start_date = row.start_date,
                    n.target_close_date = row.target_close_date,
                    n.risk_class = row.risk_class,
                    n.notes = row.notes
                """,
                rows=chunk,
            )
        # Initiative 25 P-graph: project :Topic nodes after :Program so
        # UNDER_PROGRAM edges can match.
        for i in range(0, len(topic_rows), batch):
            chunk = topic_rows[i : i + batch]
            session.run(
                """
                UNWIND $rows AS row
                MERGE (n:Topic {topic_id: row.topic_id})
                SET n.title = row.title,
                    n.topic_class = row.topic_class,
                    n.lifecycle_status = row.lifecycle_status,
                    n.primary_owner_role = row.primary_owner_role,
                    n.program_id = row.program_id,
                    n.plane = row.plane,
                    n.manifest_path = row.manifest_path,
                    n.notes = row.notes
                """,
                rows=chunk,
            )

        rt = [r for r in edge_rows if r["etype"] == "REPORTS_TO"]
        ob_proc = [r for r in edge_rows if r["etype"] == "OWNED_BY" and r["fa"] == "Process"]
        ob_prog = [r for r in edge_rows if r["etype"] == "OWNED_BY" and r["fa"] == "Program"]
        ob_topic = [r for r in edge_rows if r["etype"] == "OWNED_BY" and r["fa"] == "Topic"]
        po = [r for r in edge_rows if r["etype"] == "PARENT_OF"]
        prog_consumes = [r for r in edge_rows if r["etype"] == "CONSUMES"]
        prog_produces = [r for r in edge_rows if r["etype"] == "PRODUCES_FOR"]
        prog_parent = [r for r in edge_rows if r["etype"] == "PROGRAM_PARENT_OF"]
        prog_subsumes = [r for r in edge_rows if r["etype"] == "PROGRAM_SUBSUMES"]
        # Initiative 25 P-graph: topic-side edges
        topic_depends = [r for r in edge_rows if r["etype"] == "DEPENDS_ON"]
        topic_parent = [r for r in edge_rows if r["etype"] == "TOPIC_PARENT_OF"]
        topic_related = [r for r in edge_rows if r["etype"] == "RELATED_TO"]
        topic_subsumes = [r for r in edge_rows if r["etype"] == "TOPIC_SUBSUMES"]
        topic_under_program = [r for r in edge_rows if r["etype"] == "UNDER_PROGRAM"]
        for chunk in (rt[i : i + batch] for i in range(0, len(rt), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (a:Role {role_name: row.fid})
                MATCH (b:Role {role_name: row.tid})
                MERGE (a)-[:REPORTS_TO]->(b)
                """,
                rows=chunk,
            )
        for chunk in (ob_proc[i : i + batch] for i in range(0, len(ob_proc), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (p:Process {item_id: row.fid})
                MATCH (r:Role {role_name: row.tid})
                MERGE (p)-[:OWNED_BY]->(r)
                """,
                rows=chunk,
            )
        for chunk in (po[i : i + batch] for i in range(0, len(po), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (parent:Process {item_id: row.fid})
                MATCH (child:Process {item_id: row.tid})
                MERGE (parent)-[:PARENT_OF]->(child)
                """,
                rows=chunk,
            )
        # Initiative 23 P-graph: program-side edges
        for chunk in (ob_prog[i : i + batch] for i in range(0, len(ob_prog), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (n:Program {program_id: row.fid})
                MATCH (r:Role {role_name: row.tid})
                MERGE (n)-[:OWNED_BY]->(r)
                """,
                rows=chunk,
            )
        for chunk in (prog_consumes[i : i + batch] for i in range(0, len(prog_consumes), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (a:Program {program_id: row.fid})
                MATCH (b:Program {program_id: row.tid})
                MERGE (a)-[:CONSUMES]->(b)
                """,
                rows=chunk,
            )
        for chunk in (prog_produces[i : i + batch] for i in range(0, len(prog_produces), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (a:Program {program_id: row.fid})
                MATCH (b:Program {program_id: row.tid})
                MERGE (a)-[:PRODUCES_FOR]->(b)
                """,
                rows=chunk,
            )
        for chunk in (prog_parent[i : i + batch] for i in range(0, len(prog_parent), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (a:Program {program_id: row.fid})
                MATCH (b:Program {program_id: row.tid})
                MERGE (a)-[:PROGRAM_PARENT_OF]->(b)
                """,
                rows=chunk,
            )
        for chunk in (prog_subsumes[i : i + batch] for i in range(0, len(prog_subsumes), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (a:Program {program_id: row.fid})
                MATCH (b:Program {program_id: row.tid})
                MERGE (a)-[:PROGRAM_SUBSUMES]->(b)
                """,
                rows=chunk,
            )

        # Initiative 25 P-graph: project topic-side edges last so all node
        # types they target (Program, Role, Topic) already exist.
        for chunk in (ob_topic[i : i + batch] for i in range(0, len(ob_topic), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (n:Topic {topic_id: row.fid})
                MATCH (r:Role {role_name: row.tid})
                MERGE (n)-[:OWNED_BY]->(r)
                """,
                rows=chunk,
            )
        for chunk in (topic_depends[i : i + batch] for i in range(0, len(topic_depends), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (a:Topic {topic_id: row.fid})
                MATCH (b:Topic {topic_id: row.tid})
                MERGE (a)-[:DEPENDS_ON]->(b)
                """,
                rows=chunk,
            )
        for chunk in (topic_parent[i : i + batch] for i in range(0, len(topic_parent), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (a:Topic {topic_id: row.fid})
                MATCH (b:Topic {topic_id: row.tid})
                MERGE (a)-[:TOPIC_PARENT_OF]->(b)
                """,
                rows=chunk,
            )
        for chunk in (topic_related[i : i + batch] for i in range(0, len(topic_related), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (a:Topic {topic_id: row.fid})
                MATCH (b:Topic {topic_id: row.tid})
                MERGE (a)-[:RELATED_TO]->(b)
                """,
                rows=chunk,
            )
        for chunk in (topic_subsumes[i : i + batch] for i in range(0, len(topic_subsumes), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (a:Topic {topic_id: row.fid})
                MATCH (b:Topic {topic_id: row.tid})
                MERGE (a)-[:TOPIC_SUBSUMES]->(b)
                """,
                rows=chunk,
            )
        for chunk in (topic_under_program[i : i + batch] for i in range(0, len(topic_under_program), batch)):
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (t:Topic {topic_id: row.fid})
                MATCH (p:Program {program_id: row.tid})
                MERGE (t)-[:UNDER_PROGRAM]->(p)
                """,
                rows=chunk,
            )

    return {
        "roles_written": len(role_rows),
        "processes_written": len(proc_rows),
        "programs_written": len(prog_rows),
        "topics_written": len(topic_rows),
        "edges_written": len(edge_rows),
    }


def graph_summary(session: Session) -> dict[str, Any]:
    """Allowlisted aggregation for health/summary endpoints."""
    rows = session.run(
        """
        MATCH (n)
        RETURN labels(n)[0] AS label, count(*) AS c
        """
    ).data()
    by_label = {r["label"]: int(r["c"]) for r in rows if r.get("label")}
    rels = session.run(
        """
        MATCH ()-[r]->()
        RETURN type(r) AS t, count(*) AS c
        """
    ).data()
    by_rel = {r["t"]: int(r["c"]) for r in rels}
    return {"labels": by_label, "relationships": by_rel}


def process_neighbourhood(
    session: Session,
    item_id: str,
    *,
    depth: int,
    limit: int,
) -> dict[str, Any]:
    """Return root Process, direct Role, parent/child processes up to *depth* hops."""
    depth = max(1, min(int(depth), 5))
    limit = max(1, min(int(limit), 200))

    root_m = session.run(
        "MATCH (p:Process {item_id: $id}) RETURN p AS root LIMIT 1",
        id=item_id,
    ).single()
    if not root_m:
        return {"status": "not_found", "item_id": item_id, "nodes": [], "edges": []}

    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    def add_node(n: Any) -> str:
        d = _node_to_dict(n)
        nodes[d["element_id"]] = d
        return d["element_id"]

    root = root_m["root"]
    root_eid = add_node(root)
    root_props = dict(root)
    root_pid = root_props.get("item_id", item_id)

    row = session.run(
        """
        MATCH (root:Process {item_id: $id})
        OPTIONAL MATCH (root)-[:OWNED_BY]->(role:Role)
        OPTIONAL MATCH (parent:Process)-[:PARENT_OF]->(root)
        OPTIONAL MATCH (root)-[:PARENT_OF]->(child:Process)
        RETURN collect(DISTINCT role)[0..$lim] AS roles,
               collect(DISTINCT parent)[0..$lim] AS parents,
               collect(DISTINCT child)[0..$lim] AS children
        """,
        id=item_id,
        lim=limit,
    ).single()
    assert row is not None
    for role in row["roles"]:
        if role is None:
            continue
        reid = add_node(role)
        edges.append({"type": "OWNED_BY", "from": root_eid, "to": reid, "process_item_id": root_pid})
    for parent in row["parents"]:
        if parent is None:
            continue
        peid = add_node(parent)
        edges.append(
            {
                "type": "PARENT_OF",
                "from": peid,
                "to": root_eid,
                "parent_item_id": dict(parent).get("item_id"),
                "child_item_id": root_pid,
            }
        )
    for child in row["children"]:
        if child is None:
            continue
        ceid = add_node(child)
        edges.append(
            {
                "type": "PARENT_OF",
                "from": root_eid,
                "to": ceid,
                "parent_item_id": root_pid,
                "child_item_id": dict(child).get("item_id"),
            }
        )

    def eid_for_item_id(iid: str) -> str | None:
        for eid, nd in nodes.items():
            if nd["properties"].get("item_id") == iid:
                return eid
        return None

    if depth >= 2:
        for parent in row["parents"]:
            if parent is None or len(nodes) >= limit:
                break
            pid = dict(parent).get("item_id")
            if not pid:
                continue
            row2 = session.run(
                """
                MATCH (p:Process {item_id: $pid})
                OPTIONAL MATCH (gp:Process)-[:PARENT_OF]->(p)
                RETURN collect(DISTINCT gp)[0..$lim] AS grandparents
                """,
                pid=pid,
                lim=limit,
            ).single()
            if not row2:
                continue
            cpeid = eid_for_item_id(str(pid))
            if not cpeid:
                continue
            for gp in row2["grandparents"]:
                if gp is None:
                    continue
                gpeid = add_node(gp)
                edges.append(
                    {
                        "type": "PARENT_OF",
                        "from": gpeid,
                        "to": cpeid,
                        "parent_item_id": dict(gp).get("item_id"),
                        "child_item_id": pid,
                    }
                )
        for child in row["children"]:
            if child is None or len(nodes) >= limit:
                break
            cid = dict(child).get("item_id")
            if not cid:
                continue
            row3 = session.run(
                """
                MATCH (p:Process {item_id: $cid})
                OPTIONAL MATCH (p)-[:PARENT_OF]->(gc:Process)
                RETURN collect(DISTINCT gc)[0..$lim] AS grandchildren
                """,
                cid=cid,
                lim=limit,
            ).single()
            if not row3:
                continue
            peid = eid_for_item_id(str(cid))
            if not peid:
                continue
            for gc in row3["grandchildren"]:
                if gc is None:
                    continue
                gceid = add_node(gc)
                edges.append(
                    {
                        "type": "PARENT_OF",
                        "from": peid,
                        "to": gceid,
                        "parent_item_id": cid,
                        "child_item_id": dict(gc).get("item_id"),
                    }
                )

    out_nodes = list(nodes.values())[:limit]
    return {
        "status": "ok",
        "item_id": item_id,
        "depth": depth,
        "node_count": len(out_nodes),
        "edge_count": len(edges),
        "nodes": out_nodes,
        "edges": edges,
    }


def _match_role_root(session: Session, role_name: str) -> tuple[str, Any | None]:
    """Return (effective_role_name, row_or_none) for the Role root node.

    Tries ``role_name`` as stored in Neo4j, then a legacy digit-O alias ``05-1``
    when the canonical org token is ``O5-1`` (letter O).
    """
    q = "MATCH (r:Role {role_name: $name}) RETURN r AS node LIMIT 1"
    hit = session.run(q, name=role_name).single()
    if hit:
        return role_name, hit
    if role_name == "05-1":
        hit = session.run(q, name="O5-1").single()
        if hit:
            return "O5-1", hit
    return role_name, None


def role_neighbourhood(
    session: Session,
    role_name: str,
    *,
    depth: int,
    limit: int,
) -> dict[str, Any]:
    """Processes owned by or reporting to a role (depth capped)."""
    depth = max(1, min(int(depth), 4))
    limit = max(1, min(int(limit), 200))

    effective, hit = _match_role_root(session, role_name)
    if not hit:
        return {"status": "not_found", "role_name": role_name, "nodes": [], "edges": []}

    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    def add_node(n: Any) -> str:
        d = _node_to_dict(n)
        nodes[d["element_id"]] = d
        return d["element_id"]

    r_eid = add_node(hit["node"])

    rows = session.run(
        """
        MATCH (r:Role {role_name: $name})
        OPTIONAL MATCH (p:Process)-[:OWNED_BY]->(r)
        OPTIONAL MATCH (r)-[:REPORTS_TO]->(boss:Role)
        OPTIONAL MATCH (r2:Role)-[:REPORTS_TO]->(r)
        RETURN collect(DISTINCT p) AS owned, collect(DISTINCT boss) AS bosses, collect(DISTINCT r2) AS reports
        """,
        name=effective,
    ).single()
    assert rows is not None
    for p in rows["owned"]:
        if p is None:
            continue
        peid = add_node(p)
        edges.append({"type": "OWNED_BY", "from": peid, "to": r_eid})
    if depth > 1:
        for boss in rows["bosses"]:
            if boss is None:
                continue
            beid = add_node(boss)
            edges.append({"type": "REPORTS_TO", "from": r_eid, "to": beid})
        for r2 in rows["reports"]:
            if r2 is None:
                continue
            r2eid = add_node(r2)
            edges.append({"type": "REPORTS_TO", "from": r2eid, "to": r_eid})

    out_nodes = list(nodes.values())[:limit]
    out: dict[str, Any] = {
        "status": "ok",
        "role_name": effective,
        "depth": depth,
        "node_count": len(out_nodes),
        "edge_count": len(edges),
        "nodes": out_nodes,
        "edges": edges,
    }
    if effective != role_name:
        out["requested_role_name"] = role_name
        out["resolved_role_name"] = effective
    return out
