#!/usr/bin/env python3
"""Append Research R3 rows to holistic-agentic source ledger (+18 CORPINT, +59 OSINT).

R3: platform + infra + performance per RESEARCH_CHARTER_AND_EXECUTION_PLAN.md §5.
Appends to existing ledger; idempotent on URL dedup.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

OUT_DIR = (
    REPO_ROOT
    / "docs/wip/intelligence/holistic-agentic-capability-orchestration-2026-06-10"
)
LEDGER_PATH = OUT_DIR / "source-ledger.csv"

HEADER = [
    "source_id",
    "prong",
    "topic_cluster",
    "source_title_or_owner",
    "url",
    "format",
    "source_category",
    "source_level",
    "holistika_reliability_score",
    "external_perceived_credibility_score",
    "control_confidence_level",
    "decision_use",
    "notes",
]

CORPINT_TARGET = 18
OSINT_TARGET = 59

GITHUB_BLOB = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _ledger_url(path: Path) -> str:
    rel = _rel(path)
    return rel if rel.startswith("docs/") else f"{GITHUB_BLOB}{rel}"


def _norm_url(url: str) -> str:
    return url.split("#")[0].rstrip("/")


VAULT_HARVEST: list[tuple[str, str, str, str]] = [
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: MCP server definition SOP", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-MCP_SERVER_DEFINITION.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: TechOps discipline", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/TECHOPS_DISCIPLINE.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: CI/CD baseline", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-CICD_BASELINE_001.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: component service matrix", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: tooling standards", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-HLK_TOOLING_STANDARDS_001.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: release taxonomy", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-RELEASE_TAXONOMY_001.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: Envoy lab refactor architecture", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-ENVOYLAB_REFACTOR_ARCHITECTURE_001.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: cross-repo schema propagation", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Cross Repo/SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: external repo drift remediation", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/External Repos/SOP-EXTERNAL_REPO_DRIFT_REMEDIATION_001.md"),
    ("corp_vault_tech_r3", "P8-MADEIRA", "impacts: MADEIRA methodology mode", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_METHODOLOGY_MODE.md"),
    ("corp_vault_tech_r3", "P8-MADEIRA", "impacts: MADEIRA personality SOP", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-TECH_MADEIRA_PERSONALITY_001.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: subdomains registry", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/SUBDOMAINS_REGISTRY.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: Sentry dashboard holistika", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/SENTRY_DASHBOARD_HOLISTIKA.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: KiRBe showcase SOP", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-KIRBE_ENVOYTECH_SHOWCASE_003.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: MADEIRA incident response", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-MADEIRA_INCIDENT_RESPONSE_001.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: openclaw inventory example", "config/openclaw.json.example"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: AKOS architecture", "docs/ARCHITECTURE.md"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: MCP server script", "scripts/hlk_mcp_server.py"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: finance MCP server", "scripts/finance_mcp_server.py"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: GPU helper", "scripts/gpu.py"),
    ("corp_vault_tech_r3", "P6-TECH-SUBSTRATE", "impacts: release gate", "scripts/release-gate.py"),
]

OSINT_SOURCES: list[tuple[str, ...]] = [
    ("Cursor background agents", "https://docs.cursor.com/agent/background-agents", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; async agent sessions; CON: Cursor substrate fact"),
    ("Cursor agent tools", "https://docs.cursor.com/agent/tools", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; tool surface contract"),
    ("Cursor planning queue", "https://docs.cursor.com/agent/planning", "P5-OPS-PEOPLE", "4.1", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; queued instructions pattern"),
    ("MCP architecture", "https://modelcontextprotocol.io/docs/concepts/architecture", "P6-TECH-SUBSTRATE", "4.1", "5", "5", "Safe", "def-interop", "OSINT-INTEROP; protocol layering"),
    ("MCP transports", "https://modelcontextprotocol.io/docs/concepts/transports", "P6-TECH-SUBSTRATE", "4.1", "5", "5", "Safe", "def-interop", "OSINT-INTEROP; stdio vs SSE vs streamable HTTP"),
    ("MCP tools concept", "https://modelcontextprotocol.io/docs/concepts/tools", "P6-TECH-SUBSTRATE", "4.1", "5", "5", "Safe", "def-interop", "OSINT-INTEROP; tool schema contract"),
    ("Anthropic MCP connector", "https://docs.anthropic.com/en/docs/agents-and-tools/mcp-connector", "P6-TECH-SUBSTRATE", "4.1", "5", "5", "Safe", "def-interop", "OSINT-INTEROP; remote MCP consumption"),
    ("Google ADK docs", "https://google.github.io/adk-docs/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; Google agent dev kit"),
    ("AWS Bedrock agents", "https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html", "P6-TECH-SUBSTRATE", "4.1", "5", "5", "Euclid", "def-plat", "OSINT-PLAT; managed agent runtime"),
    ("Azure AI Agent Service", "https://learn.microsoft.com/en-us/azure/ai-services/agents/", "P6-TECH-SUBSTRATE", "4.1", "5", "5", "Euclid", "def-plat", "OSINT-PLAT; enterprise agent hosting"),
    ("Databricks agent framework", "https://docs.databricks.com/en/generative-ai/agent-framework/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; data-plane agents"),
    ("LangGraph platform", "https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/", "P6-TECH-SUBSTRATE", "3.2", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; hosted orchestration"),
    ("LangSmith deployment", "https://docs.smith.langchain.com/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; trace + deploy loop"),
    ("Continue.dev docs", "https://docs.continue.dev/", "P6-TECH-SUBSTRATE", "4.1", "4", "3", "Euclid", "def-plat", "OSINT-PLAT; OSS IDE agent; CON: smaller ecosystem"),
    ("Cline documentation", "https://docs.cline.bot/", "P6-TECH-SUBSTRATE", "4.1", "3", "3", "Euclid", "def-plat", "OSINT-PLAT; VS Code agent extension"),
    ("Aider pair programming", "https://aider.chat/docs/", "P6-TECH-SUBSTRATE", "3.2", "4", "3", "Euclid", "def-plat", "OSINT-PLAT; CLI agent harness"),
    ("OpenHands docs", "https://docs.all-hands.dev/", "P6-TECH-SUBSTRATE", "3.2", "4", "3", "Euclid", "def-plat", "OSINT-PLAT; autonomous dev agent OSS"),
    ("SWE-agent site", "https://swe-agent.com/", "P6-TECH-SUBSTRATE", "3.2", "5", "4", "Euclid", "def-plat", "OSINT-PLAT; academic agent benchmark stack"),
    ("Google SRE book", "https://sre.google/sre-book/table-of-contents/", "P6-TECH-SUBSTRATE", "5.1", "5", "5", "Safe", "def-sys", "OSINT-SYS; reliability engineering canon"),
    ("AWS WA reliability pillar", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html", "P6-TECH-SUBSTRATE", "5.1", "5", "5", "Safe", "def-sys", "OSINT-SYS; cloud reliability patterns"),
    ("Azure reliability framework", "https://learn.microsoft.com/en-us/azure/architecture/framework/resiliency/overview", "P6-TECH-SUBSTRATE", "5.1", "5", "5", "Safe", "def-sys", "OSINT-SYS; resiliency design"),
    ("Brendan Gregg USE method", "https://www.brendangregg.com/usemethod.html", "P6-TECH-SUBSTRATE", "2.1", "5", "4", "Safe", "def-sys", "OSINT-SYS; utilization saturation errors"),
    ("vLLM throughput tuning", "https://docs.vllm.ai/en/latest/serving/throughput.html", "P6-TECH-SUBSTRATE", "4.1", "5", "4", "Euclid", "def-sys", "OSINT-SYS; inference performance"),
    ("TensorRT-LLM docs", "https://nvidia.github.io/TensorRT-LLM/", "P6-TECH-SUBSTRATE", "4.1", "5", "4", "Euclid", "def-sys", "OSINT-SYS; GPU inference optimization"),
    ("OpenAI rate limits", "https://platform.openai.com/docs/guides/rate-limits", "P2-FINANCE", "4.1", "5", "5", "Safe", "def-sys", "OSINT-SYS; token throughput caps"),
    ("Anthropic rate limits", "https://docs.anthropic.com/en/api/rate-limits", "P2-FINANCE", "4.1", "5", "5", "Safe", "def-sys", "OSINT-SYS; API tier performance"),
    ("Anyscale LLM latency blog", "https://www.anyscale.com/blog/llm-latency", "P6-TECH-SUBSTRATE", "2.1", "4", "4", "Euclid", "def-sys", "OSINT-SYS; latency breakdown; CON: vendor"),
    ("Cloudflare Workers AI", "https://developers.cloudflare.com/workers-ai/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; edge inference substrate"),
    ("Fly.io machines scaling", "https://fly.io/docs/machines/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-sys", "OSINT-SYS; lightweight compute scale"),
    ("Render autoscaling", "https://render.com/docs/scaling", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-sys", "OSINT-SYS; PaaS scale patterns"),
    ("Honeycomb LLM observability", "https://www.honeycomb.io/blog/llm-observability", "P1-DATA", "2.1", "4", "4", "Euclid", "def-obs", "OSINT-SYS; trace-first LLM ops"),
    ("Datadog LLM observability", "https://www.datadoghq.com/product/llm-observability/", "P1-DATA", "4.1", "4", "4", "Euclid", "def-obs", "OSINT-SYS; enterprise LLM monitoring"),
    ("Grafana AI observability", "https://grafana.com/docs/grafana-cloud/monitor-applications/ai-observability/", "P1-DATA", "4.1", "4", "4", "Euclid", "def-obs", "OSINT-SYS; metrics+traces for agents"),
    ("Prometheus best practices", "https://prometheus.io/docs/practices/", "P6-TECH-SUBSTRATE", "5.1", "5", "5", "Safe", "def-sys", "OSINT-SYS; metrics instrumentation"),
    ("Kubernetes HPA", "https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/", "P6-TECH-SUBSTRATE", "5.1", "5", "5", "Safe", "def-sys", "OSINT-SYS; autoscale contract"),
    ("k6 load testing", "https://grafana.com/docs/k6/latest/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-sys", "OSINT-SYS; performance validation"),
    ("Agent Protocol spec", "https://agentprotocol.ai/", "P6-TECH-SUBSTRATE", "3.2", "3", "3", "Keter", "def-interop", "OSINT-INTEROP; emergent interop; CON: adoption unclear"),
    ("Microsoft Copilot Studio", "https://learn.microsoft.com/en-us/microsoft-copilot-studio/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; enterprise agent builder"),
    ("n8n AI agents", "https://docs.n8n.io/advanced-ai/", "P6-TECH-SUBSTRATE", "4.1", "3", "3", "Euclid", "def-plat", "OSINT-PLAT; workflow agent automation"),
    ("Cloudflare MCP server", "https://developers.cloudflare.com/agents/model-context-protocol/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-interop", "OSINT-INTEROP; edge MCP hosting"),
    ("Supabase MCP guide", "https://supabase.com/docs/guides/getting-started/mcp", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-interop", "OSINT-INTEROP; data-plane MCP; AKOS-adjacent"),
    ("E2B code interpreter", "https://e2b.dev/docs", "P6-TECH-SUBSTRATE", "4.1", "4", "3", "Euclid", "def-plat", "OSINT-PLAT; sandbox execution substrate"),
    ("Modal serverless GPUs", "https://modal.com/docs/guide", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-sys", "OSINT-SYS; burst GPU inference"),
    ("Runpod serverless", "https://docs.runpod.io/serverless/overview", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-sys", "OSINT-SYS; GPU serverless; operator substrate"),
    ("OpenRouter API", "https://openrouter.ai/docs", "P6-TECH-SUBSTRATE", "4.1", "4", "3", "Euclid", "def-plat", "OSINT-PLAT; model routing gateway"),
    ("LiteLLM proxy", "https://docs.litellm.ai/docs/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; unified LLM proxy"),
    ("Portkey AI gateway", "https://docs.portkey.ai/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; gateway observability"),
    ("Helicone LLM gateway", "https://docs.helicone.ai/", "P6-TECH-SUBSTRATE", "4.1", "4", "3", "Euclid", "def-plat", "OSINT-PLAT; cost+latency logging"),
    ("AgentOps monitoring", "https://docs.agentops.ai/", "P6-TECH-SUBSTRATE", "4.1", "4", "3", "Euclid", "def-obs", "OSINT-SYS; agent session monitoring"),
    ("Arize Phoenix eval", "https://docs.arize.com/phoenix", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-eval", "OSINT-SYS; trace eval harness"),
    ("Weights & Biases LLM tracking", "https://docs.wandb.ai/guides/track/llm", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-obs", "OSINT-SYS; experiment tracking"),
    ("NVIDIA NIM docs", "https://docs.nvidia.com/nim/", "P6-TECH-SUBSTRATE", "4.1", "5", "5", "Euclid", "def-sys", "OSINT-SYS; packaged inference microservices"),
    ("Red Hat OpenShift AI", "https://www.redhat.com/en/technologies/cloud-computing/openshift/openshift-ai", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "OSINT-PLAT; enterprise K8s agent stack"),
    ("IBM AI agents overview", "https://www.ibm.com/think/topics/ai-agents", "P4-MARKETING", "4.1", "4", "3", "Euclid", "def-plat", "OSINT-PLAT; market education voice; CON: marketing"),
    ("Zapier AI actions", "https://actions.zapier.com/", "P6-TECH-SUBSTRATE", "4.1", "3", "3", "Euclid", "def-interop", "OSINT-INTEROP; tool bridge pattern"),
    ("Locust load testing", "https://docs.locust.io/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-sys", "OSINT-SYS; Python load generator"),
    ("CNCF cloud native observability", "https://www.cncf.io/blog/2024/03/21/a-guide-to-cloud-native-observability/", "P6-TECH-SUBSTRATE", "2.1", "4", "4", "Euclid", "def-obs", "OSINT-SYS; observability landscape"),
    ("Salesforce Agentforce", "https://www.salesforce.com/agentforce/", "P4-MARKETING", "4.1", "3", "3", "Euclid", "def-plat", "OSINT-PLAT; CRM agent surface; CON: hype"),
    ("Stripe agent toolkit GitHub", "https://github.com/stripe/agent-toolkit", "P6-TECH-SUBSTRATE", "3.2", "4", "4", "Euclid", "def-interop", "OSINT-INTEROP; fintech MCP tools"),
]


def _load_existing() -> tuple[list[dict[str, str]], set[str], set[str]]:
    rows: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    seen_ids: set[str] = set()
    if not LEDGER_PATH.is_file():
        return rows, seen_urls, seen_ids
    with LEDGER_PATH.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for raw in reader:
            sid = raw.get("source_id", "")
            if sid in seen_ids:
                continue
            seen_ids.add(sid)
            rows.append(raw)
            seen_urls.add(_norm_url(raw["url"]))
    return rows, seen_urls, seen_ids


def _corpint_rows(seen: set[str], seen_ids: set[str], seq: list[int]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []

    def add(
        cluster: str,
        prong: str,
        title: str,
        url: str,
        fmt: str,
        notes: str,
    ) -> bool:
        key = _norm_url(url)
        if key in seen:
            return False
        seq[0] += 1
        seen.add(key)
        sid = f"SRC-HAC-R3I-{seq[0]:03d}"
        while sid in seen_ids:
            seq[0] += 1
            sid = f"SRC-HAC-R3I-{seq[0]:03d}"
        seen_ids.add(sid)
        out.append(
            {
                "source_id": sid,
                "prong": prong,
                "topic_cluster": cluster,
                "source_title_or_owner": title[:240],
                "url": url[:500],
                "format": fmt,
                "source_category": "CORPINT",
                "source_level": "5.1",
                "holistika_reliability_score": "5",
                "external_perceived_credibility_score": "2",
                "control_confidence_level": "Safe",
                "decision_use": "def-vault-platform",
                "notes": notes[:600],
            }
        )
        return True

    for cluster, prong, impact, pattern in VAULT_HARVEST:
        if len(out) >= CORPINT_TARGET:
            break
        for path in sorted(REPO_ROOT.glob(pattern) if "*" in pattern else [REPO_ROOT / pattern]):
            if not path.is_file():
                continue
            fmt = "dataset" if path.suffix.lower() == ".csv" else (
                "internal_canonical" if path.suffix.lower() in {".yaml", ".yml", ".json"} else "report"
            )
            if path.suffix.lower() == ".py":
                fmt = "report"
            add(cluster, prong, path.stem[:80], _ledger_url(path), fmt, f"R3 vault harvest; {impact}")
            if len(out) >= CORPINT_TARGET:
                break
    return out[:CORPINT_TARGET]


def _osint_rows(seen: set[str], seen_ids: set[str], seq: list[int]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    fmt_cycle = ("article", "webpage", "report", "book")
    for i, (title, url, prong, level, rel, ext, ccl, use, notes) in enumerate(OSINT_SOURCES):
        if _norm_url(url) in seen:
            continue
        seq[0] += 1
        seen.add(_norm_url(url))
        cluster = "osint_plat"
        if "OSINT-SYS" in notes:
            cluster = "osint_sys"
        elif "OSINT-INTEROP" in notes:
            cluster = "osint_interop"
        sid = f"SRC-HAC-R3E-{seq[0]:03d}"
        while sid in seen_ids:
            seq[0] += 1
            sid = f"SRC-HAC-R3E-{seq[0]:03d}"
        seen_ids.add(sid)
        out.append(
            {
                "source_id": sid,
                "prong": prong,
                "topic_cluster": cluster,
                "source_title_or_owner": title[:240],
                "url": url,
                "format": fmt_cycle[i % len(fmt_cycle)],
                "source_category": "OSINT",
                "source_level": level,
                "holistika_reliability_score": rel,
                "external_perceived_credibility_score": ext,
                "control_confidence_level": ccl,
                "decision_use": use,
                "notes": notes[:600],
            }
        )
    return out[:OSINT_TARGET]


def main() -> int:
    existing, seen, seen_ids = _load_existing()
    r3i_present = sum(1 for r in existing if r.get("source_id", "").startswith("SRC-HAC-R3I-"))
    r3e_present = sum(1 for r in existing if r.get("source_id", "").startswith("SRC-HAC-R3E-"))
    corpint_need = max(0, CORPINT_TARGET - r3i_present)
    osint_need = max(0, OSINT_TARGET - r3e_present)

    seq_c = [r3i_present]
    seq_e = [r3e_present]
    corpint = _corpint_rows(seen, seen_ids, seq_c)[:corpint_need]
    osint = _osint_rows(seen, seen_ids, seq_e)[:osint_need]
    combined = existing + corpint + osint

    with LEDGER_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(combined)

    r3i_total = r3i_present + len(corpint)
    r3e_total = r3e_present + len(osint)
    print(f"Appended to {LEDGER_PATH}")
    print(
        f"  prior={len(existing)} + corpint={len(corpint)} + osint={len(osint)} "
        f"= total={len(combined)} (R3I={r3i_total} R3E={r3e_total})"
    )
    if r3i_total < CORPINT_TARGET or r3e_total < OSINT_TARGET:
        print(
            f"WARN: R3 totals R3I={r3i_total}/{CORPINT_TARGET} "
            f"R3E={r3e_total}/{OSINT_TARGET}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
