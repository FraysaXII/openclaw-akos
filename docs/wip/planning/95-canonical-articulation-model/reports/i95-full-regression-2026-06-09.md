---
report_type: full-regression
intellectual_kind: regression_report
parent_initiative: INIT-OPENCLAW_AKOS-95
sharing_label: internal_only
authored: 2026-06-09
authored_by: Execution seat (Composer) — full back-covering regression
last_review: 2026-06-09
audience: J-OP;J-AIC
language: en
status: closed
verdict: PASS-WITH-FOLLOWUP
base_commit: bab57c2
scopes:
  - scope1_commit_chain_350154c_to_bab57c2
  - scope2_i95_intent_ranked
ratifying_decisions:
  - D-IH-95-L
  - D-IH-95-M
  - D-IH-95-J
  - D-IH-95-K
linked_runbooks:
  - scripts/intent_ranked_regression.py
  - scripts/inter_wave_regression_sweep.py
  - scripts/validate_hlk.py
  - scripts/validate_fk_verb_coverage.py
  - scripts/validate_canonical_articulation.py
  - scripts/validate_research_action.py
verdict_followup_rationale:
  followup_class: deferred-work-with-tracker
  closure_target: OPS-95-2 + OPS-95-3 closed; L3 tranche-5 chartered
  owner: PMO
  tracker_path: docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv
  notes: >-
    All fix-now findings repaired in this commit. PWF carries three named deferrals:
    OPS-95-2 (engagement_model_id backfill; canonical CSV gate), OPS-95-3
    (files-modified.csv historical backfill), and L3 tranche-5 (10 active triples
    without FK bindings; PMO queue row 7 + master-roadmap queue row 6).
---

# I95 full back-covering regression — 2026-06-09

**What this is (plain language).** A two-scope safety sweep over the Canonical Articulation
Model initiative (the "Singularity" — Holistika's enterprise ontology + governed knowledge
graph over the CSV vault). **Scope 1** re-audits everything committed today (13 commits,
`350154c`..`bab57c2`) for contradictions, stale claims, and broken links. **Scope 2** re-checks
the *whole* initiative against what the operator actually cares about, in
intent-criticality order, per the value-ranked regression discipline
([`akos-intent-ranked-regression.mdc`](../../../../../.cursor/rules/akos-intent-ranked-regression.mdc),
ratified `D-IH-88-F`).

**Constraint honored at original cut:** Neo4j was not probed during the first regression pass (operator was mid-F6). **F6 closure addendum (same day):** probe + dual-emit + CQ UAT PASS on instance `6c0d76bf`; `finops_neo4j` row still untouched per D-IH-95-L/M.

**Verdict: PASS-WITH-FOLLOWUP** — no regression that invalidates any of today's ratified
decisions; 10 fix-now findings repaired in this commit; 3 named deferrals with trackers.

---

## 1 — Verdict summary

