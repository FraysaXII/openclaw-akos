# Fleet hygiene sweep — fleet-hygiene-2026-06-04

- **Swept at:** 2026-06-04T00:41:15+00:00
- **Totals:** clean=9 drift=3 gap=0 blocked=0 skip=0

| Dimension | Surface | Verdict | Severity | Notes |
|:---|:---|:---|:---|:---|
| FLEET-01-WORKTREE | `boilerplate` | drift | medium | ## i32-akos-mirror-seed...origin/i32-akos-mirror-seed \| dirty=1 (M=1 staged=0 ??=0) \|  M i18n/messages/en.json |
| FLEET-02-PUBLISH-DRIFT | `boilerplate` | clean | low | in sync with upstream or no upstream |
| FLEET-01-WORKTREE | `hlk-erp` | drift | medium | ## i90-hlk-ci-bless-brand-ops...origin/i90-hlk-ci-bless-brand-ops \| dirty=1 (M=1 staged=0 ??=0) \|  M documentation/KIR |
| FLEET-02-PUBLISH-DRIFT | `hlk-erp` | clean | low | in sync with upstream or no upstream |
| FLEET-03-CI-CONTENT | `hlk-erp` | clean | low | ci.yml jobs OK (['lint', 'typecheck', 'audit', 'unit', 'build']) |
| FLEET-01-WORKTREE | `kirbe-platform` | clean | low | ## i90-p35-kirbe-runbooks...origin/i90-p35-kirbe-runbooks |
| FLEET-02-PUBLISH-DRIFT | `kirbe-platform` | clean | low | in sync with upstream or no upstream |
| FLEET-03-CI-CONTENT | `kirbe-platform` | clean | low | ci.yml jobs OK (['lint', 'typecheck', 'audit', 'unit', 'build']) |
| FLEET-01-WORKTREE | `openclaw-akos` | drift | high | ## main...origin/main \| dirty=5 (M=4 staged=0 ??=1) \|  M artifacts/fleet-hygiene/fleet-hygiene-2026-06-04.json;  M art |
| FLEET-02-PUBLISH-DRIFT | `openclaw-akos` | clean | low | in sync with upstream or no upstream |
| FLEET-04-STANDING-OPS | `OPS-81-1` | clean | low | I81 P1 vault integrity + DQ sprint + P2 layout-migration tranches coordination \| last_review=2026-06-01 (3d) \| runbook |
| FLEET-04-STANDING-OPS | `OPS-90-6` | clean | low | Forward KNOWLEDGE_PAIRING vault pointers to I81 P6 (env_tech_dtp_255/256) \| last_review=2026-06-01 (3d) \| runbook=n/a  |
