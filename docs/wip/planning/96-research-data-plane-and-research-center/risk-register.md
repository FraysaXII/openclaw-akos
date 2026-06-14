---
initiative_id: INIT-OPENCLAW_AKOS-96
authored: 2026-06-11
---

# I96 risk register

| ID | Risk | L | I | Mitigation |
|:---|:---|:---:|:---:|:---|
| **R-IH-96-1** | Session work stays in intelligence WIP without planning trace | H | H | P0 files-modified backfill + session-incorporation report |
| **R-IH-96-2** | I83/I92/I96 triple-own ERP Research UI | M | H | I96 spec; I92 implements; I83 owns KiRBe BFF |
| **R-IH-96-3** | KiRBe Neo4j vs AKOS Neo4j merge pressure | M | H | Document D-IH-32-M in cross-plane specs |
| **R-IH-96-4** | D4 delay blocks holistic-agentic indefinitely | H | M | Track A calendar in master-roadmap |
| **R-IH-96-5** | Canonical CSV gate fatigue | M | M | Batch AskQuestion; never silent CSV mint |
| **R-IH-96-6** | Sibling repo deploy drift (hlk-erp) | M | H | I68 deploy-health; Playwright smoke P7 |
| **R-IH-96-7** | Mirror staleness breaks Research Center freshness | H | H | E3 exploration + staleness loop P3 |
| **R-IH-96-8** | Scope creep into full DAMA program | M | H | P10 optional; closure at v1 bar |
| **R-IH-96-9** | `validate_canonical_registry --strict` multi-claim on PEOPLE_DESIGN_PATTERN_REGISTRY | L | M | Known-deferred; do not block I96 P0 |
