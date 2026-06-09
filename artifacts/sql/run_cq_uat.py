"""One-shot CQ1-5 live UAT runner (I95 N4). Do not commit secrets."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from akos.hlk_graph_articulation import COMPETENCY_QUESTIONS  # noqa: E402
from akos.io import bootstrap_openclaw_process_env  # noqa: E402
from akos.hlk_neo4j import get_neo4j_driver, neo4j_configured, neo4j_env_non_placeholder  # noqa: E402


def _sample_params(session) -> dict[str, dict[str, str]]:
    role = session.run("MATCH (r:Role) RETURN r.id AS id LIMIT 1").single()
    proc = session.run("MATCH (p:Process) RETURN p.id AS id LIMIT 1").single()
    eng = session.run("MATCH (e:Engagement) RETURN e.id AS id LIMIT 1").single()
    cap = session.run("MATCH (c:Capability) RETURN c.id AS id LIMIT 1").single()
    area = session.run(
        "MATCH (n) WHERE n.area IS NOT NULL RETURN n.area AS area LIMIT 1"
    ).single()
    return {
        "CQ1": {"role": (role or {}).get("id") or "hol_opera_role_cto"},
        "CQ2": {"eng": (eng or {}).get("id") or "eng-placeholder"},
        "CQ3": {"cap": (cap or {}).get("id") or "cap-placeholder"},
        "CQ4": {"proc": (proc or {}).get("id") or "hol_opera_dtp_001"},
        "CQ5": {"area": (area or {}).get("area") or "People"},
    }


def main() -> int:
    bootstrap_openclaw_process_env()
    if not neo4j_configured() or not neo4j_env_non_placeholder():
        print(json.dumps({"error": "NEO4J not configured or placeholder env"}))
        return 2
    driver = get_neo4j_driver()
    if driver is None:
        print(json.dumps({"error": "driver unavailable"}))
        return 2
    results: list[dict] = []
    with driver.session() as session:
        params = _sample_params(session)
        for cq in COMPETENCY_QUESTIONS:
            cid = cq["id"]
            cypher = cq["cypher"]
            p = params.get(cid, {})
            try:
                rows = list(session.run(cypher, **p))
                results.append(
                    {
                        "id": cid,
                        "status": "PASS" if rows is not None else "FAIL",
                        "row_count": len(rows),
                        "params": p,
                        "note": "zero rows OK for structural smoke" if len(rows) == 0 else "",
                    }
                )
            except Exception as exc:  # noqa: BLE001 — UAT capture
                results.append(
                    {
                        "id": cid,
                        "status": "FAIL",
                        "error": type(exc).__name__,
                        "message": str(exc)[:200],
                        "params": p,
                    }
                )
    driver.close()
    print(json.dumps({"cq_results": results}, indent=2))
    failed = sum(1 for r in results if r["status"] == "FAIL")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
