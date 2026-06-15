"""LangGraph OSS evaluation spike (I76 / CO-MBH spike lane).

Minimal research-action loop on a fixed fixture with Langfuse metadata binding
``SUBS-LANGGRAPH-OSS-SELFHOST``. Optional real LangGraph graph when the package
imports; otherwise deterministic mock path for CI and Windows dev boxes.
"""

from akos.langgraph_spike.runner import SpikeRunResult, run_research_action_spike

__all__ = ["SpikeRunResult", "run_research_action_spike"]
