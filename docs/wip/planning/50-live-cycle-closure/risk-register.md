---
language: en
status: active
initiative: 50-live-cycle-closure
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 50 — Risk register

| ID | Risk | Likelihood | Impact | Mitigation | Status |
|:---|:-----|:-----------|:-------|:-----------|:-------|
| R-50-1 | 2026-Q2 published prices regress vs 2026-05-01 entries; cost models break | Low | Cost | Monotonic-ordering test (`tests/test_model_prices.py`) fails loudly; operator approves directionally surprising changes | Open |
| R-50-2 | Live dossier emit goes over `MAX_DOSSIER_USD=5` | Low | Cost | Hard-cap raises in `aggregate_dossier_cost_under_cap`; first emit is bounded by design (D-IH-50-B); dry-run cost estimate before live | Open |
| R-50-3 | Tier-B smoke surfaces a real production regression (unexpected) | Med | Quality | Keep cells small (D-IH-50-C); roll back via `AKOS_TIER_B_ENABLED=false`; file as `R-50-3-followup` if it does | Open |
| R-50-4 | Telemetry promotion proposals include hallucinated `route_kind` or other fields | Low | Governance | Operator-merge only (D-IH-50-D); per-row decision-log; no auto-merge | Open |
| R-50-5 | FINOPS counterparty notes drift away from `model-prices.json` reality | Med | DAMA | P2 explicitly aligns FINOPS rows where eval suppliers map; `validate_finops_counterparty_register.py` covers structure | Open |
| R-50-6 | `git push` conflicts with concurrent operator-side commits on `origin/main` | Low | Sched | Pre-push `git fetch + log --oneline origin/main..HEAD` check; operator resolves before push | Open |

