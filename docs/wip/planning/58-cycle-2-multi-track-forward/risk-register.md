---
language: en
status: active
initiative: 58-cycle-2-multi-track-forward
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-05
---

# Initiative 58 — Risk register

| ID | Risk | Likelihood | Severity | Mitigation | Owner |
|:---|:-----|:-----------|:---------|:-----------|:------|
| **R-58-1** | Live cycle (Phase A) exceeds the $50 envelope mid-flight | Low | High | Abort at $40 via [`scripts/endpoint_envelope_alarm.py`](../../../../scripts/endpoint_envelope_alarm.py); partial outcomes recorded in `reports/a*-2026-MM-DD.md`; remaining A.* re-forwards as OPS-58-1. Pre-flight cost estimate is ~$25-30 leaving ~$10 abort buffer. Per D-IH-57-G inheritance | System Owner |
| **R-58-2** | GraphRAG A.3 fails the D-IH-46-E non-additive bar (no single bar hit by ≥3pp / ≥30% / ≥40%) | Medium | Low | NO-SHIP is a closure event per D-IH-58-C, not a failure; I46 P5 stays deferred. Decision logged as `D-IH-46-Decision-P3-2026-MM-DD` in both [I46](../46-neo4j-strategic-posture/decision-log.md) and [I53](../53-graphrag-poc-closure/decision-log.md). I58 still closes. | AI Engineer |
| **R-58-3** | Multi-judge calibration alignment <80% on the live A.1 burn (judge models disagree more than the I52 P3 dispatcher-validation predicted) | Low | Medium | `POL-EVAL-JUDGE-THRESHOLD-{BRAND-VOICE,CITATION,PERSONA-FIT}-V1` recalibration cycle scheduled (per D-IH-57-F inheritance); A.1 partially closes; existing single-judge fallback covers production while recalibration runs | AI Engineer |
| **R-58-4** | I29 P3 Impeccable shape brief disagrees with existing brand SSOT (Impeccable is a polish layer that consumes brand canonical, not a new brand authority) | Low | Medium | Per [`.cursor/skills/impeccable/SKILL.md`](../../../../.cursor/skills/impeccable/SKILL.md): canonical brand wins; bridge files (`PRODUCT.md` + `DESIGN.md`) redirect to brand SSOT, not duplicate it. If Impeccable critique surfaces a brand-canonical conflict, file as a brand-foundation update under I29 P3 closure report. Revert is one bridge-file commit | Brand Manager |
| **R-58-5** | I31 6-axis Holistik Ops doctrine ratification (G-58-3) stalls on founder time | Medium | Medium | Ship 5-axis-compatible artifacts first (P1 localisation + P2 PERSONA_REGISTRY + GOI/POI distance + P3 CHANNEL_TOUCHPOINT_REGISTRY + P4 touchpoint kit + P5 outbound brief + SOURCING_REGISTER); the 6-axis upgrade is a thin doctrine doc + one diagram regeneration. If G-58-3 doesn't fire by E.0, defer the 6-axis edit to a I58.5 follow-up; I58 still closes with B.4 P1–P5 + P7 closeout (P6 deferred) | Founder |
| **R-58-6** | New dimension CSVs (PERSONA_REGISTRY, CHANNEL_TOUCHPOINT_REGISTRY, SOURCING_REGISTER from B.4) miss `compliance.*_mirror` validator coverage at first commit | Low | Medium | Each ships its own `validate_*.py` + `compliance_mirror_emit` row in **the same commit** per `.cursor/rules/akos-governance-remediation.mdc` "compliance.*_mirror" pattern. Revert is the CSV + mirror commit pair atomically. `validate_hlk.py` extension covers all three at the gate | System Owner |
| **R-58-7** | Wave-2 Section 3 already closed by I57 P5; B.4 P2 GOI/POI schema bump (+3 nullable distance columns + 6 row backfill) drifts from the existing 6 rows | Low | Medium | Schema bump only adds nullable columns — can't break existing data. The 6 row backfill is operator-content per D-IH-17 (per-tranche G-58-2 approval). `git revert` of B.4 P2 if mirror sync fails. Validator extends `validate_goipoi_register.py` with the 3 new invariants | System Owner |
| **R-58-8** | Env-var alias seam (D.2) inverts precedence and breaks production gateway (`RUNPOD_ENDPOINT_URL` accidentally wins over `VLLM_RUNPOD_URL`) | Low | High | +1 unit test in `tests/test_runpod_provider.py` asserts `VLLM_*` wins precedence when both names set; deploy to dev-local first; single-line revert in `akos/runpod_provider.py` if precedence inverts. Per D-IH-58-G the alias is fallback only, not a rename | System Owner |
| **R-58-9** | Multi-track parallel commits (Phase A operator-funded + Phase B.* sequential + Phase D parallel) create unmergeable branch state | Medium | Low | Per phase = one commit; rebase often; admin-merge each track before opening next track's PR. If a track stalls, merge it independently and continue on the I58 branch with the remaining tracks. Per `.cursor/rules/akos-governance-remediation.mdc` commit discipline | System Owner |

