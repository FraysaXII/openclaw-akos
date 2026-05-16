---
initiative_id: I87
language: en
last_review: 2026-05-16
---

# I87 — Risk register

| ID | Risk | Likelihood | Impact | Owner | Mitigation | Status |
|:---|:---|:---|:---|:---|:---|:---|
| **R-IH-87-1** | OpenClaw upstream owns gateway-token UX bug and won't fix in I87 timeline | M | M | System Owner | P4 produces workaround SOP entry + files upstream ticket; no in-tree fix attempted | Open |
| **R-IH-87-2** | `OPERATOR_INBOX.md` becomes noisy if escalation threshold N=3 too low under intermittent network flap | M | L | System Owner | P1 ships with operator-tunable `AKOS_HEALTH_ESCALATION_N` env; review noise level at P6 closure UAT; promote N=5 if signal-to-noise < 50% | Open |
| **R-IH-87-3** | Plugin pinning validator (P2) regresses I77 P4.C `validate_brand_voice_register_pinning.py` patterns | L | M | System Owner | P2 follows I77 P4.C wiring verbatim; integration test references both validators sharing the `validate_*_pinning` family contract; release-gate runs both | Open |
| **R-IH-87-4** | Removing `ollama/qwen3:8b` (D-IH-87-C) breaks operator workflows relying on bonjour self-heal | L | L | System Owner | P3 ships rollback one-liner; documented in CHANGELOG; bonjour fallback to vLLM is already implicit per gateway log evidence | Open |
| **R-IH-87-5** | I87 P5 SOP+runbook collides with I77 P4.C voice-validator process_list precedent on operator-review bandwidth | L | L | PMO | I87 P5 process_list row request batches under I86 D-IH-86-C wave boundary; if conflict, defer to Wave 2 boundary | Open |

## Cross-cluster risk reference

I87 R-IH-87-1 (gateway-token upstream block) is flagged in **I86 R-IH-86-5** (upstream-dependency risk in cluster execution) as a potential delay vector for Wave 1 closure. Mitigation in both registers: P4 escalates to workaround SOP entry, never blocks on upstream fix.
