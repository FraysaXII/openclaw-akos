---
language: en
status: active
initiative: 32-holistik-ops-maturation
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder + System Owner
last_review: 2026-04-30
---

# Initiative 32 — Risk register

| ID | Risk | Likelihood | Impact | Mitigation | Rollback |
|:---|:-----|:-----------|:-------|:-----------|:---------|
| **R-32-1** | Validator graph split breaks an existing caller | Medium | High | Backward-compatible CLI is non-negotiable per D-IH-32-F; `tests/test_validate_hlk_dispatcher.py` written first | Revert refactor; mirror DDL is additive |
| **R-32-2** | I31 mirror reseed (still operator-pending) collides with I32 mirror DDL | High | High | **HARD gate per D-IH-32-O**: P0-A6 refuses to start P1 until `probe_compliance_mirror_drift.py --verify` confirms persona=16, channel=10, sourcing=1, goipoi=6 with new schema. | Hold operator apply until I31 catches up. **Only High × High risk.** |
| **R-32-3** | Skill registry seed too coarse / fine | Medium | Low | 5 seed rows; founder review post-P2 | Trim/expand per review |
| **R-32-4** | Topic-axis FK propagation breaks an existing dimension row | Medium | Medium | Pre-flight pass before validator goes strict | Nullable initially; flip strict next initiative |
| **R-32-5** | GOI/POI move breaks links | High | Low | Deprecation alias for one cycle; vault link validator runs in P7 acceptance | Move file back |
| **R-32-6** | Localisation SOP relocation conflicts with Tech ownership of validator | Low | Low | Validator stays in Tech; SOP cross-references | Move SOP back |
| **R-32-7** | Madeira eval harness false-positive trips drift canary | Medium | Medium | Tune threshold; require 2 of 5 canaries before remediation | Increase threshold |
| **R-32-8** | KiRBe team rejects §2 rewrite | Medium | Medium | P0 freeze memo gives notice; P9 architecture audit incorporates feedback | Hold §2 at v0.x; iterate |
| **R-32-9** | ERP team needs more than the 6-artifact bundle | Medium | Low | Bundle is dated; addenda ship as subsequent dated reports | Add follow-up dated reports |
| **R-32-10** | Pre-existing `validate_configs.py` AKOS sandbox-config failures still red | Low | Low (excluded posture per I29 / I30 / I31) | Same exclusion clause in UAT | None needed |
| **R-32-11** | New mirrors push KiRBe sync job over time budget | Low | Medium | Sync only deltas; new mirrors are small (< 50 rows each) | Schedule sync at off-peak |
| **R-32-12** | `tenant_scope` column gets misused before MADEIRA SaaS exists | Low | Medium | Validator enforces `^shared$` as the only valid value | Reject non-`shared` rows |
| **R-32-13** | External repo team rejects EXTERNAL_REPO_CONTRACT.md as too prescriptive | Medium | Medium | Contract is 1 page; first 3 invariants are non-negotiable, the rest are guidance; PR patch lets the team review before merging | Archive contract; iterate; KiRBe and ERP can ship without it but lose REPO_HEALTH_SNAPSHOT visibility |
| **R-32-14** | `snapshot_external_repos.py` runs against a stale local clone (operator hasn't `git pull`-ed) | High | Low | Snapshot script reports `commit_sha_at_snapshot` so staleness is visible; snapshot does not block any phase | Re-run after `git pull` in each clone |
| **R-32-15** | Neo4j extension breaks the existing `:Role` / `:Process` / `:Program` / `:Topic` / `:Document` graph | Low | High | New node labels are isolated; `assert_graph_registry_parity` covers existing labels first; `--dry-run` reports any unexpected delta to existing label counts | Remove the new label MERGEs from sync script; existing graph untouched |
| **R-32-16** | KiRBe team's local Neo4j gets confused with AKOS Neo4j projection | Medium | Medium | D-IH-32-M explicit; P9 KiRBe handoff memo calls this out as item 4 of 5; the two graphs use different `NEO4J_URI` env vars | Documentation only; no system change required |
| **R-32-17** | Boilerplate's embedded Obsidian snapshot at `app/dashboard/applications/kms/obsidian-holistika-main/` gets mistaken for live SSOT | Medium | Medium | D-IH-32-N explicit; reference-note report (P11) is unambiguous; boilerplate row in REPOSITORIES_REGISTRY notes "embedded snapshot, not SSOT" | Documentation only |
| **R-32-18** | `data-ssot.mdc` rule in HLK-ERP keeps misleading new ERP contributors | Medium | Medium | P10 architecture audit memo recommends Q10 supersession (akos-mirror.mdc takes precedence); operator forwards to ERP team | ERP team keeps both rules; agent-side, akos-mirror.mdc is `alwaysApply: true` so it wins on cursor sessions |
| **R-32-19** | Operator's local clone path differs from `c:\Users\Shadow\cd_shadow\root_cd\<repo>` | Low | Low | `snapshot_external_repos.py` reads paths from a config (default to standard locations, override via env `AKOS_EXTERNAL_REPO_ROOTS`) | Configurable; no rollback needed |

## Risk-acceptance posture

R-32-2 is the only High × High risk. P0-A6 includes an explicit hard gate (D-IH-32-O) that blocks P1 from starting until the I31 reseed is verified. R-32-15 is the second-most-impactful (Low × High); P6-A6 graph parity assertion mitigates it before P14 closes.

R-32-1 (Medium × High) is mitigated by writing the dispatcher test before the refactor lands — the test fails first against the current monolithic `validate_hlk.py`, then passes after the refactor. Same TDD posture as I29 P5 deck-from-strategy wiring.

The 7 new risks added in v0.2 (R-32-13..R-32-19) are predominantly Medium × Medium or lower. The cross-repo discipline is additive: external repos that decline the EXTERNAL_REPO_CONTRACT seed lose REPO_HEALTH_SNAPSHOT visibility but suffer no functional break.