| Dimension | Result |
|:---|:---|
| **Scope 1 (today's chain)** | 8 findings: 6 fix-now (repaired), 2 known-deferred |
| **Scope 2 (intent-ranked)** | 8 findings: 3 fix-now (repaired), 3 known-deferred, 2 PASS-posture confirmations |
| **New regressions caused today** | **0 doctrine-level**; 7 hygiene-class (CHANGELOG gaps, stale draft-claims, broken links) — all repaired |
| **Decision integrity** | `D-IH-95-K/L/M` each used exactly once in the decision register; no collisions; register↔log parity restored (J/K sections added) |
| **Mechanical gates at base** | `validate_hlk.py` OVERALL PASS · FK→verb 34 bindings PASS · drift none · tax calendar PASS · sweep self-tests PASS |
| **Findings total** | **16** — fix-now 9 · known-deferred 5 · PASS-confirmation 2 · false-positive 0 · escalate 0 |

Disposition enum used: **fix-now / defer-OPS / known-deferred / false-positive / escalate**
(the task's 5-option set; defer-OPS items carry OPS rows, known-deferred items cite existing
trackers/gates).

---

## 2 — Scope 2 ICS sweep order (what was probed, by intent value)

Ranked via `py scripts/intent_ranked_regression.py --rank` (`ICS = 3·intent + 2·time +
2·risk + 1·detection-gap`; `!` = severity-first existence-class override). Probes touching
Neo4j or paid vendors were run in **read-only/doc mode only**.

| # | Surface | ICS | Probe run | Result |
|:--:|:---|:--:|:---|:---|
| 1 | S-06 Legal/fiscal existence artifacts ! | 36 | `validate_finops_tax_calendar.py` | PASS (8 obligations; 8 expected empty-`next_due_at` WARNs — entity not live yet) |
| 2 | S-04 FINOPS commercial substrate ! | 35 | `finops_neo4j` row inspection (read-only) | PASS — notes still "Likely AuraDB free tier"; **unchanged** per D-IH-95-L/M constraint |
| 3 | S-01 Governance SSOT integrity | 34 | `validate_hlk.py` | **OVERALL PASS** (73-row governance registry; collaborator-share `--strict` inside umbrella) |
| 4 | S-05 Release-gate composite | 32 | covered via `pre_commit_fast` at commit (see §6) | PASS |
| 5 | S-12 Schema drift | 32 | `check-drift.py` | PASS — no drift |
| 6 | S-13 HCAM articulation gold layer | 32 | `validate_canonical_articulation.py --matrix` | AMBER (known): 42 entity types, 71% wired; **40/60 triples active (67%)** |
| 7 | S-02 Area-completeness | 31 | `validate_area_completeness.py --matrix` | Data 90% / Finance 94% / People 87% — no regression vs GOV-8 closure baseline |
| 8 | S-03 Structural regression | 29 | `inter_wave_regression_sweep.py --self-test` | PASS (13 probes well-formed) |
| 9 | S-07 Operator interaction surfaces | 27 | doc-mode: PMO sweep §5 operator runbook coherence | PASS after fix-now F-04 (stale draft-decision claims) |
| 10 | S-08 Brand & external-render trail | 26 | n/a this wave (no external-audience artifact shipped today) | SKIP — no J-EXT surface in chain |
| 11 | S-11 Index integrity | 26 | manual CHANGELOG/README/registry parity audit (Scope 1) | FIXED — see F-02/F-03 |
| 12 | S-09 Eval / MADEIRA quality | 24 | not in I95 chain scope | SKIP |
| 13 | S-10 Runtime / deploy health | 24 | `check-drift.py` (shared probe) | PASS |

Intent corpus distilled from: I95 decision log (`D-IH-95-A..M`), master-roadmap lanes,
today's ratification records (`i95-fq2-ratification`, `i95-round2-askquestion2-ratification`,
`l3-trp-030-036-ratification`), and the operator's standing framings — *no spec-only / no
blind all-out*, *mirror must match before close*, *per-triple inline ratify*, *tiered two-plane
governance*, *research bar = tier-specific verification + internal precedent first*, *"watch my
back" = surface cost/tier/risk before I act*, *F6 $0 primary*, *self-hosted escalation default*,
*EIC Open + Startup parallel*.

---

## 3 — Findings: Scope 1 (today's 13-commit chain)

