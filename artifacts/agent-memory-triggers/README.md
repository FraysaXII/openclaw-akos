---
language: en
status: active
---

# Agent memory trigger watch outputs

Operator-local outputs from `scripts/agent_memory_trigger_watcher.py` (Initiative 47 P13 item 3).

Files in this directory are gitignored except this README and `MANUAL_FIRE.txt` (operator edits to mark trigger 3).

Regenerate with:

```bash
py scripts/agent_memory_trigger_watcher.py
py scripts/agent_memory_trigger_watcher.py --hard-fail-on-trigger  # CI-mode
```

To mark trigger 3 (compliance ask) as fired, write the audit-ask description to:

```
artifacts/agent-memory-triggers/MANUAL_FIRE.txt
```

ADR reference: `docs/references/hlk/v3.0/Envoy Tech Lab/Neo4j/AGENT_MEMORY_DEFERRED_ADR.md`.
