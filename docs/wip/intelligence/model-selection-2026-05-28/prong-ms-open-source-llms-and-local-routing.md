---
language: en
status: draft
intellectual_kind: wip_intelligence_synthesis
sharing_label: internal_only
audience: J-OP;J-AIC
prong: MS-OSS
authored: 2026-05-28
last_review: 2026-05-28
linked_research_sources:
  - docs/wip/intelligence/model-selection-2026-05-28/source-ledger.csv
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md
  - config/model-catalog.json
  - config/model-tiers.json
---

# Prong MS-OSS — Open-source and self-hosted language models

## What this prong answers

Which **open-weight / self-hosted** language models Holistika should route to for
which jobs — separate from the Cursor IDE trio (Opus / Composer / Codex) covered
in the original one-page note.

## Ranked options (not a single winner)

| Option | When it fits Holistika | Strengths | Risks / costs |
|:---|:---|:---|:---|
| **A — Dual-tier API (recommended default for near-term)** | Bulk agent work + hard tasks without owning GPUs yet | DeepSeek V4-Flash for volume; Kimi K2.6 or V4-Pro for hard agentic coding; clean MIT on DeepSeek/GLM tiers | API spend + data residency; Modified MIT on Kimi at scale |
| **B — RunPod/vLLM self-host (recommended when GPU path is active)** | MADEIRA / AKOS production inference on models already in `model-catalog.json` | Cost control at scale; aligns with `SUBS-RUN-LLAMA-LLAMAINDEX` + existing RunPod scripts | Ops burden; need harness work not just model swap |
| **C — Local Ollama sandbox (already in production)** | Operator iteration + small-model smoke on laptop | `SUBS-OLLAMA-OLLAMA` in-production per substrate audit; matches `model-tiers.json` small/medium tiers | Not frontier quality; wrong for investor-facing or closure UAT |
| **D — OpenCode / BYOK multi-vendor shell** | Escape Cursor vendor wall while keeping model choice | Surfaces in SRC-MS-10; model-agnostic | Another toolchain to govern; out of scope for AKOS canonical path today |

**Recommendation:** adopt **A now** for exploratory agent lanes + **B** where
RunPod is already billed; keep **C** as the sandbox tier; park **D** as a forward
charter unless operator explicitly wants a second IDE/agent shell.

## Model-class map (May 2026 OSINT consensus)

Sources: SRC-MS-11..15 + SRC-MS-13 Hugging Face hub summary.

| Model class | Best for | Holistika lane | Self-host realistic? |
|:---|:---|:---|:---|
| **DeepSeek V4 Flash** | High-volume agents, cost-sensitive batch | CI agents, doc transforms, bulk CSV helpers | Yes at MoE scale; 2× H100 cited |
| **DeepSeek V4 Pro** | Long-context codebase analysis (1M tokens) | Repo-wide refactors, substrate audits | API-first for most teams |
| **Kimi K2.6** | Multi-agent swarms, long-horizon coding | Complex multi-file initiatives (I86-style) | API/hosted inference more realistic than laptop |
| **Qwen 3.6 Plus** | MCP / tool-calling reliability | MADEIRA tool routes, MCP-heavy workflows | Partner APIs; Apache-licensed smaller variants local |
| **GLM 5.1** | Enterprise MIT + strong SWE-bench Pro class scores | Compliance-friendly self-host candidate | Heavy (744B class); enterprise GPU |
| **Gemma 4 / Phi-4** | Local private coding assistant | Operator laptop offline work | Yes; fits Ollama tier |

## Benchmark skepticism (mandatory counter-weight)

Sources: SRC-MS-16, SRC-MS-17, SRC-MS-25.

- **Do not** pick an open-source model from SWE-bench **Verified** alone.
  Verified scores inflate via solution leakage; harder Pro-style evals collapse
  scores for the same weights.
- **Harness matters more than weights** on multi-file work: same model swings
  ~10 points depending on agent scaffold (Particula, SRC-MS-17).
- Holistika's bar: any model promotion into `SUBSTRATE_REGISTRY.csv` or
  `model-tiers.json` needs **Holistika-owned eval** (pytest + release-gate +
  scenario-0), not leaderboard copy-paste.

## Internal wiring (already exists — extend, don't reinvent)

| Internal surface | What it already says | Action |
|:---|:---|:---|
| `docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md` | Ollama + OpenClaw + Groq + RunPod in-production | Cite as CORPINT anchor SRC-MS-23 |
| `config/model-catalog.json` | DeepSeek R1/V3 + Llama served via vLLM | Extend when V4 weights land; don't fork catalog |
| `config/model-tiers.json` | small/medium/large/sota → prompt variant | Map OSS picks to tier slots before adding new tiers |
| `SUBSTRATE_REGISTRY.csv` | `open-weights-model` + `inference-provider` enums | New rows only via canonical CSV gate |

## Operator ratification (2026-05-28)

See [`operator-ratification-2026-05-28.md`](operator-ratification-2026-05-28.md).

1. **DQ-MS-01 Data residency:** engagement-scoped hybrid — SUEZ-class defaults
   to self-host/controlled inference; internal work may use APIs; engagement
   addendum to relax.
2. **DQ-MS-02 Composer / Kimi lineage:** no Cursor default block; law-bound
   neutrality; internal preference for open-weight token economy; external
   messaging uses capability/residency framing (dual register).
3. **DQ-MS-03 Substrate rows:** `SUBS-DEEPSEEK-DEEPSEEK-V4` +
   `SUBS-MOONSHOT-KIMI-K26` minted at `candidate` in `SUBSTRATE_REGISTRY.csv`.

## Sources used

SRC-MS-10..17, SRC-MS-23, SRC-MS-24, SRC-MS-25 (see `source-ledger.csv`).
