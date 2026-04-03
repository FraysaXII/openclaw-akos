# Madeira Model UAT Comparison Matrix

**Date**: 2026-04-03
**Hardware**: NVIDIA RTX 2000 Ada Generation (15GB VRAM), CUDA 12.7, Driver 565.90

## Local GPU Performance

| Model | Size | VRAM Usage | GPU % | Speed | Tool Calling | Admin Escalation |
|-------|------|-----------|-------|-------|-------------|-----------------|
| qwen3:8b (Q4_K_M) | 5.2GB | 7.8GB | 100% | 30 tok/s | Yes (native) | Fails on qwen3:8b -- brainstorms instead of escalating |
| deepseek-r1:14b | 9.0GB | ~9GB | ~100% | 8.3 tok/s | No (Ollama 400 error) | Cannot test -- no tool support |
| qwen3:32b (Q4_K_M) | 20GB | >15GB | Partial | Timeout (>14min) | Theoretically yes | Cannot test -- exceeds VRAM |

## RunPod Deployment Status

| Target | Status | Notes |
|--------|--------|-------|
| Serverless (deepseek-r1-70b, 2x A100) | Template created, endpoint blocked | Account balance below $0.01 minimum |
| Dedicated Pod (deepseek-r1-70b, 2x A100) | Not attempted | Same account balance issue |

## Key Findings

1. **GPU acceleration is active**: Ollama correctly detects and uses the RTX 2000 Ada. qwen3:8b runs at 30 tok/s (100% GPU).
2. **VRAM is the hard limit**: 15GB VRAM comfortably holds 8B models, partially holds 14B, cannot hold 32B.
3. **Tool calling requires model support**: deepseek-r1 distilled models do not support Ollama's native tool-calling API. Only qwen3 and llama3 family models support it.
4. **Admin escalation is model-sensitive**: The qwen3:8b model (small tier, thinking=off) consistently fails the admin-escalation contract. This is mitigated by the semantic intent classifier which provides the deterministic routing layer that the model then follows.
5. **RunPod is the path to SOTA UAT**: To test with deepseek-r1-70b (large tier, reasoning=true, tool-calling via vLLM parser), RunPod account balance needs topping up.

## Recommendations

- For daily dev: keep qwen3:8b (fast, tool-capable, 100% GPU)
- For SOTA UAT: top up RunPod balance and deploy deepseek-r1-70b via serverless endpoint
- For admin escalation: rely on the semantic intent classifier + route tool rather than model size alone
- For medium-tier testing: when RunPod is funded, qwen3:32b via ollama-gpu on a remote A100 server is the ideal middle ground
