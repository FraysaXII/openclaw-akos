---
language: en
status: archived
initiative: 20-kalavai-shadow-llamacpp-trial
report_kind: master-roadmap
program_id: shared
plane: tech
authority: System Owner
last_review: 2026-05-05
---

# Initiative 20 — Kalavai / Shadow llama.cpp trial: DeepSeek-R1-Distill-Llama-70B (Q4)

**Folder:** `docs/wip/planning/20-kalavai-shadow-llamacpp-trial/`
**Status:** **Archived** (2026-05-05) — trial window closed 2026-05-01; endpoint absorbed into the standing GPU-shadow profile via `VLLM_SHADOW_URL` and `KALAVAI_ENDPOINT_URL` (I58 D.2 alias seam).
**Archived by:** Initiative 58 D.1 (Cycle 2 multi-track forward) per [`docs/wip/planning/58-cycle-2-multi-track-forward/reports/d1-archive-i05-i20-2026-05-05.md`](../58-cycle-2-multi-track-forward/reports/d1-archive-i05-i20-2026-05-05.md).
**Original task:** [`task.md`](task.md) (vendor contact: Jean-Jacques Sauvanet, Kalavai / Shadow trial).

## 1. Why this initiative existed

I20 was the **operator-time-boxed** trial of a Kalavai-hosted llama.cpp endpoint serving `DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf`. It pre-dated the standing GPU-shadow profile and existed to:

- Wire `VLLM_SHADOW_URL` to the Kalavai endpoint (`https://deepseek-r1-distill-llama-70b-e405de-shadow-llamacpp.spaces.kalavai.net/v1`).
- Map gateway primary to `vllm-shadow/DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf` in `config/environments/gpu-shadow.json`.
- Run `switch-model.py gpu-shadow` and `browser-smoke.py` against the trial endpoint.
- Capture vendor-reported throughput (~14 tok/s @ 1 user, ~40 tok/s @ 5 concurrent; TTFT 5-10 s) and provide structured feedback to JJ before the trial-end cutoff.

## 2. Why it is archived now

The four checklist items shipped before the **2026-05-01** trial-end cutoff. The remaining `[ ]` line — *"Reply to JJ before 2026-05-01: metrics feedback + go / no-go / follow-up call"* — is operator-side correspondence with the vendor; it is not engineering scope and does not block any AKOS deliverable. The trial endpoint URL itself was preserved in the long-lived `~/.openclaw/.env` block under I58 P0 as `KALAVAI_ENDPOINT_URL`, with I58 D.2 (`runpod_provider.py` alias seam) ensuring that `VLLM_SHADOW_URL` continues to win precedence as the canonical name.

No I20-specific engineering scope remains open. The dashboard previously surfaced I20 as `unknown` because no master-roadmap.md existed in the folder. This one-paragraph archive frontmatter clears the unknown without reopening trial scope.

## 3. Surviving artifacts (governed elsewhere)

- `config/environments/gpu-shadow.env` and `gpu-shadow.json` — live GPU-shadow profile, governed by I22 (provider/model registry) and I58 D.2 (alias seam).
- `~/.openclaw/.env` — long-lived `VLLM_SHADOW_URL` + `KALAVAI_ENDPOINT_URL` block, written under I58 P0.
- [`task.md`](task.md) — original task brief, reference-only.

## 4. Reactivation path (if ever needed)

If a future vendor trial replays this pattern (operator-time-boxed remote endpoint trial), spawn a fresh initiative folder under `docs/wip/planning/<NN>-<vendor>-<slug>/` rather than reopening I20. Per the operator-SQL gate and the `.env` SSOT pattern, the canonical configuration always lives in `config/environments/<profile>.env|json` — never in trial-folder task notes.
