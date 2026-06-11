#!/usr/bin/env python3
"""Append Research R2 rows to holistic-agentic source ledger (+50 CORPINT, +58 OSINT).

R2: vault process harvest + context/KM voices per RESEARCH_CHARTER_AND_EXECUTION_PLAN.md §5.
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
PL_PATH = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv"
)

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

CORPINT_TARGET = 50
OSINT_TARGET = 58

GITHUB_BLOB = "https://github.com/FraysaXII/openclaw-akos/blob/main/"


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _ledger_url(path: Path) -> str:
    rel = _rel(path)
    return rel if rel.startswith("docs/") else f"{GITHUB_BLOB}{rel}"


def _norm_url(url: str) -> str:
    return url.split("#")[0].rstrip("/")


VAULT_HARVEST: list[tuple[str, str, str, str]] = [
    # cluster, prong, impact_note, glob or path suffix
    ("corp_vault_km", "P1-DATA", "impacts-orchestration: KM recall for agent context", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/HLK_KM_TOPIC_FACT_SOURCE.md"),
    ("corp_vault_km", "P1-DATA", "impacted-by: agent sessions must emit recall metadata", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/KB_HUMAN_READABILITY_CHARTER.md"),
    ("corp_vault_km", "P1-DATA", "impacts: derived recall for long sessions", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/KM_CHANNEL_VALUE_NARRATIVE.md"),
    ("corp_vault_km", "P7-RESEARCH", "impacts: research outake handoff to agents", "docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_OUTAKE_HANDOFF_001.md"),
    ("corp_vault_km", "P7-RESEARCH", "impacted-by: substrate audit cadence", "docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md"),
    ("corp_vault_km", "P1-DATA", "impacts: km pilot visual assets", "docs/references/hlk/v3.0/_assets/km-pilot/**/*.md"),
    ("corp_vault_agentic", "P8-MADEIRA", "impacts: MADEIRA tool catalog", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_TOOL_CATALOG.md"),
    ("corp_vault_agentic", "P8-MADEIRA", "impacts: mode parity across substrates", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/MADEIRA_MODE_PARITY.md"),
    ("corp_vault_agentic", "P8-MADEIRA", "impacted-by: MADEIRA-AKOS status", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/MADEIRA-AKOS/STATUS.md"),
    ("corp_vault_agentic", "P6-TECH-SUBSTRATE", "impacts: agentic infra SOP", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-TECH_AGENTIC_INFRA_001.md"),
    ("corp_vault_agentic", "P6-TECH-SUBSTRATE", "impacts: MADEIRA persistence", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-TECH_MADEIRA_PERSISTENCE_001.md"),
    ("corp_vault_tech", "P6-TECH-SUBSTRATE", "impacts: graph strategy for context", "docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/NEO4J_STRATEGY.md"),
    ("corp_vault_tech", "P6-TECH-SUBSTRATE", "impacts: KiRBe routing", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/Repositories/KIRBE_ROUTING_AND_HOSTING.md"),
    ("corp_vault_tech", "P6-TECH-SUBSTRATE", "impacted-by: runtime health triage", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001.md"),
    ("corp_vault_tech", "P6-TECH-SUBSTRATE", "impacts: application governance", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/SOP-TECH_APPLICATION_GOVERNANCE_001.md"),
    ("corp_vault_tech", "P6-TECH-SUBSTRATE", "impacts: agentic framework landscape", "docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md"),
    ("corp_vault_data", "P1-DATA", "impacts: DataOps quality for agent events", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATAOPS_DISCIPLINE.md"),
    ("corp_vault_data", "P1-DATA", "impacts: data contract for mirrors", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATA_CONTRACT_STANDARD.md"),
    ("corp_vault_data", "P1-DATA", "impacted-by: integration plane", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATA_INTEGRATION_PLANE.md"),
    ("corp_vault_data", "P1-DATA", "impacts: governance policy", "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATA_GOVERNANCE_POLICY.md"),
    ("corp_vault_data", "P1-DATA", "impacts: data area charter", "docs/references/hlk/v3.0/Admin/O5-1/Data/canonicals/DATA_AREA_CHARTER.md"),
    ("corp_vault_ops", "P5-OPS-PEOPLE", "impacts: cross-area handoffs", "docs/references/hlk/v3.0/Admin/O5-1/Operations/canonicals/OPERATIONS_CROSS_AREA_HANDOFFS.md"),
    ("corp_vault_ops", "P5-OPS-PEOPLE", "impacts: workspace blueprint", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md"),
    ("corp_vault_ops", "P5-OPS-PEOPLE", "impacts: delivery discipline", "docs/references/hlk/v3.0/Admin/O5-1/Operations/OPERATIONS_DELIVERY_DISCIPLINE.md"),
    ("corp_vault_ops", "P5-OPS-PEOPLE", "impacts: operations area charter", "docs/references/hlk/v3.0/Admin/O5-1/Operations/OPERATIONS_AREA_CHARTER.md"),
    ("corp_vault_ops", "P5-OPS-PEOPLE", "impacts: process catalog", "docs/references/hlk/v3.0/Admin/O5-1/Operations/canonicals/OPERATIONS_PROCESS_CATALOG.yaml"),
    ("corp_vault_people", "P5-OPS-PEOPLE", "impacted-by: inter-wave regression", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md"),
    ("corp_vault_people", "P5-OPS-PEOPLE", "impacted-by: synthesis before tranche", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md"),
    ("corp_vault_people", "P5-OPS-PEOPLE", "impacts: UAT governance", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_UAT_GOVERNANCE_001.addendum.md"),
    ("corp_vault_people", "P7-RESEARCH", "impacts: capability doctrine", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_CAPABILITY_DOCTRINE.md"),
    ("corp_vault_ux", "P4-MARKETING", "impacts: UX discipline for agent surfaces", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/UX Designer/canonicals/UX_DISCIPLINE.md"),
    ("corp_vault_ux", "P4-MARKETING", "impacts: brand gantt discipline", "docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/UX Designer/canonicals/BRAND_GANTT_DISCIPLINE.md"),
    ("corp_vault_legal_ethics", "P3-LEGAL", "impacts: ethical agentic boundaries", "docs/references/hlk/v3.0/Admin/O5-1/People/Ethics/canonicals/ETHICAL_AGENTIC_BOUNDARIES.md"),
    ("corp_vault_legal_ethics", "P3-LEGAL", "impacts: access levels for audit", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/access_levels.md"),
    ("corp_vault_legal_ethics", "P3-LEGAL", "impacts: confidence levels", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md"),
    ("corp_vault_fin", "P2-FINANCE", "impacted-by: rev-rec for agent work", "docs/references/hlk/v3.0/Admin/O5-1/Finance/Business Controller/canonicals/FINOPS_REVENUE_RECOGNITION_POLICY.md"),
    ("corp_vault_fin", "P2-FINANCE", "impacts: classification lattice", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CLASSIFICATION_LATTICE.md"),
    ("corp_vault_proc", "P5-OPS-PEOPLE", "impacts: MADEIRA per-task registry", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/MADEIRA_AIC_PER_TASK_REGISTRY.csv"),
    ("corp_vault_proc", "P8-MADEIRA", "impacts: capability registry", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv"),
    ("corp_vault_proc", "P7-RESEARCH", "impacts: intelligenceops register", "docs/references/hlk/v3.0/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv"),
    ("corp_vault_km", "P7-RESEARCH", "impacts: research area charter", "docs/references/hlk/v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md"),
    ("corp_vault_km", "P7-RESEARCH", "impacts: research lifecycle", "docs/references/hlk/v3.0/Research/canonicals/RESEARCH_LIFECYCLE_DOCTRINE.md"),
    ("corp_vault_people", "P5-OPS-PEOPLE", "impacts: founder corpus inventory", "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_CORPUS_INVENTORY.md"),
    ("corp_vault_ops", "P5-OPS-PEOPLE", "impacts: holistika ops discovery", "docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md"),
    ("corp_vault_tech", "P6-TECH-SUBSTRATE", "impacts: system reliability SOP", "docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/SOP-TECH_SYSTEM_RELIABILITY_001.md"),
    ("corp_vault_legal_ethics", "P3-LEGAL", "impacts: PRECEDENCE asset map", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md"),
]

# (title, url, prong, level, rel, ext, ccl, use, notes) — 58 OSINT rows
OSINT_SOURCES: list[tuple[str, ...]] = [
    # R1-debt substrate (30) — deferred platform/orchestration
    ("Cursor Agent modes overview", "https://docs.cursor.com/agent/modes", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-substrate", "R1-debt OSINT; Agent/Ask/Manual modes; CON: Cursor-specific not scope boundary"),
    ("Cursor hooks documentation", "https://docs.cursor.com/agent/hooks", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-substrate", "R1-debt; event hooks for agent lifecycle"),
    ("Cursor MCP overview", "https://docs.cursor.com/context/mcp", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-interop", "R1-debt; MCP as substrate fact for AKOS"),
    ("Cursor codebase indexing", "https://docs.cursor.com/context/codebase-indexing", "P1-DATA", "4.1", "4", "4", "Euclid", "def-ctx", "R1-debt; context indexing semantics"),
    ("Cursor checkpoints", "https://docs.cursor.com/agent/chat/checkpoints", "P5-OPS-PEOPLE", "4.1", "4", "3", "Euclid", "def-handoff", "R1-debt; session snapshot vs git; CON: not ratification-durable"),
    ("LangGraph human-in-the-loop", "https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/", "P5-OPS-PEOPLE", "3.2", "4", "4", "Euclid", "def-orch", "R1-debt; HITL gate patterns"),
    ("LangChain context engineering guide", "https://blog.langchain.dev/context-engineering-for-agents/", "P7-RESEARCH", "2.1", "4", "3", "Euclid", "def-ctx", "R1-debt; context as engineering discipline"),
    ("Anthropic building effective agents", "https://www.anthropic.com/research/building-effective-agents", "P7-RESEARCH", "4.1", "5", "5", "Safe", "def-orch", "R1-debt; orchestration patterns; vendor but high rigor"),
    ("OpenAI agents SDK docs", "https://openai.github.io/openai-agents-python/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "R1-debt; substrate-agnostic agent SDK reference"),
    ("MCP specification", "https://modelcontextprotocol.io/introduction", "P6-TECH-SUBSTRATE", "4.1", "5", "5", "Safe", "def-interop", "R1-debt; tool/context protocol SSOT"),
    ("A2A agent protocol Google", "https://google.github.io/A2A/", "P6-TECH-SUBSTRATE", "3.2", "4", "4", "Euclid", "def-interop", "R1-debt; agent-to-agent interop"),
    ("Langfuse tracing sessions", "https://langfuse.com/docs/tracing", "P1-DATA", "4.1", "4", "4", "Euclid", "def-obs", "R1-debt; session trace model for DAMA fields"),
    ("OpenTelemetry gen AI semconv", "https://opentelemetry.io/docs/specs/semconv/gen-ai/", "P1-DATA", "5.1", "5", "5", "Safe", "def-obs", "R1-debt; gen-AI semantic conventions"),
    ("Temporal human-in-the-loop", "https://docs.temporal.io/ai-cookbook/human-in-the-loop", "P5-OPS-PEOPLE", "4.1", "4", "4", "Euclid", "def-orch", "R1-debt; durable workflow gates"),
    ("Microsoft AutoGen HITL", "https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/human-in-the-loop.html", "P5-OPS-PEOPLE", "3.2", "4", "4", "Euclid", "def-orch", "R1-debt; multi-agent HITL"),
    ("Vercel AI SDK agents", "https://sdk.vercel.ai/docs/ai-sdk-core/agents", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "R1-debt; serverless agent harness"),
    ("LlamaIndex agent workflows", "https://docs.llamaindex.ai/en/stable/understanding/agent/", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "R1-debt; KiRBe-adjacent substrate patterns"),
    ("Semantic Kernel planners", "https://learn.microsoft.com/en-us/semantic-kernel/concepts/planning", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-orch", "R1-debt; planner/orchestrator separation"),
    ("CrewAI human input on execution", "https://docs.crewai.com/how-to/human-input-on-execution", "P5-OPS-PEOPLE", "4.1", "3", "3", "Euclid", "def-hitl", "R1-debt; inline human gate; CON: framework hype"),
    ("Instructor structured outputs", "https://python.useinstructor.com/", "P7-RESEARCH", "3.2", "4", "3", "Euclid", "def-ctx", "R1-debt; structured context contracts"),
    ("Pydantic AI agents", "https://ai.pydantic.dev/agents/", "P6-TECH-SUBSTRATE", "4.1", "5", "4", "Euclid", "def-plat", "R1-debt; AKOS-adjacent validation substrate"),
    ("GitHub Copilot agent mode", "https://docs.github.com/en/copilot/concepts/agents", "P6-TECH-SUBSTRATE", "4.1", "4", "4", "Euclid", "def-plat", "R1-debt; IDE agent category reference"),
    ("Windsurf cascade flows", "https://docs.windsurf.com/windsurf/cascade", "P6-TECH-SUBSTRATE", "4.1", "3", "3", "Euclid", "def-plat", "R1-debt; competing IDE orchestration; CON: vendor"),
    ("Replit agent architecture blog", "https://blog.replit.com/ai-agents", "P6-TECH-SUBSTRATE", "2.1", "3", "3", "Euclid", "def-plat", "R1-debt; app-builder agent UX"),
    ("Bolt.new agentic app builder", "https://bolt.new/", "P4-MARKETING", "2.1", "3", "2", "Euclid", "def-ha", "R1-debt; compositional UX harness exemplar"),
    ("Devin cognition launch post", "https://www.cognition.ai/blog/introducing-devin", "P5-OPS-PEOPLE", "2.1", "3", "2", "Keter", "def-skep", "R1-debt; hype benchmark; CON: marketing claims vs production"),
    ("SWE-agent academic", "https://arxiv.org/abs/2407.07791", "P7-RESEARCH", "3.2", "5", "5", "Safe", "def-eval", "R1-debt; agent eval rigor anchor"),
    ("AgentBench evaluation", "https://arxiv.org/abs/2308.03688", "P7-RESEARCH", "3.2", "5", "5", "Safe", "def-eval", "R1-debt; multi-environment agent benchmark"),
    ("WebArena realistic web agent eval", "https://webarena.dev/", "P7-RESEARCH", "3.2", "5", "5", "Safe", "def-eval", "R1-debt; web agent evaluation harness"),
    ("OSWorld multimodal agents", "https://os-world.github.io/", "P7-RESEARCH", "3.2", "5", "5", "Keter", "def-eval", "R1-debt; desktop agent eval; CON: lab not ops"),
    # OSINT-CTX (28) — context / PKM / prompt / NLP
    ("Obsidian help — linking your thinking", "https://help.obsidian.md/Linking+notes+and+files/Internal+links", "P1-DATA", "4.1", "4", "4", "Euclid", "def-ctx", "OSINT-CTX; PKM graph linking; PRO: operator-grade recall; CON: not agent-native"),
    ("Obsidian dataview plugin docs", "https://blacksmithgu.github.io/obsidian-dataview/", "P1-DATA", "3.2", "4", "3", "Euclid", "def-ctx", "OSINT-CTX; structured queries over notes"),
    ("Nick Milo LYT kit", "https://www.linkingyourthinking.com/", "P7-RESEARCH", "2.1", "3", "3", "Euclid", "def-ctx", "OSINT-CTX; Linking Your Thinking PKM method"),
    ("Andy Matuschak working notes", "https://notes.andymatuschak.org/", "P7-RESEARCH", "2.1", "5", "4", "Euclid", "def-ctx", "OSINT-CTX; evergreen notes craft; high practitioner signal"),
    ("Zettelkasten method overview", "https://zettelkasten.de/introduction/", "P7-RESEARCH", "2.1", "4", "4", "Euclid", "def-ctx", "OSINT-CTX; atomic note discipline"),
    ("Tiago Forte PARA method", "https://fortelabs.com/blog/para/", "P7-RESEARCH", "2.1", "4", "3", "Euclid", "def-ctx", "OSINT-CTX; action-oriented knowledge organization"),
    ("Excalidraw developer docs", "https://docs.excalidraw.com/", "P4-MARKETING", "4.1", "4", "4", "Euclid", "def-ctx", "OSINT-CTX; visual thinking + whiteboard context"),
    ("Logseq documentation", "https://docs.logseq.com/", "P1-DATA", "4.1", "4", "3", "Euclid", "def-ctx", "OSINT-CTX; outliner PKM alternative to Obsidian"),
    ("Roam Research whitepaper", "https://roamresearch.com/#/app/help/page/Vu1MmjinS", "P1-DATA", "2.1", "3", "3", "Euclid", "def-ctx", "OSINT-CTX; graph-native notes; CON: vendor lock-in history"),
    ("LlamaIndex context engineering", "https://docs.llamaindex.ai/en/stable/optimizing/context/", "P1-DATA", "4.1", "4", "4", "Euclid", "def-ctx", "OSINT-CTX; chunking + retrieval for agents"),
    ("LlamaIndex Knowledge Graph index", "https://docs.llamaindex.ai/en/stable/examples/index_structs/knowledge_graph/", "P1-DATA", "4.1", "4", "4", "Euclid", "def-ctx", "OSINT-CTX; graph RAG; aligns Neo4j strategy"),
    ("LangChain context window management", "https://python.langchain.com/docs/concepts/context/", "P1-DATA", "4.1", "4", "4", "Euclid", "def-ctx", "OSINT-CTX; window budgeting patterns"),
    ("Anthropic prompt engineering overview", "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview", "P7-RESEARCH", "4.1", "5", "5", "Safe", "def-prompt", "OSINT-CTX; prompt craft SSOT from model vendor"),
    ("OpenAI prompt engineering guide", "https://platform.openai.com/docs/guides/prompt-engineering", "P7-RESEARCH", "4.1", "5", "5", "Safe", "def-prompt", "OSINT-CTX; complementary prompt patterns"),
    ("Google prompt engineering whitepaper", "https://www.kaggle.com/whitepaper-prompt-engineering", "P7-RESEARCH", "4.1", "5", "5", "Safe", "def-prompt", "OSINT-CTX; structured prompting taxonomy"),
    ("DAIR prompt report", "https://www.dair-institute.org/blog/prompt-report", "P7-RESEARCH", "3.2", "5", "5", "Safe", "def-prompt", "OSINT-CTX; academic prompt engineering survey"),
    ("MemGPT memory management paper", "https://arxiv.org/abs/2310.08560", "P1-DATA", "3.2", "5", "5", "Safe", "def-ctx", "OSINT-CTX; virtual context paging metaphor"),
    ("Lost in the Middle paper", "https://arxiv.org/abs/2307.03172", "P1-DATA", "3.2", "5", "5", "Safe", "def-ctx", "OSINT-CTX; CON: U-shaped attention degrades mid-context"),
    ("RAG survey 2024", "https://arxiv.org/abs/2402.19473", "P1-DATA", "3.2", "5", "5", "Safe", "def-ctx", "OSINT-CTX; retrieval augmentation state of art"),
    ("GraphRAG Microsoft research", "https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/", "P1-DATA", "4.1", "5", "5", "Euclid", "def-ctx", "OSINT-CTX; graph summaries for private corpora"),
    ("Simon Willison LLM context tags", "https://simonwillison.net/tags/llms/", "P7-RESEARCH", "2.1", "4", "4", "Euclid", "def-ctx", "OSINT-CTX; practitioner public opinion on context"),
    ("Chip Huyen AI engineering book site", "https://www.aiengineering.io/", "P7-RESEARCH", "4.1", "5", "4", "Euclid", "def-ctx", "OSINT-CTX; production context + eval framing"),
    ("NLP context window economics (Epoch)", "https://epoch.ai/data-insights/context-windows", "P2-FINANCE", "4.1", "4", "4", "Euclid", "def-ctx", "OSINT-CTX; token/window growth trends"),
    ("Wikipedia — prompt engineering", "https://en.wikipedia.org/wiki/Prompt_engineering", "P7-RESEARCH", "1.3", "3", "3", "Euclid", "def-prompt", "OSINT-CTX; public baseline definition"),
    ("LlamaHub data loaders", "https://llamahub.ai/", "P1-DATA", "4.1", "4", "4", "Euclid", "def-ctx", "OSINT-CTX; ingestion surface for context pipelines"),
    ("Unstructured.io document ETL", "https://docs.unstructured.io/", "P1-DATA", "4.1", "4", "4", "Euclid", "def-ctx", "OSINT-CTX; doc → context chunking infra"),
    ("Notion AI knowledge base patterns", "https://www.notion.com/help/guides/everything-you-can-do-with-notion-ai", "P4-MARKETING", "4.1", "3", "3", "Euclid", "def-ctx", "OSINT-CTX; mainstream PKM+AI; CON: shallow vs Holistika bar"),
    ("Craft docs PKM", "https://www.craft.do/", "P4-MARKETING", "2.1", "3", "2", "Euclid", "def-ctx", "OSINT-CTX; audience use-case for pretty knowledge UX"),
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
        use: str,
        notes: str,
    ) -> bool:
        key = _norm_url(url)
        if key in seen:
            return False
        seq[0] += 1
        seen.add(key)
        sid = f"SRC-HAC-R2I-{seq[0]:03d}"
        while sid in seen_ids:
            seq[0] += 1
            sid = f"SRC-HAC-R2I-{seq[0]:03d}"
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
                "decision_use": use[:240],
                "notes": notes[:600],
            }
        )
        return True

    for cluster, prong, impact, pattern in VAULT_HARVEST:
        if len(out) >= CORPINT_TARGET:  # noqa: per-call cap; main() slices by deficit
            break
        paths = sorted(REPO_ROOT.glob(pattern))
        for path in paths:
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".md", ".csv", ".yaml", ".yml", ".json"}:
                continue
            url = _ledger_url(path)
            fmt = "dataset" if path.suffix.lower() == ".csv" else (
                "internal_canonical" if "canonical" in path.parts else "report"
            )
            add(
                cluster,
                prong,
                path.stem[:80],
                url,
                fmt,
                "def-vault-orchestration",
                f"R2 vault harvest; {impact}",
            )
            if len(out) >= CORPINT_TARGET:
                break

    # process_list agentic-impact rows
    if PL_PATH.is_file() and len(out) < CORPINT_TARGET:
        keywords = (
            "agent", "research", "mirror", "uat", "mcp", "kirbe", "madeira",
            "intelligence", "compliance", "dataops", "openclaw", "cursor",
        )
        with PL_PATH.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if len(out) >= CORPINT_TARGET:
                    break
                blob = " ".join(row.values()).lower()
                if not any(k in blob for k in keywords):
                    continue
                iid = row.get("item_id", "")
                url = f"{_rel(PL_PATH)}#{iid}"
                add(
                    "corp_vault_proc",
                    "P5-OPS-PEOPLE",
                    (row.get("item_name") or iid)[:80],
                    url,
                    "dataset",
                    "def-process-impact",
                    f"R2 process_list; area={row.get('area','')}; impacted-by orchestration",
                )

    return out[:CORPINT_TARGET]


def _osint_rows(seen: set[str], seen_ids: set[str], seq: list[int]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    fmt_cycle = ("article", "webpage", "report", "book")
    for i, (
        title,
        url,
        prong,
        level,
        rel,
        ext,
        ccl,
        use,
        notes,
    ) in enumerate(OSINT_SOURCES):
        if _norm_url(url) in seen:
            continue
        seq[0] += 1
        seen.add(_norm_url(url))
        cluster = "r1_debt_osint" if "R1-debt" in notes else "osint_ctx"
        sid = f"SRC-HAC-R2E-{seq[0]:03d}"
        while sid in seen_ids:
            seq[0] += 1
            sid = f"SRC-HAC-R2E-{seq[0]:03d}"
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
    r2i_present = sum(1 for r in existing if r.get("source_id", "").startswith("SRC-HAC-R2I-"))
    r2e_present = sum(1 for r in existing if r.get("source_id", "").startswith("SRC-HAC-R2E-"))
    corpint_need = max(0, CORPINT_TARGET - r2i_present)
    osint_need = max(0, OSINT_TARGET - r2e_present)

    seq_c = [r2i_present]
    seq_e = [r2e_present]
    corpint = _corpint_rows(seen, seen_ids, seq_c)[:corpint_need]
    osint = _osint_rows(seen, seen_ids, seq_e)[:osint_need]
    combined = existing + corpint + osint

    with LEDGER_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(combined)

    r2i_total = r2i_present + len(corpint)
    r2e_total = r2e_present + len(osint)
    print(f"Appended to {LEDGER_PATH}")
    print(
        f"  prior={len(existing)} + corpint={len(corpint)} + osint={len(osint)} "
        f"= total={len(combined)} (R2I={r2i_total} R2E={r2e_total})"
    )
    if r2i_total < CORPINT_TARGET or r2e_total < OSINT_TARGET:
        print(
            f"WARN: R2 totals R2I={r2i_total}/{CORPINT_TARGET} "
            f"R2E={r2e_total}/{OSINT_TARGET}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
