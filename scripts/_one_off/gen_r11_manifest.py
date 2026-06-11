#!/usr/bin/env python3
"""One-off generator for Automation OS R11 manifest (monorepo + agent CLI + adapter interop)."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = (
    REPO
    / "docs/wip/intelligence/akos-automation-os-governance-2026-06-10/tranches/r11-manifest.json"
)
GITHUB_MAIN = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def ledger_url(path: str) -> str:
    """Repo-relative docs/ paths pass through; other paths use GitHub blob URLs."""
    if path.startswith("docs/"):
        return path
    return GITHUB_MAIN + path.replace(chr(92), "/")


# Priority-ordered CORP-VAULT-ENVOY + CORP-VAULT-ADAPTERS (MADEIRA + adapter SSOT).
CORPINT_PATHS: list[tuple[str, str, str]] = [
    ("Envoy repositories README", "docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/README.md", "P11-ENVOY-MADEIRA"),
    ("Repositories registry", "docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md", "P11-ENVOY-MADEIRA"),
    ("External repo contract template", "docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md", "P11-ENVOY-MADEIRA"),
    ("MADEIRA tool catalog", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_TOOL_CATALOG.md", "P11-ENVOY-MADEIRA"),
    ("MADEIRA tool RBAC CSV", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/MADEIRA_TOOL_RBAC.csv", "P11-ENVOY-MADEIRA"),
    ("SOP OpenClaw runtime health triage", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001.md", "P11-ENVOY-MADEIRA"),
    ("SOP MADEIRA incident response", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-MADEIRA_INCIDENT_RESPONSE_001.md", "P11-ENVOY-MADEIRA"),
    ("SOP MADEIRA verdict and cadence", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-MADEIRA_VERDICT_AND_CADENCE_001.md", "P11-ENVOY-MADEIRA"),
    ("SOP MADEIRA scenario lifecycle", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-MADEIRA_SCENARIO_LIFECYCLE_001.md", "P11-ENVOY-MADEIRA"),
    ("Playwright config template", "docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/playwright.config.ts.tmpl", "P11-ENVOY-MADEIRA"),
    ("CI baseline workflow template", "docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/_templates/github-workflows/ci-baseline.yml.tmpl", "P11-ENVOY-MADEIRA"),
    ("Neo4j strategy", "docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/NEO4J_STRATEGY.md", "P11-ENVOY-MADEIRA"),
    ("OpenClaw config example", "config/openclaw.json.example", "P11-ENVOY-MADEIRA"),
    ("MCporter config example", "config/mcporter.json.example", "P11-ENVOY-MADEIRA"),
    ("RevOps adapter registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/Operations/RevOps/canonicals/dimensions/REVOPS_ADAPTER_REGISTRY.csv", "P12-RPA-ADAPTERS"),
    ("RPA adapter registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/dimensions/RPA_ADAPTER_REGISTRY.csv", "P12-RPA-ADAPTERS"),
    ("Rendering pipeline registry CSV", "docs/references/hlk/v3.0/Envoy Tech Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv", "P12-RPA-ADAPTERS"),
    ("Substrate registry CSV", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv", "P11-ENVOY-MADEIRA"),
    ("bless_external_repo runbook", "scripts/bless_external_repo.py", "P11-ENVOY-MADEIRA"),
    ("hlk_graph_mcp_server runbook", "scripts/hlk_graph_mcp_server.py", "P11-ENVOY-MADEIRA"),
    ("hlk_mcp_server runbook", "scripts/hlk_mcp_server.py", "P11-ENVOY-MADEIRA"),
    ("validate_repository_registry runbook", "scripts/validate_repository_registry.py", "P11-ENVOY-MADEIRA"),
    ("validate_substrate_registry runbook", "scripts/validate_substrate_registry.py", "P11-ENVOY-MADEIRA"),
    ("AIC delegation cursor rule", ".cursor/rules/akos-aic-delegation.mdc", "P11-ENVOY-MADEIRA"),
    ("akos hlk adapter registry module", "akos/hlk_adapter_registry_csv.py", "P12-RPA-ADAPTERS"),
]

# OSINT-AGENT-CLI + OSINT-MONOREPO + OSINT-INTEROP.
OSINT_SOURCES: list[tuple[str, str, str, str, str, bool]] = [
    ("Cursor CLI docs", "https://docs.cursor.com/cli/overview", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Claude Code CLI", "https://docs.anthropic.com/en/docs/claude-code", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("OpenAI Codex CLI", "https://developers.openai.com/codex/cli/", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Aider AI pair programming", "https://aider.chat/docs/", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Continue.dev agent IDE", "https://docs.continue.dev/", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("LangGraph agents", "https://langchain-ai.github.io/langgraph/", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("CrewAI multi-agent", "https://docs.crewai.com/", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("AutoGen agent framework", "https://microsoft.github.io/autogen/", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Semantic Kernel agents", "https://learn.microsoft.com/en-us/semantic-kernel/overview/", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Agent CLI hype skeptic", "https://www.theregister.com/2025/02/14/ai_coding_agent_cli_hype/", "OSINT-SKEP", "P11-ENVOY-MADEIRA", "2.1", True),
    ("Nx monorepo docs", "https://nx.dev/getting-started/intro", "OSINT-MONOREPO", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Turborepo handbook", "https://turbo.build/repo/docs/handbook", "OSINT-MONOREPO", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Lerna monorepo", "https://lerna.js.org/docs/", "OSINT-MONOREPO", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Rush.js monorepo", "https://rushjs.io/pages/intro/welcome/", "OSINT-MONOREPO", "P11-ENVOY-MADEIRA", "4.1", False),
    ("pnpm workspaces", "https://pnpm.io/workspaces", "OSINT-MONOREPO", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Yarn workspaces", "https://yarnpkg.com/features/workspaces", "OSINT-MONOREPO", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Bazel monorepo patterns", "https://bazel.build/concepts/build-ref", "OSINT-MONOREPO", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Monorepo tooling fatigue", "https://www.infoq.com/articles/monorepo-polyrepo-tradeoffs/", "OSINT-SKEP", "P11-ENVOY-MADEIRA", "2.1", True),
    ("Model Context Protocol", "https://modelcontextprotocol.io/introduction", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("LangChain MCP adapters", "https://python.langchain.com/docs/concepts/mcp/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Composio tool router", "https://docs.composio.dev/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Toolhouse agent tools", "https://docs.toolhouse.ai/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Port IO catalog", "https://docs.getport.io/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("OpenAPI generator", "https://openapi-generator.tech/docs/generators", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Smithery MCP registry", "https://smithery.ai/docs", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("MCP security best practices", "https://modelcontextprotocol.io/docs/concepts/security", "OSINT-SKEP", "P12-RPA-ADAPTERS", "3.1", True),
    ("Agent tool sprawl warning", "https://www.gartner.com/en/articles/ai-agents", "OSINT-SKEP", "P11-ENVOY-MADEIRA", "3.1", True),
    ("RunPod serverless docs", "https://docs.runpod.io/serverless/overview", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("vLLM inference server", "https://docs.vllm.ai/en/latest/", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Ollama local models", "https://github.com/ollama/ollama/blob/main/docs/api.md", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("LiteLLM proxy router", "https://docs.litellm.ai/docs/", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("OpenRouter API", "https://openrouter.ai/docs", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Agent orchestration overclaim", "https://www.nature.com/articles/d41586-024-01445-4", "OSINT-SKEP", "P11-ENVOY-MADEIRA", "2.1", True),
    ("Changesets release workflow", "https://github.com/changesets/changesets/blob/main/docs/intro-to-using-changesets.md", "OSINT-MONOREPO", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Renovate monorepo mode", "https://docs.renovatebot.com/configuration-options/#monorepo", "OSINT-MONOREPO", "P11-ENVOY-MADEIRA", "4.1", False),
    ("GitHub merge queue", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue", "OSINT-MONOREPO", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Graphile Worker Postgres jobs", "https://worker.graphile.org/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Temporal durable workflows", "https://docs.temporal.io/workflows", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Prefect orchestration", "https://docs.prefect.io/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Dagster data orchestration", "https://docs.dagster.io/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Airflow workflow platform", "https://airflow.apache.org/docs/", "OSINT-INTEROP", "P12-RPA-ADAPTERS", "4.1", False),
    ("Low-code agent builder skeptic", "https://www.theregister.com/2024/11/20/no_code_ai_agents/", "OSINT-SKEP", "P11-ENVOY-MADEIRA", "2.1", True),
    ("MCP protocol fragmentation", "https://www.infoq.com/news/2025/mcp-adoption/", "OSINT-SKEP", "P12-RPA-ADAPTERS", "3.1", True),
    ("Multi-agent coordination limits", "https://queue.acm.org/detail.cfm?id=3710842", "OSINT-SKEP", "P11-ENVOY-MADEIRA", "4.1", True),
    ("Integration platform fatigue", "https://www.chiefmartec.com/2023/12/integration-fatigue/", "OSINT-SKEP", "P12-RPA-ADAPTERS", "2.1", True),
    ("Cursor agent modes", "https://docs.cursor.com/agent/modes", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "4.1", False),
    ("Windsurf Cascade agent", "https://docs.windsurf.com/windsurf/cascade", "OSINT-AGENT-CLI", "P11-ENVOY-MADEIRA", "3.1", True),
]


def corp_row(seq: int, title: str, url: str, prong: str) -> dict:
    cluster = "corp_vault_adapters" if prong == "P12-RPA-ADAPTERS" else "corp_vault_envoy"
    return {
        "source_id": f"SRC-AOS-R11I-{seq:03d}",
        "prong": prong,
        "topic_cluster": cluster,
        "source_title_or_owner": title,
        "url": ledger_url(url),
        "format": "internal_canonical",
        "source_category": "CORPINT",
        "source_level": "5.1",
        "holistika_reliability_score": "5",
        "external_perceived_credibility_score": "2",
        "control_confidence_level": "Safe",
        "decision_use": "def-vault-harvest",
        "notes": (
            f"R11 monorepo/agent CLI/adapters vault; impacts: TECH_AUTOMATION_REGISTRY; "
            f"ICS:High; prong={prong}"
        ),
    }


def osint_row(seq: int, title: str, url: str, cluster: str, prong: str, level: str, skeptic: bool) -> dict:
    notes = "R11 OSINT; ICS:Load-bearing;"
    if skeptic:
        notes += " CON: vendor-hype or paywall;"
    return {
        "source_id": f"SRC-AOS-R11E-{seq:03d}",
        "prong": prong,
        "topic_cluster": cluster,
        "source_title_or_owner": title,
        "url": url,
        "format": "webpage",
        "source_category": "OSINT",
        "source_level": level,
        "holistika_reliability_score": "4",
        "external_perceived_credibility_score": "4",
        "control_confidence_level": "Euclid",
        "decision_use": "def-automation-os",
        "notes": notes,
    }


def main() -> None:
    corp_rows: list[dict] = []
    seq = 1
    for title, url, prong in CORPINT_PATHS:
        path = REPO / url.replace("/", "\\") if "\\" in str(REPO) else REPO / url
        if not path.is_file():
            raise SystemExit(f"missing corpint path: {url}")
        corp_rows.append(corp_row(seq, title, url, prong))
        seq += 1
    if len(corp_rows) < 25:
        raise SystemExit(f"expected >=25 corpint rows, got {len(corp_rows)}")

    osint_rows: list[dict] = []
    for idx, (title, url, cluster, prong, level, skeptic) in enumerate(OSINT_SOURCES, start=1):
        osint_rows.append(osint_row(idx, title, url, cluster, prong, level, skeptic))
    if len(osint_rows) < 46:
        raise SystemExit(f"expected >=46 osint rows, got {len(osint_rows)}")

    manifest = {
        "tranche": "R11",
        "id_prefix": "AOS-R11",
        "corpint_target": 25,
        "osint_target": 46,
        "census": {"enabled": False},
        "rows": corp_rows + osint_rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(manifest['rows'])} rows)")


if __name__ == "__main__":
    main()
