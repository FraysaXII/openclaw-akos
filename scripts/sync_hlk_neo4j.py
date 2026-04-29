#!/usr/bin/env python3
"""Sync HLK canonical CSV graph into Neo4j (mirrored projection).

Loads ``~/.openclaw/.env`` via ``bootstrap_openclaw_process_env`` (same as
``scripts/serve-api.py``), then MERGEs Role/Process nodes and edges.

Usage:
    py scripts/sync_hlk_neo4j.py [--dry-run] [--with-documents]

Requires: pip install neo4j
Env: NEO4J_URI, NEO4J_USERNAME (optional), NEO4J_PASSWORD, optional NEO4J_TRUST / NEO4J_CA_BUNDLE (see ``akos.hlk_neo4j.get_neo4j_driver`` and USER_GUIDE 9.10).
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk import get_hlk_registry
from akos.hlk_neo4j import get_neo4j_driver, sync_csv_graph
from akos.hlk_vault_links import all_vault_md_paths, iter_internal_md_edges
from akos.io import REPO_ROOT, bootstrap_openclaw_process_env
from akos.log import setup_logging

logger = logging.getLogger("akos.sync_hlk_neo4j")


def _ingest_vault_documents(driver: object) -> dict[str, int]:
    """Create Document nodes and LINKS_TO edges for internal v3.0 markdown links."""
    pairs = iter_internal_md_edges(REPO_ROOT)
    paths = all_vault_md_paths(REPO_ROOT)
    for a, b in pairs:
        paths.add(a)
        paths.add(b)
    doc_count = 0
    edge_count = 0

    with driver.session() as session:
        session.run(
            "CREATE CONSTRAINT hlk_doc_path IF NOT EXISTS FOR (d:Document) REQUIRE d.path IS UNIQUE"
        )
        for rel in sorted(paths):
            session.run(
                """
                MERGE (d:Document {path: $path})
                SET d.source = 'hlk_vault_v3'
                """,
                path=rel,
            )
            doc_count += 1
        batch = 300
        for i in range(0, len(pairs), batch):
            chunk = [{"a": a, "b": b} for a, b in pairs[i : i + batch]]
            if not chunk:
                continue
            session.run(
                """
                UNWIND $rows AS row
                MATCH (x:Document {path: row.a})
                MATCH (y:Document {path: row.b})
                MERGE (x)-[:LINKS_TO]->(y)
                """,
                rows=chunk,
            )
            edge_count += len(chunk)
    return {"documents_upserted": doc_count, "document_edges": edge_count}


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync HLK CSV graph to Neo4j")
    parser.add_argument("--dry-run", action="store_true", help="Validate parity only; do not connect")
    parser.add_argument(
        "--with-documents",
        action="store_true",
        help="Also MERGE v3.0 markdown Document nodes and LINKS_TO edges",
    )
    parser.add_argument("--json-log", action="store_true")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)
    bootstrap_openclaw_process_env()

    from akos.hlk_graph_model import assert_graph_registry_parity, build_hlk_csv_graph, build_program_graph

    reg = get_hlk_registry()
    nodes, edges = build_hlk_csv_graph(reg)
    assert_graph_registry_parity(reg, nodes, edges)
    # Initiative 23 P-graph (D-IH-18): project the program registry alongside
    # the role/process tree. CSV-driven; emits 0 nodes when the file is absent.
    prog_nodes, prog_edges = build_program_graph(reg)
    logger.info(
        "graph model: roles=%d processes=%d programs=%d edges=%d (incl. %d program-side)",
        sum(1 for n in nodes if n.label == "Role"),
        sum(1 for n in nodes if n.label == "Process"),
        len(prog_nodes),
        len(edges) + len(prog_edges),
        len(prog_edges),
    )

    if args.dry_run:
        logger.info("dry-run: skipping Neo4j write")
        return

    driver = get_neo4j_driver()
    if driver is None:
        logger.error("Neo4j not configured (NEO4J_URI + NEO4J_PASSWORD) or driver missing")
        sys.exit(2)
    try:
        stats = sync_csv_graph(driver, reg, wipe=True)
        logger.info("neo4j csv sync: %s", stats)
        if args.with_documents:
            dstats = _ingest_vault_documents(driver)
            logger.info("neo4j vault documents: %s", dstats)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
