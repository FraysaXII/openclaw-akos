# I82 — Risk register

Full risk list. Preview in [master-roadmap §8](master-roadmap.md#8-risk-register-preview-full-at-risk-registermd).

| ID | Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---:|:---:|:---|
| **R-IH-82-1** | Doctrine remains aspirational without a live test — first capability surfacing event never happens | M | H | P7 acceptance binds closure to one live external rehearsal **or** explicit waiver narrative recorded in closure decision row. Track `OPS-82-1` as the live-UAT scheduling row |
| **R-IH-82-2** | SCP-Foundation cameo confuses audiences who don't get the reference | M | M | Per Round 9 operator framing — naming is audience-aware multi-register; cameo only for methodology-curious. D-IH-82-C (renamed deferred) close at P3 with audience-translation tables for each register |
| **R-IH-82-3** | Capability inventory drifts from `process_list.csv` over time | H | M | FK to `process_list.csv` `item_id`s; `validate_capability_registry.py` enforces FK resolution; quarterly sync cadence row added to PMO |
| **R-IH-82-4** | Use case archive contains commercially-sensitive customer references | H | H | Default redaction = paraphrase; explicit `redaction_class` enum (none / paraphrase / anonymise); Compliance Officer sign-off per row before external surfacing. D-IH-82-E close at P4 |
| **R-IH-82-5** | Eloquence translation rails diverge from `BRAND_BASELINE_REALITY_MATRIX` over time | L | M | Extension lives **inside** the matrix (§N), not a separate file; drift gate is the existing matrix-drift validator |
