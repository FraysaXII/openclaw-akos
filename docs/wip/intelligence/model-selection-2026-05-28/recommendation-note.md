---
title: Model selection recommendation — Holistika (2026-05-28)
language: en
intellectual_kind: wip_intelligence_synthesis
sharing_label: internal_only
audience: J-OP
authored: 2026-05-28
last_review: 2026-05-28
status: draft
linked_research_sources:
  - docs/wip/intelligence/model-selection-2026-05-28/source-ledger.csv
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
---

# Which AI model should drive Holistika's work?

> Executive summary for the operator. Full lookup table:
> [`model-routing-map.md`](model-routing-map.md). Built under the
> **research-to-decision discipline** (source log + trust scores → synthesis);
> 25 sources in [`source-ledger.csv`](source-ledger.csv).

## One-line answer

**Route by job type:** Composer 2.5 for Cursor execution; Opus for dense
interpretation; dual-tier open-source APIs + RunPod for production agents;
FLUX/Figma/render scripts for visuals — and **never trust a leaderboard
without a skeptic source paired to it.**

---

## Part A — Cursor IDE (your daily driver)

| Model | Plain name | Use when | Skip when |
|:---|:---|:---|:---|
| **Composer 2.5 Fast** | Cheap Cursor coding agent | Multi-file edits, validators, git, CSV work | Dense strategic briefs |
| **Opus 4.x Max** | Expensive thinking model | Judgment, doctrine, messy multi-part input | Routine execution (wastes budget) |
| **Codex / GPT-5.5** | OpenAI terminal worker | Shell/CI automation only | Interpretation (feels "artificial" by design) |

**Session rule:** default Composer; switch to Opus when interpretation *is*
the job. Codex stays off the interpretation lane.

---

## Part B — Open-source / self-hosted LLMs (AKOS / MADEIRA)

Holistika already runs **Ollama, OpenClaw, RunPod, Groq** (see substrate
audit). Extend — don't replace — `config/model-catalog.json`.

| Need | Recommended class | Where it runs |
|:---|:---|:---|
| Cheap high-volume batch | DeepSeek V4 Flash | API or vLLM |
| Hard agentic coding | Kimi K2.6 or DeepSeek V4 Pro | API / large GPU |
| Tool-heavy MCP workflows | Qwen 3.6 Plus | Partner API |
| MIT-licensed self-host | GLM 5.1 | RunPod vLLM |
| Local dev smoke | Ollama (small tier) | Laptop |

**Caveat:** SWE-bench Verified scores are inflated by harness engineering
(see skeptic sources SRC-MS-16/17). Procure only after Holistika eval on
*your* repo tasks.

**Residency (DQ-MS-01, ratified):** SUEZ-class engagements default to
self-host or Holistika-controlled inference; internal work may use OSS APIs;
customer API use requires engagement addendum.

**Origin / messaging (DQ-MS-02, ratified):** law-bound neutrality — no blanket
exclusion of DeepSeek/Kimi for origin; external prose uses capability/residency
register, not geopolitics.

Deep dive: [`prong-ms-open-source-llms-and-local-routing.md`](prong-ms-open-source-llms-and-local-routing.md)

---

## Part C — Image / video / 3D

| Need | Recommended | External-safe? |
|:---|:---|:---|
| Draft concept image | FLUX.1 dev / FLUX.2 klein (12–16 GB VRAM) | Only after brand review |
| Investor/customer delivery | **Figma + render scripts** (PDF/web) | Yes — this is SSOT |
| Video / 3D | Wan 2.2 / Hunyuan3D — **defer** unless engagement requires | Rarely |

Orchestrate with **ComfyUI** on RunPod when GPU budget allows; never
send raw AI images externally without render-trail + brand gate.

Deep dive: [`prong-ms-multimodal-image-video-3d.md`](prong-ms-multimodal-image-video-3d.md)

---

## Confidence (honest)

| Lane | Confidence |
|:---|:---|
| Composer for execution | Medium-high |
| Composer for interpretation | **Under field test** (this KB = Iteration 1) |
| OSS dual-tier near-term | Medium (eval pending; residency + substrate rows ratified) |
| Multimodal draft lane | Medium (GPU hybrid + brand gate ratified DQ-MS-04/05) |

---

## What to read next

| File | Purpose |
|:---|:---|
| [`model-routing-map.md`](model-routing-map.md) | Task → model lookup |
| [`master-synthesis.md`](master-synthesis.md) | Cross-prong rollup |
| [`field-test-note.md`](field-test-note.md) | Composer safety net |
| [`operator-ratification-2026-05-28.md`](operator-ratification-2026-05-28.md) | DQ-MS-01..06 operator verdicts |

## Sources

25 rows in `source-ledger.csv` including skeptical counter-weight
(Independent AI, Particula, VentureBeat/DeepSWE).
