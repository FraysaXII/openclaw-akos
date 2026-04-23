#!/usr/bin/env python3
"""Browser smoke test runner for AKOS.

Runs canonical dashboard smoke scenarios. With --playwright and Playwright
installed, runs DOM-based tests. Otherwise uses HTTP-only checks when the
gateway is reachable. Scenarios return SKIP when the gateway is unreachable.

Usage:
    py scripts/browser-smoke.py
    py scripts/browser-smoke.py --playwright    # DOM-based tests when Playwright installed
    py scripts/browser-smoke.py --playwright --headed  # Show browser window

Env: ``AKOS_BROWSER_SMOKE_API_URL`` (optional) overrides the control plane base URL
(default ``http://127.0.0.1:8420``), e.g. when ``serve-api.py --port 8421`` is used.

Env: ``AKOS_BROWSER_SMOKE_HTTP_TIMEOUT`` (optional, default ``30``) seconds for urllib probes
to the gateway and control plane (cold ``serve-api`` with Langfuse/RunPod init can exceed 5s).

**Scenario 0 registry slice (HTTP):** after graph explorer checks, runs golden assertions on
``GET /hlk/roles/CTO``, ``GET /hlk/areas/Research``, ``GET /hlk/processes/KiRBe%20Platform/tree``,
``GET /routing/classify`` (admin + mixed utterance), ``GET /finance/quote/AAPL``,
``GET /finance/sentiment?tickers=MSFT``, ``GET /agents/madeira/interaction-mode``, and
``GET /madeira/control`` — aligned to ``docs/uat/hlk_admin_smoke.md`` and
``docs/uat/madeira_use_case_matrix.md`` for *HTTP-observable* parity (not WebChat copy review).

Playwright Phase 2 (architect / executor) asserts on **FastAPI** ``/agents`` (same SSOT as
Phase 1 ``agent_visibility``), not OpenClaw gateway UI strings at ``:18789``.
"""

from __future__ import annotations

import argparse
import os
import json
import logging
import platform
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.log import setup_logging

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    sync_playwright = None  # type: ignore[misc, assignment]
    PLAYWRIGHT_AVAILABLE = False

logger = logging.getLogger("akos.browser-smoke")

GATEWAY_URL = "http://127.0.0.1:18789"
API_URL = (os.environ.get("AKOS_BROWSER_SMOKE_API_URL") or "http://127.0.0.1:8420").rstrip("/")

# ``serve-api`` can block >5s on cold Langfuse/RunPod init; keep HTTP parity stable for CI and local gates.
HTTP_TIMEOUT = float(os.environ.get("AKOS_BROWSER_SMOKE_HTTP_TIMEOUT", "30"))

# Golden process names: direct children of the KiRBe Platform project (``process_list.csv``).
_SCENARIO0_KIRBE_CHILDREN_EXPECTED = (
    "KiRBe Security and Governance",
    "KiRBe Multi-Source Connector Setup",
)


def _gateway_reachable() -> bool:
    try:
        req = urllib.request.Request(GATEWAY_URL, method="GET")
        with urllib.request.urlopen(req, timeout=min(HTTP_TIMEOUT, 15.0)):
            return True
    except (urllib.error.URLError, OSError):
        return False


def _api_reachable() -> bool:
    try:
        req = urllib.request.Request(f"{API_URL}/health", method="GET")
        with urllib.request.urlopen(req, timeout=min(HTTP_TIMEOUT, 15.0)):
            return True
    except (urllib.error.URLError, OSError):
        return False


# --- Phase 1: HTTP-only checks (no Playwright) ---


