# I90 — Risk register

| ID | Risk | L | I | Mitigation | Status |
|:---|:---|:---:|:---:|:---|:---|
| **R-IH-90-1** | Demoting wrong rule drops governance bar mid-cluster | M | H | P2 gated on `validate_cursor_rule_tiers.py`; 33-rule inventory in ops report | open |
| **R-IH-90-2** | GATE #1 registry mint without operator = canonical violation | L | H | Hard stop at §12 GATE #1; AskQuestion batch | mitigated-at-P0 |
| **R-IH-90-3** | Context window exhaustion on full cluster in one chat | M | M | §14.7 Chat B/C stubs; P3 fleet only after §14 checkboxes | open |
| **R-IH-90-4** | Neo4j unavailable blocks I91 | M | M | Pre-flight note deferral; I91 P0 can charter without live graph | open |
| **R-IH-90-5** | OPS row close while mirror data stale | M | M | Close OPS-86-16/17 as DDL-done; keep OPS-86-32..34 for emit | open |
| **R-IH-90-6** | Two-seat misread (executor plans architecture) | L | M | planner.md `readonly: true`; guide cites D-IH-90-G | open |
| **R-IH-90-7** | Skill/rule pairing validator false positives | M | L | INFO ramp on `validate_rule_skill_pairing.py` | open |
| **R-IH-90-8** | MasterData behind git (mirrors) | H | M | Operator runbook from I86 Wave R+5; do not break-glass MCP DDL | open |
| **R-IH-90-9** | I92 ERP scope creep into I90 P2 | M | M | Initiative split 90/91/92; I92 own master-roadmap | mitigated-at-P0 |
| **R-IH-90-10** | Hook JSON breaks Cursor sessions | L | H | P2f self-test + operator smoke before FAIL ramp | open |
| **R-IH-90-11** | Duplicate INIT rows if GATE re-run | L | H | Grep before append; validator FK | mitigated-at-P0 |
| **R-IH-90-12** | Research legacy migration (OPS-86-26) started early | M | H | Explicit defer; not in P3 queue slot 4 without gate | open |
| **R-IH-90-13** | Plan todo drift vs git | L | L | Update plan YAML after P0 commit | open |
| **R-IH-90-14** | 25 always-on rules → token bloat | H | M | P2 demote to 4 core (D-IH-90-M) | open |
| **R-IH-90-15** | Vercel/deploy checks skipped in Composer session | M | M | `akos-deploy-health` stays glob-scoped to consumer repos | open |
| **R-IH-90-16** | Inter-wave/UAT rules fire on every file | M | L | P2c globs on uat + inter-wave | open |
| **R-IH-90-17** | Cluster coordinator not updated | L | M | I86 notes field bump at P0 commit | open |
