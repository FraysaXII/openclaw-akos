---
language: en
status: active
initiative: INIT-OPENCLAW_AKOS-86
authored: 2026-05-16
last_review: 2026-05-16
role_owner: PMO
---

# I86 — Risk register

| ID | Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---:|:---:|:---|
| R-IH-86-1 | PMO bandwidth collapses under nine parallel sibling contexts | med | high | D-IH-86-B event pulse + wave spotlight facilitation + blocker-overflow only when necessary |
| R-IH-86-2 | Wave spotlight handoff drops narrative between waves | med | med | One-paragraph handoff file per wave close under `reports/` |
| R-IH-86-3 | 14-day quiet floor hides a silently stalled sibling | low | high | OPS_REGISTER aging + OPERATOR_INBOX review |
| R-IH-86-4 | D-IH-86-D cross-check misses a soft dependency | med | med | Explicit §3.8 dep-map read each closure + sibling closure pause records |
| R-IH-86-5 | `_candidates/i86-*.md` redirect stub diverges from folder rename | low | low | Grep for `86-initiative-cluster` on renames |
| R-IH-86-6 | I86 planning churn blocks sibling execution | low | med | I86 commits stay planning-meta + register rows; no vault canonical mints |
