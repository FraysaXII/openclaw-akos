---
status: complete
classification: working
access_level: 5
language: en
register: internal
phase: P2
phase_name: Internal counterparty brief + elicitation plan + source grading
recorded_at: 2026-05-10
---

# P2 — Internal brief / elicitation / source-grade self-checkpoint

## Artefacts produced

| File | Lines (approx.) | Register | Notes |
|:---|:---|:---|:---|
| `counterparty-brief.md` | ~80 | internal EN | Baseline reality, WeBuy domain shape, approach posture, 4 placeholders for the bridge to confirm before Monday. |
| `elicitation-plan.md` | ~70 | internal EN + FR questions | 12 FR questions across Sections A–E (frame / direct / indirect / reverse / closing). Outward-register version ships in P5. |
| `source-grade.csv` | 9 sources + header | internal | Admiralty A–F × 1–6 grading on CDC, mode opératoire, audio briefings, public filings, vendor OSINT, Madrid SME benchmarks, off-repo competitor cost-model inspiration extracts (source identifiers operator-redacted), internal prior-engagement memory. |

## Self-review against template

* SUEZ baseline reality covers stage / sector / geography / sponsor profile / stated + inferred pain / decision-maker shape / urgency / budget / anti-patterns — same shape as `_templates/elicitation-template-customer-sme.md` adapted to enterprise.
* Approach techniques match the SOP-IO_ELICITATION_DISCIPLINE recipe for first-contact + bridge-introduced + enterprise: direct elicitation primary, indirect peer-anchored secondary, reverse-elicitation late, no provocation, no direct interrogation.
* The 4 placeholders in §4 are the only operator-facing TODOs before Monday.
* Source grading is conservative: nothing graded above B/2 except the public filings (A/2). Bridge interview is B/3 pending re-grade post Sunday call.

## Verification

* No external-register leakage check needed — these are internal-register artefacts under `docs/wip/intelligence/`, which is exempt from the brand-baseline-reality drift gate.
* `py scripts/validate_goipoi_register.py` was run after P1 and continues to pass.

## Next

P3 — Estimation discipline (P3a mint, P3b canonical CSV extensions, P3c SUEZ application). This is the largest phase by volume; it produces a reusable Holistika asset (the SOP + Python module + CLI script + worksheet template + tests) before applying it to SUEZ.
