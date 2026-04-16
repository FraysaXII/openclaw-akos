#!/usr/bin/env python3
"""Operator HLK graph explorer (Streamlit + streamlit-agraph) — **secondary** UI.

Primary operator surface is the control plane ``GET /hlk/graph/explorer`` (same
auth as other ``/hlk/graph/*`` routes). This script mirrors the same **SSOT**
REST flow. Advanced interactions (drag-end pin / magnetic heuristic) can use
the optional **``vis_component``** engine (``streamlit.components.v1`` bundle
under ``static/streamlit_components/hlk_vis_network/``) or the HTML explorer at
``/hlk/graph/explorer`` (linked from this app) when CDN access is preferred.

Reads ``~/.openclaw/.env`` via ``bootstrap_openclaw_process_env``.

Usage:
    py scripts/hlk_graph_explorer.py
    py -m streamlit run scripts/hlk_graph_explorer.py

Requires: pip install streamlit streamlit-agraph httpx networkx
Env: AKOS_API_URL, AKOS_API_KEY (optional), AKOS_WEB_DASHBOARD_URL (optional WebChat URL),
     ``py scripts/serve-api.py`` for the control plane.
"""

from __future__ import annotations

import colorsys
import hashlib
import json
import math
import os
import subprocess
import sys
from collections import defaultdict, deque
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import bootstrap_openclaw_process_env

bootstrap_openclaw_process_env()

try:
    import httpx
    import streamlit as st
    import streamlit.components.v1 as st_components
    from streamlit_agraph import Config, Edge, Node, agraph
except ImportError as exc:
    print("Install: pip install httpx streamlit streamlit-agraph networkx", file=sys.stderr)
    raise SystemExit(1) from exc

try:
    import networkx as nx
except ImportError:
    nx = None  # type: ignore[misc, assignment]

_REPO_ROOT = Path(__file__).resolve().parent.parent
_FAVICON_PATH = _REPO_ROOT / "static" / "hlk_graph_explorer_favicon.png"
_VIS_COMPONENT_PATH = (_REPO_ROOT / "static" / "streamlit_components" / "hlk_vis_network").resolve()
_hlk_vis_network_func = None

_HERO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 56" width="52" height="52" aria-hidden="true">
  <rect width="56" height="56" rx="12" fill="#0b0f14"/>
  <circle cx="16" cy="28" r="5" fill="none" stroke="#e8eef5" stroke-width="1.6"/>
  <circle cx="40" cy="18" r="5" fill="none" stroke="#5eead4" stroke-width="1.6"/>
  <circle cx="38" cy="40" r="5" fill="none" stroke="#e8eef5" stroke-width="1.6"/>
  <path d="M21 28 L35 20" stroke="#94a3b8" stroke-width="1.2" fill="none"/>
  <path d="M35 23 L36 35" stroke="#94a3b8" stroke-width="1.2" fill="none"/>
  <path d="M21 28 L33 38" stroke="#5eead4" stroke-width="1" fill="none" opacity="0.85"/>
</svg>
"""

_PRESET_STATE_KEYS = (
    "explorer_lens",
    "graph_depth",
    "graph_limit",
    "graph_merge_cap",
    "graph_bulk_max_roles",
    "graph_bulk_max_projects",
    "graph_label_mode",
    "graph_label_focus",
    "graph_label_min_degree",
    "graph_layout_seed",
    "graph_use_physics",
    "graph_use_nx_seed",
    "graph_canvas_width",
    "graph_canvas_height",
    "graph_all_roles",
    "graph_all_projects",
    "graph_focus_substring",
    "graph_edge_labels",
    "graph_node_size_basis",
    "graph_layout_mode",
    "graph_tree_direction",
    "graph_engine",
    "graph_lock_layout",
    "graph_selected_id",
    "area_filter",
    "role_pick",
    "project_pick",
    "child_pick",
    "search_q",
    "search_hit_pick",
    "manual_pid",
    "akos_web_dashboard_url",
)


def _inject_brand_css() -> None:
    st.markdown(
        """
