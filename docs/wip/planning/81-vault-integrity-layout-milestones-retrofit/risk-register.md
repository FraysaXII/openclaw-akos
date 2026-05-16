# I81 — Risk register

Full risk list. Preview in [master-roadmap §7](master-roadmap.md#7-risk-register-preview-full-at-risk-registermd).

| ID | Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---:|:---:|:---|
| **R-IH-81-1** | Retrofit fatigue if continuous mode chosen | M | M | D-IH-81-A defaults to absorbed mode; operator may switch per-phase if cadence shifts |
| **R-IH-81-2** | Per-area register-discipline expertise mis-applied (Tech Lab agent retrofits Marketing SOP without brand voice) | M | M | D-IH-81-C routes retrofits via role_owner with agent assistance; role_owner sign-off mandatory |
| **R-IH-81-3** | Body-vs-addendum split judgement drift across areas | L | M | I80 `SOP-META §"Body and Addendum split"` is the binding contract; retrofit authors cite it per pair |
| **R-IH-81-4** | Net-new SOPs minted during I81 execution skip the paired-file contract | L | M | I80 meta-SOP binding for all new SOPs; I81 reinforces; pairing validator catches |
| **R-IH-81-5** | Cross-references break when SOP bodies are trimmed | L | L | Mechanical jargon-scan + frontmatter validators catch most; per-pair PR review catches rest |
| **R-IH-81-6** | Integrity matrix becomes stale day after P1 — drift returns without ownership | M | M | Assign quarterly reconciliation row to PMO; fold into `validate_hlk` release-gate; record in P9 closure |
| **R-IH-81-7** | Layout migration breaks sibling repo `hlk-erp` without coordinated PR | M | H | Cross-repo schema propagation SOP per tranche; never merge layout wave without consumer-path audit; explicit checklist row per tranche |
| **R-IH-81-8** | Named-milestone migration mid-flight breakage — references go stale during transition window if retrofit phases reach for milestones not yet migrated | M | M | Explicit transition allowlist with hard P3-close empty-allowlist check; P3 ships ahead of P4-P8 so retrofit phases use named milestones natively |
| **R-IH-81-9** | Validator over-strict — false positives on legitimate prose mentions (`I82 P2` in discussion paragraph not intended as cross-ref) block unrelated commits | L | M | Validator scopes only **markdown link targets** + **frontmatter `milestones:` arrays** + **explicit cross-reference paragraphs** (heuristic: in lists or bold-emphasis markers); free prose mentions warn-only with allowlist override |
| **R-IH-81-10** | Closed-initiative frozen-reference policy mis-applied — agents migrate closed roadmaps in well-meaning sweeps, polluting historical record | L | M | D-IH-81-J ratifies policy; validator allowlist mechanically enforces (excludes `<NN-slug>/` paths where `INITIATIVE_REGISTRY.csv` row has `status=closed`); cursor-rule extension codifies for future plan authors |
