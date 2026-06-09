#!/usr/bin/env python3
"""Neo4j Aura connectivity probe — same env bootstrap as sync_hlk_neo4j.

Loads ``~/.openclaw/.env`` via ``bootstrap_openclaw_process_env``, runs
``RETURN 1``, and prints leak-safe diagnostics (var names, URI scheme/host,
username classification). Never logs secret values.

Exit codes:
    0 — Bolt auth OK (``RETURN 1`` succeeded)
    1 — auth failure (wrong password / user)
    2 — not configured or placeholder env
    3 — TLS / connectivity failure (non-auth)

Usage:
    py scripts/neo4j_connectivity_probe.py
"""

from __future__ import annotations

import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_neo4j import (  # noqa: E402
    _aura_instance_id_from_uri,
    _resolve_neo4j_username,
    get_neo4j_driver,
    neo4j_configured,
    neo4j_env_non_placeholder,
)
from akos.io import bootstrap_openclaw_process_env, load_runtime_env, resolve_openclaw_home  # noqa: E402


def _mask_uri(uri: str) -> dict[str, str]:
    if not uri.strip():
        return {"scheme": "(absent)", "host": "(absent)"}
    parsed = urlparse(uri.strip())
    scheme = parsed.scheme or "(no-scheme)"
    host = parsed.hostname or parsed.netloc.split("@")[-1] or "(unknown)"
    return {"scheme": scheme, "host": host}


def _env_trace() -> dict[str, object]:
    oc_home = resolve_openclaw_home()
    env_path = oc_home / ".env"
    repo_env = REPO_ROOT / ".env"
    file_vals = load_runtime_env(oc_home)

    neo4j_keys = ("NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD", "NEO4J_TRUST")
    pre = {k: bool(os.environ.get(k, "").strip()) for k in neo4j_keys}
    stale_process_would_win = [
        k
        for k in neo4j_keys
        if os.environ.get(k, "").strip()
        and (file_vals.get(k) or "").strip()
        and os.environ.get(k, "").strip() != (file_vals.get(k) or "").strip()
    ]
    bootstrap_openclaw_process_env(oc_home)
    post_uri = os.environ.get("NEO4J_URI", "").strip()
    post_user = os.environ.get("NEO4J_USERNAME", "").strip()
    post_pwd = os.environ.get("NEO4J_PASSWORD", "").strip()
    post_trust = os.environ.get("NEO4J_TRUST", "").strip()

    instance_id = _aura_instance_id_from_uri(post_uri)
    configured_user = post_user or "neo4j"
    resolved_user = _resolve_neo4j_username(post_uri, configured_user)

    return {
        "openclaw_home": str(oc_home),
        "env_file": str(env_path),
        "env_file_exists": env_path.exists(),
        "repo_env_exists": repo_env.exists(),
        "file_vars": {
            k: "present" if file_vals.get(k, "").strip() else "absent"
            for k in ("NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD", "NEO4J_TRUST")
        },
        "process_pre_bootstrap": pre,
        "process_post_bootstrap": {
            "NEO4J_URI": "present" if post_uri else "absent",
            "NEO4J_USERNAME": "present" if post_user else "absent (defaults to neo4j)",
            "NEO4J_PASSWORD": f"present (len={len(post_pwd)})" if post_pwd else "absent",
            "NEO4J_TRUST": post_trust or "(unset → system)",
        },
        "uri": _mask_uri(post_uri),
        "aura_instance_id": instance_id or "(not detected)",
        "configured_username": configured_user,
        "resolved_username": resolved_user,
        "username_misconfig_instance_id": bool(
            instance_id and configured_user == instance_id and resolved_user == "neo4j"
        ),
        "stale_process_env_overridden_keys": stale_process_would_win,
    }