Attribution classes: **new** (caused by today's chain) · **pre-existing** (predates today) ·
**known-deferred** (already tracked + gated).

| ID | Finding | Attribution | Disposition | Action taken |
|:--|:---|:---|:---|:---|
| **F-01** | Register↔log parity gap: `D-IH-95-J` and `D-IH-95-K` have `DECISION_REGISTER.csv` rows but no narrative sections in the initiative decision-log (J's register row even names the decision-log as its log path) | new | **fix-now** | Compact J + K sections inserted in [`decision-log.md`](../decision-log.md) between I and L |
| **F-02** | CHANGELOG gaps: 7 of 13 commits landed without `[Unreleased]` entries (`2d7eeab` L1 EG-2 close, `2802ef8` dual-emit, `35169fc` Hygiene B+C, `ad3e574` FK fix, `68c9dc6` mirror apply, `84e4fed` parity PASS, `142ba58` probe+env heal); the L2/L3 entry still claimed "L1 deferred" after `2d7eeab` closed it | new | **fix-now** | Consolidated back-coverage entry added to [`CHANGELOG.md`](../../../../../CHANGELOG.md); "deferred" claim annotated with same-day close |
| **F-03** | CHANGELOG stale claims: GOV-8 closure + post-GOV-8 entries still said prod mirror apply "PENDING-OPERATOR" after it was APPLIED with parity PASS | new | **fix-now** | Superseded-same-day annotations appended (history preserved, contradiction removed) |
| **F-04** | Stale draft-decision claims: funding radar + research-area synthesis still called `D-IH-95-M` "draft / pending FQ-1" after `bab57c2` ratified it (FQ-1 = D; FQ-4 sequence) | new | **fix-now** | Both docs updated — frontmatter `ratifying_decisions` += `D-IH-95-M`; FQ tables marked closed; "draft rationale" lines corrected |
| **F-05** | Broken repo-root relative links: 16 links used 4 `../` instead of 5 (to `akos/io.py`, `akos/hlk_neo4j.py`, `scripts/sync_hlk_neo4j.py`, `supabase/migrations/*`, `CHANGELOG.md`, keepalive + graph-integration workflows) across 5 reports (free charter, professional charter, credential recovery, e2e cutover charter, L2 state audit) | new | **fix-now** | All 16 repaired; link sweep re-run clean on every touched doc. *Observation (not fixed):* ~130 broken links exist in **historical** CHANGELOG entries (pre-v3.0 path era, renamed assets, deleted rules, business-strategy targets that the L6 re-home lane will move) — historical entries are point-in-time records; retro-rewrites would falsify them. Disposition: **known-deferred / accept-as-historical-record**; L6 lane is the only live consumer |
| **F-06** | Professional charter (deferred-funding appendix) still pointed `backup_artifact_path` + R0 at repo-root staging, contradicting the F6-R0 vault doctrine | new | **fix-now** | Frontmatter + R0 step updated to operator vault path with staging note |
| **F-07** | GOV closure UAT was PASS-WITH-FOLLOWUP pending Neo4j N4 CQ lane | pre-existing | **fix-now** (F6 addendum) | Amended to **PASS** in [`uat-universal-canonical-governance-2026-06-09.md`](uat-universal-canonical-governance-2026-06-09.md) after CQ UAT green |
| **F-08** | Operator `.backup` export at repo root pending F6-R0 vault move | known-deferred | **fix-now** (F6 addendum) | Moved to `%USERPROFILE%\.openclaw\vault\neo4j-backups\` + SHA256 sidecar; repo root clean |

Checks that **PASSED clean** (no finding): Professional-charter supersession markers
(frontmatter `superseded_by` + banner + funding-gate pointer all consistent with F6-primary);
keepalive workflow comment updated to deferred posture at `5ed49b4`; decision-ID uniqueness
(`D-IH-95-K/L/M` once each; `D-IH-95-F` reserved-not-minted documented); master-roadmap GOV
table + queue + blockers consistent with live state; PMO sweep F6-R0..R7 phase labels match the
F6 charter.

---

## 4 — Findings: Scope 2 (initiative-wide, intent-ranked)

| ID | Finding | Attribution | Disposition | Action taken |
|:--|:---|:---|:---|:---|
| **F-11** | **L3 binding coverage gap (missed relation):** 40 active triples vs 34 FK bindings covering 30 distinct triples → **10 active triples have no L3 binding** (TRP-019 policy influence, TRP-022 intelligence-matrix aggregation, TRP-023 channel serving, TRP-024 pattern realization, TRP-025 persona specialization, TRP-026 metrics access, TRP-028 skill→role assignment, TRP-048/049/050 BI-consumer cluster). None are scoped in bundles A/B/C | pre-existing (activated pre-tranche-4; not regressed today) | **defer-OPS-equivalent (lane-tracked)** | Named as **L3 tranche-5** in PMO queue row 7 + master-roadmap queue row 6; per-registry tranche pattern (R2-05) applies; no binding promoted without the usual per-tranche ratify |
| **F-12** | **engagement_model_id forward charter untracked:** `ad3e574` cleared 3 invalid `tmpl_*` FK values; with 4 never-populated rows, **all 7 engagement rows now carry NULL** `engagement_model_id`. The backfill was named only in mirror-apply report prose — no OPS row | new (clearing) + pre-existing (4 empties) | **fix-now (tracker mint)** | **`OPS-95-2`** appended to `OPS_REGISTER.csv` (flagged canonical append): map engagements to `eng_model_*` classes (D-IH-73-D taxonomy) OR ratify column rename; canonical CSV gate before backfill |
| **F-13** | **`files-modified.csv` absent** for I95 — mandatory per [`akos-planning-traceability.mdc`](../../../../../.cursor/rules/akos-planning-traceability.mdc) §"Per-initiative file-changes CSV"; folder created 2026-06-05 (post-rule) | pre-existing | **fix-now (seed) + defer-OPS (backfill)** | 18-column CSV seeded with this commit's rows; **`OPS-95-3`** tracks the ~40-commit historical backfill (precedent: open Research-area backfill OPS row) |
| **F-14** | **New source ledgers — validator wiring:** the 5 ledgers minted today (52-row funding area + F6 + funding-escalation + Professional + Aura-Free) are NOT in any default gate; `validate_research_action.py` defaults to the Wave R+4 ledger only | pre-existing convention | **known-deferred (convention)** | All 5 verified **PASS** against the research-action schema this run (`--source-ledger` mode): 52/3/6/8/8 rows; tier-confidence distributions recorded in §6. Wiring a ledger-manifest mode is a future validator enhancement, not a today-gap |
| **F-15** | **TOPIC_REGISTRY + INTELLIGENCEOPS proposals pending:** research-area appendices A/B propose `topic_neo4j_graph_infrastructure_funding` + 2 IO radar rows; neither is in the canonical CSVs | known-deferred | **known-deferred (operator CSV gate)** | Correct posture per D-IH-95-M constraint ("proposal-only until CSV gate"); surfaced in the PMO sweep so the gate isn't forgotten |
| **F-16** | **Backup retention process not vault-governed:** [`i95-neo4j-backup-retention-process-2026-06-09.md`](i95-neo4j-backup-retention-process-2026-06-09.md) is initiative-side doctrine with no `process_list.csv` row / vault SOP | new | **known-deferred (forward charter)** | Correct SOP-META order: CSV row must precede vault SOP; promote after F6 completes + first restore drill proves the process shape. Named in PMO sweep queue notes |
| **F-17** | **Articulation gold layer AMBER:** enterprise 71% entity coverage / 67% triple activation; 12 orphan entity types (Data 5, Marketing 2, People 2, Tech 1, Operations 1, Reach 1) | known-deferred | **known-deferred** | L4 orphan burn-down lane (R2-06: by-area equal slices, operator-ratified); Semantic Council disposition surface |
| **F-18** | **GOV UAT §4.1's 8 DIM-04 defer-OPS findings** have no dedicated OPS rows | pre-existing | **known-deferred** | Covered by the open Wave-R inter-wave DIM-04 backlog OPS row (14-finding supabase-mirror-missing class); the 8 surfaces are the same class — cited here so the chain is explicit |

PASS-posture confirmations (no action): **two-plane mirror truth** (apply APPLIED; 12/12
row-count parity; emit-contract validator PASS — operator's *mirror-must-match-before-close*
intent honored); **cost/tier guardrails** (F6 charter hard-gate STOP box + credential-recovery
DO-NOT box + radar escalation ladder all surface paid-tier cost before any operator action —
the *watch-my-back* intent).

---

## 5 — Cross-cutting verdicts the task asked for explicitly

| Question | Verdict |
|:---|:---|
| Professional-charter vs F6-primary supersession clean everywhere? | **YES** after F-06 (path) — `superseded_by` frontmatter, top banner, F6 hard gate, radar ladder, keepalive comment, decision log, PMO sweep all agree: F6 $0 primary; Professional `deferred-funding` appendix |
| `D-IH-95-K/L/M` each used once; register↔log parity? | **YES** — no collisions; parity restored via F-01 fix (J/K sections) |
| CHANGELOG coherent? | **YES** after F-02/F-03 — every today-commit now covered; no live contradictions |
| New ledgers validator-checked? | **YES** — all 5 PASS the research-action schema (run evidence §6); default-gate wiring is convention-class (F-14) |
| gitignore / backup posture? | **SAFE** — `*.backup` ignored, file untracked, vault move = operator F6-R0 in progress (F-08) |
| GOV UAT §4.3 consistent with current Neo4j status? | **YES** — §4.3 mirror APPLIED/parity PASS; Neo4j N4 **PASS** after F6 (instance `6c0d76bf`; GOV UAT amended PASS same day) |
| Master-roadmap accuracy? | **YES** — plus queue row 6 now names L3 tranche-5 (F-11) |
| L3 bindings vs registry claims? | **34 bindings / 40 active triples — 10 unbound** (F-11; named tranche-5) |
| New CSVs registry-governed or correctly out-of-scope? | **Correctly out-of-scope** — `CANONICAL_GOVERNANCE_REGISTRY` is the *vault* CSV inventory (all 73 rows under `docs/references/hlk`); wip-planning/wip-intelligence ledgers are research artifacts governed by the research-action discipline instead (F-14) |
| `engagement_model_id` NULL×3 forward charter recorded? | **NOW yes** — OPS-95-2 (F-12); was prose-only |
| `finops_neo4j` caveat? | **Untouched** — notes still free-tier; edit gate intact (S-04 probe) |
| GOV PWF tracker chain integrity? | **Coherent** — PWF reason narrowed to Neo4j N4; operator flip gate recorded (F-07) |
| Orphan AMBER items? | 12 orphan entity types; L4 lane owns them (F-17) |
| `files-modified.csv` — required or N/A? | **Required** (initiative post-dates the rule) → seeded + OPS-95-3 backfill (F-13) |

---

## 6 — Mechanical evidence (reproducible)

```text
py scripts/intent_ranked_regression.py --self-test
  PASS (self-test): 7 tiers, 13 surfaces, ICS_MAX=40, severity-first leads
py scripts/intent_ranked_regression.py --rank
  (13-surface ICS table; S-06=36 ! / S-04=35 ! / S-01=34 / ... — §2 above)

py scripts/validate_hlk.py                       → OVERALL: PASS
py scripts/validate_fk_verb_coverage.py          → PASS: FK->verb L3 - 34 bindings, 17 registry column maps
py scripts/check-drift.py                        → No drift detected
py scripts/validate_finops_tax_calendar.py       → PASS (8 obligations; 8 expected WARNs)
py scripts/inter_wave_regression_sweep.py --self-test → PASS (13 probes)
py scripts/validate_canonical_articulation.py --matrix
  → ENTERPRISE: entity_types=42 wired=30 (71%) | triples active=40/60 (67%) | Zachman=6/6 | AMBER
py scripts/validate_area_completeness.py --matrix
  → Data 90% / Finance 94% / People 87% (no regression vs GOV-8 baseline)

py scripts/validate_research_action.py --source-ledger <each new ledger>
  → funding research area: PASS (52 rows; topics=9; {'Euclid': 1, 'Safe': 51})
  → F6 restore:           PASS (3 rows)   → funding escalation: PASS (6 rows)
  → Professional restore: PASS (8 rows)   → Aura Free recovery: PASS (8 rows; 1 Euclid)

L3 coverage diff (this report §4 F-11):
  registry active=40; L3_FK_BINDINGS=34 tuples over 30 distinct triples
  unbound: TRP-019/022/023/024/025/026/028/048/049/050

Link sweep (12 touched docs incl. this report): 16 broken in pre-existing reports + 6 in this
  report's first draft → 0 after fix (historical-CHANGELOG link-rot excluded per F-05 note)
git check-ignore -v b6d76b10-…backup → matched .gitignore:9 (*.backup)
```

Commit-time gates (`validate_hlk.py`, `verify.py pre_commit_fast`,
`validate_fk_verb_coverage.py`) recorded in the commit message of this report's commit.

---

## 7 — Cross-references

- PMO sweep (updated with this verdict): [`i95-pmo-status-sweep-2026-06-09.md`](i95-pmo-status-sweep-2026-06-09.md)
- Funding ratification: [`i95-fq2-ratification-2026-06-09.md`](i95-fq2-ratification-2026-06-09.md) · decision log: [`decision-log.md`](../decision-log.md)
- F6 restore charter: [`i95-neo4j-free-backup-restore-charter-2026-06-09.md`](i95-neo4j-free-backup-restore-charter-2026-06-09.md) · retention process: [`i95-neo4j-backup-retention-process-2026-06-09.md`](i95-neo4j-backup-retention-process-2026-06-09.md)
- GOV closure UAT: [`uat-universal-canonical-governance-2026-06-09.md`](uat-universal-canonical-governance-2026-06-09.md) — **PASS** (amended 2026-06-09 after Neo4j N4)
- Neo4j CQ UAT: [`i95-neo4j-cq-uat-2026-06-09.md`](i95-neo4j-cq-uat-2026-06-09.md)
- L3 bundles charter: [`i95-l3-parallel-bundles-charter-2026-06-09.md`](i95-l3-parallel-bundles-charter-2026-06-09.md) · TRP-030/036 ratify: [`l3-trp-030-036-ratification-2026-06-09.md`](l3-trp-030-036-ratification-2026-06-09.md)
- Governing rules: [`akos-intent-ranked-regression.mdc`](../../../../../.cursor/rules/akos-intent-ranked-regression.mdc) · [`akos-inter-wave-regression.mdc`](../../../../../.cursor/rules/akos-inter-wave-regression.mdc) · [`akos-planning-traceability.mdc`](../../../../../.cursor/rules/akos-planning-traceability.mdc)
- Prior intent-ranked run (S-13 mint): [`intent-ranked-regression-2026-06-06.md`](intent-ranked-regression-2026-06-06.md)
