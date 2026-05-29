---
language: en
status: draft
intellectual_kind: wip_intelligence_synthesis
sharing_label: internal_only
audience: J-OP;J-AIC
prong: MS-MM
authored: 2026-05-28
last_review: 2026-05-28
linked_research_sources:
  - docs/wip/intelligence/model-selection-2026-05-28/source-ledger.csv
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VISUAL_PATTERNS.md
  - docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/FIGMA_FILES_REGISTRY.csv
---

# Prong MS-MM — Image, video, and 3D generation models

## What this prong answers

Which **non-text** generative models Holistika should use for brand surfaces,
investor decks, engagement demos, and future product visuals — and how they
compose with existing render scripts (`render_dossier.py`, ComfyUI-style
local workflows).

## Three lanes (do not conflate)

| Lane | Holistika use | Primary stack | Governance |
|:---|:---|:---|:---|
| **Brand / investor** | Deck slides, dossier heroes, ENISA PDFs | Figma SSOT + export scripts; AI only for draft/exploration | External register per `akos-brand-baseline-reality.mdc`; render trail required |
| **Engagement POC** | SUEZ demos, architecture visuals | Mermaid + wireframes; polish tier internal-only (DQ-MS-06) | Customer-facing = translated register + render trail; no raw AI mock SSOT |
| **R&D / sandbox** | Experimentation, RTX-local ComfyUI | Wan 2.2 + Qwen-Image + Hunyuan3D per NVIDIA pattern | Tier 1 WIP only until render parity |

## Image generation — ranked by hardware tier

Sources: SRC-MS-18..20 + SRC-MS-19 Pixazo comparison.

| VRAM available | Recommended model | Why | Holistika default |
|:---|:---|:---|:---|
| **8–12 GB** | SD 3.5 Large or Ernie Image | Ecosystem + multilingual; lowest bar | Operator laptop experiments only |
| **12–16 GB** | FLUX.1 dev / FLUX.2 klein | Photorealism + text-in-image; industry default 2026 | Draft hero images before Figma lock |
| **24 GB+** | HunyuanImage-3.0 or Qwen-Image | Complex/knowledge-heavy prompts | Defer until dedicated GPU workstation |
| **API / no GPU** | FLUX via hosted inference | Avoid local VRAM tax | Acceptable for one-off investor assets if manifest sidecar kept |

**License caution:** FLUX dev weights often need **separate commercial license**
(Pixazo SRC-MS-19). Holistika investor/customer surfaces must record license
class in render manifest (`render_tool` + `license_notes` field — forward-charter
if not in schema yet).

## Video generation

Sources: SRC-MS-21 NVIDIA ComfyUI blog.

| Model | Role | Realistic deployment |
|:---|:---|:---|
| **Wan 2.2** | Text/image-to-video; quality leader for open weights 2026 | RTX 5090-class local or RunPod GPU; ComfyUI workflow nodes |
| **Closed API fallbacks** | Kling / Runway class (not deeply researched this pass) | Use only with render-pending tracker if no OSS path |

Holistika posture: **video is not on the critical path** for Wave R+4 investor
briefs. Default = **defer** unless a specific engagement promises motion assets.

## 3D generation

Sources: SRC-MS-21 (Hunyuan3D 2.1).

| Model | Role | Holistika fit |
|:---|:---|:---|
| **Hunyuan3D 2.1** | Image/text → mesh + PBR materials | Future KiRBe / product viz; not 2026-Q2 priority |
| **Manual / Figma** | Brand 3D-ish assets | Current SSOT for holistikaresearch.com surfaces |

## Orchestration pattern (binding recommendation)

Adopt **ComfyUI-as-orchestrator** for any local multimodal pipeline (SRC-MS-21):

- One workflow graph per asset class (image / video / 3D).
- Check in **workflow JSON + model version pins** under `docs/wip/intelligence/`
  or engagement folder — not ad-hoc GUI-only state.
- Output lands in `artifacts/` with sha256 sidecar (same bar as browser UAT
  audit trail pattern).

## What NOT to do

- Do not ship raw AI images to investors without Figma or brand-token review.
- Do not treat WaveSpeed marketing copy (SRC-MS-22, Euclid confidence) as eval.
- Do not merge multimodal model picks into `model-tiers.json` — that file is
  **LLM chat tiers** only; multimodal belongs in a future
  `MEDIA_GENERATION_REGISTRY.csv` forward-charter.

## Operator ratification (2026-05-28)

See [`operator-ratification-2026-05-28.md`](operator-ratification-2026-05-28.md).

1. **DQ-MS-04 GPU:** hybrid — local Ollama/small models + RunPod for FLUX/video.
2. **DQ-MS-05 Brand gate:** yes for any external audience; draft WIP internal
   exempt (matches external-render discipline).
3. **DQ-MS-06 SUEZ demos:** internal-only; Mermaid + wireframes remain base;
   pursue more polished professional visuals (AI or not) without external SSOT.

## Sources used

SRC-MS-18..22 (see `source-ledger.csv`).