## Cycle-2 specific risks

These risks are particular to I58 cycle-2 (the first time we run this initiative shape) and either dissolve or stabilize after closure:

- **R-58-cycle2-A** — First initiative to coordinate **five tracks** (A live cycle + B strategy + C KM + D hygiene + E closure). I57 coordinated four buckets; I58 adds Track D explicit hygiene. If a future operator review wants four-track-or-less discipline, I58 sets the precedent that should be revisited at I59 planning. Mitigation: closure UAT explicitly cites D-IH-58-A as the reason; future initiatives can choose differently.
- **R-58-cycle2-B** — First time `~/.openclaw/.env` long-lived block is written by the agent (P0). Per D-IH-58-F the agent writes structure + commented flags + empty placeholders; secret values are operator-pasted. If the operator ever pastes secrets into a chat instead of into the file, AKOS doctrine (`.cursor/rules/akos-mirror-template.mdc`) stipulates secrets stay off-repo. Mitigation: P0 evidence report explicitly documents the empty-placeholder pattern and the operator's paste-only workflow.
- **R-58-cycle2-C** — Track B sequential closure stretches across multiple sittings (~20-25h serial). If one of B.1–B.4 stalls (e.g., I31 P6 6-axis ratification waits on founder per R-58-5), I58 closure UAT still fires per D-IH-58-A but explicitly forwards the unfinished sub-track as a new follow-on (e.g., I58.5). Mitigation: per-phase commit discipline + master-roadmap status flips happen at each B.* completion, so partial progress is captured even if the whole track doesn't finish.

## Risks that are *not* in scope (deliberately deferred)

- **R-OUT-1** (Initiative 27 deferred) — `process_list.csv` per-plane re-architecture trigger (row count > ~3000) is not met (we are at 1100 + 4 from I50 telemetry promotion + ≤5 from B.4 = ~1110). I58 stays well under the trigger.
- **R-OUT-2** (Initiative 26 P4 deferred) — `compliance/<plane>/` physical relocation; trigger is operator decision per the I26 persistent re-eval template. I58 does not touch.
- **R-OUT-3** (Initiative 34 not started) — Multi-tenant skill scoping; D-IH-32-J `tenant_scope='shared'` regex is still load-bearing. I58 does not change tenant scoping.
- **R-OUT-4** — MADEIRA productization roadmap (deferred to I59 candidate per the I30 D-IH-30 scope; "deck announces direction, not GA date").
- **R-OUT-5** — BRAND_FRENCH_PATTERNS.md authoring (deferred per I31 §"out of scope" until first FR external deliverable).
- **R-OUT-6** — Figma backport of I30 deck edits (separate later initiative per the I29 P1 drift-handling rule).
- **R-OUT-7** — OPS-56-1 first advisor reply (external event; I56 stays Open until reality activates).
