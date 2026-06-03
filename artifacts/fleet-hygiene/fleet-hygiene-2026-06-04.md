# Fleet hygiene sweep — fleet-hygiene-2026-06-04

- **Swept at:** 2026-06-03T22:27:18+00:00
- **Totals:** clean=9 drift=4 gap=0 blocked=0 skip=1

| Dimension | Surface | Verdict | Severity | Notes |
|:---|:---|:---|:---|:---|
| FLEET-01-WORKTREE | `boilerplate` | drift | medium | ## i32-akos-mirror-seed \| dirty=12 (M=8 staged=0 ??=4) \|  M app/services/page.tsx;  M components/home/cta-section.tsx; |
| FLEET-02-PUBLISH-DRIFT | `boilerplate` | skip | low | no upstream tracking branch |
| FLEET-01-WORKTREE | `hlk-erp` | drift | medium | ## main...origin/main \| dirty=19 (M=8 staged=0 ??=11) \|  M .gitattributes;  M .github/.akos-bless/contributing.sha256; |
| FLEET-02-PUBLISH-DRIFT | `hlk-erp` | clean | low | in sync with upstream or no upstream |
| FLEET-03-CI-CONTENT | `hlk-erp` | clean | low | ci.yml jobs OK (['lint', 'typecheck', 'audit', 'unit', 'build']) |
| FLEET-01-WORKTREE | `kirbe-platform` | drift | medium | ## i90-p35-kirbe-runbooks...origin/i90-p35-kirbe-runbooks \| dirty=3 (M=3 staged=0 ??=0) \|  M .github/.akos-bless/contr |
| FLEET-02-PUBLISH-DRIFT | `kirbe-platform` | clean | low | in sync with upstream or no upstream |
| FLEET-03-CI-CONTENT | `kirbe-platform` | clean | low | ci.yml jobs OK (['lint', 'typecheck', 'audit', 'unit', 'build']) |
| FLEET-01-WORKTREE | `openclaw-akos` | drift | high | ## main...origin/main \| dirty=10 (M=6 staged=0 ??=4) \|  M .cursor/rules/akos-deploy-health.mdc;  M CHANGELOG.md;  M co |
| FLEET-02-PUBLISH-DRIFT | `openclaw-akos` | clean | low | in sync with upstream or no upstream |
| FLEET-04-STANDING-OPS | `OPS-86-1` | clean | low | I86 cluster coordination - Waves 1-5 nine-sibling burndown \| last_review=2026-05-16 (19d) \| runbook=n/a \| evidence=mi |
| FLEET-04-STANDING-OPS | `OPS-81-1` | clean | low | I81 P1 vault integrity + DQ sprint + P2 layout-migration tranches coordination \| last_review=2026-06-01 (3d) \| runbook |
| FLEET-04-STANDING-OPS | `OPS-86-9` | clean | low | Wave N+: mint paired runbooks for the 4 Quality Fabric specialty canonicals (dat \| last_review=2026-06-01 (3d) \| runbo |
| FLEET-04-STANDING-OPS | `OPS-90-6` | clean | low | Forward KNOWLEDGE_PAIRING vault pointers to I81 P6 (env_tech_dtp_255/256) \| last_review=2026-06-01 (3d) \| runbook=n/a  |