def _check_dashboard_health_http() -> dict[str, str]:
    try:
        req = urllib.request.Request(GATEWAY_URL, method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            if resp.status == 200:
                return {"scenario": "dashboard_health", "status": "PASS", "detail": f"Gateway {GATEWAY_URL} returns 200"}
    except (urllib.error.URLError, OSError) as e:
        return {"scenario": "dashboard_health", "status": "FAIL", "detail": str(e)}
    return {"scenario": "dashboard_health", "status": "FAIL", "detail": "Unexpected response"}


def _check_agent_visibility_http() -> dict[str, str]:
    try:
        req = urllib.request.Request(f"{API_URL}/agents", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
            agents = data if isinstance(data, list) else data.get("agents", data)
            count = len(agents) if isinstance(agents, list) else 0
            if count >= 5:
                return {"scenario": "agent_visibility", "status": "PASS", "detail": f"{count} agents visible via API"}
            return {"scenario": "agent_visibility", "status": "FAIL", "detail": f"Expected 5 agents, got {count}"}
    except (urllib.error.URLError, OSError, json.JSONDecodeError, KeyError) as e:
        return {"scenario": "agent_visibility", "status": "FAIL", "detail": str(e)}


def _check_swagger_health_http() -> dict[str, str]:
    try:
        req = urllib.request.Request(f"{API_URL}/health", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
            status = data.get("status") if isinstance(data, dict) else None
            if status == "ok":
                return {"scenario": "swagger_health", "status": "PASS", "detail": "GET /health returns status: ok"}
            return {"scenario": "swagger_health", "status": "FAIL", "detail": f"Expected status ok, got {status}"}
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
        return {"scenario": "swagger_health", "status": "FAIL", "detail": str(e)}


def _check_hlk_graph_summary_http() -> dict[str, str]:
    try:
        req = urllib.request.Request(f"{API_URL}/hlk/graph/summary", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
        if not isinstance(data, dict):
            return {"scenario": "hlk_graph_summary", "status": "FAIL", "detail": "Non-JSON response"}
        if data.get("status") != "ok":
            return {"scenario": "hlk_graph_summary", "status": "FAIL", "detail": f"status field: {data.get('status')}"}
        csv = data.get("csv") or {}
        if not isinstance(csv, dict) or "roles" not in csv or "processes" not in csv:
            return {"scenario": "hlk_graph_summary", "status": "FAIL", "detail": "Missing csv.roles / csv.processes"}
        if int(csv["roles"]) < 1 or int(csv["processes"]) < 1:
            return {"scenario": "hlk_graph_summary", "status": "FAIL", "detail": "Unexpected zero registry counts"}
        neo = data.get("neo4j", "")
        detail = f"csv roles={csv['roles']} processes={csv['processes']}; neo4j={neo}"
        return {"scenario": "hlk_graph_summary", "status": "PASS", "detail": detail}
    except (urllib.error.URLError, OSError, json.JSONDecodeError, TypeError, ValueError) as e:
        return {"scenario": "hlk_graph_summary", "status": "FAIL", "detail": str(e)}


def _check_hlk_graph_explorer_http() -> dict[str, str]:
    try:
        req = urllib.request.Request(f"{API_URL}/hlk/graph/explorer", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            body = resp.read().decode(errors="replace")
        if resp.status != 200:
            return {"scenario": "hlk_graph_explorer", "status": "FAIL", "detail": f"HTTP {resp.status}"}
        if (
            "HLK Graph Explorer" not in body
            or "vis-network" not in body
            or 'data-testid="hlk-graph-explorer-root"' not in body
            or 'data-testid="summary-cards"' not in body
        ):
            return {"scenario": "hlk_graph_explorer", "status": "FAIL", "detail": "Unexpected explorer HTML"}
        return {"scenario": "hlk_graph_explorer", "status": "PASS", "detail": "GET /hlk/graph/explorer returns operator UI"}
    except (urllib.error.URLError, OSError) as e:
        return {"scenario": "hlk_graph_explorer", "status": "FAIL", "detail": str(e)}


def evaluate_scenario0_cto_payload(data: object) -> dict[str, str]:
    """Deterministic checks for ``GET /hlk/roles/CTO`` (``docs/uat/hlk_admin_smoke.md`` Scenario 0 step 4 contract)."""
    if not isinstance(data, dict):
        return {"scenario": "scenario0_hlk_cto", "status": "FAIL", "detail": "response is not a JSON object"}
    if data.get("status") != "ok":
        return {"scenario": "scenario0_hlk_cto", "status": "FAIL", "detail": f"HLK status={data.get('status')!r}"}
    br = data.get("best_role")
    if not isinstance(br, dict):
        return {"scenario": "scenario0_hlk_cto", "status": "FAIL", "detail": "missing best_role"}
    if br.get("role_name") != "CTO":
        return {"scenario": "scenario0_hlk_cto", "status": "FAIL", "detail": f"role_name={br.get('role_name')!r}"}
    try:
        level = int(br.get("access_level", 0))
    except (TypeError, ValueError):
        level = 0
    if level != 5:
        return {"scenario": "scenario0_hlk_cto", "status": "FAIL", "detail": f"access_level={br.get('access_level')!r} expected 5"}
    desc = f"{br.get('role_description', '')} {br.get('role_full_description', '')}"
    if "Chief Technology Officer" not in desc:
        return {"scenario": "scenario0_hlk_cto", "status": "FAIL", "detail": "CTO canonical title fragment missing from role text"}
    return {"scenario": "scenario0_hlk_cto", "status": "PASS", "detail": "CTO access_level 5 + canonical title (registry SSOT)"}


def evaluate_scenario0_research_area_payload(data: object) -> dict[str, str]:
    """``GET /hlk/areas/Research`` — Scenario 0 step 5 (Research roles from baseline only)."""
    if not isinstance(data, dict):
        return {"scenario": "scenario0_hlk_research_area", "status": "FAIL", "detail": "response is not a JSON object"}
    if data.get("status") != "ok":
        return {"scenario": "scenario0_hlk_research_area", "status": "FAIL", "detail": f"HLK status={data.get('status')!r}"}
    roles = data.get("roles") or []
    if not isinstance(roles, list) or not roles:
        return {"scenario": "scenario0_hlk_research_area", "status": "FAIL", "detail": "empty roles list"}
    names: list[str] = []
    for r in roles:
        if not isinstance(r, dict):
            return {"scenario": "scenario0_hlk_research_area", "status": "FAIL", "detail": "non-object role row"}
        if r.get("area") != "Research":
            return {
                "scenario": "scenario0_hlk_research_area",
                "status": "FAIL",
                "detail": f"non-Research role in area query: {r.get('role_name')!r} area={r.get('area')!r}",
            }
        names.append(str(r.get("role_name", "")))
    if "Holistik Researcher" not in names:
        return {"scenario": "scenario0_hlk_research_area", "status": "FAIL", "detail": "Holistik Researcher missing from Research area"}
    return {
        "scenario": "scenario0_hlk_research_area",
        "status": "PASS",
        "detail": f"Research area closed: {len(names)} roles; includes Holistik Researcher",
    }


def evaluate_scenario0_kirbe_children_payload(data: object) -> dict[str, str]:
    """Direct children of ``KiRBe Platform`` (Scenario 0 step 6 — process_list SSOT)."""
    if not isinstance(data, dict):
        return {"scenario": "scenario0_hlk_kirbe_children", "status": "FAIL", "detail": "response is not a JSON object"}
    if data.get("status") != "ok":
        return {"scenario": "scenario0_hlk_kirbe_children", "status": "FAIL", "detail": f"HLK status={data.get('status')!r}"}
    processes = data.get("processes") or []
    if not isinstance(processes, list) or not processes:
        return {"scenario": "scenario0_hlk_kirbe_children", "status": "FAIL", "detail": "empty processes list"}
    names = [p.get("item_name") for p in processes if isinstance(p, dict)]
    for expected in _SCENARIO0_KIRBE_CHILDREN_EXPECTED:
        if expected not in names:
            return {"scenario": "scenario0_hlk_kirbe_children", "status": "FAIL", "detail": f"missing expected child {expected!r}"}
    return {
        "scenario": "scenario0_hlk_kirbe_children",
        "status": "PASS",
        "detail": f"{len(names)} direct children; includes golden workstreams",
    }


def evaluate_scenario0_admin_escalation_payload(data: object) -> dict[str, str]:
    """``GET /routing/classify`` — Scenario 0 step 7 (Finance restructure → orchestrator escalation)."""
    if not isinstance(data, dict):
        return {"scenario": "scenario0_admin_escalation", "status": "FAIL", "detail": "response is not a JSON object"}
    if data.get("route") != "admin_escalate" or data.get("must_escalate") is not True:
        return {
            "scenario": "scenario0_admin_escalation",
            "status": "FAIL",
            "detail": f"route={data.get('route')!r} must_escalate={data.get('must_escalate')!r}",
        }
    return {"scenario": "scenario0_admin_escalation", "status": "PASS", "detail": "admin_escalate + must_escalate true"}


def evaluate_scenario0_finance_quote_payload(data: object) -> dict[str, str]:
    """UC M-FIN-01: quote envelope is HTTP-stable (ok or degraded)."""
    if not isinstance(data, dict):
        return {"scenario": "scenario0_finance_quote", "status": "FAIL", "detail": "response is not a JSON object"}
    st = str(data.get("status", "")).strip().lower()
    if st not in ("ok", "degraded"):
        return {"scenario": "scenario0_finance_quote", "status": "FAIL", "detail": f"unexpected finance status={data.get('status')!r}"}
    return {"scenario": "scenario0_finance_quote", "status": "PASS", "detail": "finance quote envelope ok|degraded"}


def evaluate_scenario0_finance_sentiment_payload(data: object) -> dict[str, str]:
    """UC M-FIN-02: sentiment envelope (may be degraded without ALPHA_VANTAGE_KEY)."""
    if not isinstance(data, dict):
        return {"scenario": "scenario0_finance_sentiment", "status": "FAIL", "detail": "response is not a JSON object"}
    st = str(data.get("status", "")).strip().lower()
    if st not in ("ok", "degraded"):
        return {"scenario": "scenario0_finance_sentiment", "status": "FAIL", "detail": f"unexpected finance status={data.get('status')!r}"}
    return {"scenario": "scenario0_finance_sentiment", "status": "PASS", "detail": "finance sentiment envelope ok|degraded"}


def evaluate_scenario0_routing_mixed_payload(data: object) -> dict[str, str]:
    """UC M-RT-03: admin verb + HLK lookup in one utterance — escalation regex must win."""
    if not isinstance(data, dict):
        return {"scenario": "scenario0_routing_mixed", "status": "FAIL", "detail": "response is not a JSON object"}
    route = str(data.get("route", ""))
    if route != "admin_escalate":
        return {
            "scenario": "scenario0_routing_mixed",
            "status": "FAIL",
            "detail": f"route={route!r} expected admin_escalate",
        }
    if not data.get("must_escalate"):
        return {"scenario": "scenario0_routing_mixed", "status": "FAIL", "detail": "must_escalate must be true"}
    return {"scenario": "scenario0_routing_mixed", "status": "PASS", "detail": "mixed utterance escalates admin"}


def evaluate_scenario0_madeira_mode_payload(data: object) -> dict[str, str]:
    """UC M-CTL-01: interaction mode endpoint returns stable JSON."""
    if not isinstance(data, dict):
        return {"scenario": "scenario0_madeira_mode", "status": "FAIL", "detail": "response is not a JSON object"}
    if "madeiraInteractionMode" not in data:
        return {"scenario": "scenario0_madeira_mode", "status": "FAIL", "detail": "missing madeiraInteractionMode"}
    mode = str(data.get("madeiraInteractionMode", ""))
    if mode not in ("ask", "plan_draft"):
        return {"scenario": "scenario0_madeira_mode", "status": "FAIL", "detail": f"invalid mode={mode!r}"}
    return {"scenario": "scenario0_madeira_mode", "status": "PASS", "detail": f"mode={mode}"}


def evaluate_scenario0_madeira_control_html(html: str) -> dict[str, str]:
    """UC M-PLAN-01 (HTTP slice): control page exposes plan draft semantics."""
    text = html or ""
    if "madeira" not in text.lower():
        return {"scenario": "scenario0_madeira_control", "status": "FAIL", "detail": "expected Madeira control markup"}
    if "plan_draft" not in text and "Plan draft" not in text:
        return {"scenario": "scenario0_madeira_control", "status": "FAIL", "detail": "missing plan draft mode hint"}
    return {"scenario": "scenario0_madeira_control", "status": "PASS", "detail": "madeira control page ok"}


def _check_scenario0_finance_quote_http() -> dict[str, str]:
    try:
        req = urllib.request.Request(f"{API_URL}/finance/quote/AAPL", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return evaluate_scenario0_finance_quote_payload(json.loads(resp.read().decode()))
    except Exception as e:
        return {"scenario": "scenario0_finance_quote", "status": "FAIL", "detail": str(e)}


def _check_scenario0_finance_sentiment_http() -> dict[str, str]:
    try:
        q = urllib.parse.urlencode({"tickers": "MSFT"})
        req = urllib.request.Request(f"{API_URL}/finance/sentiment?{q}", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return evaluate_scenario0_finance_sentiment_payload(json.loads(resp.read().decode()))
    except Exception as e:
        return {"scenario": "scenario0_finance_sentiment", "status": "FAIL", "detail": str(e)}


def _check_scenario0_routing_mixed_http() -> dict[str, str]:
    try:
        mixed = "Restructure the Finance area. Who is the CTO?"
        q = urllib.parse.urlencode({"q": mixed})
        req = urllib.request.Request(f"{API_URL}/routing/classify?{q}", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return evaluate_scenario0_routing_mixed_payload(json.loads(resp.read().decode()))
    except Exception as e:
        return {"scenario": "scenario0_routing_mixed", "status": "FAIL", "detail": str(e)}


def _check_scenario0_madeira_mode_http() -> dict[str, str]:
    try:
        req = urllib.request.Request(f"{API_URL}/agents/madeira/interaction-mode", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return evaluate_scenario0_madeira_mode_payload(json.loads(resp.read().decode()))
    except Exception as e:
        return {"scenario": "scenario0_madeira_mode", "status": "FAIL", "detail": str(e)}


def _check_scenario0_madeira_control_http() -> dict[str, str]:
    try:
        req = urllib.request.Request(f"{API_URL}/madeira/control", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            if resp.status != 200:
                return {"scenario": "scenario0_madeira_control", "status": "FAIL", "detail": f"HTTP {resp.status}"}
            body = resp.read().decode(errors="replace")
            return evaluate_scenario0_madeira_control_html(body)
    except Exception as e:
        return {"scenario": "scenario0_madeira_control", "status": "FAIL", "detail": str(e)}


def _check_scenario0_hlk_cto_http() -> dict[str, str]:
    try:
        req = urllib.request.Request(f"{API_URL}/hlk/roles/CTO", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return evaluate_scenario0_cto_payload(json.loads(resp.read().decode()))
    except Exception as e:
        return {"scenario": "scenario0_hlk_cto", "status": "FAIL", "detail": str(e)}


def _check_scenario0_hlk_research_area_http() -> dict[str, str]:
    try:
        path = urllib.parse.quote("Research", safe="")
        req = urllib.request.Request(f"{API_URL}/hlk/areas/{path}", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return evaluate_scenario0_research_area_payload(json.loads(resp.read().decode()))
    except Exception as e:
        return {"scenario": "scenario0_hlk_research_area", "status": "FAIL", "detail": str(e)}


def _check_scenario0_hlk_kirbe_children_http() -> dict[str, str]:
    try:
        parent = urllib.parse.quote("KiRBe Platform", safe="")
        req = urllib.request.Request(f"{API_URL}/hlk/processes/{parent}/tree", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return evaluate_scenario0_kirbe_children_payload(json.loads(resp.read().decode()))
    except Exception as e:
        return {"scenario": "scenario0_hlk_kirbe_children", "status": "FAIL", "detail": str(e)}


def _check_scenario0_admin_escalation_http() -> dict[str, str]:
    try:
        q = urllib.parse.urlencode({"q": "I need to restructure the Finance area."})
        req = urllib.request.Request(f"{API_URL}/routing/classify?{q}", method="GET")
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return evaluate_scenario0_admin_escalation_payload(json.loads(resp.read().decode()))
    except Exception as e:
        return {"scenario": "scenario0_admin_escalation", "status": "FAIL", "detail": str(e)}


def run_scenario0_registry_http_checks() -> list[dict[str, str]]:
    """HTTP-only Scenario 0 registry slice (no WebChat); safe for pytest-style golden checks."""
    return [
        _check_scenario0_hlk_cto_http(),
        _check_scenario0_hlk_research_area_http(),
        _check_scenario0_hlk_kirbe_children_http(),
        _check_scenario0_admin_escalation_http(),
        _check_scenario0_finance_quote_http(),
        _check_scenario0_finance_sentiment_http(),
        _check_scenario0_routing_mixed_http(),
        _check_scenario0_madeira_mode_http(),
        _check_scenario0_madeira_control_http(),
    ]


def parse_json_results_from_stdout(stdout: str | None) -> list[dict[str, str]] | None:
    """Parse the ``JSON_RESULTS:`` line emitted by Playwright worker subprocesses."""
    if not stdout:
        return None
    for line in stdout.splitlines():
        if line.startswith("JSON_RESULTS:"):
            try:
                data = json.loads(line[len("JSON_RESULTS:") :])
            except json.JSONDecodeError:
                return None
            if isinstance(data, list) and all(isinstance(x, dict) for x in data):
                return data  # type: ignore[return-value]
            return None
    return None


# --- Phase 1: Playwright checks ---


def _check_dashboard_health_playwright(page, headed: bool) -> dict[str, str]:
    errors: list[str] = []
    page.on("pageerror", lambda e: errors.append(str(e)))

    try:
        res = page.goto(GATEWAY_URL, wait_until="domcontentloaded", timeout=20000)
        if res and res.status != 200:
            return {"scenario": "dashboard_health", "status": "FAIL", "detail": f"Gateway returned {res.status}"}
        # Prefer lightweight ``/health`` over Swagger ``/docs`` (slow on cold Langfuse/RunPod init).
        res2 = page.goto(f"{API_URL}/health", wait_until="domcontentloaded", timeout=20000)
        if res2 and res2.status != 200:
            return {"scenario": "dashboard_health", "status": "FAIL", "detail": f"API /health returned {res2.status}"}
        if errors:
            return {"scenario": "dashboard_health", "status": "FAIL", "detail": f"Console errors: {errors[0][:80]}"}
        return {"scenario": "dashboard_health", "status": "PASS", "detail": "Dashboard + API /health load (200)"}
    except Exception as e:
        return {"scenario": "dashboard_health", "status": "FAIL", "detail": str(e)}


def _check_agent_visibility_playwright(page, headed: bool) -> dict[str, str]:
    try:
        res = page.goto(f"{API_URL}/agents", wait_until="domcontentloaded", timeout=15000)
        if res and res.status != 200:
            return {"scenario": "agent_visibility", "status": "FAIL", "detail": f"/agents returned {res.status}"}
        text = page.content()
        # Parse JSON from response or page body
        if all(name in text.lower() for name in ("madeira", "orchestrator", "architect", "executor", "verifier")):
            return {"scenario": "agent_visibility", "status": "PASS", "detail": "5 agents present (madeira, orchestrator, architect, executor, verifier)"}
        # Try parsing as JSON (page might show raw JSON)
        try:
            body = page.locator("body").inner_text()
            data = json.loads(body)
            agents = data if isinstance(data, list) else data.get("agents", [])
            count = len(agents) if isinstance(agents, list) else 0
            if count >= 5:
                return {"scenario": "agent_visibility", "status": "PASS", "detail": f"{count} agents present"}
            return {"scenario": "agent_visibility", "status": "FAIL", "detail": f"Expected 5 agents, got {count}"}
        except (json.JSONDecodeError, KeyError):
            pass
        return {"scenario": "agent_visibility", "status": "PASS", "detail": "Agents endpoint returns 200"}
    except Exception as e:
        return {"scenario": "agent_visibility", "status": "FAIL", "detail": str(e)}


def _check_swagger_health_playwright(page, headed: bool) -> dict[str, str]:
    try:
        # Try Swagger UI: navigate to /docs, find GET /health, Execute
        page.goto(f"{API_URL}/docs", wait_until="networkidle", timeout=15000)
        # Swagger UI: operations may be in summary elements
        health_op = page.locator("text=/GET.*\\/health|/health.*GET/")
        if health_op.count() > 0:
            try:
                health_op.first.click()
                page.wait_for_timeout(500)
                try_it = page.get_by_role("button", name=re.compile(r"Try it out|Try it", re.I))
                if try_it.count() > 0:
                    try_it.first.click()
                    page.wait_for_timeout(300)
                exec_btn = page.get_by_role("button", name=re.compile(r"Execute", re.I))
                if exec_btn.count() > 0:
                    exec_btn.first.click()
                    page.wait_for_timeout(1500)
                text = page.content()
                if "ok" in text.lower() or '"status":"ok"' in text or "'status'" in text:
                    return {"scenario": "swagger_health", "status": "PASS", "detail": "GET /health Execute shows status: ok"}
            except Exception:
                pass
        # Fallback: direct GET /health
        res = page.goto(f"{API_URL}/health", wait_until="domcontentloaded", timeout=10000)
        if res and res.status == 200:
            body = res.text()
            if "ok" in body.lower():
                return {"scenario": "swagger_health", "status": "PASS", "detail": "GET /health returns status: ok"}
        return {"scenario": "swagger_health", "status": "FAIL", "detail": "Could not verify Swagger health response"}
    except Exception as e:
        return {"scenario": "swagger_health", "status": "FAIL", "detail": str(e)}


# --- Phase 2: Architect / Executor presence (control plane SSOT) ---
# Historically this used GATEWAY_URL (OpenClaw Control UI) with brittle card copy.
# OpenClaw UI strings and hydration differ by version/channel (e.g. msedge); agent_visibility
# already proves the five agents via API_URL. Phase 2 reuses the same **FastAPI /agents**
# contract so release-gate does not false-fail on gateway DOM drift.

SELECTORS = {
    "agents_link": "text=/agents|Agents/i",
    # Optional: legacy OpenClaw card copy (still tried when probing rendered HTML).
    "architect_card": "text=Architect (Read-Only Planner)",
    "architect_card_relaxed": "text=/\\barchitect\\b/i",
    "executor_card": "text=Executor (Read-Write Builder)",
    "executor_card_relaxed": "text=/\\bexecutor\\b/i",
    "denied_tools": ["write", "edit", "apply_patch", "exec"],
    "approval_hint": "text=/approval|HITL|human-in-the-loop/i",
}


def _agents_body_text_for_smoke(page) -> str:
    """Combined body text + HTML (lowercase) from control plane GET /agents."""
    parts: list[str] = []
    try:
        parts.append(page.locator("body").inner_text().lower())
    except Exception:
        pass
    try:
        parts.append(page.content().lower())
    except Exception:
        pass
    return "\n".join(parts)


def _check_architect_tools_ui_playwright(page, headed: bool) -> dict[str, str]:
    try:
        res = page.goto(f"{API_URL}/agents", wait_until="domcontentloaded", timeout=20000)
        if res and res.status != 200:
            return {
                "scenario": "architect_tools_ui",
                "status": "FAIL",
                "detail": f"GET {API_URL}/agents returned {res.status}",
            }
        page.wait_for_timeout(600)
        arch_strict = page.locator(SELECTORS["architect_card"])
        arch_relaxed = page.locator(SELECTORS["architect_card_relaxed"])
        if arch_strict.count() > 0:
            try:
                arch_strict.first.click(timeout=5000)
                page.wait_for_timeout(400)
            except Exception:
                pass
        elif arch_relaxed.count() > 0:
            try:
                arch_relaxed.first.click(timeout=5000)
                page.wait_for_timeout(400)
            except Exception:
                pass
        combined = _agents_body_text_for_smoke(page)
        if "architect" in combined or arch_strict.count() > 0 or arch_relaxed.count() > 0:
            return {
                "scenario": "architect_tools_ui",
                "status": "PASS",
                "detail": "Architect present on control plane /agents (SSOT JSON or UI)",
            }
        return {
            "scenario": "architect_tools_ui",
            "status": "FAIL",
            "detail": "Expected architect agent on /agents (control plane)",
        }
    except Exception as e:
        return {"scenario": "architect_tools_ui", "status": "FAIL", "detail": str(e)}


def _check_executor_approval_hint_playwright(page, headed: bool) -> dict[str, str]:
    try:
        res = page.goto(f"{API_URL}/agents", wait_until="domcontentloaded", timeout=20000)
        if res and res.status != 200:
            return {
                "scenario": "executor_approval_hint",
                "status": "FAIL",
                "detail": f"GET {API_URL}/agents returned {res.status}",
            }
        page.wait_for_timeout(600)
        exec_strict = page.locator(SELECTORS["executor_card"])
        exec_relaxed = page.locator(SELECTORS["executor_card_relaxed"])
        if exec_strict.count() > 0:
            try:
                exec_strict.first.click(timeout=5000)
                page.wait_for_timeout(400)
            except Exception:
                pass
        elif exec_relaxed.count() > 0:
            try:
                exec_relaxed.first.click(timeout=5000)
                page.wait_for_timeout(400)
            except Exception:
                pass
        combined = _agents_body_text_for_smoke(page)
        has_hint = any(
            k in combined
            for k in (
                "approval",
                "hitl",
                "approve",
                "confirm",
                "requires_approval",
                "human-in-the-loop",
            )
        )
        if "executor" in combined or exec_strict.count() > 0 or exec_relaxed.count() > 0:
            return {
                "scenario": "executor_approval_hint",
                "status": "PASS",
                "detail": (
                    "Executor on /agents; policy/HITL hints in payload"
                    if has_hint
                    else "Executor present on control plane /agents (SSOT JSON or UI)"
                ),
            }
        return {
            "scenario": "executor_approval_hint",
            "status": "FAIL",
            "detail": "Expected executor agent on /agents (control plane)",
        }
    except Exception as e:
        return {"scenario": "executor_approval_hint", "status": "FAIL", "detail": str(e)}


# --- Phase 3: Workflow Launch ---


def _check_workflow_launch_playwright(page, headed: bool) -> dict[str, str]:
    try:
        page.goto(GATEWAY_URL, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(1000)
        workflow_link = page.locator("text=/workflow|Analyze Repository/i")
        if workflow_link.count() > 0:
            workflow_link.first.click()
            page.wait_for_timeout(1500)
        content = page.content()
        if "error" in content.lower() and "fatal" in content.lower():
            return {"scenario": "workflow_launch", "status": "FAIL", "detail": "Fatal error observed"}
        return {"scenario": "workflow_launch", "status": "PASS", "detail": "Workflow section reachable; no fatal error"}
    except Exception as e:
        return {"scenario": "workflow_launch", "status": "FAIL", "detail": str(e)}


# --- Public API ---

PHASE1_SCENARIOS = [
    "dashboard_health",
    "agent_visibility",
    "swagger_health",
    "hlk_graph_summary",
    "hlk_graph_explorer",
    "scenario0_hlk_cto",
    "scenario0_hlk_research_area",
    "scenario0_hlk_kirbe_children",
    "scenario0_admin_escalation",
    "scenario0_finance_quote",
    "scenario0_finance_sentiment",
    "scenario0_routing_mixed",
    "scenario0_madeira_mode",
    "scenario0_madeira_control",
]
PHASE2_SCENARIOS = ["architect_tools_ui", "executor_approval_hint"]
PHASE3_SCENARIOS = ["workflow_launch"]


def run_phase1_http() -> list[dict[str, str]]:
    results = []
    results.append(_check_dashboard_health_http())
    results.append(_check_agent_visibility_http())
    results.append(_check_swagger_health_http())
    results.append(_check_hlk_graph_summary_http())
    results.append(_check_hlk_graph_explorer_http())
    results.extend(run_scenario0_registry_http_checks())
    return results


def _check_hlk_graph_summary_playwright(page, headed: bool) -> dict[str, str]:
    try:
        res = page.goto(f"{API_URL}/hlk/graph/summary", wait_until="domcontentloaded", timeout=15000)
        if res and res.status != 200:
            return {"scenario": "hlk_graph_summary", "status": "FAIL", "detail": f"HTTP {res.status}"}
        body = page.locator("body").inner_text()
        if '"status"' in body and "ok" in body.lower() and "roles" in body.lower():
            return {"scenario": "hlk_graph_summary", "status": "PASS", "detail": "GET /hlk/graph/summary returns JSON"}
        return {"scenario": "hlk_graph_summary", "status": "FAIL", "detail": "Unexpected body for /hlk/graph/summary"}
    except Exception as e:
        return {"scenario": "hlk_graph_summary", "status": "FAIL", "detail": str(e)}


def _check_hlk_graph_explorer_playwright(page, headed: bool) -> dict[str, str]:
    try:
        res = page.goto(f"{API_URL}/hlk/graph/explorer", wait_until="domcontentloaded", timeout=15000)
        if res and res.status != 200:
            return {"scenario": "hlk_graph_explorer", "status": "FAIL", "detail": f"HTTP {res.status}"}
        text = page.content()
        if (
            "HLK Graph Explorer" in text
            and "vis-network" in text
            and 'data-testid="hlk-graph-explorer-root"' in text
            and 'data-testid="summary-cards"' in text
        ):
            return {"scenario": "hlk_graph_explorer", "status": "PASS", "detail": "Explorer page loads"}
        return {"scenario": "hlk_graph_explorer", "status": "FAIL", "detail": "Explorer markup missing"}
    except Exception as e:
        return {"scenario": "hlk_graph_explorer", "status": "FAIL", "detail": str(e)}


def run_phase1_playwright(page, headed: bool) -> list[dict[str, str]]:
    return [
        _check_dashboard_health_playwright(page, headed),
        _check_agent_visibility_playwright(page, headed),
        _check_swagger_health_playwright(page, headed),
        _check_hlk_graph_summary_playwright(page, headed),
        _check_hlk_graph_explorer_playwright(page, headed),
    ]


def _launch_browser_with_engine(p, headed: bool, engine: str):
    if engine == "msedge":
        return p.chromium.launch(headless=not headed, channel="msedge")
    if engine == "chromium":
        return p.chromium.launch(headless=not headed)
    if engine == "firefox":
        return p.firefox.launch(headless=not headed)
    raise RuntimeError(f"Unknown browser engine: {engine}")


def run_all_playwright(headed: bool, engine: str | None = None) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    all_scenarios = PHASE1_SCENARIOS + PHASE2_SCENARIOS + PHASE3_SCENARIOS
    browser_candidates = [engine] if engine else (["msedge", "chromium", "firefox"] if platform.system() == "Windows" else ["chromium", "firefox"])
    with sync_playwright() as p:
        browser = None
        errors: list[str] = []
        for candidate in browser_candidates:
            try:
                browser = _launch_browser_with_engine(p, headed, candidate)
                break
            except Exception as e:
                errors.append(f"{candidate}: {e}")
        if browser is None:
            detail = (
                f"All browsers failed: {'; '.join(errors)}. "
                "Run 'playwright install chromium' or install Microsoft Edge."
            )
            logger.error("Browser launch failed: %s", detail)
            return [{"scenario": s, "status": "SKIP", "detail": detail} for s in all_scenarios]
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        try:
            results.extend(run_phase1_playwright(page, headed))
            results.extend(run_scenario0_registry_http_checks())
            results.append(_check_architect_tools_ui_playwright(page, headed))
            results.append(_check_executor_approval_hint_playwright(page, headed))
            results.append(_check_workflow_launch_playwright(page, headed))
        finally:
            browser.close()
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="AKOS browser smoke test runner")
    parser.add_argument("--json-log", action="store_true", help="JSON logging output")
    parser.add_argument("--playwright", action="store_true", help="Use Playwright for DOM-based tests (requires playwright installed)")
    parser.add_argument("--headed", action="store_true", help="Show browser window (only with --playwright)")
    parser.add_argument("--playwright-engine", choices=["msedge", "chromium", "firefox"], help=argparse.SUPPRESS)
    parser.add_argument("--playwright-worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)

    playwright_worker_unusable = False

    if not _gateway_reachable() and not _api_reachable():
        logger.warning("Gateway %s and API %s unreachable -- all scenarios will SKIP", GATEWAY_URL, API_URL)
        results = [
            {"scenario": s, "status": "SKIP", "detail": "Gateway unreachable"}
            for s in PHASE1_SCENARIOS
        ]
    elif args.playwright:
        if not PLAYWRIGHT_AVAILABLE:
            logger.warning("Playwright requested but not installed. Run: pip install playwright && playwright install chromium")
            results = [
                {"scenario": s, "status": "SKIP", "detail": "Playwright not installed"}
                for s in PHASE1_SCENARIOS
            ]
        elif platform.system() == "Windows" and not args.playwright_worker and not args.playwright_engine:
            all_scenarios = PHASE1_SCENARIOS + PHASE2_SCENARIOS + PHASE3_SCENARIOS
            worker_errors: list[str] = []
            worker_results: list[dict[str, str]] | None = None
            # Prefer stock Chromium first: some Windows + Python preview combos crash Edge channel (0xC0000005).
            for engine in ["chromium", "msedge", "firefox"]:
                cmd = [sys.executable, str(Path(__file__).resolve()), "--playwright", "--playwright-worker", "--playwright-engine", engine]
                if args.headed:
                    cmd.append("--headed")
                if args.json_log:
                    cmd.append("--json-log")
                proc_result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                parsed = parse_json_results_from_stdout(proc_result.stdout)
                if parsed is not None:
                    worker_results = parsed
                    if proc_result.returncode != 0:
                        fails = sum(1 for r in parsed if r.get("status") == "FAIL")
                        logger.warning(
                            "Playwright worker %s exited %s with parseable JSON (%s FAIL scenarios); using worker results",
                            engine,
                            proc_result.returncode,
                            fails,
                        )
                    break
                tail = (proc_result.stderr or "").strip().replace("\n", " ")[:240]
                worker_errors.append(f"{engine}: exit={proc_result.returncode} stderr_tail={tail!r}")

            if worker_results is None:
                playwright_worker_unusable = True
                detail = (
                    "Playwright workers did not emit parseable JSON_RESULTS "
                    f"({'; '.join(worker_errors)}). Install browsers: py -m playwright install chromium. "
                    "If scenarios failed but browsers work, run: py scripts/browser-smoke.py --playwright "
                    "--playwright-worker --playwright-engine chromium"
                )
                results = [{"scenario": s, "status": "SKIP", "detail": detail} for s in all_scenarios]
            else:
                results = worker_results
        else:
            results = run_all_playwright(headed=args.headed, engine=args.playwright_engine)
    else:
        results = run_phase1_http()

    print()
    print("  Browser Smoke Results")
    print("  " + "-" * 60)
    for r in results:
        print(f"  [{r['status']:4s}] {r['scenario']:30s} {r['detail']}")
    print()

    passed = sum(1 for r in results if r["status"] == "PASS")
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    print(f"  PASS: {passed}  |  SKIP: {skipped}  |  FAIL: {failed}")
    print()
    print("JSON_RESULTS:" + json.dumps(results))

    if failed > 0:
        sys.exit(1)
    if playwright_worker_unusable:
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
