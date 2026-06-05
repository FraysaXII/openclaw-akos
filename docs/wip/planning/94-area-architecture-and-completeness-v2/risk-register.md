---
initiative_id: INIT-OPENCLAW_AKOS-94
language: en
last_review: 2026-06-05
---

# I94 — Risk register

| ID | Risk | L | I | Mitigation | Owner |
|:---|:---|:--:|:--:|:---|:---|
| R-94-1 | v2 model invalidates the Data/Finance closures (re-score drops them below bar) | M | H | Critical-at-L3 mapping designed to preserve both; **P8 regression confirms before any re-grade**; closures only move on explicit decision | CDO/CFO |
| R-94-2 | Drift moves (P4 disciplines, P7 sub-folders) break FK/links across the vault | M | H | Each move = single audited commit + `validate_hlk` after; per-area operator gate; `validate_hlk_vault_links` in matrix | System Owner |
| R-94-3 | Legal/Envoy research-first phases (P5/P6) stall the initiative | M | M | Parallel to P2/P3/P4/P7; closure (P9) requires them but the rest of the sweep does not block on them | PMO |
| R-94-4 | Scope sprawl (8 areas × 16 components × levels × entity) over-commits operator attention | M | M | Staged: model first (P1), then per-area; intent-ranked ICS orders the work; AskQuestion batched per phase | PMO |
| R-94-5 | Operations PMBOK reframe over-engineers (operator's explicit fear) | M | M | PMBOK as orientation not full implementation; "project/service as a tag"; operator-gated at P3 | COO |
| R-94-6 | Legal area mis-articulated (operator low-confidence + wants to "flex") | M | M | Research-first (P6) with source ledger; LegalOps + BI + cross-area-topic-link grounded before mint; operator co-design | Legal Counsel |
| R-94-7 | Entity axis confuses area scoring (entity vs area double-count) | L | M | Entity is a tag on the area, not a second scored unit; Envoy folds UNDER Tech (one scored area) | System Owner |
| R-94-8 | LOGIC_CHANGE_LOG bump implies external methodology-version churn | L | L | Methodology lane is independent of SemVer/HLK-vault lanes per SOP-RELEASE_TAXONOMY_001; internal-only | PMO |