def _try_bolt(user: str) -> dict[str, str]:
    os.environ["NEO4J_USERNAME"] = user
    driver = get_neo4j_driver()
    if driver is None:
        return {"user": user, "status": "SKIP", "detail": "driver unavailable"}
    try:
        with driver.session() as session:
            row = session.run("RETURN 1 AS n").single()
        return {"user": user, "status": "PASS", "detail": f"RETURN 1 → {row['n']}"}
    except Exception as exc:  # noqa: BLE001 — diagnostic capture
        name = type(exc).__name__
        msg = str(exc)[:120]
        if "AuthError" in name or "Unauthorized" in msg or "Invalid credential" in msg:
            kind = "auth"
        elif "ServiceUnavailable" in name or "SSL" in msg or "Certificate" in msg:
            kind = "tls_or_routing"
        else:
            kind = "other"
        return {"user": user, "status": "FAIL", "kind": kind, "detail": f"{name}: {msg}"}
    finally:
        driver.close()


def _try_aura_http(user: str, password: str, uri: str) -> dict[str, str]:
    """Direct Aura Query API — isolates password rejection from Bolt driver stack."""
    instance = _aura_instance_id_from_uri(uri)
    if not instance:
        return {"status": "SKIP", "detail": "not an Aura *.databases.neo4j.io URI"}
    url = f"https://{instance}.databases.neo4j.io/db/neo4j/query/v2"
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    body = json.dumps({"statement": "RETURN 1 AS n"}).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return {"status": "PASS" if resp.status == 200 else "FAIL", "detail": f"HTTP {resp.status}"}
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            return {"status": "FAIL", "kind": "auth", "detail": "HTTP 401 Unauthorized (Aura rejects credential)"}
        return {"status": "FAIL", "kind": "http", "detail": f"HTTP {exc.code}"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "FAIL", "kind": "network", "detail": type(exc).__name__}


def _classify(auth_results: list[dict], http_result: dict) -> str:
    if any(r.get("status") == "PASS" for r in auth_results):
        return "PASS"
    kinds = {r.get("kind") for r in auth_results if r.get("status") == "FAIL"}
    if http_result.get("kind") == "auth" or kinds == {"auth"}:
        return "wrong_password_or_user"
    if "tls_or_routing" in kinds:
        return "tls_or_uri_mismatch"
    return "connectivity_failure"


def main() -> int:
    trace = _env_trace()
    print(json.dumps({"env_trace": trace}, indent=2))

    if not neo4j_configured() or not neo4j_env_non_placeholder():
        print(json.dumps({"verdict": "FAIL", "reason": "NEO4J not configured or placeholder env"}))
        return 2

    uri = os.environ["NEO4J_URI"].strip()
    pwd = os.environ["NEO4J_PASSWORD"].strip()
    configured = os.environ.get("NEO4J_USERNAME", "").strip() or "neo4j"
    resolved = _resolve_neo4j_username(uri, configured)

    users_to_try: list[str] = []
    for u in (resolved, configured, "neo4j"):
        if u and u not in users_to_try:
            users_to_try.append(u)

    bolt_results = [_try_bolt(u) for u in users_to_try]
    http_result = _try_aura_http(resolved, pwd, uri)
    classification = _classify(bolt_results, http_result)

    report = {
        "bolt_attempts": bolt_results,
        "aura_http_query_api": http_result,
        "classification": classification,
        "verdict": "PASS" if classification == "PASS" else "FAIL",
    }
    if trace.get("username_misconfig_instance_id"):
        report["hint"] = (
            "NEO4J_USERNAME matches Aura instance ID; use neo4j (or a custom DB user) "
            "in ~/.openclaw/.env"
        )
    if classification == "wrong_password_or_user":
        report["hint"] = (
            report.get("hint", "")
            + " Aura rejected credentials — reset password in Aura console, copy via modal "
            "Copy button, update ~/.openclaw/.env and GitHub secrets NEO4J_PASSWORD."
        ).strip()

    print(json.dumps(report, indent=2))
    return 0 if classification == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