<style>
div[data-testid="stAppViewContainer"] > .main {
  background: hsl(220 16% 7%) !important;
}
div[data-testid="stAppViewContainer"] .block-container {
  padding-top: 1.25rem;
  padding-bottom: 2rem;
  max-width: 1280px;
}
section[data-testid="stSidebar"] {
  background: hsl(220 14% 10%) !important;
  border-right: 1px solid hsl(220 10% 20%);
}
section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {
  color: hsl(210 15% 90%);
}
section[data-testid="stSidebar"] .stCaption, section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
  color: hsl(215 10% 55%);
}
.hx-hero-row { display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; }
.hx-hero {
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  letter-spacing: -0.02em;
  color: hsl(210 15% 92%);
  font-size: 1.65rem;
  font-weight: 650;
  margin: 0 0 0.15rem 0;
}
.hx-lede {
  color: hsl(215 10% 58%);
  font-size: 0.95rem;
  line-height: 1.45;
  margin: 0 0 1rem 0;
}
.hx-pill {
  display: inline-block;
  padding: 0.12rem 0.55rem;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: hsl(168 50% 44%);
  border: 1px solid hsl(220 10% 22%);
  background: hsl(220 12% 14%);
  margin-bottom: 0.75rem;
}
.hx-panel {
  border: 1px solid hsl(220 10% 20%);
  border-radius: 12px;
  background: hsl(220 14% 10%);
  padding: 0.85rem 1rem 1rem 1rem;
  margin-top: 0.5rem;
}
.hx-panel-title {
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: hsl(215 10% 55%);
  margin-bottom: 0.35rem;
}
.hx-shell {
  font-size: 0.88rem;
  margin: 0.35rem 0 0.75rem 0;
}
.hx-shell a {
  color: hsl(168 50% 50%);
  text-decoration: none;
  margin-right: 1rem;
  font-weight: 500;
}
.hx-shell a:hover { text-decoration: underline; }
button[kind="primary"] {
  background: hsl(168 50% 40%) !important;
  border-color: hsl(168 50% 34%) !important;
  color: hsl(210 15% 98%) !important;
}
</style>
        """,
        unsafe_allow_html=True,
    )


def _base_url() -> str:
    return (st.session_state.get("akos_api_url") or os.environ.get("AKOS_API_URL") or "http://127.0.0.1:8420").rstrip(
        "/"
    )


def _bearer() -> str:
    return (st.session_state.get("akos_api_key_input") or os.environ.get("AKOS_API_KEY") or "").strip()


def _dashboard_url() -> str:
    return (
        (st.session_state.get("akos_web_dashboard_url") or os.environ.get("AKOS_WEB_DASHBOARD_URL") or "")
        .strip()
        .rstrip("/")
    )


def _api_get(path: str, params: dict | None = None) -> dict:
    base = _base_url()
    key = _bearer()
    headers = {"accept": "application/json"}
    if key:
        headers["authorization"] = f"Bearer {key}"
    url = f"{base}{path}"
    try:
        r = httpx.get(url, params=params or {}, headers=headers, timeout=60.0)
    except httpx.ConnectError as exc:
        return {
            "_http_error": 0,
            "_connect_failed": True,
            "detail": (
                f"Cannot reach API at {base} ({exc}). "
                "Start the control plane: py scripts/serve-api.py "
                "(or set AKOS_API_URL in the sidebar / env if using another port)."
            ),
        }
    except httpx.TimeoutException as exc:
        return {
            "_http_error": 0,
            "_connect_failed": True,
            "detail": f"Request timed out talking to {base}: {exc}",
        }
    if r.status_code >= 400:
        return {"_http_error": r.status_code, "detail": r.text[:500]}
    return r.json()


def _load_registry() -> None:
    areas = _api_get("/hlk/areas")
    roles = _api_get("/hlk/roles")
    procs = _api_get("/hlk/processes")
    if (
        "_http_error" in areas
        or "_http_error" in roles
        or "_http_error" in procs
        or areas.get("_connect_failed")
        or roles.get("_connect_failed")
        or procs.get("_connect_failed")
    ):
        st.session_state["_registry_error"] = {"areas": areas, "roles": roles, "processes": procs}
        return
    st.session_state["_registry_error"] = None
    st.session_state["areas_payload"] = areas
    st.session_state["roles_list"] = list(roles.get("roles") or [])
    st.session_state["projects_list"] = [
        p for p in (procs.get("processes") or []) if (p.get("item_granularity") or "") == "project"
    ]


def _filtered_roles(area_filter: str) -> list[dict]:
    roles = list(st.session_state.get("roles_list") or [])
    if not area_filter:
        return roles
    return [r for r in roles if (r.get("area") or "") == area_filter]


def _project_children(parent_item_id: str) -> list[dict]:
    if not parent_item_id.strip():
        return []
    data = _api_get(f"/hlk/processes/id/{quote(parent_item_id.strip(), safe='')}/tree")
    if "_http_error" in data:
        return []
    return list(data.get("processes") or [])


def _render_summary_metrics(summary: dict) -> None:
    if summary.get("_connect_failed"):
        st.error(summary.get("detail", summary))
        return
    if "_http_error" in summary:
        st.error(summary)
        return
    csv = summary.get("csv") or {}
    neo = summary.get("neo4j", "")
    c1, c2, c3 = st.columns(3)
    c1.metric("CSV roles (SSOT)", csv.get("roles", "—"))
    c2.metric("CSV processes (SSOT)", csv.get("processes", "—"))
    c3.metric("Neo4j mirror", neo if isinstance(neo, str) else str(neo))


def _parse_neighbourhood(data: dict) -> tuple[list[dict], list[dict]]:
    raw_nodes = data.get("nodes") or []
    if isinstance(raw_nodes, dict):
        raw_nodes = list(raw_nodes.values())
    parsed: list[dict] = []
    for i, n in enumerate(raw_nodes):
        if not isinstance(n, dict):
            continue
        props = n.get("properties") or {}
        labels = n.get("labels") or ["Node"]
        neo_label = str(labels[0] if labels else "Node")
        nid = str(n.get("element_id") or f"n{i}")
        title = (
            props.get("item_name")
            or props.get("role_name")
            or props.get("name")
            or props.get("item_id")
            or neo_label
        )
        parsed.append(
            {
                "id": nid,
                "title": str(title),
                "props": props,
                "neo_label": neo_label,
            }
        )
    edges: list[dict] = []
    for e in data.get("edges") or []:
        if not isinstance(e, dict):
            continue
        src = e.get("from")
        tgt = e.get("to")
        if not src or not tgt:
            continue
        edges.append({"source": str(src), "target": str(tgt), "type": str(e.get("type") or "")})
    return parsed, edges


def _label_for_mode(full: str, mode: str) -> str:
    if mode == "hide":
        return "·"
    if mode == "short":
        s = full.strip()
        return (s[:18] + "…") if len(s) > 19 else s
    return full[:56]


def _doi_label(
    full: str,
    label_mode: str,
    *,
    focus: str,
    degree: int,
    min_deg: int,
) -> str:
    if focus != "degree":
        return _label_for_mode(full, label_mode)
    if degree >= int(min_deg):
        return _label_for_mode(full, label_mode)
    return "·"


def _hex_to_rgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))  # type: ignore[misc]


def _rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    r, g, b = (max(0, min(1, x)) for x in rgb)
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))


def _node_color_base(neo_label: str) -> str:
    palette = {
        "Role": "#5eead4",
        "Process": "#94a3b8",
        "Document": "#cbd5e1",
        "Area": "#7dd3fc",
    }
    return palette.get(neo_label, "#64748b")


def _node_color_for(neo_label: str, stable_key: str) -> str:
    """Primary hue by Neo4j label + bounded lightness shift from a stable key."""
    base = _node_color_base(neo_label)
    h0 = hashlib.sha256(stable_key.encode("utf-8")).digest()
    delta = (h0[0] / 255.0 - 0.5) * 0.14  # ~±7% lightness
    r, g, b = _hex_to_rgb(base)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0.18, min(0.62, l + delta))
    return _rgb_to_hex(colorsys.hls_to_rgb(h, l, s))


def _rel_abbrev(rel_type: str) -> str:
    m = {
        "PARENT_OF": "parent",
        "OWNED_BY": "owns",
        "REPORTS_TO": "reports",
        "LINKS_TO": "link",
    }
    return m.get((rel_type or "").strip(), (rel_type or "rel")[:10].lower() or "rel")


def _edge_style(rel_type: str) -> dict:
    rt = (rel_type or "").strip()
    spec = {
        "PARENT_OF": ("rgba(94,234,212,0.55)", 3.2),
        "OWNED_BY": ("rgba(125,211,252,0.52)", 2.5),
        "REPORTS_TO": ("rgba(248,250,252,0.38)", 2.0),
        "LINKS_TO": ("rgba(148,163,184,0.48)", 1.6),
    }
    color, width = spec.get(rt, ("rgba(148,163,184,0.38)", 1.35))
    return {
        "color": color,
        "width": width,
        "smooth": {"type": "dynamic"},
        "arrows": {"to": {"enabled": True, "scaleFactor": 0.65}},
        "font": {"color": "#e8eef5", "size": 11, "strokeWidth": 0, "align": "middle"},
    }


def _edge_title(rel_type: str, src_id: str, tgt_id: str, id_to_name: dict[str, str]) -> str:
    a = id_to_name.get(src_id, src_id)
    b = id_to_name.get(tgt_id, tgt_id)
    rt = (rel_type or "").strip()
    if rt == "PARENT_OF":
        return f"{a} is parent of {b} (PARENT_OF)"
    if rt == "OWNED_BY":
        return f"{a} owned by role {b} (OWNED_BY)"
    if rt == "REPORTS_TO":
        return f"{a} reports to {b} (REPORTS_TO)"
    return f"{a} -[{rt}]-> {b}"


def _outgoing_parent_child_counts(edge_rows: list[dict], id_set: set[str]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for er in edge_rows:
        if er.get("type") != "PARENT_OF":
            continue
        u, v = er.get("source"), er.get("target")
        if u in id_set and v in id_set:
            counts[str(u)] += 1
    return dict(counts)


def _role_owned_process_counts(edge_rows: list[dict], id_set: set[str]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for er in edge_rows:
        if er.get("type") != "OWNED_BY":
            continue
        _proc, role = er.get("source"), er.get("target")
        if role in id_set:
            counts[str(role)] += 1
    return dict(counts)


def _metric_for_size_basis(
    nid: str,
    neo_label: str,
    *,
    basis: str,
    degree: int,
    child_out: int,
    role_owned: int,
) -> float:
    if basis == "degree":
        return float(degree)
    if basis == "children":
        if neo_label == "Role":
            return float(role_owned)
        if neo_label == "Process":
            return float(child_out)
        return 0.0
    # balanced
    hub = float(degree)
    treeish = float(role_owned if neo_label == "Role" else child_out if neo_label == "Process" else 0)
    return 0.45 * hub + 0.55 * treeish


def _node_size_from_metric(metric: float, *, len_boost: int, label_mode: str) -> int:
    base = 22 if label_mode == "hide" else 26
    curved = base + 10.0 * math.sqrt(max(0.0, metric))
    sz = int(curved + min(14, len_boost))
    return max(18, min(72, sz))


def _reports_to_cycle(edge_rows: list[dict], id_set: set[str]) -> bool:
    adj: dict[str, list[str]] = defaultdict(list)
    nodes: set[str] = set()
    for er in edge_rows:
        if er.get("type") != "REPORTS_TO":
            continue
        u, v = er.get("source"), er.get("target")
        if u not in id_set or v not in id_set:
            continue
        adj[str(u)].append(str(v))
        nodes.add(str(u))
        nodes.add(str(v))
    if not nodes:
        return False
    state: dict[str, int] = {}

    def dfs(u: str) -> bool:
        state[u] = 1
        for v in adj.get(u, []):
            if v not in state:
                if dfs(v):
                    return True
            elif state.get(v) == 1:
                return True
        state[u] = 2
        return False

    for n in nodes:
        if n not in state and dfs(n):
            return True
    return False


def _find_tree_root_eid(data: dict, parsed: list[dict], id_set: set[str], degree: dict[str, int]) -> str | None:
    iid = str(data.get("item_id") or "").strip()
    if iid:
        for p in parsed:
            if p["id"] not in id_set or p.get("neo_label") != "Process":
                continue
            props = p.get("props") or {}
            if str(props.get("item_id") or "") == iid:
                return str(p["id"])
    rn = str(data.get("role_name") or "").strip()
    if rn:
        for p in parsed:
            if p["id"] not in id_set or p.get("neo_label") != "Role":
                continue
            props = p.get("props") or {}
            if str(props.get("role_name") or "") == rn:
                return str(p["id"])
    proc_ids = [str(p["id"]) for p in parsed if p["id"] in id_set and p.get("neo_label") == "Process"]
    if proc_ids:
        return max(proc_ids, key=lambda x: degree.get(x, 0))
    for p in parsed:
        if p["id"] in id_set:
            return str(p["id"])
    return None


def _bfs_levels(root: str, id_set: set[str], pairs: list[tuple[str, str]]) -> dict[str, int]:
    adj: dict[str, set[str]] = defaultdict(set)
    for u, v in pairs:
        if u in id_set and v in id_set:
            adj[u].add(v)
            adj[v].add(u)
    dist: dict[str, int] = {root: 0}
    q: deque[str] = deque([root])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    far = max(dist.values()) if dist else 0
    for nid in id_set:
        if nid not in dist:
            dist[nid] = far + 1
    m = min(dist.values()) if dist else 0
    return {k: v - m for k, v in dist.items()}


def _parent_of_child_map(edge_rows: list[dict], id_set: set[str]) -> dict[str, str]:
    """PARENT_OF: parent (from) -> child (to); return child -> parent."""
    out: dict[str, str] = {}
    for er in edge_rows:
        if er.get("type") != "PARENT_OF":
            continue
        u, v = er.get("source"), er.get("target")
        if u in id_set and v in id_set:
            out[str(v)] = str(u)
    return out


def _spring_positions(node_ids: list[str], pairs: list[tuple[str, str]], seed: int) -> dict[str, tuple[float, float]]:
    if nx is None or len(node_ids) == 0:
        return {}
    g = nx.Graph()
    g.add_nodes_from(node_ids)
    g.add_edges_from(pairs)
    if g.number_of_nodes() == 0:
        return {}
    k = max(0.15, 2.2 / (len(node_ids) ** 0.5))
    pos = nx.spring_layout(g, seed=int(seed) % (2**31 - 1), iterations=60, k=k)
    scale = 520.0
    return {nid: (float(xy[0]) * scale, float(xy[1]) * scale) for nid, xy in pos.items()}


def _merge_neighbourhood_payloads(parts: list[dict], *, max_nodes: int, max_edges: int) -> dict:
    nodes_by_eid: dict[str, dict] = {}
    edges_out: list[dict] = []
    seen_e: set[tuple[str, str, str]] = set()
    for data in parts:
        if not isinstance(data, dict) or data.get("_connect_failed") or "_http_error" in data:
            continue
        raw_nodes = data.get("nodes") or []
        if isinstance(raw_nodes, dict):
            raw_nodes = list(raw_nodes.values())
        for n in raw_nodes:
            if not isinstance(n, dict):
                continue
            eid = str(n.get("element_id") or "")
            if not eid:
                continue
            if eid not in nodes_by_eid and len(nodes_by_eid) >= max_nodes:
                continue
            nodes_by_eid[eid] = n
        for e in data.get("edges") or []:
            if not isinstance(e, dict):
                continue
            a, b = e.get("from"), e.get("to")
            if not a or not b:
                continue
            typ = str(e.get("type") or "")
            key = (str(a), str(b), typ)
            if key in seen_e:
                continue
            if len(edges_out) >= max_edges:
                break
            seen_e.add(key)
            edges_out.append(dict(e))
    return {
        "status": "ok",
        "nodes": list(nodes_by_eid.values()),
        "edges": edges_out,
        "node_count": len(nodes_by_eid),
        "edge_count": len(edges_out),
    }


def _api_neighbourhood_ok(d: dict) -> bool:
    if not isinstance(d, dict) or d.get("_connect_failed") or "_http_error" in d:
        return False
    if str(d.get("status") or "") == "not_found":
        return False
    return True


def _show_fetch_error(d: dict) -> None:
    if d.get("_connect_failed"):
        st.error(d.get("detail", d))
        return
    if "_http_error" in d:
        st.error(d)
        return
    if str(d.get("status") or "") == "not_found":
        st.warning(d)
        return
    st.error(d)


def _vis_config(
    width: int,
    height: int,
    *,
    physics_enabled: bool,
    hierarchical: bool,
    tree_direction: str,
) -> Config:
    cfg = Config(
        width=int(width),
        height=int(height),
        directed=True,
        physics=physics_enabled,
        hierarchical=hierarchical,
        maxVelocity=26,
        timestep=0.38,
        minVelocity=0.75,
        direction=str(tree_direction or "UD"),
        sortMethod="hubsize",
        levelSeparation=185,
        nodeSpacing=135,
        treeSpacing=210,
    )
    if hierarchical and isinstance(getattr(cfg, "layout", None), dict):
        lay = cfg.layout.get("hierarchical")
        if isinstance(lay, dict):
            lay["shakeTowards"] = "roots"
    if physics_enabled and isinstance(getattr(cfg, "physics", None), dict):
        cfg.physics["barnesHut"] = {
            "gravitationalConstant": -9000,
            "centralGravity": 0.22,
            "springLength": 210,
            "springConstant": 0.038,
            "damping": 0.58,
            "avoidOverlap": 0.72,
        }
        cfg.physics["stabilization"] = {
            "enabled": True,
            "iterations": 140,
            "updateInterval": 30,
            "onlyDynamicEdges": False,
            "fit": True,
        }
    return cfg


def _config_to_vis_options(cfg: Config) -> dict:
    """vis-network options dict aligned with streamlit-agraph Config."""
    d = cfg.to_dict()
    phys = dict(d.get("physics") or {})
    lay = dict(d.get("layout") or {})
    return {
        "physics": phys,
        "layout": lay,
        "interaction": {"hover": True, "multiselect": True, "navigationButtons": False},
        "nodes": {"font": {"color": "#f1f5f9", "size": 14, "strokeWidth": 2, "strokeColor": "#0f172a"}},
        "edges": {"font": {"color": "#e8eef5", "size": 11, "strokeWidth": 0}},
    }


def _to_streamlit_graph(
    data: dict,
    *,
    label_mode: str,
    label_focus: str,
    label_min_degree: int,
    layout_seed: int,
    use_physics: bool,
    use_nx_seed: bool,
    focus_substring: str,
    edge_label_mode: str,
    node_size_basis: str,
    layout_mode: str,
    tree_direction: str,
    lock_layout: bool,
) -> tuple[list[Node], list[Edge], dict, dict]:
    parsed, edge_rows = _parse_neighbourhood(data)
    id_set = {p["id"] for p in parsed}
    pairs: list[tuple[str, str]] = []
    for er in edge_rows:
        u, v = er["source"], er["target"]
        if u in id_set and v in id_set:
            pairs.append((str(u), str(v)))
    degree: dict[str, int] = {nid: 0 for nid in id_set}
    for u, v in pairs:
        degree[u] = degree.get(u, 0) + 1
        degree[v] = degree.get(v, 0) + 1

    child_out = _outgoing_parent_child_counts(edge_rows, id_set)
    role_owned = _role_owned_process_counts(edge_rows, id_set)

    tree_force_fallback = False
    tree_reason = ""
    hierarchical = False
    if str(layout_mode) == "tree":
        if _reports_to_cycle(edge_rows, id_set):
            tree_force_fallback = True
            tree_reason = "REPORTS_TO cycle detected — hierarchical layout disabled; using force layout."
        else:
            hierarchical = True

    use_tree = hierarchical and not tree_force_fallback
    effective_lock = bool(lock_layout and nx is not None)
    want_nx_seed = bool(use_physics and use_nx_seed and nx is not None and not use_tree and not effective_lock)
    want_fixed_only = ((not use_physics) or effective_lock) and (nx is not None) and not use_tree

    positions: dict[str, tuple[float, float]] = {}
    if want_fixed_only or want_nx_seed:
        positions = _spring_positions(sorted(id_set), pairs, layout_seed)

    id_to_name = {p["id"]: str(p["title"]) for p in parsed}

    levels: dict[str, int] = {}
    if use_tree:
        root = _find_tree_root_eid(data, parsed, id_set, degree)
        if root:
            levels = _bfs_levels(root, id_set, pairs)

    fs = (focus_substring or "").strip().lower()
    nodes_out: list[Node] = []
    node_detail: dict[str, dict] = {}
    for p in parsed:
        nid = p["id"]
        full = p["title"]
        props = p.get("props") or {}
        stable_key = str(props.get("item_id") or props.get("role_name") or nid)
        lbl = _doi_label(full, label_mode, focus=label_focus, degree=degree.get(nid, 0), min_deg=label_min_degree)
        tip = json.dumps(props, indent=2)[:2400]
        neo = str(p.get("neo_label") or "Node")
        metric = _metric_for_size_basis(
            nid,
            neo,
            basis=str(node_size_basis),
            degree=degree.get(nid, 0),
            child_out=int(child_out.get(nid, 0)),
            role_owned=int(role_owned.get(nid, 0)),
        )
        len_boost = min(28, max(0, len(lbl) - 6) * 2)
        size = _node_size_from_metric(metric, len_boost=len_boost, label_mode=label_mode)
        color = _node_color_for(neo, stable_key)
        if fs and (fs in nid.lower() or fs in full.lower()):
            color = "#f8fafc"
        font_sz = 14 if label_mode != "hide" else 11
        kwargs: dict = {
            "shape": "dot",
            "font": {
                "color": "#f1f5f9",
                "size": font_sz,
                "strokeWidth": 2,
                "strokeColor": "#0f172a",
            },
        }
        if use_tree and nid in levels:
            kwargs["level"] = int(levels[nid])
        if want_fixed_only and positions:
            xy = positions.get(nid)
            if xy is not None:
                kwargs["x"] = float(xy[0])
                kwargs["y"] = float(xy[1])
                kwargs["physics"] = False
        elif want_nx_seed and positions:
            xy = positions.get(nid)
            if xy is not None:
                kwargs["x"] = float(xy[0])
                kwargs["y"] = float(xy[1])
        nodes_out.append(
            Node(
                id=nid,
                label=lbl,
                title=tip,
                color=color,
                size=size,
                **kwargs,
            )
        )
        node_detail[nid] = {"title": full, "neo_label": neo, "props": props}

    n_edges = sum(1 for er in edge_rows if er["source"] in id_set and er["target"] in id_set)
    auto_hover_only = n_edges > 120
    elab = str(edge_label_mode or "auto")
    if elab == "auto":
        show_edge_label = not auto_hover_only
    elif elab == "always":
        show_edge_label = True
    else:
        show_edge_label = False

    edges_out: list[Edge] = []
    for er in edge_rows:
        u, v = er["source"], er["target"]
        if u not in id_set or v not in id_set:
            continue
        rt = str(er.get("type") or "")
        sty = _edge_style(rt)
        abbrev = _rel_abbrev(rt)
        etitle = _edge_title(rt, str(u), str(v), id_to_name)
        label = abbrev if show_edge_label else ""
        edges_out.append(
            Edge(
                source=str(u),
                target=str(v),
                label=label,
                title=etitle,
                **sty,
            )
        )

    layout_desc = "physics"
    if use_tree:
        layout_desc = "tree-hierarchical"
    elif want_fixed_only and positions:
        layout_desc = "networkx-fixed"
    elif want_nx_seed and positions:
        layout_desc = "physics+nx-seed"
    elif use_physics:
        layout_desc = "physics"

    meta = {
        "nodes": len(nodes_out),
        "edges": len(edges_out),
        "layout": layout_desc,
        "node_detail": node_detail,
        "tree_force_fallback": tree_force_fallback,
        "tree_reason": tree_reason,
        "use_tree": use_tree,
    }

    parent_map = _parent_of_child_map(edge_rows, id_set)
    vis_bundle = {
        "nodes": [n.to_dict() for n in nodes_out],
        "edges": [e.to_dict() for e in edges_out],
        "parentMap": parent_map,
    }
    return nodes_out, edges_out, meta, vis_bundle


def _get_hlk_vis_network_component():
    global _hlk_vis_network_func
    if _hlk_vis_network_func is None:
        _hlk_vis_network_func = st_components.declare_component(
            "hlk_vis_network",
            path=str(_VIS_COMPONENT_PATH),
        )
    return _hlk_vis_network_func


def _render_graph_legend() -> None:
    rows = [
        ("Role", _node_color_base("Role"), "Neo4j Role (+ stable id hue nudge)"),
        ("Process", _node_color_base("Process"), "Neo4j Process"),
        ("Document", _node_color_base("Document"), "Document"),
        ("Area", _node_color_base("Area"), "Area"),
        ("PARENT_OF", _edge_style("PARENT_OF")["color"], "Parent → child (thicker / teal)"),
        ("OWNED_BY", _edge_style("OWNED_BY")["color"], "Process → owning role"),
        ("REPORTS_TO", _edge_style("REPORTS_TO")["color"], "Role hierarchy"),
    ]
    parts = [
        "<div style='font-size:0.85rem;color:#cbd5e1;line-height:1.5'>",
        "<strong>Nodes</strong>: size basis uses outgoing <code>PARENT_OF</code> children for processes, "
        "and <code>OWNED_BY</code> fan-in for roles (toggle in sidebar).<br/>",
        "<strong>Edges</strong>: abbreviated labels on canvas (or hover-only); full type + endpoints in edge tooltip.",
        "<table style='margin-top:0.5rem;border-collapse:collapse;width:100%'>",
    ]
    for name, color, note in rows:
        parts.append(
            "<tr><td style='width:2.2rem;padding:0.2rem 0'>"
            f"<span style='display:inline-block;width:1.5rem;height:0.85rem;background:{color};"
            "border-radius:3px;border:1px solid #334155'></span></td>"
            f"<td style='padding:0.2rem 0.4rem'><code>{name}</code></td>"
            f"<td style='padding:0.2rem;color:#94a3b8'>{note}</td></tr>"
        )
    parts.append("</table></div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def _render_graph_canvas(payload: dict) -> None:
    if payload.get("_connect_failed"):
        st.error(payload.get("detail", payload))
        return
    if "_http_error" in payload:
        st.error(payload)
        return
    label_mode = st.session_state.get("graph_label_mode") or "short"
    label_focus = st.session_state.get("graph_label_focus") or "uniform"
    label_min_degree = int(st.session_state.get("graph_label_min_degree") or 3)
    layout_seed = int(st.session_state.get("graph_layout_seed") or 42)
    use_physics = bool(st.session_state.get("graph_use_physics"))
    use_nx_seed = bool(st.session_state.get("graph_use_nx_seed"))
    focus_substring = str(st.session_state.get("graph_focus_substring") or "")
    edge_label_mode = str(st.session_state.get("graph_edge_labels") or "auto")
    node_size_basis = str(st.session_state.get("graph_node_size_basis") or "children")
    layout_mode = str(st.session_state.get("graph_layout_mode") or "force")
    tree_direction = str(st.session_state.get("graph_tree_direction") or "UD")
    graph_engine = str(st.session_state.get("graph_engine") or "agraph")
    lock_layout = bool(st.session_state.get("graph_lock_layout"))

    w = int(st.session_state.get("graph_canvas_width") or 1180)
    h = int(st.session_state.get("graph_canvas_height") or 680)
    with st.expander("Raw neighbourhood JSON", expanded=False):
        st.json(payload)
    nodes, edges, meta, vis_bundle = _to_streamlit_graph(
        payload,
        label_mode=str(label_mode),
        label_focus=str(label_focus),
        label_min_degree=label_min_degree,
        layout_seed=layout_seed,
        use_physics=use_physics,
        use_nx_seed=use_nx_seed,
        focus_substring=focus_substring,
        edge_label_mode=edge_label_mode,
        node_size_basis=node_size_basis,
        layout_mode=layout_mode,
        tree_direction=tree_direction,
        lock_layout=lock_layout,
    )
    if not nodes:
        st.warning("No nodes to draw (empty neighbourhood or unexpected payload).")
        return
    if meta.get("tree_force_fallback") and str(meta.get("tree_reason")):
        st.info(meta["tree_reason"])

    with st.expander("Color & link legend", expanded=False):
        _render_graph_legend()

    st.caption(f"{meta['nodes']} nodes · {meta['edges']} edges · layout: {meta['layout']}")

    use_tree = bool(meta.get("use_tree"))
    vis_physics = (use_physics or (nx is None)) and not lock_layout and not use_tree
    if use_tree:
        vis_physics = False

    cfg = _vis_config(w, h, physics_enabled=vis_physics, hierarchical=use_tree, tree_direction=tree_direction)
    vis_options = _config_to_vis_options(cfg)

    if graph_engine == "vis_component":
        if not (_VIS_COMPONENT_PATH / "index.html").is_file():
            st.error(f"vis component frontend missing: {_VIS_COMPONENT_PATH / 'index.html'}")
            return
        st.session_state.setdefault("vis_graph_state", {"pinnedIds": [], "positions": {}, "selectedId": None})
        comp = _get_hlk_vis_network_component()
        vs = st.session_state["vis_graph_state"]
        graph_arg = {
            "nodes": vis_bundle["nodes"],
            "edges": vis_bundle["edges"],
            "options": vis_options,
            "parentMap": vis_bundle["parentMap"],
            "pinnedIds": list(vs.get("pinnedIds") or []),
            "positions": dict(vs.get("positions") or {}),
        }
        ret = comp(
            graph=graph_arg,
            key="hlk_vis_network_canvas",
            default=None,
            height=int(h),
        )
        if isinstance(ret, dict):
            st.session_state["vis_graph_state"] = {
                "pinnedIds": list(ret.get("pinnedIds") or []),
                "positions": dict(ret.get("positions") or {}),
                "selectedId": ret.get("selectedId"),
            }
            sid = ret.get("selectedId")
            if sid:
                st.session_state["graph_selected_id"] = str(sid)
    else:
        picked = agraph(nodes=nodes, edges=edges, config=cfg)
        if isinstance(picked, dict) and picked.get("id") is not None:
            st.session_state["graph_selected_id"] = str(picked.get("id"))
        elif isinstance(picked, str) and picked.strip():
            st.session_state["graph_selected_id"] = picked.strip()

    sel = str(st.session_state.get("graph_selected_id") or "").strip()
    detail = (meta.get("node_detail") or {}).get(sel) if sel else None
    with st.expander("Selected node", expanded=False):
        if not sel:
            st.caption("Click a node in the graph to bind selection (streamlit-agraph) or use the vis component.")
        elif not detail:
            st.write(f"**{sel}** (no parsed detail in this payload)")
        else:
            st.markdown(f"**{detail.get('title', sel)}** · `{detail.get('neo_label', '')}`")
            st.json(detail.get("props") or {})


def _push_graph_history(title: str, subtitle: str, payload: dict, meta: dict) -> None:
    hist = list(st.session_state.get("_graph_history") or [])
    entry = {"title": title, "subtitle": subtitle, "payload": payload, "meta": meta}
    hist.insert(0, entry)
    st.session_state["_graph_history"] = hist[:18]
    st.session_state["current_graph"] = {"title": title, "subtitle": subtitle, "payload": payload, "meta": meta}
    st.session_state["_history_choice_idx"] = 0


def _on_history_pick() -> None:
    hist = list(st.session_state.get("_graph_history") or [])
    idx = int(st.session_state.get("_history_choice_idx") or 0)
    if hist and 0 <= idx < len(hist):
        h = hist[idx]
        st.session_state["current_graph"] = {
            "title": h["title"],
            "subtitle": h.get("subtitle", ""),
            "payload": h["payload"],
            "meta": h.get("meta", {}),
        }


def _resolve_process_target() -> str:
    child_id = (st.session_state.get("child_pick") or "").strip()
    project_id = (st.session_state.get("project_pick") or "").strip()
    hit = (st.session_state.get("search_hit_pick") or "").strip()
    pick_pid = hit[2:] if hit.startswith("p:") else ""
    manual = (st.session_state.get("manual_pid") or "").strip()
    return (child_id or project_id or pick_pid or manual).strip()


def _role_names_for_bulk() -> list[str]:
    area_filter = (st.session_state.get("area_filter") or "").strip()
    roles_opts = _filtered_roles(area_filter)
    names = sorted({str(r.get("role_name") or "").strip() for r in roles_opts if r.get("role_name")})
    return [n for n in names if n]


def _project_ids_for_bulk() -> list[str]:
    projects = st.session_state.get("projects_list") or []
    return [str(p.get("item_id") or "").strip() for p in projects if p.get("item_id")]


def _fetch_and_push_canvas(*, depth: int, limit: int) -> bool:
    merge_cap = int(st.session_state.get("graph_merge_cap") or 500)
    max_roles = int(st.session_state.get("graph_bulk_max_roles") or 40)
    max_projs = int(st.session_state.get("graph_bulk_max_projects") or 25)
    lens = str(st.session_state.get("explorer_lens") or "Role")

    if lens == "Role" and bool(st.session_state.get("graph_all_roles")):
        names = _role_names_for_bulk()[:max_roles]
        if not names:
            st.error("No roles in registry for bulk fetch.")
            return False
        parts: list[dict] = []
        prog = st.progress(0)
        for i, rn in enumerate(names):
            enc = quote(rn, safe="")
            d = _api_get(f"/hlk/graph/role/{enc}/neighbourhood", params={"depth": depth, "limit": limit})
            parts.append(d)
            prog.progress((i + 1) / max(1, len(names)))
        prog.empty()
        bad = [d for d in parts if not _api_neighbourhood_ok(d)]
        if bad:
            _show_fetch_error(bad[0])
            return False
        merged = _merge_neighbourhood_payloads(parts, max_nodes=merge_cap, max_edges=8000)
        title = f"Bulk roles · {len(names)} roles · ≤{merge_cap} nodes"
        subtitle = f"depth={depth}, per-call limit={limit}"
        meta = {"kind": "bulk_roles", "roles_count": len(names), "depth": depth, "limit": limit}
        _push_graph_history(title, subtitle, merged, meta)
        return True

    if lens == "Process" and bool(st.session_state.get("graph_all_projects")):
        ids = _project_ids_for_bulk()[:max_projs]
        if not ids:
            st.error("No projects in registry for bulk fetch.")
            return False
        parts = []
        prog = st.progress(0)
        for i, pid in enumerate(ids):
            enc = quote(pid, safe="")
            d = _api_get(f"/hlk/graph/process/{enc}/neighbourhood", params={"depth": depth, "limit": limit})
            parts.append(d)
            prog.progress((i + 1) / max(1, len(ids)))
        prog.empty()
        bad = [d for d in parts if not _api_neighbourhood_ok(d)]
        if bad:
            _show_fetch_error(bad[0])
            return False
        merged = _merge_neighbourhood_payloads(parts, max_nodes=merge_cap, max_edges=8000)
        title = f"Bulk projects · {len(ids)} roots · ≤{merge_cap} nodes"
        subtitle = f"depth={depth}, per-call limit={limit}"
        meta = {"kind": "bulk_projects", "projects_count": len(ids), "depth": depth, "limit": limit}
        _push_graph_history(title, subtitle, merged, meta)
        return True

    if lens == "Role":
        role_pick = (st.session_state.get("role_pick") or "").strip()
        if not role_pick:
            st.error("Select a role, or enable **All roles (bulk)**.")
            return False
        enc = quote(role_pick, safe="")
        data = _api_get(f"/hlk/graph/role/{enc}/neighbourhood", params={"depth": depth, "limit": limit})
        if not _api_neighbourhood_ok(data):
            _show_fetch_error(data)
            return False
        _push_graph_history(
            f"Role · {role_pick}",
            f"depth={depth}, limit={limit}",
            data,
            {"kind": "role", "role": role_pick, "depth": depth, "limit": limit},
        )
        return True

    if lens == "Process":
        target = _resolve_process_target()
        if not target:
            st.error("Pick a project, child, search hit, manual id—or enable **All projects (bulk)**.")
            return False
        enc = quote(target, safe="")
        data = _api_get(f"/hlk/graph/process/{enc}/neighbourhood", params={"depth": depth, "limit": limit})
        if not _api_neighbourhood_ok(data):
            _show_fetch_error(data)
            return False
        _push_graph_history(
            f"Process · {target}",
            f"depth={depth}, limit={limit}",
            data,
            {"kind": "process", "item_id": target, "depth": depth, "limit": limit},
        )
        return True

    st.warning("Switch to **Role** or **Process** to fetch.")
    return False


def _refetch_current_canvas() -> bool:
    cg = st.session_state.get("current_graph") or {}
    meta = cg.get("meta") or {}
    depth = int(st.session_state.get("graph_depth") or 2)
    limit = int(st.session_state.get("graph_limit") or 80)
    kind = meta.get("kind")
    if kind == "role" and meta.get("role"):
        st.session_state["explorer_lens"] = "Role"
        st.session_state["graph_all_roles"] = False
        st.session_state["role_pick"] = meta["role"]
        enc = quote(str(meta["role"]), safe="")
        data = _api_get(f"/hlk/graph/role/{enc}/neighbourhood", params={"depth": depth, "limit": limit})
        if not _api_neighbourhood_ok(data):
            _show_fetch_error(data)
            return False
        _push_graph_history(f"Role · {meta['role']}", f"depth={depth}, limit={limit}", data, meta)
        return True
    if kind == "process" and meta.get("item_id"):
        st.session_state["explorer_lens"] = "Process"
        st.session_state["graph_all_projects"] = False
        pid = str(meta["item_id"])
        enc = quote(pid, safe="")
        data = _api_get(f"/hlk/graph/process/{enc}/neighbourhood", params={"depth": depth, "limit": limit})
        if not _api_neighbourhood_ok(data):
            _show_fetch_error(data)
            return False
        _push_graph_history(f"Process · {pid}", f"depth={depth}, limit={limit}", data, meta)
        return True
    if kind == "bulk_roles":
        st.session_state["explorer_lens"] = "Role"
        st.session_state["graph_all_roles"] = True
        return _fetch_and_push_canvas(depth=depth, limit=limit)
    if kind == "bulk_projects":
        st.session_state["explorer_lens"] = "Process"
        st.session_state["graph_all_projects"] = True
        return _fetch_and_push_canvas(depth=depth, limit=limit)
    st.info("No refetch target on current canvas.")
    return False


def _preset_fetch_params(preset: dict) -> tuple[str, str] | None:
    """Returns (fetch_lens, fetch_target) or None if cannot infer."""
    v = int(preset.get("v") or 1)
    if v >= 2 and preset.get("fetch_lens"):
        return str(preset["fetch_lens"]), str(preset.get("fetch_target") or "")
    lens = str(preset.get("explorer_lens") or "Role")
    if lens == "Role":
        if preset.get("graph_all_roles"):
            return "bulk_roles", ""
        rp = str(preset.get("role_pick") or "").strip()
        if rp:
            return "role", rp
    if lens == "Process":
        if preset.get("graph_all_projects"):
            return "bulk_projects", ""
        ft = str(preset.get("effective_process_target") or "").strip()
        if ft:
            return "process", ft
    return None


def _collect_preset(name: str) -> dict:
    preset: dict = {"v": 2, "name": name.strip()}
    for k in _PRESET_STATE_KEYS:
        if k in st.session_state:
            preset[k] = st.session_state[k]
    preset["effective_process_target"] = _resolve_process_target()
    cg = st.session_state.get("current_graph") or {}
    meta = cg.get("meta") or {}
    if meta.get("kind") == "role" and meta.get("role"):
        preset["fetch_lens"] = "role"
        preset["fetch_target"] = meta["role"]
    elif meta.get("kind") == "process" and meta.get("item_id"):
        preset["fetch_lens"] = "process"
        preset["fetch_target"] = meta["item_id"]
    elif meta.get("kind") == "bulk_roles":
        preset["fetch_lens"] = "bulk_roles"
        preset["fetch_target"] = ""
    elif meta.get("kind") == "bulk_projects":
        preset["fetch_lens"] = "bulk_projects"
        preset["fetch_target"] = ""
    else:
        pair = _preset_fetch_params(preset)
        if pair:
            preset["fetch_lens"], preset["fetch_target"] = pair
    return preset


def _apply_preset(preset: dict) -> None:
    for k in _PRESET_STATE_KEYS:
        if k in preset:
            st.session_state[k] = preset[k]


def _sync_search_to_role() -> None:
    h = st.session_state.get("search_hit_pick", "")
    if h.startswith("r:"):
        name = h[2:]
        opts = st.session_state.get("_role_option_names") or []
        if name in opts:
            st.session_state["role_pick"] = name


def _shell_links_html() -> str:
    base = _base_url()
    dash = _dashboard_url()
    parts = [
        f'<a href="{base}/hlk/graph/explorer" target="_blank" rel="noopener noreferrer">HTML graph explorer</a>',
        f'<a href="{base}/docs" target="_blank" rel="noopener noreferrer">API docs</a>',
    ]
    if dash:
        parts.append(f'<a href="{dash}/" target="_blank" rel="noopener noreferrer">Web dashboard</a>')
    return '<p class="hx-shell">' + " · ".join(parts) + "</p>"


def main() -> None:
    page_icon: str | Path = str(_FAVICON_PATH) if _FAVICON_PATH.is_file() else "🕸️"
    st.set_page_config(
        page_title="HLK Graph Explorer",
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _inject_brand_css()

    if "akos_api_url" not in st.session_state:
        st.session_state["akos_api_url"] = os.environ.get("AKOS_API_URL", "http://127.0.0.1:8420").rstrip("/")
    if "akos_api_key_input" not in st.session_state:
        st.session_state["akos_api_key_input"] = os.environ.get("AKOS_API_KEY") or ""
    st.session_state.setdefault("akos_web_dashboard_url", os.environ.get("AKOS_WEB_DASHBOARD_URL", ""))
    if "graph_depth" not in st.session_state:
        st.session_state["graph_depth"] = 2
    if "graph_limit" not in st.session_state:
        st.session_state["graph_limit"] = 80
    if "graph_merge_cap" not in st.session_state:
        st.session_state["graph_merge_cap"] = 500
    if "graph_bulk_max_roles" not in st.session_state:
        st.session_state["graph_bulk_max_roles"] = 40
    if "graph_bulk_max_projects" not in st.session_state:
        st.session_state["graph_bulk_max_projects"] = 25
    if "graph_label_mode" not in st.session_state:
        st.session_state["graph_label_mode"] = "short"
    if "graph_label_focus" not in st.session_state:
        st.session_state["graph_label_focus"] = "uniform"
    if "graph_label_min_degree" not in st.session_state:
        st.session_state["graph_label_min_degree"] = 3
    if "graph_layout_seed" not in st.session_state:
        st.session_state["graph_layout_seed"] = 42
    if "graph_use_physics" not in st.session_state:
        st.session_state["graph_use_physics"] = True
    if "graph_use_nx_seed" not in st.session_state:
        st.session_state["graph_use_nx_seed"] = True
    if "graph_canvas_width" not in st.session_state:
        st.session_state["graph_canvas_width"] = 1180
    if "graph_canvas_height" not in st.session_state:
        st.session_state["graph_canvas_height"] = 680
    if "graph_all_roles" not in st.session_state:
        st.session_state["graph_all_roles"] = False
    if "graph_all_projects" not in st.session_state:
        st.session_state["graph_all_projects"] = False
    if "graph_focus_substring" not in st.session_state:
        st.session_state["graph_focus_substring"] = ""
    st.session_state.setdefault("graph_edge_labels", "auto")
    st.session_state.setdefault("graph_node_size_basis", "children")
    st.session_state.setdefault("graph_layout_mode", "force")
    st.session_state.setdefault("graph_tree_direction", "UD")
    st.session_state.setdefault("graph_engine", "agraph")
    st.session_state.setdefault("graph_lock_layout", False)
    st.session_state.setdefault("graph_selected_id", "")
    st.session_state.setdefault("explorer_lens", "Role")
    if "_graph_history" not in st.session_state:
        st.session_state["_graph_history"] = []
    if "saved_lenses" not in st.session_state:
        st.session_state["saved_lenses"] = []

    st.markdown('<p class="hx-pill">Holistika · HLK graph</p>', unsafe_allow_html=True)
    c0, c1 = st.columns([0.09, 0.91])
    with c0:
        st.markdown(_HERO_SVG, unsafe_allow_html=True)
    with c1:
        st.markdown('<h1 class="hx-hero">HLK Graph Explorer</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hx-lede">Read-only canvas: registry from <code>/hlk/*</code>, neighbourhoods from '
        "<code>/hlk/graph/*</code> — same SSOT as the FastAPI explorer. "
        "<strong>(No memorized IDs.)</strong> Pickers, search, and optional manual fallback carry "
        "<code>item_id</code> values for you.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(_shell_links_html(), unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("##### Connection")
        st.session_state["akos_api_url"] = st.text_input(
            "API base URL",
            value=st.session_state["akos_api_url"],
            help="Control plane base URL (same host as `py scripts/serve-api.py`). Used to build links to the HTML explorer and OpenAPI docs.",
        )
        st.session_state["akos_api_key_input"] = st.text_input(
            "Access token (optional)",
            value=st.session_state["akos_api_key_input"],
            type="password",
            help="Bearer token when the API enforces AKOS_API_KEY. Never logged; kept only in this Streamlit session.",
        )
        st.session_state["akos_web_dashboard_url"] = st.text_input(
            "Web dashboard URL (optional)",
            value=st.session_state.get("akos_web_dashboard_url") or "",
            help="e.g. your OpenClaw WebChat origin if different from the API. Env override: AKOS_WEB_DASHBOARD_URL. Shown as a shell link when set.",
        )
        st.divider()
        with st.expander("Control glossary", expanded=False):
            st.markdown(
                """
