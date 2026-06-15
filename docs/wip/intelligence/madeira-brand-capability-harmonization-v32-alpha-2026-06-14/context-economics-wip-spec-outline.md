---
authored: 2026-06-14
status: wip_outline
control_confidence: Keter
---

# Context economics — WIP spec outline (T0)

> Closes GAP-MBH-01/02. Implementation tranche T2 after operator ratify.

## 1. Prompt assembly layers (static → dynamic)

| Order | Content | Cache posture |
|:---:|:---|:---|
| 1 | System / doctrine slice (mode-aware) | `cache_control` breakpoint 1 |
| 2 | Tool schemas + MCP descriptors | breakpoint 2 |
| 3 | Vault slice / KiRBe retrieval | breakpoint 3 (optional) |
| 4 | User message + tool results | no cache |

## 2. Compaction policy (per MADEIRA_AIC_PER_TASK)

- Max turns before compact: task-class specific
- Compact preserves: decision IDs, source IDs, ratify outcomes
- Drop: redundant tool output (hash-dedupe)

## 3. Postprocessing pipeline (`akos/postprocess.py` — proposed)

1. Citation requirement check (research surfaces)
2. `lint_brand_voice_offline.py` pass
3. PII / secret pattern gate (existing hooks)
4. Optional: truncate for channel (ENVOY adapters)

## 4. Telemetry fields (Langfuse)

- `cache_read_tokens`, `cache_write_tokens`
- `alpha_scenario`, `alpha_cohort` tags
- `substrate_adapter_id` from SUBSTRATE_REGISTRY

## 5. Finops join

- Session cost rolls to FINOPS counterparty via provider ID
- Cache savings reported as **cost avoidance** in dossier narrative

## 6. Verification (T2)

- Unit: prompt assembler ordering tests
- Integration: mock provider cache hit metrics
- UAT: dossier shows cost + cache line

## References

- arXiv 2601.06007 (agentic cache boundaries)
- Prong P-B synthesis
- Infonomics join doc (DG-B)