- **Lens**: whether you target a role, a process, or a saved preset.
- **Depth / limit**: Neo4j hop depth and per-call node cap (server-capped).
- **Bulk**: merge many role or project neighbourhoods into one canvas (respect merge cap).
- **Physics**: vis force simulation (default on). **NX seed**: only initial positions before physics runs.
- **Label focus**: *uniform* vs *degree* (show text labels on higher-degree nodes only).
- **Layout mode**: *Force* for exploration; *Tree* for a hierarchical read path (falls back if a `REPORTS_TO` cycle blocks levels).
- **Graph engine**: `streamlit-agraph` (default) vs **vis component** (local `streamlit.components.v1` bundle) for drag-end pin / magnetic MVP and **zoom-out hub labels** (same idea as the HTML explorer; not available on `agraph` alone).
- **Lock layout**: freezes NetworkX positions (requires **networkx**); not compatible with hierarchical tree mode.
- **HTML graph explorer**: CDN/offline full vis page when you need parity outside Streamlit.
                """.strip()
            )
        st.markdown("##### Lens & filters")
        st.caption(
            "One canvas: pick a lens, then **Fetch & render**. "
            "(No memorized IDs: pickers, search, optional manual fallback.)"
        )
        st.radio(
            "Active lens",
            ["Role", "Process", "Saved"],
            horizontal=False,
            key="explorer_lens",
            help="Role = neighbourhood around one role (or bulk all roles). Process = one process subtree (or bulk all project roots). Saved = restore presets.",
        )
        lens = str(st.session_state.get("explorer_lens") or "Role")

        areas_payload = st.session_state.get("areas_payload") or {}
        area_rows = list(areas_payload.get("roles") or [])
        area_names = [str(r.get("role_name") or "") for r in area_rows if r.get("role_name")]

        if lens == "Role":
            st.selectbox(
                "Filter by area (optional)",
                options=[""] + sorted(set(area_names)),
                format_func=lambda x: "All areas" if x == "" else x,
                key="area_filter",
                help="Narrows the role list to one HLK area row (from `/hlk/areas`).",
            )
            roles_opts = _filtered_roles(st.session_state.get("area_filter") or "")
            role_labels = [r.get("role_name") or "" for r in roles_opts if r.get("role_name")]
            st.session_state["_role_option_names"] = sorted(role_labels)
            st.checkbox(
                "All roles (bulk discovery)",
                key="graph_all_roles",
                help="Fetches each role’s neighbourhood sequentially and merges into one graph (see merge cap).",
            )
            st.selectbox(
                "Role",
                options=[""] + sorted(role_labels),
                format_func=lambda x: "Choose a role…" if x == "" else x,
                key="role_pick",
                help="Ignored when **All roles** is checked.",
            )
        elif lens == "Process":
            projects = st.session_state.get("projects_list") or []
            proj_ids = [""] + [p.get("item_id") or "" for p in projects if p.get("item_id")]
            proj_labels = {"": "Choose a project…"}
            for p in projects:
                iid = p.get("item_id") or ""
                if iid:
                    proj_labels[iid] = f"{p.get('item_name') or iid} — {iid}"
            st.checkbox(
                "All projects (bulk discovery)",
                key="graph_all_projects",
                help="Fetches each project root’s neighbourhood and merges (see merge cap).",
            )
            st.selectbox(
                "Project",
                options=proj_ids,
                format_func=lambda x: proj_labels.get(x, x),
                key="project_pick",
                help="Top-level project rows from `/hlk/processes` (granularity project).",
            )
            project_id = (st.session_state.get("project_pick") or "").strip()
            children: list[dict] = []
            if project_id:
                children = _project_children(project_id)
            child_ids = [""] + [c.get("item_id") or "" for c in children if c.get("item_id")]
            child_labels = {"": "Whole project (root neighbourhood)"}
            for c in children:
                cid = c.get("item_id") or ""
                if cid:
                    child_labels[cid] = f"{c.get('item_name') or cid} — {cid}"
            st.selectbox(
                "Child process (optional)",
                options=child_ids,
                format_func=lambda x: child_labels.get(x, x),
                key="child_pick",
                help="Optional deeper anchor; overrides project root for the neighbourhood API.",
            )
            st.text_input(
                "Search registry",
                placeholder="e.g. governance, KiRBe",
                key="search_q",
                help="Runs `/hlk/search`; pick a hit below to bind a process or role.",
            )
            if st.button("Run search", use_container_width=True, help="Executes `/hlk/search` with the query above."):
                q = (st.session_state.get("search_q") or "").strip()
                if q:
                    sr = _api_get("/hlk/search", params={"q": q})
                    if "_http_error" in sr:
                        st.error(sr)
                    else:
                        st.session_state["last_search"] = sr
                        st.session_state["search_hit_pick"] = ""
            sr = st.session_state.get("last_search") or {}
            if sr.get("status") == "ok":
                procs = sr.get("processes") or []
                roles_h = sr.get("roles") or []
                opts: list[tuple[str, str]] = [("", "— pick a search hit —")]
                for p in procs[:25]:
                    iid = p.get("item_id") or ""
                    if iid:
                        opts.append((f"p:{iid}", f"Process: {p.get('item_name') or iid} ({iid})"))
                for r in roles_h[:15]:
                    rn = r.get("role_name") or ""
                    if rn:
                        opts.append((f"r:{rn}", f"Role: {rn}"))
                if len(opts) > 1:
                    st.selectbox(
                        "Search hit",
                        options=[o[0] for o in opts],
                        format_func=lambda x: next(o[1] for o in opts if o[0] == x),
                        key="search_hit_pick",
                        on_change=_sync_search_to_role,
                        help="Process hits apply here; role hits sync to the Role lens when you switch back.",
                    )
            with st.expander("Manual item_id (fallback)", expanded=False):
                st.caption(
                    "Paste a process `item_id` when you already have it from another tool. "
                    "You do not need to memorize IDs for normal use — pickers and search stay primary."
                )
                st.text_input("Process item_id", key="manual_pid", placeholder="hol_resea_dtp_99", help="Direct `item_id` for `/hlk/graph/process/{id}/neighbourhood`.")
        else:
            saved = list(st.session_state.get("saved_lenses") or [])
            if not saved:
                st.info("No saved lenses yet. Fetch a graph, then save a preset from the canvas panel.")
            else:
                names = [s.get("name") or "untitled" for s in saved]
                pick = st.selectbox("Saved lens", options=list(range(len(saved))), format_func=lambda i: names[i])
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("Apply", use_container_width=True, help="Restore widget state from the preset."):
                        _apply_preset(saved[int(pick)])
                with c2:
                    if st.button(
                        "Apply & fetch",
                        use_container_width=True,
                        help="Restore preset, then run the same neighbourhood request(s).",
                    ):
                        pr = saved[int(pick)]
                        _apply_preset(pr)
                        fl = str(pr.get("fetch_lens") or "")
                        if fl in ("role", "bulk_roles") or pr.get("graph_all_roles"):
                            st.session_state["explorer_lens"] = "Role"
                        elif fl in ("process", "bulk_projects") or pr.get("graph_all_projects"):
                            st.session_state["explorer_lens"] = "Process"
                        elif (pr.get("role_pick") or "").strip():
                            st.session_state["explorer_lens"] = "Role"
                        elif _resolve_process_target().strip():
                            st.session_state["explorer_lens"] = "Process"
                        _fetch_and_push_canvas(
                            depth=int(st.session_state.get("graph_depth") or 2),
                            limit=int(st.session_state.get("graph_limit") or 80),
                        )
                with c3:
                    if st.button("Delete", use_container_width=True):
                        saved.pop(int(pick))
                        st.session_state["saved_lenses"] = saved
                        st.rerun()

        st.divider()
        st.markdown("##### Graph rendering")
        st.slider(
            "Graph depth (hops)",
            1,
            5,
            key="graph_depth",
            help="Traversal depth for neighbourhood queries (server also caps).",
        )
        st.slider(
            "Node limit (per API call)",
            20,
            200,
            step=10,
            key="graph_limit",
            help="Per-call node cap passed to the API; bulk merges may stop growing when merge cap is reached.",
        )
        st.slider(
            "Merge cap (nodes)",
            100,
            2000,
            step=50,
            key="graph_merge_cap",
            help="Maximum distinct nodes kept when merging bulk role/project fetches.",
        )
        st.slider(
            "Bulk max roles",
            5,
            120,
            step=5,
            key="graph_bulk_max_roles",
            help="Upper bound on how many roles to fetch in **All roles** mode.",
        )
        st.slider(
            "Bulk max projects",
            3,
            80,
            step=1,
            key="graph_bulk_max_projects",
            help="Upper bound on how many project roots to fetch in **All projects** mode.",
        )
        st.selectbox(
            "Node labels",
            options=["hide", "short", "full"],
            format_func=lambda m: {"hide": "Hidden (hover)", "short": "Abbreviated", "full": "Full (dense)"}[m],
            key="graph_label_mode",
            help="How much text is drawn on nodes (hover always shows JSON properties).",
        )
        st.selectbox(
            "Label focus",
            options=["uniform", "degree"],
            format_func=lambda m: {"uniform": "All nodes (same label mode)", "degree": "Labels on hubs only"}[m],
            key="graph_label_focus",
            help="Degree mode shows text only when degree ≥ threshold; others show a dot (tooltip still full).",
        )
        st.slider(
            "Label degree threshold",
            0,
            12,
            key="graph_label_min_degree",
            help="Used when **Label focus** = degree.",
        )
        st.selectbox(
            "Edge labels",
            options=["auto", "always", "hover_only"],
            format_func=lambda m: {
                "auto": "Auto (labels when graph is small)",
                "always": "Always show",
                "hover_only": "Hover only (canvas stays clean)",
            }[m],
            key="graph_edge_labels",
            help="Abbreviated relationship text on edges; full sentence stays in edge tooltip.",
        )
        st.selectbox(
            "Node size basis",
            options=["children", "degree", "balanced"],
            format_func=lambda m: {
                "children": "Children / ownership (default)",
                "degree": "Total degree",
                "balanced": "Weighted blend",
            }[m],
            key="graph_node_size_basis",
            help="Processes: outgoing PARENT_OF count. Roles: OWNED_BY fan-in. Documents/areas: neutral.",
        )
        st.radio(
            "Layout mode",
            ["force", "tree"],
            format_func=lambda m: "Force (explore)" if m == "force" else "Tree (hierarchical)",
            key="graph_layout_mode",
            horizontal=True,
            help="Tree = vis hierarchical layout + BFS levels from API root when possible.",
        )
        st.selectbox(
            "Tree direction",
            options=["UD", "LR"],
            format_func=lambda d: "Top-down (UD)" if d == "UD" else "Left-right (LR)",
            key="graph_tree_direction",
            help="Used when **Layout mode** = Tree.",
        )
        st.radio(
            "Graph engine",
            ["agraph", "vis_component"],
            format_func=lambda e: "streamlit-agraph" if e == "agraph" else "vis component (drag/pin)",
            key="graph_engine",
            horizontal=True,
            help="vis_component loads `static/streamlit_components/hlk_vis_network/` (vis-network CDN + Streamlit bridge). "
            "Includes **zoom-based landmark labels** (hub names when zoomed out). `streamlit-agraph` cannot hook vis zoom; use **HTML** explorer for the same behaviour.",
        )
        st.checkbox(
            "Lock layout (NetworkX freeze)",
            key="graph_lock_layout",
            help="Static positions + physics off (force mode only). Ignored without networkx.",
        )
        st.number_input(
            "Initial layout seed",
            min_value=1,
            max_value=999_999,
            key="graph_layout_seed",
            help="Random seed for NetworkX spring positions used as initial hints (or fixed layout when physics is off). Same graph + same seed ⇒ same starting arrangement.",
        )
        st.checkbox(
            "Force-directed physics (vis)",
            key="graph_use_physics",
            help="Primary interaction mode. When off, NetworkX lays out a static graph.",
        )
        st.checkbox(
            "NetworkX initial seed",
            key="graph_use_nx_seed",
            help="When physics is on, optionally place nodes from a spring layout first so the simulation starts less tangled.",
        )
        st.slider("Canvas width (px)", 800, 1400, key="graph_canvas_width", help="vis-network canvas width.")
        st.slider("Canvas height (px)", 480, 920, key="graph_canvas_height", help="vis-network canvas height.")
        if nx is None:
            st.warning("Install **networkx** for initial seed / static layout (`pip install networkx`).")

        st.divider()
        if st.button("Fetch & render to canvas", type="primary", use_container_width=True, help="Calls `/hlk/graph/.../neighbourhood` per your lens and bulk flags."):
            depth = int(st.session_state.get("graph_depth") or 2)
            limit = int(st.session_state.get("graph_limit") or 80)
            _fetch_and_push_canvas(depth=depth, limit=limit)
        if st.button("Refresh snapshot", use_container_width=True, help="Clears cached `/hlk/graph/summary` so the next run refetches."):
            st.session_state.pop("summary", None)
        if st.button("Reload registry pickers", use_container_width=True, help="Refetches `/hlk/areas`, `/hlk/roles`, `/hlk/processes`."):
            for k in ("areas_payload", "roles_list", "projects_list", "_registry_error"):
                st.session_state.pop(k, None)

    if "summary" not in st.session_state:
        st.session_state["summary"] = _api_get("/hlk/graph/summary")

    st.markdown('<div class="hx-panel">', unsafe_allow_html=True)
    st.markdown('<div class="hx-panel-title">Registry snapshot</div>', unsafe_allow_html=True)
    _render_summary_metrics(st.session_state["summary"])
    st.markdown("</div>", unsafe_allow_html=True)

    if "roles_list" not in st.session_state:
        _load_registry()

    if st.session_state.get("_registry_error"):
        st.warning("Registry load had errors (check API URL / token).")
        st.json(st.session_state["_registry_error"])

    st.divider()
    st.subheader("Canvas")

    hist = list(st.session_state.get("_graph_history") or [])
    if hist:
        st.selectbox(
            "Recent graphs (switch without re-fetching)",
            options=list(range(len(hist))),
            format_func=lambda i: hist[i]["title"],
            key="_history_choice_idx",
            on_change=_on_history_pick,
            help="Swaps the payload rendered below without a new API call.",
        )

    cg = st.session_state.get("current_graph")
    if isinstance(cg, dict) and cg.get("payload") is not None:
        st.markdown(f"**{cg.get('title', 'Graph')}**")
        if cg.get("subtitle"):
            st.caption(cg["subtitle"])
        r1, r2 = st.columns(2)
        with r1:
            if st.button("Re-fetch current", use_container_width=True, help="Same canvas target, current depth/limit/sidebar flags."):
                _refetch_current_canvas()
        with r2:
            st.text_input(
                "Highlight substring",
                key="graph_focus_substring",
                placeholder="element id or name fragment",
                help="Case-insensitive match on node id or display name; highlights matching nodes.",
            )
        _render_graph_canvas(cg["payload"])
        save_name = st.text_input("Save this lens as…", placeholder="e.g. PMO delivery hub", key="save_lens_name")
        b1, b2, b3 = st.columns([1, 1, 2])
        with b1:
            if st.button("Save lens", use_container_width=True, help="Stores sidebar + rendering state and fetch identity from the current graph.") and save_name.strip():
                preset = _collect_preset(save_name.strip())
                saved = list(st.session_state.get("saved_lenses") or [])
                saved = [s for s in saved if (s.get("name") or "") != preset["name"]]
                saved.append(preset)
                st.session_state["saved_lenses"] = saved
                st.success(f"Saved “{preset['name']}”. Open **Saved** in the sidebar to reapply.")
        with b2:
            data_json = json.dumps(st.session_state.get("saved_lenses") or [], indent=2)
            st.download_button(
                "Export lenses JSON",
                data=data_json,
                file_name="hlk_graph_saved_lenses.json",
                mime="application/json",
                use_container_width=True,
            )
        with b3:
            pasted = st.text_area("Import lenses (JSON array)", height=70, key="import_lenses_json")
            if st.button("Merge import", use_container_width=True) and pasted.strip():
                try:
                    arr = json.loads(pasted)
                    if not isinstance(arr, list):
                        raise ValueError("root must be a list")
                    cur = list(st.session_state.get("saved_lenses") or [])
                    for item in arr:
                        if isinstance(item, dict) and item.get("name"):
                            cur = [s for s in cur if (s.get("name") or "") != item.get("name")]
                            cur.append(item)
                    st.session_state["saved_lenses"] = cur
                    st.success("Merged imported lenses.")
                except Exception as exc:
                    st.error(f"Invalid JSON: {exc}")
    else:
        st.info(
            "No graph on canvas yet. In the sidebar, choose **Role** or **Process**, tune depth and labels, "
            "then click **Fetch & render to canvas**."
        )


def _inside_streamlit_app() -> bool:
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        return get_script_run_ctx() is not None
    except Exception:
        return False


_STREAMLIT_CHILD_ENV = "_AKOS_HLK_GRAPH_EXPLORER_STREAMLIT"


if __name__ == "__main__":
    if os.environ.get(_STREAMLIT_CHILD_ENV) == "1" or _inside_streamlit_app():
        main()
    else:
        script_path = str(Path(__file__).resolve())
        cmd = [sys.executable, "-m", "streamlit", "run", script_path, *sys.argv[1:]]
        env = {**os.environ, _STREAMLIT_CHILD_ENV: "1"}
        print("Launching Streamlit (use Ctrl+C to stop):", " ".join(cmd), file=sys.stderr)
        raise SystemExit(subprocess.call(cmd, env=env))
